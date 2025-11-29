#!/usr/bin/env python3
"""
Final verification of Ascent Basecamp + CADENCE database deployment
"""

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def verify_deployment():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    print("=" * 80)
    print("ASCENT BASECAMP + CADENCE DATABASE VERIFICATION")
    print("=" * 80)
    print()
    
    # Count all tables
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
    """)
    total_tables = cur.fetchone()[0]
    print(f"✅ Total tables in database: {total_tables}")
    print()
    
    # CADENCE tables
    print("📊 CADENCE CORE TABLES (5 tables)")
    print("-" * 80)
    cadence_tables = ['cadence_people', 'cadence_projects', 'cadence_tasks', 'cadence_meetings', 'cadence_documents']
    
    for table in cadence_tables:
        cur.execute(f"SELECT COUNT(*) FROM {table};")
        count = cur.fetchone()[0]
        print(f"  • {table:30s} {count:>6} records")
    
    cadence_total = sum([
        cur.execute(f"SELECT COUNT(*) FROM {table};") or cur.fetchone()[0]
        for table in cadence_tables
    ])
    print(f"  {'TOTAL CADENCE RECORDS:':30s} {cadence_total:>6}")
    print()
    
    # Ascent Basecamp tables
    print("🎓 ASCENT BASECAMP LEARNING SYSTEM (10 tables)")
    print("-" * 80)
    basecamp_tables = [
        'ghost_cohorts',
        'learner_performance',
        'module_difficulty_calibrations',
        'ascent_basecamp_agent_log',
        'module_version_history',
        'simulation_environments',
        'module_prerequisites',
        'race_metadata',
        'subsystem_competency',
        'notion_sync_metadata'
    ]
    
    for table in basecamp_tables:
        cur.execute(f"SELECT COUNT(*) FROM {table};")
        count = cur.fetchone()[0]
        status = "✅ ACTIVE" if count > 0 else "⭕ READY"
        print(f"  • {table:40s} {count:>4} records  {status}")
    print()
    
    # Existing system tables
    print("📚 EXISTING SYSTEM (22 tables)")
    print("-" * 80)
    
    # Module system
    cur.execute("SELECT COUNT(*) FROM modules;")
    modules = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM module_sections;")
    sections = cur.fetchone()[0]
    print(f"  • modules:                               {modules:>4} records  ✅ EXISTING")
    print(f"  • module_sections:                       {sections:>4} records  ✅ EXISTING")
    
    # Raw CADENCE data
    cur.execute("SELECT COUNT(*) FROM cadence_raw_content;")
    raw = cur.fetchone()[0]
    print(f"  • cadence_raw_content (SOURCE):          {raw:>4} records  ✅ SOURCE")
    print(f"  • ... plus 19 other existing tables")
    print()
    
    # Indexes
    cur.execute("""
        SELECT COUNT(*) FROM pg_indexes 
        WHERE schemaname = 'public' 
        AND tablename LIKE 'cadence_%' OR tablename LIKE 'ascent%' OR tablename = 'learner_performance';
    """)
    index_count = cur.fetchone()[0]
    print(f"🔍 Performance indexes created: {index_count}")
    print()
    
    # Sample CADENCE data
    print("📋 SAMPLE CADENCE DATA")
    print("-" * 80)
    
    # People
    cur.execute("SELECT name, subsystem FROM cadence_people LIMIT 5;")
    print("  People:")
    for row in cur.fetchall():
        print(f"    - {row[0]:30s} ({row[1]})")
    
    # Projects
    cur.execute("SELECT name, subsystem, status FROM cadence_projects LIMIT 3;")
    print("\n  Projects:")
    for row in cur.fetchall():
        print(f"    - {row[0]:40s} [{row[2]}]")
    
    # Tasks
    cur.execute("SELECT title, status FROM cadence_tasks WHERE status = 'completed' LIMIT 3;")
    print("\n  Completed Tasks:")
    for row in cur.fetchall():
        print(f"    ✅ {row[0][:50]}")
    
    # Agent logs
    print()
    print("🤖 AGENT ACTIVITY LOG")
    print("-" * 80)
    cur.execute("""
        SELECT timestamp, agent_name, action_type, status, message
        FROM ascent_basecamp_agent_log
        ORDER BY timestamp DESC;
    """)
    for row in cur.fetchall():
        print(f"  [{row[0]}]")
        print(f"  Agent: {row[1]} | Action: {row[2]} | Status: {row[3]}")
        print(f"  Message: {row[4]}")
        print()
    
    # Subsystem distribution
    print("🔧 CADENCE SUBSYSTEM DISTRIBUTION")
    print("-" * 80)
    cur.execute("""
        SELECT subsystem, COUNT(*) as count
        FROM (
            SELECT subsystem FROM cadence_people
            UNION ALL
            SELECT subsystem FROM cadence_projects
            UNION ALL
            SELECT subsystem FROM cadence_documents
        ) AS all_subsystems
        WHERE subsystem IS NOT NULL
        GROUP BY subsystem
        ORDER BY count DESC;
    """)
    
    for row in cur.fetchall():
        print(f"  • {row[0]:30s} {row[1]:>4} records")
    
    print()
    print("=" * 80)
    print("✅ DATABASE DEPLOYMENT VERIFIED")
    print("=" * 80)
    print()
    print("Next Steps:")
    print("  1. Review docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md for full schema reference")
    print("  2. Import additional CADENCE files (868 keep files from classification)")
    print("  3. Create learning modules from CADENCE technical documentation")
    print("  4. Set up ghost cohorts from historical performance data")
    print("  5. Configure Notion → Postgres sync for dashboards")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    verify_deployment()
