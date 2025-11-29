#!/usr/bin/env python3
"""
Check existing table structures for foreign key compatibility
"""

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

tables_to_check = ['students', 'modules']

for table_name in tables_to_check:
    print(f"\n{table_name.upper()} table columns:")
    print("=" * 60)
    
    cur.execute("""
        SELECT column_name, data_type, character_maximum_length
        FROM information_schema.columns
        WHERE table_name = %s
        ORDER BY ordinal_position;
    """, (table_name,))
    
    columns = cur.fetchall()
    
    if columns:
        for col in columns:
            print(f"  {col[0]:30s} {col[1]:20s} {col[2] if col[2] else ''}")
    else:
        print(f"  Table {table_name} does not exist")

cur.close()
conn.close()
