# Notion Workspace Setup Guide

This guide will help you create your complete FRAMES Notion workspace with all databases and parent pages.

## What Gets Created

### 📊 Databases

1. **Development Tasks**
   - Task (title)
   - Status (Not Started, In Progress, In Review, Blocked, Done)
   - GitHub Issue URL
   - Due Date
   - Phase (1-6)
   - Application (LMS, Analytics, AI Core, Infra)
   - Priority (P0-P3)
   - Type (Feature, Bug, Chore)
   - Blocked? (checkbox)
   - Blocker (text)
   - Effort (number)

2. **Module Library**
   - Module Name (title)
   - Status (Intake, Drafting, In Review, Ready, Live)
   - Team Lead (people)
   - Owner (people)
   - University (select)
   - Cohort (select)
   - Content Source (AI-assisted, Form, Interview)
   - GitHub Branch/PR (url)
   - Last Updated (date)
   - Application (LMS)
   - Related Task (relation to Development Tasks)

3. **Technical Decisions**
   - Decision (title)
   - Status (Proposed, Approved, Implemented, Reversed)
   - Impact (High, Medium, Low)
   - Context (text)
   - Rationale (text)
   - Reversible? (checkbox)
   - Related Task (relation to Development Tasks)

4. **Integration Checklist**
   - Integration (title)
   - Status (Planned, Setup, Active, Done, Deprecated)
   - Priority (P0-P3)
   - Owner (people)
   - Last Health Check (date)
   - Next Action (text)
   - Cost (number, dollar format)

### 📄 Parent Pages

1. **Delivery Dashboard**
   - Instructions for creating linked views:
     - Sprint Board (group by Status, sort by Priority)
     - This Week (filter by Due within 7 days)
     - Blocked items
     - By Phase
     - Active Integrations

2. **Student Onboarding LMS**
   - Module Library views:
     - Intake Queue
     - Review Queue
     - Live Catalog
     - By Team Lead
   - Instructions for creating a Notion Form

3. **Documentation Hub**
   - Callout explaining GitHub sync setup

4. **Weekly Review Template**
   - Template with instructions for:
     - Completed tasks
     - In Progress
     - Blockers
     - Recent decisions
     - Next week priorities

## Setup Steps

### 1. Get Your Parent Page ID

1. Create a new page in Notion (this will be your FRAMES workspace hub)
2. Give it a name like "FRAMES Project"
3. Share the page with your Notion integration:
   - Click "Share" in the top right
   - Click "Invite"
   - Find and select your integration
   - Click "Invite"
4. Copy the page ID from the URL:
   - The URL looks like: `https://notion.so/My-Page-2b76b8ea578a8040b328c8527dedea93`
   - The page ID is: `2b76b8ea578a8040b328c8527dedea93` (the last part)
   - Or with dashes: `2b76b8ea-578a-8040-b328-c8527dedea93`

### 2. Set Environment Variables

Make sure you have these set:

```powershell
# Your Notion integration token
$env:NOTION_TOKEN="secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# The parent page ID you just copied
$env:NOTION_PARENT_PAGE_ID="2b76b8ea578a8040b328c8527dedea93"
```

You can also add these to your `.env` file:

```
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_PARENT_PAGE_ID=2b76b8ea578a8040b328c8527dedea93
```

### 3. Run the Setup Script

#### Option A: Using environment variable

```powershell
python scripts\create_notion_workspace.py
```

#### Option B: Passing page ID as argument

```powershell
python scripts\create_notion_workspace.py 2b76b8ea578a8040b328c8527dedea93
```

### 4. What Happens Next

The script will:
1. ✅ Create all 4 databases
2. ✅ Set up relations between databases
3. ✅ Create all 4 parent pages with instructions
4. ✅ Display all created database IDs

You'll see output like:

```
🚀 Creating FRAMES Notion Workspace...

📊 Creating Development Tasks database...
   ✅ Development Tasks DB: 1234abcd...

📚 Creating Module Library database...
   ✅ Module Library DB: 5678efgh...

🎯 Creating Technical Decisions database...
   ✅ Technical Decisions DB: 90ijklmn...

🔗 Creating Integration Checklist database...
   ✅ Integration Checklist DB: opqrstuv...

🔗 Patching relations...
   ✅ Module Library → Development Tasks
   ✅ Technical Decisions → Development Tasks

📄 Creating parent pages...
   ✅ Delivery Dashboard
   ✅ Student Onboarding LMS
   ✅ Documentation Hub
   ✅ Weekly Review Template

================================================================
✨ All done! FRAMES Notion Workspace created successfully.
================================================================
```

### 5. Manual Setup in Notion

After the script completes, you need to manually add linked database views:

#### In Delivery Dashboard:
1. Type `/linked` and select "Create linked database"
2. Choose "Development Tasks"
3. Create views as described in the page

#### In Student Onboarding LMS:
1. Type `/linked` and select "Create linked database"
2. Choose "Module Library"
3. Create views and filters as described
4. Create a Notion Form (type `/form`) pointing to Module Library

#### In Documentation Hub:
1. This will eventually sync with your GitHub `/docs` folder
2. For now, you can manually add documentation pages

#### In Weekly Review Template:
1. Duplicate this template each week
2. Add linked views as described in the page

## Troubleshooting

### Error: "NOTION_TOKEN environment variable not set"
- Make sure you've set `$env:NOTION_TOKEN` or added it to `.env`
- Check that your `.env` file is in the repo root

### Error: "NOTION_PARENT_PAGE_ID environment variable not set"
- Either set `$env:NOTION_PARENT_PAGE_ID` or pass the page ID as an argument
- Make sure you copied the full page ID from the URL

### Error: "Could not find page"
- Make sure you've shared the parent page with your integration
- Verify the page ID is correct (check the URL)

### Error: "Unauthorized"
- Check that your `NOTION_TOKEN` is valid
- Make sure it starts with `secret_`
- Verify the integration has the right permissions

## Next Steps

Once your workspace is set up:

1. **Add your first tasks** to Development Tasks
2. **Create module entries** in Module Library
3. **Document decisions** in Technical Decisions
4. **Track integrations** in Integration Checklist
5. **Set up linked views** in your dashboard pages
6. **Create a weekly review** from the template

## Customization

You can customize the databases by:
- Adding more select/status options
- Adding custom properties
- Creating additional views
- Setting up automations
- Creating templates

Enjoy your new FRAMES Notion workspace! 🎉
