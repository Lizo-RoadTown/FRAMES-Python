# GitHub Codespace Quick Start - Three Agent System

**TL;DR:** Wake up 3 autonomous agents in separate VS Code sessions to build Ascent Basecamp LMS

---

## ⚡ 30-Second Setup

### 1. Create `.env` file
```bash
cat > .env << 'EOF'
DATABASE_URL=postgresql://YOUR_NEON_CONNECTION_STRING_HERE
EOF
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
cd frontend-react && npm install && cd ..
```

### 3. Wake up agents in 3 VS Code windows

**Window 1 - Alpha (Module Creator):**
```
You are Agent Alpha. Read: START_THREE_AGENTS.md, AGENT_TEAM_CHAT.md, agent_work_queues/alpha_queue.md
Run: from shared.agent_utils import startup_protocol; startup_protocol('alpha')
Next task: Create Command & Data Handling Systems module
```

**Window 2 - Beta (Frontend Developer):**
```
You are Agent Beta. Read: START_THREE_AGENTS.md, AGENT_TEAM_CHAT.md, agent_work_queues/beta_queue.md
Run: from shared.agent_utils import startup_protocol; startup_protocol('beta')
Next task: Build supporting React components (ModuleCard, ProgressStepper, etc.)
```

**Window 3 - Gamma (Infrastructure):**
```
You are Agent Gamma. Read: START_THREE_AGENTS.md, AGENT_TEAM_CHAT.md, agent_work_queues/gamma_queue.md
Run: from shared.agent_utils import startup_protocol; startup_protocol('gamma')
PRIORITY: Populate ghost_cohorts table (Alpha and Beta are waiting!)
```

---

## 📄 Full Wake-Up Prompts

**For detailed context, use these files:**
- [AGENT_ALPHA_WAKEUP_PROMPT.md](AGENT_ALPHA_WAKEUP_PROMPT.md) - Full Alpha orientation
- [AGENT_BETA_WAKEUP_PROMPT.md](AGENT_BETA_WAKEUP_PROMPT.md) - Full Beta orientation
- [AGENT_GAMMA_WAKEUP_PROMPT.md](AGENT_GAMMA_WAKEUP_PROMPT.md) - Full Gamma orientation

**For system overview:**
- [START_HERE_AGENTS.md](START_HERE_AGENTS.md) - Master index and guide

---

## 🎯 Current Status (2025-11-29)

| Agent | Progress | Next Task | Blockers |
|-------|----------|-----------|----------|
| **Alpha** | 11 modules created (71-82) | Create more avionics modules | Race metadata (waiting on Gamma) |
| **Beta** | API + React scaffolding done | Build supporting components | None |
| **Gamma** | Neon docs updated | **Populate ghost_cohorts** | Notion sync (can defer) |

---

## 🚨 Critical Path

```
Gamma populates ghost_cohorts
    ↓
Alpha adds race metadata to modules
    ↓
Beta tests race features in frontend
    ↓
Full competitive learning experience ready!
```

**Gamma is the blocker!** Prioritize ghost_cohorts over Notion sync.

---

## ✅ Success Check

After all 3 agents wake up, verify they're online:

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

Expected:
```
alpha: startup - ready
beta: startup - ready
gamma: startup - ready
```

---

## 📞 Need Help?

**Full documentation:** [START_HERE_AGENTS.md](START_HERE_AGENTS.md)

**Agent coordination:** [AUTONOMOUS_AGENT_SYSTEM.md](AUTONOMOUS_AGENT_SYSTEM.md)

**Work plans:** [THREE_AGENT_PARALLEL_WORK_PLAN.md](THREE_AGENT_PARALLEL_WORK_PLAN.md)

**Team updates:** [AGENT_TEAM_CHAT.md](AGENT_TEAM_CHAT.md)
