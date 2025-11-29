# CADENCE Export → Neon PostgreSQL Migration Plan

**Date:** 2025-11-28
**Agent:** Alpha
**Goal:** Load all CADENCE export data into Neon database for automatic Notion population

---

## 📊 Current State Analysis

### What We Have:
1. **CADENCE Export:** 1,417 markdown files in `temp_cadence_extract/content/`
2. **Extracted Modules:** 68 JSON files in `modules/exports/` (Gamma's work)
3. **Neon Database:** Connected via DATABASE_URL in .env
4. **Existing Schema:** Teams, Faculty, Projects, Interfaces (from db_models.py)

### What We Need:
- **New tables** to store CADENCE-specific data
- **Import scripts** to process all 1,417 files
- **Notion sync** automation to populate from database

---

## 🗄️ Proposed Database Schema

### Table 1: `cadence_pages`
Stores all CADENCE Notion pages (the 1,417 markdown files)

```sql
CREATE TABLE cadence_pages (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    slug VARCHAR UNIQUE,
    page_type VARCHAR,  -- 'module', 'task', 'meeting', 'document', etc.
    content TEXT,  -- Full markdown content
    notion_page_id VARCHAR,
    parent_page_id VARCHAR,  -- For hierarchy
    tags TEXT[],  -- Array of tags
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    metadata JSONB  -- Flexible metadata storage
);
```

### Table 2: `cadence_modules` (Enhanced)
Stores the 68 training modules (extends Gamma's JSON structure)

```sql
CREATE TABLE cadence_modules (
    id VARCHAR PRIMARY KEY,
    module_id VARCHAR UNIQUE NOT NULL,
    title VARCHAR NOT NULL,
    slug VARCHAR UNIQUE,
    description TEXT,
    category VARCHAR,
    difficulty VARCHAR,
    estimated_minutes INTEGER,
    target_audience VARCHAR,
    status VARCHAR DEFAULT 'Draft',
    tags TEXT[],
    sections JSONB,  -- Array of section objects
    notion_page_id VARCHAR,
    github_file VARCHAR,
    github_sync VARCHAR,
    source_file VARCHAR,  -- Path in CADENCE export
    fetched_at TIMESTAMP,
    deployed_at TIMESTAMP,
    metadata JSONB
);
```

### Table 3: `cadence_tasks`
Stores tasks/todos from CADENCE export

```sql
CREATE TABLE cadence_tasks (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    status VARCHAR,  -- 'Not Started', 'In Progress', 'Complete', 'Blocked'
    priority VARCHAR,  -- 'P0', 'P1', 'P2', 'P3'
    assignee VARCHAR,
    due_date TIMESTAMP,
    subsystem VARCHAR,  -- 'Avionics', 'Power', etc.
    notion_page_id VARCHAR,
    parent_page_id VARCHAR,
    tags TEXT[],
    created_at TIMESTAMP,
    metadata JSONB
);
```

### Table 4: `cadence_meetings`
Stores meeting notes from CADENCE export

```sql
CREATE TABLE cadence_meetings (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    meeting_date TIMESTAMP,
    attendees TEXT[],
    content TEXT,  -- Meeting notes
    action_items JSONB,  -- Array of action items
    subsystem VARCHAR,
    notion_page_id VARCHAR,
    created_at TIMESTAMP,
    metadata JSONB
);
```

### Table 5: `cadence_documents`
Stores general documents, procedures, etc.

```sql
CREATE TABLE cadence_documents (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    document_type VARCHAR,  -- 'ConOps', 'Procedure', 'Reference', etc.
    content TEXT,
    subsystem VARCHAR,
    tags TEXT[],
    notion_page_id VARCHAR,
    parent_page_id VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    metadata JSONB
);
```

---

## 🔄 Migration Strategy

### Phase 1: Analyze CADENCE Export (30 min)
**Goal:** Understand the structure of all 1,417 files

**Script:** `analyze_cadence_export.py`
```python
# Scan all .md files
# Categorize by type (module, task, meeting, document)
# Extract metadata (title, dates, tags)
# Generate classification report
```

**Output:** `cadence_export_analysis.json`
```json
{
  "total_files": 1417,
  "by_type": {
    "modules": 68,
    "tasks": 243,
    "meetings": 156,
    "documents": 950
  },
  "classification": {
    "filename.md": {"type": "module", "title": "...", "tags": [...]},
    ...
  }
}
```

### Phase 2: Create Database Schema (15 min)
**Goal:** Add CADENCE tables to Neon

**Script:** `create_cadence_schema.py`
```python
# Connect to Neon via DATABASE_URL
# Create tables: cadence_pages, cadence_modules, cadence_tasks, cadence_meetings, cadence_documents
# Create indexes for performance
# Verify schema creation
```

### Phase 3: Import CADENCE Data (1-2 hours)
**Goal:** Load all 1,417 files into Neon

**Script:** `import_cadence_to_neon.py`
```python
# Read cadence_export_analysis.json
# For each file:
#   - Parse markdown
#   - Extract frontmatter/metadata
#   - Determine table (modules → cadence_modules, etc.)
#   - Insert into Neon
# Handle duplicates (update existing)
# Log import results
```

**Process:**
1. Import modules (68 files) → `cadence_modules`
2. Import tasks (243 files) → `cadence_tasks`
3. Import meetings (156 files) → `cadence_meetings`
4. Import documents (950 files) → `cadence_documents`
5. Create parent-child relationships
6. Import all to `cadence_pages` as master table

### Phase 4: Verify Data Integrity (20 min)
**Goal:** Ensure all data imported correctly

**Script:** `verify_cadence_import.py`
```python
# Query each table for counts
# Verify relationships (parent_page_id)
# Check for missing notion_page_ids
# Generate validation report
```

### Phase 5: Create Notion Sync Automation (45 min)
**Goal:** Automatically populate Notion from Neon

**Script:** `sync_neon_to_notion.py`
```python
# Query Neon for all records
# For each record:
#   - Check if exists in Notion (by notion_page_id)
#   - If not, create Notion page
#   - If yes, update Notion page
#   - Update database with notion_page_id
# Log sync results
```

---

## 📋 Implementation Tasks

### Task 1: Analyze CADENCE Export Structure
- [ ] Create `analyze_cadence_export.py`
- [ ] Scan all 1,417 markdown files
- [ ] Classify by type (module, task, meeting, document)
- [ ] Generate `cadence_export_analysis.json`
- [ ] Estimate: 30 minutes

### Task 2: Create Database Schema
- [ ] Create `create_cadence_schema.py`
- [ ] Define SQLAlchemy models for 5 tables
- [ ] Connect to Neon and create tables
- [ ] Create indexes for performance
- [ ] Estimate: 15 minutes

### Task 3: Import Modules (Gamma's 68 JSONs)
- [ ] Create `import_modules_to_neon.py`
- [ ] Read 68 JSON files from `modules/exports/`
- [ ] Insert into `cadence_modules` table
- [ ] Estimate: 15 minutes

### Task 4: Import All CADENCE Pages
- [ ] Create `import_cadence_to_neon.py`
- [ ] Process remaining 1,349 markdown files
- [ ] Insert into appropriate tables
- [ ] Estimate: 1-2 hours (bulk import)

### Task 5: Verify Import
- [ ] Create `verify_cadence_import.py`
- [ ] Query counts from each table
- [ ] Check data integrity
- [ ] Generate validation report
- [ ] Estimate: 20 minutes

### Task 6: Create Notion Sync
- [ ] Create `sync_neon_to_notion.py`
- [ ] Query Neon for all records
- [ ] Sync to Notion databases
- [ ] Update notion_page_ids in Neon
- [ ] Estimate: 45 minutes

---

## 🎯 Success Criteria

1. ✅ All 1,417 CADENCE files analyzed and categorized
2. ✅ 5 new tables created in Neon
3. ✅ All 68 modules imported to `cadence_modules`
4. ✅ All 1,417 pages imported to respective tables
5. ✅ Data integrity verified (counts match, relationships intact)
6. ✅ Notion sync automation created and tested
7. ✅ Notion databases automatically populated from Neon

---

## 🔗 Dependencies

- ✅ Neon database connected (DATABASE_URL in .env)
- ✅ Notion API token configured
- ✅ SQLAlchemy installed
- ✅ Gamma's 68 module JSONs exist
- ✅ CADENCE export extracted to `temp_cadence_extract/`

---

## 📝 Notes

- **Why Neon as source of truth?**
  - Easier to query and filter
  - Version control via SQL migrations
  - Supports complex relationships
  - Can rebuild Notion from database if needed

- **Why not just import directly to Notion?**
  - Notion API rate limits (3 req/sec)
  - Hard to query and maintain
  - No easy bulk operations
  - Neon → Notion is one-way sync

- **What about existing Notion data?**
  - Keep existing Module Library database
  - Sync will update existing entries
  - New entries will be created

---

**Total Estimated Time:** 3.5-4.5 hours
**Priority:** HIGH - Enables automatic Notion population
**Owner:** Agent Alpha
