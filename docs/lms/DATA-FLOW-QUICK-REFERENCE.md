# Module Data Flow - Quick Reference

**Last Updated:** November 26, 2025

---

## 🎯 The Three Systems

```
┌──────────┐      ┌──────────┐      ┌──────────────┐
│  NOTION  │ ───▶ │  GITHUB  │ ───▶ │ POSTGRESQL   │
│  (Create)│      │ (Approve)│      │   (Serve)    │
└──────────┘      └──────────┘      └──────────────┘
Team Leads        Developers        Students
Easy editing      Version control   Fast runtime
```

---

## 📋 Source of Truth

| What | Lives In | Why |
|------|----------|-----|
| **Module content (drafts)** | Notion | Team leads create here |
| **Module content (approved)** | GitHub | Version control + review |
| **Module content (live)** | PostgreSQL | Serve to students |
| **Student progress** | PostgreSQL ONLY | Never sync to Notion/GitHub |
| **Analytics** | PostgreSQL ONLY | High-volume, query performance |
| **Workflow status** | Notion | Who's working on what |

---

## 🔄 The Module Journey

### **Step 1: CREATE (Notion)**
- Team lead fills out Module Library entry
- Creates content page with sections
- Status: Intake → Drafting → In Review → Ready

### **Step 2: EXPORT (Notion → GitHub)**
```bash
python scripts/export_notion_to_github.py
# Creates: data/modules/module-name.json
```

### **Step 3: REVIEW (GitHub)**
- Developer creates PR
- Reviewer checks content
- Merge to `main` when approved

### **Step 4: DEPLOY (GitHub → PostgreSQL)**
```bash
python scripts/deploy_modules_to_db.py
# Updates modules & module_sections tables
```

### **Step 5: SERVE (PostgreSQL → Students)**
- Student opens LMS
- React calls: `GET /api/modules/module-name`
- Flask queries PostgreSQL
- Content rendered

### **Step 6: UPDATE (If needed)**
- Edit in Notion OR directly in GitHub JSON
- Re-export & re-deploy
- Increment revision number

---

## ⚠️ Critical Rules

### **DO:**
- ✅ Create modules in Notion
- ✅ Review changes via GitHub PR
- ✅ Deploy to PostgreSQL via script
- ✅ Track student data in PostgreSQL only
- ✅ Keep GitHub as canonical version

### **DON'T:**
- ❌ Edit PostgreSQL directly (except for testing)
- ❌ Store student data in Notion or GitHub
- ❌ Deploy without PR review
- ❌ Skip validation before deploy
- ❌ Lose Notion page ID (needed for sync)

---

## 🗂️ File Locations

### **Notion**
- Database: `Module Library`
- Content: Individual pages linked from database
- Metadata: Status, Team Lead, University, etc.

### **GitHub**
- Content: `data/modules/*.json`
- Assets: `data/assets/images/`, `data/assets/videos/`
- Scripts: `scripts/export_notion_to_github.py`, `scripts/deploy_modules_to_db.py`
- Schema: `data/schemas/module-schema.json`

### **PostgreSQL**
- Tables: `modules`, `module_sections`
- Progress: `module_progress`, `module_assignments`
- Analytics: `module_analytics_events`, `module_feedback`

---

## 🛠️ Common Tasks

### **Add a New Module**
1. Create in Notion Module Library
2. Write content in Notion page
3. Set status to "Ready"
4. Run: `python scripts/export_notion_to_github.py --module <notion-page-id>`
5. Create PR, get review, merge
6. Run: `python scripts/deploy_modules_to_db.py data/modules/<module>.json`
7. Update Notion status to "Live"

### **Update Existing Module**
**Option A: Minor edit**
1. Edit `data/modules/<module>.json` directly in GitHub
2. Create PR, review, merge
3. Re-deploy: `python scripts/deploy_modules_to_db.py data/modules/<module>.json`

**Option B: Major revision**
1. Edit Notion page
2. Re-export from Notion
3. PR review process
4. Deploy to PostgreSQL

### **Rollback Module**
```bash
# 1. Find last good version in Git
git log data/modules/<module>.json

# 2. Revert to that version
git checkout <commit-hash> -- data/modules/<module>.json

# 3. Re-deploy
python scripts/deploy_modules_to_db.py data/modules/<module>.json
```

---

## 🔍 Validation Checklist

Before deploying any module:

- [ ] JSON validates against schema
- [ ] `module_id` is unique (or updating existing)
- [ ] All sections have sequential numbers
- [ ] Media URLs are accessible
- [ ] Content is approved via PR
- [ ] Notion page ID is recorded
- [ ] Status progression is correct

---

## 🚨 Emergency Procedures

### **Module Breaking Production**
1. Immediately rollback to last known good version (see above)
2. Mark module as "draft" in PostgreSQL
3. Investigate issue in GitHub JSON
4. Fix and re-deploy

### **Notion API Down**
- Continue using GitHub as source
- Manual module creation via JSON
- Sync back to Notion when API restored

### **PostgreSQL Data Loss**
- Restore from Neon backup (daily snapshots)
- Re-deploy modules from GitHub
- Student progress may need manual intervention

---

## 📊 Data Never Leaves PostgreSQL

**These stay in PostgreSQL ONLY:**
- Student progress (`module_progress`)
- Analytics events (`module_analytics_events`)
- Student feedback (`module_feedback`)
- Module assignments (`module_assignments`)

**Why:** Privacy, security, performance, FERPA compliance

---

## 🎯 Quick Decisions

**Q: Team lead wants to create module. Where?**
A: Notion Module Library

**Q: Developer needs to review module. Where?**
A: GitHub PR

**Q: Student accesses module. Where from?**
A: PostgreSQL via Flask API

**Q: Where is the canonical, approved version?**
A: GitHub `main` branch

**Q: What if Notion and GitHub disagree?**
A: GitHub wins. Re-export from Notion or edit GitHub directly.

**Q: Can I edit PostgreSQL directly?**
A: Only for testing. Production should come from GitHub deploy.

---

**For full details, see:** [MODULE-DATA-ARCHITECTURE.md](MODULE-DATA-ARCHITECTURE.md)

**For workflow steps, see:** [MODULE-CREATION-WORKFLOW.md](MODULE-CREATION-WORKFLOW.md)
