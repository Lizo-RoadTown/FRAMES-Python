# LMS Module Export Pipeline

## Overview

Complete pipeline for exporting learning modules from Notion and deploying them to PostgreSQL.

```
Notion Module Library
        ↓
export_modules_from_notion.py  (Fetch & Export to JSON)
        ↓
data/modules/*.json  (Validated JSON files)
        ↓
deploy_modules_to_db.py  (Import to PostgreSQL)
        ↓
PostgreSQL Database
        ↓
Flask API (lms_routes.py)
        ↓
React Frontend (NotionPage.jsx)
```

---

## Files Created

### 1. `schemas/module_schema.json`
JSON Schema for validating module data structure.

**Validates:**
- Required fields (module_id, title, sections)
- Data types and formats
- Enum values (category, status, target_audience)
- Notion page ID format (32 hex chars)

### 2. `scripts/export_modules_from_notion.py`
Exports modules from Notion Module Library to JSON files.

**Features:**
- Fetches from Notion database via API
- Extracts all properties (title, description, category, tags, etc.)
- Fetches full page content including blocks
- Generates recordMap for react-notion-x rendering
- Validates against JSON schema
- Exports one JSON file per module

**Usage:**
```bash
# Export all modules
python scripts/export_modules_from_notion.py

# Export specific module
python scripts/export_modules_from_notion.py --module-id <notion_page_id>
```

**Environment variables required:**
- `NOTION_API_KEY` - Your Notion integration API key
- `NOTION_MODULE_DB_ID` - Notion Module Library database ID

**Output:**
- JSON files in `data/modules/`
- Named by module_id: `intro-to-research.json`

### 3. `scripts/deploy_modules_to_db.py`
Deploys module JSON files to PostgreSQL database.

**Features:**
- Reads and validates JSON files
- Inserts new modules or updates existing ones
- Creates all module sections
- Handles Notion recordMap storage
- Dry-run mode for testing

**Usage:**
```bash
# Deploy all modules
python scripts/deploy_modules_to_db.py

# Deploy specific module
python scripts/deploy_modules_to_db.py --module-file data/modules/intro-to-research.json

# Test without writing to DB
python scripts/deploy_modules_to_db.py --dry-run
```

**Environment variables required:**
- `DATABASE_URL` - PostgreSQL connection string (Neon)

### 4. `data/modules/` Directory
Contains exported module JSON files.

**Structure:**
```
data/modules/
├── intro-to-research.json
├── collaboration-basics.json
├── safety-protocols.json
└── ...
```

---

## Complete Workflow

### Step 1: Setup Notion Module Library

Create a Notion database with these properties:
- **Title** (title) - Module name
- **Description** (rich text) - Module description
- **Category** (select) - Module category
- **Status** (select) - draft/published/archived
- **Target Audience** (select) - undergraduate/graduate/faculty/all
- **Estimated Time (min)** (number) - Duration in minutes
- **Tags** (multi-select) - Searchable tags
- **Prerequisites** (relation) - Links to other modules
- **Related Modules** (relation) - Related content
- **Team Lead** (person) - Module creator
- **University** (select) - University-specific modules

### Step 2: Get Database ID

```bash
python scripts/get_notion_db_ids.py
```

Copy the Module Library database ID and add to `.env`:
```
NOTION_MODULE_DB_ID=abc123...
```

### Step 3: Create Modules in Notion

Team leads create rich module content in Notion:
- Full-page Notion documents
- Images, videos, callouts, code blocks
- Structured with headings and sections
- All Notion block types supported

### Step 4: Export to JSON

```bash
python scripts/export_modules_from_notion.py
```

**Output:**
```
Found 5 modules in database
Processing 1/5...
  Fetching content for: Introduction to Research
  ✓ Exported to: data/modules/introduction-to-research.json
...
Export complete!
  Exported: 5
  Failed: 0
```

### Step 5: Deploy to Database

```bash
# Test first
python scripts/deploy_modules_to_db.py --dry-run

# Deploy for real
python scripts/deploy_modules_to_db.py
```

**Output:**
```
Found 5 module files
[1/5] Processing: introduction-to-research.json
  → Creating new module...
  → Adding 1 sections...
  ✓ Deployed: Introduction to Research (ID: 1)
...
Deployment complete!
  Deployed: 5
  Failed: 0
```

### Step 6: Verify in Flask API

```bash
curl http://localhost:5000/api/lms/modules
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "modules": [...]
}
```

### Step 7: View in React Frontend

React components automatically fetch and render:
```javascript
// ModulePage.jsx fetches from API
const response = await fetch(`/api/lms/modules/${moduleId}`);
const data = await response.json();

// NotionPage.jsx renders with recordMap
<NotionPage recordMap={section.record_map} darkMode={true} />
```

---

## Data Flow

### Module Data Structure

```json
{
  "module_id": "intro-to-research",
  "title": "Introduction to Research",
  "description": "Learn research fundamentals",
  "category": "fundamentals",
  "estimated_minutes": 45,
  "status": "published",
  "target_audience": "undergraduate",
  "notion_page_id": "abc123...",
  "content_source": "notion",
  "tags": ["research", "methodology"],
  "prerequisites": ["module-id-1"],
  "related_modules": ["module-id-2"],
  "sections": [
    {
      "section_number": 1,
      "section_type": "notion_page",
      "title": "Introduction to Research",
      "content": "Notion page content",
      "record_map": {
        "block": {...},
        "collection": {...}
      }
    }
  ]
}
```

### Database Schema

**modules table:**
- id (PK)
- module_id (unique)
- title, description, category
- estimated_minutes, target_audience, status
- notion_page_id, content_source
- tags, prerequisites, related_modules (JSON)
- created_by_id, university_id
- created_at, updated_at, published_at

**module_sections table:**
- id (PK)
- module_id (FK)
- section_number
- section_type
- title, content
- media_url, duration_seconds
- created_at

---

## Troubleshooting

### Export Issues

**"NOTION_MODULE_DB_ID not found"**
- Run `python scripts/get_notion_db_ids.py`
- Add database ID to `.env`

**"Validation failed"**
- Check Notion database properties match schema
- Required: Title, at least one section
- Status must be: draft/published/archived

**"Error fetching page content"**
- Verify Notion integration has access to pages
- Check API key permissions

### Deploy Issues

**"DATABASE_URL not found"**
- Add Neon connection string to `.env`

**"Validation error"**
- JSON files must match schema
- Re-export from Notion with `export_modules_from_notion.py`

**"Module already exists"**
- Script will update existing module
- Old sections are deleted and recreated

---

## Automation

### GitHub Actions (Optional)

Auto-sync when Notion content changes:

```yaml
# .github/workflows/sync-modules.yml
name: Sync Modules from Notion

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:  # Manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install notion-client jsonschema python-dotenv
      - name: Export from Notion
        env:
          NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
          NOTION_MODULE_DB_ID: ${{ secrets.NOTION_MODULE_DB_ID }}
        run: python scripts/export_modules_from_notion.py
      - name: Deploy to Database
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: python scripts/deploy_modules_to_db.py
```

---

## Next Steps

1. **Create test modules** in Notion
2. **Run export pipeline** to test
3. **Verify in Flask API** with curl
4. **Test React rendering** in browser
5. **Set up automation** (optional)

---

## Support

- **Export script:** `scripts/export_modules_from_notion.py --help`
- **Deploy script:** `scripts/deploy_modules_to_db.py --help`
- **Schema:** `schemas/module_schema.json`
- **API docs:** `backend/LMS_API_README.md`
