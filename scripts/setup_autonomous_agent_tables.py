"""
Setup Database Tables for Autonomous Agent System
Creates tables needed for three independent agents to coordinate
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def setup_tables():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()

    print('Creating tables for autonomous agent system...\n')

    # 1. Update agent_log table
    print('1. Updating ascent_basecamp_agent_log...')
    cur.execute('ALTER TABLE ascent_basecamp_agent_log ADD COLUMN IF NOT EXISTS resource_claim VARCHAR(255);')
    cur.execute('ALTER TABLE ascent_basecamp_agent_log ADD COLUMN IF NOT EXISTS session_id VARCHAR(100);')
    cur.execute('ALTER TABLE ascent_basecamp_agent_log ADD COLUMN IF NOT EXISTS check_in_time TIMESTAMP;')
    cur.execute('ALTER TABLE ascent_basecamp_agent_log ADD COLUMN IF NOT EXISTS next_check_in TIMESTAMP;')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_agent_log_resource ON ascent_basecamp_agent_log(resource_claim);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_agent_log_session ON ascent_basecamp_agent_log(session_id);')
    print('   [OK] Agent log table updated\n')

    # 2. Create technical_decisions table
    print('2. Creating technical_decisions table...')
    cur.execute("""
        CREATE TABLE IF NOT EXISTS technical_decisions (
            decision_id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            agent_name VARCHAR(100),
            decision_type VARCHAR(100),
            decision TEXT NOT NULL,
            rationale TEXT,
            alternatives_considered TEXT,
            impact VARCHAR(50),
            status VARCHAR(50) DEFAULT 'proposed',
            metadata JSONB
        );
    """)
    cur.execute('CREATE INDEX IF NOT EXISTS idx_decisions_status ON technical_decisions(status);')
    print('   [OK] Technical decisions table created\n')

    # 3. Create error_log table
    print('3. Creating error_log table...')
    cur.execute("""
        CREATE TABLE IF NOT EXISTS error_log (
            error_id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            agent_name VARCHAR(100),
            error_type VARCHAR(100),
            error_message TEXT NOT NULL,
            stack_trace TEXT,
            resolution_status VARCHAR(50) DEFAULT 'unresolved',
            resolution TEXT,
            severity VARCHAR(50),
            metadata JSONB
        );
    """)
    cur.execute('CREATE INDEX IF NOT EXISTS idx_errors_status ON error_log(resolution_status);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_errors_severity ON error_log(severity);')
    print('   [OK] Error log table created\n')

    conn.commit()
    conn.close()

    print('[COMPLETE] All tables created successfully!\n')
    print('New tables:')
    print('  - technical_decisions (for Liz to review agent decisions)')
    print('  - error_log (for Liz to monitor agent errors)')
    print('\nUpdated tables:')
    print('  - ascent_basecamp_agent_log (added resource_claim, session_id, check_in fields)')

if __name__ == '__main__':
    setup_tables()
