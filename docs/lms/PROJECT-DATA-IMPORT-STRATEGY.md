# Project Data Import & Organization Strategy

## 🎯 Challenge

**Situation:**
- First partner project has 1GB+ of Notion data
- Contains information from multiple teams
- Needs to be imported into FRAMES Notion workspace
- Must organize for two purposes:
  1. **Onboarding modules** - Extract training content
  2. **Research analytics** - Extract team collaboration data

**Goal:**
- Decide what to keep vs. discard
- Organize into FRAMES-compatible structure
- Design scalable storage for large datasets
- Create repeatable workflow for future projects

---

## 📊 Step 1: Audit the Project Workspace

### Questions to Answer

**Content Inventory:**
1. How many databases exist?
2. How many pages (top-level vs. nested)?
3. What types of content? (docs, meetings, tasks, designs, code, etc.)
4. What file attachments exist? (images, PDFs, videos - these add to 1GB)
5. What's the date range? (historical archive vs. active content)

**Team Structure:**
1. How many teams are in this project?
2. What disciplines? (engineering, design, management, etc.)
3. How are teams organized in Notion? (workspaces, databases, pages?)

**Content Quality:**
1. What's actually useful for onboarding?
2. What's useful for research (collaboration patterns)?
3. What's just noise? (old drafts, duplicates, personal notes)

### Audit Checklist

```markdown
## Project Workspace Audit

### Databases
- [ ] Count databases: _____
- [ ] List database names and purposes:
  - Database 1: _____ (_____ rows)
  - Database 2: _____ (_____ rows)

### Pages
- [ ] Count top-level pages: _____
- [ ] Identify page categories:
  - [ ] Project documentation
  - [ ] Team workspaces
  - [ ] Meeting notes
  - [ ] Design files
  - [ ] Technical specs
  - [ ] Administrative

### Files & Attachments
- [ ] Total file size: _____
- [ ] File types:
  - [ ] Images (_____ MB)
  - [ ] PDFs (_____ MB)
  - [ ] Videos (_____ MB)
  - [ ] Other (_____ MB)

### Team Information
- [ ] Number of teams: _____
- [ ] Team names:
  - 1. _____
  - 2. _____
- [ ] Active members per team: _____

### Content Age
- [ ] Created date range: _____ to _____
- [ ] Last updated: _____
- [ ] Still active? Yes / No
```

---

## 🗂️ Step 2: Categorize Information

### The Two Buckets

#### **Bucket 1: Onboarding Modules** 🎓
**What to KEEP:**
- ✅ **Training documentation** - How-to guides, tutorials
- ✅ **Best practices** - Lessons learned, standards
- ✅ **Templates** - Reusable workflows, forms
- ✅ **Safety protocols** - Critical procedures
- ✅ **Tool guides** - Software, hardware usage
- ✅ **Onboarding checklists** - New member orientation

**Examples:**
- "How to set up your development environment"
- "Collaboration tools we use"
- "Code review process"
- "Safety certification requirements"
- "Project management workflow"

**Destination:** `Module Library` database in FRAMES Notion

---

#### **Bucket 2: Research Analytics** 📊
**What to KEEP:**
- ✅ **Team rosters** - Members, roles, disciplines
- ✅ **Project timeline** - Milestones, deliverables
- ✅ **Collaboration patterns** - Who worked with whom
- ✅ **Interface data** - Cross-team interactions
- ✅ **Outcomes** - Success/failure metrics
- ✅ **Meeting frequency** - Team health indicators

**Examples:**
- Team member lists with roles
- Project duration and phases
- Cross-team collaboration records
- Final project outcomes (mission success?)
- Team size changes over time

**Destination:** PostgreSQL database (structured data) + Notion dashboard (reference)

---

#### **Bucket 3: Archive** 🗄️
**What to DISCARD or ARCHIVE:**
- ❌ **Personal notes** - Individual scratchpads
- ❌ **Old drafts** - Superseded versions
- ❌ **Duplicate content** - Same info in multiple places
- ❌ **Meeting notes** - Outdated, no actionable insights
- ❌ **Irrelevant files** - Memes, off-topic content
- ⚠️ **Archive (maybe):**
  - Historical design files (if storage permits)
  - Old technical specs (reference only)

**Destination:**
- Delete or move to separate "Archive" Notion page
- Store file links only (not full content)

---

## 🏗️ Step 3: Design FRAMES Notion Structure

### Option A: Separate Import Workspace (Recommended)

Create a temporary "Project Import" workspace to organize before integrating:

```
FRAMES Notion Workspace
│
├── 📚 Module Library (database)
│   └── (Clean, curated training modules)
│
├── 🔬 Research Data (database)
│   └── (Structured team/project analytics)
│
└── 📦 Project Imports
    │
    ├── 🏗️ Project Alpha (imported)
    │   ├── 📋 Raw Data (everything imported)
    │   ├── ✅ Curated Content
    │   │   ├── For Modules (linked to Module Library)
    │   │   └── For Research (linked to Research DB)
    │   └── 🗑️ Archive (noise, old drafts)
    │
    ├── 🏗️ Project Beta (future import)
    └── 🏗️ Project Gamma (future import)
```

**Workflow:**
1. Import full project → `Project Alpha / Raw Data`
2. Manually curate → `Project Alpha / Curated Content`
3. Link to Module Library → Create module entries
4. Extract to PostgreSQL → Research analytics data
5. Archive the rest → `Project Alpha / Archive`

---

### Option B: Direct Integration (Risky)

Import directly into Module Library and Research databases.

⚠️ **Warning:** Can pollute your clean workspace with noise.

---

## 💾 Step 4: Storage Strategy

### Large File Problem (1GB+)

**Where does the 1GB come from?**
- Likely: Images, PDFs, videos embedded in pages
- Problem: Notion has file size limits per workspace

**Solutions:**

#### **Solution 1: Notion Links Only** (Recommended)
```
Original Project Workspace (keep as archive)
    ↓
Extract text/structure → FRAMES Notion
    ↓
Link back to original for media:
"See [original design file](link to original workspace)"
```

**Pros:**
- ✅ Keeps FRAMES workspace small
- ✅ Preserves original context
- ✅ No duplication

**Cons:**
- ⚠️ Requires maintaining two workspaces
- ⚠️ Links can break if original deleted

---

#### **Solution 2: External Storage + Notion**
```
Media Files (images, videos, PDFs)
    ↓
Upload to: AWS S3 / Google Drive / Dropbox
    ↓
Embed links in Notion pages
```

**Pros:**
- ✅ Unlimited storage
- ✅ Cheaper than Notion storage
- ✅ Faster loading

**Cons:**
- ⚠️ Requires external service
- ⚠️ More complex setup

---

#### **Solution 3: Selective Import**
```
Only import:
- Text content (takes minimal space)
- Critical diagrams/images
- Skip: videos, large PDFs, historical files
```

**Pros:**
- ✅ Keeps workspace manageable
- ✅ Focus on essential content

**Cons:**
- ⚠️ Loses some context

---

## 📋 Step 5: Extraction Workflow

### For Onboarding Modules

**Manual Process (First Time):**

1. **Identify training content** in imported project
   - Search for: "how to", "guide", "tutorial", "onboarding"
   - Look for: checklists, step-by-step pages

2. **Create module in Module Library database**
   - Title: "Collaboration Tools Setup" (example)
   - Category: "tools"
   - Status: "draft"
   - Source: Link to original project page

3. **Copy or link content**
   - Option A: Duplicate page into Module Library
   - Option B: Link to original project page

4. **Clean up**
   - Remove project-specific details
   - Generalize for all students (not team-specific)
   - Add context/intro if needed

5. **Assign properties**
   - Target Audience: undergraduate/graduate
   - Estimated Time: 30 minutes
   - Prerequisites: List other modules
   - Tags: Add for searchability

**Repeat for each useful piece of training content.**

---

### For Research Analytics

**Automated Process (Via Script):**

Create a script: `scripts/extract_team_data_from_notion.py`

```python
# Pseudo-code
def extract_research_data(project_page_id):
    # 1. Find team roster database/page
    teams = find_teams(project_page_id)

    # 2. Extract structured data
    for team in teams:
        team_data = {
            'name': team.name,
            'discipline': team.discipline,
            'members': extract_members(team),
            'project_id': project_id,
        }
        # Insert into PostgreSQL
        insert_team(team_data)

    # 3. Extract interfaces (collaboration)
    interfaces = find_collaboration_events(project_page_id)
    for interface in interfaces:
        insert_interface(interface)

    # 4. Extract outcomes
    outcomes = find_project_outcomes(project_page_id)
    insert_outcomes(outcomes)
```

**Result:** PostgreSQL database populated with structured analytics data.

---

## 🔄 Step 6: Repeatable Process for Future Projects

### Standardized Import Workflow

Create a checklist for each new project:

```markdown
## Project Import Checklist

### Pre-Import
- [ ] Get Notion workspace link from project team
- [ ] Run audit: count databases, pages, files
- [ ] Estimate storage needs
- [ ] Create "Project [Name]" page in FRAMES Imports section

### Import
- [ ] Duplicate project workspace into FRAMES (or just link)
- [ ] Organize into: Raw Data / Curated / Archive

### Curate for Modules
- [ ] Identify training content (how-to's, guides)
- [ ] Create entries in Module Library database
- [ ] Link or duplicate content
- [ ] Generalize content (remove project-specific details)
- [ ] Assign properties (category, audience, time)

### Extract for Research
- [ ] Run extraction script: `python scripts/extract_team_data_from_notion.py`
- [ ] Verify data in PostgreSQL:
  - [ ] Teams table populated
  - [ ] Faculty/members linked
  - [ ] Interfaces recorded
  - [ ] Outcomes captured
- [ ] Create research dashboard page in Notion (visualizations)

### Cleanup
- [ ] Archive noise (old drafts, duplicates)
- [ ] Store large files externally (if needed)
- [ ] Document what was kept vs. discarded
- [ ] Update project status in FRAMES tracking

### Verify
- [ ] Test modules in LMS: export → deploy → render
- [ ] Test research data: run analytics queries
- [ ] Get feedback from team leads
```

---

## 💡 Recommendations

### Immediate Actions (This Week)

1. **Audit the project workspace**
   - Use the checklist above
   - Understand what you have

2. **Create "Project Imports" section in Notion**
   - Set up the folder structure
   - Start with one project

3. **Manually curate 3-5 sample modules**
   - Pick obvious training content
   - Practice the workflow
   - Test with export pipeline

4. **Extract basic team data**
   - Team names, members, project duration
   - Insert into PostgreSQL manually (or via script)

### Medium-Term (Next 2 Weeks)

5. **Build extraction script**
   - `extract_team_data_from_notion.py`
   - Automate team/interface data extraction

6. **Decide on storage strategy**
   - Keep original workspace as archive?
   - Move large files to S3/Drive?
   - Selective import only?

7. **Refine module curation**
   - Create template for generalizing content
   - Define quality standards
   - Get team lead feedback

### Long-Term (Ongoing)

8. **Standardize import process**
   - Document workflow
   - Create scripts/tools
   - Train team leads to prepare data

9. **Scale to 8 universities**
   - Repeat workflow for each project
   - Compare modules across universities
   - Identify common patterns

---

## 🎯 Decision Framework: Keep vs. Discard

### Quick Filter Questions

**For Onboarding Modules:**
1. ❓ Does this teach a skill/concept students need?
2. ❓ Is it generalizable (not project-specific)?
3. ❓ Is it still relevant (not outdated)?
4. ❓ Would new students find this useful?

**If YES to all 4 → KEEP for Module Library**

**For Research Analytics:**
1. ❓ Does this show team structure/composition?
2. ❓ Does this show collaboration patterns?
3. ❓ Does this show project outcomes?
4. ❓ Can this be quantified (numbers, dates, relationships)?

**If YES to any → EXTRACT to PostgreSQL**

**For Everything Else:**
1. ❓ Is this a duplicate of something we kept?
2. ❓ Is this outdated or superseded?
3. ❓ Is this personal/individual work?
4. ❓ Is this just noise (memes, off-topic)?

**If YES to any → ARCHIVE or DELETE**

---

## 📊 Expected Outcomes

### After Processing First Project

**Module Library:**
- 10-20 curated training modules
- Organized by category
- Ready for export → deployment

**PostgreSQL Database:**
- 5-10 teams recorded
- 20-50 team members
- 50-200 interfaces
- Project outcomes captured

**Storage:**
- FRAMES Notion: <100 MB (text + critical images)
- Original archive: 1GB (preserved for reference)
- External storage: 500 MB (if using S3/Drive for media)

### Scalability

**For 8 Universities:**
- Module Library: 100-200 modules (deduplicated)
- PostgreSQL: 50-100 teams, 500-1000 members, 2000+ interfaces
- Storage: <1GB in FRAMES Notion (lean)

---

## 🚀 Next Steps

1. **Run the audit** (1-2 hours)
   - Count databases, pages, files
   - Categorize content types

2. **Share audit results** with me
   - I'll help refine the strategy
   - Identify quick wins

3. **Test with 1 module** (30 min)
   - Pick one piece of training content
   - Create module in Module Library
   - Run export → deploy → test in React

4. **Extract 1 team** (30 min)
   - Manually insert team data into PostgreSQL
   - Test research analytics queries

5. **Iterate and scale**
   - Refine workflow based on learnings
   - Process more content
   - Build automation scripts

---

## 📞 Questions to Answer

Before we proceed, can you tell me:

1. **What does the project workspace contain?**
   - Engineering docs? Design files? Meeting notes?
   - Is it organized in databases or just pages?

2. **What are you most interested in?**
   - Priority A: Extracting training modules?
   - Priority B: Understanding team collaboration?
   - Both equally?

3. **Storage constraints?**
   - Can you keep the original 1GB workspace as archive?
   - Do you have AWS/GCS for external file storage?
   - Need to stay within Notion limits?

4. **Timeline?**
   - Need to process this project ASAP?
   - Or can we take time to build proper workflow?

Let me know and I'll help you execute! 🎯
