#!/usr/bin/env python3
"""Agent Gamma automation toolkit.

This script centralises Gamma's responsibilities:
1. Generate module analytics and publish a Notion page.
2. Update the student leaderboard in Notion.
3. Export published Notion modules to JSON for GitHub.
4. Deploy new module JSON files into PostgreSQL.
5. Produce a weekly summary card for team leads.

Each function can be executed individually via sub-commands.
"""

from __future__ import annotations

import argparse
import json
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor
import requests
from dotenv import load_dotenv
import re

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
NOTION_TOKEN = os.getenv("NOTION_API_KEY") or os.getenv("NOTION_TOKEN")
MODULE_DB_ID = (
    os.getenv("NOTION_MODULE_DB_ID")
    or os.getenv("NOTION_MODULE_LIBRARY_DB_ID")
    or os.getenv("NOTION_MODULES_DB_ID")
    or os.getenv("NOTION_MODULE_LIBRARY_ID")
)
DEV_TASKS_DB_ID = os.getenv("NOTION_DEV_TASKS_DB_ID") or os.getenv("NOTION_TASKS_DB_ID")
ANALYTICS_PARENT_ID = os.getenv("NOTION_ANALYTICS_PARENT_ID") or DEV_TASKS_DB_ID or os.getenv("NOTION_PARENT_PAGE_ID")
LEADERBOARD_PARENT_ID = os.getenv("NOTION_LEADERBOARD_PARENT_ID") or os.getenv("NOTION_PARENT_PAGE_ID")
NEW_HIRE_PAGE_ID = os.getenv("NOTION_NEW_HIRE_PAGE_ID")

EXPORT_DIR = Path("modules/exports")
DEPLOY_LOG = Path("agent_coordination/deployment_log.json")

NOTION_VERSION = "2022-06-28"

DB_PROPERTIES_CACHE = None


def require_env(value: Optional[str], name: str):
    if not value:
        raise RuntimeError(f"{name} is required. Set it via environment variable or CLI flag.")
    return value


def notion_headers():
    token = require_env(NOTION_TOKEN, "NOTION_API_KEY/NOTION_TOKEN")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }


def notion_request(method: str, path: str, **kwargs):
    response = requests.request(method, f"https://api.notion.com/v1/{path}", headers=notion_headers(), **kwargs)
    if not response.ok:
        raise RuntimeError(f"Notion API error ({response.status_code}): {response.text}")
    return response.json()


def get_db_properties():
    global DB_PROPERTIES_CACHE
    if DB_PROPERTIES_CACHE is None:
        database_id = require_env(MODULE_DB_ID, "NOTION_MODULE_DB_ID/NOTION_MODULE_LIBRARY_DB_ID")
        data = notion_request("get", f"databases/{database_id}")
        DB_PROPERTIES_CACHE = data.get("properties", {})
    return DB_PROPERTIES_CACHE


def db_has_property(name: str) -> bool:
    props = get_db_properties()
    return name in props


def postgres_cursor():
    url = require_env(DATABASE_URL, "DATABASE_URL")
    conn = psycopg2.connect(url)
    return conn, conn.cursor(cursor_factory=RealDictCursor)


# ---------------------------------------------------------------------------
# Task 1: Analytics
# ---------------------------------------------------------------------------


def fetch_module_metrics():
    conn, cur = postgres_cursor()
    query = """
        SELECT
            m.id as module_pk,
            m.module_id,
            m.title,
            COALESCE(m.estimated_minutes, 0) AS estimated_minutes,
            COUNT(DISTINCT mp.student_id) FILTER (WHERE mp.status IS NOT NULL) AS students_started,
            COUNT(DISTINCT mp.student_id) FILTER (WHERE mp.status = 'completed') AS students_completed,
            COUNT(DISTINCT mp.student_id) FILTER (WHERE mp.status = 'abandoned') AS students_abandoned,
            AVG(NULLIF(mp.total_time_seconds, 0)) AS avg_duration_seconds
        FROM modules m
        LEFT JOIN module_progress mp ON mp.module_id = m.id
        WHERE m.status = 'published'
        GROUP BY m.id
        ORDER BY students_started DESC, m.title ASC;
    """
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def build_insights(rows: List[Dict]) -> List[Dict]:
    insights = []
    for row in rows:
        started = row["students_started"] or 0
        completed = row["students_completed"] or 0
        estimated = row["estimated_minutes"] or 0
        avg_minutes = (row["avg_duration_seconds"] or 0) / 60 if row["avg_duration_seconds"] else None

        completion_rate = (completed / started * 100) if started else 0

        if started and completion_rate < 50:
            insights.append(
                {
                    "module": row["title"],
                    "issue": "Low completion rate",
                    "metric": f"{completion_rate:.1f}%",
                    "recommendation": "Review content length or complexity; consider splitting sections.",
                    "severity": "high",
                }
            )

        if avg_minutes and estimated:
            ratio = avg_minutes / estimated
            if ratio > 1.5:
                insights.append(
                    {
                        "module": row["title"],
                        "issue": "Students spending longer than estimated",
                        "metric": f"{avg_minutes:.0f} min vs {estimated} min estimate",
                        "recommendation": "Update the estimate or streamline dense sections.",
                        "severity": "medium",
                    }
                )
            elif ratio < 0.5:
                insights.append(
                    {
                        "module": row["title"],
                        "issue": "Completing faster than estimated",
                        "metric": f"{avg_minutes:.0f} min vs {estimated} min estimate",
                        "recommendation": "Add depth or reduce the published estimate.",
                        "severity": "low",
                    }
                )

        if completion_rate > 90 and started >= 5:
            insights.append(
                {
                    "module": row["title"],
                    "issue": "Excellent completion rate",
                    "metric": f"{completion_rate:.1f}%",
                    "recommendation": "Use as reference for tone and pacing.",
                    "severity": "success",
                }
            )
    return insights


def publish_analytics_page(rows: List[Dict], insights: List[Dict], parent_id: str):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    children = [
        {
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": f"📊 Analytics generated {timestamp}"}}],
                "icon": {"emoji": "📈"},
                "color": "blue_background",
            },
        },
        {"type": "divider", "divider": {}},
    ]

    severity_order = ["high", "medium", "low", "success"]
    severity_emoji = {"high": "🚨", "medium": "⚠️", "low": "ℹ️", "success": "✅"}
    severity_color = {"high": "red", "medium": "yellow", "low": "gray", "success": "green"}

    for severity in severity_order:
        matches = [insight for insight in insights if insight["severity"] == severity]
        if not matches:
            continue
        children.append(
            {
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": f"{severity_emoji[severity]} {severity.title()} Priority"}}],
                    "color": severity_color[severity],
                },
            }
        )
        for insight in matches:
            children.append(
                {
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {"type": "text", "text": {"content": f"{insight['module']}\n", "bold": True}},
                            {"type": "text", "text": {"content": f"{insight['issue']}: {insight['metric']}\n"}},
                            {"type": "text", "text": {"content": insight["recommendation"], "italic": True}},
                        ],
                        "icon": {"emoji": severity_emoji[severity]},
                        "color": f"{severity_color[severity]}_background",
                    },
                }
            )

    summary_table_rows = [
        {
            "type": "table_row",
            "table_row": {
                "cells": [
                    [{"type": "text", "text": {"content": "Module"}}],
                    [{"type": "text", "text": {"content": "Started"}}],
                    [{"type": "text", "text": {"content": "Completed"}}],
                    [{"type": "text", "text": {"content": "Completion %"}}],
                    [{"type": "text", "text": {"content": "Est. mins"}}],
                    [{"type": "text", "text": {"content": "Avg mins"}}],
                ]
            },
        }
    ]

    for row in rows[:25]:
        started = row["students_started"] or 0
        completed = row["students_completed"] or 0
        completion_rate = (completed / started * 100) if started else 0.0
        avg_minutes = (row["avg_duration_seconds"] or 0) / 60 if row["avg_duration_seconds"] else 0
        summary_table_rows.append(
            {
                "type": "table_row",
                "table_row": {
                    "cells": [
                        [{"type": "text", "text": {"content": row["title"]}}],
                        [{"type": "text", "text": {"content": str(started)}}],
                        [{"type": "text", "text": {"content": str(completed)}}],
                        [{"type": "text", "text": {"content": f"{completion_rate:.1f}%"}}],
                        [{"type": "text", "text": {"content": str(row['estimated_minutes'])}}],
                        [{"type": "text", "text": {"content": f"{avg_minutes:.1f}"}}],
                    ]
                },
            }
        )

    children.extend(
        [
            {"type": "divider", "divider": {}},
            {
                "type": "table",
                "table": {
                    "table_width": 6,
                    "has_column_header": True,
                    "has_row_header": False,
                    "children": summary_table_rows,
                },
            },
        ]
    )

    notion_request(
        "post",
        "pages",
        json={
            "parent": {"database_id": parent_id} if parent_id else {"page_id": require_env(ANALYTICS_PARENT_ID, "Analytics parent")},
            "icon": {"emoji": "📊"},
            "properties": {"Name": {"title": [{"type": "text", "text": {"content": f"📊 Module Analytics - {datetime.utcnow().strftime('%Y-%m-%d')}"}}]}},
            "children": children,
        },
    )


# ---------------------------------------------------------------------------
# Task 2: Leaderboard
# ---------------------------------------------------------------------------


def fetch_student_progress(limit: int = 20):
    conn, cur = postgres_cursor()
    query = """
        WITH published AS (
            SELECT COUNT(*) AS total FROM modules WHERE status = 'published'
        )
        SELECT
            s.id,
            s.name,
            s.team_id,
            s.expertise_area,
            COUNT(DISTINCT CASE WHEN mp.status = 'completed' THEN mp.module_id END) AS modules_completed,
            COALESCE(MAX(published.total), 0) AS total_modules
        FROM students s
        LEFT JOIN module_progress mp ON mp.student_id = s.id
        CROSS JOIN published
        WHERE COALESCE(s.active, TRUE)
        GROUP BY s.id, s.name, s.team_id, s.expertise_area, published.total
        ORDER BY modules_completed DESC, s.name ASC
        LIMIT %s;
    """
    cur.execute(query, (limit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def publish_leaderboard(rows: List[Dict], parent_id: Optional[str]):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    table_rows = [
        {
            "type": "table_row",
            "table_row": {
                "cells": [
                    [{"type": "text", "text": {"content": "Rank"}}],
                    [{"type": "text", "text": {"content": "Student"}}],
                    [{"type": "text", "text": {"content": "Team"}}],
                    [{"type": "text", "text": {"content": "Completed"}}],
                    [{"type": "text", "text": {"content": "% Done"}}],
                    [{"type": "text", "text": {"content": "Updated"}}],
                ]
            },
        }
    ]

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for idx, row in enumerate(rows, start=1):
        total = row["total_modules"] or 0
        pct = (row["modules_completed"] / total * 100) if total else 0
        table_rows.append(
            {
                "type": "table_row",
                "table_row": {
                    "cells": [
                        [{"type": "text", "text": {"content": medals.get(idx, str(idx))}}],
                        [{"type": "text", "text": {"content": row["name"] or "N/A"}}],
                        [{"type": "text", "text": {"content": row["team_id"] or "—"}}],
                        [{"type": "text", "text": {"content": str(row["modules_completed"])}}],
                        [{"type": "text", "text": {"content": f"{pct:.1f}%"}},],
                        [{"type": "text", "text": {"content": timestamp}}],
                    ]
                },
            }
        )

    notion_request(
        "post",
        "pages",
        json={
            "parent": {"page_id": require_env(parent_id, "Leaderboard parent page")},
            "icon": {"emoji": "🚀"},
            "properties": {"title": {"title": [{"type": "text", "text": {"content": "🚀 Module Completion Leaderboard"}}]}},
            "children": [
                {
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"Top performers across CADENCE onboarding modules. Updated {timestamp}."
                                },
                            }
                        ],
                        "icon": {"emoji": "📣"},
                        "color": "blue_background",
                    },
                },
                {"type": "divider", "divider": {}},
                {"type": "table", "table": {"table_width": 6, "has_column_header": True, "children": table_rows}},
            ],
        },
    )


# ---------------------------------------------------------------------------
# Task 3: Export Notion modules
# ---------------------------------------------------------------------------


def fetch_published_notions(status_property: str = "Status"):
    database_id = require_env(MODULE_DB_ID, "NOTION_MODULE_DB_ID/NOTION_MODULE_LIBRARY_DB_ID")
    payload = {
        "filter": {
            "property": status_property,
            "select": {"equals": "Published"},
        }
    }
    results = []
    while True:
        data = notion_request("post", f"databases/{database_id}/query", json=payload)
        results.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        payload["start_cursor"] = data["next_cursor"]
    return results


def collect_blocks(page_id: str) -> List[Dict]:
    blocks = []
    cursor = None
    while True:
        params = {"page_size": 100}
        if cursor:
            params["start_cursor"] = cursor
        data = notion_request("get", f"blocks/{page_id}/children", params=params)
        blocks.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data["next_cursor"]
    return blocks


def notion_rich_text_to_plain(block):
    if isinstance(block, list):
        items = block
    elif isinstance(block, dict):
        items = block.get("rich_text", [])
    else:
        items = []
    lines = []
    for item in items:
        text = item.get("plain_text") or item.get("text", {}).get("content", "")
        lines.append(text)
    return "".join(lines).strip()


def convert_blocks_to_sections(blocks: List[Dict]) -> List[Dict]:
    sections = []
    current = {"heading": "Overview", "content_blocks": []}
    for block in blocks:
        block_type = block["type"]
        if block_type.startswith("heading_"):
            if current["content_blocks"]:
                sections.append(current)
            current = {
                "heading": notion_rich_text_to_plain(block[block_type]) or "Untitled Section",
                "content_blocks": [],
            }
        else:
            current["content_blocks"].append(block)
    if current["content_blocks"]:
        sections.append(current)
    return sections


def export_modules_from_notion():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    pages = fetch_published_notions()
    if not pages:
        print("No Notion modules require export.")
        return

    exported = []
    for page in pages:
        props = page.get("properties", {})
        title_prop = props.get("Name") or props.get("Title") or {}
        title = notion_rich_text_to_plain(title_prop.get("title", [])) if isinstance(title_prop, dict) else "Untitled"
        slug = slugify(title)
        status_prop = props.get("Status", {})

        blocks = collect_blocks(page["id"])
        sections = convert_blocks_to_sections(blocks)

        module_record = {
            "module_id": page.get("id"),
            "title": title,
            "slug": slug,
            "description": notion_rich_text_to_plain(props.get("Description", {}).get("rich_text", [])),
            "category": props.get("Category", {}).get("select", {}).get("name"),
            "difficulty": props.get("Difficulty", {}).get("select", {}).get("name"),
            "estimated_minutes": props.get("Estimated Minutes", {}).get("number"),
            "target_audience": props.get("Target Audience", {}).get("select", {}).get("name"),
            "status": status_prop.get("select", {}).get("name") if isinstance(status_prop, dict) else None,
            "tags": [tag["name"] for tag in props.get("Tags", {}).get("multi_select", [])],
            "sections": sections,
            "notion_page_id": page["id"],
            "fetched_at": datetime.utcnow().isoformat(),
        }
        output_file = EXPORT_DIR / f"{slug}.json"
        with output_file.open("w", encoding="utf-8") as handle:
            json.dump(module_record, handle, indent=2, ensure_ascii=False)
        exported.append((page["id"], title, output_file))
        print(f"Exported {title} -> {output_file}")

        # Update Notion properties if available
        props_update = {}
        if db_has_property("GitHub Sync"):
            props_update["GitHub Sync"] = {"select": {"name": "Exported"}}
        if db_has_property("GitHub File"):
            props_update["GitHub File"] = {"url": f"modules/exports/{output_file.name}"}
        if props_update:
            try:
                notion_request(
                    "patch",
                    f"pages/{page['id']}",
                    json={"properties": props_update},
                )
            except RuntimeError as exc:
                print(f"Warning: failed to update Notion page {title}: {exc}")

    print(f"Exported {len(exported)} modules.")


# ---------------------------------------------------------------------------
# Task 4: Deploy modules to PostgreSQL
# ---------------------------------------------------------------------------


def read_existing_sources(cur) -> set:
    cur.execute("SELECT content_source FROM modules WHERE content_source IS NOT NULL")
    return {row["content_source"] for row in cur.fetchall() if row["content_source"]}


def deploy_modules_to_db():
    if not EXPORT_DIR.exists():
        print("No exports directory found.")
        return

    files = sorted(EXPORT_DIR.glob("*.json"))
    if not files:
        print("No module JSON files detected.")
        return

    conn, cur = postgres_cursor()
    existing_sources = read_existing_sources(cur)
    deployed = []

    for path in files:
        if path.name in existing_sources:
            continue

        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)

        module_id = data.get("module_id") or str(uuid.uuid4())
        now = datetime.utcnow()

        cur.execute(
            """
            INSERT INTO modules
            (module_id, title, description, category, estimated_minutes, status, target_audience,
             tags, created_at, updated_at, published_at, content_source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, to_json(%s::text[]), %s, %s, %s, %s)
            RETURNING id;
            """,
            (
                module_id,
                data.get("title"),
                data.get("description"),
                data.get("category"),
                data.get("estimated_minutes"),
                data.get("status", "published"),
                data.get("target_audience"),
                data.get("tags", []),
                now,
                now,
                now,
                path.name,
            ),
        )
        module_pk = cur.fetchone()["id"]

        for index, section in enumerate(data.get("sections", []), start=1):
            cur.execute(
                """
                INSERT INTO module_sections (module_id, section_number, section_type, title, content, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    module_pk,
                    index,
                    "notion_blocks",
                    section.get("heading"),
                    json.dumps(section, ensure_ascii=False),
                    now,
                ),
            )

        deployed.append({"module_id": module_id, "title": data.get("title"), "source_file": path.name, "timestamp": now.isoformat()})

    if deployed:
        conn.commit()
        DEPLOY_LOG.parent.mkdir(parents=True, exist_ok=True)
        existing_log = []
        if DEPLOY_LOG.exists():
            with DEPLOY_LOG.open(encoding="utf-8") as handle:
                existing_log = json.load(handle)
        existing_log.extend(deployed)
        with DEPLOY_LOG.open("w", encoding="utf-8") as handle:
            json.dump(existing_log, handle, indent=2)
        print(f"Deployed {len(deployed)} modules and updated deployment log.")
    else:
        print("No new modules required deployment.")

    cur.close()
    conn.close()


# ---------------------------------------------------------------------------
# Task 5: Weekly report
# ---------------------------------------------------------------------------


def generate_weekly_report(parent_id: Optional[str]):
    conn, cur = postgres_cursor()
    one_week_ago = datetime.utcnow() - timedelta(days=7)

    cur.execute("SELECT COUNT(*) AS total FROM modules WHERE status = 'published'")
    total_modules = cur.fetchone()["total"]

    cur.execute("SELECT COUNT(*) AS recent FROM modules WHERE created_at >= %s AND status = 'published'", (one_week_ago,))
    new_this_week = cur.fetchone()["recent"]

    cur.execute(
        """
        SELECT AVG(completion_pct) AS average_completion FROM (
            SELECT
                COUNT(DISTINCT CASE WHEN status = 'completed' THEN student_id END)::float /
                NULLIF(COUNT(DISTINCT student_id), 0) * 100 AS completion_pct
            FROM module_progress
            GROUP BY module_id
        ) metrics
        """
    )
    avg_completion = cur.fetchone()["average_completion"] or 0.0

    cur.execute(
        """
        SELECT title, created_at
        FROM modules
        WHERE created_at >= %s
        ORDER BY created_at DESC
        LIMIT 5
        """,
        (one_week_ago,),
    )
    recent_modules = cur.fetchall()

    cur.close()
    conn.close()

    children = [
        {"type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": "📌 Highlights"}}]}},
        {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"Total modules published: {total_modules}"}}]}},
        {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"New modules this week: {new_this_week}"}}]}},
        {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": f"Average completion rate: {avg_completion:.1f}%"}}, ]}},
        {"type": "divider", "divider": {}},
        {"type": "heading_3", "heading_3": {"rich_text": [{"type": "text", "text": {"content": "🆕 Newly published modules"}}]}},
    ]

    if recent_modules:
        for module in recent_modules:
            children.append(
                {
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"{module['title']} — {module['created_at'].strftime('%Y-%m-%d') if isinstance(module['created_at'], datetime) else module['created_at']}"
                                },
                                "annotations": {"bold": True},
                            }
                        ]
                    },
                }
            )
    else:
        children.append(
            {"type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "No new modules this week."}}]}}
        )

    notion_request(
        "post",
        "pages",
        json={
            "parent": {"database_id": require_env(parent_id, "Weekly report destination")},
            "icon": {"emoji": "🛰️"},
            "properties": {"Name": {"title": [{"type": "text", "text": {"content": f"🛰️ Weekly Lead Report - {datetime.utcnow().strftime('%Y-%m-%d')}"}}]}},
            "children": children,
        },
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def slugify(value: str) -> str:
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", value.lower())).strip("-")


def main():
    parser = argparse.ArgumentParser(description="Agent Gamma task runner")
    subparsers = parser.add_subparsers(dest="command")

    parser_analytics = subparsers.add_parser("analytics", help="Build module analytics and publish to Notion")
    parser_analytics.add_argument("--parent-id", help="Override Notion parent (database or page) for analytics.")

    parser_leaderboard = subparsers.add_parser("leaderboard", help="Publish leaderboard page")
    parser_leaderboard.add_argument("--parent-id", help="Parent page for leaderboard table.")

    subparsers.add_parser("export-modules", help="Export published Notion modules to JSON")
    subparsers.add_parser("deploy-modules", help="Deploy module JSON files to PostgreSQL")

    parser_report = subparsers.add_parser("weekly-report", help="Create weekly lead summary in Notion")
    parser_report.add_argument("--parent-id", help="Parent database for the weekly report entries.")

    args = parser.parse_args()

    if args.command == "analytics":
        rows = fetch_module_metrics()
        insights = build_insights(rows)
        for insight in insights:
            print(f"[{insight['severity']}] {insight['module']}: {insight['issue']} ({insight['metric']})")
        if args.parent_id or ANALYTICS_PARENT_ID:
            publish_analytics_page(rows, insights, args.parent_id or ANALYTICS_PARENT_ID)
        else:
            print("Analytics parent not configured; skipping Notion publish.")
    elif args.command == "leaderboard":
        rows = fetch_student_progress()
        if args.parent_id or LEADERBOARD_PARENT_ID:
            publish_leaderboard(rows, args.parent_id or LEADERBOARD_PARENT_ID)
        else:
            print("Leaderboard parent not configured; printing to console.")
            for idx, row in enumerate(rows, start=1):
                total = row['total_modules'] or 0
                pct = (row['modules_completed'] / total * 100) if total else 0
                print(f"{idx}. {row['name']} - {row['modules_completed']} modules ({pct:.1f}%)")
    elif args.command == "export-modules":
        export_modules_from_notion()
    elif args.command == "deploy-modules":
        deploy_modules_to_db()
    elif args.command == "weekly-report":
        parent = args.parent_id or DEV_TASKS_DB_ID
        generate_weekly_report(parent)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
