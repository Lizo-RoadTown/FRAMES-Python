# Agent Alpha Work Queue
## Module Creation Engine

**Agent Role:** Transform CADENCE documentation into learning modules
**Resource Claims:** `modules/*`, `modules` table (write), `module_sections` table (write)

---

## Current Status: Ready to Start

### Session Start Checklist
- [ ] Log startup to ascent_basecamp_agent_log
- [ ] Read AGENT_TEAM_CHAT.md for context
- [ ] Check for resource conflicts in agent_log
- [ ] Claim first resource from queue below
- [ ] Begin work with logging every 10 minutes

---

## Phase 1: Power Subsystem Modules (Priority: HIGH)

### Module 1: Power Subsystem Orientation
- **Resource:** `modules/power/orientation.md`
- **Source:** `cadence_documents` where subsystem='power'
- **Type:** Orientation module
- **Estimated Duration:** 45 minutes
- **Deliverable:** JSON spec in `modules` table

**Tasks:**
1. Query cadence_documents for power subsystem overview
2. Extract key concepts and terminology
3. Create module outline (5-7 sections)
4. Write learning objectives
5. Create orientation quiz (10 questions)
6. Log completion with module_id

### Module 2: Battery Sizing Fundamentals
- **Resource:** `modules/power/battery_sizing_101.md`
- **Source:** CADENCE power docs on battery selection
- **Type:** Core module
- **Estimated Duration:** 60 minutes

**Tasks:**
1. Extract battery sizing methodology from CADENCE docs
2. Create step-by-step calculation guide
3. Add example problems
4. Create checks for each calculation step
5. Add reflection questions
6. Link to power budget module (prerequisite)

### Module 3: EPS Characterization
- **Resource:** `modules/power/eps_characterization.md`
- **Source:** CADENCE EPS testing procedures
- **Type:** Core module
- **Estimated Duration:** 60 minutes

**Tasks:**
1. Document EPS testing workflow
2. Create hands-on lab steps
3. Add LTSpice simulation link
4. Create data analysis checks
5. Add troubleshooting guide

### Module 4: Power Budget Analysis
- **Resource:** `modules/power/power_budget_analysis.md`
- **Source:** CADENCE power budget spreadsheets
- **Type:** Core module
- **Estimated Duration:** 60 minutes

**Tasks:**
1. Extract power budget methodology
2. Create Excel/spreadsheet template
3. Add validation checks
4. Create example mission profile
5. Link to battery sizing (dependent)

### Module 5: Solar Panel Selection
- **Resource:** `modules/power/solar_panel_selection.md`
- **Source:** CADENCE solar panel docs
- **Type:** Core module
- **Estimated Duration:** 60 minutes

**Tasks:**
1. Document panel selection criteria
2. Create sizing calculator
3. Add datasheet interpretation guide
4. Create comparison matrix
5. Link to power budget (prerequisite)

---

## Phase 2: Race Metadata Enhancement (Priority: MEDIUM)

### Task: Add Race Features to Power Modules
- **Resource:** `modules` table where subsystem='power'
- **Dependencies:** Gamma must populate ghost_cohorts first
- **Estimated Duration:** 90 minutes

**Tasks:**
1. Check with Gamma on ghost cohort status (log 'help' action if needed)
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
