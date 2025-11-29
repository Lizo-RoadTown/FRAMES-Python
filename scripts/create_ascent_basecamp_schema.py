#!/usr/bin/env python3
"""
Ascent Basecamp + CADENCE Database Schema Creation
Creates all necessary tables for the unified learning system
"""

import os
from dotenv import load_dotenv
import psycopg2
from datetime import datetime

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def create_tables():
    """Create all required database tables"""
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    print("=" * 80)
    print("CREATING ASCENT BASECAMP + CADENCE DATABASE SCHEMA")
    print("=" * 80)
    print()
    
    # =========================================================================
    # CADENCE CORE TABLES (5 canonical tables from spec)
    # Note: Using "cadence_" prefix to avoid conflicts with existing tables
    # =========================================================================
    
    print("Creating CADENCE core tables...")
    
    # 1. CADENCE_PEOPLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cadence_people (
            person_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            role VARCHAR(255),
            subsystem VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            notion_page_id VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("  ✓ cadence_people")
    
    # 2. CADENCE_PROJECTS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cadence_projects (
            project_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            subsystem VARCHAR(255),
            status VARCHAR(100),
            owner_id INTEGER REFERENCES cadence_people(person_id),
            notion_page_id VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("  ✓ cadence_projects")
    
    # 3. CADENCE_TASKS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cadence_tasks (
            task_id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(100),
            due_date DATE,
            assignee_id INTEGER REFERENCES cadence_people(person_id),
            project_id INTEGER REFERENCES cadence_projects(project_id),
            notion_page_id VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("  ✓ cadence_tasks")
    
    # 4. CADENCE_MEETINGS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cadence_meetings (
            meeting_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            meeting_date TIMESTAMP,
            attendees TEXT,
            project_id INTEGER REFERENCES cadence_projects(project_id),
            notes TEXT,
            notion_page_id VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("  ✓ cadence_meetings")
    
    # 5. CADENCE_DOCUMENTS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cadence_documents (
            doc_id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            url TEXT,
            doc_type VARCHAR(100),
            category VARCHAR(100),
            subsystem VARCHAR(255),
            notion_page_id VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("  ✓ cadence_documents")
    
    print()
    
    # =========================================================================
    # ASCENT BASECAMP LEARNING SYSTEM TABLES
    # =========================================================================
    
    print("Creating Ascent Basecamp learning system tables...")
    
    # GHOST COHORTS - Performance benchmarking
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ghost_cohorts (
            cohort_id SERIAL PRIMARY KEY,
            cohort_name VARCHAR(255) NOT NULL,
            semester VARCHAR(100),
            university VARCHAR(255),
            subsystem VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("  ✓ ghost_cohorts")
    
    # LEARNER PERFORMANCE - Student activity logs
    cur.execute("""
        CREATE TABLE IF NOT EXISTS learner_performance (
            log_id SERIAL PRIMARY KEY,
            student_id VARCHAR(255),
            module_id INTEGER,
            attempt_number INTEGER,
            time_spent_seconds INTEGER,
            errors_count INTEGER,
            mastery_score DECIMAL(5,2),
            completed BOOLEAN DEFAULT FALSE,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (module_id) REFERENCES modules(id)
        );
    """)
    print("  ✓ learner_performance")
    
    # MODULE DIFFICULTY CALIBRATIONS - Adaptive difficulty
    cur.execute("""
        CREATE TABLE IF NOT EXISTS module_difficulty_calibrations (
            calibration_id SERIAL PRIMARY KEY,
            module_id INTEGER REFERENCES modules(id),
            difficulty_level VARCHAR(50),
            average_time_seconds INTEGER,
            success_rate DECIMAL(5,2),
            sample_size INTEGER,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("  ✓ module_difficulty_calibrations")
    
    # AGENT LOGS - Multi-agent development tracking
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ascent_basecamp_agent_log (
            log_id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            agent_name VARCHAR(100) NOT NULL,
            action_type VARCHAR(100) NOT NULL,
            subsystem VARCHAR(255),
            status VARCHAR(50),
            error TEXT,
            resolution TEXT,
            message TEXT,
            metadata JSONB
        );
    """)
    print("  ✓ ascent_basecamp_agent_log")
    
    # MODULE VERSION HISTORY - Spec tracking
    cur.execute("""
        CREATE TABLE IF NOT EXISTS module_version_history (
            version_id SERIAL PRIMARY KEY,
            module_id INTEGER REFERENCES modules(id),
            version_number VARCHAR(50),
            spec_json JSONB,
            change_description TEXT,
            created_by VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("  ✓ module_version_history")
    
    # SIMULATION ENVIRONMENTS - Tool/sandbox tracking
    cur.execute("""
        CREATE TABLE IF NOT EXISTS simulation_environments (
            env_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type VARCHAR(100), -- CircuitJS, LTSpice, FreeCAD, WebContainer, etc.
            subsystem VARCHAR(255),
            config_json JSONB,
            status VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("  ✓ simulation_environments")
    
    # MODULE PREREQUISITES - Learning path graph
    cur.execute("""
        CREATE TABLE IF NOT EXISTS module_prerequisites (
            prereq_id SERIAL PRIMARY KEY,
            module_id INTEGER REFERENCES modules(id),
            prerequisite_module_id INTEGER REFERENCES modules(id),
            required BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("  ✓ module_prerequisites")
    
    # RACE METADATA - Competition/challenge data
    cur.execute("""
        CREATE TABLE IF NOT EXISTS race_metadata (
            race_id SERIAL PRIMARY KEY,
            module_id INTEGER REFERENCES modules(id),
            ghost_data JSONB,
            time_targets JSONB,
            checkpoints JSONB,
            leaderboard_data JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("  ✓ race_metadata")
    
    # SUBSYSTEM COMPETENCY TRACKING
    cur.execute("""
        CREATE TABLE IF NOT EXISTS subsystem_competency (
            competency_id SERIAL PRIMARY KEY,
            student_id VARCHAR(255) REFERENCES students(id),
            subsystem VARCHAR(255) NOT NULL,
            competency_level VARCHAR(50), -- orientation, competency, integration, autonomy
            modules_completed INTEGER DEFAULT 0,
            last_activity TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print("  ✓ subsystem_competency")
    
    # NOTION SYNC METADATA - Track sync operations
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notion_sync_metadata (
            sync_id SERIAL PRIMARY KEY,
            sync_type VARCHAR(100), -- people, tasks, projects, documents, modules
            last_sync TIMESTAMP,
            records_synced INTEGER,
            errors INTEGER,
            status VARCHAR(50),
            error_details TEXT
        );
    """)
    print("  ✓ notion_sync_metadata")
    
    print()
    
    # =========================================================================
    # CREATE INDEXES FOR PERFORMANCE
    # =========================================================================
    
    print("Creating indexes...")
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_cadence_people_email ON cadence_people(email);",
        "CREATE INDEX IF NOT EXISTS idx_cadence_people_subsystem ON cadence_people(subsystem);",
        "CREATE INDEX IF NOT EXISTS idx_cadence_tasks_assignee ON cadence_tasks(assignee_id);",
        "CREATE INDEX IF NOT EXISTS idx_cadence_tasks_project ON cadence_tasks(project_id);",
        "CREATE INDEX IF NOT EXISTS idx_cadence_tasks_status ON cadence_tasks(status);",
        "CREATE INDEX IF NOT EXISTS idx_cadence_documents_subsystem ON cadence_documents(subsystem);",
        "CREATE INDEX IF NOT EXISTS idx_cadence_documents_category ON cadence_documents(category);",
        "CREATE INDEX IF NOT EXISTS idx_learner_perf_student ON learner_performance(student_id);",
        "CREATE INDEX IF NOT EXISTS idx_learner_perf_module ON learner_performance(module_id);",
        "CREATE INDEX IF NOT EXISTS idx_agent_log_timestamp ON ascent_basecamp_agent_log(timestamp);",
        "CREATE INDEX IF NOT EXISTS idx_agent_log_agent ON ascent_basecamp_agent_log(agent_name);",
        "CREATE INDEX IF NOT EXISTS idx_subsystem_comp_student ON subsystem_competency(student_id);",
        "CREATE INDEX IF NOT EXISTS idx_subsystem_comp_subsystem ON subsystem_competency(subsystem);",
    ]
    
    for idx_sql in indexes:
        cur.execute(idx_sql)
    
    print(f"  ✓ Created {len(indexes)} indexes")
    print()
    
    # Commit all changes
    conn.commit()
    
    # =========================================================================
    # VERIFY TABLES
    # =========================================================================
    
    print("=" * 80)
    print("VERIFICATION")
    print("=" * 80)
    
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)
    tables = cur.fetchall()
    
    print(f"✓ Total tables in database: {len(tables)}")
    print()
    print("Tables created:")
    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table[0]};")
        count = cur.fetchone()[0]
        print(f"  • {table[0]:40s} ({count:>5} rows)")
    
    print()
    print("=" * 80)
    print("✅ DATABASE SCHEMA CREATION COMPLETE")
    print("=" * 80)
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    try:
        create_tables()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
