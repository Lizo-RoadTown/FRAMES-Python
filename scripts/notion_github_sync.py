#!/usr/bin/env python
"""
Sync Notion tasks with GitHub issues:
- Marks Notion tasks Done when the linked GitHub issue is closed.
- Marks Notion tasks In Progress when the linked GitHub issue is open.
- Flags overdue tasks (prints summary).

Environment variables:
  NOTION_API_KEY        (required)
  NOTION_TASKS_DB_ID    (required) Notion database ID for Tasks
  GITHUB_TOKEN          (required) token with repo:read scope (GITHUB_TOKEN works)
  GITHUB_REPO           (optional) defaults to owner/repo from linked issue URL
  DRY_RUN               (optional) if set to "1", no Notion updates are written

Assumed Notion properties (adjust below if different):
  TITLE_PROP   = "Task"          (title)
  STATUS_PROP  = "Status"        (select: Todo, In Progress, Blocked, Done)
  DUE_PROP     = "Due"           (date)
  ISSUE_PROP   = "GitHub Issue URL" (rich_text or url)
"""

from __future__ import annotations

import datetime as dt
import logging
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

import requests
from notion_client import Client

# Notion property names
TITLE_PROP = "Task"
STATUS_PROP = "Status"
DUE_PROP = "Due"
ISSUE_PROP = "GitHub Issue URL"

STATUS_TODO = {"Todo", "In Progress"}
STATUS_DONE = {"Done"}
STATUS_BLOCKED = {"Blocked"}

# GitHub sync defaults
SYNC_LABEL = os.getenv("GITHUB_SYNC_LABEL", "notion-sync")
DEFAULT_REPO = os.getenv("GITHUB_SYNC_REPO")  # owner/repo for creating issues


def setup_logging() -> None:
    level = logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")
    log_file = os.getenv("LOG_FILE")
    if log_file:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logging.getLogger().addHandler(fh)


def env_var(name: str, required: bool = False) -> Optional[str]:
    val = os.getenv(name)
    if required and not val:
        sys.exit(f"Missing required env var: {name}")
    return val


def get_notion_client() -> Client:
    return Client(auth=env_var("NOTION_API_KEY", required=True))


def get_tasks(notion: Client, db_id: str) -> List[Dict]:
    results: List[Dict] = []
    cursor = None
    while True:
        resp = notion.databases.query(
            database_id=db_id,
            start_cursor=cursor,
            page_size=50,
        )
        results.extend(resp.get("results", []))
        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")
    return results


def get_prop(props: Dict, name: str, kind: str):
    prop = props.get(name)
    if not prop:
        return None
    if kind == "title":
        return "".join([t.get("plain_text", "") for t in prop.get("title", [])])
    if kind == "select":
        sel = prop.get("select")
        return sel.get("name") if sel else None
    if kind == "date":
        date = prop.get("date")
        return date.get("start") if date else None
    if kind == "rich_text":
        return "".join([t.get("plain_text", "") for t in prop.get("rich_text", [])])
    if kind == "url":
        return prop.get("url")
    return None


ISSUE_RE = re.compile(r"https?://github\\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/issues/(?P<num>\\d+)")


def parse_issue_ref(text: str) -> Optional[Tuple[str, str, int]]:
    if not text:
        return None
    m = ISSUE_RE.search(text.strip())
    if not m:
        return None
    return m.group("owner"), m.group("repo"), int(m.group("num"))


def fetch_issue(owner: str, repo: str, num: int, token: str) -> Optional[Dict]:
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{num}"
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def list_issues(repo: str, token: str, label: str) -> List[Dict]:
    issues: List[Dict] = []
    page = 1
    while True:
        resp = requests.get(
            f"https://api.github.com/repos/{repo}/issues",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
            params={"state": "all", "labels": label, "page": page, "per_page": 50},
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        issues.extend(batch)
        page += 1
    return issues


def create_issue(repo: str, token: str, title: str, body: str) -> str:
    resp = requests.post(
        f"https://api.github.com/repos/{repo}/issues",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        json={"title": title, "body": body, "labels": [SYNC_LABEL]},
    )
    resp.raise_for_status()
    return resp.json()["html_url"]


def update_status(notion: Client, page_id: str, status: str, dry_run: bool) -> None:
    if dry_run:
        return
    notion.pages.update(page_id=page_id, properties={STATUS_PROP: {"select": {"name": status}}})


def update_issue_link(notion: Client, page_id: str, url: str, dry_run: bool) -> None:
    if dry_run:
        return
    notion.pages.update(page_id=page_id, properties={ISSUE_PROP: {"url": url}})


def create_notion_task(notion: Client, db_id: str, title: str, issue_url: str, dry_run: bool) -> None:
    if dry_run:
        logging.info("DRY RUN: would create Notion task for issue %s", issue_url)
        return
    notion.pages.create(
        parent={"database_id": db_id},
        properties={
            TITLE_PROP: {"title": [{"type": "text", "text": {"content": title}}]},
            STATUS_PROP: {"select": {"name": "Todo"}},
            ISSUE_PROP: {"url": issue_url},
        },
    )


def main() -> None:
    setup_logging()
    notion = get_notion_client()
    tasks_db_id = env_var("NOTION_TASKS_DB_ID", required=True)
    gh_token = env_var("GITHUB_TOKEN", required=True)
    dry_run = env_var("DRY_RUN") == "1"

    tasks = get_tasks(notion, tasks_db_id)
    today = dt.date.today()

    overdue = []
    closed_updates = []
    open_updates = []
    created_issues = []
    created_tasks = []

    # Map of issue URL -> page_id for dedup
    existing_issue_links = {}
    for t in tasks:
        props = t.get("properties", {})
        issue_url = get_prop(props, ISSUE_PROP, "url") or get_prop(props, ISSUE_PROP, "rich_text")
        if issue_url:
            existing_issue_links[issue_url.split("#")[0]] = t["id"]

    # Notion -> GitHub (create issues for tasks without links)
    repo_for_new = DEFAULT_REPO

    for task in tasks:
        props = task.get("properties", {})
        page_id = task["id"]
        title = get_prop(props, TITLE_PROP, "title") or "(untitled)"
        status = get_prop(props, STATUS_PROP, "select")
        due_raw = get_prop(props, DUE_PROP, "date")
        issue_text = get_prop(props, ISSUE_PROP, "url") or get_prop(props, ISSUE_PROP, "rich_text")

        due = None
        if due_raw:
            try:
                due = dt.date.fromisoformat(due_raw.split("T")[0])
            except Exception:
                due = None

        # Overdue check
        if status in STATUS_TODO and due and due < today:
            overdue.append((title, due_raw, issue_text, task.get("url")))

        issue_ref = parse_issue_ref(issue_text) if issue_text else None
        issue_state = None
        if issue_ref:
            owner, repo, num = issue_ref
            issue = fetch_issue(owner, repo, num, gh_token)
            if issue:
                issue_state = issue.get("state")  # open | closed

        # Status adjustments from GitHub
        if issue_state == "closed" and status not in STATUS_DONE:
            closed_updates.append((page_id, title))
            update_status(notion, page_id, "Done", dry_run)
        elif issue_state == "open" and status in STATUS_DONE:
            open_updates.append((page_id, title))
            update_status(notion, page_id, "In Progress", dry_run)

        # Create GitHub issue if missing link and repo configured
        if not issue_ref and repo_for_new and status in STATUS_TODO:
            body = f"Created from Notion task: {task.get('url')}"
            try:
                issue_url = create_issue(repo_for_new, gh_token, title, body)
                created_issues.append((title, issue_url))
                update_issue_link(notion, page_id, issue_url, dry_run)
                logging.info("Created GitHub issue %s for task %s", issue_url, title)
            except Exception as e:
                logging.error("Failed to create issue for task %s: %s", title, e)

    # GitHub -> Notion (import labeled issues without link)
    if DEFAULT_REPO:
        try:
            gh_issues = list_issues(DEFAULT_REPO, gh_token, SYNC_LABEL)
            for issue in gh_issues:
                url = issue.get("html_url")
                if not url:
                    continue
                if url in existing_issue_links:
                    continue
                title = issue.get("title") or "GitHub Issue"
                create_notion_task(notion, tasks_db_id, title, url, dry_run)
                created_tasks.append((title, url))
                logging.info("Created Notion task for GitHub issue %s", url)
        except Exception as e:
            logging.error("Failed to import GitHub issues: %s", e)

    print(f"Checked {len(tasks)} tasks in Notion DB {tasks_db_id}")
    if closed_updates:
        print(f"Marked Done from GitHub closed issues: {len(closed_updates)}")
        for _, t in closed_updates[:5]:
            print(f"  - {t}")
    if open_updates:
        print(f"Reopened (set In Progress) because GitHub issues are open: {len(open_updates)}")
        for _, t in open_updates[:5]:
            print(f"  - {t}")
    if created_issues:
        print(f"Created GitHub issues for Notion tasks: {len(created_issues)}")
        for t, url in created_issues[:5]:
            print(f"  - {t} -> {url}")
    if created_tasks:
        print(f"Created Notion tasks from GitHub issues: {len(created_tasks)}")
        for t, url in created_tasks[:5]:
            print(f"  - {t} -> {url}")
    if overdue:
        print(f"Overdue tasks: {len(overdue)}")
        for t, due, issue, url in overdue[:5]:
            extra = f" (issue {issue})" if issue else ""
            print(f"  - {t} due {due}{extra} -> {url}")
    if dry_run:
        print("Dry run: no Notion updates were written.")


if __name__ == "__main__":
    main()
