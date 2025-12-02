# DEPRECATED

**This file is no longer canonical.**

**Replaced by:** canon/OPERATIONAL_ONTOLOGY.md
**Reason:** Superseded by operational ontology

**Archived:** 2025-12-01

---

# Team Lead Module Builder

## Critical Understanding

**Notion IS the Team Lead Module Builder** - there is NO separate web dashboard for Team Leads.

Team Leads use their existing Notion workspace to:

- Document real CubeSat missions and engineering work
- Create knowledge base pages from project experience
- Manage student interactions and team workflows
- Track project progress and deliverables

This is NOT being replaced with a separate React application.

## Why Notion Works as the Module Builder

### Team Lead Workflow Reality

Team Leads are already working in Notion daily for:

- **Real mission documentation** - documenting actual CubeSat projects
- **Student mentoring** - tracking student progress on real tasks
- **Knowledge capture** - turning project experience into reusable content
- **Team coordination** - managing cross-university collaboration

### Engineering Learning is Different

Engineering onboarding follows **project workflow**, not traditional step-by-step learning:

- Students need to understand what to know and WHEN based on project phase
- Learning is contextual to real engineering tasks
- Onboarding is difficult because engineering learning curves are steep
- Content must sync with typical project timelines, not arbitrary learning sequences

## The Real Module Creation Process

### NOT This (Wrong)

1. ❌ Team Lead logs into separate web app
2. ❌ Fills out forms to create module from scratch
3. ❌ Manually types content into structured fields
4. ❌ Publishes to students

### YES This (Correct)

1. ✅ Team Lead documents real mission work in Notion (already happening)
2. ✅ Alpha agent reads Team Lead Notion pages (via MCP/sync)
3. ✅ Alpha extracts relevant content for onboarding
4. ✅ Alpha structures content using OATutor pedagogical framework
5. ✅ Structured modules stored in database
6. ✅ Student LMS delivers modules with scaffolding/hints
7. ✅ Student progress syncs back to database → Notion for Team Lead visibility

## Data Flow

```text
Team Lead works in Notion (real missions, student mentoring)
         ↓
Notion content syncs to Database (bidirectional)
         ↓
Alpha extracts + structures content (OATutor framework)
         ↓
Database stores validated modules
         ↓
Student LMS delivers to students (React PWA)
         ↓
Student progress tracked in Database
         ↓
Analytics visible in Notion (for Team Leads) + Researcher Platform
```

## What Team Leads Actually Need

### Visibility (Not Creation Tools)

- See which students completed which modules
- View student progress on real project tasks
- Access analytics on learning outcomes
- Monitor team performance across universities

### Content Extraction Support (Not Manual Entry)

- Agents help extract onboarding content from their existing Notion docs
- Agents structure content using pedagogical frameworks
- Agents validate content meets learning objectives
- Team Leads review/approve, don't manually create

## Implications for Development

### Beta Agent (Applications)

- **Build**: Student Onboarding LMS (React PWA) only
- **Do NOT build**: Separate Team Lead web dashboard
- **Focus**: Mobile-first student experience consuming database modules

### Alpha Agent (Module Content)

- **Read**: Team Lead Notion pages via MCP server
- **Extract**: Relevant content for student onboarding
- **Structure**: Using OATutor pedagogical framework
- **Validate**: Content meets learning objectives before storing

### Gamma Agent (Infrastructure)

- **Bidirectional sync**: Notion ↔ Database (critical)
- **Analytics pipeline**: Database → Notion for Team Lead visibility
- **MCP integration**: Enable Alpha to read Notion content

## Understanding Team Lead Workflow First

Before designing student experience, we must understand:

1. How Team Leads currently work in Notion
2. What they document during real CubeSat projects
3. When students need specific knowledge (project phase alignment)
4. What content is reusable for onboarding vs project-specific

This is why simply building a web app was the wrong approach - it doesn't match how Team Leads actually work or how engineering learning actually happens.
