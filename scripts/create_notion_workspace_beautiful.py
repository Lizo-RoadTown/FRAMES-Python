#!/usr/bin/env python3
"""
Create Visually Stunning FRAMES Notion Workspace with Space-Themed Covers
Uses high-quality space photography and implements Notion design best practices.

Best Practices Implemented:
1. Cover images on all pages for visual appeal
2. Emoji icons for quick recognition
3. Callout blocks for important information
4. Consistent color coding
5. Visual hierarchy with dividers
6. Descriptive headers with context
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


# ============================================================================
# Space-Themed Cover Images (High Quality from Unsplash)
# ============================================================================

SPACE_COVERS = {
    # Deep space imagery for databases
    "development_tasks": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920&q=90",  # Galaxy spiral
    "module_library": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=1920&q=90",  # Milky Way
    "technical_decisions": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=1920&q=90",  # Earth from space
    "integration_checklist": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&q=90",  # Connected network space
    
    # Themed pages
    "dashboard": "https://images.unsplash.com/photo-1464802686167-b939a6910659?w=1920&q=90",  # Blue nebula
    "lms": "https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=1920&q=90",  # Colorful nebula
    "docs_hub": "https://images.unsplash.com/photo-1543722530-d2c3201371e7?w=1920&q=90",  # Star field
    "weekly_review": "https://images.unsplash.com/photo-1502134249126-9f3755a50d78?w=1920&q=90",  # Purple nebula
}


def create_database(parent_page_id, title, icon_emoji, properties, cover_url=None):
    """Create a new Notion database with emoji icon and optional cover image"""
    try:
        database_props = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "icon": {"type": "emoji", "emoji": icon_emoji},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties
        }
        
        # Add cover image if provided
        if cover_url:
            database_props["cover"] = {
                "type": "external",
                "external": {"url": cover_url}
            }
        
        database = notion.databases.create(**database_props)
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


def create_page(parent_page_id, title, icon_emoji, children, cover_url=None):
    """Create a new Notion page with icon, optional cover image, and content"""
    try:
        page_props = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "icon": {"type": "emoji", "emoji": icon_emoji},
            "properties": {"title": {"title": [{"text": {"content": title}}]}}
        }
        
        # Add cover image if provided
        if cover_url:
            page_props["cover"] = {
                "type": "external",
                "external": {"url": cover_url}
            }
        
        page = notion.pages.create(**page_props)
        
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
    """Create Development Tasks database with space-themed cover"""
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
        "Component": {
            "select": {
                "options": [
                    {"name": "🎨 Frontend", "color": "purple"},
                    {"name": "⚙️ Backend", "color": "blue"},
                    {"name": "🗄️ Database", "color": "brown"},
                    {"name": "🔗 Integration", "color": "orange"},
                    {"name": "📊 Analytics", "color": "green"},
                    {"name": "📱 UI/UX", "color": "pink"}
                ]
            }
        },
        "Assignee": {"people": {}},
        "Due Date": {"date": {}},
        "Estimated Hours": {"number": {"format": "number"}},
        "Notes": {"rich_text": {}},
        "Blocked?": {"checkbox": {}}
    }
    return create_database(
        parent_page_id, 
        "🚀 Development Tasks", 
        "🚀", 
        properties,
        SPACE_COVERS["development_tasks"]
    )


def create_module_library_db(parent_page_id):
    """Create Module Library database with space-themed cover"""
    properties = {
        "Module Name": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "📝 Planning", "color": "gray"},
                    {"name": "✍️ Drafting", "color": "blue"},
                    {"name": "👀 Review", "color": "yellow"},
                    {"name": "✅ Published", "color": "green"},
                    {"name": "📦 Archived", "color": "red"}
                ]
            }
        },
        "Category": {
            "select": {
                "options": [
                    {"name": "🎓 Fundamentals", "color": "blue"},
                    {"name": "🔬 Research Skills", "color": "purple"},
                    {"name": "🤝 Collaboration", "color": "green"},
                    {"name": "🛠️ Technical Tools", "color": "orange"},
                    {"name": "📊 Data Analysis", "color": "pink"}
                ]
            }
        },
        "Target Audience": {
            "multi_select": {
                "options": [
                    {"name": "🎯 Incoming Students", "color": "blue"},
                    {"name": "👥 Team Leads", "color": "purple"},
                    {"name": "👨‍🏫 Faculty", "color": "green"}
                ]
            }
        },
        "Estimated Time": {"number": {"format": "number"}},
        "Author": {"people": {}},
        "Notion Page": {"url": {}},
        "Last Updated": {"date": {}},
        "Tags": {"multi_select": {}}
    }
    return create_database(
        parent_page_id,
        "📚 Module Library",
        "📚",
        properties,
        SPACE_COVERS["module_library"]
    )


def create_technical_decisions_db(parent_page_id):
    """Create Technical Decisions database with space-themed cover"""
    properties = {
        "Decision": {"title": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "🤔 Proposed", "color": "gray"},
                    {"name": "💬 Discussing", "color": "blue"},
                    {"name": "✅ Approved", "color": "green"},
                    {"name": "⏸️ On Hold", "color": "yellow"},
                    {"name": "❌ Rejected", "color": "red"}
                ]
            }
        },
        "Impact": {
            "select": {
                "options": [
                    {"name": "🌟 High - System-wide", "color": "red"},
                    {"name": "📌 Medium - Component-level", "color": "orange"},
                    {"name": "💤 Low - Local change", "color": "gray"}
                ]
            }
        },
        "Area": {
            "select": {
                "options": [
                    {"name": "🏗️ Architecture", "color": "purple"},
                    {"name": "💾 Data Model", "color": "blue"},
                    {"name": "🎨 UI/UX", "color": "pink"},
                    {"name": "🔐 Security", "color": "red"},
                    {"name": "⚡ Performance", "color": "orange"}
                ]
            }
        },
        "Decider": {"people": {}},
        "Date Decided": {"date": {}},
        "Rationale": {"rich_text": {}},
        "Alternatives Considered": {"rich_text": {}}
    }
    return create_database(
        parent_page_id,
        "💡 Technical Decisions",
        "💡",
        properties,
        SPACE_COVERS["technical_decisions"]
    )


def create_integration_checklist_db(parent_page_id):
    """Create Integration Checklist database with space-themed cover"""
    properties = {
        "Item": {"title": {}},
        "Type": {
            "select": {
                "options": [
                    {"name": "🔌 API Endpoint", "color": "blue"},
                    {"name": "🗄️ Database Schema", "color": "purple"},
                    {"name": "🎨 UI Component", "color": "pink"},
                    {"name": "📝 Documentation", "color": "green"},
                    {"name": "✅ Testing", "color": "orange"}
                ]
            }
        },
        "Status": {
            "status": {
                "options": [
                    {"name": "⏳ Pending", "color": "gray"},
                    {"name": "🚧 In Progress", "color": "blue"},
                    {"name": "✅ Complete", "color": "green"},
                    {"name": "🚨 Blocked", "color": "red"}
                ]
            }
        },
        "Owner": {"people": {}},
        "Dependencies": {"rich_text": {}},
        "Completion Date": {"date": {}}
    }
    return create_database(
        parent_page_id,
        "✅ Integration Checklist",
        "✅",
        properties,
        SPACE_COVERS["integration_checklist"]
    )


# ============================================================================
# Enhanced Page Templates with Space Covers
# ============================================================================

def create_delivery_dashboard(parent_page_id):
    """Create main delivery dashboard with space cover"""
    children = [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "🎯"},
                "color": "blue_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Mission Control: Track all workstreams, monitor progress, and coordinate deliveries for the FRAMES project."
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🚀 Active Workstreams"}}],
                "color": "blue"
            }
        },
        
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Agent A: Notion → GitHub Export Pipeline"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "📤"},
                "color": "gray_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add linked view: Development Tasks → Filter: Component = Integration, Assignee = Agent A"
                }}]
            }
        },
        
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Agent B: React Frontend with NotionRenderer"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "⚛️"},
                "color": "gray_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add linked view: Development Tasks → Filter: Component = Frontend, Assignee = Agent B"
                }}]
            }
        },
        
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Agent C: Flask LMS API"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "🔌"},
                "color": "gray_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add linked view: Development Tasks → Filter: Component = Backend, Assignee = Agent C"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "📊 Status Overview"}}],
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
                    "content": "Add linked view: Development Tasks → Group by: Status, Sort by: Priority"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🚨 Blockers & Issues"}}],
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
                    "content": "Add linked view: Development Tasks → Filter: Blocked? = checked OR Status = Blocked"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "📚 Quick Links"}}],
                "color": "purple"
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "📖 NOTION_RENDERING_ARCHITECTURE.md - Technical guide"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "🤖 AGENT_README.md - Agent quick reference"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "🏗️ MODULE-DATA-ARCHITECTURE.md - Data flow"}}]
            }
        }
    ]
    return create_page(
        parent_page_id, 
        "🏠 Delivery Dashboard", 
        "🏠", 
        children,
        SPACE_COVERS["dashboard"]
    )


def create_lms_page(parent_page_id):
    """Create LMS overview page with colorful nebula cover"""
    children = [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "🎓"},
                "color": "purple_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Student Onboarding LMS: Interactive learning modules powered by Notion content, rendered beautifully with react-notion-x."
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "📚 Module Library"}}],
                "color": "blue"
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {
                    "content": "All learning modules are managed in the Module Library database below. Create beautiful content in Notion, and it automatically syncs to the student portal."
                }}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "💡"},
                "color": "gray_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add linked view: Module Library → Filter: Status = Published, Sort by: Category"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "✨ Content Creation Tips"}}],
                "color": "purple"
            }
        },
        {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Use headings (H1, H2, H3) for clear structure"}}],
                "checked": False
            }
        },
        {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Add callouts for important concepts"}}],
                "checked": False
            }
        },
        {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Include images, videos, and embeds"}}],
                "checked": False
            }
        },
        {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Use toggles for expandable sections"}}],
                "checked": False
            }
        },
        {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Add to-do lists for student activities"}}],
                "checked": False
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🔄 Sync Workflow"}}],
                "color": "green"
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {
                    "content": "Create module content in Notion (rich text, images, videos, etc.)"
                }}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {
                    "content": "Mark module as 'Published' in Module Library database"
                }}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {
                    "content": "Run export script to sync to GitHub and PostgreSQL"
                }}]
            }
        },
        {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {
                    "content": "Students see updated content instantly in the portal"
                }}]
            }
        }
    ]
    return create_page(
        parent_page_id,
        "📚 Student Onboarding LMS",
        "📚",
        children,
        SPACE_COVERS["lms"]
    )


def create_docs_hub(parent_page_id):
    """Create documentation hub with star field cover"""
    children = [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "📖"},
                "color": "blue_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Central hub for all FRAMES project documentation, technical decisions, and architectural guides."
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🏗️ Architecture & Design"}}],
                "color": "blue"
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {
                    "content": "NOTION_RENDERING_ARCHITECTURE.md - How Notion content flows to students"
                }}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {
                    "content": "MODULE-DATA-ARCHITECTURE.md - Three-tier content flow (Notion → GitHub → PostgreSQL)"
                }}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {
                    "content": "INTEGRATION_ARCHITECTURE.md - System integration overview"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "💡 Technical Decisions"}}],
                "color": "purple"
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {
                    "content": "Important architectural and technical decisions are documented in the Technical Decisions database."
                }}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "💡"},
                "color": "gray_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add linked view: Technical Decisions → Filter: Status = Approved, Sort by: Date Decided"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🛠️ Developer Resources"}}],
                "color": "orange"
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {
                    "content": "AGENT_README.md - Quick reference for AI agents"
                }}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {
                    "content": "shared/database/db_models.py - Database schema reference"
                }}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {
                    "content": "backend/LMS_API_README.md - API endpoint documentation"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "✅ Implementation Guides"}}],
                "color": "green"
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {
                    "content": "MODULE-CREATION-WORKFLOW.md - How to create learning modules"
                }}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {
                    "content": "QUICK_START_NOTION_INTEGRATION.md - Getting started guide"
                }}]
            }
        }
    ]
    return create_page(
        parent_page_id,
        "📖 Documentation Hub",
        "📖",
        children,
        SPACE_COVERS["docs_hub"]
    )


def create_weekly_review(parent_page_id):
    """Create weekly review template with purple nebula cover"""
    children = [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "📅"},
                "color": "purple_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Weekly Review: Reflect on progress, identify blockers, and plan for the week ahead. Duplicate this template each week."
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
                "color": "gray_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add linked view: Development Tasks → Filter: Status = Done, Date = This Week"
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
                "color": "gray_background",
                "rich_text": [{"type": "text", "text": {
                    "content": "Add linked view: Development Tasks → Filter: Status = In Progress OR In Review"
                }}]
            }
        },
        
        {"object": "block", "type": "divider", "divider": {}},
        
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🚨 Blockers & Challenges"}}],
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
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "🎯 Next Week Top 3"}}],
                "color": "purple"
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
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "💭 Notes & Learnings"}}],
                "color": "orange"
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
    return create_page(
        parent_page_id,
        "📅 Weekly Review Template",
        "📅",
        children,
        SPACE_COVERS["weekly_review"]
    )


# ============================================================================
# Main Setup
# ============================================================================

def setup_workspace(parent_page_id):
    """Set up complete FRAMES Notion workspace with stunning space-themed visuals"""
    print()
    print("✨ Creating Visually Stunning FRAMES Notion Workspace...")
    print("🌌 With high-quality space photography from Unsplash")
    print()
    
    # Create Databases with Cover Images
    print("📊 Creating databases with space-themed covers...")
    dev_db = create_development_tasks_db(parent_page_id)
    print(f"   ✅ Development Tasks (Galaxy spiral): {dev_db['id']}")
    
    mod_db = create_module_library_db(parent_page_id)
    print(f"   ✅ Module Library (Milky Way): {mod_db['id']}")
    
    dec_db = create_technical_decisions_db(parent_page_id)
    print(f"   ✅ Technical Decisions (Earth from space): {dec_db['id']}")
    
    int_db = create_integration_checklist_db(parent_page_id)
    print(f"   ✅ Integration Checklist (Connected network): {int_db['id']}")
    
    # Add Relations
    print()
    print("🔗 Adding database relations...")
    patch_database(mod_db["id"], {"Related Task": {"relation": {"database_id": dev_db["id"]}}})
    print("   ✅ Module Library → Development Tasks")
    
    patch_database(dec_db["id"], {"Related Task": {"relation": {"database_id": dev_db["id"]}}})
    print("   ✅ Technical Decisions → Development Tasks")
    
    # Create Pages with Cover Images
    print()
    print("📄 Creating pages with stunning space covers...")
    create_delivery_dashboard(parent_page_id)
    print("   ✅ 🏠 Delivery Dashboard (Blue nebula)")
    
    create_lms_page(parent_page_id)
    print("   ✅ 📚 Student Onboarding LMS (Colorful nebula)")
    
    create_docs_hub(parent_page_id)
    print("   ✅ 📖 Documentation Hub (Star field)")
    
    create_weekly_review(parent_page_id)
    print("   ✅ 📅 Weekly Review Template (Purple nebula)")
    
    # Summary
    print()
    print("=" * 80)
    print("🎉 BEAUTIFUL SPACE-THEMED WORKSPACE CREATED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print("✨ Design Features:")
    print("   • 🌌 High-quality space photography cover images on all pages")
    print("   • 🎨 Emoji icons for visual recognition")
    print("   • 🎯 Color-coded status options with emoji prefixes")
    print("   • 📦 Callout blocks for important information")
    print("   • ➖ Dividers for clear section separation")
    print("   • ✅ To-do lists for actionable items")
    print("   • 🌈 Colored headings for visual hierarchy")
    print()
    print("🌠 Space Images Used:")
    print("   • Development Tasks: Spiral galaxy (deep blue/purple)")
    print("   • Module Library: Milky Way star field")
    print("   • Technical Decisions: Earth from ISS")
    print("   • Integration Checklist: Network/constellation")
    print("   • Dashboard: Blue nebula")
    print("   • LMS Page: Colorful nebula (pink/blue/orange)")
    print("   • Docs Hub: Dense star field")
    print("   • Weekly Review: Purple nebula")
    print()
    print("📊 Database IDs:")
    print(f"   Development Tasks:     {dev_db['id']}")
    print(f"   Module Library:        {mod_db['id']}")
    print(f"   Technical Decisions:   {dec_db['id']}")
    print(f"   Integration Checklist: {int_db['id']}")
    print()
    print("🎨 Notion Best Practices Implemented:")
    print("   ✓ Cover images for visual appeal and quick page recognition")
    print("   ✓ Consistent emoji system across all databases and pages")
    print("   ✓ Callouts to highlight important instructions")
    print("   ✓ Color-coded elements by function (blue=active, green=done, red=blocked)")
    print("   ✓ Clear visual hierarchy with headings and dividers")
    print("   ✓ Descriptive placeholder text to guide users")
    print("   ✓ Linked database views for dynamic content")
    print()
    print("🚀 Next Steps:")
    print("   1. Open your Notion workspace and enjoy the beautiful visuals!")
    print("   2. Add linked database views as indicated in gray callout blocks")
    print("   3. Customize colors and layouts to match your team's preferences")
    print("   4. Duplicate the Weekly Review template for each week")
    print("   5. Start adding content - it will look amazing! 🌟")
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
            print("Usage: python scripts/create_notion_workspace_beautiful.py <PARENT_PAGE_ID>")
            print("\nOr set environment variable:")
            print("  $env:NOTION_PARENT_PAGE_ID='your-page-id-here'")
            sys.exit(1)
        parent_page_id = PARENT_PAGE_ID
    else:
        parent_page_id = sys.argv[1]
    
    setup_workspace(parent_page_id)
