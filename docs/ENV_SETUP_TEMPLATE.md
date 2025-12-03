# Environment Setup Template

Copy these values into a `.env` file in the `FRAMES-Python/` root directory.

## Required Configuration

```env
# ===========================================
# DATABASE (Neon PostgreSQL)
# ===========================================
# Get this from: https://console.neon.tech -> Your Project -> Connection Details
DATABASE_URL=postgresql://user:password@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# ===========================================
# NOTION API (Fallback if MCP not available)
# ===========================================
# Get API key from: https://www.notion.so/my-integrations
# Create integration, copy the "Internal Integration Token"
NOTION_API_KEY=secret_YOUR_INTEGRATION_TOKEN_HERE

# Get database ID from your Module Library database URL
# URL looks like: https://notion.so/workspace/DATABASE_ID_HERE?v=...
NOTION_DATABASE_ID=your_32_character_database_id
```

## Optional Configuration

```env
# ===========================================
# GITHUB (if not using MCP)
# ===========================================
# Get from: https://github.com/settings/tokens
GITHUB_TOKEN=ghp_your_token_here
```

## Quick Setup Commands

```powershell
# Create the .env file (PowerShell)
Copy-Item FRAMES-Python\docs\ENV_SETUP_TEMPLATE.md FRAMES-Python\.env

# Or manually create .env and paste your values
```

