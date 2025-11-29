# CADENCE Hub Implementation Plan

**Date:** 2025-11-27
**Purpose:** Transform Proto-type page into CADENCE project management hub with integrated onboarding

---

## 🎯 Architecture Summary

### The Unified Workspace Concept

**CADENCE team members see ONE workspace that serves both purposes:**
1. **Their normal project hub** - Mission control, subsystems, active work
2. **New hire onboarding** - Integrated "New Hire HQ" column on the same page

**No separation.** New hires navigate the same page as veterans, just with their own dedicated column.

---

## 📐 Page Layout (Proto-type → CADENCE Hub)

### Current Proto-type Structure
- Page ID: `2b86b8ea-578a-80cb-8f25-f080444ec266`
- Has: Multiple column layouts, Navigation DB, empty callouts
- Status: Template skeleton ready for population

### Target CADENCE Hub Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                          HERO SECTION                            │
│   CADENCE Mission Statement + Current Focus + Launch KPIs       │
│   Cover: Space/mission imagery                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     NAVIGATION DATABASE                          │
│   Universal menu with Subsystem, Surface, Priority properties   │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┬──────────────────┬──────────────────────────┐
│   COLUMN A:      │   COLUMN B:      │   COLUMN C:              │
│ MISSION CONTROL  │  ACTIVE WORK     │   NEW HIRE HQ            │
├──────────────────┼──────────────────┼──────────────────────────┤
│                  │                  │                          │
│ • Mission Brief  │ • Dev Tasks      │ 🚀 LAUNCH APP BUTTON     │
│ • Launch Checklist│  (Status≠Done)  │                          │
│ • Key Contacts   │ • Integration    │ ☑️ Week 1 Jumpstart      │
│ • Subsystem Links│   Checklist      │   □ Join Discord         │
│   - Avionics     │   (Blocked)      │   □ Read Mission Brief   │
│   - Power        │ • Tech Decisions │   □ Complete Module 1    │
│   - Mission Ops  │   (In Review)    │   □ Schedule Mentor Call │
│   - Structures   │                  │                          │
│                  │                  │ 📚 MODULE LIBRARY        │
│                  │                  │   (Embedded DB view)     │
│                  │                  │   Filter: Published      │
│                  │                  │                          │
│                  │                  │ 📊 ONBOARDING PROGRESS   │
│                  │                  │   Name | Cohort | % Done │
│                  │                  │   (Leaderboard style)    │
│                  │                  │                          │
│                  │                  │ 💬 NEED HELP?            │
│                  │                  │   Contact: Team Lead     │
└──────────────────┴──────────────────┴──────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│               ADDITIONAL PERSONA-SPECIFIC SECTIONS               │
│   • Leadership Snapshots (KPIs, risks, Beta status)             │
│   • Subsystem Boards (filtered Dev Tasks by discipline)         │
│   • Docs & Decisions (Technical Decisions + Documentation)      │
│   • Automation Surfaces (Gamma analytics, Beta deployment log)  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Data Architecture

### Notion Databases

**1. Module Library** (ID: `eac1ce58-6169-4dc3-a821-29858ae59e76`)
- Type: Classic database (NOT data source)
- Properties: Name, Category, Description, Target Audience, Discipline, Estimated Minutes, Status, Difficulty, Source Type, Source File, Tags, Prerequisites
- Content Source: Import from `data/projects/CADENCE/notion_modules_categorized.csv` (68 modules)
- Views:
  - "Published" (Status = Published)
  - "New Hire" (Target Audience = Incoming Students)
  - "By Category" (Grouped by Category)

**2. Onboarding Progress** (NEW - to create)
- Type: Classic database
- Properties:
  - Name (Person or text)
  - Cohort (Select: Fall 2025, Spring 2026, etc.)
  - Modules Completed (Number)
  - % Complete (Formula: Modules Completed / Total Modules * 100)
  - Last Updated (Date)
  - Current Module (Text)
- Embedded View: Table sorted by "Modules Completed" DESC (leaderboard)

**3. Development Tasks** (ID: `662cbb0c-1cca-4c12-9991-c566f220eb0c`)
- Already exists
- Embedded views in Column B filtered by Status

**4. Navigation** (ID: `2b86b8ea-578a-81f6-8104-f5eb8575ee54`)
- Already exists in Proto-type
- Add properties:
  - Subsystem (Select: Avionics, Power, Mission Ops, Structures, etc.)
  - Surface (Select: Page, Database, Workflow)
  - Priority (Select: P0, P1, P2, P3)

### PostgreSQL Tables

**modules** (for runtime)
```sql
CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    module_id UUID UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    difficulty VARCHAR(50),
    estimated_minutes INTEGER,
    target_audience VARCHAR(100),
    status VARCHAR(50),
    source_file VARCHAR(255),
    notion_page_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
```

**module_sections** (for runtime)
```sql
CREATE TABLE module_sections (
    id SERIAL PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),
    section_number INTEGER,
    title VARCHAR(255),
    content_type VARCHAR(50),
    content_data JSONB,  -- Notion recordMap or markdown
    created_at TIMESTAMP DEFAULT NOW()
);
```

**module_progress** (student tracking)
```sql
CREATE TABLE module_progress (
    id SERIAL PRIMARY KEY,
    student_id INTEGER,
    module_id INTEGER REFERENCES modules(id),
    status VARCHAR(50),
    total_time_seconds INTEGER,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);
```

---

## 🔄 Data Flow

```
┌────────────────────────────────────────────────────────────────┐
│ STEP 1: Content Creation (ALREADY DONE via CADENCE export)    │
│   1.1GB CADENCE export on OneDrive                            │
│   Contains: 68 modules as Notion pages with recordMaps        │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             │ Ingestion Script
                             ↓
┌────────────────────────────────────────────────────────────────┐
│ STEP 2: Extraction & Cataloging                               │
│   scripts/ingest_cadence_export.py                            │
│   • Downloads 1.1GB ZIP from OneDrive                         │
│   • Extracts markdown/recordMaps from 68 modules              │
│   • Creates JSON files in modules/exports/                    │
│   • Reads notion_modules_categorized.csv for metadata         │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             │ GitHub Storage
                             ↓
┌────────────────────────────────────────────────────────────────┐
│ STEP 3: Version Control                                       │
│   modules/exports/*.json                                      │
│   • new-recruits.json                                         │
│   • github-guide.json                                         │
│   • ... (68 total)                                            │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             │ Deployment Script
                             ↓
┌────────────────────────────────────────────────────────────────┐
│ STEP 4: PostgreSQL Deployment                                 │
│   scripts/gamma_tasks.py deploy-modules                       │
│   • Reads JSON files from modules/exports/                    │
│   • Inserts into PostgreSQL (modules + module_sections)       │
│   • Creates deployment_log.json for Beta                      │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             │ API Access
                             ↓
┌────────────────────────────────────────────────────────────────┐
│ STEP 5: Student Access (React App)                            │
│   React onboarding app using react-notion-x                   │
│   • Fetches: GET /api/modules/<id>                            │
│   • Renders: NotionRenderer with recordMap from Postgres      │
│   • Logs progress: POST /api/progress                         │
│   • Students see: Dark-themed, custom-styled pages            │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             │ Analytics
                             ↓
┌────────────────────────────────────────────────────────────────┐
│ STEP 6: Progress Tracking & Reporting                         │
│   scripts/gamma_tasks.py analytics/leaderboard                │
│   • Queries module_progress table                             │
│   • Generates completion stats                                │
│   • Updates Onboarding Progress DB in Notion (optional)       │
│   • Creates leaderboard view in New Hire HQ column            │
└────────────────────────────────────────────────────────────────┘
```

---

## 🎬 Implementation Roadmap

### Phase 1: Notion Hub Setup (TODAY)

**1.1 Update Hero Section**
- Replace placeholder text with CADENCE mission statement
- Add launch date: "Launch Readiness: 2/14"
- Add KPIs callout (modules ready, team size, systems integration %)

**1.2 Configure Navigation Database**
- Add properties: Subsystem, Surface, Priority
- Populate with CADENCE subsystem pages
- Embed at top of Proto-type page

**1.3 Build Three-Column Layout**
- Merge existing 5 columns into 3:
  - Columns 1-2 → Mission Control
  - Column 3 → Active Workstreams
  - Columns 4-5 → New Hire HQ

**Column A: Mission Control**
```
📋 Mission Brief (callout with CADENCE overview)
✅ Launch Checklist (to-do list)
👥 Key Contacts (table or bullets)
🔗 Subsystem Quick Links
   • Avionics → [link to page]
   • Power → [link to page]
   • Mission Ops → [link to page]
   • Structures → [link to page]
```

**Column B: Active Workstreams**
```
Embedded Dev Tasks DB (Status ≠ Done)
Embedded Integration Checklist (Blocked items)
Embedded Technical Decisions (Status = In Review)
```

**Column C: New Hire HQ**
```
🚀 Launch Onboarding App (callout with button/link)
   "Complete modules in the FRAMES onboarding app"
   [Launch App →]

☑️ Week 1 Jumpstart
   □ Join Discord/Slack
   □ Read Mission Brief
   □ Complete Module 1: New Recruits
   □ Schedule Mentor Call
   □ Review GitHub Guide

📚 Module Library
   [Embedded classic DB view]
   Filter: Status = Published
   View: Gallery or List
   Show: Title, Category, Estimated Minutes

📊 Onboarding Progress
   [Embedded mini-database]
   Name      | Cohort    | Modules | % Done | Last Updated
   Alice     | Fall 2025 | 8       | 47%    | Nov 26
   Bob       | Fall 2025 | 5       | 29%    | Nov 25

💬 Need Help?
   Contact: @TeamLead or #onboarding-help
```

**1.4 Create Onboarding Progress Database**
- Create new classic database in Notion
- Add properties as specified above
- Manually seed with 2-3 test entries
- Embed table view in Column C

**1.5 Import Module Library CSV**
- Verify Module Library is "classic" (not data source)
- Import `data/projects/CADENCE/notion_modules_categorized.csv`
- Configure "Published" view
- Embed in Column C

---

### Phase 2: Ingestion Pipeline (THIS WEEK)

**2.1 Run CADENCE Ingestion**
```bash
# Test with 5 modules first
python scripts/ingest_cadence_export.py --limit 5

# Verify JSON files created
ls modules/exports/

# Run full ingestion
python scripts/ingest_cadence_export.py --overwrite
```

**2.2 Verify Exports**
- Check that 68 JSON files created in `modules/exports/`
- Validate structure matches schema
- Check recordMaps are included

**2.3 Document Process**
- Update NOTION_WORKSPACE_ENHANCEMENT.md with actual steps
- Document OneDrive link in `data/archive/notion_exports/README.md`

---

### Phase 3: PostgreSQL Deployment (NEXT WEEK)

**3.1 Set Up PostgreSQL**
- Configure DATABASE_URL in `.env`
- Run schema migrations
- Test connection

**3.2 Deploy Modules**
```bash
# Deploy to PostgreSQL
python scripts/gamma_tasks.py deploy-modules

# Verify deployment
python scripts/gamma_tasks.py analytics --parent-id <dev_tasks_db>
```

**3.3 Test API Endpoints**
- Create Flask endpoint: `GET /api/modules`
- Create Flask endpoint: `GET /api/modules/<id>`
- Create Flask endpoint: `POST /api/progress`
- Test with Postman/curl

---

### Phase 4: React App Integration (WEEK 2)

**4.1 Create NotionPage Component**
```tsx
import { NotionRenderer } from 'react-notion-x'
import { Code } from 'react-notion-x/build/third-party/code'
import { Collection } from 'react-notion-x/build/third-party/collection'

export function ModulePage({ moduleId }) {
  const [recordMap, setRecordMap] = useState(null)

  useEffect(() => {
    fetch(`/api/modules/${moduleId}`)
      .then(res => res.json())
      .then(data => setRecordMap(data.recordMap))
  }, [moduleId])

  return (
    <div className="notion-page-wrapper">
      <NotionRenderer
        recordMap={recordMap}
        fullPage={true}
        darkMode={true}
        components={{ Code, Collection }}
      />
    </div>
  )
}
```

**4.2 Apply Space-Tech Theme**
- Import `space-tech.css` with dark theme variables
- Test rendering with different module types
- Ensure mobile responsiveness

**4.3 Add Progress Tracking**
- Hook up completion logging
- Test progress updates to PostgreSQL
- Verify Onboarding Progress DB updates

---

### Phase 5: Automation & Polish (WEEK 3-4)

**5.1 Schedule Nightly Tasks**
- Nightly ingestion check (new CADENCE content)
- Nightly analytics generation
- Weekly leaderboard update

**5.2 Beta Integration**
- Beta monitors deployment_log.json
- Beta updates Notion status fields
- Beta generates weekly summaries

**5.3 Gamma Analytics**
```bash
# Daily analytics
python scripts/gamma_tasks.py analytics --parent-id <dev_tasks_db>

# Daily leaderboard
python scripts/gamma_tasks.py leaderboard --parent-id <new_hire_hq_page>

# Weekly team lead report
python scripts/gamma_tasks.py weekly-report --parent-id <dev_tasks_db>
```

---

## 📝 Next Immediate Actions

### TODAY
1. ✅ Read and understand architecture (DONE)
2. 🎯 Populate Proto-type page with CADENCE Hub content
3. 🎯 Create Onboarding Progress database
4. 🎯 Import Module Library CSV (68 modules)
5. 🎯 Test embedded views in columns

### THIS WEEK
6. Run ingestion script for all 68 modules
7. Set up PostgreSQL connection
8. Deploy modules to database
9. Test API endpoints

### NEXT WEEK
10. Build React NotionPage component
11. Apply space-tech styling
12. Hook up progress tracking
13. Test full student flow

---

## ✅ Success Criteria

**CADENCE team sees:**
- Familiar project hub with their subsystems and work
- Integrated New Hire HQ on same page
- New hires can launch app directly from Notion
- Progress tracking visible to everyone

**New hires experience:**
- One workspace for everything
- Clear Week 1 checklist
- Module library browse-able from Notion
- React app with dark-themed, beautiful module pages

**System delivers:**
- Automated ingestion from CADENCE exports
- Version-controlled module content in GitHub
- Fast runtime from PostgreSQL
- Beautiful rendering via react-notion-x
- Progress tracking and analytics

---

**Status:** Ready to implement Phase 1
**Next Step:** Populate Proto-type page with CADENCE Hub content
