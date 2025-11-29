#!/usr/bin/env python3
"""
Create FRAMES Notion Workspace
Creates databases and parent pages for project management in Notion.
Matches the exact schema from PowerShell version.
"""

import os
import sys
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

# Configuration
NOTION_TOKEN = os.getenv('NOTION_TOKEN') or os.getenv('NOTION_API_KEY')
PARENT_PAGE_ID = os.getenv('NOTION_PARENT_PAGE_ID', '')

if not NOTION_TOKEN:
    print("❌ Error: NOTION_TOKEN environment variable not set")
    sys.exit(1)

notion = Client(auth=NOTION_TOKEN)


def create_database(parent_page_id, title, properties):
    """Create a new Notion database"""
    try:
        database = notion.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            title=[{"type": "text", "text": {"content": title}}],
            properties=properties
        )
        return database
    except Exception as e:
        print(f"❌ Error creating {title}: {e}")
        sys.exit(1)


def patch_database(db_id, properties):
    """Update database properties"""
    try:
        return notion.databases.update(
            database_id=db_id,
            properties=properties
        )
    except Exception as e:
        print(f"❌ Error patching database {db_id}: {e}")
        sys.exit(1)


def create_page(parent_page_id, title, children):
    """Create a new Notion page"""
    try:
        page = notion.pages.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            properties={
                "title": {"title": [{"text": {"content": title}}]}
            }
        )
        
        # Add content blocks
        if children:
            notion.blocks.children.append(
                block_id=page['id'],
                children=children
            )
        
        return page
    except Exception as e:
        print(f"❌ Error creating page {title}: {e}")
        sys.exit(1)


# ============================================================================
# Database Schemas
# ============================================================================

def create_development_tasks_db(parent_page_id):
    """Create Development Tasks database"""
    properties = {
        "Task": {"title": {}},
        "Status": {
            "status": {
                "options": [
                    {"name": "Not Started"},
                    {"name": "In Progress"},
                    {"name": "In Review"},
                    {"name": "Blocked"},
                    {"name": "Done"}
                ]
            }
        },
        "GitHub Issue URL": {"url": {}},
        "Due": {"date": {}},
        "Phase": {
            "select": {
                "options": [
                    {"name": "Phase 1"},
                    {"name": "Phase 2"},
                    {"name": "Phase 3"},
                    {"name": "Phase 4"},
                    {"name": "Phase 5"},
                    {"name": "Phase 6"}
                ]
            }
        },
        "Application": {
            "select": {
                "options": [
                    {"name": "LMS"},
                    {"name": "Analytics"},
                    {"name": "AI Core"},
                    {"name": "Infra"}
                ]
            }
        },
        "Priority": {
            "select": {
                "options": [
                    {"name": "P0"},
                    {"name": "P1"},
                    {"name": "P2"},
                    {"name": "P3"}
                ]
            }
        },
        "Type": {
            "select": {
                "options": [
                    {"name": "Feature"},
                    {"name": "Bug"},
                    {"name": "Chore"}
                ]
            }
        },
        "Blocked?": {"checkbox": {}},
        "Blocker": {"rich_text": {}},
        "Effort": {"number": {"format": "number"}}
    }
    
    return create_database(parent_page_id, "Development Tasks", properties)


def create_module_library_db(parent_page_id):
    """Create Module Library database"""
    properties = {
        "Module Name": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "Intake"},
                    {"name": "Drafting"},
                    {"name": "In Review"},
                    {"name": "Ready"},
                    {"name": "Live"}
                ]
            }
        },
        "Team Lead": {"people": {}},
        "Owner": {"people": {}},
        "University": {"select": {"options": []}},
        "Cohort": {"select": {"options": []}},
        "Content Source": {
            "select": {
                "options": [
                    {"name": "AI-assisted"},
                    {"name": "Form"},
                    {"name": "Interview"}
                ]
            }
        },
        "GitHub Branch/PR": {"url": {}},
        "Last Updated": {"date": {}},
        "Application": {
            "select": {
                "options": [{"name": "LMS"}]
            }
        }
    }
    
    return create_database(parent_page_id, "Module Library", properties)


def create_technical_decisions_db(parent_page_id):
    """Create Technical Decisions database"""
    properties = {
        "Decision": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "Proposed"},
                    {"name": "Approved"},
                    {"name": "Implemented"},
                    {"name": "Reversed"}
                ]
            }
        },
        "Impact": {
            "select": {
                "options": [
                    {"name": "High"},
                    {"name": "Medium"},
                    {"name": "Low"}
                ]
            }
        },
        "Context": {"rich_text": {}},
        "Rationale": {"rich_text": {}},
        "Reversible?": {"checkbox": {}}
    }
    
    return create_database(parent_page_id, "Technical Decisions", properties)


def create_integration_checklist_db(parent_page_id):
    """Create Integration Checklist database"""
    properties = {
        "Integration": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "Planned"},
                    {"name": "Setup"},
                    {"name": "Active"},
                    {"name": "Done"},
                    {"name": "Deprecated"}
                ]
            }
        },
        "Priority": {
            "select": {
                "options": [
                    {"name": "P0"},
                    {"name": "P1"},
                    {"name": "P2"},
                    {"name": "P3"}
                ]
            }
        },
        "Owner": {"people": {}},
        "Last Health Check": {"date": {}},
        "Next Action": {"rich_text": {}},
        "Cost": {"number": {"format": "dollar"}}
    }
    
    return create_database(parent_page_id, "Integration Checklist", properties)



# ============================================================================
# Page Templates
# ============================================================================

def create_delivery_dashboard(parent_page_id):
    """Create Delivery Dashboard page"""
    children = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Add linked views from Development Tasks:"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Sprint Board: Board; Group by Status; Sort Priority desc"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "This Week: Table/List; Filter Due is within next 7 days; Sort Due asc, Priority desc"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Blocked: Table/List; Filter Blocked? = checked; Sort Priority desc"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "By Phase: Table; Group by Phase; Sort Priority desc"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Add linked view from Integration Checklist:"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Active Integrations: Table; Filter Status is not Done/Deprecated; Show Owner, Next Action, Last Health Check; Sort Priority desc, Last Health Check desc"}}]
            }
        }
    ]
    return create_page(parent_page_id, "Delivery Dashboard", children)


def create_lms_page(parent_page_id):
    """Create Student Onboarding LMS page"""
    children = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Module Library views to add:"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Intake Queue: Status = Intake or Drafting; Sort Last Updated desc; Show Team Lead, University, Cohort, Content Source, Related Task"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Review Queue: Status = In Review; Sort Last Updated desc; Show Team Lead, University, Cohort, Related Task, GitHub Branch/PR"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Live Catalog: Status = Live; Gallery/Table; Sort Last Updated desc; Show University, Cohort, Owner, GitHub Branch/PR"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "By Team Lead: Board; Group by Team Lead; Sort Last Updated desc; Show Status, University, Cohort"}}]
            }
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Intake Form:"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Create a Notion Form into Module Library with defaults Status=Intake, Application=LMS, Content Source=Form"}}]
            }
        }
    ]
    return create_page(parent_page_id, "Student Onboarding LMS", children)


def create_docs_hub(parent_page_id):
    """Create Documentation Hub page"""
    children = [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "📄"},
                "rich_text": [{"type": "text", "text": {"content": "Docs are synced from GitHub /docs; edit in GitHub. Notion is read-only for these pages."}}]
            }
        }
    ]
    return create_page(parent_page_id, "Documentation Hub", children)


def create_weekly_review(parent_page_id):
    """Create Weekly Review Template page"""
    children = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Weekly Review Template"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Completed: linked view of Development Tasks filtered Status=Done and Last Edited Time is within past 7 days"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "In Progress: linked view Status=In Progress"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Blockers: linked view Blocked? = checked"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Decisions: linked view of Technical Decisions filtered Last Edited Time within past 7 days"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Next Week Top 3: simple checklist"}}]
            }
        }
    ]
    return create_page(parent_page_id, "Weekly Review Template", children)


# ============================================================================
# Main Setup
# ============================================================================

def setup_workspace(parent_page_id):
    """Set up complete FRAMES Notion workspace"""
    print()
    print("🚀 Creating FRAMES Notion Workspace...")
    print()
    
    # ========================================================================
    # 1. Create Databases
    # ========================================================================
    print("📊 Creating Development Tasks database...")
    dev_db = create_development_tasks_db(parent_page_id)
    dev_db_id = dev_db["id"]
    print(f"   ✅ Development Tasks DB: {dev_db_id}")
    
    print("📚 Creating Module Library database...")
    mod_db = create_module_library_db(parent_page_id)
    mod_db_id = mod_db["id"]
    print(f"   ✅ Module Library DB: {mod_db_id}")
    
    print("🎯 Creating Technical Decisions database...")
    dec_db = create_technical_decisions_db(parent_page_id)
    dec_db_id = dec_db["id"]
    print(f"   ✅ Technical Decisions DB: {dec_db_id}")
    
    print("🔗 Creating Integration Checklist database...")
    int_db = create_integration_checklist_db(parent_page_id)
    int_db_id = int_db["id"]
    print(f"   ✅ Integration Checklist DB: {int_db_id}")
    
    # ========================================================================
    # 2. Add Relations
    # ========================================================================
    print()
    print("🔗 Patching relations...")
    
    patch_database(mod_db_id, {
        "Related Task": {
            "relation": {"database_id": dev_db_id}
        }
    })
    print("   ✅ Module Library → Development Tasks")
    
    patch_database(dec_db_id, {
        "Related Task": {
            "relation": {"database_id": dev_db_id}
        }
    })
    print("   ✅ Technical Decisions → Development Tasks")
    
    # ========================================================================
    # 3. Create Parent Pages
    # ========================================================================
    print()
    print("📄 Creating parent pages...")
    
    create_delivery_dashboard(parent_page_id)
    print("   ✅ Delivery Dashboard")
    
    create_lms_page(parent_page_id)
    print("   ✅ Student Onboarding LMS")
    
    create_docs_hub(parent_page_id)
    print("   ✅ Documentation Hub")
    
    create_weekly_review(parent_page_id)
    print("   ✅ Weekly Review Template")
    
    # ========================================================================
    # Summary
    # ========================================================================
    print()
    print("=" * 60)
    print("✨ All done! FRAMES Notion Workspace created successfully.")
    print("=" * 60)
    print()
    print("📊 Database IDs:")
    print(f"   Development Tasks:     {dev_db_id}")
    print(f"   Module Library:        {mod_db_id}")
    print(f"   Technical Decisions:   {dec_db_id}")
    print(f"   Integration Checklist: {int_db_id}")
    print()
    print("📄 Pages created:")
    print("   • Delivery Dashboard")
    print("   • Student Onboarding LMS")
    print("   • Documentation Hub")
    print("   • Weekly Review Template")
    print()
    print("🔗 Next steps:")
    print("   1. Open your Notion workspace")
    print("   2. Add linked database views as described in each page")
    print("   3. Customize views, filters, and sorts as needed")
    print("   4. Create a Notion Form for the Module Library")
    print()
    
    return {
        'development_tasks': dev_db_id,
        'module_library': mod_db_id,
        'technical_decisions': dec_db_id,
        'integration_checklist': int_db_id
    }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        if not PARENT_PAGE_ID:
            print("Usage: python scripts/create_notion_workspace.py <PARENT_PAGE_ID>")
            print("\nOr set environment variable:")
            print("  $env:NOTION_PARENT_PAGE_ID='your-page-id-here'")
            print("\nSteps:")
            print("1. Create a new page in Notion")
            print("2. Share it with the FRAMES integration")
            print("3. Copy the page ID from the URL")
            print("4. Run this script with the page ID or set it as env var")
            sys.exit(1)
        parent_page_id = PARENT_PAGE_ID
    else:
        parent_page_id = sys.argv[1]
    
    setup_workspace(parent_page_id)
