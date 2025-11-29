"""
Create Module Creation Workflow page in Notion
Converts the markdown workflow document to a properly formatted Notion page
"""
import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv('NOTION_API_KEY'))


def create_workflow_page(parent_page_id):
    """Create comprehensive Module Creation Workflow page"""

    # Part 1: Create the main page
    try:
        page = notion.pages.create(
            parent={"type": "page_id", "page_id": parent_page_id},
            icon={"type": "emoji", "emoji": "🔄"},
            properties={
                "title": [{"text": {"content": "Module Creation Workflow"}}]
            }
        )
        page_id = page['id']
        print(f"[OK] Created page: Module Creation Workflow")
    except Exception as e:
        print(f"[ERROR] Failed to create page: {e}")
        return None

    # Part 2: Add content blocks (in batches of 100)
    blocks_batch_1 = [
        # Header and Metadata
        {
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "Version 1.0 | Last Updated: November 26, 2025 | Status: Active - Phase 1 Implementation"}}],
                "icon": {"emoji": "📋"}
            }
        },
        {
            "type": "divider",
            "divider": {}
        },

        # Table of Contents
        {
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "Table of Contents"}}]
            }
        },
        {
            "type": "table_of_contents",
            "table_of_contents": {}
        },
        {
            "type": "divider",
            "divider": {}
        },

        # Overview
        {
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "Overview"}}]
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "This workflow guides instructors and developers through creating effective training modules for the FRAMES Student Onboarding LMS. The system supports 5 module types with varying levels of interactivity and complexity."}
                }]
            }
        },

        # Current System Status
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Current System Status"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Database: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "6 LMS tables operational (Neon PostgreSQL)"}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Frontend: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "React viewer with Vision UI Dashboard"}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Backend: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "Flask REST API at http://localhost:5001"}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Supported Types: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "Text (Phase 0), Interactive/Sandbox/Game/Buddy (Phase 1+)"}}
                ]
            }
        },

        # Who Should Use This Workflow
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "Who Should Use This Workflow?"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Team Leads: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "Creating onboarding content for incoming students"}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Faculty: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "Designing domain-specific training modules"}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Developers: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "Implementing new module types"}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Content Designers: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "Building interactive learning experiences"}}
                ]
            }
        },

        {
            "type": "divider",
            "divider": {}
        },

        # The 7-Step Workflow
        {
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "The 7-Step Workflow"}}]
            }
        },
        {
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "Follow these steps sequentially to create high-quality training modules"}}],
                "icon": {"emoji": "🎯"}
            }
        },

        # STEP 1: CONCEPT & PLANNING
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "STEP 1: CONCEPT & PLANNING"}}],
                "color": "blue"
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Goal: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "Define what you're building and why"}}
                ]
            }
        },
        {
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "1.1 Define Learning Objective"}}]
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Answer these questions:"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "What should students KNOW after completing this module?"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "What should students BE ABLE TO DO?"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "How does this fit into the larger onboarding journey?"}}]
            }
        },
        {
            "type": "callout",
            "callout": {
                "rich_text": [{
                    "type": "text",
                    "text": {"content": "Example: After completing 'Lab Safety 101', students will be able to identify 5 key safety protocols and locate emergency equipment in the lab."}
                }],
                "icon": {"emoji": "💡"}
            }
        },

        # 1.2 Choose Module Type
        {
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "1.2 Choose Module Type"}}]
            }
        },
        {
            "type": "table",
            "table": {
                "table_width": 3,
                "has_column_header": True,
                "has_row_header": False,
                "children": [
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Type"}}],
                                [{"type": "text", "text": {"content": "Best For"}}],
                                [{"type": "text", "text": {"content": "Phase"}}]
                            ]
                        }
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Text"}}],
                                [{"type": "text", "text": {"content": "Reading comprehension, policies, background"}}],
                                [{"type": "text", "text": {"content": "Phase 0 ✅"}}]
                            ]
                        }
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Interactive"}}],
                                [{"type": "text", "text": {"content": "Spatial learning, exploration, discovery"}}],
                                [{"type": "text", "text": {"content": "Phase 2 🎯"}}]
                            ]
                        }
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Sandbox"}}],
                                [{"type": "text", "text": {"content": "Coding practice, debugging, hands-on"}}],
                                [{"type": "text", "text": {"content": "Phase 3 💻"}}]
                            ]
                        }
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Game"}}],
                                [{"type": "text", "text": {"content": "Speed drills, memorization, patterns"}}],
                                [{"type": "text", "text": {"content": "Phase 4 🎮"}}]
                            ]
                        }
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Buddy"}}],
                                [{"type": "text", "text": {"content": "Guided struggle, problem-solving"}}],
                                [{"type": "text", "text": {"content": "Phase 5 🤖"}}]
                            ]
                        }
                    }
                ]
            }
        },

        # Decision Criteria
        {
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "Decision Criteria"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Passive consumption? → ", "annotations": {"italic": True}}},
                    {"type": "text", "text": {"content": "Text", "annotations": {"bold": True}}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Spatial/visual learning? → ", "annotations": {"italic": True}}},
                    {"type": "text", "text": {"content": "Interactive", "annotations": {"bold": True}}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Coding practice? → ", "annotations": {"italic": True}}},
                    {"type": "text", "text": {"content": "Sandbox", "annotations": {"bold": True}}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Speed/accuracy drills? → ", "annotations": {"italic": True}}},
                    {"type": "text", "text": {"content": "Game", "annotations": {"bold": True}}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Complex problem-solving? → ", "annotations": {"italic": True}}},
                    {"type": "text", "text": {"content": "Buddy", "annotations": {"bold": True}}}
                ]
            }
        },

        # Action Items for Step 1
        {
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "Action Items"}}]
            }
        },
        {
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Complete learning objective statement"}}],
                "checked": False
            }
        },
        {
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Choose module type from table above"}}],
                "checked": False
            }
        },
        {
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Estimate completion time"}}],
                "checked": False
            }
        },
        {
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "List prerequisites"}}],
                "checked": False
            }
        },
        {
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": "Create Notion planning page"}}],
                "checked": False
            }
        },

        {
            "type": "divider",
            "divider": {}
        },

        # STEP 2: DESIGN & CONTENT
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "STEP 2: DESIGN & CONTENT"}}],
                "color": "purple"
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Goal: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "Create the instructional content and assets"}}
                ]
            }
        },
        {
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "2.1 Write Instructional Content"}}]
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "For Text Modules:", "annotations": {"bold": True}}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Break content into 3-7 logical sections"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Use clear headings and subheadings"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Keep paragraphs short (2-4 sentences)"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Add summaries at the end"}}]
            }
        },
    ]

    # Add first batch of blocks
    try:
        notion.blocks.children.append(
            block_id=page_id,
            children=blocks_batch_1
        )
        print(f"[OK] Added content batch 1")
    except Exception as e:
        print(f"[ERROR] Failed to add content batch 1: {e}")
        return None

    # Part 3: Add remaining workflow steps (batch 2)
    blocks_batch_2 = [
        # Continue with remaining steps overview
        {
            "type": "divider",
            "divider": {}
        },
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "STEP 3: DATABASE ENTRY"}}],
                "color": "green"
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Goal: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "Add module to database with proper structure"}}
                ]
            }
        },
        {
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "Use Python scripts to create Module and ModuleSection records in the database"}}],
                "icon": {"emoji": "🗄️"}
            }
        },

        {
            "type": "divider",
            "divider": {}
        },
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "STEP 4: COMPONENT DEVELOPMENT"}}],
                "color": "orange"
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Goal: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "Build the React viewer component (if new module type)"}}
                ]
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Note: ", "annotations": {"bold": True, "italic": True}}},
                    {"type": "text", "text": {"content": "Skip this step if using an existing module type (e.g., text)"}}
                ]
            }
        },

        {
            "type": "divider",
            "divider": {}
        },
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "STEP 5: TESTING"}}],
                "color": "yellow"
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Goal: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "Verify module works correctly on all devices"}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Desktop testing (Chrome DevTools)"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Tablet testing (iPad/Android)"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Cross-browser testing"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Analytics verification"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Student pilot test"}}]
            }
        },

        {
            "type": "divider",
            "divider": {}
        },
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "STEP 6: DEPLOYMENT"}}],
                "color": "pink"
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Goal: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "Make module available to students"}}
                ]
            }
        },
        {
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Update module status to 'published'"}}]
            }
        },
        {
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Assign to target students"}}]
            }
        },
        {
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Monitor completion rates"}}]
            }
        },
        {
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Gather feedback"}}]
            }
        },

        {
            "type": "divider",
            "divider": {}
        },
        {
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "STEP 7: ITERATION"}}],
                "color": "red"
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Goal: ", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": "Improve module based on data and feedback"}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Review analytics (completion rates, time spent, drop-offs)"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Adjust difficulty based on struggle signals"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Update content based on feedback"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Increment revision number"}}]
            }
        },

        {
            "type": "divider",
            "divider": {}
        },

        # Key Metrics
        {
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "Key Metrics"}}]
            }
        },
        {
            "type": "table",
            "table": {
                "table_width": 3,
                "has_column_header": True,
                "has_row_header": False,
                "children": [
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Metric"}}],
                                [{"type": "text", "text": {"content": "Good Range"}}],
                                [{"type": "text", "text": {"content": "Red Flag"}}]
                            ]
                        }
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Completion rate"}}],
                                [{"type": "text", "text": {"content": ">80%"}}],
                                [{"type": "text", "text": {"content": "<60%"}}]
                            ]
                        }
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Average time"}}],
                                [{"type": "text", "text": {"content": "Within 20% of estimate"}}],
                                [{"type": "text", "text": {"content": "2x estimate"}}]
                            ]
                        }
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Drop-off rate"}}],
                                [{"type": "text", "text": {"content": "<10%"}}],
                                [{"type": "text", "text": {"content": ">25%"}}]
                            ]
                        }
                    },
                    {
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Hint usage"}}],
                                [{"type": "text", "text": {"content": "2-4 per student"}}],
                                [{"type": "text", "text": {"content": ">6 or 0"}}]
                            ]
                        }
                    }
                ]
            }
        },

        {
            "type": "divider",
            "divider": {}
        },

        # Resources
        {
            "type": "heading_1",
            "heading_1": {
                "rich_text": [{"type": "text", "text": {"content": "Resources"}}]
            }
        },
        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "Documentation:", "annotations": {"bold": True}}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Database Schema (03-DATABASE-SCHEMA.md)"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Development Roadmap (04-DEVELOPMENT-ROADMAP.md)"}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": "Module Type Specifications (02-MODULE-TYPE-SPECIFICATIONS.md)"}}]
            }
        },

        {
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": "External Tools:", "annotations": {"bold": True}}}]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Monaco Editor", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": " - Code editor for sandbox modules"}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Chakra UI", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": " - React component library"}}
                ]
            }
        },
        {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Pyodide", "annotations": {"bold": True}}},
                    {"type": "text", "text": {"content": " - Python in browser"}}
                ]
            }
        },

        {
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": "For detailed technical documentation, see MODULE-CREATION-WORKFLOW.md in the docs/lms folder"}}],
                "icon": {"emoji": "📚"}
            }
        }
    ]

    # Add second batch
    try:
        notion.blocks.children.append(
            block_id=page_id,
            children=blocks_batch_2
        )
        print(f"[OK] Added content batch 2")
    except Exception as e:
        print(f"[ERROR] Failed to add content batch 2: {e}")
        return None

    print(f"[OK] Module Creation Workflow page created successfully!")
    print(f"[OK] Page ID: {page_id}")
    return page_id


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python scripts/create_workflow_notion_page.py <PARENT_PAGE_ID>")
        print("\nSteps:")
        print("1. Create a new page in Notion (or use existing FRAMES workspace)")
        print("2. Share it with the FRAMES integration")
        print("3. Copy the page ID from the URL")
        print("4. Run this script with the page ID")
        print("\nExample:")
        print("  python scripts/create_workflow_notion_page.py 123abc456def")
        sys.exit(1)

    parent_page_id = sys.argv[1]
    result = create_workflow_page(parent_page_id)

    if result:
        print(f"\n✅ Success! Your Module Creation Workflow page is ready in Notion")
        print(f"📄 Page ID: {result}")
    else:
        print(f"\n❌ Failed to create Notion page. Check the error messages above.")
