"""
Continuous Neon → Notion Sync Daemon
Syncs database tables to Notion dashboards every 30-120 seconds

This is the CRITICAL piece that lets Liz monitor all three agents in real-time.
"""

import os
import sys
import time
import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta
from notion_client import Client
from dotenv import load_dotenv, set_key
from pathlib import Path
import json

# Force UTF-8 output so Windows console prints without encoding errors
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Load environment
load_dotenv()
ENV_PATH = Path('.env')

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL')
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_PARENT_PAGE_ID = os.getenv('NOTION_PARENT_PAGE_ID')

# Notion client
notion = Client(auth=NOTION_API_KEY)

# Sync intervals (seconds)
AGENT_LOG_SYNC_INTERVAL = 30      # Real-time agent activity
DASHBOARD_SYNC_INTERVAL = 120     # Team/project dashboards
MODULE_SYNC_INTERVAL = 300        # Module library

# Notion Database IDs (will be created if not exist)
NOTION_DBS = {
    'agent_activity': None,
    'resource_claims': None,
    'team_dashboard': None,
    'project_dashboard': None,
    'task_dashboard': None,
    'module_library': None,
}

# Notion Data Source IDs (used for querying pages)
NOTION_DS = {
    'agent_activity': None,
    'resource_claims': None,
    'team_dashboard': None,
    'project_dashboard': None,
    'task_dashboard': None,
    'module_library': None,
}


def load_ids_from_env():
    """Populate database/data source IDs from .env if present."""
    for key in NOTION_DBS.keys():
        db_env = os.getenv(f'NOTION_DB_{key.upper()}')
        ds_env = os.getenv(f'NOTION_DS_{key.upper()}')
        if db_env:
            NOTION_DBS[key] = db_env
        if ds_env:
            NOTION_DS[key] = ds_env


load_ids_from_env()


def query_data_source(data_source_id, **kwargs):
    """Call the data_sources/{id}/query endpoint."""
    if not data_source_id:
        raise ValueError("Missing Notion data source ID - run setup first.")
    auth = kwargs.pop("auth", None)
    body = kwargs or {}
    return notion.request(
        path=f"data_sources/{data_source_id}/query",
        method="POST",
        body=body,
        auth=auth,
    )

# Track last sync times
last_sync = {
    'agent_logs': None,
    'dashboards': None,
    'modules': None,
}


def get_db_connection():
    """Get PostgreSQL connection"""
    return psycopg2.connect(DATABASE_URL)


def create_notion_database(parent_page_id, title, properties):
    """
    Create a Notion database if it doesn't exist

    Args:
        parent_page_id: Parent page ID
        title: Database title
        properties: Dict of property definitions

    Returns:
        Tuple(database_id, data_source_id)
    """
    try:
        db = notion.databases.create(
            parent={'type': 'page_id', 'page_id': parent_page_id},
            title=[{'type': 'text', 'text': {'content': title}}],
            properties=properties
        )

        data_source_id = None
        data_sources = db.get('data_sources') or []
        if data_sources:
            data_source_id = data_sources[0].get('id')

        print(f"[OK] Created Notion database: {title} (ID: {db['id']})")
        return db['id'], data_source_id

    except Exception as e:
        print(f"[ERROR] Error creating database {title}: {e}")
        return None, None


def register_database(key, title, properties):
    """
    Ensure a Notion database exists with the expected schema.
    Updates existing databases or creates new ones if needed.
    """
    existing_id = NOTION_DBS.get(key)

    if existing_id:
        try:
            db = notion.databases.update(
                database_id=existing_id,
                title=[{'type': 'text', 'text': {'content': title}}],
                properties=properties
            )
            data_sources = db.get('data_sources') or []
            if data_sources:
                NOTION_DS[key] = data_sources[0].get('id')
            print(f"[OK] Updated Notion database: {title} (ID: {existing_id})")
            return existing_id, NOTION_DS.get(key)
        except Exception as exc:
            print(f"[WARN] Could not update {title} ({existing_id}): {exc}. Creating new database instead.")

    db_id, ds_id = create_notion_database(NOTION_PARENT_PAGE_ID, title, properties)
    if db_id:
        NOTION_DBS[key] = db_id
    if ds_id:
        NOTION_DS[key] = ds_id
    return db_id, ds_id


def setup_notion_databases():
    """Create all required Notion databases"""

    print("\n" + "="*60)
    print("Setting up Notion Databases")
    print("="*60 + "\n")

    # 1. Agent Activity Dashboard
    register_database(
        'agent_activity',
        'Agent Activity Dashboard',
        {
            'Agent': {'title': {}},
            'Status': {
                'select': {
                    'options': [
                        {'name': 'Working', 'color': 'green'},
                        {'name': 'Waiting', 'color': 'yellow'},
                        {'name': 'Blocked', 'color': 'red'},
                        {'name': 'Idle', 'color': 'gray'},
                    ]
                }
            },
            'Current Task': {'rich_text': {}},
            'Progress': {'number': {'format': 'percent'}},
            'Last Update': {'date': {}},
            'Blockers': {'rich_text': {}},
        }
    )

    # 2. Resource Claims Dashboard
    register_database(
        'resource_claims',
        'Resource Claims',
        {
            'Resource': {'title': {}},
            'Claimed By': {'select': {'options': [
                {'name': 'Alpha', 'color': 'blue'},
                {'name': 'Beta', 'color': 'purple'},
                {'name': 'Gamma', 'color': 'orange'},
            ]}},
            'Status': {'select': {'options': [
                {'name': 'Working', 'color': 'green'},
                {'name': 'Complete', 'color': 'gray'},
            ]}},
            'Started': {'date': {}},
            'ETA': {'date': {}},
        }
    )

    # 3. Team Dashboard
    register_database(
        'team_dashboard',
        'Team Dashboard',
        {
            'Name': {'title': {}},
            'Role': {'select': {}},
            'Subsystem': {'select': {}},
            'Email': {'email': {}},
        }
    )

    # 4. Project Dashboard
    register_database(
        'project_dashboard',
        'Project Dashboard',
        {
            'Project Name': {'title': {}},
            'Subsystem': {'select': {}},
            'Status': {'select': {'options': [
                {'name': 'Active', 'color': 'green'},
                {'name': 'In Progress', 'color': 'blue'},
                {'name': 'Completed', 'color': 'gray'},
                {'name': 'Blocked', 'color': 'red'},
            ]}},
            'Owner': {'rich_text': {}},
            'Description': {'rich_text': {}},
        }
    )

    # 5. Task Dashboard
    register_database(
        'task_dashboard',
        'Task Dashboard',
        {
            'Title': {'title': {}},
            'Status': {'select': {}},
            'Assignee': {'rich_text': {}},
            'Due Date': {'date': {}},
            'Project': {'rich_text': {}},
        }
    )

    # 6. Module Library
    register_database(
        'module_library',
        'Module Library',
        {
            'Module Name': {'title': {}},
            'Subsystem': {'select': {}},
            'Difficulty': {'select': {'options': [
                {'name': 'Beginner', 'color': 'green'},
                {'name': 'Intermediate', 'color': 'yellow'},
                {'name': 'Advanced', 'color': 'red'},
            ]}},
            'Type': {'select': {}},
            'Status': {'select': {}},
            'Created': {'date': {}},
        }
    )

    print("\nAll Notion databases created!\n")

    # Save database IDs to .env for persistence
    save_db_ids_to_env()


def ensure_data_sources_loaded():
    """Ensure data source IDs are known for every database."""
    updated = False
    for key, db_id in NOTION_DBS.items():
        if db_id and not NOTION_DS.get(key):
            try:
                db_meta = notion.databases.retrieve(database_id=db_id)
                data_sources = db_meta.get('data_sources') or []
                if data_sources:
                    NOTION_DS[key] = data_sources[0].get('id')
                    updated = True
            except Exception as exc:
                print(f"[WARN] Could not load data source for {key}: {exc}")
    if updated:
        save_db_ids_to_env()


def save_db_ids_to_env():
    """Save Notion database and data source IDs to .env"""
    if not ENV_PATH.exists():
        print("[WARN] .env file missing - cannot persist IDs")
        return
    for key, db_id in NOTION_DBS.items():
        if db_id:
            set_key(str(ENV_PATH), f"NOTION_DB_{key.upper()}", db_id, quote_mode="never")
    for key, ds_id in NOTION_DS.items():
        if ds_id:
            set_key(str(ENV_PATH), f"NOTION_DS_{key.upper()}", ds_id, quote_mode="never")
    print("Notion database IDs saved to .env")


ensure_data_sources_loaded()


def sync_agent_activity():
    """Sync agent activity from ascent_basecamp_agent_log to Notion"""

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Syncing agent activity...")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Get latest status for each agent
    cur.execute("""
        WITH latest_logs AS (
            SELECT DISTINCT ON (agent_name)
                agent_name,
                action_type,
                status,
                resource_claim,
                message,
                error,
                metadata,
                timestamp
            FROM ascent_basecamp_agent_log
            ORDER BY agent_name, timestamp DESC
        )
        SELECT * FROM latest_logs;
    """)

    agents = cur.fetchall()

    for agent in agents:
        # Calculate progress from metadata
        progress = 0
        if agent['metadata'] and 'progress_percent' in agent['metadata']:
            progress = agent['metadata']['progress_percent'] / 100.0

        # Map status to emoji
        status_map = {
            'working': '🟢 Working',
            'blocked': '🔴 Blocked',
            'waiting': '🟡 Waiting',
            'done': '⚪ Idle',
        }
        status = status_map.get(agent['status'], '⚪ Idle')

        # Upsert to Notion
        try:
            # Check if agent already has a row
            existing = query_data_source(
                NOTION_DS['agent_activity'],
                filter={
                    'property': 'Agent',
                    'title': {'equals': agent['agent_name'].capitalize()}
                }
            )

            properties = {
                'Agent': {'title': [{'text': {'content': agent['agent_name'].capitalize()}}]},
                'Status': {'select': {'name': status}},
                'Current Task': {'rich_text': [{'text': {'content': agent['resource_claim'] or 'Idle'}}]},
                'Progress': {'number': progress},
                'Last Update': {'date': {'start': agent['timestamp'].isoformat()}},
                'Blockers': {'rich_text': [{'text': {'content': agent['error'] or ''}}]},
            }

            if existing['results']:
                # Update existing row
                notion.pages.update(
                    page_id=existing['results'][0]['id'],
                    properties=properties
                )
            else:
                # Create new row
                notion.pages.create(
                    parent={'database_id': NOTION_DBS['agent_activity']},
                    properties=properties
                )

        except Exception as e:
            print(f"  ❌ Error syncing agent {agent['agent_name']}: {e}")

    cur.close()
    conn.close()

    print(f"  ✅ Synced {len(agents)} agents")


def sync_resource_claims():
    """Sync active resource claims to Notion"""

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Syncing resource claims...")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Get all active claims
    cur.execute("""
        SELECT DISTINCT ON (resource_claim)
            agent_name,
            resource_claim,
            status,
            timestamp,
            metadata
        FROM ascent_basecamp_agent_log
        WHERE action_type = 'claim'
          AND resource_claim IS NOT NULL
          AND timestamp > NOW() - INTERVAL '24 hours'
        ORDER BY resource_claim, timestamp DESC;
    """)

    claims = cur.fetchall()

    for claim in claims:
        # Calculate ETA from metadata
        eta = None
        if claim['metadata'] and 'estimated_duration_minutes' in claim['metadata']:
            eta_time = claim['timestamp'] + timedelta(minutes=claim['metadata']['estimated_duration_minutes'])
            eta = eta_time.isoformat()

        try:
            # Check if claim already exists
            existing = query_data_source(
                NOTION_DS['resource_claims'],
                filter={
                    'property': 'Resource',
                    'title': {'equals': claim['resource_claim']}
                }
            )

            properties = {
                'Resource': {'title': [{'text': {'content': claim['resource_claim']}}]},
                'Claimed By': {'select': {'name': claim['agent_name'].capitalize()}},
                'Status': {'select': {'name': 'Working' if claim['status'] == 'working' else 'Complete'}},
                'Started': {'date': {'start': claim['timestamp'].isoformat()}},
            }

            if eta:
                properties['ETA'] = {'date': {'start': eta}}

            if existing['results']:
                notion.pages.update(
                    page_id=existing['results'][0]['id'],
                    properties=properties
                )
            else:
                notion.pages.create(
                    parent={'database_id': NOTION_DBS['resource_claims']},
                    properties=properties
                )

        except Exception as e:
            print(f"  ❌ Error syncing claim {claim['resource_claim']}: {e}")

    cur.close()
    conn.close()

    print(f"  ✅ Synced {len(claims)} resource claims")


def sync_team_dashboard():
    """Sync cadence_people table to Notion Team Dashboard"""

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Syncing team dashboard...")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT * FROM cadence_people LIMIT 50;")
    people = cur.fetchall()

    for person in people:
        try:
            properties = {
                'Name': {'title': [{'text': {'content': person['name'] or 'Unknown'}}]},
                'Role': {'select': {'name': person['role'] or 'Member'}},
                'Subsystem': {'select': {'name': person['subsystem'] or 'General'}},
            }

            if person['email']:
                properties['Email'] = {'email': person['email']}

            # Check if person exists
            existing = query_data_source(
                NOTION_DS['team_dashboard'],
                filter={
                    'property': 'Name',
                    'title': {'equals': person['name']}
                }
            )

            if existing['results']:
                notion.pages.update(
                    page_id=existing['results'][0]['id'],
                    properties=properties
                )
            else:
                notion.pages.create(
                    parent={'database_id': NOTION_DBS['team_dashboard']},
                    properties=properties
                )

        except Exception as e:
            print(f"  ❌ Error syncing person {person['name']}: {e}")

    cur.close()
    conn.close()

    print(f"  ✅ Synced {len(people)} team members")


def sync_project_dashboard():
    """Sync cadence_projects table to Notion"""

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Syncing project dashboard...")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT * FROM cadence_projects LIMIT 100;")
    projects = cur.fetchall()

    for project in projects:
        try:
            properties = {
                'Project Name': {'title': [{'text': {'content': project['name'] or 'Untitled'}}]},
                'Subsystem': {'select': {'name': project['subsystem'] or 'General'}},
                'Status': {'select': {'name': project['status'] or 'Active'}},
                'Description': {'rich_text': [{'text': {'content': (project['description'] or '')[:2000]}}]},
            }

            existing = query_data_source(
                NOTION_DS['project_dashboard'],
                filter={
                    'property': 'Project Name',
                    'title': {'equals': project['name']}
                }
            )

            if existing['results']:
                notion.pages.update(
                    page_id=existing['results'][0]['id'],
                    properties=properties
                )
            else:
                notion.pages.create(
                    parent={'database_id': NOTION_DBS['project_dashboard']},
                    properties=properties
                )

        except Exception as e:
            print(f"  ❌ Error syncing project {project['name']}: {e}")

    cur.close()
    conn.close()

    print(f"  ✅ Synced {len(projects)} projects")


def sync_module_library():
    """Sync modules table to Notion"""

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Syncing module library...")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT * FROM modules ORDER BY created_at DESC LIMIT 100;")
    modules = cur.fetchall()

    for module in modules:
        try:
            properties = {
                'Module Name': {'title': [{'text': {'content': module['title'] or 'Untitled'}}]},
                'Subsystem': {'select': {'name': module['subsystem'] or 'General'}},
                'Difficulty': {'select': {'name': module['difficulty'] or 'Intermediate'}},
                'Type': {'select': {'name': module['module_type'] or 'Core'}},
                'Status': {'select': {'name': module['status'] or 'Draft'}},
            }

            if module.get('created_at'):
                properties['Created'] = {'date': {'start': module['created_at'].isoformat()}}

            existing = query_data_source(
                NOTION_DS['module_library'],
                filter={
                    'property': 'Module Name',
                    'title': {'equals': module['title']}
                }
            )

            if existing['results']:
                notion.pages.update(
                    page_id=existing['results'][0]['id'],
                    properties=properties
                )
            else:
                notion.pages.create(
                    parent={'database_id': NOTION_DBS['module_library']},
                    properties=properties
                )

        except Exception as e:
            print(f"  ❌ Error syncing module {module['title']}: {e}")

    cur.close()
    conn.close()

    print(f"  ✅ Synced {len(modules)} modules")


def run_continuous_sync():
    """Main sync loop - runs forever"""

    print("\n" + "="*60)
    print("🚀 Notion Continuous Sync Daemon Starting")
    print("="*60 + "\n")
    print(f"Agent logs sync: Every {AGENT_LOG_SYNC_INTERVAL}s")
    print(f"Dashboard sync: Every {DASHBOARD_SYNC_INTERVAL}s")
    print(f"Module sync: Every {MODULE_SYNC_INTERVAL}s")
    print("\nPress Ctrl+C to stop\n")

    iteration = 0

    try:
        while True:
            iteration += 1
            now = datetime.now()

            print(f"\n{'='*60}")
            print(f"Sync Iteration #{iteration} - {now.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}\n")

            # Always sync agent activity (real-time)
            try:
                sync_agent_activity()
                sync_resource_claims()
            except Exception as e:
                print(f"❌ Error syncing agent activity: {e}")

            # Sync dashboards every 2 minutes
            if last_sync['dashboards'] is None or \
               (now - last_sync['dashboards']).seconds >= DASHBOARD_SYNC_INTERVAL:
                try:
                    sync_team_dashboard()
                    sync_project_dashboard()
                    last_sync['dashboards'] = now
                except Exception as e:
                    print(f"❌ Error syncing dashboards: {e}")

            # Sync modules every 5 minutes
            if last_sync['modules'] is None or \
               (now - last_sync['modules']).seconds >= MODULE_SYNC_INTERVAL:
                try:
                    sync_module_library()
                    last_sync['modules'] = now
                except Exception as e:
                    print(f"❌ Error syncing modules: {e}")

            # Sleep until next sync
            time.sleep(AGENT_LOG_SYNC_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n🛑 Sync daemon stopped by user")
        sys.exit(0)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Continuous Neon → Notion Sync')
    parser.add_argument('--setup', action='store_true', help='Set up Notion databases')
    parser.add_argument('--run', action='store_true', help='Run continuous sync daemon')

    args = parser.parse_args()

    if args.setup:
        setup_notion_databases()
    elif args.run:
        # Load database IDs from .env
        for key in NOTION_DBS.keys():
            env_key = f"NOTION_DB_{key.upper()}"
            NOTION_DBS[key] = os.getenv(env_key)

        # Check if databases are set up
        if not all(NOTION_DBS.values()):
            print("❌ Notion databases not set up. Run with --setup first.")
            sys.exit(1)

        run_continuous_sync()
    else:
        print("Usage:")
        print("  python scripts/notion_continuous_sync.py --setup   # Create Notion databases")
        print("  python scripts/notion_continuous_sync.py --run     # Run continuous sync")
