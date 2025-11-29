# Multi-Agent System Setup Guide
## Get Three Agents Working in Parallel with Notion Monitoring

**Created:** 2025-11-28
**Purpose:** Step-by-step guide to deploy the three-agent parallel work system

---

## What You're Setting Up

A system where **three AI agents work simultaneously** on different parts of Ascent Basecamp, with **real-time monitoring via Notion dashboards**.

### The Agents:
- **Alpha:** Creates learning modules from CADENCE docs
- **Beta:** Builds student platform (API + frontend)
- **Gamma:** Manages infrastructure and data pipelines

### The Monitoring:
You'll see everything in real-time via Notion:
- What each agent is working on
- Progress percentages
- Resource claims (no conflicts)
- Live activity feed

---

## Architecture Overview

```
┌─────────────────┐
│  Agent Alpha    │────┐
│ (Module Creator)│    │
└─────────────────┘    │
                       │
┌─────────────────┐    │     ┌──────────────────┐     ┌──────────────┐
│   Agent Beta    │────┼────→│  Neon PostgreSQL │────→│ Sync Daemon  │────→│ Notion     │
│ (Platform Dev)  │    │     │  (Source of Truth│     │ (Every 30s)  │     │ Dashboards │
└─────────────────┘    │     └──────────────────┘     └──────────────┘     └──────────────┘
                       │                                                          ↑
┌─────────────────┐    │                                                          │
│  Agent Gamma    │────┘                                                    You monitor here
│ (Infrastructure)│
└─────────────────┘
```

**Key Point:** Agents NEVER touch Notion directly. They only write to Postgres, and the sync daemon pushes updates to Notion.

---

## Step 1: Database Schema Updates

First, add the `resource_claim` column to support the coordination protocol:

```sql
-- Connect to Neon database
ALTER TABLE ascent_basecamp_agent_log
ADD COLUMN IF NOT EXISTS resource_claim VARCHAR(255);

CREATE INDEX IF NOT EXISTS idx_agent_log_resource
ON ascent_basecamp_agent_log(resource_claim);

CREATE INDEX IF NOT EXISTS idx_agent_log_agent_timestamp
ON ascent_basecamp_agent_log(agent_name, timestamp DESC);
```

Run this via:
```bash
python -c "
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

cur.execute('''
    ALTER TABLE ascent_basecamp_agent_log
    ADD COLUMN IF NOT EXISTS resource_claim VARCHAR(255);
''')

cur.execute('''
    CREATE INDEX IF NOT EXISTS idx_agent_log_resource
    ON ascent_basecamp_agent_log(resource_claim);
''')

conn.commit()
print('✅ Database schema updated')
"
```

---

## Step 2: Refresh Notion API Token

The current token in `.env` appears to be expired.

1. Go to https://www.notion.so/my-integrations
2. Find your "FRAMES LMS" integration (or create new one)
3. Click "Show" next to "Internal Integration Token"
4. Copy the token (starts with `ntn_`)
5. Update `.env`:
   ```
   NOTION_API_KEY=ntn_YOUR_NEW_TOKEN_HERE
   NOTION_TOKEN=ntn_YOUR_NEW_TOKEN_HERE
   ```

6. Share your Foundation page with the integration:
   - Open the Foundation page in Notion
   - Click "..." → "Add connections"
   - Select your FRAMES LMS integration

---

## Step 3: Set Up Notion Databases

Run the setup script to create all 6 dashboards:

```bash
python scripts/notion_continuous_sync.py --setup
```

This creates:
1. 🤖 **Agent Activity Dashboard** - Real-time agent status
2. 🔒 **Resource Claims** - What's currently claimed
3. 👥 **Team Dashboard** - CADENCE people
4. 📊 **Project Dashboard** - CADENCE projects
5. ✅ **Task Dashboard** - CADENCE tasks
6. 📚 **Module Library** - Learning modules

The script will save the database IDs to your `.env` file.

---

## Step 4: Deploy the Sync Daemon

### Option A: Run in Terminal (for testing)
```bash
python scripts/notion_continuous_sync.py --run
```

Keep this terminal open. You should see:
```
🚀 Notion Continuous Sync Daemon Starting
Agent logs sync: Every 30s
Dashboard sync: Every 120s
Module sync: Every 300s

Press Ctrl+C to stop

Sync Iteration #1 - 2025-11-28 14:30:00
Syncing agent activity...
  ✅ Synced 0 agents
...
```

### Option B: Run as Background Service (recommended)

**Windows:**
Create a batch file `run_sync_daemon.bat`:
```batch
@echo off
cd "c:\Users\LizO5\FRAMES Python"
python scripts/notion_continuous_sync.py --run >> logs/sync_daemon.log 2>&1
```

Then create a Windows Task Scheduler task:
1. Open Task Scheduler
2. Create Basic Task → Name: "Notion Sync Daemon"
3. Trigger: At system startup
4. Action: Start a program → Browse to `run_sync_daemon.bat`
5. Settings: "If the task fails, restart every 5 minutes"

**Linux/Mac:**
```bash
# Create systemd service
sudo nano /etc/systemd/system/notion-sync.service

# Add:
[Unit]
Description=Notion Continuous Sync Daemon
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/FRAMES Python
ExecStart=/usr/bin/python3 scripts/notion_continuous_sync.py --run
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable notion-sync
sudo systemctl start notion-sync
sudo systemctl status notion-sync
```

---

## Step 5: Verify Notion Dashboards

Open Notion → Your Foundation page → You should see 6 new databases.

Click into **Agent Activity Dashboard** → It should show 3 rows (one per agent) but all idle initially.

---

## Step 6: Start the Three Agents

Each agent needs to run their startup protocol. Here's how to manually trigger each:

### Start Agent Gamma (Infrastructure)

Gamma should start first since they set up the monitoring.

```bash
# Log Gamma startup
python -c "
from scripts.log_agent_gamma_work import log_gamma_action

log_gamma_action(
    action_type='startup',
    status='ready',
    message='Agent Gamma online - Infrastructure and data pipelines ready'
)
print('✅ Gamma started')
"
```

Then Gamma's first task from `agent_work_queues/gamma_queue.md`:
- Verify sync daemon is running
- Monitor Notion dashboards
- Wait for Alpha/Beta to start

### Start Agent Alpha (Module Creation)

```bash
# Log Alpha startup
python -c "
from scripts.log_agent_gamma_work import log_gamma_action

log_gamma_action(
    action_type='startup',
    status='ready',
    message='Agent Alpha online - Module creation engine ready',
    agent_name='alpha'  # Override default
)
print('✅ Alpha started')
"
```

Then Alpha's first task from `agent_work_queues/alpha_queue.md`:
- Claim `modules/power/orientation.md`
- Start creating power subsystem orientation module

### Start Agent Beta (Platform Development)

```bash
# Log Beta startup
python -c "
from scripts.log_agent_gamma_work import log_gamma_action

log_gamma_action(
    action_type='startup',
    status='ready',
    message='Agent Beta online - Student platform development ready',
    agent_name='beta'
)
print('✅ Beta started')
"
```

Then Beta's first task from `agent_work_queues/beta_queue.md`:
- Claim `backend/lms_routes.py::start_module`
- Complete API endpoint #3

---

## Step 7: Monitor in Notion

Open Notion → **Agent Activity Dashboard**

Within 30 seconds, you should see:
- All 3 agents showing "🟢 Working" status
- Current tasks listed
- Progress percentages updating
- Last update timestamps

Open **Resource Claims** → You should see:
- Different resources claimed by each agent
- No conflicts (each agent working on different subsystem)

---

## Step 8: Test the Coordination System

### Test 1: Progress Logging
Wait 10 minutes. Each agent should log progress automatically.
Check Notion → Progress percentages should increase.

### Test 2: Resource Conflict Prevention
Try to have two agents claim the same resource.
The second agent should detect the conflict and back off.

### Test 3: Handoff
Have Alpha request help from Gamma:
```python
log_gamma_action(
    action_type='help',
    status='blocked',
    message='Need ghost cohort data for power modules',
    metadata={'help_needed_from': 'gamma', 'modules': [124, 125]},
    agent_name='alpha'
)
```

Gamma should see this in the agent log and respond.

### Test 4: Completion Tracking
When an agent finishes a task, check:
- Notion → Resource Claims → Status changes to "Complete"
- Notion → Agent Activity → Task updates to next item
- `AGENT_TEAM_CHAT.md` → End-of-session summary appears

---

## Troubleshooting

### Problem: Sync daemon shows "401 Unauthorized"
**Fix:** Refresh Notion API token (Step 2)

### Problem: Databases not appearing in Notion
**Fix:**
1. Check that Foundation page is shared with integration
2. Re-run setup: `python scripts/notion_continuous_sync.py --setup`

### Problem: Agents not appearing in Notion
**Fix:**
1. Check sync daemon is running
2. Check agents are logging to `ascent_basecamp_agent_log` table
3. Query database: `SELECT * FROM ascent_basecamp_agent_log ORDER BY timestamp DESC LIMIT 10;`

### Problem: Two agents claiming same resource
**Fix:**
1. Check agent log for conflict
2. Agent with later timestamp should auto-release
3. If not, manually release: Update agent log to set status='error'

---

## Success Checklist

After setup is complete, you should have:

- [x] Database schema updated with `resource_claim` column
- [x] Notion API token refreshed
- [x] 6 Notion databases created
- [x] Sync daemon running (visible in terminal or as service)
- [x] All 3 agents started and logging to database
- [x] Notion dashboards showing real-time updates (<1 min latency)
- [x] No resource conflicts in Resource Claims dashboard
- [x] Agent Activity Dashboard showing progress

---

## Daily Operations

### Morning:
1. Open Notion → Check Agent Activity Dashboard
2. Review what each agent completed yesterday (AGENT_TEAM_CHAT.md)
3. Check for blockers in Agent Activity Dashboard

### During the Day:
Monitor Notion dashboards casually. You should see:
- Progress percentages increasing
- Tasks completing
- New modules appearing in Module Library
- Team/Project/Task dashboards staying current

### Evening:
1. Check AGENT_TEAM_CHAT.md for session summaries
2. Review metrics (modules created, endpoints deployed, etc.)
3. Identify any blockers to address tomorrow

---

## Advanced: Agent Communication Examples

### Alpha asks Gamma for ghost cohorts:
```python
# Alpha logs help request
log_gamma_action(
    agent_name='alpha',
    action_type='help',
    status='blocked',
    message='Need ghost cohort benchmarks for power modules 124-128',
    metadata={'help_needed_from': 'gamma', 'priority': 'high'}
)

# Gamma sees this and responds
log_gamma_action(
    agent_name='gamma',
    action_type='claim',
    resource_claim='ghost_cohorts::power_modules',
    status='working',
    message='Populating ghost cohorts for Alpha - ETA 30 minutes',
    metadata={'handoff_from': 'alpha'}
)

# Gamma completes and notifies
log_gamma_action(
    agent_name='gamma',
    action_type='complete',
    resource_claim='ghost_cohorts::power_modules',
    status='done',
    message='Ghost cohorts ready for modules 124-128',
    metadata={'cohorts_created': 3, 'modules_affected': [124,125,126,127,128]}
)
```

---

## Files Created in This Setup

- [temp_docs/05_agent_coordination_protocol.md](temp_docs/05_agent_coordination_protocol.md) - Coordination rules
- [THREE_AGENT_PARALLEL_WORK_PLAN.md](THREE_AGENT_PARALLEL_WORK_PLAN.md) - Overall work plan
- [scripts/notion_continuous_sync.py](scripts/notion_continuous_sync.py) - Sync daemon
- [agent_work_queues/alpha_queue.md](agent_work_queues/alpha_queue.md) - Alpha's task list
- [agent_work_queues/beta_queue.md](agent_work_queues/beta_queue.md) - Beta's task list
- [agent_work_queues/gamma_queue.md](agent_work_queues/gamma_queue.md) - Gamma's task list

---

## Next Steps

1. **Complete setup** (Steps 1-7 above)
2. **Let agents run** for 1 hour
3. **Check Notion** to see progress
4. **Review this evening** - read session summaries in AGENT_TEAM_CHAT.md
5. **Iterate** - adjust work queues based on progress

---

**Questions?** Review the [Agent Coordination Protocol](temp_docs/05_agent_coordination_protocol.md) for detailed rules.

**Ready to start?** Begin with Step 1: Database Schema Updates
