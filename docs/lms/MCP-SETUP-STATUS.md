# Notion MCP Setup Status

This tracks the MCP connection for Notion and the fallback API flow.

## Current configuration
- Config file: `.vscode/mcp.json`
- Streamable HTTP endpoint in use (official default): `https://mcp.notion.com/mcp`
- GitHub MCP entry kept (Docker) with cleaned args; optional.

```json
{
  "mcpServers": {
    "Notion": { "url": "https://mcp.notion.com/mcp" }
  }
}
```

## How to connect (per Notion guide)
1. In the Notion app, open Settings -> Connections -> Notion MCP.
2. Pick your AI tool (Claude Desktop, VS Code, etc.) and finish the OAuth flow.
3. Ensure the MCP client reads `.vscode/mcp.json` (or your global MCP config) and reload the client/window.
4. Confirm a `Notion` MCP server appears in the tool list; tools show up with the `mcp__` prefix after auth.

## Alternative connection types
Use these only if the client cannot use the default streamable HTTP endpoint.

**SSE (server-sent events)**
```json
{
  "mcpServers": {
    "Notion": { "type": "sse", "url": "https://mcp.notion.com/sse" }
  }
}
```

**STDIO bridge (for clients that block remote URLs)**
```json
{
  "mcpServers": {
    "Notion": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.notion.com/mcp"]
    }
  }
}
```

## Expected prompts after reload
- Browser opens for Notion OAuth and workspace selection.
- After approval, MCP tools become available and reflect your workspace permissions.

## Fallback: Notion API (ready now)
- API key stored in `.env` as `NOTION_API_KEY`.
- Verify access: `python scripts/test_notion_access.py`.
- Create workspace if MCP is unavailable: `python scripts/create_notion_workspace.py <PAGE_ID>` after sharing the parent page with the FRAMES integration.

## Status
- [x] Config updated to official MCP structure and endpoint.
- [ ] OAuth handshake completed in the client.
- [ ] Tools verified inside the client.
- [ ] API fallback used if MCP remains unavailable.
