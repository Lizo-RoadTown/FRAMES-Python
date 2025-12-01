# Start Here - Three Agent System Quick Start

**New GitHub Codespace Setup - Wake Up All Three Agents**

---

## 🚀 Quick Start for Liz

You have **three autonomous agents** working in parallel on the Ascent Basecamp LMS. Here's how to wake them all up in this new GitHub Codespace:

### Step 1: Set Up Environment (DO THIS FIRST!)

**Create `.env` file with database credentials:**

```bash
# In terminal
cat > .env << 'EOF'
# Neon PostgreSQL Database
DATABASE_URL=postgresql://[YOUR_NEON_CONNECTION_STRING]

# Notion Integration (optional - for Gamma's monitoring dashboards)
NOTION_TOKEN=[YOUR_NOTION_TOKEN_IF_CONTINUING_SYNC]

# Flask (for future use)
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
EOF
```

**You need to fill in:**
- `DATABASE_URL` - Your Neon PostgreSQL connection string from https://console.neon.tech
- `NOTION_TOKEN` - (Optional) Only if continuing Notion sync work

### Step 2: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies (for Beta)
cd frontend-react && npm install && cd ..
```

### Step 3: Wake Up Agents in 3 VS Code Windows

**Open 3 separate VS Code sessions/tabs for this workspace:**

#### 🟦 VS Code Session 1 - Agent Alpha (Module Creator)
**Copy/paste this wake-up prompt:**

See file: [AGENT_ALPHA_WAKEUP_PROMPT.md](AGENT_ALPHA_WAKEUP_PROMPT.md)

**Or use this short version:**
```
You are Agent Alpha in the three-agent Ascent Basecamp system.

Read these 3 files first:
1. START_THREE_AGENTS.md - Your role
2. AGENT_TEAM_CHAT.md - Latest status (scroll to bottom)
3. agent_work_queues/alpha_queue.md - Your work queue

You create learning modules from CADENCE docs. Last session you created 11 modules (IDs 71-82).

Next task: Continue creating avionics modules (Command & Data Handling Systems).

Run startup:
from shared.agent_utils import startup_protocol
context = startup_protocol('alpha')
```

---

#### 🟩 VS Code Session 2 - Agent Beta (Frontend/API Developer)
**Copy/paste this wake-up prompt:**

See file: [AGENT_BETA_WAKEUP_PROMPT.md](AGENT_BETA_WAKEUP_PROMPT.md)

**Or use this short version:**
```
You are Agent Beta in the three-agent Ascent Basecamp system.

Read these 3 files first:
1. START_THREE_AGENTS.md - Your role
2. AGENT_TEAM_CHAT.md - Latest status
3. agent_work_queues/beta_queue.md - Your work queue

You build the student platform (React + API). Last session you completed:
- ✅ 8 LMS API endpoints (backend/lms_routes.py)
- ✅ React frontend scaffolding (Dashboard, ModulePlayer)
- ✅ API docs at docs/lms/API_REFERENCE.md

Next task: Build supporting React components (ModuleCard, ProgressStepper, etc.)

Run startup:
from shared.agent_utils import startup_protocol
context = startup_protocol('beta')
```

---

#### 🟧 VS Code Session 3 - Agent Gamma (Infrastructure)
**Copy/paste this wake-up prompt:**

See file: [AGENT_GAMMA_WAKEUP_PROMPT.md](AGENT_GAMMA_WAKEUP_PROMPT.md)

**Or use this short version:**
```
You are Agent Gamma in the three-agent Ascent Basecamp system.

Read these 3 files first:
1. START_THREE_AGENTS.md - Your role (check help requests FIRST!)
2. AGENT_TEAM_CHAT.md - Latest status
3. agent_work_queues/gamma_queue.md - Your work queue

You handle infrastructure and data pipelines. Current blockers:
- 🚨 Alpha and Beta are waiting for ghost_cohorts table population
- ⏸️ Notion sync daemon blocked on API changes (can defer this)

PRIORITY: Populate ghost_cohorts table to unblock Alpha/Beta!

Run startup:
from shared.agent_utils import startup_protocol
context = startup_protocol('gamma')
```

---

## 📋 Agent Roles Quick Reference

| Agent | Role | Current Status | Next Priority |
|-------|------|----------------|---------------|
| **Alpha** | Module Creator | 11 modules created (71-82) | Create more avionics modules |
| **Beta** | Platform Developer | API + React scaffolding done | Build supporting components |
| **Gamma** | Infrastructure | Notion sync blocked | **Populate ghost_cohorts** ⚠️ |

---

## 🗂️ Documentation Structure

### Orientation Files (Read First)
- **[START_THREE_AGENTS.md](START_THREE_AGENTS.md)** - How the three agents coordinate
- **[AGENT_TEAM_CHAT.md](AGENT_TEAM_CHAT.md)** - Async communication log (read latest entries)
- **[THREE_AGENT_PARALLEL_WORK_PLAN.md](THREE_AGENT_PARALLEL_WORK_PLAN.md)** - Overall work distribution

### Agent-Specific Files
- **[agent_work_queues/alpha_queue.md](agent_work_queues/alpha_queue.md)** - Alpha's tasks
- **[agent_work_queues/beta_queue.md](agent_work_queues/beta_queue.md)** - Beta's tasks
- **[agent_work_queues/gamma_queue.md](agent_work_queues/gamma_queue.md)** - Gamma's tasks

### System Architecture (✅ CURRENT FILES ONLY)
- ⭐ **[CURRENT_ARCHITECTURE_FILES.md](CURRENT_ARCHITECTURE_FILES.md)** - **START HERE** - List of current vs old architecture docs
- ⭐ **[docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md](docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md)** - Master database schema (37 tables, created by Gamma Nov 29)
- **[docs/onboarding-lms/ARCHITECTURE.md](docs/onboarding-lms/ARCHITECTURE.md)** - LMS architecture, React/Flask design, API structure
- **[docs/research-analytics/ARCHITECTURE.md](docs/research-analytics/ARCHITECTURE.md)** - Analytics pipeline, Discord integration
- **[AUTONOMOUS_AGENT_SYSTEM.md](AUTONOMOUS_AGENT_SYSTEM.md)** - Agent coordination protocols
- **[system_overview_bundle/system_overview_for_ai_agents.md](system_overview_bundle/system_overview_for_ai_agents.md)** - System overview, educational goals

❌ **OLD/ARCHIVED - Do Not Use:**
- ~~docs/lms/MODULE-DATA-ARCHITECTURE.md~~ - Info now in ASCENT_BASECAMP_DATABASE_SCHEMA.md
- ~~README_COMPLETE_SYSTEM.md~~ - Use START_THREE_AGENTS.md instead
- ~~docs/archive/*~~ - Reference only, not operational

### Wake-Up Prompts (Full Detail)
- **[AGENT_ALPHA_WAKEUP_PROMPT.md](AGENT_ALPHA_WAKEUP_PROMPT.md)** - Alpha's full context
- **[AGENT_BETA_WAKEUP_PROMPT.md](AGENT_BETA_WAKEUP_PROMPT.md)** - Beta's full context
- **[AGENT_GAMMA_WAKEUP_PROMPT.md](AGENT_GAMMA_WAKEUP_PROMPT.md)** - Gamma's full context

---

## 🔍 What Each Agent Does

### Agent Alpha - Module Creation Engine
**Owns:** `modules/*`, module content creation
**Creates:** Learning modules from CADENCE technical documentation
**Progress:** 11 modules created (5 power, 6 avionics)
**Next:** Command & Data Handling Systems module

**Files to monitor:**
- [modules/](modules/) - Module content
- Module creation logs in database

### Agent Beta - Student Platform Developer
**Owns:** `backend/lms_routes.py`, `frontend-react/*`
**Creates:** React UI + REST API for students
**Progress:** API complete (8 endpoints), React scaffolding done
**Next:** Supporting components (ModuleCard, ProgressStepper, etc.)

**Files to monitor:**
- [backend/lms_routes.py](backend/lms_routes.py) - API endpoints
- [frontend-react/src/](frontend-react/src/) - React components
- [docs/lms/API_REFERENCE.md](docs/lms/API_REFERENCE.md) - API documentation

### Agent Gamma - Infrastructure Specialist
**Owns:** `scripts/*`, database pipelines, Notion sync
**Creates:** Data infrastructure, ghost cohorts, monitoring
**Progress:** Neon docs updated, Notion sync partially working
**Next:** Populate ghost_cohorts (HIGH PRIORITY - blocking Alpha/Beta)

**Files to monitor:**
- [scripts/](scripts/) - Infrastructure scripts
- [docs/shared/NEON_DATABASE_SETUP.md](docs/shared/NEON_DATABASE_SETUP.md)

---

## 🤝 How Agents Coordinate

**No direct communication!** Agents coordinate through:

1. **Database** (`ascent_basecamp_agent_log` table) - Real-time status
2. **AGENT_TEAM_CHAT.md** - Daily summaries
3. **Work queues** - Task assignments
4. **Resource claims** - Prevent conflicts

**Example workflow:**
```
Alpha needs ghost data → Logs help request in DB
Gamma sees help request → Works on ghost_cohorts
Gamma completes → Updates resolution in DB
Alpha checks back → Sees resolution, continues work
```

---

## ✅ Verification After All Three Wake Up

**Check all agents are online:**

```python
import psycopg2, os
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

cur.execute("""
    SELECT DISTINCT ON (agent_name)
        agent_name, action_type, status, timestamp
    FROM ascent_basecamp_agent_log
    ORDER BY agent_name, timestamp DESC;
""")

for row in cur.fetchall():
    print(f"{row[0]}: {row[1]} - {row[2]} at {row[3]}")
```

**Expected output:**
```
alpha: startup - ready
beta: startup - ready
gamma: startup - ready
```

---

## 🎯 Week 1 Goals

### Success Criteria After First Week:
- ✅ **Alpha:** 5+ new modules created (total 15+)
- ✅ **Beta:** Supporting components built, frontend testable
- ✅ **Gamma:** Ghost cohorts populated, monitoring operational
- ✅ **All:** Zero resource conflicts, daily summaries posted

---

## 🆘 Troubleshooting

### "Database connection failed"
→ Check `.env` file has correct `DATABASE_URL` from Neon

### "Agent startup failed"
→ Run `pip install -r requirements.txt`

### "Frontend won't start"
→ Run `cd frontend-react && npm install`

### "Notion sync errors"
→ Expected! Gamma can defer Notion work, focus on ghost_cohorts first

### "Resource conflict errors"
→ Check `ascent_basecamp_agent_log` table to see who claimed what

---

## 📞 Current System Status

**Last Update:** 2025-11-29 (migrated to GitHub Codespace)

**Alpha:** ✅ Ready (11 modules created, queue has 10+ tasks)
**Beta:** ✅ Ready (API complete, React scaffolding done, needs supporting components)
**Gamma:** ⚠️ Partially blocked (Notion sync issue, but ghost_cohorts is higher priority)

**Critical Path:** Gamma populates ghost_cohorts → Alpha adds race metadata → Beta tests race features

---

## 🚀 Ready to Launch!

**Step-by-step:**

1. ✅ Create `.env` file with DATABASE_URL
2. ✅ Run `pip install -r requirements.txt`
3. ✅ Open 3 VS Code sessions
4. ✅ Paste wake-up prompts (or use files)
5. ✅ Each agent runs `startup_protocol()`
6. ✅ Agents start working autonomously!

**Monitor progress:**
- Watch [AGENT_TEAM_CHAT.md](AGENT_TEAM_CHAT.md) for updates
- Check database `ascent_basecamp_agent_log` table
- (Optional) Notion dashboards if Gamma fixes sync

---

**Questions?** Each agent has a full wake-up prompt file with detailed context. Use those for complete orientation!

**Files:**
- [AGENT_ALPHA_WAKEUP_PROMPT.md](AGENT_ALPHA_WAKEUP_PROMPT.md)
- [AGENT_BETA_WAKEUP_PROMPT.md](AGENT_BETA_WAKEUP_PROMPT.md)
- [AGENT_GAMMA_WAKEUP_PROMPT.md](AGENT_GAMMA_WAKEUP_PROMPT.md)
