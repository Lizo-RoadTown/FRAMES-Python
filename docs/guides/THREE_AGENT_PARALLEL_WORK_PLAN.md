# Three-Agent Parallel Work Plan
## Non-Overlapping Task Distribution

**Created:** 2025-11-28
**Duration:** Ongoing (continuous autonomous work)
**Coordination:** Via [05_agent_coordination_protocol.md](temp_docs/05_agent_coordination_protocol.md)

---

## Overview

Three agents work simultaneously on different parts of the Ascent Basecamp system:
- **Agent Alpha:** Content transformation (CADENCE → modules)
- **Agent Beta:** Student platform development (frontend + API)
- **Agent Gamma:** Infrastructure & data pipelines

**Key Principle:** Zero resource conflicts through subsystem partitioning

---

## Agent Alpha: Module Creation Engine

### Primary Responsibility
Transform CADENCE technical documentation into structured learning modules

### Resource Claims
- `modules/*` - All module creation/editing
- `cadence_documents` table - Read only
- `cadence_tasks` table - Read only
- `modules` table - Write access
- `module_sections` table - Write access
- `module_version_history` table - Write

### Work Queue

#### Phase 1: Power Subsystem Modules (Week 1)
- [ ] Create power subsystem orientation module
- [ ] Create battery sizing fundamentals module
- [ ] Create EPS characterization module
- [ ] Create power budget analysis module
- [ ] Create solar panel selection module
- [ ] Add race metadata to all power modules
- [ ] Create prerequisite links between power modules

**Deliverable:** 5-7 power modules ready for student use

#### Phase 2: Avionics Subsystem Modules (Week 2)
- [ ] Create avionics orientation module
- [ ] Create firmware flashing basics module
- [ ] Create telemetry debugging module
- [ ] Create I2C communication module
- [ ] Create sensor integration module
- [ ] Add difficulty calibrations for avionics modules

**Deliverable:** 5-6 avionics modules

#### Phase 3: Structures Subsystem Modules (Week 3)
- [ ] Create structures orientation module
- [ ] Create CAD tolerance design module
- [ ] Create FreeCAD workflow module
- [ ] Create DFM (Design for Manufacturing) module
- [ ] Link to existing fabrication curricula

**Deliverable:** 4-5 structures modules

#### Phase 4: Module Enhancement (Ongoing)
- [ ] Add ghost cohort benchmarks to existing 69 modules
- [ ] Create challenge variants for high-difficulty modules
- [ ] Build prerequisite graph across all modules
- [ ] Add simulation environment links (CircuitJS, LTSpice)

### Logging Protocol
```python
# Alpha logs to agent_log every 10 minutes
log_agent_action(
    agent_name='alpha',
    action_type='progress',
    resource_claim='modules/power/battery_sizing.md',
    status='working',
    message='Step 3/5: Creating assessment questions',
    metadata={
        'progress_percent': 60,
        'module_id': 124,
        'subsystem': 'power',
    }
)
```

### Success Metrics
- **Modules created:** 20+ in first month
- **Existing modules enhanced:** 69 modules with race metadata
- **Prerequisite graph:** Complete for all subsystems
- **Quality:** All modules pass educational framework validation

---

## Agent Beta: Student Platform Developer

### Primary Responsibility
Build the student-facing learning platform (frontend + API)

### Resource Claims
- `backend/lms_routes.py` - Write access
- `frontend/*` - Write access (when React app created)
- `learner_performance` table - Write access
- `subsystem_competency` table - Write access
- `ghost_cohorts` table - Read only (Gamma populates)
- `race_metadata` table - Read only (Alpha populates)

### Work Queue

#### Phase 1: LMS API Layer (Week 1)
- [ ] Complete all 10 LMS API endpoints
  - [x] GET /students/{id}/modules
  - [x] GET /students/{id}/progress
  - [ ] POST /students/{id}/modules/{module_id}/start
  - [ ] POST /students/{id}/modules/{module_id}/complete
  - [ ] POST /students/{id}/modules/{module_id}/log_activity
  - [ ] GET /modules/{id}/ghost_cohorts
  - [ ] GET /students/{id}/leaderboard
  - [ ] GET /students/{id}/subsystem_competency
  - [ ] POST /students/{id}/race/start
  - [ ] POST /students/{id}/race/complete
- [ ] Add authentication/authorization
- [ ] Add input validation and error handling
- [ ] Write API tests

**Deliverable:** Complete REST API for student platform

#### Phase 2: Student Dashboard Frontend (Week 2)
- [ ] Set up React app structure
- [ ] Create student dashboard layout
- [ ] Build module browsing interface
- [ ] Create module detail view
- [ ] Add progress tracking UI
- [ ] Implement subsystem navigation
- [ ] Add dark mode toggle

**Deliverable:** Functional student dashboard

#### Phase 3: Learning Experience (Week 3)
- [ ] Build module player component
- [ ] Create step-by-step interface
- [ ] Add check validation UI
- [ ] Implement hint system
- [ ] Create quiz/reflection forms
- [ ] Add timer display for race modules

**Deliverable:** Interactive module player

#### Phase 4: Competition Features (Week 4)
- [ ] Build leaderboard display
- [ ] Create ghost cohort racing UI
- [ ] Add "AI classmate" racing feature
- [ ] Implement live progress bars
- [ ] Create celebration animations for completions
- [ ] Add achievement badges

**Deliverable:** Gamified learning experience

### Logging Protocol
```python
# Beta logs API endpoint deployments
log_agent_action(
    agent_name='beta',
    action_type='complete',
    resource_claim='backend/lms_routes.py::POST /students/{id}/modules/{module_id}/complete',
    status='done',
    message='Deployed endpoint: module completion with performance logging',
    metadata={
        'endpoint': 'POST /students/{id}/modules/{module_id}/complete',
        'tests_passing': True,
        'lines_of_code': 87,
    }
)
```

### Success Metrics
- **API coverage:** 100% (all 10 endpoints)
- **Frontend components:** 15+ reusable components
- **Test coverage:** 80%+ for API layer
- **User experience:** Sub-200ms page loads

---

## Agent Gamma: Infrastructure & Data Pipelines

### Primary Responsibility
Build data infrastructure and automation systems

### Resource Claims
- `scripts/*` - All infrastructure scripts
- `notion_sync_metadata` table - Write access
- `ghost_cohorts` table - Write access
- `module_difficulty_calibrations` table - Write access
- `simulation_environments` table - Write access
- Notion API - Read/write (via sync daemon)

### Work Queue

#### Phase 1: Notion Sync Infrastructure (Week 1)
- [x] Create continuous sync daemon script
- [ ] Test Notion API connection with fresh token
- [ ] Run `--setup` to create all Notion databases
- [ ] Deploy sync daemon as background service
- [ ] Test real-time agent activity sync
- [ ] Verify all dashboard syncs working
- [ ] Add error recovery and retry logic

**Deliverable:** Live Notion dashboards syncing every 30s

#### Phase 2: Ghost Cohort System (Week 2)
- [ ] Extract historical performance from CADENCE data
- [ ] Populate ghost_cohorts table (3-5 cohorts)
- [ ] Calculate benchmark times for each module
- [ ] Create ghost "profiles" (fast/medium/slow)
- [ ] Build ghost cohort query API for Beta to consume
- [ ] Add ghost data to Notion dashboards

**Deliverable:** Historical benchmarking system

#### Phase 3: Difficulty Calibration (Week 3)
- [ ] Analyze existing module complexity
- [ ] Populate module_difficulty_calibrations table
- [ ] Build adaptive difficulty system
- [ ] Create difficulty prediction model
- [ ] Add calibration data to module specs
- [ ] Build admin dashboard for difficulty tuning

**Deliverable:** Adaptive learning system

#### Phase 4: Simulation Environment Catalog (Week 4)
- [ ] Document CircuitJS configurations for avionics
- [ ] Document LTSpice setups for power modules
- [ ] Document FreeCAD workflows for structures
- [ ] Populate simulation_environments table
- [ ] Create environment launch scripts
- [ ] Build sandbox management API

**Deliverable:** Integrated simulation tools

### Logging Protocol
```python
# Gamma logs infrastructure deployments
log_agent_action(
    agent_name='gamma',
    action_type='complete',
    resource_claim='scripts/notion_continuous_sync.py',
    status='done',
    message='Sync daemon deployed - monitoring 3 agents + 5 dashboards',
    metadata={
        'sync_interval_seconds': 30,
        'dashboards_synced': 6,
        'tables_monitored': ['agent_log', 'modules', 'people', 'projects', 'tasks'],
        'uptime_target': '99.9%',
    }
)
```

### Success Metrics
- **Sync uptime:** 99%+ (daemon runs continuously)
- **Sync latency:** <1 minute (Neon → Notion delay)
- **Ghost cohorts:** 3-5 historical cohorts populated
- **Simulation environments:** 10+ documented and integrated

---

## Resource Conflict Prevention

### Subsystem Partitioning

| Subsystem | Alpha | Beta | Gamma |
|-----------|-------|------|-------|
| **Database Tables** |
| modules | ✍️ Write | 👁️ Read | 👁️ Read |
| module_sections | ✍️ Write | 👁️ Read | - |
| learner_performance | - | ✍️ Write | 👁️ Read |
| ghost_cohorts | 👁️ Read | 👁️ Read | ✍️ Write |
| cadence_* tables | 👁️ Read | - | 👁️ Read |
| **Code Files** |
| modules/*.md | ✍️ Write | - | - |
| backend/lms_routes.py | - | ✍️ Write | - |
| frontend/* | - | ✍️ Write | - |
| scripts/* | - | - | ✍️ Write |
| **External APIs** |
| Notion API | - | - | ✍️ Write |

### Claim Before Work

Every agent MUST claim resources before starting:

```python
# Before touching ANY file or table
claim_resource(
    agent_name='alpha',
    resource='modules/power/battery_sizing.md'
)

# ... do work ...

# Release when done
release_resource(
    agent_name='alpha',
    resource='modules/power/battery_sizing.md'
)
```

---

## Communication Channels

### 1. Database Agent Log (Real-time)
All agents read/write to `ascent_basecamp_agent_log` continuously

### 2. AGENT_TEAM_CHAT.md (Daily summaries)
Each agent writes end-of-session summary

### 3. Notion Dashboards (Human monitoring)
Liz sees all activity in real-time via sync daemon

### 4. Work Queue Files (Task assignment)
- `agent_work_queues/alpha_queue.md`
- `agent_work_queues/beta_queue.md`
- `agent_work_queues/gamma_queue.md`

---

## Handoff Scenarios

### Scenario 1: Alpha needs ghost data from Gamma
```sql
-- Alpha requests help
INSERT INTO ascent_basecamp_agent_log (
    agent_name, action_type, status, message, metadata
) VALUES (
    'alpha', 'help', 'blocked',
    'Need ghost cohort data for power modules before creating race variants',
    '{"help_needed_from": "gamma", "modules": [124, 125, 126]}'::jsonb
);

-- Gamma sees request and responds
INSERT INTO ascent_basecamp_agent_log (
    agent_name, action_type, status, message, metadata
) VALUES (
    'gamma', 'claim', 'working',
    'Populating ghost cohorts for power modules 124-126',
    '{"handoff_from": "alpha", "eta_minutes": 20}'::jsonb
);
```

### Scenario 2: Beta needs new modules from Alpha
```sql
-- Beta requests more modules
INSERT INTO ascent_basecamp_agent_log (
    agent_name, action_type, status, message, metadata
) VALUES (
    'beta', 'help', 'waiting',
    'Frontend ready for testing - need 5+ modules in avionics subsystem',
    '{"help_needed_from": "alpha", "priority": "high"}'::jsonb
);

-- Alpha prioritizes avionics modules
-- (updates work queue and starts creating)
```

---

## Daily Standup (Automated)

Every 24 hours, each agent writes to AGENT_TEAM_CHAT.md:

### Template:
```markdown
## Agent [Alpha/Beta/Gamma] - Session #N

### What I Completed Today
- [List of completed tasks]

### What I'm Working On Next
- [Next 3-5 tasks from queue]

### Messages for Other Agents
**To [Agent]:** [Specific request or update]

### Blockers
- [None / List blockers]

### Metrics
- [Quantitative progress metrics]
```

---

## Week 1 Kickoff Plan

### Day 1: Infrastructure Setup
- **Gamma:** Deploy Notion sync daemon, verify dashboards
- **Beta:** Complete LMS API endpoints 1-5
- **Alpha:** Create power subsystem orientation module

### Day 2: Foundation Building
- **Gamma:** Populate ghost_cohorts table
- **Beta:** Complete LMS API endpoints 6-10
- **Alpha:** Create battery sizing module + EPS module

### Day 3: Integration Testing
- **Gamma:** Test sync daemon under load (3 agents working)
- **Beta:** Test all API endpoints with Postman
- **Alpha:** Create power budget module + solar panel module

### Day 4: Enhancement
- **Gamma:** Add difficulty calibrations for power modules
- **Beta:** Start React frontend scaffolding
- **Alpha:** Add race metadata to all power modules

### Day 5: Review & Plan Next Week
- **All agents:** Write session summaries
- **All agents:** Update work queues for Week 2
- **All agents:** Review Notion dashboards for issues

---

## Success Criteria

After 1 week of parallel work:

✅ **Gamma:** Notion dashboards show real-time agent activity
✅ **Alpha:** 5+ power modules created and deployed
✅ **Beta:** Complete REST API with 10 endpoints
✅ **All:** Zero resource conflicts logged
✅ **All:** Complete audit trail in agent_log table
✅ **All:** Daily summaries in AGENT_TEAM_CHAT.md

After 1 month:

✅ **Alpha:** 20+ modules across power, avionics, structures
✅ **Beta:** Functional student platform with module player
✅ **Gamma:** Ghost cohort racing system operational
✅ **System:** Students can complete full subsystem learning paths

---

## Implementation Steps

### Step 1: Set Up Infrastructure (Gamma leads)
```bash
# Create work queue directory
mkdir -p agent_work_queues

# Set up Notion databases
python scripts/notion_continuous_sync.py --setup

# Deploy sync daemon (runs in background)
python scripts/notion_continuous_sync.py --run &
```

### Step 2: Initialize Work Queues (Manual)
Create initial task lists in:
- `agent_work_queues/alpha_queue.md`
- `agent_work_queues/beta_queue.md`
- `agent_work_queues/gamma_queue.md`

### Step 3: Add resource_claim Column to Agent Log
```sql
ALTER TABLE ascent_basecamp_agent_log
ADD COLUMN resource_claim VARCHAR(255);

CREATE INDEX idx_agent_log_resource ON ascent_basecamp_agent_log(resource_claim);
```

### Step 4: Start Agents (Simultaneously)
Each agent runs their startup protocol:
1. Log startup to agent_log
2. Read AGENT_TEAM_CHAT.md for context
3. Check for resource conflicts
4. Read work queue
5. Claim first task
6. Begin work with periodic logging

### Step 5: Monitor in Notion
Liz opens Notion → "Agent Activity Dashboard" → See all three agents working in real-time

---

## Troubleshooting

### Problem: Two agents claim same resource
**Solution:** Earlier timestamp wins, later agent backs off

### Problem: Agent stops responding
**Solution:** Other agents detect via agent_log timeout, release claimed resources

### Problem: Notion sync fails
**Solution:** Gamma investigates, updates API token, restarts daemon

### Problem: Merge conflict in code
**Solution:** Agents work on separate files (enforced by resource claims)

---

**Status:** Ready to deploy
**Next Step:** Run infrastructure setup and start all three agents

**Coordination Reference:** [05_agent_coordination_protocol.md](temp_docs/05_agent_coordination_protocol.md)
