"""Test Neon and Notion connections for Desktop Claude."""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_neon_connection():
    """Test connection to Neon PostgreSQL database."""
    print("\n" + "="*80)
    print("TESTING NEON DATABASE CONNECTION")
    print("="*80)

    try:
        import psycopg2
        database_url = os.getenv('DATABASE_URL')

        if not database_url:
            print("ERROR: DATABASE_URL not found in .env file")
            return False

        print(f"Database URL: {database_url[:50]}...")

        # Test connection
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        # Get list of tables
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)

        tables = [row[0] for row in cursor.fetchall()]

        print(f"\nSUCCESS! Connected to Neon database")
        print(f"Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")

        # Get some basic stats if tables exist
        if 'universities' in tables:
            cursor.execute("SELECT COUNT(*) FROM universities;")
            uni_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM teams;")
            team_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM students;")
            student_count = cursor.fetchone()[0]

            print(f"\nData counts:")
            print(f"  - Universities: {uni_count}")
            print(f"  - Teams: {team_count}")
            print(f"  - Students: {student_count}")
        else:
            print(f"\nNOTE: Database is empty or has minimal schema")
            print(f"      You may need to run bootstrap or migration scripts")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"ERROR: Failed to connect to Neon database")
        print(f"Error: {str(e)}")
        return False


def test_notion_connection():
    """Test connection to Notion API."""
    print("\n" + "="*80)
    print("TESTING NOTION API CONNECTION")
    print("="*80)

    try:
        from notion_client import Client

        notion_key = os.getenv('NOTION_API_KEY')

        if not notion_key:
            print("ERROR: NOTION_API_KEY not found in .env file")
            return False

        print(f"Notion API Key: {notion_key[:20]}...")

        # Initialize client
        notion = Client(auth=notion_key)

        # Test by listing users
        response = notion.users.list()

        print(f"\nSUCCESS! Connected to Notion API")
        print(f"Found {len(response.get('results', []))} users in workspace")

        # Try to search for pages (databases are a type of page)
        try:
            search_response = notion.search(filter={"property": "object", "value": "page"})
            pages = search_response.get('results', [])
            databases = [p for p in pages if p.get('object') == 'database']

            print(f"Found {len(databases)} databases:")
            for db in databases[:5]:  # Show first 5
                title = db.get('title', [{}])[0].get('plain_text', 'Untitled') if db.get('title') else 'Untitled'
                print(f"  - {title}")

            if len(databases) == 0:
                print("  (No databases found - workspace may be empty)")
        except Exception as search_err:
            print(f"  (Could not search databases: {search_err})")

        return True

    except Exception as e:
        print(f"ERROR: Failed to connect to Notion API")
        print(f"Error: {str(e)}")
        return False


def main():
    print("\n" + "="*80)
    print("DESKTOP CLAUDE - CONNECTION TEST")
    print("="*80)

    neon_ok = test_neon_connection()
    notion_ok = test_notion_connection()

    print("\n" + "="*80)
    print("CONNECTION TEST SUMMARY")
    print("="*80)
    print(f"Neon Database:  {'CONNECTED' if neon_ok else 'FAILED'}")
    print(f"Notion API:     {'CONNECTED' if notion_ok else 'FAILED'}")

    if neon_ok and notion_ok:
        print("\nAll connections successful! You're ready to use both services.")
    else:
        print("\nSome connections failed. Check the error messages above.")

    print("="*80 + "\n")


if __name__ == "__main__":
    main()
