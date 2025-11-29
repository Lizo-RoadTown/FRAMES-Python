# Autonomous Agent System for VS Code
## Three Independent Claude Code Sessions Working Together

**Purpose:** Enable three separate Claude Code agent sessions to work autonomously and coordinate through shared files and database

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                        Liz (Human)                            │
│  Monitors via: Notion dashboards + VS Code check-ins         │
│  Intervenes: Permissions, approvals, course corrections       │
└──────────────────────────────────────────────────────────────┘
                              ↓ ↑
        ┌─────────────────────────────────────────┐
        │        Shared Communication Layer        │
        │  - AGENT_TEAM_CHAT.md (daily summaries)  │
        │  - agent_log table (real-time status)    │
        │  - work_queues/ (task assignments)       │
        │  - technical_decisions table (DB)        │
        │  - error_log table (DB)                  │
        └─────────────────────────────────────────┘
                 ↓ ↑           ↓ ↑           ↓ ↑
        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
        │  VS Code 1  │ │  VS Code 2  │ │  VS Code 3  │
        │             │ │             │ │             │
        │Agent Alpha  │ │ Agent Beta  │ │Agent Gamma  │
        │(Module      │ │(Platform    │ │(Infra-      │
        │ Creator)    │ │ Developer)  │ │ structure)  │
        └─────────────┘ └─────────────┘ └─────────────┘
         Autonomous      Autonomous      Autonomous
         Works on:       Works on:       Works on:
         modules/*       backend/        scripts/
         enhancement     frontend/       infrastructure
```

---

## Key Principle: Asynchronous Coordination

**Agents NEVER directly communicate.** They coordinate through:
1. **Database tables** - Real-time status and work claims
2. **Shared files** - Daily summaries and task queues
3. **Notion dashboards** - Liz monitors everything

---

## Database Schema for Coordination

### 1. Enhanced Agent Log Table
```sql
ALTER TABLE ascent_basecamp_agent_log
ADD COLUMN IF NOT EXISTS resource_claim VARCHAR(255),
ADD COLUMN IF NOT EXISTS session_id VARCHAR(100),
ADD COLUMN IF NOT EXISTS check_in_time TIMESTAMP,
ADD COLUMN IF NOT EXISTS next_check_in TIMESTAMP;

-- This table is the real-time communication hub
```

### 2. Technical Decisions Table (NEW)
```sql
CREATE TABLE IF NOT EXISTS technical_decisions (
    decision_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_name VARCHAR(100),
    decision_type VARCHAR(100), -- 'architecture', 'api_design', 'data_model', etc.
    decision TEXT NOT NULL,
    rationale TEXT,
    alternatives_considered TEXT,
    impact VARCHAR(50), -- 'low', 'medium', 'high'
    status VARCHAR(50) DEFAULT 'proposed', -- 'proposed', 'approved', 'implemented'
    metadata JSONB
);
```

### 3. Error Log Table (NEW)
```sql
CREATE TABLE IF NOT EXISTS error_log (
    error_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_name VARCHAR(100),
    error_type VARCHAR(100), -- 'conflict', 'dependency', 'code_error', 'timeout'
    error_message TEXT NOT NULL,
    stack_trace TEXT,
    resolution_status VARCHAR(50) DEFAULT 'unresolved', -- 'unresolved', 'resolved', 'escalated'
    resolution TEXT,
    severity VARCHAR(50), -- 'low', 'medium', 'high', 'critical'
    metadata JSONB
);
```

---

## Agent Startup Protocol

When any agent starts a work session, they follow this exact sequence:

### Step 1: Announce Presence
```python
import uuid
import psycopg2
from datetime import datetime, timedelta

# Generate unique session ID
session_id = f"{agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

# Log startup
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
    INSERT INTO ascent_basecamp_agent_log (
        agent_name, action_type, status, session_id,
        check_in_time, next_check_in, message
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
""", (
    agent_name,
    'startup',
    'ready',
    session_id,
    datetime.now(),
    datetime.now() + timedelta(minutes=10),
    f'{agent_name} online - session {session_id}'
))
conn.commit()
```

### Step 2: Read Team Chat for Context
```python
# Read what other agents have been doing
with open('AGENT_TEAM_CHAT.md', 'r') as f:
    team_chat = f.read()

# Look for messages directed at this agent
my_messages = [line for line in team_chat.split('\n')
               if f'**To {agent_name}:**' in line]

print(f"Messages for me: {len(my_messages)}")
for msg in my_messages:
    print(f"  - {msg}")
```

### Step 3: Check for Active Resource Claims
```python
# See what other agents are currently working on
cur.execute("""
    SELECT agent_name, resource_claim, status, timestamp
    FROM ascent_basecamp_agent_log
    WHERE action_type = 'claim'
      AND status = 'working'
      AND agent_name != %s
      AND timestamp > NOW() - INTERVAL '2 hours'
    ORDER BY timestamp DESC;
""", (agent_name,))

active_claims = cur.fetchall()
print(f"Active claims by other agents: {len(active_claims)}")
for claim in active_claims:
    print(f"  - {claim['agent_name']} working on {claim['resource_claim']}")
```

### Step 4: Check for Help Requests
```python
# See if any agent needs help from me
cur.execute("""
    SELECT log_id, agent_name, message, metadata, timestamp
    FROM ascent_basecamp_agent_log
    WHERE action_type = 'help'
      AND status IN ('blocked', 'waiting')
      AND metadata->>'help_needed_from' = %s
      AND timestamp > NOW() - INTERVAL '24 hours'
    ORDER BY timestamp DESC;
""", (agent_name,))

help_requests = cur.fetchall()
if help_requests:
    print(f"⚠️ {len(help_requests)} help requests waiting for me!")
    for req in help_requests:
        print(f"  - From {req['agent_name']}: {req['message']}")
```

### Step 5: Read Work Queue
```python
# Read my assigned tasks
queue_file = f'agent_work_queues/{agent_name.lower()}_queue.md'
with open(queue_file, 'r') as f:
    my_queue = f.read()

# Parse next uncompleted task (look for [ ] checkbox)
import re
tasks = re.findall(r'- \[ \] (.+)', my_queue)
if tasks:
    next_task = tasks[0]
    print(f"Next task: {next_task}")
else:
    print("No pending tasks in queue")
```

### Step 6: Decide What to Work On
```python
# Priority order:
# 1. Help requests from other agents (unblock them)
# 2. Tasks from work queue
# 3. Idle if nothing to do

if help_requests:
    work_on = 'help_request'
    work_detail = help_requests[0]
elif tasks:
    work_on = 'queue_task'
    work_detail = next_task
else:
    work_on = 'idle'
    work_detail = None

print(f"Decision: Working on {work_on}")
```

---

## Work Execution Protocol

### Before Starting ANY Work

```python
def claim_resource(agent_name, resource, estimated_minutes=30):
    """
    Claim a resource before working on it.
    Returns True if claim successful, False if conflict.
    """
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Check if already claimed
    cur.execute("""
        SELECT agent_name FROM ascent_basecamp_agent_log
        WHERE resource_claim = %s
          AND status = 'working'
          AND action_type = 'claim'
          AND timestamp > NOW() - INTERVAL '2 hours'
        ORDER BY timestamp DESC LIMIT 1;
    """, (resource,))

    existing_claim = cur.fetchone()

    if existing_claim and existing_claim[0] != agent_name:
        # Resource already claimed by another agent
        print(f"❌ Conflict: {resource} claimed by {existing_claim[0]}")

        # Log conflict
        cur.execute("""
            INSERT INTO error_log (
                agent_name, error_type, error_message, severity
            ) VALUES (%s, %s, %s, %s)
        """, (
            agent_name,
            'conflict',
            f'Attempted to claim {resource} but already claimed by {existing_claim[0]}',
            'medium'
        ))
        conn.commit()
        return False

    # Claim it
    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log (
            agent_name, action_type, resource_claim, status,
            message, metadata, check_in_time, next_check_in
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        agent_name,
        'claim',
        resource,
        'working',
        f'Claimed {resource} - ETA {estimated_minutes} minutes',
        json.dumps({'estimated_minutes': estimated_minutes}),
        datetime.now(),
        datetime.now() + timedelta(minutes=10)
    ))
    conn.commit()

    print(f"✅ Claimed: {resource}")
    return True
```

### During Work: Regular Check-Ins

```python
def check_in(agent_name, resource, progress_percent, message):
    """
    Report progress every 10 minutes while working.
    Also checks if any other agent needs help.
    """
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Update progress
    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log (
            agent_name, action_type, resource_claim, status,
            message, metadata, check_in_time, next_check_in
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        agent_name,
        'progress',
        resource,
        'working',
        message,
        json.dumps({'progress_percent': progress_percent}),
        datetime.now(),
        datetime.now() + timedelta(minutes=10)
    ))
    conn.commit()

    # Check for help requests (in case priorities changed)
    cur.execute("""
        SELECT COUNT(*) FROM ascent_basecamp_agent_log
        WHERE action_type = 'help'
          AND status IN ('blocked', 'waiting')
          AND metadata->>'help_needed_from' = %s
          AND timestamp > NOW() - INTERVAL '1 hour'
    """, (agent_name,))

    help_count = cur.fetchone()[0]
    if help_count > 0:
        print(f"⚠️ {help_count} new help requests! Consider pausing current work.")

    conn.close()
```

### After Completing Work

```python
def release_resource(agent_name, resource, outcome_message):
    """
    Release resource when done, log completion.
    """
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log (
            agent_name, action_type, resource_claim, status,
            message, check_in_time
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        agent_name,
        'complete',
        resource,
        'done',
        outcome_message,
        datetime.now()
    ))
    conn.commit()

    print(f"✅ Released: {resource}")

    # Update work queue (mark task as done)
    queue_file = f'agent_work_queues/{agent_name.lower()}_queue.md'
    # (Implementation: convert [ ] to [x] for completed task)

    conn.close()
```

---

## Handoff Protocol (Agent-to-Agent Dependencies)

### Scenario: Alpha needs ghost cohort data from Gamma

**Alpha's code:**
```python
# Alpha realizes they need Gamma's help
def request_help(agent_name, help_from, reason, priority='medium'):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log (
            agent_name, action_type, status, message, metadata
        ) VALUES (%s, %s, %s, %s, %s)
    """, (
        agent_name,
        'help',
        'blocked',
        reason,
        json.dumps({
            'help_needed_from': help_from,
            'priority': priority,
            'task_blocked': 'module_enhancement'
        })
    ))
    conn.commit()

    print(f"📨 Help requested from {help_from}")
    print(f"   Reason: {reason}")
    print(f"   I'll check back in 30 minutes...")

    # Alpha pauses this task and works on something else
    # Or Alpha goes idle and waits

# Alpha calls this
request_help(
    agent_name='alpha',
    help_from='gamma',
    reason='Need ghost cohort data for power modules before adding race metadata',
    priority='high'
)
```

**Gamma's code (runs every startup):**
```python
# Gamma checks for help requests at startup
cur.execute("""
    SELECT log_id, agent_name, message, metadata, timestamp
    FROM ascent_basecamp_agent_log
    WHERE action_type = 'help'
      AND status = 'blocked'
      AND metadata->>'help_needed_from' = 'gamma'
    ORDER BY
        CASE metadata->>'priority'
            WHEN 'high' THEN 1
            WHEN 'medium' THEN 2
            ELSE 3
        END,
        timestamp ASC
    LIMIT 5;
""")

help_requests = cur.fetchall()

if help_requests:
    # Gamma prioritizes helping others
    top_request = help_requests[0]

    print(f"⚠️ {top_request['agent_name']} needs help!")
    print(f"   {top_request['message']}")
    print(f"   I'll work on this first.")

    # Gamma responds
    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log (
            agent_name, action_type, status, message, metadata
        ) VALUES (%s, %s, %s, %s, %s)
    """, (
        'gamma',
        'claim',
        'working',
        f'Working on help request from {top_request["agent_name"]} - ETA 30 minutes',
        json.dumps({'responding_to_log_id': top_request['log_id']})
    ))
    conn.commit()

    # Gamma works on populating ghost cohorts...
    # When done, Gamma updates the original help request

    cur.execute("""
        UPDATE ascent_basecamp_agent_log
        SET status = 'resolved',
            resolution = 'Ghost cohorts populated for power subsystem'
        WHERE log_id = %s
    """, (top_request['log_id'],))

    # Gamma also logs completion
    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log (
            agent_name, action_type, status, message
        ) VALUES (%s, %s, %s, %s)
    """, (
        'gamma',
        'complete',
        'done',
        f'Completed help request for {top_request["agent_name"]} - ghost cohorts ready'
    ))
    conn.commit()
```

**Alpha's code (checks periodically):**
```python
# Every 10 minutes, Alpha checks if help request was resolved
cur.execute("""
    SELECT resolution FROM ascent_basecamp_agent_log
    WHERE agent_name = 'alpha'
      AND action_type = 'help'
      AND message LIKE '%ghost cohort%'
      AND status = 'resolved'
    ORDER BY timestamp DESC LIMIT 1;
""")

result = cur.fetchone()
if result:
    print(f"✅ My help request was resolved!")
    print(f"   Resolution: {result['resolution']}")
    print(f"   I can continue my work now.")

    # Alpha resumes module enhancement with race metadata
```

---

## Error Logging for Liz's Visibility

Every error gets logged to `error_log` table:

```python
def log_error(agent_name, error_type, error_message, severity='medium', stack_trace=None):
    """
    Log errors for Liz to review in Notion.
    """
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO error_log (
            agent_name, error_type, error_message,
            stack_trace, severity, resolution_status
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        agent_name,
        error_type,
        error_message,
        stack_trace,
        severity,
        'unresolved'
    ))
    conn.commit()
    conn.close()

# Usage examples:
log_error('alpha', 'dependency', 'Cannot enhance modules without ghost cohort data', 'medium')
log_error('beta', 'code_error', 'API endpoint failing: 500 error', 'high', traceback_str)
log_error('gamma', 'timeout', 'Notion API not responding after 30s', 'critical')
```

---

## Technical Decisions Tracking

Any architectural decision gets logged:

```python
def log_decision(agent_name, decision_type, decision, rationale, impact='medium'):
    """
    Log technical decisions for Liz to review and approve.
    """
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO technical_decisions (
            agent_name, decision_type, decision,
            rationale, impact, status
        ) VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING decision_id;
    """, (
        agent_name,
        decision_type,
        decision,
        rationale,
        impact,
        'proposed'
    ))

    decision_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    print(f"📝 Decision logged (ID: {decision_id}) - awaiting approval")
    return decision_id

# Usage:
log_decision(
    agent_name='beta',
    decision_type='api_design',
    decision='Use JWT tokens for authentication instead of session cookies',
    rationale='Better for React SPA, enables stateless API, easier to scale',
    impact='high'
)

# Liz can review in Notion and approve/reject
```

---

## Daily Summary Protocol

At end of work session, each agent writes to AGENT_TEAM_CHAT.md:

```python
def write_daily_summary(agent_name, session_number, completed, next_tasks, messages, blockers, metrics):
    """
    Append daily summary to team chat.
    """
    summary = f"""
## Agent {agent_name.capitalize()} - Session #{session_number}

### What I Completed Today
{completed}

### What I'm Working On Next
{next_tasks}

### Messages for Other Agents
{messages}

### Blockers
{blockers}

### Metrics
{metrics}

---
"""

    with open('AGENT_TEAM_CHAT.md', 'a') as f:
        f.write(summary)

    print(f"✅ Daily summary written to AGENT_TEAM_CHAT.md")

# Usage:
write_daily_summary(
    agent_name='alpha',
    session_number=4,
    completed="- Enhanced 5 power modules with race metadata\n- Built prerequisite graph for 20 modules",
    next_tasks="- Continue with avionics modules\n- Add difficulty calibrations",
    messages="**To Gamma:** Thanks for ghost cohort data!\n**To Beta:** Power modules ready for testing",
    blockers="None",
    metrics="- Modules enhanced: 5\n- Database writes: 47\n- Time: 2.5 hours"
)
```

---

## Notion Sync Integration

The sync daemon (already created) automatically syncs to Notion:

**New tables to add to sync:**
```python
# In notion_continuous_sync.py, add:

def sync_error_log():
    """Sync recent errors to Notion Error Log dashboard"""
    cur.execute("""
        SELECT * FROM error_log
        WHERE timestamp > NOW() - INTERVAL '7 days'
        ORDER BY timestamp DESC LIMIT 100;
    """)
    # ... sync to Notion

def sync_technical_decisions():
    """Sync decisions to Notion Technical Decisions dashboard"""
    cur.execute("""
        SELECT * FROM technical_decisions
        WHERE status = 'proposed'
        ORDER BY timestamp DESC;
    """)
    # ... sync to Notion (Liz can approve/reject here)
```

---

## What Liz Sees in Notion

### 1. Agent Activity Dashboard (Real-time)
| Agent | Status | Current Task | Progress | Last Check-In | Next Check-In |
|-------|--------|--------------|----------|---------------|---------------|
| Alpha | 🟢 Working | modules/power/* | 60% | 2m ago | in 8m |
| Beta | 🟢 Working | backend/lms_routes.py | 80% | 1m ago | in 9m |
| Gamma | 🟡 Idle | (waiting) | 100% | 5m ago | in 5m |

### 2. Error Log Dashboard
| Time | Agent | Type | Message | Severity | Status |
|------|-------|------|---------|----------|--------|
| 14:45 | Beta | code_error | API endpoint 500 | High | Unresolved |
| 14:30 | Alpha | dependency | Need ghost cohorts | Medium | Resolved |

### 3. Technical Decisions Dashboard
| Time | Agent | Decision | Impact | Status | Actions |
|------|-------|----------|--------|--------|---------|
| 14:20 | Beta | Use JWT auth | High | Proposed | [Approve] [Reject] |
| 13:50 | Gamma | Redis for caching | Medium | Approved | - |

### 4. Resource Claims Dashboard
| Resource | Agent | Status | Started | ETA |
|----------|-------|--------|---------|-----|
| modules/power/* | Alpha | Working | 14:30 | 15:00 |
| backend/lms_routes.py | Beta | Working | 14:35 | 15:30 |

---

## Agent Session Script Template

Each agent runs this script to work autonomously:

```python
# alpha_session.py (example)

import os
import sys
import time
from datetime import datetime, timedelta
from agent_utils import (
    startup_protocol,
    claim_resource,
    check_in,
    release_resource,
    request_help,
    log_error,
    log_decision,
    write_daily_summary
)

AGENT_NAME = 'alpha'
SESSION_NUMBER = 4
CHECK_IN_INTERVAL = 600  # 10 minutes

def main():
    print(f"=== Agent {AGENT_NAME.upper()} Starting ===")

    # Startup protocol
    context = startup_protocol(AGENT_NAME)

    # Decide what to work on
    if context['help_requests']:
        # Help another agent first
        work_on_help_request(context['help_requests'][0])
    elif context['my_tasks']:
        # Work on next task from queue
        work_on_next_task(context['my_tasks'][0])
    else:
        # Idle
        print("No tasks. Going idle.")
        time.sleep(CHECK_IN_INTERVAL)

    # End of session summary
    write_daily_summary(
        agent_name=AGENT_NAME,
        session_number=SESSION_NUMBER,
        completed="...",
        next_tasks="...",
        messages="...",
        blockers="None",
        metrics="..."
    )

def work_on_next_task(task):
    """
    Work on a task from the queue with regular check-ins.
    """
    resource = task['resource']

    # Claim resource
    if not claim_resource(AGENT_NAME, resource, estimated_minutes=60):
        print("Resource conflict - skipping")
        return

    try:
        # Do work with periodic check-ins
        start_time = time.time()
        last_check_in = start_time

        while True:
            # ... do actual work ...

            # Check in every 10 minutes
            if time.time() - last_check_in > CHECK_IN_INTERVAL:
                check_in(
                    AGENT_NAME,
                    resource,
                    progress_percent=calculate_progress(),
                    message="Making progress..."
                )
                last_check_in = time.time()

            # Check if done
            if work_complete():
                break

        # Release resource
        release_resource(AGENT_NAME, resource, "Task completed successfully")

    except Exception as e:
        # Log error
        log_error(
            AGENT_NAME,
            'code_error',
            str(e),
            severity='high',
            stack_trace=traceback.format_exc()
        )
        release_resource(AGENT_NAME, resource, f"Failed with error: {str(e)}")

if __name__ == '__main__':
    main()
```

---

## Next Steps

1. **Create database tables** (technical_decisions, error_log)
2. **Create agent utility library** (`agent_utils.py` with all helper functions)
3. **Create session scripts** for each agent (`alpha_session.py`, `beta_session.py`, `gamma_session.py`)
4. **Update Notion sync daemon** to include error log and decisions
5. **Test with all three agents** running simultaneously

Should I start building these components?
