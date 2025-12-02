# React Notion X Integration Plan

**Agent Beta | December 1, 2025**

## Overview

This document details how **react-notion-x** complements **notionary** to provide complete Notion integration for FRAMES/Ascent Basecamp.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Notion Workspace                       │
│              (Foundation Templates)                      │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│              notionary (Backend)                         │
│  • Smart discovery by title                              │
│  • Fetch page content                                    │
│  • Extract markdown                                      │
│  • Read database schemas                                 │
└────────────┬───────────────────────┬────────────────────┘
             │                       │
             ▼                       ▼
    ┌────────────────┐      ┌──────────────────┐
    │  PostgreSQL    │      │  recordMap       │
    │  (existing)    │      │  (for frontend)  │
    └────────────────┘      └────────┬─────────┘
             │                       │
             ▼                       ▼
    ┌────────────────┐      ┌──────────────────┐
    │  Flask API     │      │  Flask API       │
    │  /api/teams    │      │  /api/notion/*   │
    │  (existing)    │      │  (new)           │
    └────────────────┘      └────────┬─────────┘
             │                       │
             ▼                       ▼
    ┌────────────────┐      ┌──────────────────┐
    │  React UI      │      │  react-notion-x  │
    │  (existing)    │      │  NotionRenderer  │
    └────────────────┘      └──────────────────┘
```

## Why Both Libraries?

### notionary (Backend)
- **Role**: Fetch data from Notion
- **Output**: Markdown, structured data, database schemas
- **Language**: Python (async/await)
- **Use Cases**:
  - Find pages by title
  - Extract template structures
  - Read database content
  - Sync to PostgreSQL

### react-notion-x (Frontend)
- **Role**: Render Notion content in React
- **Input**: recordMap (Notion's internal format)
- **Language**: TypeScript/React
- **Use Cases**:
  - Display module templates with full fidelity
  - Show Notion databases in React UI
  - Preview pages with proper formatting
  - Render code blocks, equations, embeds

## Frontend Integration

### Package Installation

```json
{
  "dependencies": {
    "react-notion-x": "^6.16.0",
    "notion-types": "^6.16.0",
    "prismjs": "^1.29.0",
    "katex": "^0.16.9"
  }
}
```

### Required CSS

```tsx
// In apps/research-analytics/src/App.tsx or _app.tsx
import 'react-notion-x/src/styles.css'
import 'prismjs/themes/prism-tomorrow.css'  // Code highlighting
import 'katex/dist/katex.min.css'           // Math equations
```

### Basic Component

```tsx
// apps/research-analytics/src/components/NotionViewer.tsx
import { NotionRenderer } from 'react-notion-x'
import type { ExtendedRecordMap } from 'notion-types'

interface NotionViewerProps {
  recordMap: ExtendedRecordMap
  rootPageId?: string
}

export function NotionViewer({ recordMap, rootPageId }: NotionViewerProps) {
  return (
    <NotionRenderer
      recordMap={recordMap}
      fullPage={false}
      darkMode={false}
      rootPageId={rootPageId}
    />
  )
}
```

### Advanced Component (Lazy Loading)

```tsx
// apps/research-analytics/src/components/NotionViewerFull.tsx
import dynamic from 'next/dynamic'  // or use React.lazy for Vite
import { NotionRenderer } from 'react-notion-x'
import type { ExtendedRecordMap } from 'notion-types'

// Lazy-load heavy components
const Code = dynamic(() =>
  import('react-notion-x/build/third-party/code').then(m => m.Code)
)
const Collection = dynamic(() =>
  import('react-notion-x/build/third-party/collection').then(m => m.Collection)
)
const Equation = dynamic(() =>
  import('react-notion-x/build/third-party/equation').then(m => m.Equation)
)
const Pdf = dynamic(() =>
  import('react-notion-x/build/third-party/pdf').then(m => m.Pdf),
  { ssr: false }
)
const Modal = dynamic(() =>
  import('react-notion-x/build/third-party/modal').then(m => m.Modal),
  { ssr: false }
)

interface NotionViewerFullProps {
  recordMap: ExtendedRecordMap
  rootPageId?: string
}

export function NotionViewerFull({ recordMap, rootPageId }: NotionViewerFullProps) {
  return (
    <NotionRenderer
      recordMap={recordMap}
      fullPage={true}
      darkMode={false}
      rootPageId={rootPageId}
      components={{
        Code,
        Collection,
        Equation,
        Pdf,
        Modal
      }}
    />
  )
}
```

## Backend Integration

### Converting notionary → recordMap

The backend needs to transform notionary data into the `recordMap` format that react-notion-x expects.

```python
# backend/notion_template_reader.py
from notionary import NotionPage
import json

async def fetch_page_as_recordmap(page_title: str) -> dict:
    """
    Fetch a Notion page and convert to react-notion-x recordMap format.
    
    Args:
        page_title: Title of Notion page (e.g., "Foundation")
    
    Returns:
        recordMap dict compatible with react-notion-x
    """
    page = await NotionPage.from_title(page_title)
    
    # notionary provides access to raw Notion API response
    # which contains the recordMap structure
    raw_data = await page.get_raw_notion_data()
    
    # Transform to recordMap format
    record_map = {
        "block": raw_data.get("block", {}),
        "collection": raw_data.get("collection", {}),
        "collection_view": raw_data.get("collection_view", {}),
        "collection_query": {},
        "notion_user": raw_data.get("notion_user", {}),
        "signed_urls": {}
    }
    
    return record_map

@app.route('/api/notion/page/<page_title>', methods=['GET'])
async def get_notion_page(page_title: str):
    """
    Flask endpoint to serve Notion page in react-notion-x format.
    """
    try:
        record_map = await fetch_page_as_recordmap(page_title)
        return jsonify(record_map), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
```

### Dual Output Services

Each service provides data in TWO formats:

```python
# backend/notion_data_display.py

class NotionDataService:
    """
    Provides Notion data in dual formats:
    1. PostgreSQL (for existing backend/analytics)
    2. recordMap (for React frontend rendering)
    """
    
    async def get_team_roster(self, team_id: str, output_format: str = 'postgres'):
        """
        Fetch team roster from Notion.
        
        Args:
            team_id: Team identifier
            output_format: 'postgres' or 'recordmap'
        
        Returns:
            Data in requested format
        """
        page = await NotionPage.from_title(f"Team {team_id} Roster")
        
        if output_format == 'postgres':
            # Transform to PostgreSQL format (existing logic)
            return await self._to_postgres(page)
        elif output_format == 'recordmap':
            # Transform to react-notion-x format
            return await self._to_recordmap(page)
        else:
            raise ValueError(f"Unknown format: {output_format}")
    
    async def _to_postgres(self, page: NotionPage) -> list[dict]:
        """Convert to PostgreSQL-compatible dicts."""
        # Extract student data, create dict for each row
        students = []
        # ... existing transformation logic ...
        return students
    
    async def _to_recordmap(self, page: NotionPage) -> dict:
        """Convert to react-notion-x recordMap."""
        raw_data = await page.get_raw_notion_data()
        return {
            "block": raw_data.get("block", {}),
            "collection": raw_data.get("collection", {}),
            "collection_view": raw_data.get("collection_view", {}),
            "collection_query": {},
            "notion_user": raw_data.get("notion_user", {}),
            "signed_urls": {}
        }

# Flask routes
@app.route('/api/notion/team/<team_id>/roster', methods=['GET'])
async def get_team_roster_for_display(team_id: str):
    """Return recordMap for React rendering."""
    service = NotionDataService()
    record_map = await service.get_team_roster(team_id, output_format='recordmap')
    return jsonify(record_map), 200

@app.route('/api/notion/team/<team_id>/sync', methods=['POST'])
async def sync_team_roster_to_db(team_id: str):
    """Sync to PostgreSQL (existing flow)."""
    service = NotionDataService()
    students = await service.get_team_roster(team_id, output_format='postgres')
    
    # Insert into PostgreSQL students table
    for student_data in students:
        student = StudentModel(**student_data)
        db.session.add(student)
    db.session.commit()
    
    return jsonify({"synced": len(students)}), 200
```

## Frontend Usage Examples

### Module Template Preview

```tsx
// apps/research-analytics/src/pages/ModuleBuilder.tsx
import { useState, useEffect } from 'react'
import { NotionViewerFull } from '../components/NotionViewerFull'

export function ModuleBuilder() {
  const [recordMap, setRecordMap] = useState(null)
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    // Fetch Foundation template
    fetch('/api/notion/page/Foundation')
      .then(res => res.json())
      .then(data => {
        setRecordMap(data)
        setLoading(false)
      })
  }, [])
  
  if (loading) return <div>Loading template...</div>
  
  return (
    <div className="module-builder">
      <h1>Foundation Module Template</h1>
      <NotionViewerFull recordMap={recordMap} />
    </div>
  )
}
```

### Team Roster Display

```tsx
// apps/research-analytics/src/pages/TeamRoster.tsx
import { useState, useEffect } from 'react'
import { NotionViewerFull } from '../components/NotionViewerFull'

export function TeamRoster({ teamId }: { teamId: string }) {
  const [recordMap, setRecordMap] = useState(null)
  
  useEffect(() => {
    fetch(`/api/notion/team/${teamId}/roster`)
      .then(res => res.json())
      .then(setRecordMap)
  }, [teamId])
  
  if (!recordMap) return <div>Loading...</div>
  
  return (
    <div className="team-roster">
      <h2>Team {teamId} Roster</h2>
      {/* Full Notion database rendering with Collections support */}
      <NotionViewerFull recordMap={recordMap} />
    </div>
  )
}
```

## Supported Block Types

react-notion-x supports **all** Notion block types:

### Basic Blocks
- ✅ Text with formatting (bold, italic, code, links)
- ✅ Headings (H1, H2, H3)
- ✅ Lists (bulleted, numbered, to-do)
- ✅ Quotes, Callouts, Toggles
- ✅ Dividers

### Rich Media
- ✅ Images (with zoom)
- ✅ Videos (YouTube, Vimeo, etc.)
- ✅ PDFs (embedded viewer)
- ✅ Audio files
- ✅ File attachments

### Advanced Blocks
- ✅ Code blocks (syntax highlighting via Prism)
- ✅ Equations (KaTeX rendering)
- ✅ Databases (tables, galleries, boards, calendars)
- ✅ Embeds (Figma, Miro, Google Maps, etc.)
- ✅ Table of Contents

### Databases/Collections
- ✅ Table view
- ✅ Gallery view
- ✅ Board view (Kanban)
- ✅ List view
- ✅ Calendar view

## Implementation Timeline

### Phase 1: Setup (1 hour)
1. Install react-notion-x packages in `apps/research-analytics/`
2. Add CSS imports
3. Create basic `NotionViewer` component
4. Test with hardcoded recordMap

### Phase 2: Backend Transform (2 hours)
1. Research notionary's raw data access
2. Build recordMap conversion utility
3. Create `/api/notion/page/<title>` endpoint
4. Test with Foundation template

### Phase 3: Advanced Component (1 hour)
1. Create `NotionViewerFull` with lazy-loaded components
2. Test Code, Collection, Equation rendering
3. Optimize bundle size

### Phase 4: Integration (2 hours)
1. Add to Team Lead Module Builder
2. Add to Researcher Platform (template preview)
3. Test with real Notion content

### Phase 5: Dual Format Services (2 hours)
1. Update existing sync services to support both formats
2. Maintain PostgreSQL flow (no breaking changes)
3. Add recordMap endpoints for React

**Total: ~8 hours**

## Dependencies

### Backend
```txt
# requirements.txt
notionary>=0.1.0
flask>=3.0.0
sqlalchemy>=2.0.0
```

### Frontend (research-analytics)
```json
{
  "dependencies": {
    "react": "^18.0.0",
    "react-notion-x": "^6.16.0",
    "notion-types": "^6.16.0",
    "prismjs": "^1.29.0",
    "katex": "^0.16.9"
  }
}
```

## Benefits

### For Team Leads
- **Full-fidelity preview**: See templates exactly as in Notion
- **Rich content**: Code examples, equations, embedded videos
- **Database views**: Tables, galleries, boards render natively

### For Researchers
- **Template validation**: Preview before cloning to student workspaces
- **Analytics dashboards**: Display Notion data with proper formatting
- **Documentation**: Rich module content with all Notion features

### For Developers (Us)
- **No HTML parsing**: react-notion-x handles rendering
- **Type safety**: Full TypeScript support via notion-types
- **Lazy loading**: Heavy components load on-demand
- **Maintained**: Active library with regular updates

## Safety Constraints

- ✅ **Read-only first**: Start with display, no writes
- ✅ **No page creation**: Agent Beta forbidden from creating Notion pages
- ✅ **Template analysis**: Focus on understanding existing structure
- ✅ **PostgreSQL primary**: Notion is supplementary data source
- ✅ **Explicit transforms**: Clear PostgreSQL ↔ recordMap conversions

## Next Steps

1. **Human approval**: Review this integration plan
2. **Install libraries**: Backend (notionary) + Frontend (react-notion-x)
3. **Test basic rendering**: Hardcoded recordMap → NotionRenderer
4. **Build transform utility**: notionary → recordMap converter
5. **Create dual-format services**: Support both PostgreSQL and React needs

---

**Status**: 📋 Planning complete, awaiting approval to proceed

**Related Documents**:
- `NOTION_CLEANUP_AND_MIGRATION_PLAN.md` - Full cleanup strategy
- `NOTION_CLEANUP_CHECKLIST.md` - Step-by-step tracking
- `AGENT_BETA_NOTION_REPORT.md` - Executive summary
