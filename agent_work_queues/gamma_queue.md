# Agent Gamma Work Queue
## Infrastructure & Data Pipeline Specialist

**Agent Role:** Build data infrastructure, sync systems, and automation
**Resource Claims:** `scripts/*` (write), `ghost_cohorts` (write), `notion_sync_metadata` (write)

---

## Current Status: Ready to Start

### Session Start Checklist
- [ ] Log startup to ascent_basecamp_agent_log
- [ ] Read AGENT_TEAM_CHAT.md for context
- [ ] Check for resource conflicts in agent_log
- [ ] Claim first resource from queue below
- [ ] Begin work with logging every 10 minutes

---

## Phase 1: Notion Sync Infrastructure (Priority: CRITICAL)

### Task 1: Refresh Notion API Token
- **Resource:** `.env` file, Notion integration
- **Estimated Duration:** 15 minutes

**Tasks:**
1. Go to Notion integrations page
2. Regenerate API token
3. Update NOTION_API_KEY in .env
4. Test connection with simple API call
5. Log success

### Task 2: Set Up Notion Databases
- **Resource:** Notion workspace (via API)
- **Estimated Duration:** 30 minutes

**Tasks:**
1. Run `python scripts/notion_continuous_sync.py --setup`
2. Verify all 6 databases created:
   - Agent Activity Dashboard
   - Resource Claims
   - Team Dashboard
   - Project Dashboard
   - Task Dashboard
   - Module Library
3. Note database IDs in .env
4. Log completion with database IDs

### Task 3: Deploy Continuous Sync Daemon
- **Resource:** `scripts/notion_continuous_sync.py`
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
