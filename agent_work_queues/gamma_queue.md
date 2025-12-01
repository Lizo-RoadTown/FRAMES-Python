# Agent Gamma Work Queue — UPDATED 2025-11-30
## Infrastructure & Data Operations Specialist

**Agent Role:** Audit Notion scripts, eliminate page creation, consolidate dashboards, prepare ghost cohort data  
**Resource Claims:** `scripts/*` (write), Database schema (write), Notion API (template-filling only)

**⚠️ CRITICAL CHANGE:** STOP all page creation. Audit existing scripts, refactor to template-only mode. Focus on data operations.

---

## Current Status: Ready for Audit & Cleanup

### Session Start Checklist
- [ ] Log startup to ascent_basecamp_agent_log
- [ ] Read `/docs/agents/AGENT_TEAM_CHAT.md` for context
- [ ] Read `/docs/agents/THREE_BRANCH_WORK_PLAN_2025_11_30.md` for coordination plan
- [ ] Check for resource conflicts in agent_log
- [ ] Claim first resource from queue below
- [ ] Begin work with logging every 10 minutes

---

## PHASE 1: AUDIT & DAMAGE CONTROL (PRIORITY: URGENT) 🔴

**Goal:** Identify all page-creating code, document the problem, lockdown dangerous scripts  
**Duration:** 2-3 hours  
**Human Approval:** NOT REQUIRED for audit, REQUIRED for deletion plan  
**Deliverable:** `docs/notion/NOTION_AUDIT_REPORT.md`

### Task 1.1: Script Inventory & Code Audit
- **Resource:** `scripts/*.py` (read)
- **Estimated Duration:** 60 minutes

**Actions:**
1. List all Python files in `scripts/` directory
2. Grep each file for Notion API calls:
   - `create_page`
   - `create_database`
   - `duplicate`
   - `append_block_children`
3. Document which scripts call these functions
4. Extract line numbers and context
5. Create table: `SCRIPT_NAME | FUNCTION_CALLED | LINE_NUMBER | PURPOSE`
6. Log completion

**Output:** Section 1 of audit report with dangerous code inventory

---

### Task 1.2: Page Creation Impact Assessment
- **Resource:** Notion API (read-only, if access granted)
- **Estimated Duration:** 60 minutes

**Actions:**
1. Request human to share Notion workspace access
2. If granted: Query for pages created by integration
3. Count total pages created
4. Categorize pages:
   - Legitimate (team pages, project pages)
   - Duplicates (multiple pages same content)
   - Test/Debug (clearly experimental)
   - Unknown (can't determine purpose)
5. Document page IDs and titles
6. Create deletion recommendation list
7. Log completion

**Output:** Section 2 of audit report with page inventory and deletion plan

---

### Task 1.3: Script Lockdown (Immediate Safety Measure)
- **Resource:** `scripts/*.py` (write - add warnings only)
- **Estimated Duration:** 30 minutes

**Actions:**
1. For each dangerous script identified:
   - Add comment at top: `# ⚠️ WARNING: Creates Notion pages - DO NOT RUN without approval`
   - Add runtime check: `if not os.getenv('ALLOW_PAGE_CREATION'): raise Exception('...')`
   - Consider renaming: `script.py` → `script.UNSAFE.py`
2. Document changes made
3. Commit with clear message about safety lockdown
4. Log completion

**Output:** Scripts locked down, cannot create pages accidentally

---

### Task 1.4: Audit Report Assembly
- **Resource:** Previous outputs
- **Estimated Duration:** 30 minutes

**Actions:**
1. Combine sections into `docs/notion/NOTION_AUDIT_REPORT.md`
2. Add executive summary
3. Create clear recommendations:
   - Scripts to disable/archive
   - Pages to delete (for human approval)
   - Refactoring priorities
4. Flag for human review
5. Log completion

**Output:** Complete audit report ready for human review

---

## PHASE 2: DATABASE SCHEMA VALIDATION (PRIORITY: HIGH)

**Goal:** Ensure all required tables exist for agent coordination and LMS  
**Duration:** 2-3 hours  
**Human Approval:** NOT REQUIRED  
**Deliverable:** Complete database schema with all tables

### Task 2.1: Agent Coordination Tables
- **Resource:** Database (write)
- **Estimated Duration:** 60 minutes

**Actions:**
1. Check if `ascent_basecamp_agent_log` table exists
2. If exists, verify columns:
   - `agent_name`, `current_task`, `status`
   - `resource_claim` (NEW - may be missing)
   - `session_id` (NEW - may be missing)
   - `check_in_time`, `next_check_in` (NEW - may be missing)
3. Add missing columns with ALTER TABLE
4. Create `technical_decisions` table (per canon spec):
   ```sql
   CREATE TABLE IF NOT EXISTS technical_decisions (
       decision_id SERIAL PRIMARY KEY,
       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       agent_name VARCHAR(100),
       decision_type VARCHAR(100),
       decision TEXT NOT NULL,
       rationale TEXT,
       alternatives_considered TEXT,
       impact VARCHAR(50),
       status VARCHAR(50) DEFAULT 'proposed',
       metadata JSONB
   );
   ```
5. Create `error_log` table (per canon spec)
6. Add indexes for performance
7. Test inserts/queries
8. Log completion

**Output:** All agent coordination tables exist and functional

---

### Task 2.2: LMS Tables Validation
- **Resource:** Database (write), Beta's requirements
- **Estimated Duration:** 60 minutes

**Actions:**
1. Check for required LMS tables (coordinate with Beta via agent_log):
   - `learner_performance`
   - `subsystem_competency`
   - `race_metadata`
   - `ghost_cohorts`
   - `modules`, `module_sections`
2. For each missing table, create with proper schema
3. Add foreign key constraints
4. Add indexes for common queries
5. Test with sample data
6. Notify Beta in agent_log when complete
7. Log completion

**Output:** All LMS tables exist, Beta can proceed with testing

---

### Task 2.3: Data Integrity & Performance
- **Resource:** Database (optimize)
- **Estimated Duration:** 30 minutes

**Actions:**
1. Add foreign key constraints where missing
2. Create indexes for:
   - `modules.subsystem`
   - `learner_performance.student_id`
   - `ghost_cohorts.module_id`
3. Run VACUUM ANALYZE on Neon database
4. Test query performance
5. Log completion

**Output:** Optimized database with proper constraints

---

## PHASE 3: GHOST COHORT DATA PIPELINE (PRIORITY: HIGH)

**Goal:** Populate historical performance data for race mode  
**Duration:** 3-4 hours  
**Human Approval:** NOT REQUIRED for data extraction, helpful for validation  
**Deliverable:** Populated `ghost_cohorts` table

### Task 3.1: Historical Data Analysis
- **Resource:** `cadence_tasks` table (read), Database (analyze)
- **Estimated Duration:** 90 minutes

**Actions:**
1. Query `cadence_tasks` for historical completion data
2. Group by semester/university:
   - Fall 2022, Spring 2023, Fall 2023, etc.
3. For each cohort, calculate:
   - Fast benchmark (25th percentile time)
   - Medium benchmark (50th percentile)
   - Slow benchmark (75th percentile)
4. Group by subsystem (Power, Structures, etc.)
5. Create cohort profiles with metadata
6. Document data quality issues
7. Log completion

**Output:** Cohort data ready for insertion

---

### Task 3.2: Ghost Cohort Table Population
- **Resource:** `ghost_cohorts` table (write)
- **Estimated Duration:** 60 minutes

**Actions:**
1. For each historical cohort:
   - Insert cohort metadata (name, semester, university)
   - Insert benchmark times per module/subsystem
   - Add team size, completion rate
2. Aim for 3-5 representative cohorts
3. Validate data integrity
4. Test queries Beta's endpoint will use
5. Notify Beta in agent_log when data available
6. Log completion

**Output:** `ghost_cohorts` table populated with historical data

---

### Task 3.3: API Endpoint Coordination
- **Resource:** Beta's endpoint (test), Database (verify)
- **Estimated Duration:** 30 minutes

**Actions:**
1. Test Beta's `/modules/{id}/ghost_cohorts` endpoint
2. Verify data format matches Beta's expectations
3. Check query performance
4. Add caching recommendations if slow
5. Document expected API response format
6. Log completion

**Output:** Ghost cohort data accessible via API

---

## PHASE 4: NOTION SYNC REFACTOR (BLOCKED until human provides templates)

**Goal:** Rewrite sync scripts to fill templates, NOT create pages  
**Duration:** 4-5 hours  
**Human Approval:** REQUIRED for template access and refactor design  
**Deliverable:** `scripts/notion_continuous_sync.py` in template-only mode

### Task 4.1: Wait for Human Approval & Template Info
- **Resource:** AGENT_TEAM_CHAT.md (monitor)
- **Status:** BLOCKED

**Waiting for:**
1. Audit report review and approval
2. Page deletion approval
3. Premade template locations
4. Template structure (coordinate with Beta)
5. Single dashboard design preferences

**Actions while blocked:**
- Complete Phase 2 and 3 work
- Answer human questions about audit
- Prepare refactor design

---

### Task 4.2: Sync Script Refactor (After Approval)
- **Resource:** `scripts/notion_continuous_sync.py` (rewrite)
- **Estimated Duration:** 3 hours

**Actions:**
1. Remove ALL page/database creation code
2. Implement template-filling approach:
   - Read premade template structure
   - Query database for current data
   - Update existing page properties only
   - Validate before write (no structure changes)
3. Add comprehensive error handling
4. Add logging to file
5. Test in read-only mode first
6. Get human review before deployment

**Output:** Refactored sync script (template-only mode)

---

### Task 4.3: Single Dashboard Consolidation
- **Resource:** Notion template (write to properties)
- **Estimated Duration:** 90 minutes

**Actions:**
1. Work with human to understand dashboard layout
2. Design data pipeline: DATABASE → Dashboard Template
3. Implement update logic for:
   - Team data
   - Project status
   - Student progress
   - Module library
4. Schedule sync frequency (every 5 minutes?)
5. Test with real data
6. Monitor for 24 hours

**Output:** Single consolidated dashboard, auto-updated from database

---

## Coordination with Other Agents

### Messages for Agent Alpha
- "Database schema ready - modules table validated"
- "Ghost cohort table structure ready for your race metadata"
- "Let me know when modules need new subsystem fields"

### Messages for Agent Beta
- "Created missing LMS tables: [list]"
- "Ghost cohort data populated and tested"
- "Will coordinate on Notion template structure once human provides access"

### Conflict Avoidance
- Only Gamma writes to `scripts/*` directory
- Only Gamma modifies database schema (tables, indexes)
- Beta reads ghost_cohorts (Gamma writes)
- Use agent_log to coordinate Notion API access

---

## Success Criteria

**Phase 1 Complete:**
- ✅ Complete audit report with all dangerous scripts identified
- ✅ Scripts locked down (cannot create pages accidentally)
- ✅ Page deletion plan documented
- ✅ Human review completed

**Phase 2 Complete:**
- ✅ All agent coordination tables exist
- ✅ All LMS tables exist (Beta notified)
- ✅ Database optimized with indexes

**Phase 3 Complete:**
- ✅ Ghost cohort data populated (3-5 cohorts)
- ✅ Data tested with Beta's API
- ✅ Performance validated

**Phase 4 Complete (after approval):**
- ✅ Notion sync refactored (template-only)
- ✅ No page creation possible
- ✅ Single dashboard operational

---

**Queue Status:** Updated 2025-11-30 by Agent Beta coordination  
**Next Review:** After Phase 1 audit completion

- **Estimated Duration:** 45 minutes

**Tasks:**
1. Test sync daemon with `--run` flag
2. Verify agent activity sync working
3. Verify all dashboard syncs working
4. Set up as background service (Windows Task Scheduler or nohup)
5. Add error logging to file
6. Create monitoring script to check daemon health
7. Log deployment

### Task 4: Sync Validation & Monitoring
- **Resource:** Notion dashboards (read)
- **Estimated Duration:** 30 minutes

**Tasks:**
1. Open Notion workspace
2. Verify real-time updates appear in Agent Activity Dashboard
3. Check data accuracy in Team/Project/Task dashboards
4. Test sync latency (should be <1 minute)
5. Document any issues
6. Log validation results

---

## Phase 2: Ghost Cohort System (Priority: HIGH)

### Task 5: Extract Historical Performance Data
- **Resource:** `scripts/extract_ghost_cohorts.py`
- **Estimated Duration:** 90 minutes

**Tasks:**
1. Analyze CADENCE historical data in cadence_tasks
2. Identify 3-5 representative cohorts (Fall 2022, Spring 2023, etc.)
3. Extract completion times per subsystem/task
4. Calculate fast/medium/slow benchmarks
5. Create cohort profiles (metadata: semester, university, team size)
6. Log extraction results

### Task 6: Populate Ghost Cohorts Table
- **Resource:** `ghost_cohorts` table (write)
- **Estimated Duration:** 60 minutes

**Tasks:**
1. Insert 3-5 ghost cohorts into database
2. For each cohort, add:
   - cohort_name (e.g., "Fall 2022 Structures Team")
   - semester
   - university
   - subsystem
   - performance_data (JSONB with timing benchmarks)
3. Validate data integrity
4. Log completion with cohort_ids

### Task 7: Build Ghost Cohort Query API
- **Resource:** `scripts/ghost_cohort_utils.py`
- **Estimated Duration:** 45 minutes

**Tasks:**
1. Create Python utility functions:
   - get_ghost_cohorts_for_module(module_id)
   - get_benchmark_times(module_id, difficulty)
   - get_cohort_leaderboard(subsystem)
2. Add caching for performance
3. Write unit tests
4. Document API for Beta to consume
5. Log completion

### Task 8: Notify Alpha & Beta
- **Resource:** `ascent_basecamp_agent_log`
- **Estimated Duration:** 5 minutes

**Tasks:**
1. Log 'complete' action for ghost cohort system
2. Message Alpha: "Ghost cohorts ready for race metadata"
3. Message Beta: "Ghost cohort API ready for endpoint integration"

---

## Phase 3: Difficulty Calibration System (Priority: MEDIUM)

### Task 9: Analyze Existing Module Complexity
- **Resource:** `scripts/analyze_module_difficulty.py`
- **Estimated Duration:** 60 minutes

**Tasks:**
1. Query modules table for all existing modules
2. Analyze module_sections for step count, complexity
3. Use heuristics to estimate difficulty:
   - Number of steps
   - Presence of simulations
   - Prerequisite depth
   - Estimated time
4. Generate difficulty recommendations
5. Log analysis results

### Task 10: Populate Difficulty Calibrations
- **Resource:** `module_difficulty_calibrations` table (write)
- **Estimated Duration:** 45 minutes

**Tasks:**
1. For each module, insert calibration record:
   - difficulty_level (beginner/intermediate/advanced)
   - average_time_seconds (estimated)
   - success_rate (default 0.85)
   - sample_size (0 initially)
2. Update modules table with difficulty tags
3. Log completion

### Task 11: Build Adaptive Difficulty System
- **Resource:** `scripts/adaptive_difficulty.py`
- **Estimated Duration:** 90 minutes

**Tasks:**
1. Create algorithm to update difficulty based on learner_performance
2. If success_rate < 70%, downgrade difficulty
3. If success_rate > 95%, upgrade difficulty
4. Adjust estimated times based on actual student data
5. Create cron job to run weekly
6. Log completion

---

## Phase 4: Simulation Environment Catalog (Priority: MEDIUM)

### Task 12: Document CircuitJS Configurations
- **Resource:** `scripts/catalog_simulations.py`, `simulation_environments` table
- **Estimated Duration:** 90 minutes

**Tasks:**
1. Research CircuitJS integration for avionics modules
2. Create sample circuit configurations
3. Document how to embed CircuitJS in modules
4. Insert records into simulation_environments:
   - name: "CircuitJS - I2C Pull-up Resistor"
   - type: "circuit_simulation"
   - subsystem: "avionics"
   - config_json: {circuit URL or config}
5. Log completion

### Task 13: Document LTSpice Setups
- **Resource:** `simulation_environments` table
- **Estimated Duration:** 90 minutes

**Tasks:**
1. Document LTSpice integration for power modules
2. Create example .asc files for EPS characterization
3. Document how to link LTSpice files to modules
4. Insert records into simulation_environments
5. Log completion

### Task 14: Document FreeCAD Workflows
- **Resource:** `simulation_environments` table
- **Estimated Duration:** 60 minutes

**Tasks:**
1. Document FreeCAD integration for structures modules
2. Create example part files
3. Document CAD tolerance design workflow
4. Insert records into simulation_environments
5. Log completion

---

## Phase 5: Data Pipeline Automation (Priority: LOW)

### Task 15: Scheduled Notion Sync
- **Resource:** Windows Task Scheduler / cron
- **Estimated Duration:** 30 minutes

**Tasks:**
1. Create scheduled task to run sync daemon on system boot
2. Add restart on failure
3. Configure logging to file
4. Test restart behavior
5. Log completion

### Task 16: Database Backup Script
- **Resource:** `scripts/backup_neon_db.py`
- **Estimated Duration:** 45 minutes

**Tasks:**
1. Create script to export Neon database to .sql file
2. Use pg_dump via DATABASE_URL
3. Compress and timestamp backups
4. Store in `backups/` directory
5. Create scheduled task (weekly)
6. Log completion

### Task 17: Agent Health Monitor
- **Resource:** `scripts/monitor_agents.py`
- **Estimated Duration:** 60 minutes

**Tasks:**
1. Create script to check agent activity
2. Query ascent_basecamp_agent_log for agents with no activity in 30+ min
3. Send alert if agent appears dead
4. Auto-release claimed resources from dead agents
5. Create scheduled task (every 15 minutes)
6. Log completion

---

## Handoff Scenarios

### Alpha Needs Ghost Cohorts
```sql
-- Check for Alpha's requests
SELECT * FROM ascent_basecamp_agent_log
WHERE action_type = 'help'
  AND metadata->>'help_needed_from' = 'gamma'
  AND message LIKE '%ghost%'
ORDER BY timestamp DESC;

-- Respond and claim task
INSERT INTO ascent_basecamp_agent_log (
    agent_name, action_type, status, message, metadata
) VALUES (
    'gamma', 'claim', 'working',
    'Prioritizing ghost cohort population for Alpha',
    '{"handoff_from": "alpha", "eta_minutes": 60}'::jsonb
);
```

### Beta Needs Infrastructure
```sql
-- Check for Beta's requests
SELECT * FROM ascent_basecamp_agent_log
WHERE action_type = 'help'
  AND metadata->>'help_needed_from' = 'gamma'
ORDER BY timestamp DESC;

-- Respond as needed
```

---

## Daily Summary Template

At end of session, append to AGENT_TEAM_CHAT.md:

```markdown
## Agent Gamma - Session #X

### What I Completed Today
- [Infrastructure tasks completed]
- [Tables populated: X records]
- [Scripts deployed]

### What I'm Working On Next
- [Next 3 tasks from queue]

### Messages for Other Agents
**To Alpha:** [Infrastructure status, data availability]
**To Beta:** [API readiness, sync status]

### Blockers
- [None / List]

### Metrics
- Database records created: N
- Scripts deployed: N
- Sync uptime: X%
- Time spent: X hours
```

---

## Success Metrics

**Week 1 Target:**
- Notion sync daemon running 24/7 with 99%+ uptime
- All 6 Notion dashboards live and syncing
- 3-5 ghost cohorts populated
- Agent monitoring active

**Month 1 Target:**
- Adaptive difficulty system operational
- 10+ simulation environments cataloged
- Database backup automation
- Agent health monitoring
- Complete data pipeline documentation

---

## Infrastructure Checklist

Before marking sync system complete:
- [ ] Notion API token refreshed
- [ ] All 6 databases created in Notion
- [ ] Sync daemon running as background service
- [ ] Real-time updates visible in Notion (<1 min latency)
- [ ] Error logging configured
- [ ] Health monitoring script deployed
- [ ] Documentation complete

---

## Monitoring Dashboard Goals

By end of Week 1, Liz should be able to open Notion and see:

1. **Agent Activity Dashboard**
   - All 3 agents' current status
   - What each is working on
   - Progress percentages
   - Last update timestamp

2. **Resource Claims Dashboard**
   - Active claims from each agent
   - No conflicts
   - ETAs for each task

3. **Team Dashboard**
   - 27 CADENCE people synced from database

4. **Project Dashboard**
   - 69 CADENCE projects synced

5. **Module Library**
   - Growing list of modules as Alpha creates them
   - Real-time updates

6. **Recent Activity Feed**
   - Live log of all agent actions
   - Scrollable history

---

**Status:** Waiting for agent to claim first task
**Next Action:** Refresh Notion API token and run database setup
