# Notion API Setup Guide

## Quick Start (5 Minutes)

I've created an automated script to import all 68 CADENCE modules directly into your Notion workspace!

**File:** `scripts/import_to_notion.py`

---

## Step 1: Get Your Notion API Key (2 minutes)

### Create Integration:
1. Go to: **https://www.notion.so/my-integrations**
2. Click **"+ New integration"**
3. Name it: **"FRAMES Module Importer"**
4. Select your workspace (where your template is)
5. Click **"Submit"**

### Copy API Key:
6. You'll see **"Internal Integration Token"**
7. Click **"Show"** then **"Copy"**
8. Save it somewhere (you'll need it in Step 3)

**Example:** `secret_ABC123xyz...` (starts with `secret_`)

---

## Step 2: Get Your Database ID (1 minute)

### Find Your Database:
1. Open your Notion template workspace
2. Find or create the **"Module Library"** database
3. Click the **"..."** menu (top right)
4. Select **"Copy link"**

### Extract Database ID:
The link looks like:
```
https://www.notion.so/workspace-name/a1b2c3d4e5f6...?v=xyz
                                      ^^^^^^^^^^^^
                                      This is your database ID
```

**Copy the part between the last `/` and the `?`**

**Example:** If link is:
```
https://www.notion.so/myworkspace/a1b2c3d4e5f67890?v=123
```
Your database ID is: `a1b2c3d4e5f67890`

---

## Step 3: Give Integration Access to Database (30 seconds)

**IMPORTANT:** Your integration needs permission to access the database!

1. Open your **Module Library** database in Notion
2. Click the **"..."** menu (top right)
3. Scroll down to **"Connections"**
4. Click **"+ Add connection"**
5. Search for: **"FRAMES Module Importer"** (the integration you created)
6. Click to add it

**Now your integration can access the database!**

---

## Step 4: Configure the Script (1 minute)

### Create `.env` file:

In your project root (`c:\Users\LizO5\FRAMES Python`), create a file named `.env`:

```bash
# .env file
NOTION_API_KEY=secret_YOUR_INTEGRATION_TOKEN_HERE
NOTION_DATABASE_ID=YOUR_DATABASE_ID_HERE
```

**Replace with your actual values from Steps 1 and 2!**

### Example `.env` file:
```bash
NOTION_API_KEY=secret_ABC123XYZ789...
NOTION_DATABASE_ID=a1b2c3d4e5f67890
```

---

## Step 5: Install Dependencies (30 seconds)

```bash
pip install notion-client python-dotenv
```

---

## Step 6: Test with Dry Run (30 seconds)

Preview what will be imported without actually creating pages:

```bash
python scripts/import_to_notion.py --dry-run
```

**Expected output:**
```
Configuration valid
  CSV file: data/projects/CADENCE/notion_modules_categorized.csv
  Database ID: a1b2c3d4...

Reading CSV file...
  Found 68 modules

DRY RUN MODE - No pages will be created

Modules to import:
  1. New Recruits (Getting Started)
  2. GitHub Guide (Getting Started)
  3. GitHub Practice (Getting Started)
  ...
  68. Read UNP User's Guide Section 2 (Systems Engineering)

Total: 68 modules
```

---

## Step 7: Import! (1-2 minutes)

Run the actual import:

```bash
python scripts/import_to_notion.py
```

**Expected output:**
```
IMPORTING MODULES TO NOTION

Configuration valid
  CSV file: data/projects/CADENCE/notion_modules_categorized.csv
  Database ID: a1b2c3d4...

Reading CSV file...
  Found 68 modules

Importing 68 modules...
  [1/68] New Recruits... OK (ID: abc12345...)
  [2/68] GitHub Guide... OK (ID: def67890...)
  [3/68] GitHub Practice... OK (ID: ghi11213...)
  ...
  [68/68] Read UNP User's Guide Section 2... OK (ID: xyz99988...)

IMPORT COMPLETE
  Success: 68
  Failed:  0
  Total:   68

Open your Notion database to see the imported modules!
```

---

## What Gets Imported

Each module page will have these properties automatically filled:

- **Title:** Module name
- **Category:** Getting Started / Software Development / Hardware & Subsystems / etc.
- **Description:** Brief description
- **Target Audience:** All / Undergraduate / Graduate
- **Discipline:** Software / Electrical / Aerospace / Systems / All
- **Estimated Minutes:** Time to complete
- **Status:** Published / Draft
- **Difficulty:** Beginner / Intermediate / Advanced
- **Source Type:** Markdown / PDF
- **Source File:** Filename reference
- **Tags:** Searchable keywords (github, f-prime, nasa, etc.)
- **Prerequisites:** Learning path dependencies

---

## Troubleshooting

### Error: "NOTION_API_KEY not found"
- Make sure `.env` file is in the project root
- Check that variable name is exactly `NOTION_API_KEY=`
- No spaces around the `=` sign
- API key should start with `secret_`

### Error: "Could not find database"
- Make sure you added the integration to the database (Step 3!)
- Check database ID is correct (copy link again)
- Database ID should be 32 characters (alphanumeric)

### Error: "Unauthorized"
- API key is incorrect - copy it again from notion.so/my-integrations
- Make sure you're using the "Internal Integration Token", not a workspace URL

### Error: "Invalid property"
- Your database might be missing some properties
- The script will create pages with whatever properties exist
- You can add missing properties to your database manually

### Import succeeded but pages are blank
- This is normal! The script creates the database rows with metadata
- You'll need to populate the page content separately (from markdown files)
- For now, the database has all the organizational data

---

## Next Steps After Import

### 1. Create Category Views (15 minutes)
For each category, create filtered views:

1. Click **"+ New view"** in database
2. Choose **Gallery** or **Table**
3. Name it (e.g., "Getting Started")
4. Add filter: **Category = "Getting Started"**
5. Repeat for all 6 categories

### 2. Link Image Buttons (10 minutes)
1. Open each category view
2. Click **"..."** → **"Copy link to view"**
3. Go to template homepage
4. Click each image button → Add the view link

### 3. Populate Content (Ongoing)
For key modules, copy content from markdown files:

```bash
# Markdown files are in:
data/projects/CADENCE/markdown/

# Example:
# Open "GitHub Guide" module page in Notion
# Copy content from: data/projects/CADENCE/markdown/GitHub Guide.md
# Paste and format in Notion
```

---

## Summary Checklist

- [ ] Created Notion integration (Step 1)
- [ ] Got API key and saved it
- [ ] Got database ID from Module Library
- [ ] Added integration to database (Step 3 - IMPORTANT!)
- [ ] Created `.env` file with credentials
- [ ] Installed dependencies (`pip install`)
- [ ] Ran dry run successfully
- [ ] Ran actual import
- [ ] Verified 68 modules in Notion database
- [ ] Created category views
- [ ] Linked image buttons to views

---

## You're Ready! 🚀

**Total time:** ~10 minutes setup + 2 minutes import = **12 minutes**

After import, you'll have:
- ✅ 68 organized modules in Notion
- ✅ All metadata and categorization complete
- ✅ Searchable tags and prerequisites
- ✅ Ready for category views and navigation setup

Much faster than manual CSV import! 🎉
