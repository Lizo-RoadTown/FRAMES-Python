# DEPRECATED

**This file is no longer canonical.**

**Replaced by:** canon/Notion_Interface_layer.md
**Reason:** Old conceptual framing of Notion's role

**Archived:** 2025-12-01

---

# Notion Integration Overview

## Critical Understanding

**Notion IS the Team Lead workspace** - it is NOT being replaced by a web application.

Team Leads work in Notion daily to:

- Document real CubeSat missions and engineering work
- Track student interactions and progress
- Maintain living project documentation
- Create knowledge base content from real missions
- Manage team/project workflows

## Role in System Architecture

Notion serves as the **primary workspace for Team Leads**, not just a data export destination.

### Data Flow

```text
Team Lead Notion Workspace (living engineering docs)
         ↕ (BIDIRECTIONAL sync - critical infrastructure)
PostgreSQL Database (single source of truth)
         ↓ (one-way)
Student LMS (consumption only)
```

### Why Bidirectional Sync is Necessary

- **Old Notion data exists in database** - needs to sync TO new Notion workspace
- **Team Leads work in Notion** - their updates need to sync TO database
- **Preserves existing workflows** - Team Leads shouldn't change how they work
- **Enables real-time visibility** - Database reflects current Notion state
- **Powers module creation** - Modules extract content from Team Lead Notion workspace

## Module Content Sourcing

Modules are NOT created from scratch. They are extracted from:

1. Team Lead Notion documentation (real mission content)
2. Existing CADENCE project materials (historical data)
3. Team Lead knowledge base pages (domain expertise)

This content is then:

- Structured using OATutor pedagogical framework
- Formatted for student consumption
- Enhanced with scaffolding, hints, and validation
- Delivered through Student LMS

## Technical Implementation

### Sync Service Requirements

- Must preserve existing Notion page structure (no overwrites)
- Must handle conflicts gracefully (log, don't auto-resolve)
- Must sync in both directions (Notion ↔ Database)
- Must respect Notion's rate limits
- Must maintain data integrity

### MCP Integration

- Use Notion MCP server for API access
- Use notionary library for Python integration
- Sync coordination via `ascent_basecamp_agent_log` table

## Key Rules

- Agents may NOT create new Notion pages without user approval
- Agents may NOT overwrite existing Notion content without validation
- All module generation must extract from existing Team Lead content
- Bidirectional sync is REQUIRED infrastructure (not optional)
- react-notion-x may be used for rendering Notion content inside the LMS

## What This Means for Each Agent

### Alpha (Module Content)

- Read Team Lead Notion pages for source material
- Extract content using OATutor framework
- Do NOT create modules from scratch - use Team Lead docs
- Coordinate with Gamma for sync service access

### Beta (Applications)

- Student LMS consumes database content (sourced from Notion)
- Do NOT build separate Team Lead web app (Notion is their workspace)
- Focus on student-facing React PWA only

### Gamma (Infrastructure)

- Bidirectional Notion sync is CRITICAL infrastructure work
- Must sync old database data TO new Notion workspace
- Must sync Team Lead Notion updates TO database
- Coordinate logging to prevent conflicts
