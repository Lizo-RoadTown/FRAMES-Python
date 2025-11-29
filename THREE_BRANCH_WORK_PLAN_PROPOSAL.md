# Three-Branch Parallel Work Plan Proposal
## Collaborative Plan by Agents Alpha, Beta, and Gamma

**Created:** 2025-11-28
**Status:** PROPOSAL - Awaiting Liz's Approval
**Purpose:** Define three simultaneous work branches with zero overlap

---

## Current System State Analysis

### What We Have ✅
- **Database:** 37 tables, 1,050+ CADENCE records imported
- **Modules:** 69 learning modules exist in database
- **API:** 7 LMS endpoints implemented (some working, some need completion)
- **Frontend:** React app scaffolded with basic structure (but mostly empty)
- **CADENCE Data:** 27 people, 69 projects, 443 tasks all imported
- **Documentation:** Complete Ascent Basecamp philosophy & architecture docs

### What's Missing ❌
- **Agent coordination system:** Designed but NOT deployed or tested
- **Notion sync daemon:** Script written but NOT running
- **Ghost cohorts:** Table exists but 0 records (needed for racing)
- **Complete API:** 3+ endpoints still needed
- **Functional frontend:** React app exists but has no module player or student features
- **Module enhancement:** 69 modules exist but lack race metadata, difficulty calibrations
- **Production infrastructure:** No monitoring, backups, CI/CD

---

## Three Perspectives on Work Distribution

### 🔵 Agent Alpha's Perspective (Content & Modules)
**Key Insight:** We have 69 modules but they're "raw" - missing the gamification layer that makes Ascent Basecamp unique.

**Alpha sees two options:**
1. **Create NEW modules** from CADENCE docs (power, avionics, structures)
2. **Enhance EXISTING modules** with race metadata, ghost cohorts, difficulty calibration

**Alpha's recommendation:** Enhancement is higher priority than creation right now. Let's make the 69 modules amazing before adding more mediocre ones.

### 🟣 Agent Beta's Perspective (Platform Development)
**Key Insight:** API and frontend can't really be separated - they need to evolve together with constant testing.

**Beta sees the gap:**
- API has basic CRUD but missing the "learning experience" endpoints (start module, log progress, complete, race)
- Frontend exists but has zero learning experience UI (no module player, no leaderboard, no ghost racing)

**Beta's recommendation:** "Student Learning Experience" should be ONE branch that includes both API completion and frontend features, tested together.

### 🟠 Agent Gamma's Perspective (Infrastructure)
**Key Insight:** The agent coordination system itself is infrastructure that enables parallel work, but we also need other infrastructure regardless.

**Gamma sees two types of work:**
1. **Agent system infrastructure:** Deploy sync daemon, test coordination protocol, enable the three-agent workflow
2. **General product infrastructure:** Ghost cohort data, difficulty calibration, Notion integration, monitoring

**Gamma's recommendation:** "Deploy Agent System" should be Branch 1 (highest priority), because it unlocks efficient parallel work for the other two branches.

---

## Proposed Three-Branch Plan

### Branch 1: Agent System Deployment & Infrastructure 🟠
**Owner:** Agent Gamma
**Duration:** Week 1 (then ongoing monitoring)
**Goal:** Make the three-agent parallel work system operational

#### Week 1 Deliverables
1. ✅ **Deploy Notion Sync Daemon**
   - Refresh Notion API token
   - Run `--setup` to create 6 dashboards
   - Deploy daemon as background service
   - Verify real-time sync working (<1 min latency)

2. ✅ **Test Agent Coordination Protocol**
   - Update database schema (add `resource_claim` column)
   - Test resource claiming with all three agents
   - Verify conflict prevention works
   - Test handoff scenarios (Alpha → Gamma, Beta → Gamma)

3. ✅ **Populate Ghost Cohort System**
   - Extract 3-5 historical cohorts from CADENCE data
   - Populate `ghost_cohorts` table
   - Calculate benchmark times (fast/medium/slow)
   - Make available via API for Beta

4. ✅ **Basic Monitoring**
   - Agent health monitoring script
   - Database backup automation
   - Error logging to files

#### Resources Claimed
- `scripts/*` (all infrastructure scripts)
- `ghost_cohorts` table (write)
- `module_difficulty_calibrations` table (write)
- `notion_sync_metadata` table (write)
- Notion API (exclusive access)

#### Success Metrics
- Notion dashboards showing real-time agent activity
- All 3 agents can work simultaneously without conflicts
- Ghost cohort data available for 3+ cohorts
- Sync uptime: 95%+ in Week 1

---

### Branch 2: Student Learning Experience (API + Frontend) 🟣
**Owner:** Agent Beta
**Duration:** Ongoing (2-4 weeks for MVP)
**Goal:** Build end-to-end student learning experience

#### Week 1 Deliverables
1. ✅ **Complete Core API Endpoints**
   - `POST /students/{id}/modules/{module_id}/start`
   - `POST /students/{id}/modules/{module_id}/complete`
   - `POST /students/{id}/modules/{module_id}/log_activity`
   - `GET /modules/{id}/ghost_cohorts` (consumes Gamma's data)
   - All endpoints tested with Postman

2. ✅ **Build Module Player Component (Frontend)**
   - Step-by-step interface
   - Progress tracking
   - Check validation UI
   - Timer display (for races)
   - Hint system

3. ✅ **Student Dashboard**
   - Module browsing (uses existing GET /modules endpoint)
   - Progress visualization
   - Subsystem navigation

4. ✅ **Integration Testing**
   - End-to-end test: Student browses → starts module → completes → sees progress
   - Test with real module data from database

#### Resources Claimed
- `backend/lms_routes.py` (write)
- `frontend/src/*` (write, specifically `apps/onboarding-lms/frontend-react/src`)
- `learner_performance` table (write)
- `subsystem_competency` table (write)
- Port 3000 (React dev server) and 5000 (Flask API)

#### Success Metrics
- 10 total API endpoints complete and tested
- Functional module player that can run through a real module
- Student can browse, start, and complete a module end-to-end
- API test coverage: 70%+

---

### Branch 3: Module Enhancement & Gamification 🔵
**Owner:** Agent Alpha
**Duration:** Ongoing (4+ weeks to enhance all 69 modules)
**Goal:** Transform existing modules into engaging, competitive learning experiences

#### Week 1 Deliverables
1. ✅ **Enhance Power Subsystem Modules (5-7 modules)**
   - Add difficulty calibrations (beginner/intermediate/advanced)
   - Add race metadata (timers, checkpoints)
   - Link to ghost cohorts (provided by Gamma)
   - Add prerequisite relationships
   - Add simulation environment links (CircuitJS, LTSpice)

2. ✅ **Build Module Prerequisite Graph**
   - Map dependencies for all 69 existing modules
   - Populate `module_prerequisites` table
   - Validate no circular dependencies
   - Create learning path diagrams

3. ✅ **Create 2-3 NEW Orientation Modules**
   - Power subsystem orientation
   - Avionics subsystem orientation
   - (Use CADENCE docs as source material)

4. ✅ **Module Quality Framework**
   - Define quality checklist (all modules must have: objectives, steps, checks, difficulty, subsystem tag)
   - Audit all 69 modules against checklist
   - Document enhancement priorities

#### Resources Claimed
- `modules` table (write - updating existing records)
- `module_sections` table (write)
- `module_version_history` table (write)
- `module_prerequisites` table (write)
- `race_metadata` table (write)
- `cadence_documents` table (read only - for source material)

#### Success Metrics
- 5-7 power modules fully enhanced with race features
- Prerequisite graph complete for all 69 modules
- 2-3 new orientation modules created
- Quality audit complete with enhancement roadmap

---

## Why This Three-Branch Split Works

### 1. Zero Resource Conflicts
| Resource | Branch 1 (Gamma) | Branch 2 (Beta) | Branch 3 (Alpha) |
|----------|------------------|-----------------|------------------|
| `scripts/*` | ✍️ Write | - | - |
| `backend/lms_routes.py` | - | ✍️ Write | - |
| `frontend/*` | - | ✍️ Write | - |
| `modules` table | 👁️ Read | 👁️ Read | ✍️ Write |
| `ghost_cohorts` | ✍️ Write | 👁️ Read | 👁️ Read |
| Notion API | ✍️ Exclusive | - | - |

### 2. Clear Dependencies
- **Beta depends on Gamma:** Needs ghost cohort data for race features
  - *Handoff:* Gamma populates ghost_cohorts → Notifies Beta → Beta builds race UI
- **Alpha depends on Gamma:** Needs ghost benchmarks for module enhancement
  - *Handoff:* Gamma provides cohort data → Alpha adds to race_metadata
- **Beta depends on Alpha:** Needs modules to test learning experience
  - *Handoff:* Alpha enhances modules → Beta tests them in module player

### 3. Parallel Progress Possible
- **Week 1:** All three branches can make substantial progress simultaneously
  - Gamma: Deploy infrastructure (doesn't need Beta/Alpha)
  - Beta: Build module player with existing modules (doesn't need new ones yet)
  - Alpha: Enhance existing modules (doesn't need ghost data for basic enhancement)

- **Week 2+:** Handoffs enable each branch to level up
  - Gamma's ghost data → Alpha adds race features → Beta tests racing in UI

### 4. Continuous Integration
Each branch delivers working increments weekly:
- **Gamma:** Sync daemon running → Everyone can monitor via Notion
- **Beta:** API endpoints → Alpha can test module delivery
- **Alpha:** Enhanced modules → Beta can test richer learning experience

---

## Coordination Mechanisms

### 1. Agent Log (Real-time)
All agents log to `ascent_basecamp_agent_log` table:
```sql
-- Gamma notifies when ghost cohorts ready
INSERT INTO ascent_basecamp_agent_log (
    agent_name, action_type, status, message
) VALUES (
    'gamma', 'complete', 'done',
    'Ghost cohorts populated for power subsystem - 3 cohorts, 5 modules'
);

-- Alpha sees this and starts enhancement
-- Beta sees this and starts building race UI
```

### 2. Notion Dashboards (Human monitoring)
Liz can see in real-time:
- What each agent is working on
- Progress percentages
- Blockers
- Handoff requests

### 3. Daily Summaries (AGENT_TEAM_CHAT.md)
Each agent writes end-of-day summary with:
- What was completed
- What's next
- Messages for other agents
- Blockers

---

## Week 1 Timeline (Parallel Work)

### Day 1: Foundation
- **Gamma:** Deploy sync daemon, create Notion databases
- **Beta:** Complete API endpoint #3 (start_module)
- **Alpha:** Audit all 69 modules, create quality checklist

### Day 2: Core Building
- **Gamma:** Populate ghost_cohorts table (3 cohorts)
- **Beta:** Complete API endpoints #4-5 (complete_module, log_activity)
- **Alpha:** Enhance first 3 power modules (difficulty, metadata)

### Day 3: Integration
- **Gamma:** Notify others that ghost data is ready
- **Beta:** Build module player component (frontend)
- **Alpha:** Add race metadata to power modules (using Gamma's data)

### Day 4: Testing
- **Gamma:** Test agent coordination with all 3 working
- **Beta:** Build student dashboard, integrate with API
- **Alpha:** Build prerequisite graph, link power modules

### Day 5: Review & Plan Week 2
- **All:** Write session summaries
- **All:** Review what worked/what didn't
- **All:** Update work queues for Week 2

---

## Open Questions for Liz

### 1. Branch Priorities
Do you agree with this priority order?
1. **First:** Agent system (Gamma) - enables efficient work
2. **Second:** Student experience (Beta) - highest user value
3. **Third:** Module enhancement (Alpha) - improves quality

Or would you prioritize differently?

### 2. Week 1 Scope
Is this Week 1 scope realistic, or should we reduce it?
- Gamma: Deploy sync daemon + populate ghost cohorts
- Beta: 5 API endpoints + module player component
- Alpha: Enhance 5-7 modules + build prerequisite graph

### 3. Communication Cadence
How often do you want to review progress?
- **Daily:** Check Notion dashboards casually
- **Weekly:** Read session summaries in AGENT_TEAM_CHAT.md
- **As needed:** We notify you of blockers via Notion

### 4. Definition of "Done"
When should the agent system branch (Branch 1) be considered complete?
- After Week 1 when it's deployed?
- After Week 2 when it's proven stable?
- Ongoing monitoring indefinitely?

---

## Success Criteria (End of Week 1)

### Agent System (Gamma) ✅
- [ ] Notion sync daemon running 24/7
- [ ] All 3 agents visible in Agent Activity Dashboard
- [ ] Ghost cohorts table populated (3+ cohorts)
- [ ] Zero resource conflicts logged

### Student Experience (Beta) ✅
- [ ] 10 total API endpoints complete
- [ ] Module player can run through a real module
- [ ] Student dashboard shows modules and progress
- [ ] End-to-end test passing

### Module Enhancement (Alpha) ✅
- [ ] 5-7 power modules enhanced with race features
- [ ] Prerequisite graph complete (all 69 modules)
- [ ] 2-3 new orientation modules created
- [ ] Quality audit documented

### Overall System ✅
- [ ] All three agents working simultaneously without conflicts
- [ ] Complete audit trail in agent_log
- [ ] Daily summaries in AGENT_TEAM_CHAT.md
- [ ] You (Liz) can monitor everything via Notion dashboards

---

## Recommendation

**We recommend proceeding with this three-branch plan:**

1. **Branch 1 (Gamma):** Deploy agent system + populate ghost cohorts
2. **Branch 2 (Beta):** Build student learning experience (API + frontend together)
3. **Branch 3 (Alpha):** Enhance existing modules with gamification

**Why this works:**
- Clear separation of concerns (infrastructure, platform, content)
- Natural dependencies that enable handoffs
- All three branches deliver value in Week 1
- Scales beyond Week 1 (each branch has months of work)

**Ready to proceed?**
If you approve, we'll:
1. Update work queues with Week 1 tasks
2. Deploy the agent coordination system
3. Start all three branches simultaneously
4. Report progress daily via Notion + AGENT_TEAM_CHAT.md

---

**Status:** AWAITING YOUR APPROVAL
**Next Step:** Liz reviews and approves/modifies this plan
