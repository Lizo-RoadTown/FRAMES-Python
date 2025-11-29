#!/usr/bin/env python
"""
Interactive setup wizard for GitHub-Notion integration
Guides user through complete configuration process
"""
import os
import sys
from pathlib import Path
from notion_client import Client
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}ℹ {text}{Colors.ENDC}")

def print_step(number, text):
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}Step {number}: {text}{Colors.ENDC}")

def test_notion_connection():
    """Test Notion API connection"""
    api_key = os.getenv('NOTION_API_KEY')
    
    if not api_key:
        return False, "NOTION_API_KEY not found in .env file"
    
    try:
        client = Client(auth=api_key)
        me = client.users.me()
        return True, f"Connected as: {me.get('name', 'Unknown')}"
    except Exception as e:
        return False, str(e)

def list_accessible_pages():
    """List all pages accessible to the integration"""
    try:
        client = Client(auth=os.getenv('NOTION_API_KEY'))
        results = client.search(filter={'property': 'object', 'value': 'page'}).get('results', [])
        
        pages = []
        for page in results:
            title = "Untitled"
            if page.get('properties', {}).get('title', {}).get('title'):
                title = page['properties']['title']['title'][0].get('plain_text', 'Untitled')
            pages.append((page['id'], title))
        
        return pages
    except Exception as e:
        print_error(f"Failed to list pages: {e}")
        return []

def create_workspace(parent_page_id):
    """Create Notion workspace databases"""
    try:
        # Import the workspace creation function
        sys.path.insert(0, str(Path(__file__).parent))
        from create_notion_workspace import setup_workspace
        
        result = setup_workspace(parent_page_id)
        return True, result
    except Exception as e:
        return False, str(e)

def update_env_file(tasks_db_id, parent_page_id):
    """Update .env file with new IDs"""
    env_path = Path(__file__).parent.parent / '.env'
    
    try:
        # Read existing .env
        if env_path.exists():
            with open(env_path, 'r') as f:
                lines = f.readlines()
        else:
            lines = []
        
        # Remove old entries
        lines = [l for l in lines if not l.startswith('NOTION_TASKS_DB_ID=') 
                 and not l.startswith('NOTION_PARENT_PAGE_ID=')]
        
        # Add new entries
        if not any('NOTION_TASKS_DB_ID' in l for l in lines):
            lines.append(f"\n# Notion Workspace IDs (auto-generated)\n")
            lines.append(f"NOTION_TASKS_DB_ID={tasks_db_id}\n")
            lines.append(f"NOTION_PARENT_PAGE_ID={parent_page_id}\n")
        
        # Write back
        with open(env_path, 'w') as f:
            f.writelines(lines)
        
        return True
    except Exception as e:
        return False, str(e)

def generate_github_secrets_instructions(tasks_db_id, parent_page_id):
    """Generate instructions for setting GitHub secrets"""
    api_key = os.getenv('NOTION_API_KEY')
    
    print_header("GitHub Repository Secrets Setup")
    
    print("📋 Copy these values to your GitHub repository secrets:\n")
    print("Go to: https://github.com/YOUR_USERNAME/YOUR_REPO/settings/secrets/actions\n")
    
    print(f"{Colors.BOLD}Secret 1: NOTION_API_KEY{Colors.ENDC}")
    print(f"Value: {Colors.OKCYAN}{api_key}{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}Secret 2: NOTION_TASKS_DB_ID{Colors.ENDC}")
    print(f"Value: {Colors.OKCYAN}{tasks_db_id}{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}Secret 3: NOTION_PARENT_PAGE_ID{Colors.ENDC}")
    print(f"Value: {Colors.OKCYAN}{parent_page_id}{Colors.ENDC}\n")
    
    print(f"{Colors.WARNING}How to add each secret:{Colors.ENDC}")
    print("1. Click 'New repository secret'")
    print("2. Enter the name exactly as shown above")
    print("3. Paste the value")
    print("4. Click 'Add secret'")
    print("5. Repeat for all 3 secrets\n")

def main():
    """Interactive setup wizard"""
    print_header("FRAMES GitHub-Notion Integration Setup Wizard")
    
    print("This wizard will help you set up automated sync between GitHub and Notion.\n")
    print("What you'll accomplish:")
    print("  • Test Notion API connection")
    print("  • Create or select parent page in Notion")
    print("  • Create workspace databases automatically")
    print("  • Configure environment variables")
    print("  • Get GitHub secrets for Actions workflows\n")
    
    input("Press Enter to begin...")
    
    # Step 1: Test connection
    print_step(1, "Testing Notion API Connection")
    success, message = test_notion_connection()
    
    if success:
        print_success(message)
    else:
        print_error(f"Connection failed: {message}")
        print_info("Make sure NOTION_API_KEY is set in your .env file")
        return
    
    # Step 2: List or create parent page
    print_step(2, "Select or Create Parent Page")
    print("\nSearching for accessible pages in Notion...")
    
    pages = list_accessible_pages()
    
    if pages:
        print_success(f"Found {len(pages)} accessible pages:\n")
        for i, (page_id, title) in enumerate(pages, 1):
            print(f"  {i}. {title}")
            print(f"     ID: {Colors.OKCYAN}{page_id}{Colors.ENDC}\n")
        
        print(f"  {len(pages) + 1}. Create a new page in Notion and enter its ID\n")
        
        choice = input(f"Select a page (1-{len(pages) + 1}): ").strip()
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(pages):
                parent_page_id = pages[choice_num - 1][0]
                print_success(f"Selected: {pages[choice_num - 1][1]}")
            else:
                parent_page_id = input("\nEnter the page ID from Notion URL: ").strip()
        except ValueError:
            parent_page_id = input("\nEnter the page ID from Notion URL: ").strip()
    else:
        print_warning("No accessible pages found.")
        print("\nCreate a new page in Notion:")
        print("1. Open Notion and create a page titled 'FRAMES Project Hub'")
        print("2. Click 'Share' → 'Invite' → Add the FRAMES integration")
        print("3. Copy the page ID from the URL")
        print("   Example: https://notion.so/Page-Name-<THIS_IS_THE_ID>\n")
        
        parent_page_id = input("Enter the page ID: ").strip()
    
    if not parent_page_id:
        print_error("Page ID is required. Exiting.")
        return
    
    # Step 3: Create workspace
    print_step(3, "Creating Notion Workspace Databases")
    print("This will create:")
    print("  • Development Tasks database")
    print("  • Technical Decisions database")
    print("  • Integration Checklist database")
    print("  • Module Library database")
    print("  • Project Overview page\n")
    
    confirm = input("Proceed with creation? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print_warning("Skipped workspace creation.")
        print_info("You can run this later with: python scripts/create_notion_workspace.py <PAGE_ID>")
        return
    
    success, result = create_workspace(parent_page_id)
    
    if success:
        print_success("Workspace created successfully!")
        tasks_db_id = result.get('tasks')
        
        print(f"\n{Colors.BOLD}Created Resources:{Colors.ENDC}")
        print(f"  Tasks DB: {Colors.OKCYAN}{result.get('tasks')}{Colors.ENDC}")
        print(f"  Decisions DB: {Colors.OKCYAN}{result.get('decisions')}{Colors.ENDC}")
        print(f"  Integrations DB: {Colors.OKCYAN}{result.get('integrations')}{Colors.ENDC}")
        print(f"  Modules DB: {Colors.OKCYAN}{result.get('modules')}{Colors.ENDC}")
        print(f"  Overview Page: {Colors.OKCYAN}{result.get('overview')}{Colors.ENDC}")
    else:
        print_error(f"Failed to create workspace: {result}")
        return
    
    # Step 4: Update .env file
    print_step(4, "Updating Environment Configuration")
    
    success = update_env_file(tasks_db_id, parent_page_id)
    
    if success:
        print_success("Updated .env file with workspace IDs")
    else:
        print_warning("Could not update .env automatically")
        print_info(f"Manually add these to .env:")
        print(f"  NOTION_TASKS_DB_ID={tasks_db_id}")
        print(f"  NOTION_PARENT_PAGE_ID={parent_page_id}")
    
    # Step 5: GitHub secrets
    print_step(5, "Configure GitHub Repository Secrets")
    generate_github_secrets_instructions(tasks_db_id, parent_page_id)
    
    # Step 6: Final instructions
    print_step(6, "Next Steps")
    print_success("Setup Complete! 🎉\n")
    
    print("What to do next:\n")
    print("1. ✅ Add the 3 secrets to GitHub (instructions above)")
    print("2. 🔄 Trigger a workflow manually to test:")
    print("   https://github.com/YOUR_USERNAME/YOUR_REPO/actions")
    print("3. 📝 Create a test task in Notion and verify it syncs to GitHub")
    print("4. 🐛 Create a GitHub issue with 'notion-sync' label and verify it syncs to Notion")
    print("5. 📚 Read the full guide: NOTION_GITHUB_INTEGRATION_SETUP.md\n")
    
    print_info("Test the sync manually:")
    print(f"  python scripts\\notion_github_sync.py\n")
    
    print_header("Setup Wizard Complete")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Setup cancelled by user.{Colors.ENDC}\n")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
