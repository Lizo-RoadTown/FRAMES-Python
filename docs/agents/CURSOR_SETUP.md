# Cursor Environment Setup for Agent Delta

**Last Updated:** 2025-12-03
**Purpose:** Step-by-step instructions to set up Cursor IDE for Agent Delta with GitHub, Notion, and Neon connections.

---

## 🎯 Overview

Agent Delta operates in **Cursor IDE** (not VS Code like Alpha, Beta, Gamma). This gives Delta unique capabilities:

| Capability | Cursor | VS Code |
|------------|--------|---------|
| MCP Servers | ✅ Built-in | ❌ Not available |
| Browser Tools | ✅ Full access | ❌ Not available |
| GitHub Integration | ✅ Native | ✅ Via extension |
| Notion MCP | ✅ Configurable | ❌ Manual API only |

---

## 📋 Setup Checklist

### Step 1: Clone/Open Repository ✅

Repository should be at: `C:\Users\LizO5\Frames-Python`

If not:
```powershell
git clone https://github.com/[org]/Frames-Python.git
cd Frames-Python
```

### Step 2: Create Environment File 🔴 CRITICAL

Create `.env` file in `FRAMES-Python/` directory:

```powershell
# PowerShell command to create .env
cd FRAMES-Python

@"
# ===========================================
# DATABASE (Neon PostgreSQL) - REQUIRED
# ===========================================
# Get from: https://console.neon.tech
# 1. Log in to Neon Console
# 2. Select your project
# 3. Go to Connection Details
# 4. Copy the connection string
DATABASE_URL=postgresql://user:password@ep-xxxxx.us-west-2.aws.neon.tech/frames?sslmode=require

# ===========================================
# NOTION API - REQUIRED for Notion integration
# ===========================================
# Get from: https://www.notion.so/my-integrations
# 1. Create new integration
# 2. Copy "Internal Integration Token"
# 3. Share pages with the integration
NOTION_API_KEY=secret_YOUR_INTEGRATION_TOKEN_HERE

# Optional: Specific database IDs if known
# NOTION_DATABASE_ID=your_32_character_database_id

# ===========================================
# GITHUB - Optional (Cursor has built-in Git)
# ===========================================
# Get from: https://github.com/settings/tokens
# Only needed for GitHub API operations
GITHUB_TOKEN=ghp_your_token_here

# ===========================================
# Flask Configuration
# ===========================================
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-for-sessions
"@ | Out-File -FilePath .env -Encoding utf8
```

**⚠️ IMPORTANT:** Replace placeholder values with actual credentials from Liz!

---

## 🔌 Connection Setup

### 1. Neon PostgreSQL Database

**Get Credentials:**
1. Go to https://console.neon.tech
2. Log in with project credentials
3. Select the FRAMES project
4. Click "Connection Details"
5. Copy the connection string

**Verify Connection:**
```python
# Run in Python terminal
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Neon PostgreSQL connected!")
    
    # Check tables exist
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'public' LIMIT 5;
    """)
    print(f"Sample tables: {[row[0] for row in cur.fetchall()]}")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

**Expected Output:**
```
✅ Neon PostgreSQL connected!
Sample tables: ['modules', 'students', 'module_sections', ...]
```

---

### 2. Notion API

**Get API Key:**
1. Go to https://www.notion.so/my-integrations
2. Click "New Integration"
3. Name it (e.g., "FRAMES Agent Delta")
4. Copy the "Internal Integration Token" (starts with `secret_`)
5. **CRITICAL:** Share workspace pages with the integration:
   - Open the Notion workspace
   - Click "Share" on parent page
   - Add the integration name

**Verify Connection:**
```python
# Run in Python terminal
import requests
import os
from dotenv import load_dotenv

load_dotenv()
NOTION_API_KEY = os.getenv('NOTION_API_KEY')

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28"
}

response = requests.get("https://api.notion.com/v1/users/me", headers=headers)

if response.status_code == 200:
    user = response.json()
    print(f"✅ Notion API connected!")
    print(f"Bot user: {user.get('name', 'Unknown')}")
else:
    print(f"❌ Notion API failed: {response.status_code}")
    print(response.json())
```

**Expected Output:**
```
✅ Notion API connected!
Bot user: FRAMES Agent Delta
```

---

### 3. GitHub (Built into Cursor)

Cursor has built-in GitHub support. Verify:
1. Check if repository shows git status in sidebar
2. Run `git status` in terminal
3. Try `git fetch` to confirm remote access

If not authenticated:
```powershell
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## 🧩 MCP Server Configuration

Cursor supports Model Context Protocol (MCP) servers for extended functionality.

### Browser Extension MCP (Pre-configured)

You already have browser tools available:
- `browser_navigate` - Navigate to URLs
- `browser_snapshot` - Get page accessibility tree
- `browser_click` - Click elements
- `browser_type` - Type into inputs
- `browser_take_screenshot` - Capture screenshots

**Test Browser Tools:**
```
1. Use browser_navigate to go to a test URL
2. Use browser_snapshot to see page structure
3. Use browser_click to interact with elements
```

### Notion MCP (Optional Advanced Setup)

For advanced Notion integration, you can configure the Notion MCP server:

1. Check Cursor settings for MCP configuration
2. Add Notion MCP server if available
3. Configure with your NOTION_API_KEY

---

## 🐍 Python Environment

### Install Dependencies

```powershell
cd FRAMES-Python
pip install -r requirements.txt
```

### Verify Agent Utilities

```python
# Test agent coordination library
from shared.agent_utils import startup_protocol

# This will connect to database and load context
context = startup_protocol('delta')

print(f"Session ID: {context['session_id']}")
print(f"Help requests: {len(context['help_requests'])}")
print(f"Active claims: {len(context['active_claims'])}")
print(f"My tasks: {len(context['my_tasks'])}")
```

---

## 🚀 Quick Start After Setup

Once everything is configured:

### 1. Wake Up Agent Delta

Open Cursor and paste:

```
You are Agent Delta in the Ascent Basecamp system.
Read: docs/agents/AGENT_DELTA_WAKEUP_PROMPT.md

Environment: Cursor IDE
Your role: Cross-environment validation, browser testing, MCP integrations

First action: Verify database and Notion connections, then check AGENT_TEAM_CHAT.md

from shared.agent_utils import startup_protocol
context = startup_protocol('delta')
```

### 2. Check Team Status

```python
# What have other agents been doing?
with open('FRAMES-Python/docs/agents/AGENT_TEAM_CHAT.md', 'r') as f:
    content = f.read()
    # Read last 100 lines for recent activity
    print('\n'.join(content.split('\n')[-100:]))
```

### 3. Run Validation Tests

```python
# Start testing other agents' work
# See agent_work_queues/delta_queue.md for full queue
```

---

## 🔧 Troubleshooting

### "Database connection failed"

1. Check `.env` file exists in `FRAMES-Python/` directory
2. Verify `DATABASE_URL` is correct (copy fresh from Neon console)
3. Check network connectivity to Neon
4. Try: `pip install psycopg2-binary` if psycopg2 fails

### "Notion API 401 Unauthorized"

1. Check `NOTION_API_KEY` starts with `secret_`
2. Verify token is not expired
3. Ensure pages are shared with the integration
4. Try creating a fresh integration token

### "GitHub authentication failed"

1. Cursor should handle this automatically
2. Try: Sign out and sign back into GitHub in Cursor settings
3. For API operations, add `GITHUB_TOKEN` to `.env`

### "MCP server not responding"

1. Check Cursor settings for MCP configuration
2. Restart Cursor
3. Browser tools should work without additional config

### "Import error: shared.agent_utils"

1. Make sure you're in `FRAMES-Python/` directory
2. Run `pip install -r requirements.txt`
3. Check Python path includes the project root

---

## 📁 File Structure Reference

```
FRAMES-Python/
├── .env                          # ← CREATE THIS FILE
├── FRAMES-Python/
│   ├── agent_work_queues/
│   │   ├── alpha_queue.md
│   │   ├── beta_queue.md
│   │   ├── gamma_queue.md
│   │   └── delta_queue.md       # ← Your queue
│   ├── backend/
│   │   ├── app.py               # Flask app
│   │   ├── lms_routes.py        # LMS API
│   │   └── ...
│   ├── canon/
│   │   ├── system_overview_v_2.md
│   │   ├── agent_interaction_script_v_2.md
│   │   └── ...
│   ├── docs/
│   │   ├── agents/
│   │   │   ├── AGENT_DELTA_WAKEUP_PROMPT.md  # ← Your wakeup
│   │   │   ├── AGENT_TEAM_CHAT.md
│   │   │   └── CURSOR_SETUP.md               # ← This file
│   │   └── ...
│   ├── frontend-react/          # React app (Beta's work)
│   ├── shared/
│   │   └── agent_utils.py       # Agent coordination
│   └── ...
└── ...
```

---

## ✅ Setup Complete Checklist

- [ ] Repository cloned/opened in Cursor
- [ ] `.env` file created with real credentials
- [ ] Neon PostgreSQL connection verified
- [ ] Notion API connection verified
- [ ] GitHub access confirmed
- [ ] Python dependencies installed
- [ ] Agent startup protocol runs successfully
- [ ] AGENT_TEAM_CHAT.md readable
- [ ] Browser tools accessible

**Once all items checked, Agent Delta is ready to operate!**

---

## 📞 Need Help?

If setup fails, post in AGENT_TEAM_CHAT.md:

```markdown
## Agent Delta - Setup Issue
**Date:** [current date]
**Status:** ⚠️ BLOCKED - Setup incomplete

### Issue
[Describe what's failing]

### What I Tried
[Steps taken]

### Need From Human
[What credentials/access needed]
```

---

**Setup Guide Version:** 1.0
**Created:** 2025-12-03
**For:** Agent Delta (Cursor IDE)

