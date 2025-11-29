"""
Setup Agent Capability Tracking
Identifies which agent needs more supervision/review
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def setup_capability_tracking():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()

    print('Setting up agent capability tracking...\n')

    # 1. Add capability level to agent log
    print('1. Updating agent_log table...')
    cur.execute("""
        ALTER TABLE ascent_basecamp_agent_log
        ADD COLUMN IF NOT EXISTS agent_capability VARCHAR(50) DEFAULT 'standard';
    """)
    print('   [OK] Added agent_capability column\n')

    # 2. Create agent capabilities tracking table
    print('2. Creating agent_capabilities table...')
    cur.execute("""
        CREATE TABLE IF NOT EXISTS agent_capabilities (
            agent_name VARCHAR(100) PRIMARY KEY,
            capability_level VARCHAR(50) DEFAULT 'standard',
            model_name VARCHAR(100),
            needs_review BOOLEAN DEFAULT FALSE,
            supervision_level VARCHAR(50) DEFAULT 'normal',
            error_rate DECIMAL(5,2) DEFAULT 0.00,
            success_rate DECIMAL(5,2) DEFAULT 100.00,
            notes TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print('   [OK] Agent capabilities table created\n')

    # 3. Insert default capabilities for three agents
    print('3. Initializing agent capabilities...')

    # Alpha - standard capability
    cur.execute("""
        INSERT INTO agent_capabilities (
            agent_name, capability_level, supervision_level, notes
        ) VALUES (%s, %s, %s, %s)
        ON CONFLICT (agent_name) DO NOTHING;
    """, ('alpha', 'standard', 'normal', 'Module creation specialist'))

    # Beta - weaker capability (if this is the weaker one)
    cur.execute("""
        INSERT INTO agent_capabilities (
            agent_name, capability_level, supervision_level, needs_review, notes
        ) VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (agent_name) DO NOTHING;
    """, ('beta', 'limited', 'high', True, 'Platform developer - needs more review'))

    # Gamma - standard capability
    cur.execute("""
        INSERT INTO agent_capabilities (
            agent_name, capability_level, supervision_level, notes
        ) VALUES (%s, %s, %s, %s)
        ON CONFLICT (agent_name) DO NOTHING;
    """, ('gamma', 'standard', 'normal', 'Infrastructure specialist'))

    print('   [OK] Default capabilities set:\n')
    print('      - Alpha: standard (normal supervision)')
    print('      - Beta: limited (high supervision, needs review)')
    print('      - Gamma: standard (normal supervision)\n')

    conn.commit()
    conn.close()

    print('[COMPLETE] Agent capability tracking ready!\n')
    print('Capability levels:')
    print('  - "standard" = Full autonomy')
    print('  - "limited" = Needs more review/supervision')
    print('  - "advanced" = Can handle complex tasks')
    print('\nSupervision levels:')
    print('  - "normal" = Standard check-ins')
    print('  - "high" = Review all decisions, more frequent check-ins')
    print('  - "low" = Minimal oversight (for advanced agents)')

if __name__ == '__main__':
    setup_capability_tracking()
