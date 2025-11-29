"""
Reconfigure Beta as Autonomous Agent
Beta is highly autonomous but better suited for moderate complexity tasks
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

print('Reconfiguring agent capabilities...\n')

# Beta: Autonomous, good at UI/frontend, best with moderate complexity
cur.execute("""
    UPDATE agent_capabilities
    SET capability_level = 'standard',
        supervision_level = 'normal',
        needs_review = FALSE,
        notes = 'Autonomous agent. Excellent at UI/frontend with explicit requirements. Best suited for moderate complexity, well-defined tasks. May need support on very complex architectural decisions.'
    WHERE agent_name = 'beta';
""")

# Alpha: Complex content and module design
cur.execute("""
    UPDATE agent_capabilities
    SET notes = 'Module creation specialist. Handles complex content transformation, educational design, and learning experience architecture.'
    WHERE agent_name = 'alpha';
""")

# Gamma: Complex infrastructure and system architecture
cur.execute("""
    UPDATE agent_capabilities
    SET notes = 'Infrastructure specialist. Handles complex system architecture, data pipelines, coordination, and technical problem-solving.'
    WHERE agent_name = 'gamma';
""")

conn.commit()

# Show updated configuration
print('='*60)
print('UPDATED AGENT CAPABILITIES')
print('='*60 + '\n')

cur.execute('SELECT agent_name, capability_level, supervision_level, needs_review, notes FROM agent_capabilities ORDER BY agent_name;')

for row in cur.fetchall():
    print(f'{row[0].upper()}:')
    print(f'  Capability: {row[1]}')
    print(f'  Supervision: {row[2]}')
    print(f'  Needs Review: {row[3]}')
    print(f'  Notes: {row[4]}')
    print()

conn.close()

print('='*60)
print('Task Assignment Strategy:')
print('='*60)
print('ALPHA: Complex module design, content transformation')
print('BETA: UI implementation, well-defined features, moderate complexity')
print('GAMMA: Infrastructure, architecture, complex technical coordination')
