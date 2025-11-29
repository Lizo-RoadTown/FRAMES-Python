"""
Agent Utility Library for Autonomous Multi-Agent Coordination

Used by three independent Claude Code sessions (Alpha, Beta, Gamma)
to coordinate work through shared database and files.
"""

import os
import json
import uuid
import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta
from dotenv import load_dotenv
import traceback

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(DATABASE_URL)


def startup_protocol(agent_name):
    """
    Execute startup protocol for an agent.
    Returns context dictionary with messages, tasks, claims, etc.

    Returns:
        dict: {
            'session_id': str,
            'my_messages': list,
            'active_claims': list,
            'help_requests': list,
            'my_tasks': list,
            'capability_level': str,
            'supervision_level': str,
            'needs_review': bool
        }
    """
    print(f"\n{'='*60}")
    print(f"Agent {agent_name.upper()} Starting Up")
    print(f"{'='*60}\n")

    # Step 1: Generate session ID and announce presence
    session_id = f"{agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check agent capabilities
    cur.execute("""
        SELECT capability_level, supervision_level, needs_review
        FROM agent_capabilities
        WHERE agent_name = %s;
    """, (agent_name,))

    capability = cur.fetchone()
    if capability:
        capability_level = capability['capability_level']
        supervision_level = capability['supervision_level']
        needs_review = capability['needs_review']

        print(f"[CAPABILITY] Level: {capability_level}")
        print(f"[SUPERVISION] Level: {supervision_level}")
        if needs_review:
            print("[NOTICE] This agent requires review of major decisions")
    else:
        capability_level = 'standard'
        supervision_level = 'normal'
        needs_review = False

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

    print(f"[OK] Session ID: {session_id}")

    # Step 2: Read team chat for messages
    print("\n[Step 2] Reading team chat for messages...")
    my_messages = []
    try:
        with open('AGENT_TEAM_CHAT.md', 'r') as f:
            team_chat = f.read()
            for line in team_chat.split('\n'):
                if f'**To {agent_name.capitalize()}:**' in line:
                    my_messages.append(line)

        print(f"   Found {len(my_messages)} messages for me")
        for msg in my_messages:
            print(f"   - {msg}")
    except FileNotFoundError:
        print("   [WARN] AGENT_TEAM_CHAT.md not found")

    # Step 3: Check active resource claims by other agents
    print("\n[Step 3] Checking active resource claims...")
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
    print(f"   Found {len(active_claims)} active claims by other agents")
    for claim in active_claims:
        print(f"   - {claim['agent_name']} working on {claim['resource_claim']}")

    # Step 4: Check for help requests directed at me
    print("\n[Step 4] Checking for help requests...")
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
        print(f"   [ALERT] {len(help_requests)} help requests waiting for me!")
        for req in help_requests:
            print(f"   - From {req['agent_name']}: {req['message']}")
    else:
        print("   No pending help requests")

    # Step 5: Read my work queue
    print("\n[Step 5] Reading work queue...")
    my_tasks = []
    queue_file = f'agent_work_queues/{agent_name.lower()}_queue.md'
    try:
        with open(queue_file, 'r') as f:
            queue_content = f.read()

            # Parse uncompleted tasks (look for [ ] checkbox)
            import re
            task_matches = re.finditer(r'- \[ \] (.+)', queue_content)
            for match in task_matches:
                task_text = match.group(1)
                my_tasks.append({'text': task_text, 'checked': False})

        print(f"   Found {len(my_tasks)} pending tasks")
        if my_tasks:
            print(f"   Next task: {my_tasks[0]['text']}")
    except FileNotFoundError:
        print(f"   [WARN] Queue file not found: {queue_file}")

    conn.close()

    # Return context
    context = {
        'session_id': session_id,
        'my_messages': my_messages,
        'active_claims': [dict(c) for c in active_claims],
        'help_requests': [dict(r) for r in help_requests],
        'my_tasks': my_tasks,
        'capability_level': capability_level,
        'supervision_level': supervision_level,
        'needs_review': needs_review
    }

    print(f"\n{'='*60}")
    print("Startup Complete")
    if needs_review:
        print("[REMINDER] Major decisions require Liz's approval before implementing")
    print(f"{'='*60}\n")

    return context


def claim_resource(agent_name, resource, estimated_minutes=30):
    """
    Claim a resource before working on it.

    Args:
        agent_name: Name of agent claiming resource
        resource: Resource identifier (file path, table name, etc.)
        estimated_minutes: Estimated time to complete

    Returns:
        bool: True if claim successful, False if conflict
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

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

    if existing_claim and existing_claim['agent_name'] != agent_name:
        # Resource already claimed by another agent
        print(f"[CONFLICT] {resource} already claimed by {existing_claim['agent_name']}")

        # Log conflict
        cur.execute("""
            INSERT INTO error_log (
                agent_name, error_type, error_message, severity
            ) VALUES (%s, %s, %s, %s)
        """, (
            agent_name,
            'conflict',
            f'Attempted to claim {resource} but already claimed by {existing_claim["agent_name"]}',
            'medium'
        ))
        conn.commit()
        conn.close()
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
    conn.close()

    print(f"[CLAIMED] {resource} (ETA: {estimated_minutes} min)")
    return True


def check_in(agent_name, resource, progress_percent, message, metadata=None):
    """
    Report progress while working on a resource.

    Args:
        agent_name: Name of agent
        resource: Resource being worked on
        progress_percent: Progress percentage (0-100)
        message: Status message
        metadata: Optional dict of additional data
    """
    conn = get_db_connection()
    cur = conn.cursor()

    if metadata is None:
        metadata = {}

    metadata['progress_percent'] = progress_percent

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
        json.dumps(metadata),
        datetime.now(),
        datetime.now() + timedelta(minutes=10)
    ))
    conn.commit()

    # Check for new help requests
    cur.execute("""
        SELECT COUNT(*) FROM ascent_basecamp_agent_log
        WHERE action_type = 'help'
          AND status IN ('blocked', 'waiting')
          AND metadata->>'help_needed_from' = %s
          AND timestamp > NOW() - INTERVAL '1 hour'
    """, (agent_name,))

    help_count = cur.fetchone()[0]
    conn.close()

    print(f"[CHECK-IN] {resource} - {progress_percent}% - {message}")

    if help_count > 0:
        print(f"   [ALERT] {help_count} new help requests! Consider pausing current work.")

    return help_count > 0


def release_resource(agent_name, resource, outcome_message, metadata=None):
    """
    Release resource when done.

    Args:
        agent_name: Name of agent
        resource: Resource to release
        outcome_message: Description of outcome
        metadata: Optional dict with results
    """
    conn = get_db_connection()
    cur = conn.cursor()

    if metadata is None:
        metadata = {}

    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log (
            agent_name, action_type, resource_claim, status,
            message, metadata, check_in_time
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        agent_name,
        'complete',
        resource,
        'done',
        outcome_message,
        json.dumps(metadata),
        datetime.now()
    ))
    conn.commit()
    conn.close()

    print(f"[RELEASED] {resource} - {outcome_message}")


def request_help(agent_name, help_from, reason, priority='medium', metadata=None):
    """
    Request help from another agent.

    Args:
        agent_name: Name of requesting agent
        help_from: Name of agent to request help from
        reason: Description of what's needed
        priority: 'low', 'medium', 'high'
        metadata: Optional dict with additional context

    Returns:
        int: log_id of help request
    """
    conn = get_db_connection()
    cur = conn.cursor()

    if metadata is None:
        metadata = {}

    metadata['help_needed_from'] = help_from
    metadata['priority'] = priority

    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log (
            agent_name, action_type, status, message, metadata
        ) VALUES (%s, %s, %s, %s, %s)
        RETURNING log_id;
    """, (
        agent_name,
        'help',
        'blocked',
        reason,
        json.dumps(metadata)
    ))

    log_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    print(f"[HELP REQUESTED] From {help_from}")
    print(f"   Reason: {reason}")
    print(f"   Priority: {priority}")
    print(f"   Request ID: {log_id}")

    return log_id


def resolve_help_request(agent_name, request_log_id, resolution_message):
    """
    Mark a help request as resolved.

    Args:
        agent_name: Name of agent resolving request
        request_log_id: ID of original help request
        resolution_message: Description of resolution
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE ascent_basecamp_agent_log
        SET status = 'resolved',
            resolution = %s
        WHERE log_id = %s;
    """, (resolution_message, request_log_id))

    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log (
            agent_name, action_type, status, message, metadata
        ) VALUES (%s, %s, %s, %s, %s)
    """, (
        agent_name,
        'complete',
        'done',
        f'Resolved help request #{request_log_id}',
        json.dumps({'resolved_request_id': request_log_id})
    ))

    conn.commit()
    conn.close()

    print(f"[RESOLVED] Help request #{request_log_id} - {resolution_message}")


def log_error(agent_name, error_type, error_message, severity='medium', stack_trace=None, metadata=None):
    """
    Log an error for Liz to review.

    Args:
        agent_name: Name of agent
        error_type: Type of error ('conflict', 'dependency', 'code_error', 'timeout')
        error_message: Description of error
        severity: 'low', 'medium', 'high', 'critical'
        stack_trace: Optional stack trace
        metadata: Optional dict with additional context

    Returns:
        int: error_id
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO error_log (
            agent_name, error_type, error_message,
            stack_trace, severity, resolution_status, metadata
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING error_id;
    """, (
        agent_name,
        error_type,
        error_message,
        stack_trace,
        severity,
        'unresolved',
        json.dumps(metadata) if metadata else None
    ))

    error_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    print(f"[ERROR LOGGED] #{error_id} - {error_type} - {severity}")
    print(f"   {error_message}")

    return error_id


def log_decision(agent_name, decision_type, decision, rationale, impact='medium', alternatives=None, metadata=None):
    """
    Log a technical decision for Liz to review/approve.

    Args:
        agent_name: Name of agent
        decision_type: Type of decision ('architecture', 'api_design', 'data_model', etc.)
        decision: The decision made
        rationale: Why this decision was made
        impact: 'low', 'medium', 'high'
        alternatives: Optional description of alternatives considered
        metadata: Optional dict with additional context

    Returns:
        int: decision_id
    """
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO technical_decisions (
            agent_name, decision_type, decision,
            rationale, alternatives_considered, impact, status, metadata
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING decision_id;
    """, (
        agent_name,
        decision_type,
        decision,
        rationale,
        alternatives,
        impact,
        'proposed',
        json.dumps(metadata) if metadata else None
    ))

    decision_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    print(f"[DECISION LOGGED] #{decision_id} - {decision_type} - {impact} impact")
    print(f"   Decision: {decision}")
    print(f"   Rationale: {rationale}")

    return decision_id


def write_daily_summary(agent_name, session_number, completed, next_tasks, messages, blockers, metrics):
    """
    Append daily summary to team chat.

    Args:
        agent_name: Name of agent
        session_number: Session number
        completed: String describing completed work
        next_tasks: String describing next tasks
        messages: String with messages for other agents
        blockers: String describing any blockers
        metrics: String with quantitative metrics
    """
    summary = f"""
## Agent {agent_name.capitalize()} - Session #{session_number}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

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

    try:
        with open('AGENT_TEAM_CHAT.md', 'a', encoding='utf-8') as f:
            f.write(summary)

        print(f"[SUMMARY WRITTEN] Daily summary added to AGENT_TEAM_CHAT.md")
    except Exception as e:
        print(f"[ERROR] Failed to write summary: {e}")


if __name__ == '__main__':
    # Test the utilities
    print("Testing agent utilities...")

    # Test startup
    context = startup_protocol('test_agent')
    print(f"\nContext: {context}")
