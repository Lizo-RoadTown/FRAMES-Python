# How to Start the Three Autonomous Agents

## 🎯 Agent Roles & Task Complexity

### Agent Alpha (You - Current Session)
**Specialty:** Complex content transformation and module design
**Best at:** Educational architecture, complex learning experiences
**Work queue:** [agent_work_queues/alpha_queue.md](agent_work_queues/alpha_queue.md)

### Agent Beta (VS Code Session 2)
**Specialty:** UI/frontend implementation with explicit requirements
**Best at:** Well-defined features, moderate complexity tasks, following UI rules
**May struggle with:** Very complex architectural decisions
**Work queue:** [agent_work_queues/beta_queue.md](agent_work_queues/beta_queue.md)

### Agent Gamma (VS Code Session 3)
**Specialty:** Infrastructure and system architecture
**Best at:** Complex technical coordination, data pipelines
**Work queue:** [agent_work_queues/gamma_queue.md](agent_work_queues/gamma_queue.md)

---

## 🟣 Prompt for Agent Beta (VS Code Session 2)

```
You are Agent Beta, an autonomous worker in a three-agent system for Ascent Basecamp.

YOUR STRENGTHS:
- UI/frontend implementation with explicit design requirements
- Well-defined, moderate complexity tasks
- Following established patterns and rules
- Component-based development

WORK WITH GAMMA on complex architectural decisions - they handle infrastructure complexity.

Read: AUTONOMOUS_AGENT_SYSTEM.md

Responsibilities:
- Build React UI components (apps/onboarding-lms/frontend-react/src)
- Implement well-defined API endpoints (backend/lms_routes.py)
- Create student-facing features with clear requirements

Work queue: agent_work_queues/beta_queue.md

Use shared/agent_utils.py for coordination:
from shared.agent_utils import startup_protocol, claim_resource, check_in, request_help

context = startup_protocol('beta')
# You're fully autonomous - no approval needed for normal work
# Ask Gamma for help on complex architecture questions
```

---

## 🟠 Prompt for Agent Gamma (VS Code Session 3)

```
You are Agent Gamma, an autonomous worker in a three-agent system for Ascent Basecamp.

YOUR STRENGTHS:
- Complex system architecture and infrastructure
- Data pipelines and coordination
- Technical problem-solving
- Supporting other agents on architectural questions

SUPPORT BETA when they encounter complex architectural decisions.

Read: AUTONOMOUS_AGENT_SYSTEM.md

Responsibilities:
- Deploy/maintain Notion sync daemon
- Populate ghost_cohorts and complex data structures
- Infrastructure scripts and automation
- **Respond to help requests from Alpha/Beta**

Work queue: agent_work_queues/gamma_queue.md

PRIORITY: Check for help requests FIRST - other agents may be blocked.

Use shared/agent_utils.py:
from shared.agent_utils import startup_protocol, claim_resource, request_help

context = startup_protocol('gamma')
# Check context['help_requests'] immediately - respond to blockers first!
```

---

## 📋 Task Assignment Strategy

### Assign to ALPHA:
- ✅ Creating learning modules from CADENCE docs
- ✅ Educational content design
- ✅ Complex module enhancement (race features, difficulty)
- ✅ Prerequisite graph design

### Assign to BETA:
- ✅ Building React UI components (module player, dashboard)
- ✅ Implementing API endpoints with clear specs
- ✅ UI features with explicit design requirements
- ✅ Form validation, user interactions
- ❌ Complex authentication architecture (ask Gamma)
- ❌ Database schema design (ask Gamma)

### Assign to GAMMA:
- ✅ Infrastructure setup (Notion sync, backups)
- ✅ Complex data pipelines (ghost cohorts)
- ✅ System architecture decisions
- ✅ Database optimization
- ✅ Responding to Alpha/Beta help requests

---

## 🚀 Recommended Startup Sequence

### Step 1: Start Gamma First
**In VS Code Session 3:**
- Paste Gamma's prompt above
- Gamma sets up infrastructure and stands ready to help

### Step 2: Start Alpha (You!)
```python
from shared.agent_utils import startup_protocol, claim_resource

context = startup_protocol('alpha')
print(f"I have {len(context['my_tasks'])} tasks")

# Start working on module enhancement...
```

### Step 3: Start Beta
**In VS Code Session 2:**
- Paste Beta's prompt above
- Beta starts building UI components
- If Beta hits complex architecture, they'll request help from Gamma

---

## 🤝 How Beta Requests Help (Example)

**Beta encounters complex decision:**
```python
from shared.agent_utils import request_help

# Beta realizes JWT vs sessions is a complex architectural choice
request_help(
    agent_name='beta',
    help_from='gamma',
    reason='Need architectural guidance: Should we use JWT tokens or session cookies for auth? Building login UI but not sure which backend approach.',
    priority='medium'
)

# Beta pauses auth work, moves to simpler task (building module player UI)
```

**Gamma sees help request at next startup:**
```python
context = startup_protocol('gamma')

if context['help_requests']:
    # Gamma sees Beta's question about auth
    # Gamma makes architectural decision
    # Gamma responds

    resolve_help_request(
        'gamma',
        request_log_id=123,
        'Use JWT tokens - better for SPA, stateless API. Here's the implementation pattern...'
    )

# Beta checks back, sees resolution, implements JWT with Gamma's guidance
```

---

## ✅ Verification After All Three Started

### Check All Agents Online:
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

## 🎯 Task Complexity Guidelines

### Simple/Moderate (→ Beta):
- Implement a form with validation
- Build a dashboard component showing data
- Create API endpoint with clear spec
- Add styling to existing component

### Complex (→ Alpha or Gamma):
- Design learning module structure
- Architect authentication system
- Build data transformation pipeline
- Design database schema

### If Unsure:
- Start Beta on it
- If Beta requests help → Gamma steps in
- Natural load balancing through help requests

---

## 📚 Reference

- [AUTONOMOUS_AGENT_SYSTEM.md](AUTONOMOUS_AGENT_SYSTEM.md) - Complete design
- [shared/agent_utils.py](shared/agent_utils.py) - Coordination utilities
- [AUTONOMOUS_AGENT_SETUP_COMPLETE.md](AUTONOMOUS_AGENT_SETUP_COMPLETE.md) - Infrastructure

---

**Ready to launch!**
1. Start Gamma (VS Code Session 3)
2. Start your work as Alpha
3. Start Beta (VS Code Session 2)

All three coordinate autonomously through database and shared files!
