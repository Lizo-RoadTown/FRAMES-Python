# Three-Branch Agent Work Plan
**Date:** November 30, 2025  
**Status:** Awaiting Human Approval  
**Context:** Canon documentation refresh + Notion integration fixes

---

## Executive Summary

After comprehensive canon review, Agent Beta has identified critical system alignment issues requiring coordinated three-agent response:

1. **Notion Integration Crisis:** Agents creating new pages instead of filling premade templates → unusable page proliferation
2. **Module Obsolescence:** 65+ modules use pre-canon terminology, need review/remake with human guidance
3. **Coordination Gap:** Need non-interfering parallel work streams

**Solution:** Three specialized branches working simultaneously with strict resource boundaries.

---

## Critical Context

### Canon Documentation Changes
- Project renamed: "FRAMES / Ascent Basecamp"
- Three distinct applications clarified: Student LMS, Team Lead Module Builder, Researcher Platform
- Single PostgreSQL database (Neon) as shared truth
- Strict agent safety rules: NO page creation without approval
- Template-based approach: Fill existing structures, don't create new ones

### Current State Assessment

**✅ Working:**
- Backend LMS API: 8 endpoints implemented
- React frontend: Dashboard + ModulePlayer scaffolded
- Database connection configured
- 82 modules created by Alpha

**⚠️ Needs Attention:**
- Backend import errors (models.py)
- Modules use outdated terminology
- Notion sync creating unwanted pages
- Templates exist but not being used correctly

**🔴 Critical Blockers:**
- Premade template structure unknown
- Module terminology mapping unclear
- Page creation audit needed

---

## Branch 1: Agent Alpha — Module Content Architect

### Primary Mission
Review existing modules against canon, create terminology mapping, prepare for human-approved remake.

### Resource Claims
- **Read:** `modules/enhanced/*.json` (all existing modules)
- **Read:** `/canon/*.md` (reference for terminology)
- **Write:** `docs/modules/MODULE_ANALYSIS_REPORT.md` (new analysis doc)
- **Write:** `modules/*` (only after human approval)
- **Database:** `modules` table (read for analysis, write only after approval)

### Non-Interference Protocol
- ✅ Can work in modules directory
- ✅ Can read canon docs
- ✅ Can create analysis documents
- ❌ Cannot modify backend code
- ❌ Cannot modify frontend code
- ❌ Cannot run infrastructure scripts
- ❌ Cannot create/modify Notion pages

### Phase 1: Analysis (No Human Approval Needed)
**Duration:** 2-3 hours

1. **Terminology Mapping**
   - Read all canon docs to extract official terminology
   - Read all 65+ module JSONs to extract current terminology
   - Create mapping document: OLD_TERM → NEW_TERM
   - Flag ambiguous cases for human review
   
2. **Module Classification**
   - Category A: Can be updated with simple term replacement
   - Category B: Needs partial restructure (content salvageable)
   - Category C: Complete remake required (obsolete concepts)
   - Category D: Perfect alignment (no changes needed)
   
3. **Subsystem Structure Analysis**
   - Extract canon-approved subsystems from `STUDENT_LMS.md`
   - Map existing modules to subsystems
   - Identify gaps in subsystem coverage
   - Propose new module structure aligned with competency levels:
     * Orientation modules (intro to subsystem)
     * Competency modules (core skills)
     * Integration modules (cross-subsystem)
     * Autonomy modules (advanced/leadership)

4. **Ghost Cohort Metadata Review**
   - Check which modules have race metadata
   - Propose ghost cohort data structure for missing modules
   - Coordinate with Gamma on data availability

**Deliverable:** `docs/modules/MODULE_ANALYSIS_REPORT.md` containing:
- Complete terminology mapping
- Module classification table (65+ rows)
- Subsystem coverage matrix
- Recommended actions for each module
- Human decision points flagged

### Phase 2: Human Review & Approval (BLOCKED until human input)
**Duration:** Human-dependent

Alpha waits for human to:
- Review analysis report
- Approve terminology changes
- Clarify ambiguous cases
- Give go/no-go for each module category

### Phase 3: Module Remake (After Human Approval)
**Duration:** 5-10 hours

1. **Category A Updates** (Simple replacements)
   - Automated term replacement
   - Verify JSON schema compliance
   - Update database entries
   
2. **Category B Restructure** (Partial remake)
   - Preserve salvageable content
   - Restructure to canon format
   - Add missing competency metadata
   - Add ghost cohort compatibility
   
3. **Category C Recreation** (Full remake)
   - Start from scratch using canon guidelines
   - Align with subsystem structure
   - Include all required metadata
   - Add race mode features

4. **New Module Creation** (Fill gaps)
   - Create missing orientation modules
   - Build prerequisite chains
   - Ensure competency progression

**Deliverable:** Updated module library with canon-compliant terminology and structure

---

## Branch 2: Agent Beta — Platform Integration Specialist

### Primary Mission
Fix backend issues, learn Notion template structure (read-only), integrate LMS with real data.

### Resource Claims
- **Read/Write:** `backend/app.py`, `backend/lms_routes.py` (fix bugs, test)
- **Read/Write:** `frontend-react/*` (enhance integration)
- **Read Only:** Notion workspace (learn template structure, NO CREATION)
- **Read:** Database (test queries)
- **Write:** `backend/notion_template_service.py` (new service for filling templates)
- **Write:** `docs/notion/TEMPLATE_STRUCTURE_ANALYSIS.md` (documentation)

### Non-Interference Protocol
- ✅ Can modify backend code
- ✅ Can modify frontend code
- ✅ Can read Notion templates (with human guidance on access)
- ✅ Can test database queries
- ❌ Cannot modify modules content
- ❌ Cannot run infrastructure deployment scripts
- ❌ Cannot create Notion pages (read-only access only)

### Phase 1: Backend Stabilization (No Approval Needed)
**Duration:** 1-2 hours

1. **Fix Import Issues**
   - Resolve `models.py` import error in `backend/app.py`
   - Ensure proper module structure
   - Test Flask app startup
   
2. **Database Connection Validation**
   - Verify Neon connection string
   - Test all tables exist
   - Check agent coordination tables (agent_log, technical_decisions, error_log)
   - Create missing tables if needed (coordinate with Gamma)
   
3. **API Endpoint Testing**
   - Run `backend/test_lms_endpoints.py`
   - Fix any failures
   - Test with real database data
   - Document any missing database tables

**Deliverable:** Fully functional backend with passing tests

### Phase 2: Notion Template Analysis (BLOCKED until human grants access)
**Duration:** 2-3 hours

1. **Human Coordination**
   - Request Notion workspace access
   - Request specific template locations
   - Understand which template serves which purpose
   
2. **Template Structure Documentation**
   - Read each template (no modifications)
   - Document database schema/properties
   - Document expected data types
   - Document relationship fields
   - Create mapping: DATABASE_TABLE → NOTION_TEMPLATE
   
3. **Template Filling Strategy**
   - Design service that queries database and fills template
   - No page creation, only property updates
   - Respect template structure exactly
   - Build validation to prevent structure changes

**Deliverable:** `docs/notion/TEMPLATE_STRUCTURE_ANALYSIS.md` + design for template-filling service

### Phase 3: Notion Integration Service (After Template Analysis)
**Duration:** 3-4 hours

1. **Create Template Service**
   - New file: `backend/notion_template_service.py`
   - Functions to read database
   - Functions to format data for Notion properties
   - Functions to update existing pages (NO creation)
   - Error handling and logging
   
2. **Team Lead Dashboard Integration**
   - Connect dashboard to premade template
   - Display team data from database
   - Display module assignments
   - Display student progress
   - All within existing template structure
   
3. **Testing & Validation**
   - Test template filling with sample data
   - Verify no new pages created
   - Verify data accuracy
   - Human review before production use

**Deliverable:** `notion_template_service.py` with strict read/fill-only operations

### Phase 4: Frontend Enhancement (Parallel with Phase 3)
**Duration:** 2-3 hours

1. **Connect to Real Database**
   - Update API service to use production endpoints
   - Test with actual module data from database
   - Handle edge cases (missing data, null values)
   
2. **Module Player Enhancement**
   - Load real module sections
   - Display actual competency data
   - Show ghost cohort comparisons (if data available from Gamma)
   
3. **Dashboard Refinement**
   - Display real subsystem data
   - Show actual student progress
   - Filter modules by university/team

**Deliverable:** Production-ready React frontend with real data integration

---

## Branch 3: Agent Gamma — Infrastructure & Data Operations

### Primary Mission
Audit Notion sync scripts, eliminate page creation, consolidate dashboards, prepare ghost cohort data.

### Resource Claims
- **Read/Write:** `scripts/*.py` (audit and refactor)
- **Write:** Notion API (template-filling only, NO page creation)
- **Write:** `ghost_cohorts` table (populate with historical data)
- **Write:** Database schema tables (create missing coordination tables)
- **Read:** `canon/*.md` (reference for requirements)

### Non-Interference Protocol
- ✅ Can modify infrastructure scripts
- ✅ Can modify database schema
- ✅ Can populate data tables
- ✅ Can refactor Notion sync (template mode only)
- ❌ Cannot modify module content
- ❌ Cannot modify backend API endpoints
- ❌ Cannot modify frontend code

### Phase 1: Audit & Damage Control (URGENT - No Approval Needed)
**Duration:** 2-3 hours

1. **Script Audit**
   - List all files in `scripts/` that call Notion API
   - Grep for `create_page`, `create_database`, `duplicate`
   - Document which scripts created unwanted pages
   - Estimate number of unwanted pages created
   
2. **Page Creation Inventory**
   - Work with human to access Notion workspace
   - Identify pages that shouldn't exist
   - Create deletion plan (for human approval)
   - Document which were from agents vs which are legitimate
   
3. **Immediate Script Lockdown**
   - Add comments to dangerous scripts: "⚠️ DO NOT RUN - Creates pages"
   - Consider moving to `archive/` or renaming with `.UNSAFE` extension
   - Create safe replacement versions

**Deliverable:** `docs/notion/NOTION_AUDIT_REPORT.md` with complete inventory and remediation plan

### Phase 2: Template-Only Sync Refactor (After Human Approval)
**Duration:** 4-5 hours

1. **Notion Sync Redesign**
   - Refactor `scripts/notion_continuous_sync.py`
   - Remove all page/database creation code
   - Implement template-filling approach:
     * Read premade template structure
     * Query database for data
     * Update properties only (no structure changes)
     * Validate before write
   
2. **Single Dashboard Consolidation**
   - Work with human to understand preferred dashboard layout
   - Design data pipeline: DATABASE → Single Dashboard Template
   - Implement update logic
   - Add rate limiting and error handling
   
3. **Sync Daemon Testing**
   - Test in read-only mode first
   - Verify no new pages created
   - Verify data accuracy
   - Monitor for 24 hours before production

**Deliverable:** Refactored `notion_continuous_sync.py` with strict template-only operations

### Phase 3: Ghost Cohort Data Pipeline (Parallel with Phase 2)
**Duration:** 3-4 hours

1. **Historical Data Analysis**
   - Query `cadence_tasks` table for historical completion times
   - Identify 3-5 representative cohorts (semesters/universities)
   - Calculate fast/medium/slow benchmarks per subsystem
   
2. **Ghost Cohort Table Population**
   - Create cohort profiles (metadata: semester, university, team size)
   - Insert benchmark data
   - Add module-specific timing data
   - Validate data quality
   
3. **API Endpoint Coordination**
   - Verify Beta's `/modules/{id}/ghost_cohorts` endpoint works
   - Test data retrieval
   - Add caching if needed
   - Document expected format

**Deliverable:** Populated `ghost_cohorts` table with 3-5 historical cohorts

### Phase 4: Database Schema Validation (Ongoing)
**Duration:** 2-3 hours

1. **Agent Coordination Tables**
   - Verify `ascent_basecamp_agent_log` exists with all required columns
   - Create `technical_decisions` table (per canon spec)
   - Create `error_log` table (per canon spec)
   - Add indexes for performance
   
2. **Missing LMS Tables**
   - Check for `learner_performance` table
   - Check for `subsystem_competency` table
   - Check for `race_metadata` table
   - Create any missing tables per API requirements
   
3. **Data Integrity**
   - Add foreign key constraints
   - Add indexes for common queries
   - Run VACUUM/ANALYZE on Neon database

**Deliverable:** Complete database schema with all required tables

---

## Resource Conflict Prevention Matrix

| Resource | Alpha | Beta | Gamma | Conflict Risk |
|----------|-------|------|-------|---------------|
| `modules/*.json` | R/W | R | - | 🟢 Low (Alpha exclusive) |
| `backend/app.py` | - | R/W | - | 🟢 Low (Beta exclusive) |
| `frontend-react/*` | - | R/W | - | 🟢 Low (Beta exclusive) |
| `scripts/*.py` | - | - | R/W | 🟢 Low (Gamma exclusive) |
| `canon/*.md` | R | R | R | 🟢 Low (read-only all) |
| Database `modules` table | R/W | R | - | 🟡 Medium (Alpha writes, Beta reads) |
| Database `ghost_cohorts` | - | R | R/W | 🟡 Medium (Gamma writes, Beta reads) |
| Database coordination tables | R/W | R/W | R/W | 🟡 Medium (All agents log here) |
| Notion API | - | R | R/W | 🟡 Medium (Beta reads, Gamma writes) |

**Conflict Resolution:**
- 🟢 Low: No coordination needed
- 🟡 Medium: Use database transaction locks, communicate via agent_log table
- 🔴 High: Requires sequential work (none in this plan)

---

## Communication Protocol

### Agent Log Updates (Every 10 minutes)
Each agent updates `ascent_basecamp_agent_log` table with:
- Current task
- Resource claim
- Estimated completion time
- Status (in_progress, blocked, completed)

### Daily AGENT_TEAM_CHAT Updates
Each agent adds entry to `/docs/agents/AGENT_TEAM_CHAT.md` with:
- What was completed
- What's next
- Messages for other agents
- Blockers

### Error Logging
Any errors logged to `error_log` table with:
- Error type
- Resolution status
- Severity
- Full details

---

## Human Approval Required For

### All Agents
- [ ] Approve overall three-branch plan
- [ ] Provide Notion workspace access credentials
- [ ] Identify premade template locations

### Agent Alpha
- [ ] Review `MODULE_ANALYSIS_REPORT.md`
- [ ] Approve which modules to remake vs update
- [ ] Clarify terminology ambiguities
- [ ] Approve new module creation

### Agent Beta
- [ ] Review Notion template structure analysis
- [ ] Approve `notion_template_service.py` design
- [ ] Test template-filling functionality before production

### Agent Gamma
- [ ] Review `NOTION_AUDIT_REPORT.md`
- [ ] Approve page deletion plan
- [ ] Approve refactored sync daemon
- [ ] Verify ghost cohort data accuracy

---

## Success Criteria

### Agent Alpha
- ✅ Complete terminology mapping document
- ✅ All 65+ modules classified
- ✅ Human-approved module remake plan
- ✅ Updated modules aligned with canon

### Agent Beta
- ✅ Backend import errors fixed
- ✅ All LMS API tests passing
- ✅ Notion template structure documented
- ✅ Template-filling service operational
- ✅ Frontend integrated with real data

### Agent Gamma
- ✅ Complete Notion page audit
- ✅ Unwanted pages identified (for deletion)
- ✅ Sync scripts refactored (template-only)
- ✅ Ghost cohort data populated
- ✅ All coordination tables exist

---

## Timeline Estimate

**Phase 1 (Immediate - No Approval Needed):** 1-2 days
- Alpha: Analysis and mapping
- Beta: Backend fixes and testing
- Gamma: Script audit and lockdown

**Phase 2 (After Human Review):** 3-5 days
- Alpha: Module updates/remakes
- Beta: Notion integration and frontend
- Gamma: Sync refactor and data pipeline

**Total:** 1-2 weeks with human review cycles

---

## Next Steps

1. **Human Oversight Reviews This Plan**
   - Approve/modify approach
   - Answer critical blocker questions
   - Provide Notion access

2. **Agents Begin Phase 1 Work**
   - Alpha starts module analysis
   - Beta fixes backend issues
   - Gamma audits Notion scripts

3. **Daily Check-ins**
   - Agents update AGENT_TEAM_CHAT.md
   - Human monitors Notion dashboard
   - Course corrections as needed

4. **Phase 2 Gate Review**
   - Human reviews all Phase 1 deliverables
   - Approves proceeding to Phase 2
   - Provides any additional guidance

---

**Document Status:** Draft awaiting human approval  
**Created by:** Agent Beta  
**Date:** 2025-11-30  
**Last Updated:** 2025-11-30
