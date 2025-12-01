# Three-Agent Parallel Work Plan – Post-Canon Update
**Date:** 2025-11-30
**Status:** Ready for execution
**Agents:** Alpha, Beta, Gamma

---

## Executive Summary

The new canon documentation establishes a much stricter, cleaner architecture. This plan divides work into three **non-overlapping tracks** that can run in parallel without conflicts:

- **Agent Alpha (Module Specialist):** Module cleanup, template understanding, and canon-compliant module rebuilding
- **Agent Beta (Application Developer):** Frontend/backend cleanup and Student LMS feature completion
- **Agent Gamma (Infrastructure):** Notion template learning, dashboard fixes, and database maintenance

---

## Agent Alpha: Module Content & Cleanup Track

### Mission
Understand the new module schema, clean up obsolete modules, and learn to work with existing Notion templates rather than creating new pages.

### Branch: `alpha/module-cleanup-and-templates`

### Phase 1: Audit & Understanding (4-6 hours)
**Resource Claim:** `modules/*`, `templates/modules/*`, `docs/MODULE_SCHEMA.md`

#### Tasks:
1. **Read and internalize the module schema**
   - Study [MODULE_SCHEMA.md](../MODULE_SCHEMA.md) thoroughly
   - Compare against existing templates in `templates/modules/`
   - Understand the difference between old modules (DB IDs 71-82) and the new JSON-based schema

2. **Audit existing enhanced modules**
   - List all files in `modules/enhanced/` (currently ~60 modules from CADENCE)
   - Validate against MODULE_SCHEMA.md requirements
   - Create audit report: `docs/agents/MODULE_AUDIT_POST_CANON.md`
   - Flag modules missing required fields (learning_objectives, sections, etc.)

3. **Understand Notion template structure**
   - Request from human: Access to existing Notion module templates
   - Document the **exact layout** of pre-made templates
   - Create guide: `docs/agents/ALPHA_NOTION_TEMPLATE_GUIDE.md`
   - Learn to **fill in** templates rather than create new pages

4. **Database module cleanup**
   - Query database for modules created in old sessions (IDs 71-82)
   - Document what fields they're missing vs. new schema
   - Propose deprecation/migration strategy
   - Create SQL migration script: `database/migrations/deprecate_old_modules.sql`

#### Deliverables:
- `docs/agents/MODULE_AUDIT_POST_CANON.md` - Complete inventory of module status
- `docs/agents/ALPHA_NOTION_TEMPLATE_GUIDE.md` - How to use existing templates
- `database/migrations/deprecate_old_modules.sql` - Clean up old data
- Agent log entry documenting understanding of new schema

#### Messages for Other Agents:
**To Beta:** Will provide list of valid, canon-compliant modules for LMS testing
**To Gamma:** Need read-only access to Notion templates (page IDs) to document structure

---

### Phase 2: Template-Based Module Creation (6-8 hours)
**Resource Claim:** `modules/enhanced/*`, Notion templates (read/write)

#### Tasks:
1. **Create pilot module using template workflow**
   - Pick one CADENCE subsystem (e.g., "Power Subsystem Orientation")
   - Use existing Notion template (provided by human)
   - Fill in template sections with database-backed content
   - Export as JSON following MODULE_SCHEMA.md exactly
   - Save to `modules/enhanced/power-orientation.json`
   - Insert into database with proper metadata

2. **Build module creation workflow document**
   - Document step-by-step process for future modules
   - Include: Template selection → Content filling → Validation → DB insertion
   - Save as `docs/agents/ALPHA_MODULE_CREATION_WORKFLOW.md`
   - Include validation checklist from MODULE_SCHEMA.md

3. **Create 3-5 priority modules**
   - Focus on high-value CADENCE subsystems:
     - Power Subsystem Orientation
     - Avionics Fundamentals
     - GitHub Workflow for Teams
     - Safety & Mission Requirements
     - (One more TBD with human)
   - Each module must pass JSON validation
   - Each module references existing template in Notion (no new pages!)

#### Deliverables:
- 3-5 fully canon-compliant modules in `modules/enhanced/`
- `docs/agents/ALPHA_MODULE_CREATION_WORKFLOW.md`
- Database entries with all required metadata
- Notion templates filled (not created) with module content

#### Success Criteria:
- All modules validate against MODULE_SCHEMA.md
- No new Notion pages created (only existing templates used)
- Database entries include: learning_objectives, sections, reflection_prompts, metadata
- Modules ready for Beta's LMS frontend testing

---

### Phase 3: Module Enhancement Pipeline (4-6 hours)
**Resource Claim:** `scripts/enhance_modules.py`, `modules/exports/*`

#### Tasks:
1. **Test enhancement script**
   - Review `scripts/enhance_modules.py` against new canon
   - Test validation mode: `python scripts/enhance_modules.py --validate`
   - Document any mismatches with MODULE_SCHEMA.md
   - Create issue report if script needs updating

2. **Enhance stub modules**
   - Identify "stub" modules in `modules/enhanced/` (minimal content)
   - Run enhancement pipeline to add missing sections
   - Validate output matches schema
   - Commit enhanced versions

3. **Create module dependencies map**
   - Extract prerequisites from all modules
   - Build dependency graph (can use mermaid.js)
   - Save to `docs/agents/MODULE_DEPENDENCIES.md`
   - Identify any circular dependencies or gaps

#### Deliverables:
- Updated enhancement script (if needed)
- Enhanced versions of stub modules
- `docs/agents/MODULE_DEPENDENCIES.md` with visual graph
- Validation report showing all modules pass schema check

---

## Agent Beta: Application Development & Cleanup Track

### Mission
Complete Student LMS features, clean up old documentation, and prepare frontend for module testing.

### Branch: `beta/lms-completion-and-cleanup`

### Phase 1: Documentation & Code Cleanup (3-4 hours)
**Resource Claim:** `docs/lms/*`, `docs/archive/*`, `frontend-react/*`

#### Tasks:
1. **Archive obsolete documentation**
   - Review all files in `docs/lms/` against new canon
   - Move outdated files to `docs/archive/` with timestamp
   - Update `canon/ARCHIVE_INDEX.md` with moved files
   - Create `docs/lms/README.md` pointing to canon sources

2. **Clean up frontend dependencies**
   - Review `frontend-react/package.json`
   - Remove unused dependencies
   - Update to latest stable versions (where safe)
   - Document any breaking changes

3. **Verify API alignment with canon**
   - Compare `backend/lms_routes.py` with [STUDENT_LMS.md](../../canon/STUDENT_LMS.md)
   - Ensure endpoints match canon-defined workflows
   - Remove any endpoints not in canon
   - Document API surface in `docs/lms/API_SURFACE.md`

#### Deliverables:
- Clean `docs/lms/` directory with clear README
- Updated `canon/ARCHIVE_INDEX.md`
- `docs/lms/API_SURFACE.md` matching canon
- Updated `frontend-react/package.json`

#### Messages for Other Agents:
**To Alpha:** Ready to test modules when you have canon-compliant content
**To Gamma:** Archiving old DB migration docs - see ARCHIVE_INDEX.md

---

### Phase 2: React Component Development (8-10 hours)
**Resource Claim:** `frontend-react/src/components/*`, `frontend-react/src/pages/*`

#### Tasks:
1. **Build supporting components** (from previous TODO)
   - `ModuleCard.jsx` - Display module metadata with competency indicators
   - `SubsystemNav.jsx` - Sidebar navigation by subsystem
   - `CompetencyBar.jsx` - Visual progress indicator
   - `LoadingSpinner.jsx` - Standard loading UI
   - `ProgressStepper.jsx` - Step-by-step indicator
   - `CheckValidation.jsx` - Interactive check/hint display
   - `RaceTimer.jsx` - Timer with ghost comparison
   - `HintTooltip.jsx` - Contextual help
   - `CelebrationModal.jsx` - Module completion celebration

2. **Integrate with useModulePlayer hook**
   - Connect components to existing hook logic
   - Test state management (timer, checks, progress)
   - Verify race mode functionality
   - Add error boundaries

3. **Create component storybook/documentation**
   - Document props for each component
   - Create usage examples
   - Save to `frontend-react/src/components/README.md`

#### Deliverables:
- 9 production-ready React components
- Integration with useModulePlayer hook
- Component documentation
- Passing ESLint/tests

---

### Phase 3: LMS Testing & Polish (4-6 hours)
**Resource Claim:** `frontend-react/src/*`, `backend/lms_routes.py`

#### Tasks:
1. **Integration testing with real modules**
   - Load modules from Alpha's canon-compliant set
   - Test full workflow: start → progress → complete
   - Test race mode with ghost data (if Gamma provides)
   - Test leaderboard features

2. **Mobile responsiveness**
   - Test on various screen sizes
   - Adjust Tailwind classes for mobile-first design
   - Verify competency colors work on dark mode

3. **Error handling & edge cases**
   - Test with missing data
   - Test with network errors
   - Add retry logic where needed
   - User-friendly error messages

4. **Performance optimization**
   - Lazy load components
   - Optimize re-renders
   - Check bundle size

#### Deliverables:
- Fully functional Student LMS frontend
- Mobile-responsive design
- Comprehensive error handling
- Performance report

#### Success Criteria:
- Can load and complete a module end-to-end
- Race mode works with ghost data
- Mobile experience is smooth
- No console errors

---

## Agent Gamma: Infrastructure & Notion Integration Track

### Mission
Fix Notion dashboard integration, learn template structure, and maintain database infrastructure.

### Branch: `gamma/notion-templates-and-infrastructure`

### Phase 1: Notion Template Learning (4-6 hours)
**Resource Claim:** `scripts/notion_continuous_sync.py`, `.env`, Notion workspace

#### Tasks:
1. **Document existing Notion templates**
   - Request from human: List of pre-made template page IDs
   - For each template, document:
     - Page structure (headings, blocks, databases)
     - Property names and types
     - Expected content flow
   - Save to `docs/notion/NOTION_TEMPLATE_INVENTORY.md`

2. **Create template filling guide**
   - Document how to populate a template (vs. creating new page)
   - Show API calls for updating existing pages
   - Include code examples
   - Save to `docs/notion/NOTION_TEMPLATE_USAGE_GUIDE.md`

3. **Fix dashboard property mapping**
   - Work with human to get exact property names from dashboards
   - Update `scripts/notion_continuous_sync.py` with hard-coded mappings
   - Test sync to each dashboard
   - Document mapping in `docs/notion/NOTION_DASHBOARD_SCHEMA.md`

#### Deliverables:
- `docs/notion/NOTION_TEMPLATE_INVENTORY.md`
- `docs/notion/NOTION_TEMPLATE_USAGE_GUIDE.md`
- `docs/notion/NOTION_DASHBOARD_SCHEMA.md`
- Working sync daemon (at least for 2-3 dashboards)

#### Messages for Other Agents:
**To Alpha:** Template inventory ready - check NOTION_TEMPLATE_INVENTORY.md
**To Beta:** Dashboard sync working - activity logs should appear in Notion

---

### Phase 2: Dashboard Integration Fix (6-8 hours)
**Resource Claim:** `scripts/notion_continuous_sync.py`, Notion API

#### Tasks:
1. **Resolve API v2.7.0 property issue**
   - Research Notion's data-source query model
   - Implement workaround for missing schema endpoint
   - Test with all six dashboards:
     - Agent Activity
     - Resource Claims
     - Team
     - Projects
     - Tasks
     - Module Library

2. **Implement continuous sync mode**
   - Test `--run` mode with real data
   - Verify check-ins appear in Agent Activity
   - Verify resource claims populate correctly
   - Add error retry logic

3. **Create monitoring dashboard**
   - Build simple view showing sync status
   - Show last successful sync per dashboard
   - Display any errors
   - Save as Notion page (using template!)

#### Deliverables:
- Fully working sync daemon for all 6 dashboards
- Continuous mode running without errors
- Monitoring dashboard in Notion
- Error logs in database

---

### Phase 3: Database Maintenance & Optimization (4-6 hours)
**Resource Claim:** `shared/database/*`, Neon database

#### Tasks:
1. **Create missing tables from canon**
   - Review [DATABASE_SCHEMA.md](../../canon/DATABASE_SCHEMA.md)
   - Check which tables exist in Neon
   - Create SQL for missing tables (if any)
   - Execute migrations safely

2. **Populate ghost_cohorts table**
   - Create sample ghost data for race features
   - Populate with realistic timing data
   - Link to appropriate modules
   - Enable Beta's race mode testing

3. **Database health check**
   - Check indexes on common queries
   - Verify foreign key constraints
   - Check for orphaned records
   - Document in `docs/shared/DATABASE_HEALTH_REPORT.md`

4. **Backup strategy**
   - Document Neon backup configuration
   - Create manual backup script
   - Test restore procedure
   - Save to `docs/shared/BACKUP_STRATEGY.md`

#### Deliverables:
- All canon-required tables present
- `ghost_cohorts` populated with test data
- `docs/shared/DATABASE_HEALTH_REPORT.md`
- `docs/shared/BACKUP_STRATEGY.md`
- Working backup script

#### Success Criteria:
- All modules can query ghost data
- No database errors in application logs
- Backup tested and verified
- Performance acceptable (<100ms for common queries)

---

## Coordination & Communication

### Daily Check-ins
Each agent updates [AGENT_TEAM_CHAT.md](AGENT_TEAM_CHAT.md) with:
- Session number and date
- Completed tasks
- In-progress work
- Messages for other agents
- Blockers
- Metrics (files created, tests passing, etc.)

### Resource Claim Protocol
Before starting work, claim resource in database:
```python
claim_resource(agent_name='Alpha', resource='modules/enhanced', estimated_minutes=60)
```

Check for conflicts:
```python
check_active_claims(agent_name='Alpha')
```

Release when done:
```python
release_resource(agent_name='Alpha', resource='modules/enhanced', outcome='5 modules created')
```

### Handoff Points

**Alpha → Beta:**
- When canon-compliant modules ready for testing
- Notify via agent_log and AGENT_TEAM_CHAT.md
- Provide module IDs and JSON file paths

**Gamma → Alpha:**
- When template inventory complete
- Provide template page IDs
- Share dashboard access patterns

**Gamma → Beta:**
- When ghost_cohorts populated
- When dashboards syncing correctly
- Share database connection patterns

**Beta → Gamma:**
- Report any database performance issues
- Share API usage patterns for optimization
- Request additional ghost data if needed

### Blocker Resolution
If blocked:
1. Log to database: `log_error(agent_name, error_type, message, severity)`
2. Post to AGENT_TEAM_CHAT.md with clear blocker description
3. Tag which agent can help (if known)
4. Continue with non-blocked tasks
5. Check back every 2 hours for resolution

---

## Success Metrics

### Agent Alpha
- ✅ 5+ canon-compliant modules in `modules/enhanced/`
- ✅ All modules validate against MODULE_SCHEMA.md
- ✅ Zero new Notion pages created (only templates used)
- ✅ Module audit report complete
- ✅ Workflow documentation for future module creation

### Agent Beta
- ✅ All 9 supporting components built and tested
- ✅ Student LMS works end-to-end
- ✅ Mobile-responsive and accessible
- ✅ Old docs archived per canon rules
- ✅ API surface documented and canon-aligned

### Agent Gamma
- ✅ All 6 dashboards syncing correctly
- ✅ Template inventory documented
- ✅ ghost_cohorts populated for race mode
- ✅ Database health report shows no issues
- ✅ Backup strategy tested and documented

### Overall System
- ✅ No resource conflicts between agents
- ✅ All work aligned with canon documentation
- ✅ Human can see progress via Notion dashboards
- ✅ Student LMS ready for user testing
- ✅ Module creation pipeline ready for scaling

---

## Human Intervention Points

These require human approval/input:

1. **Module template access** (Alpha needs this first)
   - Provide Notion page IDs for module templates
   - Or describe how to find them in workspace

2. **Dashboard property verification** (Gamma needs this first)
   - Manually verify property names in 6 dashboards
   - Or grant Gamma permission to recreate them

3. **Module prioritization** (Alpha Phase 2)
   - Which 5 modules should Alpha create first?
   - Any specific CADENCE subsystems to prioritize?

4. **Deployment readiness** (Beta Phase 3)
   - When to deploy Student LMS for user testing?
   - Which students/teams for pilot testing?

5. **Database migrations** (Gamma Phase 3)
   - Approve any schema changes
   - Review backup strategy before implementation

---

## Timeline Estimate

**Parallel execution:** All agents working simultaneously

| Phase | Alpha | Beta | Gamma | Wall Time |
|-------|-------|------|-------|-----------|
| Phase 1 | 4-6h | 3-4h | 4-6h | **1-2 days** |
| Phase 2 | 6-8h | 8-10h | 6-8h | **2-3 days** |
| Phase 3 | 4-6h | 4-6h | 4-6h | **1-2 days** |
| **Total** | 14-20h | 15-20h | 14-20h | **4-7 days** |

If working in 4-hour sessions, each agent completes in ~5 sessions.

---

## Next Steps

1. **Human:** Review and approve this plan
2. **Human:** Provide template access info to Alpha & Gamma
3. **Human:** Wake Gamma and Beta with same context
4. **All Agents:** Check in to AGENT_TEAM_CHAT.md
5. **All Agents:** Claim Phase 1 resources
6. **All Agents:** Begin work on non-conflicting tasks

Ready to execute! 🚀
