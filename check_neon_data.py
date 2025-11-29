#!/usr/bin/env python3
"""
Quick script to check what data is in the Neon database
"""

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def check_database():
    """Check what tables and data exist in the database"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        print("=" * 80)
        print("NEON DATABASE INSPECTION")
        print("=" * 80)
        print()
        
        # List all tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cur.fetchall()
        
        print(f"📊 Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table['table_name']}")
        print()
        
        # Check each table for row counts
        print("=" * 80)
        print("TABLE ROW COUNTS")
        print("=" * 80)
        
        for table in tables:
            table_name = table['table_name']
            try:
                cur.execute(f"SELECT COUNT(*) as count FROM {table_name};")
                count = cur.fetchone()['count']
                print(f"{table_name:30s} {count:>10,} rows")
                
                # If there are rows, show a sample
                if count > 0 and count <= 5:
                    cur.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                    rows = cur.fetchall()
                    print(f"  Sample data:")
                    for row in rows:
                        print(f"    {dict(row)}")
                
            except Exception as e:
                print(f"{table_name:30s} Error: {e}")
        
        print()
        
        # Check specifically for CADENCE-related data
        print("=" * 80)
        print("CADENCE DATA CHECK")
        print("=" * 80)
        
        # Check for people
        try:
            cur.execute("SELECT COUNT(*) as count FROM people;")
            people_count = cur.fetchone()['count']
            print(f"People: {people_count}")
            if people_count > 0:
                cur.execute("SELECT name, role FROM people LIMIT 5;")
                print("  Sample:")
                for row in cur.fetchall():
                    print(f"    {row['name']} - {row['role']}")
        except Exception as e:
            print(f"People table: {e}")
        
        print()
        
        # Check for projects
        try:
            cur.execute("SELECT COUNT(*) as count FROM projects;")
            projects_count = cur.fetchone()['count']
            print(f"Projects: {projects_count}")
            if projects_count > 0:
                cur.execute("SELECT name, subsystem FROM projects LIMIT 5;")
                print("  Sample:")
                for row in cur.fetchall():
                    print(f"    {row['name']} - {row['subsystem']}")
        except Exception as e:
            print(f"Projects table: {e}")
        
        print()
        
        # Check for tasks
        try:
            cur.execute("SELECT COUNT(*) as count FROM tasks;")
            tasks_count = cur.fetchone()['count']
            print(f"Tasks: {tasks_count}")
            if tasks_count > 0:
                cur.execute("SELECT title, status FROM tasks LIMIT 5;")
                print("  Sample:")
                for row in cur.fetchall():
                    print(f"    {row['title']} - {row['status']}")
        except Exception as e:
            print(f"Tasks table: {e}")
        
        print()
        
        # Check for meetings
        try:
            cur.execute("SELECT COUNT(*) as count FROM meetings;")
            meetings_count = cur.fetchone()['count']
            print(f"Meetings: {meetings_count}")
        except Exception as e:
            print(f"Meetings table: {e}")
        
        print()
        
        # Check for documents
        try:
            cur.execute("SELECT COUNT(*) as count FROM documents;")
            docs_count = cur.fetchone()['count']
            print(f"Documents: {docs_count}")
            if docs_count > 0:
                cur.execute("SELECT title, category FROM documents LIMIT 5;")
                print("  Sample:")
                for row in cur.fetchall():
                    print(f"    {row['title']} - {row['category']}")
        except Exception as e:
            print(f"Documents table: {e}")
        
        print()
        print("=" * 80)
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        print(f"DATABASE_URL: {DATABASE_URL[:50]}...")

if __name__ == '__main__':
    check_database()
