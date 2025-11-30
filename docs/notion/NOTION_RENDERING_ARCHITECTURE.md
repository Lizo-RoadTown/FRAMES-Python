# Notion Rendering Architecture

**Last Updated:** November 26, 2025  
**Critical:** ALL agents working on Notion integration must read this first

---

## 🎯 Core Concept

**We DO NOT show users raw Notion pages.** Instead:

1. Content creators use Notion (easy, visual interface)
2. We fetch content via Notion API
3. **We render it beautifully in React using react-notion-x**
4. Users see our custom-styled, dark-mode, space-tech themed pages

---

## 📦 Key Library: react-notion-x

**Location:** `react-notion-x-master.zip` (extracted to `react-notion-x-master/`)

**What it does:**
- Fetches Notion pages via API
- Renders them as React components
- 10-100x faster than native Notion
- Full dark mode support
- Custom styling capability

**Documentation:** See `react-notion-x-master/readme.md`

**DO NOT DELETE THIS ZIP FILE** - It's the foundation of our Notion rendering strategy.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTENT CREATION LAYER                   │
│                         (Notion)                            │
│                                                             │
│  Team leads create content in Notion:                      │
│  • Module Library database (LMS modules)                   │
│  • Project management pages (internal use)                 │
│  • Documentation pages                                     │
│                                                             │
│  Benefits: Visual editing, collaboration, no Git needed    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Notion API
                           │ (notion-client npm package)
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                     FETCH & TRANSFORM                       │
│                    (Node.js/Python)                         │
│                                                             │
│  const notion = new NotionAPI()                            │
│  const recordMap = await notion.getPage(pageId)            │
│                                                             │
│  Store in: GitHub (version control) or PostgreSQL (cache)  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Pass recordMap to React
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                    RENDERING LAYER                          │
│                (React + react-notion-x)                     │
│                                                             │
│  import { NotionRenderer } from 'react-notion-x'           │
│                                                             │
│  <NotionRenderer                                           │
│    recordMap={recordMap}                                   │
│    darkMode={true}                                         │
│    fullPage={true}                                         │
│    components={{                                           │
│      // Custom components with space-tech theme            │
│      Code,                                                 │
│      Collection,                                           │
│      Equation,                                             │
│      Pdf                                                   │
│    }}                                                      │
│  />                                                        │
│                                                             │
│  Styled with: /frontend/static/space-tech.css             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                       USER SEES                             │
│                                                             │
│  Beautiful, fast, dark-mode pages with:                    │
│  • Custom space-tech theme (cyan/purple accents)           │
│  • Smooth animations                                       │
│  • Optimized performance                                   │
│  • Branded experience                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Styling Strategy

### CSS Files to Import (in React app):

```tsx
// Required: Core react-notion-x styles
import 'react-notion-x/src/styles.css'

// Optional: Syntax highlighting
import 'prismjs/themes/prism-tomorrow.css'

// Optional: Math equations
import 'katex/dist/katex.min.css'

// FRAMES custom theme override
import '/static/space-tech.css'  // Our dark space theme
```

### Custom Theme Variables (space-tech.css):

```css
:root {
  --notion-bg-primary: #0a0a0f;      /* Override Notion's white bg */
  --notion-bg-secondary: #0d1117;
  --notion-text-primary: #e6edf3;    /* Light text for dark mode */
  --notion-accent: #00f0ff;          /* Cyan accent */
  --notion-purple: #8b5cf6;          /* Purple accent */
}
```

---

## 📋 Content Types & Use Cases

### 1. **LMS Modules** (Student-facing)
- **Source:** Module Library database in Notion
- **Flow:** Notion → API → GitHub JSON → PostgreSQL → React render
- **Why:** Team leads create content easily, students see beautiful pages
- **Implementation:** See `docs/lms/MODULE-DATA-ARCHITECTURE.md`

### 2. **Project Management** (Internal)
- **Source:** Notion databases (Tasks, Decisions, Integrations)
- **Flow:** Notion → API → React admin dashboard
- **Why:** Solo developer needs easy project tracking
- **Implementation:** TBD - can stay in Notion or render in custom dashboard

### 3. **Documentation** (Developer-facing)
- **Source:** Notion pages (synced from GitHub `/docs`)
- **Flow:** Bidirectional sync: GitHub ↔ Notion → React render
- **Why:** Write in Markdown (GitHub) or Notion, render beautifully
- **Implementation:** See `NOTION_GITHUB_INTEGRATION_SETUP.md`

---

## 🔧 Implementation Requirements

### Node.js Dependencies:
```json
{
  "dependencies": {
    "notion-client": "^6.16.0",
    "react-notion-x": "^7.0.0",
    "prismjs": "^1.29.0",
    "katex": "^0.16.0"
  }
}
```

### Python Dependencies:
```txt
notion-client==2.2.1  # For Python scripts (export, sync)
```

### Integration Points:
1. **Flask Backend:** Serves React app with Notion content
2. **React Frontend:** Renders Notion via react-notion-x
3. **PostgreSQL:** Caches rendered content (optional)
4. **GitHub:** Version control for exported Notion content

---

## 📁 File Organization

```
FRAMES Python/
├── react-notion-x-master/          ← THE LIBRARY (DO NOT DELETE)
│   ├── packages/                   ← Core packages
│   ├── examples/                   ← Reference implementations
│   └── readme.md                   ← Documentation
│
├── frontend/
│   ├── components/
│   │   └── NotionPage.jsx          ← Custom wrapper for NotionRenderer
│   ├── static/
│   │   ├── space-tech.css          ← Our dark theme
│   │   └── notion-overrides.css    ← Notion-specific overrides
│   └── templates/
│       └── module.html             ← Module display template
│
├── scripts/
│   ├── export_modules_from_notion.py    ← Notion → GitHub
│   ├── deploy_modules_to_db.py          ← GitHub → PostgreSQL
│   └── fetch_notion_page.js             ← Notion API helper
│
└── docs/
    ├── NOTION_RENDERING_ARCHITECTURE.md  ← This file
    └── lms/
        └── MODULE-DATA-ARCHITECTURE.md   ← Module content flow
```

---

## ⚠️ Critical Rules for Agents

### ✅ DO:
- Use react-notion-x to render Notion content
- Apply space-tech dark theme to all Notion renders
- Cache Notion content in PostgreSQL for performance
- Version control exported Notion content in GitHub
- Keep content creation in Notion (team-friendly)

### ❌ DON'T:
- Show users raw Notion pages directly
- Delete or move `react-notion-x-master.zip`
- Ignore dark mode requirement
- Bypass the rendering layer
- Store sensitive student data in Notion

---

## 🚀 Quick Start for Agents

**When asked to work with Notion content:**

1. Check if content exists in Notion (Module Library, etc.)
2. Use `notion-client` to fetch via API
3. Pass to `react-notion-x` NotionRenderer component
4. Apply `darkMode={true}` and custom CSS
5. Integrate with existing Flask/React app

**Example Component:**

```tsx
import { NotionRenderer } from 'react-notion-x'
import { Code } from 'react-notion-x/build/third-party/code'
import { Collection } from 'react-notion-x/build/third-party/collection'

export function ModulePage({ recordMap }) {
  return (
    <div className="notion-page-wrapper">
      <NotionRenderer
        recordMap={recordMap}
        fullPage={true}
        darkMode={true}
        components={{
          Code,
          Collection,
          // Add other heavy components as needed
        }}
      />
    </div>
  )
}
```

---

## 📚 Related Documentation

- **react-notion-x README:** `react-notion-x-master/readme.md`
- **Module Architecture:** `docs/lms/MODULE-DATA-ARCHITECTURE.md`
- **Notion Integration Setup:** `NOTION_GITHUB_INTEGRATION_SETUP.md`
- **Space-tech Theme:** `frontend/static/space-tech.css`

---

## 🎯 Current Status (Nov 26, 2025)

- ✅ react-notion-x library downloaded and extracted
- ✅ Space-tech dark theme exists (`space-tech.css`)
- ✅ PostgreSQL schema for modules exists (`shared/database/db_models.py`)
- ✅ Notion workspace structure defined
- ❌ React components for Notion rendering (TODO)
- ❌ Notion API fetching scripts (TODO)
- ❌ Integration with Flask backend (TODO)

**Next Steps:**
1. Create NotionPage React component
2. Write Notion API fetch scripts
3. Integrate into module display flow
4. Apply custom CSS overrides
