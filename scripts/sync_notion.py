"""
Notion API Integration - Sync Documentation to Notion
Automatically updates FRAMES LMS documentation in Notion workspace
"""
import os
from pathlib import Path
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Notion client
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
if not NOTION_API_KEY:
    raise ValueError("NOTION_API_KEY not found in .env file")

notion = Client(auth=NOTION_API_KEY)

# Documentation files to sync
DOCS_DIR = Path(__file__).resolve().parents[1] / 'docs' / 'lms' / 'notion-import'

DOCUMENTATION_FILES = [
    {
        'file': '01-PROJECT-OVERVIEW.md',
        'title': 'Project Overview',
        'icon': '📘'
    },
    {
        'file': '02-MODULE-TYPE-SPECIFICATIONS.md',
        'title': 'Module Type Specifications',
        'icon': '📚'
    },
    {
        'file': '03-DATABASE-SCHEMA.md',
        'title': 'Database Schema',
        'icon': '🗄️'
    },
    {
        'file': '04-DEVELOPMENT-ROADMAP.md',
        'title': 'Development Roadmap',
        'icon': '🗺️'
    },
    {
        'file': '05-INTEGRATION-CHECKLIST.md',
        'title': 'Integration Checklist',
        'icon': '✅'
    },
    {
        'file': '06-TECHNICAL-DECISIONS.md',
        'title': 'Technical Decisions',
        'icon': '⚙️'
    }
]


def markdown_to_notion_blocks(markdown_text):
    """
    Convert markdown to Notion blocks.
    This is a simplified converter - Notion API supports rich blocks.
    For now, we'll create paragraph blocks for each line.

    Future enhancement: Parse markdown properly (headers, lists, code blocks)
    """
    blocks = []
    lines = markdown_text.split('\n')

    for line in lines:
        if not line.strip():
            continue

        # Headers
        if line.startswith('# '):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })
        elif line.startswith('## '):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                }
            })
        elif line.startswith('### '):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                }
            })
        # Code blocks
        elif line.startswith('```'):
            # TODO: Handle code blocks properly
            continue
        # Bullet lists
        elif line.strip().startswith('- '):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line.strip()[2:]}}]
                }
            })
        # Regular paragraphs
        else:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": line}}]
                }
            })

    return blocks


def create_or_update_page(parent_page_id, doc_config):
    """
    Create or update a documentation page in Notion.

    Args:
        parent_page_id: ID of parent page in Notion
        doc_config: Dict with 'file', 'title', 'icon'
    """
    file_path = DOCS_DIR / doc_config['file']

    print(f"Processing {doc_config['title']}...")

    # Read markdown file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Convert to Notion blocks
    blocks = markdown_to_notion_blocks(content)

    # Limit to first 100 blocks (Notion API limit)
    if len(blocks) > 100:
        print(f"  Warning: {len(blocks)} blocks found, limiting to 100")
        blocks = blocks[:100]

    try:
        # Create new page
        page = notion.pages.create(
            parent={"page_id": parent_page_id},
            icon={"type": "emoji", "emoji": doc_config['icon']},
            properties={
                "title": {
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": doc_config['title']}
                        }
                    ]
                }
            },
            children=blocks[:100]  # Notion allows max 100 blocks in create
        )

        print(f"  [OK] Created: {doc_config['title']} (ID: {page['id']})")
        return page['id']

    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        return None


def sync_documentation(parent_page_id):
    """
    Sync all documentation files to Notion.

    Args:
        parent_page_id: ID of the parent page in Notion where docs will be created
    """
    print(f"\n{'='*60}")
    print("FRAMES LMS - Notion Documentation Sync")
    print(f"{'='*60}\n")
    print(f"Parent Page ID: {parent_page_id}")
    print(f"Documentation Directory: {DOCS_DIR}\n")

    for doc in DOCUMENTATION_FILES:
        create_or_update_page(parent_page_id, doc)

    print(f"\n{'='*60}")
    print("[OK] Sync Complete!")
    print(f"{'='*60}\n")


def test_connection():
    """Test Notion API connection"""
    print("Testing Notion API connection...")
    try:
        # List all accessible pages
        response = notion.search(filter={"property": "object", "value": "page"})
        print(f"[OK] Connected! Found {len(response['results'])} accessible pages.")

        # Print first few pages
        print("\nAccessible pages:")
        for page in response['results'][:5]:
            title = page['properties'].get('title', {})
            if title:
                title_text = title.get('title', [{}])[0].get('plain_text', 'Untitled')
            else:
                title_text = 'Untitled'
            print(f"  - {title_text} (ID: {page['id']})")

        return True
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return False


if __name__ == '__main__':
    import sys

    # Test connection first
    if not test_connection():
        print("\n[WARNING] Fix connection issues before syncing.")
        sys.exit(1)

    # Get parent page ID
    if len(sys.argv) > 1:
        parent_page_id = sys.argv[1]
    else:
        print("\n" + "="*60)
        print("How to use this script:")
        print("="*60)
        print("\n1. Create a page in Notion for FRAMES LMS documentation")
        print("2. Copy the page ID from the URL:")
        print("   https://notion.so/Your-Page-Name-<THIS-IS-THE-PAGE-ID>")
        print("3. Run: python scripts/sync_notion.py <PAGE_ID>")
        print("\nExample:")
        print("  python scripts/sync_notion.py abc123def456\n")

        parent_page_id = input("Enter parent page ID (or press Enter to skip): ").strip()

        if not parent_page_id:
            print("\n[SKIP] Skipping sync. Run again with page ID when ready.")
            sys.exit(0)

    # Sync documentation
    sync_documentation(parent_page_id)
