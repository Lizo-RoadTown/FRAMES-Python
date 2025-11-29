#!/usr/bin/env python3
"""
Populate structured CADENCE tables from cadence_raw_content
Transforms raw markdown data into relational schema
"""

import os
import re
import json
from dotenv import load_dotenv
import psycopg2
from datetime import datetime

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def extract_people_from_content(content):
    """Extract people mentions from markdown content"""
    # Look for @mentions and name patterns
    people = set()
    
    if not content:
        return people
    
    # Find @mentions
    mentions = re.findall(r'@([A-Za-z\s]+?)(?:\s|$|,|\.|:)', content)
    people.update([m.strip() for m in mentions if len(m.strip()) > 2])
    
    # Find "Assigned to:" patterns
    assigned = re.findall(r'Assigned to:\s*([A-Za-z\s]+?)(?:\n|$|,)', content, re.IGNORECASE)
    people.update([a.strip() for a in assigned if len(a.strip()) > 2])
    
    # Find "Owner:" patterns
    owners = re.findall(r'Owner:\s*([A-Za-z\s]+?)(?:\n|$|,)', content, re.IGNORECASE)
    people.update([o.strip() for o in owners if len(o.strip()) > 2])
    
    return people

def extract_date_from_content(content):
    """Extract dates from content"""
    if not content:
        return None
    
    # Look for "Due:" dates
    due_match = re.search(r'Due:\s*(\d{4}-\d{2}-\d{2})', content, re.IGNORECASE)
    if due_match:
        return due_match.group(1)
    
    # Look for ISO dates
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', content)
    if date_match:
        return date_match.group(1)
    
    return None

def extract_status_from_content(content):
    """Extract status information from content"""
    if not content:
        return 'unknown'
    
    # Check for common status indicators
    content_lower = content.lower()
    
    if '✅' in content or 'completed' in content_lower or 'done' in content_lower:
        return 'completed'
    elif '🚧' in content or 'in progress' in content_lower or 'wip' in content_lower:
        return 'in_progress'
    elif '❌' in content or 'blocked' in content_lower:
        return 'blocked'
    elif '📝' in content or 'todo' in content_lower or 'to do' in content_lower:
        return 'todo'
    
    return 'active'

def populate_people(cur):
    """Populate cadence_people table"""
    print("Populating cadence_people...")
    
    # Get all content to extract people mentions
    cur.execute("""
        SELECT DISTINCT content, subsystem
        FROM cadence_raw_content
        WHERE content IS NOT NULL;
    """)
    
    all_people = {}  # {name: subsystem}
    
    for row in cur.fetchall():
        content, subsystem = row
        people = extract_people_from_content(content)
        
        for person in people:
            if person not in all_people:
                all_people[person] = subsystem
    
    # Insert unique people
    inserted = 0
    for name, subsystem in all_people.items():
        try:
            cur.execute("""
                INSERT INTO cadence_people (name, subsystem, role)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (name, subsystem, 'team_member'))
            inserted += 1
        except Exception as e:
            print(f"  Warning: Could not insert {name}: {e}")
    
    print(f"  ✓ Inserted {inserted} people")
    return inserted

def populate_projects(cur):
    """Populate cadence_projects table from documents_program"""
    print("Populating cadence_projects...")
    
    cur.execute("""
        SELECT id, title, content, subsystem, notion_id
        FROM cadence_raw_content
        WHERE category IN ('documents_program', 'documents_technical')
        AND title IS NOT NULL;
    """)
    
    inserted = 0
    for row in cur.fetchall():
        raw_id, title, content, subsystem, notion_id = row
        
        # Extract description (first paragraph)
        description = None
        if content:
            paragraphs = content.split('\n\n')
            if len(paragraphs) > 0:
                description = paragraphs[0][:500]  # First 500 chars
        
        status = extract_status_from_content(content)
        
        try:
            cur.execute("""
                INSERT INTO cadence_projects (name, description, subsystem, status, notion_page_id)
                VALUES (%s, %s, %s, %s, %s);
            """, (title, description, subsystem, status, notion_id))
            inserted += 1
        except Exception as e:
            print(f"  Warning: Could not insert project '{title}': {e}")
    
    print(f"  ✓ Inserted {inserted} projects")
    return inserted

def populate_tasks(cur):
    """Populate cadence_tasks table"""
    print("Populating cadence_tasks...")
    
    cur.execute("""
        SELECT id, title, content, subsystem, notion_id
        FROM cadence_raw_content
        WHERE category = 'tasks'
        AND title IS NOT NULL;
    """)
    
    inserted = 0
    for row in cur.fetchall():
        raw_id, title, content, subsystem, notion_id = row
        
        description = content[:1000] if content else None
        status = extract_status_from_content(content)
        due_date = extract_date_from_content(content)
        
        # Try to find assignee
        assignee_id = None
        if content:
            people = extract_people_from_content(content)
            if people:
                # Get first person from database
                person_name = list(people)[0]
                cur.execute("SELECT person_id FROM cadence_people WHERE name = %s LIMIT 1;", (person_name,))
                result = cur.fetchone()
                if result:
                    assignee_id = result[0]
        
        try:
            cur.execute("""
                INSERT INTO cadence_tasks (title, description, status, due_date, assignee_id, notion_page_id)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (title, description, status, due_date, assignee_id, notion_id))
            inserted += 1
        except Exception as e:
            print(f"  Warning: Could not insert task '{title}': {e}")
    
    print(f"  ✓ Inserted {inserted} tasks")
    return inserted

def populate_meetings(cur):
    """Populate cadence_meetings table"""
    print("Populating cadence_meetings...")
    
    cur.execute("""
        SELECT id, title, content, subsystem, notion_id, date_extracted
        FROM cadence_raw_content
        WHERE category = 'meetings'
        AND title IS NOT NULL;
    """)
    
    inserted = 0
    for row in cur.fetchall():
        raw_id, title, content, subsystem, notion_id, date_extracted = row
        
        # Extract attendees
        attendees = None
        if content:
            people = extract_people_from_content(content)
            if people:
                attendees = ', '.join(people)
        
        # Use extracted date or find date in content
        meeting_date = date_extracted
        if not meeting_date and content:
            date_str = extract_date_from_content(content)
            if date_str:
                try:
                    meeting_date = datetime.strptime(date_str, '%Y-%m-%d')
                except:
                    pass
        
        try:
            cur.execute("""
                INSERT INTO cadence_meetings (name, meeting_date, attendees, notes, notion_page_id)
                VALUES (%s, %s, %s, %s, %s);
            """, (title, meeting_date, attendees, content, notion_id))
            inserted += 1
        except Exception as e:
            print(f"  Warning: Could not insert meeting '{title}': {e}")
    
    print(f"  ✓ Inserted {inserted} meetings")
    return inserted

def populate_documents(cur):
    """Populate cadence_documents table"""
    print("Populating cadence_documents...")
    
    cur.execute("""
        SELECT id, title, filename, category, subsystem, notion_id
        FROM cadence_raw_content
        WHERE category IN ('documents_technical', 'documents_program', 'documents_workflow')
        AND title IS NOT NULL;
    """)
    
    inserted = 0
    for row in cur.fetchall():
        raw_id, title, filename, category, subsystem, notion_id = row
        
        # Create URL from notion_id
        url = f"https://notion.so/{notion_id}" if notion_id else None
        
        # Map category to doc_type
        doc_type = category.replace('documents_', '') if category else 'general'
        
        try:
            cur.execute("""
                INSERT INTO cadence_documents (title, url, doc_type, category, subsystem, notion_page_id)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (title, url, doc_type, category, subsystem, notion_id))
            inserted += 1
        except Exception as e:
            print(f"  Warning: Could not insert document '{title}': {e}")
    
    print(f"  ✓ Inserted {inserted} documents")
    return inserted

def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    print("=" * 80)
    print("POPULATING CADENCE STRUCTURED TABLES")
    print("=" * 80)
    print()
    
    try:
        # Get raw data count
        cur.execute("SELECT COUNT(*) FROM cadence_raw_content;")
        raw_count = cur.fetchone()[0]
        print(f"Source: {raw_count} records in cadence_raw_content")
        print()
        
        # Populate tables in order (respecting foreign keys)
        people_count = populate_people(cur)
        projects_count = populate_projects(cur)
        tasks_count = populate_tasks(cur)
        meetings_count = populate_meetings(cur)
        documents_count = populate_documents(cur)
        
        # Commit all changes
        conn.commit()
        
        print()
        print("=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"  • cadence_people:       {people_count:>5} records")
        print(f"  • cadence_projects:     {projects_count:>5} records")
        print(f"  • cadence_tasks:        {tasks_count:>5} records")
        print(f"  • cadence_meetings:     {meetings_count:>5} records")
        print(f"  • cadence_documents:    {documents_count:>5} records")
        print()
        print("✅ CADENCE DATA POPULATION COMPLETE")
        print("=" * 80)
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    main()
