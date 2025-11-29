#!/usr/bin/env python3
"""
Create Visually Enhanced FRAMES Notion Workspace
Creates beautiful, color-coded databases and pages for project management.
"""

import os
import sys
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv('NOTION_TOKEN') or os.getenv('NOTION_API_KEY')
PARENT_PAGE_ID = os.getenv('NOTION_PARENT_PAGE_ID', '')

if not NOTION_TOKEN:
    print("❌ Error: NOTION_TOKEN environment variable not set")
    sys.exit(1)

notion = Client(auth=NOTION_TOKEN)


def create_database(parent_page_id, title, icon_emoji, properties):
    """Create a new Notion database with emoji icon"""
    try:
        database = notion.databases.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            icon={"type": "emoji", "emoji": icon_emoji},
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
        return notion.databases.update(database_id=db_id, properties=properties)
    except Exception as e:
        print(f"❌ Error patching database {db_id}: {e}")
        sys.exit(1)


def create_page(parent_page_id, title, icon_emoji, children):
    """Create a new Notion page with icon and content"""
    try:
        page = notion.pages.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            icon={"type": "emoji", "emoji": icon_emoji},
            properties={"title": {"title": [{"text": {"content": title}}]}}
        )
        
        if children:
            notion.blocks.children.append(block_id=page['id'], children=children)
        
        return page
    except Exception as e:
        print(f"❌ Error creating page {title}: {e}")
        sys.exit(1)


# ============================================================================
# Database Schemas with Enhanced Status Options
# ============================================================================

def create_development_tasks_db(parent_page_id):
    """Create Development Tasks database"""
    properties = {
        "Task": {"title": {}},
        "Status": {
            "status": {
                "options": [
                    {"name": "📋 Not Started", "color": "gray"},
                    {"name": "🚧 In Progress", "color": "blue"},
                    {"name": "👀 In Review", "color": "yellow"},
                    {"name": "🚨 Blocked", "color": "red"},
                    {"name": "✅ Done", "color": "green"}
                ],
                "groups": [
                    {"id": "todo", "name": "To Do", "color": "gray", "option_ids": ["📋 Not Started"]},
                    {"id": "active", "name": "Active", "color": "blue", "option_ids": ["🚧 In Progress", "👀 In Review"]},
                    {"id": "blocked", "name": "Issues", "color": "red", "option_ids": ["🚨 Blocked"]},
                    {"id": "done", "name": "Complete", "color": "green", "option_ids": ["✅ Done"]}
                ]
            }
        },
        "Priority": {
            "select": {
                "options": [
                    {"name": "🔥 P0 Critical", "color": "red"},
                    {"name": "⚡ P1 High", "color": "orange"},
                    {"name": "📌 P2 Medium", "color": "yellow"},
                    {"name": "💤 P3 Low", "color": "gray"}
                ]
            }
        },
        "Phase": {
            "select": {
                "options": [
                    {"name": "1️⃣ Foundation", "color": "green"},
                    {"name": "2️⃣ Discord", "color": "purple"},
                    {"name": "3️⃣ GitHub", "color": "default"},
                    {"name": "4️⃣ PostgreSQL", "color": "blue"},
                    {"name": "5️⃣ LMS", "color": "pink"},
                    {"name": "6️⃣ AI Core", "color": "orange"}
                ]
            }
        },
        "Application": {
            "select": {
                "options": [
                    {"name": "📚 LMS", "color": "blue"},
                    {"name": "📊 Analytics", "color": "green"},
                    {"name": "🤖 AI Core", "color": "purple"},
                    {"name": "🔧 Infrastructure", "color": "gray"}
                ]
            }
        },
        "Type": {
            "select": {
                "options": [
                    {"name": "✨ Feature", "color": "blue"},
                    {"name": "🐛 Bug", "color": "red"},
                    {"name": "🔧 Chore", "color": "gray"},
                    {"name": "📖 Documentation", "color": "yellow"}
                ]
            }
        },
        "GitHub Issue URL": {"url": {}},
        "Due": {"date": {}},
        "Estimated Hours": {"number": {"format": "number"}},
        "Actual Hours": {"number": {"format": "number"}},
        "Blocked?": {"checkbox": {}},
        "Blocker Description": {"rich_text": {}},
        "Notes": {"rich_text": {}}
    }
    
    return create_database(parent_page_id, "Development Tasks", "📝", properties)


def create_module_library_db(parent_page_id):
    """Create Module Library database"""
    properties = {
        "Module Name": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "📥 Intake", "color": "gray"},
                    {"name": "✏️ Drafting", "color": "yellow"},
                    {"name": "👀 In Review", "color": "orange"},
                    {"name": "✅ Ready", "color": "blue"},
                    {"name": "🚀 Live", "color": "green"}
                ]
            }
        },
        "University": {
            "select": {
                "options": [
                    {"name": "🎓 Cal Poly Pomona", "color": "green"},
                    {"name": "🎓 Texas State", "color": "orange"},
                    {"name": "🎓 Columbia", "color": "blue"},
                    {"name": "🎓 Other", "color": "gray"}
                ]
            }
        },
        "Cohort": {
            "select": {
                "options": [
                    {"name": "2024-2025", "color": "blue"},
                    {"name": "2025-2026", "color": "green"},
                    {"name": "2026-2027", "color": "purple"}
                ]
            }
        },
        "Content Source": {
            "select": {
                "options": [
                    {"name": "🤖 AI-assisted", "color": "purple"},
                    {"name": "📝 Form", "color": "blue"},
                    {"name": "🎙️ Interview", "color": "orange"}
                ]
            }
        },
        "Team Lead": {"people": {}},
        "Owner": {"people": {}},
        "GitHub Branch/PR": {"url": {}},
        "Last Updated": {"date": {}},
        "Application": {
            "select": {
                "options": [{"name": "📚 LMS", "color": "blue"}]
            }
        }
    }
    
    return create_database(parent_page_id, "Module Library", "📚", properties)


def create_technical_decisions_db(parent_page_id):
    """Create Technical Decisions database"""
    properties = {
        "Decision": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "💭 Proposed", "color": "gray"},
                    {"name": "✅ Approved", "color": "green"},
                    {"name": "🚀 Implemented", "color": "blue"},
                    {"name": "🔄 Reversed", "color": "red"}
                ]
            }
        },
        "Impact": {
            "select": {
                "options": [
                    {"name": "🔴 High", "color": "red"},
                    {"name": "🟡 Medium", "color": "yellow"},
                    {"name": "🟢 Low", "color": "green"}
                ]
            }
        },
        "Decision Date": {"date": {}},
        "Context": {"rich_text": {}},
        "Options Considered": {"rich_text": {}},
        "Rationale": {"rich_text": {}},
        "Reversible?": {"checkbox": {}}
    }
    
    return create_database(parent_page_id, "Technical Decisions", "🎯", properties)


def create_integration_checklist_db(parent_page_id):
    """Create Integration Checklist database"""
    properties = {
        "Integration": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "📋 Planned", "color": "gray"},
                    {"name": "🔧 Setup", "color": "yellow"},
                    {"name": "✅ Active", "color": "green"},
                    {"name": "⏸️ Paused", "color": "orange"},
                    {"name": "❌ Deprecated", "color": "red"}
                ]
            }
        },
        "Priority": {
            "select": {
                "options": [
                    {"name": "🔥 P0", "color": "red"},
                    {"name": "⚡ P1", "color": "orange"},
                    {"name": "📌 P2", "color": "yellow"},
                    {"name": "💤 P3", "color": "gray"}
                ]
            }
        },
        "Purpose": {"rich_text": {}},
        "API Documentation": {"url": {}},
        "Owner": {"people": {}},
        "Last Health Check": {"date": {}},
        "Next Action": {"rich_text": {}},
        "Monthly Cost": {"number": {"format": "dollar"}},
        "Notes": {"rich_text": {}}
    }
    
    return create_database(parent_page_id, "Integration Checklist", "🔗", properties)


# ============================================================================
# Enhanced Page Templates with Visual Elements
# ============================================================================

def create_delivery_dashboard(parent_page_id):
    """Create visually enhanced Delivery Dashboard"""
    children = [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "🎯"},
                "color": "blue_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Welcome to the FRAMES Delivery Dashboard - Your central command center for tracking development progress."
                }}]
            }
        },
        {"object": "block", "type": "divider", "divider": {}},
        
        # This Week Section
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "📅 This Week"}}],
                "color": "blue"
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "💡"},
                "color": "yellow_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add a linked view: Development Tasks → Filter: Due is within 7 days → Sort: Priority desc, Due asc"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        # Sprint Board Section
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🚧 Active Sprint"}}],
                "color": "purple"
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "💡"},
                "color": "yellow_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add a linked view: Development Tasks → Board view → Group by: Status → Sort: Priority desc"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        # Blockers Section
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🚨 Blockers"}}],
                "color": "red"
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "⚠️"},
                "color": "red_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add a linked view: Development Tasks → Filter: Blocked? = checked → Sort: Priority desc"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        # Integrations Section
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🔗 Active Integrations"}}],
                "color": "green"
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "💡"},
                "color": "yellow_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add a linked view: Integration Checklist → Filter: Status ≠ Deprecated → Show: Owner, Next Action, Last Health Check"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        # Quick Actions
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "⚡ Quick Actions"}}]
            }
        },
        {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Review blocked tasks"}}],
                "checked": False
            }
        },
        {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Update task statuses"}}],
                "checked": False
            }
        },
        {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Check integration health"}}],
                "checked": False
            }
        }
    ]
    return create_page(parent_page_id, "🏠 Delivery Dashboard", "🏠", children)


def create_lms_page(parent_page_id):
    """Create Student Onboarding LMS page"""
    children = [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "📚"},
                "color": "blue_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Student Onboarding LMS - AI-powered learning management for training incoming students across 8 universities."
                }}]
            }
        },
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "📥 Intake Queue"}}],
                "color": "orange"
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "💡"},
                "color": "yellow_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add linked view: Module Library → Filter: Status = Intake or Drafting → Show: Team Lead, University, Cohort, Content Source"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "👀 Review Queue"}}],
                "color": "yellow"
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "💡"},
                "color": "yellow_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add linked view: Module Library → Filter: Status = In Review → Show: Team Lead, GitHub Branch/PR, Related Task"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🚀 Live Catalog"}}],
                "color": "green"
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "💡"},
                "color": "yellow_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add linked view: Module Library → Filter: Status = Live → Gallery or Table view → Show: University, Cohort, Owner"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📝 Module Intake Form"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "ℹ️"},
                "color": "gray_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Create a Notion Form connected to Module Library database with defaults: Status = 📥 Intake, Application = 📚 LMS, Content Source = 📝 Form"
                }}]
            }
        }
    ]
    return create_page(parent_page_id, "📚 Student Onboarding LMS", "📚", children)


def create_docs_hub(parent_page_id):
    """Create Documentation Hub page"""
    children = [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "📖"},
                "color": "gray_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Documentation is synced from GitHub /docs folder. Edit files in GitHub - Notion pages are read-only mirrors."
                }}]
            }
        },
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🏗️ Architecture"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "System Overview (from README.md)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Database Schema"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "API Documentation"}}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🚀 Deployment"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "PythonAnywhere Setup"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "PostgreSQL Hosting"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Environment Variables"}}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "💻 Development"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Getting Started (START_HERE.md)"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Git Workflow"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Testing Strategy"}}]
            }
        }
    ]
    return create_page(parent_page_id, "📖 Documentation Hub", "📖", children)


def create_weekly_review(parent_page_id):
    """Create Weekly Review Template"""
    children = [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "📅"},
                "color": "purple_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Use this template weekly to track progress, identify blockers, and plan ahead. Duplicate this page each week."
                }}]
            }
        },
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "✅ Completed This Week"}}],
                "color": "green"
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "💡"},
                "color": "yellow_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add linked view: Development Tasks → Filter: Status = ✅ Done AND Last Edited Time within 7 days"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🚧 In Progress"}}],
                "color": "blue"
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "💡"},
                "color": "yellow_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add linked view: Development Tasks → Filter: Status = 🚧 In Progress"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🚨 Blockers"}}],
                "color": "red"
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "💡"},
                "color": "yellow_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add linked view: Development Tasks → Filter: Blocked? = checked"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🎯 Next Week Top 3"}}]
            }
        },
        {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Priority 1: [Add task]"}}],
                "checked": False
            }
        },
        {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Priority 2: [Add task]"}}],
                "checked": False
            }
        },
        {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Priority 3: [Add task]"}}],
                "checked": False
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "💭 Notes & Learnings"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "📝"},
                "color": "gray_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "What worked well? What was challenging? Key insights or decisions made this week?"
                }}]
            }
        }
    ]
    return create_page(parent_page_id, "📅 Weekly Review Template", "📅", children)


# ============================================================================
# Main Setup
# ============================================================================

def setup_workspace(parent_page_id):
    """Set up complete FRAMES Notion workspace with visual enhancements"""
    print()
    print("✨ Creating Visually Enhanced FRAMES Notion Workspace...")
    print()
    
    # Create Databases
    print("📊 Creating databases...")
    dev_db = create_development_tasks_db(parent_page_id)
    print(f"   ✅ Development Tasks: {dev_db['id']}")
    
    mod_db = create_module_library_db(parent_page_id)
    print(f"   ✅ Module Library: {mod_db['id']}")
    
    dec_db = create_technical_decisions_db(parent_page_id)
    print(f"   ✅ Technical Decisions: {dec_db['id']}")
    
    int_db = create_integration_checklist_db(parent_page_id)
    print(f"   ✅ Integration Checklist: {int_db['id']}")
    
    # Add Relations
    print()
    print("🔗 Adding database relations...")
    patch_database(mod_db["id"], {"Related Task": {"relation": {"database_id": dev_db["id"]}}})
    print("   ✅ Module Library → Development Tasks")
    
    patch_database(dec_db["id"], {"Related Task": {"relation": {"database_id": dev_db["id"]}}})
    print("   ✅ Technical Decisions → Development Tasks")
    
    # Create Pages
    print()
    print("📄 Creating pages with visual enhancements...")
    create_delivery_dashboard(parent_page_id)
    print("   ✅ 🏠 Delivery Dashboard")
    
    create_lms_page(parent_page_id)
    print("   ✅ 📚 Student Onboarding LMS")
    
    create_docs_hub(parent_page_id)
    print("   ✅ 📖 Documentation Hub")
    
    create_weekly_review(parent_page_id)
    print("   ✅ 📅 Weekly Review Template")
    
    # Summary
    print()
    print("=" * 70)
    print("🎉 VISUAL WORKSPACE CREATED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("✨ Enhanced Features:")
    print("   • Emoji icons on all databases and pages")
    print("   • Color-coded status options with emoji prefixes")
    print("   • Callout blocks for important info")
    print("   • Dividers for visual separation")
    print("   • To-do lists for quick actions")
    print("   • Structured sections with colored headings")
    print()
    print("📊 Database IDs:")
    print(f"   Development Tasks:     {dev_db['id']}")
    print(f"   Module Library:        {mod_db['id']}")
    print(f"   Technical Decisions:   {dec_db['id']}")
    print(f"   Integration Checklist: {int_db['id']}")
    print()
    print("🎨 Next Steps:")
    print("   1. Open your Notion workspace")
    print("   2. Add linked database views as indicated in callout blocks")
    print("   3. Customize colors and layouts to your preference")
    print("   4. Duplicate the Weekly Review template for each week")
    print()
    
    return {
        'development_tasks': dev_db['id'],
        'module_library': mod_db['id'],
        'technical_decisions': dec_db['id'],
        'integration_checklist': int_db['id']
    }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        if not PARENT_PAGE_ID:
            print("Usage: python scripts/create_notion_workspace_styled.py <PARENT_PAGE_ID>")
            print("\nOr set environment variable:")
            print("  $env:NOTION_PARENT_PAGE_ID='your-page-id-here'")
            sys.exit(1)
        parent_page_id = PARENT_PAGE_ID
    else:
        parent_page_id = sys.argv[1]
    
    setup_workspace(parent_page_id)
