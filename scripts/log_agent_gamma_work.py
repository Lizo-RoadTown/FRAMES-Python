#!/usr/bin/env python3
"""
Log Agent Gamma's database schema creation work
"""

import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def log_agent_work():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Log schema creation
    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log 
        (agent_name, action_type, subsystem, status, message, metadata)
        VALUES 
        ('Agent Gamma', 'database_schema_creation', 'ascent_basecamp', 'success',
         'Created complete Ascent Basecamp + CADENCE database schema with 15 new tables',
         '{"tables_created": ["cadence_people", "cadence_projects", "cadence_tasks", "cadence_meetings", "cadence_documents", "ghost_cohorts", "learner_performance", "module_difficulty_calibrations", "ascent_basecamp_agent_log", "module_version_history", "simulation_environments", "module_prerequisites", "race_metadata", "subsystem_competency", "notion_sync_metadata"], "indexes_created": 13}'::jsonb
        );
    """)
    
    # Log data population
    cur.execute("""
        INSERT INTO ascent_basecamp_agent_log 
        (agent_name, action_type, subsystem, status, message, metadata)
        VALUES 
        ('Agent Gamma', 'data_import', 'cadence', 'success',
         'Populated CADENCE structured tables from 1,416 raw content records',
         '{"source": "cadence_raw_content", "records_imported": {"people": 27, "projects": 69, "tasks": 443, "meetings": 440, "documents": 71}, "total_records": 1050}'::jsonb
        );
    """)
    
    conn.commit()
    
    print("✅ Logged Agent Gamma work to ascent_basecamp_agent_log")
    
    # Show recent logs
    cur.execute("""
        SELECT timestamp, agent_name, action_type, status, message
        FROM ascent_basecamp_agent_log
        ORDER BY timestamp DESC
        LIMIT 5;
    """)
    
    print("\nRecent agent activity:")
    print("=" * 80)
    for row in cur.fetchall():
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
        print(f"  {row[4]}")
        print()
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    log_agent_work()
