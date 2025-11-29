#!/usr/bin/env python3
"""
Inspect the existing cadence_raw_content table
"""

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Check structure
print("CADENCE_RAW_CONTENT table structure:")
print("=" * 80)
cur.execute("""
    SELECT column_name, data_type, character_maximum_length
    FROM information_schema.columns
    WHERE table_name = 'cadence_raw_content'
    ORDER BY ordinal_position;
""")

columns = cur.fetchall()
for col in columns:
    print(f"  {col[0]:30s} {col[1]:20s} {col[2] if col[2] else ''}")

print()
print("Sample data:")
print("=" * 80)

# Get sample records
cur.execute("""
    SELECT id, title, category, file_type, subsystem, notion_id
    FROM cadence_raw_content
    LIMIT 10;
""")

rows = cur.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Title: {row[1][:50] if row[1] else 'N/A'}")
    print(f"  Category: {row[2]}, Type: {row[3]}, Subsystem: {row[4]}, Notion ID: {row[5]}")
    print()

# Get counts by category and type
print("Distribution by category:")
print("=" * 80)
cur.execute("""
    SELECT category, COUNT(*) as count
    FROM cadence_raw_content
    GROUP BY category
    ORDER BY count DESC;
""")

for row in cur.fetchall():
    print(f"  {row[0]:30s} {row[1]:>5} rows")

print()
print("Distribution by file_type:")
print("=" * 80)
cur.execute("""
    SELECT file_type, COUNT(*) as count
    FROM cadence_raw_content
    GROUP BY file_type
    ORDER BY count DESC;
""")

for row in cur.fetchall():
    print(f"  {row[0]:30s} {row[1]:>5} rows")

cur.close()
conn.close()
