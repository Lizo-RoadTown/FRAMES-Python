# CADENCE Project Data Analysis & Storage Strategy

## 📊 What You Have

**File:** `539febca-778f-4de9-97d3-1ece55645f17_ExportBlock-e881308d-93d4-492e-bdac-6d92e7bb342e.zip`
**Size:** 1.1 GB
**Project:** CADENCE CubeSat Mission

### Content Breakdown

**Total Files:** ~2,160 files

**By Type:**
- **1,417 Markdown files** (.md) - Notion pages exported as markdown
- **527 Images** (.png/.jpg) - Screenshots, diagrams, photos
- **138 CSV files** (.csv) - Notion databases exported as CSV
- **63 PDFs** - Technical documents, presentations, guides

**Size Distribution:**
- **PDFs:** ~60-70% of size (large NASA guides, presentations)
- **Images:** ~20-30% of size (mission patch, screenshots)
- **Markdown + CSV:** <5% of size (actual text content)

---

## 🗂️ Content Categories

### 1. **Team Workspaces** (7 Technical Teams)
- Avionics Hardware
- Power Systems
- Structures
- Thermals
- Communications RF
- Mission Ops
- CADENCE-SWANS (overall)

**Files:**
- Team pages (.md)
- Daily logs (.csv)
- Task trackers (.csv)
- Meeting notes (.csv)

---

### 2. **Reference Documents** (PDFs - 700+ MB)
- **NASA Training Materials:**
  - `UNP_Mission_Design_Course_Presentation` (11.7 MB)
  - `UNP_NS12_Users_Guide` (3.8 MB)
  - `NASA_MSFC_Electrical_Power_Systems_for_Cubesats` (6.8 MB)
  - `4_UNP_NASA_Electrical_Power_Systems` (6 MB)

- **Project Documents:**
  - `CADENCE_Mission_Design_Document_-_PDR` (2.2 MB)
  - `Requirements_Verification_Matrix` (492 KB)
  - `PDR_Budget_Documents` (multiple versions)

- **Technical Guides:**
  - `16_UNP_Communications_Subsystem` (1.8 MB)
  - `1610_-_Clark_-_Power_Budgets_for_CubeSat_Mission_Success` (1.2 MB)
  - `outlook_calendar_tutorial` (441 KB)

- **Papers:**
  - `IEEE_Aerospace_Conference_Mission_Ops_Paper_2026` (8 MB)

---

### 3. **Databases** (CSV Exports)
- **Meeting Notes:**
  - Spring & Summer 2025 Meeting Notes
  - EAT Meeting Notes
  - Fall 2025 Meetings

- **Task Tracking:**
  - Tasks Tracker (main)
  - Summer 2025 Tasks
  - Task Progress
  - Daily Logs (multiple teams)

- **Team-Specific:**
  - Avionics Calendar
  - Components tracking
  - CAD Task Comments
  - Mass Budget

---

### 4. **Guide Pages** (Useful for Modules!)
- **GitHub Guide** - Version control onboarding
- **Software** - Tools and setup
- **New Recruits** - Onboarding documentation
- **Outlook Calendar Tutorial** (PDF)

---

### 5. **Management Pages**
- Program Manager Zone
- Chief Engineer Zone
- PI Meetings and Questions

---

## 🎯 What to Keep vs. Archive

### ✅ **KEEP for Module Library** (Priority: HIGH)

**Training/Onboarding Content:**
1. **GitHub Guide** (.md) - Version control tutorial
2. **New Recruits** (.md) - Onboarding process
3. **Software** (.md) - Tools setup guide
4. **Outlook Calendar Tutorial** (.pdf) - Calendar management

**Technical Training Materials:**
5. **NASA Power Systems Guide** (4_UNP_NASA_Electrical_Power_Systems.pdf)
6. **Communications Subsystem Guide** (16_UNP_Communications_Subsystem.pdf)
7. **Mission Design Course** (UNP_Mission_Design_Course_Presentation.pdf)
8. **NS12 Users Guide** (UNP_NS12_Users_Guide_RevA_18Feb25.pdf)

**Best Practices:**
9. Team workflow pages (extract collaboration patterns)
10. Task tracking templates (reusable workflows)

**Estimated Total:** ~30-50 MB (markdown + select PDFs)

---

### 📊 **EXTRACT for Research Database** (Priority: HIGH)

**Team Structure:**
- 7 technical teams from CSV/markdown
- Team member names from daily logs
- Roles/disciplines from team pages

**Collaboration Data:**
- Meeting notes CSVs → Who attended which meetings
- Task tracker CSVs → Cross-team dependencies
- Spring/Summer/Fall meeting patterns → Temporal collaboration

**Project Timeline:**
- Task progress CSV → Milestones
- Meeting dates → Project phases
- PDR (Preliminary Design Review) date → Key event

**Outcomes:**
- Mission success? (TBD - may need to ask)
- Budget data (from PDR_Budget_Documents.pdf)
- Requirements met? (from Requirements_Verification_Matrix.pdf)

**Estimated Data:** ~50-100 database rows (teams, members, interfaces)

---

### 🗄️ **ARCHIVE** (Priority: LOW - Delete or External Storage)

**Large PDFs (not training-focused):**
- Mission Design Document (2.2 MB) - Project-specific, not reusable
- Budget documents - Historical reference only
- IEEE conference paper - Research artifact
- **Total:** ~20-30 MB

**Images:**
- 527 images (mostly screenshots)
- Mission patch (1 MB) - Keep this one!
- Screenshots of status - Not needed for modules
- **Total:** ~400-500 MB

**Old/Redundant CSVs:**
- "_all.csv" versions (duplicates)
- Multiple versions of same database
- **Total:** ~5 MB

**Management Pages:**
- Program Manager Zone
- Chief Engineer Zone
- PI Meetings
- **Total:** ~1-2 MB

---

## 💾 Storage Strategy Recommendations

### **Option 1: Three-Tier Storage** (RECOMMENDED)

```
Tier 1: FRAMES Notion (Training Content)
├── GitHub Guide
├── New Recruits Onboarding
├── Software Setup
└── Links to Tier 2 for media
Size: ~5 MB (markdown only)

Tier 2: AWS S3 / Google Drive (Reference PDFs)
├── NASA Training PDFs (10 files, ~40 MB)
├── Technical Guides
└── Mission Patch image
Size: ~50 MB
Cost: $0-1/month

Tier 3: Original Archive (Everything Else)
├── Keep zip file in cloud storage
├── Or: Upload to GitHub as release asset
└── Access only when needed for deep research
Size: 1.1 GB
Cost: Free (GitHub) or ~$0.02/month (S3)
```

**Total FRAMES Notion Impact:** <10 MB (tiny!)

---

### **Option 2: GitHub Large File Storage (LFS)**

```
GitHub Repository
├── /data/project-archives/
│   └── CADENCE_export.zip (via Git LFS)
├── /docs/projects/CADENCE/
│   └── extracted-modules/ (markdown only)
└── README with links to PDFs on S3

Size in repo: ~5 MB (pointers only)
LFS storage: 1.1 GB
Cost: Free up to 1GB, then $5/month per 50GB
```

---

### **Option 3: Neon Postgres Blob Storage** (NOT RECOMMENDED)

⚠️ **Don't do this:**
- PostgreSQL not designed for large files
- Will slow down database
- Expensive
- Hard to access files later

---

## 🚀 Recommended Workflow

### **Phase 1: Extract Text Content** (Do This Now)

```bash
# 1. Extract the zip
unzip "539febca...zip" -d cadence_export

# 2. Copy markdown files only to processing folder
mkdir -p data/projects/CADENCE/markdown
find cadence_export -name "*.md" -exec cp {} data/projects/CADENCE/markdown/ \;

# 3. Copy useful CSVs
mkdir -p data/projects/CADENCE/databases
cp cadence_export/*Meeting*csv data/projects/CADENCE/databases/
cp cadence_export/*Tasks*csv data/projects/CADENCE/databases/
cp cadence_export/*Daily*Logs*csv data/projects/CADENCE/databases/

# Result: ~5-10 MB of text files only
```

---

### **Phase 2: Upload PDFs to External Storage** (This Week)

**Option A: Google Drive** (Easiest)
```
1. Create folder: "FRAMES Project Archives/CADENCE"
2. Upload 10 useful PDFs
3. Set to "Anyone with link can view"
4. Copy shareable links
5. Add links to Notion module pages
```

**Option B: AWS S3** (Best long-term)
```bash
# Upload PDFs to S3
aws s3 sync cadence_export/*.pdf s3://frames-project-archives/CADENCE/pdfs/ --acl public-read

# Get URLs
aws s3 ls s3://frames-project-archives/CADENCE/pdfs/ --recursive
```

---

### **Phase 3: Archive Original Zip** (This Week)

**Option A: GitHub Release** (Free, permanent)
```bash
# Create release with large file
gh release create v1.0-cadence-archive \
  "539febca...zip#CADENCE Full Export" \
  --notes "Complete CADENCE project export (1.1GB)"

# Anyone can download from:
# https://github.com/[your-repo]/releases/download/v1.0-cadence-archive/539febca...zip
```

**Option B: S3 Glacier Deep Archive** (Cheapest)
```bash
# Upload and immediately archive
aws s3 cp "539febca...zip" s3://frames-archives/CADENCE/ \
  --storage-class DEEP_ARCHIVE

# Cost: $0.00099/GB/month = $0.001/month for 1GB
# Retrieval: $0.02/GB (only when needed)
```

**Option C: OneDrive/Google Drive** (Simple)
- Just upload and delete local copy
- Free up to 15GB (Google) or 5GB (OneDrive personal)

---

### **Phase 4: Delete Local Zip** (After Upload)

```bash
# Verify uploaded successfully
# Then:
rm "539febca-778f-4de9-97d3-1ece55645f17_ExportBlock-e881308d-93d4-492e-bdac-6d92e7bb342e.zip"
rm -rf temp_extract/

# Keep only extracted text:
# data/projects/CADENCE/markdown/ (~5 MB)
# data/projects/CADENCE/databases/ (~2 MB)
```

---

## 📋 Immediate Action Plan

**Today (30 minutes):**

1. **Extract text content**
   ```bash
   python scripts/extract_cadence_project.py
   ```
   (I'll create this script for you)

2. **Identify 5 useful modules**
   - GitHub Guide → Module
   - New Recruits → Module
   - Software Setup → Module
   - NASA Power Systems PDF → Link in module
   - Communications Guide → Link in module

3. **Upload original zip to cloud**
   - Google Drive or OneDrive (easiest)
   - Get shareable link
   - Document location

4. **Delete local 1.1GB file**
   - Free up disk space immediately

**This Week:**

5. **Curate 5 modules** manually
   - Add to Module Library in Notion
   - Link to external PDFs
   - Test export → deploy → render

6. **Extract team data** to PostgreSQL
   - Team names, members, disciplines
   - Meeting patterns from CSVs
   - Task dependencies

7. **Set up S3/Drive for PDFs** (optional, but recommended)
   - Upload 10 useful training PDFs
   - Create permanent links
   - Reference in modules

---

## 💰 Cost Analysis

### Storage Costs

**Option 1: Google Drive** (Free Tier)
- 15 GB free
- CADENCE: 1.1 GB
- 7 more projects fit easily
- Cost: **$0/month**

**Option 2: AWS S3 Standard**
- $0.023/GB/month
- 1.1 GB = $0.025/month
- 8 projects (8 GB) = $0.18/month
- Cost: **~$2/year**

**Option 3: AWS S3 Glacier Deep Archive**
- $0.00099/GB/month
- 1.1 GB = $0.001/month
- 8 projects (8 GB) = $0.008/month
- Cost: **~$0.10/year**
- (Retrieval: $0.02/GB when needed)

**Option 4: GitHub LFS**
- 1 GB free
- Additional: $5/month per 50 GB
- Cost: **$0 for 1 project**, $5/month for 8 projects

**Recommendation:** Start with **Google Drive** (free), move to **S3 Glacier** when you have 8 projects.

---

## 🎯 Next Steps

1. **Run extraction script** (I'll create it)
2. **Upload zip to Google Drive**
3. **Delete local 1.1GB file**
4. **Curate first 3 modules from markdown**
5. **Test full pipeline with real data**

Ready to proceed? I can create the extraction script now!
