"""Check database tables and schema."""
from dotenv import load_dotenv
load_dotenv()

import os
import psycopg2

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()

# List all tables
cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name
""")
tables = cur.fetchall()

print(f"📊 Found {len(tables)} table(s) in database:\n")
for table in tables:
    table_name = table[0]
    # Get row count
    cur.execute(f'SELECT count(*) FROM "{table_name}"')
    count = cur.fetchone()[0]
    print(f"  • {table_name}: {count} rows")

conn.close()
print("\n✅ Database connection working!")

