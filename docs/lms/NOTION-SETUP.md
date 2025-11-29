# Notion Integration Setup Guide

Set up the FRAMES LMS Notion workspace with automated GitHub syncing.

## Step 1: Create Notion integration (done)
- Integration name: FRAMES
- API key stored in `.env` as `NOTION_API_KEY`

## Step 2: Create parent page
1. Create a page named "FRAMES LMS" in Notion.
2. Share it with the FRAMES integration (Share -> Invite -> FRAMES).
3. Copy the page ID from the URL (the string after the last dash).

## Step 3: Run workspace setup script
```
python scripts/create_notion_workspace.py <YOUR_PAGE_ID>
```
Creates databases: Development Tasks, Technical Decisions, Integration Checklist, Module Library.
Creates page: Project Overview.

## Step 4: Set up GitHub auto-sync
Add GitHub secrets:
- `NOTION_API_KEY`
- `NOTION_PARENT_PAGE_ID` (value from Step 2)

Workflow: `.github/workflows/sync-notion.yml` (runs on main pushes, docs changes, manual dispatch).

## Step 5: Test the integration
- Manual: `python scripts/create_notion_workspace.py <YOUR_PAGE_ID>`
- GitHub: push a docs change and confirm the workflow updates Notion.

## What gets auto-synced
- Documentation in `docs/lms/`
- Database schema changes
- API endpoint changes
- Technical decision logs

## Using the databases
### Development Tasks
Add tasks with Phase, Status, Priority, Estimate, Assignee, Due Date, GitHub Issue, Notes. Use Kanban or timeline views.

### Technical Decisions
Track decisions with status, category, rationale, alternatives, and commit links.

### Integration Checklist
Track frameworks with type, status, priority, repo, bundle size, and notes.

### Module Library
Track modules with type, status, category, estimated minutes, tier, module ID, and description.

## Advanced: linking databases
- Link tasks to decisions via relation properties.
- Link integrations to tasks.
- Link modules to tasks to see progress.

## Troubleshooting
- If auth fails: confirm API key in `.env` and the page is shared with the integration.
- If pages are missing: recopy the page ID and rerun the script.
- If Actions fail: verify GitHub secrets and file paths in the workflow.
- If Notion pages are not updating: check the workflow logs and secret values.

## Next steps
- Populate tasks from the roadmap.
- Add the first decision entry.
- Track integrations (Monaco, Phaser, Three.js).
- Add initial modules (for example, Lab Safety 101) and link them to tasks.

## Resources
- Notion API docs: https://developers.notion.com/
- GitHub Actions docs: https://docs.github.com/en/actions
- FRAMES repo: https://github.com/Lizo-RoadTown/Frames-App

## Support
- Review `scripts/create_notion_workspace.py` for examples.
- Ask for help if additional debugging is needed.
