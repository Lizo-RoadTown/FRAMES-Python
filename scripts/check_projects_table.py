#!/usr/bin/env python3
"""
Check existing projects table structure
"""

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Check if projects table exists and its structure
cur.execute("""
    SELECT column_name, data_type, character_maximum_length
    FROM information_schema.columns
    WHERE table_name = 'projects'
    ORDER BY ordinal_position;
""")

columns = cur.fetchall()

if columns:
    print("PROJECTS table columns:")
    for col in columns:
        print(f"  {col[0]:30s} {col[1]:20s} {col[2] if col[2] else ''}")
else:
    print("PROJECTS table does not exist yet")

cur.close()
conn.close()
