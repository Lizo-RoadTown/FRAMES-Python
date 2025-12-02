# DEPRECATED

**This file is no longer canonical.**

**Replaced by:** (Being rewritten for V2)
**Reason:** Agent roles based on outdated conceptual model

**Archived:** 2025-12-01

---

# Agent System Overview

## Architecture

FRAMES uses a three-agent autonomous system for parallel development:

```
┌──────────────────────────────────────────────────────────────┐
│                        Human Oversight                        │
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
        │Agent Alpha  │ │ Agent Beta  │ │Agent Gamma  │
        │(Module      │ │(Platform    │ │(Infra-      │
        │ Creator)    │ │ Developer)  │ │ structure)  │
        └─────────────┘ └─────────────┘ └─────────────┘
         Works on:       Works on:       Works on:
         modules/*       backend/        scripts/
         enhancement     frontend/       infrastructure
```

## Key Principles

**Asynchronous Coordination:** Agents NEVER directly communicate. They coordinate through:
1. **Database tables** - Real-time status and work claims
2. **Shared files** - Daily summaries and task queues
3. **Notion dashboards** - Human monitoring

**Agent Boundaries:**
- Hard schema constraints
- Strict command interfaces
- Explicit user overrides only

**Prohibited Actions:**
- Modify architecture without approval
- Self-replicate
- Create Notion structures without permission
- Delete system files

## Database Schema for Coordination

### Agent Log Table
```sql
ALTER TABLE ascent_basecamp_agent_log
ADD COLUMN IF NOT EXISTS resource_claim VARCHAR(255),
ADD COLUMN IF NOT EXISTS session_id VARCHAR(100),
ADD COLUMN IF NOT EXISTS check_in_time TIMESTAMP,
ADD COLUMN IF NOT EXISTS next_check_in TIMESTAMP;
```

### Technical Decisions Table
```sql
CREATE TABLE IF NOT EXISTS technical_decisions (
    decision_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_name VARCHAR(100),
    decision_type VARCHAR(100), -- 'architecture', 'api_design', 'data_model'
    decision TEXT NOT NULL,
    rationale TEXT,
    alternatives_considered TEXT,
    impact VARCHAR(50), -- 'low', 'medium', 'high'
    status VARCHAR(50) DEFAULT 'proposed', -- 'proposed', 'approved', 'implemented'
    metadata JSONB
);
```

### Error Log Table
```sql
CREATE TABLE IF NOT EXISTS error_log (
    error_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_name VARCHAR(100),
    error_type VARCHAR(100), -- 'conflict', 'dependency', 'code_error', 'timeout'
    error_message TEXT NOT NULL,
    stack_trace TEXT,
    resolution_status VARCHAR(50) DEFAULT 'unresolved',
    resolution TEXT,
    severity VARCHAR(50), -- 'low', 'medium', 'high', 'critical'
    metadata JSONB
);
```

## Agent Startup Protocol

Every agent follows this sequence on startup:

### 1. Announce Presence
```python
import uuid
from datetime import datetime, timedelta
from shared.agent_utils import get_db_connection

# Generate unique session ID
session_id = f"{agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

# Log startup
conn = get_db_connection()
cur = conn.cursor()
cur.execute("""
    INSERT INTO ascent_basecamp_agent_log (
        agent_name, action_type, status, session_id,
        check_in_time, next_check_in, message
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
""", (agent_name, 'startup', 'ready', session_id,
      datetime.now(), datetime.now() + timedelta(minutes=10),
      f'{agent_name} online - session {session_id}'))
conn.commit()
```

### 2. Check for Active Resource Claims
```python
# See what other agents are working on
cur.execute("""
    SELECT agent_name, resource_claim, status, timestamp
    FROM ascent_basecamp_agent_log
    WHERE action_type = 'claim' AND status = 'working'
      AND agent_name != %s
      AND timestamp > NOW() - INTERVAL '2 hours'
    ORDER BY timestamp DESC;
""", (agent_name,))
active_claims = cur.fetchall()
```

### 3. Check for Help Requests
```python
# See if any agent needs help
cur.execute("""
    SELECT log_id, agent_name, message, metadata, timestamp
    FROM ascent_basecamp_agent_log
    WHERE action_type = 'help' AND status IN ('blocked', 'waiting')
      AND metadata->>'help_needed_from' = %s
      AND timestamp > NOW() - INTERVAL '24 hours'
    ORDER BY timestamp DESC;
""", (agent_name,))
help_requests = cur.fetchall()
```

### 4. Read Work Queue
```python
# Read assigned tasks
queue_file = f'agent_work_queues/{agent_name.lower()}_queue.md'
with open(queue_file, 'r') as f:
    my_queue = f.read()

# Parse uncompleted tasks
import re
tasks = re.findall(r'- \[ \] (.+)', my_queue)
```

## Work Execution Protocol

### Claim Resource Before Work
```python
def claim_resource(agent_name, resource, estimated_minutes=30):
    """Claim a resource before working on it."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if already claimed
    cur.execute("""
        SELECT agent_name FROM ascent_basecamp_agent_log
        WHERE resource_claim = %s AND status = 'working'
          AND action_type = 'claim'
          AND timestamp > NOW() - INTERVAL '2 hours'
        ORDER BY timestamp DESC LIMIT 1;
    """, (resource,))
    
    existing_claim = cur.fetchone()
    if existing_claim and existing_claim[0] != agent_name:
        # Conflict detected
        log_error(agent_name, 'conflict',
                  f'Resource {resource} claimed by {existing_claim[0]}',
                  'medium')
        return False
    
    # Claim it
    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log (
            agent_name, action_type, resource_claim, status,
            message, check_in_time, next_check_in
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (agent_name, 'claim', resource, 'working',
          f'Claimed {resource} - ETA {estimated_minutes}m',
          datetime.now(), datetime.now() + timedelta(minutes=10)))
    conn.commit()
    return True
```

### Regular Check-Ins During Work
```python
def check_in(agent_name, resource, progress_percent, message):
    """Report progress every 10 minutes."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log (
            agent_name, action_type, resource_claim, status,
            message, metadata, check_in_time, next_check_in
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (agent_name, 'progress', resource, 'working', message,
          json.dumps({'progress_percent': progress_percent}),
          datetime.now(), datetime.now() + timedelta(minutes=10)))
    conn.commit()
```

### Release Resource After Completion
```python
def release_resource(agent_name, resource, outcome_message):
    """Release resource when done."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log (
            agent_name, action_type, resource_claim, status,
            message, check_in_time
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (agent_name, 'complete', resource, 'done',
          outcome_message, datetime.now()))
    conn.commit()
```

## Handoff Protocol (Agent Dependencies)

### Request Help
```python
def request_help(agent_name, help_from, reason, priority='medium'):
    """Request help from another agent."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log (
            agent_name, action_type, status, message, metadata
        ) VALUES (%s, %s, %s, %s, %s)
    """, (agent_name, 'help', 'blocked', reason,
          json.dumps({'help_needed_from': help_from, 'priority': priority})))
    conn.commit()
```

### Respond to Help Request
```python
# Check for help requests at startup
cur.execute("""
    SELECT log_id, agent_name, message, metadata
    FROM ascent_basecamp_agent_log
    WHERE action_type = 'help' AND status = 'blocked'
      AND metadata->>'help_needed_from' = %s
    ORDER BY CASE metadata->>'priority'
        WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
        timestamp ASC LIMIT 5;
""", (agent_name,))

# When resolved, update status
cur.execute("""
    UPDATE ascent_basecamp_agent_log
    SET status = 'resolved', resolution = %s
    WHERE log_id = %s
""", (resolution_message, request_log_id))
```

## Error Logging

```python
def log_error(agent_name, error_type, error_message, severity='medium', stack_trace=None):
    """Log errors for human review."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO error_log (
            agent_name, error_type, error_message,
            stack_trace, severity, resolution_status
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (agent_name, error_type, error_message,
          stack_trace, severity, 'unresolved'))
    conn.commit()
```

## Technical Decision Logging

```python
def log_decision(agent_name, decision_type, decision, rationale, impact='medium'):
    """Log technical decisions for approval."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO technical_decisions (
            agent_name, decision_type, decision, rationale, impact, status
        ) VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING decision_id;
    """, (agent_name, decision_type, decision, rationale, impact, 'proposed'))
    decision_id = cur.fetchone()[0]
    conn.commit()
    return decision_id
```

## Daily Summary Protocol

```python
def write_daily_summary(agent_name, session_number, completed, next_tasks, 
                       messages, blockers, metrics):
    """Append daily summary to team chat."""
    summary = f"""
## Agent {agent_name.capitalize()} - Session #{session_number}

### Completed
{completed}

### Next Tasks
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
```

## Notion Dashboard Integration

Human oversight via real-time dashboards:

### Agent Activity Dashboard
- Current status (working/idle/blocked)
- Active resource claims
- Progress percentages
- Last check-in times

### Error Log Dashboard
- Recent errors by severity
- Resolution status
- Stack traces for debugging

### Technical Decisions Dashboard
- Proposed decisions awaiting approval
- Impact assessment
- Approve/reject actions

### Resource Claims Dashboard
- What each agent is working on
- Estimated completion times
- Conflict detection
