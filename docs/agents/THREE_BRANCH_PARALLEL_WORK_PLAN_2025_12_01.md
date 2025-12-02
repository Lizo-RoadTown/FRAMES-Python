# Three-Branch Parallel Work Plan
**Created:** 2025-12-01
**Status:** Draft - Awaiting Human Approval
**Purpose:** Minimize agent interference, maximize parallel progress

---

## Core Principle: Zero Overlap

Each agent works in COMPLETELY separate domains:
- **Different file paths** (no shared files modified)
- **Different database operations** (coordinated via logging only)
- **Different deliverables** (independent outputs)
- **Async communication** (via AGENT_TEAM_CHAT.md only)

---

## 🟦 BRANCH ALPHA - Module Content & Enhancement
**Agent:** Alpha
**Domain:** Module creation, content quality, OATutor integration
**Timeline:** 2-3 weeks

### Resources OWNED by Alpha:
- `modules/` (all subdirectories)
- `docs/agents/MODULE_*.md` (analysis documents)
- `data/projects/CADENCE/markdown/` (source material - read only)
- Database tables: `modules`, `module_sections` (write access)

### Resources CLAIMED (No other agent touches):
- `modules/enhanced/` - Read/write for enhancement work
- `modules/validated/` - New directory for canon-compliant modules
- Any files matching `*module*.json` in modules directory

---

### Phase 1A: Module Cleanup & Validation (Week 1)
**Duration:** 20-25 hours

#### Task 1.1: Archive Non-Learning Modules (2 hours)
- Move 16 non-learning modules (meeting notes, tasks) to `docs/cadence/archive/`
- Update module count in documentation
- **Deliverable:** `docs/agents/ARCHIVED_MODULES_LIST.md`

#### Task 1.2: Export Database Modules to JSON (3 hours)
- Export 10 database modules (IDs 71-82) to canon-compliant JSON format
- Store in `modules/validated/power/` and `modules/validated/avionics/`
- Ensure full MODULE_SCHEMA.md compliance
- **Deliverable:** 10 JSON files with full OATutor structure

#### Task 1.3: Validate Existing Enhanced Modules (4 hours)
- Run validation script on all 68 enhanced modules
- Flag missing fields: learning_objectives, prerequisites, discipline
- Generate repair queue
- **Deliverable:** `docs/agents/MODULE_VALIDATION_REPORT.md`

#### Task 1.4: Define Module Prerequisite Graph (3 hours)
- Map learning dependencies between modules
- Create visual prerequisite tree
- Identify "gateway" modules (must complete first)
- **Deliverable:** `modules/PREREQUISITE_GRAPH.json` + visualization

#### Task 1.5: Tier 1 Module Selection (2 hours)
- Select 3-5 flagship modules for deep enhancement
- Based on: subsystem coverage, student demand, CADENCE relevance
- Get human approval on selection
- **Deliverable:** `docs/agents/TIER_1_MODULES_PLAN.md`

---

### Phase 1B: Content Enhancement (Week 2)
**Duration:** 25-30 hours

#### Task 2.1: Enhance 3 Flagship Modules (Deep) (18 hours = 6h each)
For each flagship module:
- Research CADENCE source documents (data/projects/CADENCE/)
- Write detailed learning objectives (Bloom's taxonomy)
- Create interactive sections (OATutor-style scaffolds)
- Add race_metadata framework (ghost cohort benchmarks)
- Include practical exercises with validation
- Write assessment quizzes
- **Deliverable:** 3 production-ready modules in `modules/validated/`

#### Task 2.2: Enhance 10 Standard Modules (Light) (10 hours = 1h each)
For each standard module:
- Fill in placeholder content with real technical info
- Add basic learning objectives
- Define prerequisites
- Set correct discipline tag
- Basic quality check
- **Deliverable:** 10 enhanced modules ready for Beta testing

---

### Phase 1C: OATutor Integration (Week 3)
**Duration:** 15 hours

#### Task 3.1: OATutor Content Adaptation (8 hours)
- Clone OATutor repository (https://github.com/Lizo-RoadTown/OATutor)
- Extract relevant problem types (engineering/math)
- Adapt OATutor JSON format to FRAMES MODULE_SCHEMA
- Create conversion script
- **Deliverable:** `scripts/oatutor_converter.py` + sample modules

#### Task 3.2: Interactive Problem Integration (5 hours)
- Add OATutor-style problems to 3 modules
- Test hint pathways
- Validate scaffolding structure
- **Deliverable:** Enhanced modules with interactive problems

#### Task 3.3: Documentation (2 hours)
- Create module authoring guide
- Document validation process
- Provide examples of good vs bad modules
- **Deliverable:** `docs/MODULE_AUTHORING_GUIDE.md`

---

### Alpha Success Criteria:
- ✅ 13+ canon-compliant modules (3 flagship + 10 standard)
- ✅ Prerequisite graph established
- ✅ OATutor integration proven
- ✅ Clear module creation workflow documented
- ✅ All modules testable by Beta

---

## 🟩 BRANCH BETA - Application Development
**Agent:** Beta
**Domain:** React frontends, Flask APIs, UI/UX
**Timeline:** 3-4 weeks

### Resources OWNED by Beta:
- `apps/onboarding-lms/frontend-react/` (Student LMS)
- `apps/team-lead-dashboard/` (NEW - Team Lead app)
- `backend/lms_routes.py` (LMS API)
- `backend/team_lead_routes.py` (NEW - Team Lead API)
- Database tables: `module_progress`, `module_assignments`, `module_analytics_events` (write access)

### Resources CLAIMED (No other agent touches):
- All files in `apps/onboarding-lms/frontend-react/src/`
- All files in `apps/team-lead-dashboard/` (when created)
- `backend/lms_routes.py`, `backend/team_lead_routes.py`

---

### Phase 2A: Complete Student LMS (Week 1)
**Duration:** 20-25 hours

#### Task 1.1: Build Supporting Components (12 hours)
Create 9 missing React components:
- `ModuleCard.jsx` - Display module in grid/list view (2h)
- `SubsystemNav.jsx` - Sidebar navigation by subsystem (2h)
- `CompetencyBar.jsx` - Visual progress indicator (1h)
- `LoadingSpinner.jsx` - Loading states (1h)
- `ProgressStepper.jsx` - Step-by-step navigation (2h)
- `CheckValidation.jsx` - Exercise validation UI (2h)
- `RaceTimer.jsx` - Race mode timer + ghost comparison (2h)
- `HintTooltip.jsx` - Hint display system (1h)
- `CelebrationModal.jsx` - Success animations (1h)
- **Deliverable:** 9 production-ready components

#### Task 1.2: Data Integration (6 hours)
- Wire components to real PostgreSQL data
- Connect to Alpha's modules (IDs 71-82 + enhanced)
- Test with real student accounts
- Handle edge cases (empty data, loading states)
- **Deliverable:** Fully functional Student LMS

#### Task 1.3: Testing & Polish (4 hours)
- User acceptance testing
- Mobile responsiveness check
- Performance optimization
- Bug fixes
- **Deliverable:** Production-ready Student LMS

---

### Phase 2B: Build Team Lead Module Builder (Week 2-3)
**Duration:** 35-40 hours

#### Task 2.1: Backend API (8 hours)
Create `backend/team_lead_routes.py`:
- `POST /api/team-lead/modules` - Create new module (2h)
- `PUT /api/team-lead/modules/{id}` - Update module (2h)
- `POST /api/team-lead/modules/{id}/sections` - Add sections (2h)
- `POST /api/team-lead/modules/{id}/publish` - Publish workflow (1h)
- `POST /api/team-lead/assignments` - Assign to students (1h)
- **Deliverable:** Team Lead API (5 endpoints, tested)

#### Task 2.2: React App Setup (4 hours)
- Create new React app: `apps/team-lead-dashboard/`
- Install dependencies (react-router, axios, material-ui, react-quill)
- Configure routing
- Set up API service layer
- **Deliverable:** Scaffolded Team Lead app

#### Task 2.3: Module Creation Form (8 hours)
- Multi-step form (module info → sections → review)
- Form validation
- Draft saving (auto-save every 2 min)
- Rich text editor integration (react-quill)
- Image upload support
- **Deliverable:** Module creation workflow

#### Task 2.4: Section Editor (8 hours)
- Rich text editor for content
- Section type selector (reading, exercise, quiz, video)
- Check/quiz builder (validation rules, hints)
- Duration estimator
- Reorder sections (drag-drop)
- **Deliverable:** Section editing interface

#### Task 2.5: Preview & Publish (4 hours)
- Preview mode (see student view)
- Publish button (draft → published)
- Unpublish option
- Version history
- **Deliverable:** Publishing workflow

#### Task 2.6: Assignment Interface (4 hours)
- Student/team selector
- Bulk assignment
- Due date setting
- Assignment history
- **Deliverable:** Assignment management

#### Task 2.7: Progress Dashboard (4 hours)
- Module completion stats
- Student progress visualization
- Time-on-task metrics
- Quiz scores
- **Deliverable:** Analytics dashboard for Team Leads

---

### Phase 2C: Optional Notion Export (Week 4)
**Duration:** 4-6 hours (if time permits)

#### Task 3.1: Simple Export Endpoint (3 hours)
- `POST /api/modules/{id}/export-to-notion`
- One-way only (PostgreSQL → Notion)
- Uses notionary library
- Creates/updates Notion page
- **Deliverable:** Export functionality

#### Task 3.2: Export UI (2 hours)
- "Export to Notion" button in Team Lead dashboard
- Export status indicator
- Error handling
- **Deliverable:** User-facing export feature

---

### Beta Success Criteria:
- ✅ Student LMS 100% complete and tested
- ✅ Team Lead Module Builder fully functional
- ✅ Team Leads can create, edit, publish, assign modules
- ✅ Team Leads can monitor student progress
- ✅ (Optional) Simple Notion export working

---

## 🟨 BRANCH GAMMA - Infrastructure & Data
**Agent:** Gamma
**Domain:** Database, deployment, Notion (optional), ghost cohorts
**Timeline:** 2-3 weeks

### Resources OWNED by Gamma:
- `scripts/` (all infrastructure scripts)
- `shared/database/` (schema, migrations)
- `.github/workflows/` (CI/CD)
- Database: schema changes, migrations, seeding
- Notion integration (if needed)

### Resources CLAIMED (No other agent touches):
- All files in `scripts/`
- All files in `shared/database/`
- All `.sql` migration files
- CI/CD configuration files

---

### Phase 3A: Database & Ghost Cohorts (Week 1)
**Duration:** 20-25 hours

#### Task 1.1: Ghost Cohort Data Generation (8 hours)
- Extract historical CADENCE performance data
- Calculate benchmark statistics (median, quartiles)
- Generate ghost_data arrays for each module
- Populate `ghost_cohorts` table
- **Deliverable:** Real ghost cohort data for race mode

#### Task 1.2: Database Schema Validation (4 hours)
- Run schema validation script
- Check all foreign keys
- Verify indexes exist
- Test query performance
- **Deliverable:** Validated database schema

#### Task 1.3: Database Seeding (6 hours)
- Create seed script for test data
- Generate sample students, teams, universities
- Create module assignments
- Generate sample progress data
- **Deliverable:** `scripts/seed_database.py`

#### Task 1.4: Migration System (3 hours)
- Set up Alembic for migrations
- Create migration for ghost_cohorts
- Test rollback procedures
- **Deliverable:** Migration framework

---

### Phase 3B: Infrastructure & Deployment (Week 2)
**Duration:** 20-25 hours

#### Task 2.1: CI/CD Pipeline (8 hours)
- GitHub Actions for tests
- Automatic deployment to staging
- Database migration automation
- Frontend build optimization
- **Deliverable:** `.github/workflows/deploy.yml`

#### Task 2.2: Environment Configuration (4 hours)
- Production .env template
- Secrets management
- Database connection pooling
- API rate limiting
- **Deliverable:** Production-ready configs

#### Task 2.3: Monitoring & Logging (6 hours)
- Error tracking setup
- Performance monitoring
- Database query logging
- Agent coordination dashboard
- **Deliverable:** Monitoring infrastructure

#### Task 2.4: Documentation (3 hours)
- Deployment guide
- Troubleshooting guide
- Database backup/restore procedures
- **Deliverable:** Infrastructure docs

---

### Phase 3C: Notion Integration (Week 3 - Optional)
**Duration:** 15-20 hours (if needed)

#### Task 3.1: Evaluate Notion Necessity (2 hours)
- Review if Team Lead dashboard replaces Notion need
- Consult with human on Notion role
- **Decision Point:** Proceed or skip Notion work

#### Task 3.2: Simple One-Way Sync (8 hours - if approved)
- Read Foundation page structure
- Create sync service (one-way: PostgreSQL → Notion)
- Sync module library for visibility
- Sync team/student data for stakeholders
- **Deliverable:** Notion visibility (read-only for stakeholders)

#### Task 3.3: Sync Automation (4 hours - if approved)
- Scheduled sync (daily)
- Manual trigger endpoint
- Conflict detection (warn only)
- **Deliverable:** Automated sync daemon

---

### Gamma Success Criteria:
- ✅ Ghost cohort data populated (race mode works)
- ✅ Database fully validated and optimized
- ✅ CI/CD pipeline operational
- ✅ Monitoring and logging in place
- ✅ (Optional) Notion sync if needed

---

## 🔄 Coordination Protocols

### Daily Check-ins
Each agent posts to `docs/agents/AGENT_TEAM_CHAT.md`:
- What completed today
- What starting tomorrow
- Any blockers
- Help needed from other agents

### Resource Claims
Before touching ANY file:
```python
# Log claim to database
INSERT INTO ascent_basecamp_agent_log (
    agent_name, action_type, resource_claim, status
) VALUES ('alpha', 'claim', 'modules/enhanced/', 'working');
```

### Handoffs
When work depends on another agent:
1. Complete your piece
2. Post to AGENT_TEAM_CHAT.md with clear handoff message
3. Mark task as "blocked - waiting for [agent]"
4. Move to next independent task

### Conflicts
If two agents need same resource:
1. Check agent_log for active claims
2. If claimed, find alternative task
3. If urgent, post to AGENT_TEAM_CHAT.md requesting coordination
4. Human breaks tie if needed

---

## 📊 Success Metrics

### Week 1 Deliverables:
- **Alpha:** Module validation complete, 3 flagship modules selected
- **Beta:** Student LMS 100% complete
- **Gamma:** Ghost cohorts populated, database validated

### Week 2 Deliverables:
- **Alpha:** 3 flagship modules enhanced (deep)
- **Beta:** Team Lead API complete, React app scaffolded
- **Gamma:** CI/CD pipeline operational

### Week 3 Deliverables:
- **Alpha:** 10 standard modules enhanced, OATutor integration
- **Beta:** Team Lead Module Builder complete
- **Gamma:** Monitoring/logging complete, (optional) Notion sync

### Week 4 (Optional):
- **Alpha:** Additional modules, documentation
- **Beta:** Polish, optional Notion export UI
- **Gamma:** Infrastructure optimization

---

## 🚨 Hard Constraints

### Alpha NEVER touches:
- ❌ `backend/` (except reading for context)
- ❌ `apps/` (except reading for context)
- ❌ `scripts/` (except running read-only)
- ❌ `.github/workflows/`

### Beta NEVER touches:
- ❌ `modules/` (except reading for testing)
- ❌ `scripts/` (except running for local dev)
- ❌ Database schema (except via API)
- ❌ Infrastructure configs

### Gamma NEVER touches:
- ❌ `modules/` (except seeding)
- ❌ `apps/` (except deployment)
- ❌ Backend route logic (only schema)
- ❌ React components

---

## 📋 Human Approval Checkpoints

**Before starting work, human must approve:**
1. ✅ This three-branch plan (overall structure)
2. ✅ Alpha's Tier 1 module selection
3. ✅ Beta's Team Lead dashboard design/wireframes
4. ✅ Gamma's decision on Notion integration (proceed or skip)

**During work, human reviews:**
- Alpha's flagship modules (before marking complete)
- Beta's Team Lead dashboard (before production)
- Gamma's CI/CD pipeline (before going live)

---

## 📝 Notes

This plan assumes:
- All three agents work in parallel VSCode sessions
- Human monitors via AGENT_TEAM_CHAT.md daily
- Database coordination via agent_log table
- Zero file conflicts (each agent owns separate paths)
- Async handoffs (no real-time communication needed)

**Estimated Total Timeline:** 3-4 weeks for complete system
**Estimated Agent Hours:** 60-75 hours per agent

---

**Status:** DRAFT - Awaiting human additions and approval

**Next Steps:**
1. Human reviews plan
2. Human adds additional tasks if needed
3. Human approves to proceed
4. Agents begin work in parallel branches

