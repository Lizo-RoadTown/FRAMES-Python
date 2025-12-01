# Agent Alpha Work Queue — UPDATED 2025-11-30
## Module Content Architect

**Agent Role:** Review existing modules against canon, create terminology mapping, prepare for remake  
**Resource Claims:** `modules/*` (read/write), `modules` table (read/analyze, write after approval)

**⚠️ CRITICAL CHANGE:** New canon documentation has changed project terminology. All existing modules need review before any new creation.

---

## Current Status: Ready for Canon Alignment Work

### Session Start Checklist
- [ ] Log startup to ascent_basecamp_agent_log
- [ ] Read `/docs/agents/AGENT_TEAM_CHAT.md` for context
- [ ] Read `/docs/agents/THREE_BRANCH_WORK_PLAN_2025_11_30.md` for coordination plan
- [ ] Check for resource conflicts in agent_log
- [ ] Claim first resource from queue below
- [ ] Begin work with logging every 10 minutes

---

## PHASE 1: MODULE ANALYSIS (PRIORITY: CRITICAL) ⭐

**Goal:** Understand what exists, map old→new terminology, create human-readable analysis  
**Duration:** 2-3 hours  
**Human Approval:** NOT REQUIRED for analysis phase  
**Deliverable:** `docs/modules/MODULE_ANALYSIS_REPORT.md`

### Task 1.1: Canon Terminology Extraction
- **Resource:** `/canon/*.md` (read only)
- **Estimated Duration:** 30 minutes

**Actions:**
1. Read all 14 canonical documents
2. Extract official terminology for:
   - Project name (Ascent Basecamp vs FRAMES)
   - Subsystem names (Power, Structures, Thermal, etc.)
   - Competency levels (Orientation, Competency, Integration, Autonomy)
   - Application names (Student LMS, Team Lead Module Builder, Researcher Platform)
   - Database/architecture terms
3. Create master terminology list in structured format
4. Log completion to agent_log

**Output:** Section 1 of analysis report with official terminology table

---

### Task 1.2: Existing Module Inventory
- **Resource:** `modules/enhanced/*.json` (read only)
- **Estimated Duration:** 45 minutes

**Actions:**
1. List all 65+ JSON files in `modules/enhanced/`
2. For each module extract:
   - Current title and slug
   - Category/discipline/tags
   - Any terminology that might be outdated
   - Subsystem classification (if mentioned)
   - Learning objectives
3. Create spreadsheet-style table
4. Log completion

**Output:** Section 2 of analysis report with complete module inventory

---

(See full updated queue in `/workspaces/FRAMES-Python/agent_work_queues/alpha_queue.md`)

2. For each power module:
   - Add timer metadata
   - Add checkpoint definitions
   - Link to ghost cohort benchmarks
   - Create leaderboard config
3. Update race_metadata table
4. Log completion

---

## Phase 3: Avionics Subsystem Modules (Priority: HIGH)

### Module 6: Avionics Orientation
- **Resource:** `modules/avionics/orientation.md`
- **Estimated Duration:** 45 minutes

### Module 7: Firmware Flashing Basics
- **Resource:** `modules/avionics/firmware_flashing_101.md`
- **Estimated Duration:** 60 minutes

### Module 8: Telemetry Debugging
- **Resource:** `modules/avionics/telemetry_debugging.md`
- **Estimated Duration:** 60 minutes

### Module 9: I2C Communication
- **Resource:** `modules/avionics/i2c_communication.md`
- **Estimated Duration:** 60 minutes

### Module 10: Sensor Integration
- **Resource:** `modules/avionics/sensor_integration.md`
- **Estimated Duration:** 60 minutes

---

## Phase 4: Prerequisite Graph (Priority: MEDIUM)

### Task: Build Module Prerequisite Links
- **Resource:** `module_prerequisites` table (write)
- **Estimated Duration:** 45 minutes

**Tasks:**
1. Define prerequisite relationships for all created modules
2. Insert into module_prerequisites table
3. Validate no circular dependencies
4. Create subsystem learning path diagrams
5. Log completion

---

## Phase 5: Existing Module Enhancement (Priority: LOW)

### Task: Enhance 69 Existing Modules
- **Resource:** `modules` table (update existing records)
- **Estimated Duration:** 5-10 hours (ongoing)

**Tasks:**
1. For each existing module:
   - Add subsystem tag if missing
   - Add difficulty level
   - Add estimated completion time
   - Link to simulation environments (if applicable)
   - Add race metadata (if suitable for competition)
2. Log progress every 10 modules
3. Final summary log

---

## Handoff Scenarios

### Need Ghost Cohort Data
```sql
INSERT INTO ascent_basecamp_agent_log (
    agent_name, action_type, status, message, metadata
) VALUES (
    'alpha', 'help', 'blocked',
    'Need ghost cohort data for [subsystem] modules',
    '{"help_needed_from": "gamma", "modules": [list of module_ids]}'::jsonb
);
```

### Need API Testing
```sql
INSERT INTO ascent_basecamp_agent_log (
    agent_name, action_type, status, message, metadata
) VALUES (
    'alpha', 'help', 'waiting',
    'X modules ready for Beta to test in frontend',
    '{"help_needed_from": "beta", "modules_ready": X}'::jsonb
);
```

---

## Daily Summary Template

At end of session, append to AGENT_TEAM_CHAT.md:

```markdown
## Agent Alpha - Session #X

### What I Completed Today
- Created [N] modules: [list module names]
- Enhanced [N] existing modules
- Added race metadata to [N] modules

### What I'm Working On Next
- [Next 3 tasks from queue]

### Messages for Other Agents
**To Beta:** [Status update]
**To Gamma:** [Requests or updates]

### Blockers
- [None / List]

### Metrics
- Modules created: N
- Modules enhanced: N
- Database writes: N
- Time spent: X hours
```

---

## Success Metrics

**Week 1 Target:**
- 5+ power modules created
- All modules have complete specs
- Zero resource conflicts
- Daily summaries posted

**Month 1 Target:**
- 20+ modules across power, avionics, structures
- Prerequisite graph complete
- All existing modules enhanced
- Race metadata added to suitable modules

---

**Status:** Waiting for agent to claim first task
**Next Action:** Claim `modules/power/orientation.md` and start Module 1
