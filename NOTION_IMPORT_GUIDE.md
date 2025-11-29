# 🚀 Notion Module Import Guide

## ✅ What You Have

**CSV File Created:** `data/projects/CADENCE/notion_modules_categorized.csv`

**Contains:** 68 training modules organized into 6 categories
- 🚀 Getting Started: 10 modules
- 💻 Software Development: 27 modules
- ⚡ Hardware & Subsystems: 16 modules
- 🛰️ Mission Design & Analysis: 9 modules
- 🔧 Systems Engineering: 6 modules

**Each module includes:**
- Title, Description, Category
- Target Audience (All/Undergraduate/Graduate)
- Discipline (Software/Electrical/Aerospace/Systems/All)
- Estimated Minutes
- Difficulty (Beginner/Intermediate/Advanced)
- Source Type (Markdown/PDF)
- Source File name
- Tags (searchable keywords)
- Prerequisites (learning path)

---

## 📋 How to Import into Notion

### **Option 1: Create New Database (Recommended)**

**Step 1: Create Database**
1. Open your Notion template
2. Click where you want the database
3. Type `/database` and select "Table - Full page"
4. Name it: "Module Library" or "Training Modules"

**Step 2: Import CSV**
1. In the new database, click "..." (top right)
2. Select "Merge with CSV"
3. Click "Choose a file"
4. Upload: `data/projects/CADENCE/notion_modules_categorized.csv`
5. Preview shows all 68 rows
6. Click "Import"

**Result:** Instant 68 modules with all properties! 🎉

---

### **Option 2: Add to Existing Database**

If your template already has a module database:

**Step 1: Open Database**
1. Navigate to existing module database in template
2. Click "..." menu

**Step 2: Merge CSV**
1. Select "Merge with CSV"
2. Upload: `notion_modules_categorized.csv`
3. **Map columns** to existing properties:
   - CSV "Title" → Database "Title"
   - CSV "Category" → Database "Category"
   - etc.
4. Choose: "Merge" (adds new rows) or "Replace" (replaces all)
5. Click "Import"

**Result:** Modules added to existing structure! 🎉

---

## 🎨 Set Up Category Views

After importing, create filtered views for each category:

### **View 1: Getting Started (🚀)**
1. In database, click "+ New view" → Gallery
2. Name: "Getting Started"
3. Filter: Category = "Getting Started"
4. Sort: Difficulty (Beginner first), then Estimated Minutes
5. Layout: Cards with cover images

### **View 2: Software Development (💻)**
1. "+ New view" → Table
2. Name: "Software Development"
3. Filter: Category = "Software Development"
4. Group by: Difficulty
5. Sort: Tags (alphabetical)

### **View 3-6: Repeat for other categories**
- Hardware & Subsystems (⚡)
- Mission Design & Analysis (🛰️)
- Systems Engineering (🔧)

---

## 🔗 Link Image Buttons to Category Views

### **Step 1: Get View URLs**
1. Open "Getting Started" view
2. Click "..." → "Copy link to view"
3. Paste somewhere to save
4. Repeat for all 6 category views

### **Step 2: Update Image Buttons**
1. Go back to your template homepage
2. Click first image button (edit mode)
3. Select the image/button
4. Click "Link" icon
5. Paste the "Getting Started" view URL
6. Change button text: "🚀 Getting Started"
7. Upload icon (rocket emoji or image)

**Repeat for all 6 buttons:**
- Button 1: 🚀 Getting Started
- Button 2: 💻 Software Development
- Button 3: ⚡ Hardware & Subsystems
- Button 4: 🛰️ Mission Design
- Button 5: 🔧 Systems Engineering
- Button 6: 📚 Advanced Topics

---

## 📊 Create Learning Paths

Use the "Prerequisites" column to create guided paths:

### **Software Engineer Path:**
```
1. New Recruits (no prereqs)
2. GitHub Guide (after New Recruits)
3. Software Overview (after GitHub)
4. F-Prime Tutorials (after Software Overview)
5. EAT Software Design (after F-Prime)
```

**To visualize:**
1. Create view: "Software Learning Path"
2. Filter: Discipline contains "Software"
3. Sort: By prerequisites (manual ordering)
4. Add Timeline view showing progression

---

## 🎯 Add to Sidebar Quick Links

**Update your template sidebar:**

```markdown
## 📍 Start Here
- [New Recruits Onboarding](#link-to-module)
- [GitHub Guide](#link-to-module)
- [UNP Nanosatellite User Guide](#link-to-module)

## 💻 Popular Software
- [F-Prime Tutorials](#link-to-module)
- [EAT Software Design Notes](#link-to-module)
- [How to Run scales-software](#link-to-module)

## ⚡ Essential Hardware
- [NASA Power Systems Guide](#link-to-module)
- [Avionics Onboarding](#link-to-module)

## 🎓 Must-Read PDFs
- [UNP Mission Design Course](#link-to-module)
- [GMAT Users Guide](#link-to-module)
- [Systems Engineering Series](#link-to-view)
```

---

## 🔍 Enable Smart Search

Add database properties for powerful searching:

### **Tags Column:**
Already populated with keywords like:
- `github`, `f-prime`, `nasa`, `gmat`
- `power`, `comms`, `avionics`, `testing`
- `architecture`, `design`, `documentation`

**To search:**
1. Database view → Add filter
2. "Tags contains [keyword]"
3. Find all modules on a topic instantly

### **Full-Text Search:**
1. Click search bar in database
2. Type: "power systems"
3. Searches titles, descriptions, tags

---

## 📅 Add to Calendar

Use the calendar embed in your template:

**Create Timeline View:**
1. In Module Library database
2. "+ New view" → Timeline
3. Date property: Add "Recommended Completion Date"
4. Group by: Category
5. Color-code by Difficulty

**Add to Template Calendar:**
1. Copy timeline view link
2. Paste as `/embed` in your template's calendar section
3. Shows when students should complete modules

---

## 🎨 Customize Module Pages

For each module row, you can:

### **Add Rich Content:**
1. Click module title → Opens full page
2. Paste markdown content from `data/projects/CADENCE/markdown/[file].md`
3. Format with:
   - Headings (`/heading`)
   - Callouts (`/callout`)
   - Code blocks (`/code`)
   - Toggle lists (`/toggle`)

### **Add Cover Images:**
1. Hover over module row
2. Click "..." → "Add cover"
3. Upload space-themed image or use Unsplash
4. Suggested searches: "rocket", "satellite", "circuit board"

### **Link to PDFs:**
For PDF modules:
1. Upload PDF to Google Drive
2. Get shareable link
3. Add to module page: `/link` or `/file`
4. Or embed: `/embed [Drive link]`

---

## ✅ Quick Checklist

**After Import:**
- [ ] 68 modules imported successfully
- [ ] 6 category views created (Gallery/Table)
- [ ] Image buttons linked to category views
- [ ] Sidebar quick links updated
- [ ] Tags working for search
- [ ] At least 5 module pages populated with content
- [ ] PDFs uploaded and linked

**Test It:**
- [ ] Click image button → Takes you to filtered category
- [ ] Click module row → Opens full page
- [ ] Search "github" → Finds all GitHub modules
- [ ] Prerequisites show learning path
- [ ] Quick links in sidebar work

---

## 🚀 Next Steps

### **Week 1: Structure (You Are Here!)**
- ✅ CSV created with 68 modules
- Import into Notion database
- Set up category views
- Link image buttons

### **Week 2: Content Population**
- Copy markdown files into top 10 module pages
- Upload PDFs to Google Drive
- Link PDFs in module pages
- Add cover images

### **Week 3: Enhancement**
- Create learning path views
- Add progress tracking
- Set up calendar timeline
- Add welcome message

### **Week 4: Launch**
- Test with 1-2 pilot students
- Get feedback
- Refine categories if needed
- Roll out to full cohort

---

## 💡 Pro Tips

**Color-Coding:**
- Getting Started: Blue
- Software: Green
- Hardware: Orange
- Mission Design: Purple
- Systems Eng: Red
- Advanced: Gray

**Icon Strategy:**
- Use emoji in titles for visual scanning
- Or upload custom icons for each category
- Keep consistent across template

**Mobile-Friendly:**
- Gallery view works best on mobile
- Keep descriptions concise (< 100 chars)
- Use tags for filtering on small screens

**Automation Ideas:**
- Notion API to sync with GitHub (future)
- Auto-assign modules based on student role
- Track completion with checkbox property

---

## 📞 Troubleshooting

**Import Failed?**
- Check CSV encoding (should be UTF-8)
- Open in Excel/Sheets, verify no corrupted rows
- Try importing 10 rows at a time to find issue

**Categories Not Showing?**
- Verify "Category" column is type: Select
- Check spelling matches exactly
- Create select options manually if needed

**Links Not Working?**
- Make sure you copied "link to view" not "link to page"
- Views must be in same workspace
- Try duplicating template to same workspace

**Missing Content?**
- Source files in: `data/projects/CADENCE/markdown/`
- PDFs listed in: `data/projects/CADENCE/useful_pdfs.json`
- Copy-paste content manually if needed

---

## 🎉 You're Ready!

Your Notion workspace now has:
- ✅ 68 organized training modules
- ✅ 6 intuitive categories
- ✅ Smart filtering and search
- ✅ Learning paths via prerequisites
- ✅ Professional dashboard with working navigation

**Time to import:** 5 minutes
**Time to set up views:** 15 minutes
**Time to populate content:** 2-4 hours (do over time)

**GO FOR IT! 🚀**
