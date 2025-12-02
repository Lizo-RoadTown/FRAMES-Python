# DEPRECATED

**This file is no longer canonical.**

**Replaced by:** canon/system_overview_v_2.md
**Reason:** V1 ontology caused architectural confusion among agents

**Archived:** 2025-12-01

---

# System Overview

FRAMES / Ascent Basecamp is a unified ecosystem built on:

- One PostgreSQL database (Neon)
- Two user-facing applications + Notion workspace
- Embedded agent swarm (partitioned)
- Bidirectional Notion sync (critical infrastructure)
- OATutor-derived pedagogical framework

## Applications & Workspaces

### 1. Team Lead Workspace (Notion)

**Primary workspace for Team Leads** documenting real CubeSat missions and engineering work.

- **NOT being replaced** by a separate web app
- Contains living engineering documentation, student interactions, project data
- Team Leads work here daily on active projects
- Source material for module content extraction

### 2. Student Onboarding LMS (React PWA)

Mobile-first progressive web app for student training.

- Consumes module content extracted from Team Lead Notion workspace
- Uses OATutor pedagogical framework for scaffolding/hints
- Syncs student progress back to database
- **Purpose**: Engineering onboarding aligned with real project workflow

### 3. Researcher Platform (Jupyter/Analytics)

Advanced analytics + AI prediction tools.

- Visual analytics dashboards
- ML experiment management
- Prediction API

## Data Flow Architecture

```text
Team Lead Notion Workspace (living docs, real missions)
         ↕ (bidirectional sync)
PostgreSQL Database (Neon) - single source of truth
         ↕
Student LMS (React) + Researcher Platform (Analytics)
```

**Key Points**:

- Old Notion data is in database, needs to sync to NEW Notion workspace
- Bidirectional sync preserves Team Lead workflow
- Module content sources from Team Lead Notion → Database → Student LMS
- Student progress flows back: Student LMS → Database → Notion analytics

## Core Principles

- Single source of truth (PostgreSQL)
- Notion is Team Lead workspace (not optional, not being replaced)
- Clear boundaries between applications
- Deterministic agent interfaces
- No auto‑creation of new structures without approval
- Engineering learning follows project workflow (not traditional step-by-step)
