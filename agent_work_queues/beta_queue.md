# Agent Beta Work Queue
## Student Platform Developer

**Agent Role:** Build student-facing learning platform (API + Frontend)
**Resource Claims:** `backend/lms_routes.py` (write), `frontend/*` (write)

---

## Current Status: Ready to Start

### Session Start Checklist
- [ ] Log startup to ascent_basecamp_agent_log
- [ ] Read AGENT_TEAM_CHAT.md for context
- [ ] Check for resource conflicts in agent_log
- [ ] Claim first resource from queue below
- [ ] Begin work with logging every 10 minutes

---

## Phase 1: LMS API Completion (Priority: CRITICAL)

### Endpoint 3: POST /students/{id}/modules/{module_id}/start
- **Resource:** `backend/lms_routes.py::start_module`
- **Estimated Duration:** 30 minutes

**Tasks:**
1. Create endpoint to log module start
2. Insert into learner_performance table
3. Return current attempt number
4. Add validation (module exists, student exists)
5. Write unit test
6. Log completion

### Endpoint 4: POST /students/{id}/modules/{module_id}/complete
- **Resource:** `backend/lms_routes.py::complete_module`
- **Estimated Duration:** 45 minutes

**Tasks:**
1. Create endpoint to log module completion
2. Update learner_performance table
3. Calculate mastery score
4. Update subsystem_competency table
5. Check if prerequisites unlocked new modules
6. Write unit test
7. Log completion

### Endpoint 5: POST /students/{id}/modules/{module_id}/log_activity
- **Resource:** `backend/lms_routes.py::log_activity`
- **Estimated Duration:** 30 minutes

**Tasks:**
1. Create endpoint for progress logging during module
2. Track time_spent, errors_count
3. Update learner_performance table
4. Add timestamp tracking
5. Write unit test
6. Log completion

### Endpoint 6: GET /modules/{id}/ghost_cohorts
- **Resource:** `backend/lms_routes.py::get_ghost_cohorts`
- **Estimated Duration:** 30 minutes
- **Dependency:** Gamma must populate ghost_cohorts table

**Tasks:**
1. Query ghost_cohorts table for module
2. Return benchmark times (fast/medium/slow)
3. Include cohort metadata (semester, university)
4. Add caching for performance
5. Write unit test
6. Log completion

### Endpoint 7: GET /students/{id}/leaderboard
- **Resource:** `backend/lms_routes.py::get_leaderboard`
- **Estimated Duration:** 45 minutes

**Tasks:**
1. Query learner_performance for module rankings
2. Calculate student position
3. Return top 10 + student position
4. Add filtering by subsystem/timeframe
5. Include ghost cohort comparisons
6. Write unit test
7. Log completion

### Endpoint 8: GET /students/{id}/subsystem_competency
- **Resource:** `backend/lms_routes.py::get_subsystem_competency`
- **Estimated Duration:** 30 minutes

**Tasks:**
1. Query subsystem_competency table
2. Calculate competency level (orientation/competency/integration/autonomy)
3. Return modules completed per subsystem
4. Include next recommended modules
5. Write unit test
6. Log completion

### Endpoint 9: POST /students/{id}/race/start
- **Resource:** `backend/lms_routes.py::start_race`
- **Estimated Duration:** 45 minutes

**Tasks:**
1. Create race session in database
2. Load ghost cohort data
3. Return race configuration (timer, checkpoints)
4. Initialize race state
5. Write unit test
6. Log completion

### Endpoint 10: POST /students/{id}/race/complete
- **Resource:** `backend/lms_routes.py::complete_race`
- **Estimated Duration:** 45 minutes

**Tasks:**
1. Record final race time
2. Compare to ghost cohorts
3. Update leaderboard
4. Calculate ranking
5. Return results with celebration metadata
6. Write unit test
7. Log completion

---

## Phase 2: API Testing & Documentation (Priority: HIGH)

### Task: Comprehensive API Testing
- **Resource:** `backend/test_lms_endpoints.py`
- **Estimated Duration:** 90 minutes

**Tasks:**
1. Write integration tests for all 10 endpoints
2. Test error handling (404, 400, 500)
3. Test authentication
4. Test edge cases (invalid student_id, non-existent module)
5. Run full test suite
6. Log results

### Task: API Documentation
- **Resource:** `docs/lms/API_REFERENCE.md`
- **Estimated Duration:** 60 minutes

**Tasks:**
1. Document all endpoints with examples
2. Add request/response schemas
3. Document error codes
4. Add Postman collection
5. Create quick start guide
6. Log completion

---

## Phase 3: React Frontend Scaffolding (Priority: HIGH)

### Task: Create React App Structure
- **Resource:** `frontend/*`
- **Estimated Duration:** 60 minutes

**Tasks:**
1. Run `npx create-react-app frontend-react`
2. Set up React Router
3. Configure Axios for API calls
4. Create base layout components
5. Set up state management (Context API)
6. Add Tailwind CSS
7. Log completion

### Task: Student Dashboard Layout
- **Resource:** `frontend/src/pages/Dashboard.jsx`
- **Estimated Duration:** 90 minutes

**Tasks:**
1. Create dashboard wireframe
2. Build navigation sidebar
3. Add subsystem selector
4. Create module grid/list view
5. Add progress indicators
6. Implement dark mode toggle
7. Log completion

---

## Phase 4: Module Player Component (Priority: CRITICAL)

### Task: Module Player UI
- **Resource:** `frontend/src/components/ModulePlayer.jsx`
- **Estimated Duration:** 2 hours

**Tasks:**
1. Create step-by-step interface
2. Add progress stepper component
3. Build check validation UI
4. Add hint/tooltip system
5. Create quiz/reflection forms
6. Add timer display (for race modules)
7. Test with real module data
8. Log completion

### Task: Module Player State Management
- **Resource:** `frontend/src/hooks/useModulePlayer.js`
- **Estimated Duration:** 90 minutes

**Tasks:**
1. Create custom hook for module state
2. Track current step, progress
3. Handle check validation
4. Manage timer for races
5. Log activity to API every 30 seconds
6. Add error recovery
7. Log completion

---

## Phase 5: Competition Features (Priority: MEDIUM)

### Task: Leaderboard Component
- **Resource:** `frontend/src/components/Leaderboard.jsx`
- **Estimated Duration:** 60 minutes

**Tasks:**
1. Create leaderboard table
2. Add filtering (subsystem, timeframe)
3. Highlight current student
4. Show ghost cohort comparisons
5. Add animations for rank changes
6. Log completion

### Task: Ghost Cohort Racing UI
- **Resource:** `frontend/src/components/GhostRace.jsx`
- **Estimated Duration:** 90 minutes

**Tasks:**
1. Create split-screen race view
2. Add progress bars for student + ghost
3. Show checkpoint indicators
4. Add "ahead/behind" messaging
5. Create finish line celebration
6. Log completion

### Task: Achievement Badges
- **Resource:** `frontend/src/components/Achievements.jsx`
- **Estimated Duration:** 60 minutes

**Tasks:**
1. Design badge system (first module, subsystem complete, etc.)
2. Create badge display component
3. Add unlock animations
4. Store badges in student profile
5. Log completion

---

## Handoff Scenarios

### Need More Modules from Alpha
```sql
INSERT INTO ascent_basecamp_agent_log (
    agent_name, action_type, status, message, metadata
) VALUES (
    'beta', 'help', 'waiting',
    'Frontend ready for testing - need more modules in [subsystem]',
    '{"help_needed_from": "alpha", "priority": "high"}'::jsonb
);
```

### Need Ghost Cohort Data from Gamma
```sql
INSERT INTO ascent_basecamp_agent_log (
    agent_name, action_type, status, message, metadata
) VALUES (
    'beta', 'help', 'blocked',
    'Race UI ready but ghost_cohorts table is empty',
    '{"help_needed_from": "gamma", "blocking_feature": "ghost_race"}'::jsonb
);
```

---

## Daily Summary Template

At end of session, append to AGENT_TEAM_CHAT.md:

```markdown
## Agent Beta - Session #X

### What I Completed Today
- Deployed [N] API endpoints: [list endpoints]
- Built [N] frontend components: [list components]
- Tests passing: [N/N]

### What I'm Working On Next
- [Next 3 tasks from queue]

### Messages for Other Agents
**To Alpha:** [Status update on module consumption]
**To Gamma:** [Requests for infrastructure/data]

### Blockers
- [None / List]

### Metrics
- API endpoints deployed: N
- Frontend components: N
- Test coverage: X%
- Time spent: X hours
```

---

## Success Metrics

**Week 1 Target:**
- All 10 API endpoints deployed and tested
- React app scaffolded
- Module player component functional

**Month 1 Target:**
- Complete student dashboard with module browsing
- Functional module player with step-by-step UI
- Leaderboard and ghost racing features
- 80%+ test coverage on API layer

---

## Testing Checklist

Before marking any endpoint complete:
- [ ] Unit test written and passing
- [ ] Integration test passing
- [ ] Error handling tested
- [ ] Postman collection updated
- [ ] Documentation updated
- [ ] Logged to ascent_basecamp_agent_log

---

**Status:** Waiting for agent to claim first task
**Next Action:** Claim `backend/lms_routes.py::start_module` and start Endpoint 3
