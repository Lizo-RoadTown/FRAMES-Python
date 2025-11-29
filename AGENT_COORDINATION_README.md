# Agent Coordination System
## Three Agents Working in Parallel with Notion Monitoring

---

## 🎯 What This Is

A complete system for running **three AI agents simultaneously** on different parts of Ascent Basecamp, with **real-time monitoring via Notion dashboards**.

### The Problem We Solved
You asked: *"How can we write a script that prompts continuous discussion and work and updates through Notion so me (the user) can see it?"*

### The Solution
1. **Agents work autonomously** and log everything to Neon (Postgres)
2. **A sync daemon runs continuously** (every 30s) pushing updates from Neon → Notion
3. **You monitor everything in Notion** dashboards in real-time
4. **This same pattern works for ALL dashboards** (team, projects, modules, etc.)

---

## 📚 Documentation Structure

### 1. Core Philosophy & Architecture
- [temp_docs/01_ascent_basecamp_philosophy.md](temp_docs/01_ascent_basecamp_philosophy.md) - Educational foundation
- [temp_docs/02_learning_system_architecture.md](temp_docs/02_learning_system_architecture.md) - 3-layer system
- [temp_docs/03_data_and_dashboards.md](temp_docs/03_data_and_dashboards.md) - Data flow
- [temp_docs/04_agents_and_dev_process.md](temp_docs/04_agents_and_dev_process.md) - Agent contract

### 2. NEW: Agent Coordination Protocol ⭐
- [temp_docs/05_agent_coordination_protocol.md](temp_docs/05_agent_coordination_protocol.md) - **Critical** - How agents coordinate

### 3. Work Plans
- [THREE_AGENT_PARALLEL_WORK_PLAN.md](THREE_AGENT_PARALLEL_WORK_PLAN.md) - Overall parallel work strategy
- [agent_work_queues/alpha_queue.md](agent_work_queues/alpha_queue.md) - Alpha's task list
- [agent_work_queues/beta_queue.md](agent_work_queues/beta_queue.md) - Beta's task list
- [agent_work_queues/gamma_queue.md](agent_work_queues/gamma_queue.md) - Gamma's task list

### 4. Implementation
- [MULTI_AGENT_SYSTEM_SETUP_GUIDE.md](MULTI_AGENT_SYSTEM_SETUP_GUIDE.md) - **Start here** - Step-by-step setup
- [scripts/notion_continuous_sync.py](scripts/notion_continuous_sync.py) - The sync daemon

### 5. Agent Communication
- [AGENT_TEAM_CHAT.md](AGENT_TEAM_CHAT.md) - Daily summaries and messages between agents

---

## 🚀 Quick Start

### Option 1: Read First, Then Deploy
1. Read [05_agent_coordination_protocol.md](temp_docs/05_agent_coordination_protocol.md) (10 min)
2. Read [THREE_AGENT_PARALLEL_WORK_PLAN.md](THREE_AGENT_PARALLEL_WORK_PLAN.md) (15 min)
3. Follow [MULTI_AGENT_SYSTEM_SETUP_GUIDE.md](MULTI_AGENT_SYSTEM_SETUP_GUIDE.md) (30 min setup)

### Option 2: Deploy Now, Learn Later
```bash
# Step 1: Update database schema
python -c "
import os, psycopg2
from dotenv import load_dotenv
load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()
cur.execute('ALTER TABLE ascent_basecamp_agent_log ADD COLUMN IF NOT EXISTS resource_claim VARCHAR(255);')
conn.commit()
print('✅ Schema updated')
"

# Step 2: Refresh Notion API token in .env (see setup guide)

# Step 3: Create Notion databases
python scripts/notion_continuous_sync.py --setup

# Step 4: Run sync daemon
python scripts/notion_continuous_sync.py --run
```

Then open Notion → Your Foundation page → See 6 new dashboards appearing!

---

## 🎨 What You'll See in Notion

### 1. 🤖 Agent Activity Dashboard
Real-time view of all three agents:
| Agent | Status | Current Task | Progress | Last Update | Blockers |
|-------|--------|--------------|----------|-------------|----------|
| Alpha | 🟢 Working | Creating power modules | 60% (3/5) | 2m ago | None |
| Beta | 🟢 Working | Building API endpoints | 80% (8/10) | 1m ago | None |
| Gamma | 🟡 Waiting | Notion sync daemon | 100% | 5m ago | None |

### 2. 🔒 Resource Claims
See what each agent has claimed (prevents conflicts):
| Resource | Claimed By | Status | Started | ETA |
|----------|------------|--------|---------|-----|
| modules/power/* | Alpha | Working | 14:30 | 15:00 |
| backend/lms_routes.py | Beta | Working | 14:35 | 15:30 |

### 3. 👥 Team Dashboard
Auto-synced from `cadence_people` table (27 records)

### 4. 📊 Project Dashboard
Auto-synced from `cadence_projects` table (69 records)

### 5. ✅ Task Dashboard
Auto-synced from `cadence_tasks` table (443 records)

### 6. 📚 Module Library
New modules appear here as Alpha creates them!

---

## 🔧 How It Works

### The Agent Contract
From [04_agents_and_dev_process.md](temp_docs/04_agents_and_dev_process.md):
- Agents MUST log all actions to `ascent_basecamp_agent_log`
- Dashboards are **immutable** (agents never write directly to Notion)
- Database-first: Postgres is source of truth, Notion is a view
- Agents must claim resources before working on them

### The Coordination Protocol
From [05_agent_coordination_protocol.md](temp_docs/05_agent_coordination_protocol.md):

**Before working on ANY resource:**
```python
# 1. Check for existing claims
claims = query_agent_log(resource='modules/power/battery.md')
if claims:
    print('Resource already claimed, backing off')
    return

# 2. Claim it
log_agent_action(
    agent_name='alpha',
    action_type='claim',
    resource_claim='modules/power/battery.md',
    status='working'
)

# 3. Do work with progress logging every 10 minutes
# ...

# 4. Release when done
log_agent_action(
    agent_name='alpha',
    action_type='complete',
    resource_claim='modules/power/battery.md',
    status='done'
)
```

### The Sync Daemon
From [scripts/notion_continuous_sync.py](scripts/notion_continuous_sync.py):

**Runs continuously:**
- Every 30s: Sync agent activity + resource claims (real-time)
- Every 2m: Sync team/project/task dashboards
- Every 5m: Sync module library

**Data flow:**
```
Agents → Postgres (ascent_basecamp_agent_log) → Sync Daemon → Notion Dashboards → You
```

---

## 🎯 Agent Responsibilities

### Agent Alpha: Module Creation Engine
**What:** Transforms CADENCE docs into learning modules
**Claims:** `modules/*`, `modules` table (write)
**Week 1 Goal:** 5+ power subsystem modules

### Agent Beta: Student Platform Developer
**What:** Builds frontend + API for student learning platform
**Claims:** `backend/lms_routes.py`, `frontend/*`
**Week 1 Goal:** Complete 10 LMS API endpoints

### Agent Gamma: Infrastructure Specialist
**What:** Data pipelines, sync systems, automation
**Claims:** `scripts/*`, `ghost_cohorts` (write), Notion API
**Week 1 Goal:** Sync daemon running 24/7 with 99%+ uptime

---

## 📊 How Agents Communicate

### 1. Database Agent Log (Real-time)
```sql
-- Alpha requests help from Gamma
INSERT INTO ascent_basecamp_agent_log (
    agent_name, action_type, status, message, metadata
) VALUES (
    'alpha', 'help', 'blocked',
    'Need ghost cohort data for power modules',
    '{"help_needed_from": "gamma"}'::jsonb
);

-- Gamma sees it (queries agent_log regularly)
SELECT * FROM ascent_basecamp_agent_log
WHERE action_type = 'help'
  AND metadata->>'help_needed_from' = 'gamma'
ORDER BY timestamp DESC;

-- Gamma responds
INSERT INTO ascent_basecamp_agent_log (
    agent_name, action_type, status, message
) VALUES (
    'gamma', 'claim', 'working',
    'Populating ghost cohorts for Alpha - ETA 30 min'
);
```

### 2. AGENT_TEAM_CHAT.md (Daily summaries)
Each agent writes end-of-session summary:
```markdown
## Agent Alpha - Session #4

### What I Completed Today
- Created 5 power modules
- Added race metadata

### Messages for Other Agents
**To Beta:** Power modules ready for testing (IDs 124-128)
**To Gamma:** Need ghost cohorts for avionics next

### Blockers
- None
```

### 3. Notion Dashboards (You monitor)
All communication visible in real-time via Agent Activity Dashboard

---

## 🔍 Key Files to Understand

### Must Read (30 minutes)
1. [temp_docs/05_agent_coordination_protocol.md](temp_docs/05_agent_coordination_protocol.md) - The rules
2. [THREE_AGENT_PARALLEL_WORK_PLAN.md](THREE_AGENT_PARALLEL_WORK_PLAN.md) - The strategy
3. [MULTI_AGENT_SYSTEM_SETUP_GUIDE.md](MULTI_AGENT_SYSTEM_SETUP_GUIDE.md) - The implementation

### Reference (as needed)
4. [agent_work_queues/alpha_queue.md](agent_work_queues/alpha_queue.md) - Alpha's tasks
5. [agent_work_queues/beta_queue.md](agent_work_queues/beta_queue.md) - Beta's tasks
6. [agent_work_queues/gamma_queue.md](agent_work_queues/gamma_queue.md) - Gamma's tasks

### Implementation
7. [scripts/notion_continuous_sync.py](scripts/notion_continuous_sync.py) - The sync daemon

---

## ✅ Success Criteria

### After 1 Day:
- ✅ Sync daemon running continuously
- ✅ All 6 Notion dashboards live
- ✅ All 3 agents logging activity
- ✅ You can see real-time updates in Notion

### After 1 Week:
- ✅ Alpha: 5+ power modules created
- ✅ Beta: 10 API endpoints complete
- ✅ Gamma: Ghost cohort system operational
- ✅ Zero resource conflicts logged
- ✅ Complete audit trail in agent_log

### After 1 Month:
- ✅ Alpha: 20+ modules across multiple subsystems
- ✅ Beta: Functional student platform with module player
- ✅ Gamma: Adaptive difficulty system operational
- ✅ Students can complete full learning paths

---

## 🐛 Troubleshooting

See [MULTI_AGENT_SYSTEM_SETUP_GUIDE.md](MULTI_AGENT_SYSTEM_SETUP_GUIDE.md#troubleshooting) for detailed troubleshooting.

**Quick fixes:**
- **401 Unauthorized:** Refresh Notion API token
- **Agents not appearing:** Check sync daemon is running
- **Conflicts:** Check Resource Claims dashboard
- **Sync too slow:** Adjust intervals in sync daemon script

---

## 🎓 Learning Path

1. **Understand the philosophy** - Read [01_ascent_basecamp_philosophy.md](temp_docs/01_ascent_basecamp_philosophy.md)
2. **Understand the architecture** - Read [02_learning_system_architecture.md](temp_docs/02_learning_system_architecture.md)
3. **Understand data flow** - Read [03_data_and_dashboards.md](temp_docs/03_data_and_dashboards.md)
4. **Understand agent rules** - Read [04_agents_and_dev_process.md](temp_docs/04_agents_and_dev_process.md)
5. **Understand coordination** - Read [05_agent_coordination_protocol.md](temp_docs/05_agent_coordination_protocol.md) ⭐
6. **See the work plan** - Read [THREE_AGENT_PARALLEL_WORK_PLAN.md](THREE_AGENT_PARALLEL_WORK_PLAN.md)
7. **Deploy the system** - Follow [MULTI_AGENT_SYSTEM_SETUP_GUIDE.md](MULTI_AGENT_SYSTEM_SETUP_GUIDE.md)
8. **Monitor via Notion** - Open your dashboards and watch agents work!

---

## 🚦 Current Status

- ✅ Database schema complete (37 tables, 1,050+ records)
- ✅ Agent coordination protocol defined
- ✅ Three-agent work plan created
- ✅ Work queues initialized
- ✅ Sync daemon script complete
- ⏳ **Next step:** Deploy sync daemon and start agents

---

## 📞 Contact / Questions

- Review the [Agent Coordination Protocol](temp_docs/05_agent_coordination_protocol.md) for detailed rules
- Check [MULTI_AGENT_SYSTEM_SETUP_GUIDE.md](MULTI_AGENT_SYSTEM_SETUP_GUIDE.md) for step-by-step instructions
- Look at [AGENT_TEAM_CHAT.md](AGENT_TEAM_CHAT.md) for agent communication examples

---

## 🎉 What Makes This Cool

1. **Three agents work in parallel** without stepping on each other
2. **You see everything in real-time** via Notion dashboards
3. **Complete audit trail** - every agent action is logged
4. **Scalable pattern** - same approach works for all data (team, projects, tasks, modules)
5. **Database-first** - Postgres is source of truth, Notion is just a view
6. **Autonomous but coordinated** - Agents communicate via database, not direct messages

---

**Ready to start?** → [MULTI_AGENT_SYSTEM_SETUP_GUIDE.md](MULTI_AGENT_SYSTEM_SETUP_GUIDE.md)

**Want to understand the theory first?** → [temp_docs/05_agent_coordination_protocol.md](temp_docs/05_agent_coordination_protocol.md)

**Just want to see the work plan?** → [THREE_AGENT_PARALLEL_WORK_PLAN.md](THREE_AGENT_PARALLEL_WORK_PLAN.md)
