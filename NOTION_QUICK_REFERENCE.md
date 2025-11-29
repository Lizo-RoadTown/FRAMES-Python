# 🌌 Quick Reference: Beautiful Notion Workspace

## Run the Script

```bash
python scripts/create_notion_workspace_beautiful.py <PARENT_PAGE_ID>
```

## What You Get

### 8 Beautiful Space Covers
- 🚀 Development Tasks - Galaxy spiral
- 📚 Module Library - Milky Way
- 💡 Technical Decisions - Earth from space
- ✅ Integration Checklist - Star network
- 🏠 Dashboard - Blue nebula
- 📚 LMS Page - Colorful nebula
- 📖 Docs Hub - Star field
- 📅 Weekly Review - Purple nebula

### Design Features
- ✨ High-res space photography
- 🎨 Emoji icons everywhere
- 🌈 Color-coded statuses
- 📦 Callout blocks
- ➖ Visual dividers
- ✅ Structured layouts

## Color Code

```
🔴 Red    - Critical/Blocked
🟠 Orange - High Priority
🟡 Yellow - Review/Warning
🟢 Green  - Done/Success
🔵 Blue   - Active/Info
🟣 Purple - Planning
⚪ Gray   - Not Started
```

## Emoji System

```
🚀 Tasks        📚 Learning
💡 Ideas        ✅ Checklists
📊 Analytics    🎨 Frontend
⚙️ Backend      🗄️ Database
🔗 Integration  📖 Docs
🏠 Home         📅 Calendar
```

## Best Practices

1. ✅ Add cover to every page
2. ✅ Use emoji icons
3. ✅ Color-code statuses
4. ✅ Add callouts for instructions
5. ✅ Use dividers between sections
6. ✅ Create linked database views
7. ✅ Follow consistent structure
8. ✅ Keep it mobile-friendly

## CADANCE Hub Quick Setup

1. **Prototype Layout (Page ID `2b86b8ea-578a-80cb-8f25-f080444ec266`)**
   - Keep the template hero row but swap copy for CADANCE mission + current objectives.
   - Use the existing Navigation database as the global menu (add Subsystem + Surface properties).
   - Recombine the five skinny columns into three lanes:
     - **Mission Control** → briefs, launch checklist, key contacts, subsystem jump links.
     - **Active Workstreams** → Development Tasks (Status ≠ Done), Integration Checklist (Blocked), Technical Decisions (In Review).
     - **New Hire HQ** → onboarding CTA, Week 1 Jumpstart checklist, Module Library view, progress + leaderboard blocks, "Need Help?" callout.
   - Dedicate the follow-on column lists to Leadership Snapshots, Subsystem Boards, Docs & Decisions, and Automation Surfaces.

2. **New Hire HQ Elements**
   - CTA button to the React onboarding app (plus optional QR code).
   - Week 1 Jumpstart checklist (accounts, mission brief, first module, mentor intro).
   - Embedded Module Library view (classic DB filtered to Published + Getting Started).
   - Progress mini-table (Name, Cohort, Modules Completed, % Complete, Last Updated) and leaderboard snapshot fed by Gamma analytics.
   - "Need Help?" callout with team lead + Slack channel.

3. **Classic Module Library**
   - Fields: Name, Category, Description, Target Audience, Discipline, Estimated Minutes, Status, Difficulty, Source Type, Source File, Tags, Prerequisites.
   - Import `data/projects/CADENCE/notion_modules_categorized.csv` once the DB is classic; embed Published + Category shortcuts inside Proto-type Column C.

4. **Automation Hooks**
   - CADANCE exports tracked in `data/archive/notion_exports/README.md`.
   - `scripts/ingest_cadence_export.py` → `modules/exports/` → `scripts/gamma_tasks.py deploy-modules` populates Postgres.
   - `scripts/gamma_tasks.py analytics` + `leaderboard` keep the Column C progress/leaderboard blocks in sync with Neon.
## Resources

- **Free Images:** unsplash.com, images.nasa.gov
- **Best Practices:** NOTION_DESIGN_BEST_PRACTICES.md
- **Full Guide:** NOTION_WORKSPACE_ENHANCEMENT.md

---

**Made with 💫 for FRAMES Project**
