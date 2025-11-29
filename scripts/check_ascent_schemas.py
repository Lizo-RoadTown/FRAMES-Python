#!/usr/bin/env python3
"""Check Ascent Basecamp table schemas"""
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

tables = ['learner_performance', 'subsystem_competency', 'ghost_cohorts', 'race_metadata']

for table in tables:
    print(f"\n{table.upper()}:")
    print("=" * 60)
    cur.execute(f"""
        SELECT column_name, data_type, character_maximum_length
        FROM information_schema.columns
        WHERE table_name = '{table}'
        ORDER BY ordinal_position;
    """)
    
    for col in cur.fetchall():
        max_len = f"({col[2]})" if col[2] else ""
        print(f"  {col[0]:30s} {col[1]}{max_len}")

cur.close()
conn.close()
