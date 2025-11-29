"""
Add Notion integration support to modules table
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from shared.database.db_connection import get_engine
from sqlalchemy import text

def migrate():
    """Add Notion fields to modules table"""
    engine = get_engine()

    with engine.connect() as conn:
        # Add notion_page_id column
        try:
            conn.execute(text("""
                ALTER TABLE modules
                ADD COLUMN notion_page_id VARCHAR(255)
            """))
            conn.commit()
            print("[OK] Added notion_page_id column")
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e).lower():
                print("[SKIP] notion_page_id column already exists")
            else:
                print(f"[ERROR] Failed to add notion_page_id: {e}")

        # Add content_source column
        try:
            conn.execute(text("""
                ALTER TABLE modules
                ADD COLUMN content_source VARCHAR(50) DEFAULT 'database'
            """))
            conn.commit()
            print("[OK] Added content_source column")
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e).lower():
                print("[SKIP] content_source column already exists")
            else:
                print(f"[ERROR] Failed to add content_source: {e}")

    print("\n[OK] Migration complete!")

if __name__ == '__main__':
    migrate()
