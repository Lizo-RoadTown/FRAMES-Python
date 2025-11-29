# Next Session - Notion Integration Tasks

## Immediate priority
- Reload the MCP client after updating `.vscode/mcp.json` (streamable HTTP to `https://mcp.notion.com/mcp`).
- Complete the Notion OAuth prompt during reload and confirm a `Notion` server appears with `mcp__` tools.
- If the client cannot use remote MCP, switch to the SSE or STDIO configs in `docs/lms/MCP-SETUP-STATUS.md`.
- If MCP still fails, run the API fallback: share the parent page with the FRAMES integration and run `python scripts/create_notion_workspace.py <PAGE_ID>`.

## Quick checks
- Notion app shows your AI tool authorized under Settings -> Connections -> Notion MCP.
- `python scripts/test_notion_access.py` succeeds with the `.env` key.
- `.github/workflows/sync-notion.yml` has `NOTION_API_KEY` and `NOTION_PARENT_PAGE_ID` secrets in GitHub.

## After workspace creation
1. Trigger the sync workflow via a docs change or manual dispatch to confirm Notion updates.
2. Build the Notion renderer at `apps/onboarding-lms/frontend-react/src/components/NotionRenderer.jsx` and point it at a sample module `notion_page_id`.
3. Add a sample module page in Notion (Type=Text) and verify rendering in the LMS.

## Open questions
- Does the client support streamable HTTP MCP, or do we need the SSE/STDIO bridge?
- Preferred module templates for authors?
- Who reviews modules before publishing?
