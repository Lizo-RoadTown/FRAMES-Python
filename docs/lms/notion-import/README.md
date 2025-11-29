# FRAMES LMS - Notion Import Guide

Created: November 26, 2025
Purpose: Documentation bundle for importing into the Notion workspace.

## What is in this folder
Six markdown documents ready to import:
1. 01-PROJECT-OVERVIEW.md
2. 02-MODULE-TYPE-SPECIFICATIONS.md
3. 03-DATABASE-SCHEMA.md
4. 04-DEVELOPMENT-ROADMAP.md
5. 05-INTEGRATION-CHECKLIST.md
6. 06-TECHNICAL-DECISIONS.md

## How to import into Notion
**Drag and drop (easiest)**
1. Create a page called "FRAMES LMS Documentation" in Notion.
2. Drag the six `.md` files into the page; Notion will create sub-pages.

**Import menu**
1. Click "Import" in the Notion sidebar.
2. Pick "Markdown" and select the six files.

**Copy/paste**
1. Open each `.md` file locally.
2. Copy the contents and paste into a new Notion page.

## Recommended reading order
Day 1: 01 Project Overview, 02 Module Type Specifications
Day 2: 03 Database Schema, 06 Technical Decisions
Day 3: 04 Development Roadmap, 05 Integration Checklist

## Suggested organization
- Single page with six sub-pages under "FRAMES LMS Documentation", or
- Group by category:
  - Planning: Overview, Development Roadmap
  - Technical: Database Schema, Technical Decisions, Integration Checklist
  - Design: Module Type Specifications
- Advanced: create a Notion database with Title, Category, Status, Last Updated, Related To.

## Checklist after importing
- [ ] All six documents present and readable.
- [ ] Headers and code blocks look correct.
- [ ] Tables render correctly.
- [ ] Optional: links between pages added with `@` mentions.
- [ ] Workspace shared with the team.

## Keeping Notion synced
- Current: edit the `.md` files and re-import when they change.
- Automated option: use `scripts/sync_notion.py` (already created) with `NOTION_API_KEY` and a parent page ID to push docs via the API.

## Optional: Notion API setup
1. Create a Notion integration and copy the API key.
2. Share the target page with the integration.
3. Install SDK: `pip install notion-client` (already in requirements).
4. Run `python scripts/sync_notion.py <PARENT_PAGE_ID>` to push the docs.

## Formatting tips
- Use `#`/`##`/`###` for headings.
- Keep lists as `- item` bullets.
- Wrap code with triple backticks (```python).
- Use `@` mentions inside Notion to link related pages.

## Next steps after import
1. Review content and add any missing context.
2. Create a task database for roadmap items.
3. Link modules, tasks, and decisions as needed.

## Troubleshooting
- If import fails, resave the file as UTF-8 and retry.
- If formatting looks off, use Notion's block types to adjust.
- If links are missing, recreate them with `@` mentions.

## Support
- Notion import docs: https://www.notion.so/help/import-data-into-notion
- For regeneration or API questions, ask in the repo.
