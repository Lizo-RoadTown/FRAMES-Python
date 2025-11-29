"""
Create a root workspace page that the integration owns
This doesn't require pre-sharing a parent page
"""
import os
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

client = Client(auth=os.getenv('NOTION_API_KEY'))

print("Attempting to create FRAMES workspace root...")
print("=" * 60)

# Verify authentication
try:
    me = client.users.me()
    print(f"[OK] Authenticated as: {me.get('name')}")
    print(f"     Bot ID: {me.get('id')}")
except Exception as e:
    print(f"[ERROR] Authentication failed: {e}")
    exit(1)

# Try to create a page in the integration's workspace
# Note: This may not work - integrations typically can't create root pages
try:
    print("\nAttempting to create workspace root page...")
    page = client.pages.create(
        parent={"type": "workspace", "workspace": True},
        properties={
            "title": [
                {
                    "type": "text",
                    "text": {"content": "FRAMES LMS Workspace"}
                }
            ]
        },
        children=[
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "FRAMES Learning Management System"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": "Welcome to the FRAMES workspace. This page was created automatically by the FRAMES integration."}
                    }]
                }
            }
        ]
    )

    print(f"[OK] Created workspace root!")
    print(f"     Page ID: {page['id']}")
    print(f"     URL: {page['url']}")
    print(f"\nYou can now run:")
    print(f"     python scripts/create_notion_workspace.py {page['id']}")

except Exception as e:
    print(f"[ERROR] Could not create root page: {e}")
    print("\nThis is expected - integrations cannot create root workspace pages.")
    print("\nYou need to manually:")
    print("1. Go to Notion and create a new page called 'FRAMES LMS Workspace'")
    print("2. Click the '...' menu (top right) > 'Add connections'")
    print("3. Search for and select 'FRAMES'")
    print("4. Copy the page ID from the URL (the long string after the title)")
    print("5. Run: python scripts/create_notion_workspace.py <PAGE_ID>")
    print("\nExample page URL: https://www.notion.so/Page-Title-2b76b8ea578a8040b328c8527dedea93")
    print("Example page ID: 2b76b8ea578a8040b328c8527dedea93")
