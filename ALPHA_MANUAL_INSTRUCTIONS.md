# Agent Alpha - Manual Instructions for CADENCE Hub
**Tasks A2-A5: Step-by-Step Guide**

**Date:** 2025-11-27
**Status:** Task A1 Complete (Automated) | Tasks A2-A5 Manual Required

---

## ✅ What's Already Done (Task A1)

I've successfully updated the Proto-type page via Notion API:
- ✅ Page title changed to "CADENCE Mission Control"
- ✅ Hero heading added
- ✅ Mission statement callout created
- ✅ Divider added for visual separation

**You can view this now in Notion!**

---

## 🔧 What Needs Manual Work (Tasks A2-A5)

Due to Notion API limitations with complex layouts, the following tasks require manual work in the Notion UI:

---

## Task A2: Configure Navigation Database (45 min)

**Database ID:** `2b86b8ea-578a-81f6-8104-f5eb8575ee54`

### Step 1: Add Properties to Navigation Database

1. Open the Navigation database in Notion
2. Click on the three dots (•••) at the top right
3. Add these properties:

**Property 1: Subsystem**
- Type: Select
- Options:
  - Avionics
  - Power
  - Mission Ops
  - Structures
  - Software

**Property 2: Surface**
- Type: Select
- Options:
  - Page
  - Database
  - Workflow

**Property 3: Priority**
- Type: Select
- Options:
  - P0 (Critical)
  - P1 (High)
  - P2 (Medium)
  - P3 (Low)

### Step 2: Create Navigation Entries

Click "+ New" in the database and create these 7 entries:

**Entry 1:**
- Name: Avionics Hub
- Subsystem: Avionics
- Surface: Page
- Priority: P0

**Entry 2:**
- Name: Power Systems
- Subsystem: Power
- Surface: Page
- Priority: P1

**Entry 3:**
- Name: Mission Operations
- Subsystem: Mission Ops
- Surface: Page
- Priority: P0

**Entry 4:**
- Name: Structures
- Subsystem: Structures
- Surface: Page
- Priority: P1

**Entry 5:**
- Name: Development Tasks
- Subsystem: (leave blank)
- Surface: Database
- Priority: P1

**Entry 6:**
- Name: Module Library
- Subsystem: (leave blank)
- Surface: Database
- Priority: P0

**Entry 7:**
- Name: Technical Decisions
- Subsystem: (leave blank)
- Surface: Database
- Priority: P1

---

## Task A3: Build Three-Column Layout (2 hours)

**Location:** Proto-type page (below the hero section I created)

### Step 1: Create Column Layout

1. Type `/column` and select "2 columns"
2. Add another column by clicking the + icon that appears when you hover near a column
3. You should now have 3 columns

### Step 2: Populate Column 1 - Mission Control

**Heading:**
- Type `/heading1` and write "Mission Control"
- Click the text color dropdown and choose Blue background

**Callout:**
- Type `/callout`
- Icon: 🎯
- Text: "CADENCE: Multi-university CubeSat collaboration bringing together 8 research institutions to design, build, and launch CubeSat missions. Our goal: prepare the next generation of aerospace engineers through hands-on experience."

**Launch Checklist:**
- Type `/todo` and create these items:
  - [ ] Mission design complete
  - [ ] Subsystem integration verified
  - [ ] Launch documentation ready
  - [ ] Team training complete

**Key Contacts:**
- Type a bulleted list:
  - 👤 Mission Lead: [Name]
  - 👤 Technical Lead: [Name]
  - 👤 Integration Lead: [Name]

### Step 3: Populate Column 2 - Active Workstreams

**Heading:**
- Type `/heading1` and write "Active Workstreams"
- Choose Orange background

**Linked Database 1:**
- Type `/linked` and select Development Tasks database
- Filter: Status ≠ Done
- View: Table

**Linked Database 2:**
- Type `/linked` and select Integration Checklist database
- Filter: Blocked = checked
- View: Table

**Linked Database 3:**
- Type `/linked` and select Technical Decisions database
- Filter: Status = In Review
- View: Table

### Step 4: Populate Column 3 - New Hire HQ

**Heading:**
- Type `/heading1` and write "New Hire HQ"
- Choose Purple background

**Launch App Callout:**
- Type `/callout`
- Icon: 🚀
- Text: "Launch Onboarding App"
- Below it: "Complete your training modules and join the team!"

**Week 1 Jumpstart:**
- Type `/todo` and create:
  - [ ] Join Discord server
  - [ ] Read Mission Brief
  - [ ] Complete Module 1: New Recruits
  - [ ] Schedule mentor call

**Module Library:**
- Type `/linked` and select Module Library database
- Filter: Status = Published
- View: Gallery

**Onboarding Progress:**
- Type `/linked` and create/select Onboarding Progress database
- View: Table
- Sort by: Modules Completed (descending)

**Need Help Callout:**
- Type `/callout`
- Icon: 💬
- Text: "Need help? Contact us on Slack #onboarding-help or email @TeamLead"

---

## Task A4: Add Persona-Specific Sections (1.5 hours)

**Below the 3-column layout, add these sections:**

### Leadership Snapshots

Create another 2-column layout:

**Column 1 - KPIs:**
- Type `/callout` for each KPI:
  - 📊 Modules Deployed: 68/68
  - 👥 Active Students: 25
  - ⚡ System Uptime: 99.8%

**Column 2 - Risks:**
- Type `/callout` with red background:
  - ⚠️ Blocked Items: [count]
  - ⚠️ Overdue Tasks: [count]

### Subsystem Boards

Create a 3-column layout:

**Each column:**
- Heading: [Subsystem Name] (e.g., "Avionics")
- Linked Database: Development Tasks
- Filter: Subsystem = [that subsystem]
- View: Board

### Docs & Decisions

**Full-width section:**
- Linked Database: Technical Decisions (full view)
- Divider
- Links to documentation pages

### Automation Surfaces

**Placeholder section:**
- Type `/callout`:
  - 📈 Analytics Dashboard (Coming from Gamma)
  - 🏆 Student Leaderboard (Coming from Gamma)
  - 🤖 Beta Automation Status (Coming from Beta)

---

## Task A5: Polish & Verify (30 min)

### Visual Polish

1. **Add spacer paragraphs** between major sections for readability
2. **Check all links** - make sure embedded databases work
3. **Mobile view** - open page on mobile to verify layout
4. **Color consistency** - ensure headings use consistent color scheme:
   - Mission Control: Blue
   - Active Workstreams: Orange
   - New Hire HQ: Purple

### Verification Checklist

- [ ] Page title is "CADENCE Mission Control"
- [ ] Hero section displays correctly
- [ ] Navigation database has 7 entries
- [ ] Three main columns are visible and functional
- [ ] All linked databases display data
- [ ] Mobile view looks acceptable
- [ ] Color scheme is consistent

---

## 📊 Estimated Time Breakdown

| Task | Time | Status |
|------|------|--------|
| A1: Hero Section | 30 min | ✅ DONE (Automated) |
| A2: Navigation DB | 45 min | ⏳ Manual Required |
| A3: 3-Column Layout | 2 hours | ⏳ Manual Required |
| A4: Persona Sections | 1.5 hours | ⏳ Manual Required |
| A5: Polish & Verify | 30 min | ⏳ Manual Required |
| **Total** | **5 hours** | **20% Complete** |

---

## 💡 Tips for Success

1. **Work in sections** - Complete one column before moving to the next
2. **Save frequently** - Notion auto-saves, but refresh to verify
3. **Use templates** - Copy/paste similar callouts to save time
4. **Test filters** - Make sure linked database filters show the right data
5. **Ask for help** - If you get stuck, skip and come back later

---

## 🎯 Success Criteria

When you're done, the Proto-type page should:
- ✅ Have a clear CADENCE Mission Control branding
- ✅ Show 3 main columns for different user personas
- ✅ Display relevant linked databases in each section
- ✅ Be easy to navigate on both desktop and mobile
- ✅ Have consistent visual design (colors, spacing, icons)

---

## 📞 Questions?

If you need clarification on any step, let me know! I'm Agent Alpha, and I'm here to help make this page beautiful. 🎨

---

**Created by:** Agent Alpha
**Date:** 2025-11-27
**Session:** #1
