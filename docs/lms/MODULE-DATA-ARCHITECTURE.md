# Module Data Architecture & Flow

**Created:** November 26, 2025
**Purpose:** Define source of truth and data flow for LMS modules across GitHub, Notion, and PostgreSQL
**Status:** CRITICAL DECISION DOCUMENT

---

## 🎯 The Core Question

**Where does module content live, and how does it sync between systems?**

This matters because:
- **Team Leads** need to create/edit modules easily (Notion is best)
- **Students** need fast, reliable access (PostgreSQL is best)
- **Developers** need version control (GitHub is best)
- **System** needs a single source of truth

---

## 🏗️ Three Storage Systems

### **System 1: PostgreSQL (Neon) - RUNTIME DATABASE**

**Purpose:** Production data for running application

**What it stores:**
- Module metadata (title, status, estimated_minutes, etc.)
- Module sections (content, media URLs, configs)
- Student progress (who completed what, when)
- Analytics events (clicks, time spent, struggle signals)
- Module assignments (which students get which modules)

**Why this is NOT the source of truth:**
- ❌ Hard to edit (requires SQL or Python scripts)
- ❌ No version history
- ❌ Team leads can't access it directly
- ❌ Risky to make changes (could break production)

**Role:** Runtime database for serving content to students

---

### **System 2: Notion - CONTENT MANAGEMENT**

**Purpose:** User-friendly interface for creating and editing modules

**What it stores:**
- Module planning pages (ideas, outlines, drafts)
- Module Library database (catalog of all modules)
- Rich content (formatted text, embedded images, tables)
- Collaborative editing (comments, task assignments)
- Review status (Intake → Drafting → Review → Ready → Live)

**Why this COULD be the source of truth:**
- ✅ Easy for team leads to create content
- ✅ Visual formatting (bold, lists, headings)
- ✅ Built-in collaboration features
- ✅ Access control (share with specific people)
- ✅ Change history (page revisions)

**Why this might NOT be the source of truth:**
- ❌ Notion API can be slow
- ❌ Rate limits (3 requests/second)
- ❌ Not designed for high-frequency reads
- ❌ Requires internet to access
- ❌ Vendor lock-in

**Role:** Content creation and approval workflow

---

### **System 3: GitHub - VERSION CONTROL**

**Purpose:** Code, documentation, and version-controlled content

**What it stores:**
- Application code (React, Flask, database models)
- Migration scripts (database schema changes)
- Documentation (workflow guides, technical specs)
- Module content templates (starter files)
- Configuration files (.env.example, database schemas)

**Why this COULD be the source of truth:**
- ✅ Version control (full history, diff, rollback)
- ✅ Peer review (pull requests, code review)
- ✅ Free and reliable
- ✅ Integrates with CI/CD
- ✅ Markdown support

**Why this might NOT be the source of truth:**
- ❌ Team leads may not be comfortable with Git
- ❌ Requires technical knowledge
- ❌ Not as visual as Notion
- ❌ Slower iteration cycle (commit, push, PR)

**Role:** Code repository and versioned documentation

---

## 🔄 Proposed Architecture: Hybrid Source of Truth

### **Decision: Three-Tier Content Flow**

```
┌─────────────────────────────────────────────────────────────────┐
│                    TIER 1: CONTENT CREATION                     │
│                         Notion (Source)                         │
│   Team leads create modules in Module Library database         │
│   Status: Intake → Drafting → In Review → Ready                │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ EXPORT/SYNC
                      │ (Manual or scripted)
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│                  TIER 2: VERSION CONTROL                        │
│                     GitHub (Canonical)                          │
│   Module content as JSON/YAML files in /data/modules/          │
│   Status: Ready → Approved (via PR)                            │
│   - Full version history                                       │
│   - Peer review process                                        │
│   - Rollback capability                                        │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ DEPLOY/SYNC
                      │ (Scripted on approval)
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│                   TIER 3: PRODUCTION RUNTIME                    │
│                  PostgreSQL (Neon) (Live)                       │
│   Module data served to students via Flask API                 │
│   Status: Live                                                  │
│   + Student progress, analytics, assignments                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Module Content Lifecycle

### **Phase 1: CREATION (Notion)**

**Who:** Team leads, faculty, content creators

**What happens:**
1. Team lead creates new entry in **Module Library** Notion database
2. Sets metadata:
   - Module Name: "Lab Safety 101"
   - Status: "Intake"
   - Team Lead: @JohnDoe
   - University: "Cal Poly Pomona"
   - Cohort: "Fall 2025"
   - Content Source: "AI-assisted" or "Form" or "Interview"

3. Team lead creates module content in Notion page:
   - Uses rich text formatting
   - Embeds images, videos
   - Structures into sections
   - Adds learning objectives

4. Updates status: Intake → Drafting → In Review

**Output:** Rich content in Notion, ready for export

---

### **Phase 2: EXPORT (Notion → GitHub)**

**Who:** Developer or automated script

**What happens:**
1. Run export script: `python scripts/export_notion_to_github.py`
2. Script uses Notion API to fetch module data
3. Converts Notion blocks to structured format (JSON/YAML)
4. Creates file: `data/modules/lab-safety-101.json`

**Example: lab-safety-101.json**
```json
{
  "module_id": "lab-safety-101",
  "title": "Lab Safety 101",
  "description": "Essential safety protocols for entering the lab",
  "category": "Safety",
  "estimated_minutes": 10,
  "created_by_id": "faculty-john-doe",
  "university_id": "cpp",
  "status": "ready",
  "prerequisites": [],
  "tags": ["safety", "onboarding", "required"],
  "target_audience": "incoming_students",
  "notion_page_id": "abc123def456",
  "content_source": "notion",
  "sections": [
    {
      "section_number": 1,
      "section_type": "text",
      "title": "Welcome to Lab Safety",
      "content": "# Welcome to Lab Safety 101\n\nThis module will teach you...",
      "media_url": null,
      "duration_seconds": 120
    },
    {
      "section_number": 2,
      "section_type": "interactive",
      "title": "Locate Safety Equipment",
      "content": {
        "instruction": "Click on 5 safety equipment locations",
        "hotspots": [
          {"id": "fire-extinguisher", "x": 100, "y": 200, "label": "Fire Extinguisher"},
          {"id": "eye-wash", "x": 300, "y": 150, "label": "Eye Wash Station"}
        ],
        "completion_criteria": {"hotspots_clicked": 5}
      },
      "media_url": "/assets/lab-floor-plan.png"
    }
  ],
  "metadata": {
    "revision": 1,
    "exported_at": "2025-11-26T14:30:00Z",
    "exported_by": "notion_sync_bot"
  }
}
```

5. Commit to GitHub: `git add data/modules/lab-safety-101.json`
6. Create PR: "Add Lab Safety 101 module"
7. Update Notion status: In Review → Ready

**Output:** Version-controlled JSON file in GitHub

---

### **Phase 3: REVIEW & APPROVAL (GitHub)**

**Who:** Content reviewer, technical lead

**What happens:**
1. Reviewer opens PR on GitHub
2. Checks JSON structure is valid
3. Previews content rendering (if preview tool exists)
4. Reviews learning objectives, technical accuracy
5. Suggests edits via PR comments
6. If changes needed → back to Notion, re-export
7. If approved → merge PR to `main` branch

**Output:** Approved module file in `main` branch

---

### **Phase 4: DEPLOYMENT (GitHub → PostgreSQL)**

**Who:** Automated deployment script or manual trigger

**What happens:**
1. PR merged to `main` triggers deployment script
2. Script runs: `python scripts/deploy_modules_to_db.py`
3. Script reads `data/modules/lab-safety-101.json`
4. Creates/updates records in PostgreSQL:
   - Insert into `modules` table
   - Insert sections into `module_sections` table
5. Sets status to "published"
6. Module is now live for students

**Example: deploy_modules_to_db.py**
```python
import json
from pathlib import Path
from shared.database.db_models import Module, ModuleSection, db

def deploy_module(json_path):
    with open(json_path) as f:
        data = json.load(f)

    # Create or update module
    module = Module.query.filter_by(module_id=data['module_id']).first()
    if not module:
        module = Module(module_id=data['module_id'])

    # Update fields
    module.title = data['title']
    module.description = data['description']
    module.category = data['category']
    # ... set all other fields

    db.session.add(module)
    db.session.commit()

    # Delete old sections, add new ones
    ModuleSection.query.filter_by(module_id=module.id).delete()

    for section_data in data['sections']:
        section = ModuleSection(
            module_id=module.id,
            section_number=section_data['section_number'],
            section_type=section_data['section_type'],
            # ... set all fields
        )
        db.session.add(section)

    db.session.commit()
    print(f"✅ Deployed module: {data['module_id']}")

# Deploy all modules in data/modules/
for json_file in Path('data/modules/').glob('*.json'):
    deploy_module(json_file)
```

7. Update Notion status: Ready → Live
8. Update GitHub Branch/PR field in Notion with link

**Output:** Live module accessible to students via API

---

### **Phase 5: CONSUMPTION (Students Access)**

**Who:** Students via React frontend

**What happens:**
1. Student opens LMS: `http://localhost:3000`
2. React app fetches module list: `GET /api/modules`
3. Student clicks "Lab Safety 101"
4. React app fetches module details: `GET /api/modules/lab-safety-101`
5. Flask API queries PostgreSQL:
   ```python
   module = Module.query.filter_by(module_id='lab-safety-101').first()
   sections = ModuleSection.query.filter_by(module_id=module.id).all()
   ```
6. API returns JSON to frontend
7. React renders module using appropriate viewer (TextViewer, InteractiveViewer, etc.)
8. Student progresses through sections
9. Progress tracked in `module_progress` table
10. Analytics events logged to `module_analytics_events` table

**Output:** Student learning, data collected

---

### **Phase 6: ITERATION (Updates)**

**Who:** Team lead or content creator

**What happens if module needs updates:**

**Option A: Minor edit (typo, small change)**
1. Edit directly in GitHub JSON file
2. Create PR
3. Review & merge
4. Re-deploy to PostgreSQL
5. Increment `revision` number

**Option B: Major revision**
1. Edit Notion page
2. Re-export to GitHub (overwrites or creates v2 file)
3. PR review process
4. Deploy to PostgreSQL
5. Increment `revision` number
6. Old version archived in Git history

**Version Control:**
- Git history shows all changes
- Database `revision` field tracks current version
- Old versions can be restored from Git

---

## 🔍 Source of Truth Summary

| Data Type | Source of Truth | Why |
|-----------|----------------|-----|
| **Module content (draft)** | Notion | Easy for team leads to create |
| **Module content (approved)** | GitHub | Version control, review process |
| **Module content (live)** | PostgreSQL | Fast runtime access for students |
| **Student progress** | PostgreSQL | Real-time data, no need for version control |
| **Analytics events** | PostgreSQL | High-volume writes, query performance |
| **Module metadata** | All three (synced) | Notion for editing, GitHub for versioning, PostgreSQL for serving |

---

## 🔄 Sync Strategies

### **Strategy 1: Manual Sync (Phase 0 - Current)**

**Process:**
1. Create in Notion
2. Manually run export script
3. Manually commit to GitHub
4. Manually run deployment script

**Pros:**
- Full control
- Simple to understand
- No complex automation

**Cons:**
- Time-consuming
- Prone to human error
- Doesn't scale

**Recommended for:** Initial modules, proof of concept

---

### **Strategy 2: Semi-Automated Sync (Phase 1 - Near Future)**

**Process:**
1. Create in Notion
2. Mark status as "Ready"
3. **Automated export script** runs nightly:
   - Fetches all modules with status="Ready"
   - Exports to GitHub
   - Creates PR automatically
4. Developer reviews PR
5. Merge PR triggers **automated deployment**

**Pros:**
- Less manual work
- Consistent exports
- Review step preserved

**Cons:**
- Requires scheduled task (cron job)
- Notion API rate limits

**Recommended for:** Regular module creation workflow

---

### **Strategy 3: Fully Automated Sync (Phase 2 - Future)**

**Process:**
1. Create in Notion
2. Mark status as "Ready"
3. **Notion webhook** triggers on status change
4. Export → GitHub PR → Auto-deploy (if tests pass)
5. Notion updated with "Live" status automatically

**Pros:**
- Instant sync
- Minimal manual intervention
- Scales to high volume

**Cons:**
- Complex to set up
- Requires testing infrastructure
- Higher risk of errors reaching production

**Recommended for:** Mature system with many contributors

---

## 📂 Proposed Repository Structure

```
FRAMES Python/
├── data/
│   ├── modules/                    # Module content (GitHub source of truth)
│   │   ├── lab-safety-101.json
│   │   ├── equipment-tour.json
│   │   ├── first-pull-request.json
│   │   └── ...
│   ├── assets/                     # Media assets for modules
│   │   ├── images/
│   │   │   ├── lab-floor-plan.png
│   │   │   └── safety-equipment.jpg
│   │   └── videos/
│   │       └── lab-tour.mp4
│   └── schemas/
│       └── module-schema.json      # JSON schema for validation
├── scripts/
│   ├── export_notion_to_github.py  # Notion → GitHub sync
│   ├── deploy_modules_to_db.py     # GitHub → PostgreSQL sync
│   ├── validate_module_json.py     # Check JSON against schema
│   └── sync_assets.py              # Upload assets to CDN/storage
├── shared/
│   └── database/
│       ├── db_models.py            # PostgreSQL models
│       └── migrations/             # Database migrations
└── docs/
    └── lms/
        ├── MODULE-CREATION-WORKFLOW.md
        ├── MODULE-DATA-ARCHITECTURE.md  # This file
        └── ...
```

---

## 🛡️ Data Integrity Safeguards

### **1. Validation**

**Before GitHub commit:**
```python
# scripts/validate_module_json.py
import json
import jsonschema

def validate_module(json_path):
    with open('data/schemas/module-schema.json') as f:
        schema = json.load(f)

    with open(json_path) as f:
        module = json.load(f)

    try:
        jsonschema.validate(instance=module, schema=schema)
        print(f"✅ {json_path} is valid")
        return True
    except jsonschema.ValidationError as e:
        print(f"❌ {json_path} validation failed: {e}")
        return False
```

**Before PostgreSQL deployment:**
- Check all required fields present
- Verify `module_id` is unique (or updating existing)
- Validate section numbers are sequential
- Check media URLs are accessible

---

### **2. Rollback Process**

**If bad module deployed:**

```bash
# 1. Identify the issue
git log data/modules/lab-safety-101.json

# 2. Revert to previous version
git checkout abc123 -- data/modules/lab-safety-101.json

# 3. Re-deploy
python scripts/deploy_modules_to_db.py data/modules/lab-safety-101.json

# 4. Verify in PostgreSQL
python
>>> from shared.database.db_models import Module
>>> m = Module.query.filter_by(module_id='lab-safety-101').first()
>>> print(m.revision)  # Should be decremented or marked as rollback
```

---

### **3. Backup Strategy**

**PostgreSQL backups:**
- Neon provides automatic daily backups
- Manual snapshot before major deployments

**GitHub backups:**
- Inherent (Git is distributed)
- All history preserved

**Notion backups:**
- Export entire workspace weekly
- Store as JSON in GitHub: `data/backups/notion/`

---

## 🔌 Notion Integration Details

### **Module Library Database Schema (Notion)**

```
Module Library (Database)
├── Module Name (Title)
├── Status (Select)
│   ├── Intake
│   ├── Drafting
│   ├── In Review
│   ├── Ready
│   └── Live
├── Team Lead (Person)
├── Owner (Person)
├── University (Select)
├── Cohort (Select)
├── Content Source (Select)
│   ├── AI-assisted
│   ├── Form
│   └── Interview
├── Module ID (Text) - e.g., "lab-safety-101"
├── GitHub Branch/PR (URL)
├── Last Updated (Date)
├── Related Task (Relation → Development Tasks)
└── Content Page (Link to Notion page with actual content)
```

### **Module Content Page Template (Notion)**

```markdown
# Lab Safety 101

**Metadata**
- Module ID: lab-safety-101
- Category: Safety
- Estimated Time: 10 minutes
- Target Audience: Incoming Students

**Learning Objectives**
1. Identify 5 key safety protocols
2. Locate emergency equipment in the lab
3. Understand PPE requirements

**Sections**

### Section 1: Welcome to Lab Safety
[Rich text content here...]

### Section 2: Interactive Equipment Locator
Type: Interactive
[Hotspot configuration here...]

### Section 3: PPE Requirements
[Rich text content here...]

**Export Notes**
- Last exported: 2025-11-26
- Exported by: @Developer
- GitHub PR: #123
```

---

## 🚀 Implementation Roadmap

### **Phase 0: Foundation (Current)**
- ✅ PostgreSQL schema created
- ✅ Flask API serving modules
- ✅ React viewer displaying content
- ⬜ Manual module creation (Python scripts)

**Next:** Create first module manually, test entire stack

---

### **Phase 1: Notion Integration (Weeks 1-2)**
- ⬜ Create Module Library database in Notion
- ⬜ Create module content page template
- ⬜ Write `export_notion_to_github.py` script
- ⬜ Test export with 1 module

**Deliverable:** Team lead can create module in Notion, developer exports to GitHub

---

### **Phase 2: Validation & Deployment (Weeks 3-4)**
- ⬜ Create JSON schema for modules
- ⬜ Write validation script
- ⬜ Write `deploy_modules_to_db.py` script
- ⬜ Test full pipeline: Notion → GitHub → PostgreSQL

**Deliverable:** Validated, reviewable, deployable module pipeline

---

### **Phase 3: Automation (Weeks 5-8)**
- ⬜ Schedule nightly export script (cron or GitHub Actions)
- ⬜ Auto-create GitHub PRs from exports
- ⬜ Auto-deploy on PR merge
- ⬜ Auto-update Notion status after deployment

**Deliverable:** Semi-automated workflow, minimal manual intervention

---

### **Phase 4: Scale & Optimize (Months 2-3)**
- ⬜ Notion webhook integration
- ⬜ Real-time sync (optional)
- ⬜ CDN for media assets
- ⬜ Module versioning system
- ⬜ A/B testing infrastructure

**Deliverable:** Production-grade content pipeline

---

## 🎯 Decision Summary

### **APPROVED ARCHITECTURE**

1. **Source of Truth:**
   - **Notion** = Content creation (Team lead friendly)
   - **GitHub** = Canonical version (Version controlled)
   - **PostgreSQL** = Runtime database (Student facing)

2. **Content Flow:**
   - Notion → GitHub (Export script, manual or scheduled)
   - GitHub → PostgreSQL (Deployment script, triggered on merge)
   - PostgreSQL → Students (Flask API, real-time)

3. **Sync Strategy:**
   - Start: Manual sync (Phase 0)
   - Near-term: Semi-automated with review (Phase 1-2)
   - Long-term: Fully automated with safeguards (Phase 3+)

4. **Data Ownership:**
   - Module content: All three systems (synced)
   - Student data: PostgreSQL only (never in Notion/GitHub)
   - Analytics: PostgreSQL only
   - Workflow metadata: Notion (status, assignees, etc.)

---

## 📞 Next Actions

**Immediate (This Session):**
1. Create Module Library database in Notion
2. Create first module content page in Notion
3. Write basic export script
4. Test export → GitHub → PostgreSQL flow

**Short-term (This Week):**
1. Formalize JSON schema
2. Add validation to export
3. Document sync process
4. Create module creation tutorial

**Medium-term (Next 2 Weeks):**
1. Automate export (scheduled task)
2. Set up PR automation
3. Add deployment triggers
4. Train team leads on Notion workflow

---

**This document serves as the architectural specification for module data management in FRAMES LMS. All future decisions about module storage, sync, and workflow should reference this design.**

**Version:** 1.0
**Last Updated:** November 26, 2025
**Status:** APPROVED - Ready for Implementation
