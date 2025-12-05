# Omega-Delta Feedback & Learning System

**Purpose**: Define how Agent Omega and Agent Delta provide feedback to the Planning Trio (Alpha, Beta, Gamma) to enable continuous improvement of planning quality.

**Based on Canon**:
- `agent_issue_log_spec.md` - Structured issue reporting
- `agent_interaction_script_v_2.md` - Role definitions and coordination
- `canonical_refresh_policy.md` - When agents must re-read canon
- `negotiation_loop_one_script.py` - Planning negotiation structure

---

## 1. The Feedback Architecture

```
┌────────────────────────────────────────────────────┐
│        PLANNING TRIO (Negotiation Loop)            │
│                                                     │
│  Alpha (Content) ←→ Beta (Application) ←→ Gamma    │
│                     (Infrastructure)                │
│                                                     │
│  MAX_ROUNDS negotiation → produce 3 plans          │
└──────────────────┬─────────────────────────────────┘
                   ↓
         ┌─────────────────┐
         │  HUMAN (Liz)    │
         │  Selects Plan   │
         └────────┬────────┘
                  ↓
  ┌───────────────────────────────────────┐
  │     EXECUTION LAYER                   │
  │                                       │
  │  Omega: Backend, DB, Scripts          │
  │  Delta: Frontend, UI, Testing         │
  │                                       │
  │  Work separately OR together          │
  └──────────┬────────────────────────────┘
             ↓
   ┌──────────────────────────────────┐
   │  FEEDBACK COLLECTION             │
   │                                  │
   │  Omega logs: Execution issues    │
   │  Delta logs: Testing results     │
   │                                  │
   │  Both write to Issue Log         │
   └──────────┬───────────────────────┘
              ↓
   ┌────────────────────────────────────┐
   │  LEARNING LOOP                     │
   │                                    │
   │  Planning Trio reads feedback      │
   │  Adjusts negotiation for next task │
   │  Improves plan quality over time   │
   └────────────────────────────────────┘
```

---

## 2. Omega's Feedback Responsibilities

### **What Omega Reports**

As the Great Executor, Omega encounters issues during:
- Database operations
- Backend API implementation
- Infrastructure script execution
- Cross-system coordination

**Omega Must Log**:

#### **Category 1: Plan Ambiguity**
When plan instructions are unclear or incomplete:

```markdown
**To Planning Trio (via Agent Issue Log)**

Timestamp: 2025-12-03T15:30Z
AgentRole: Omega (Executor)
TaskSummary: Bootstrap Neon database with 37-table schema
Surfaces: Database
RuleArea: Agent Interaction Script - Plan Clarity
IssueType: UnclearDefinition
Description:
Step 3 of approved plan said "Run migration script". Plan did not
specify which script or path. Found 3 candidates:
  - scripts/migrations/bootstrap.sql
  - shared/database/bootstrap_db.py
  - backend/run_migration.py
Had to escalate to human for clarification (10 min delay).

ActionTaken: Escalated to human, received clarification, executed correct script
SuggestedChange:
Planning Trio should specify EXACT file paths in execution steps.
Format: "Run script: `scripts/migrations/bootstrap.sql`"

OtherAgentsInvolved: Gamma (Infrastructure planner)

**Direct Feedback**:
To Gamma: Your infrastructure plan was technically sound, but
execution step 3 needs exact file path. For next time: use backticks
with full path from repo root.
```

#### **Category 2: Technical Feasibility Issues**
When a plan step is technically impossible or has unforeseen constraints:

```markdown
**To Planning Trio (via Agent Issue Log)**

Timestamp: 2025-12-03T16:15Z
AgentRole: Omega (Executor)
TaskSummary: Populate ghost_cohorts table with historical data
Surfaces: Database
RuleArea: Module Definition - Ghost Cohorts
IssueType: TooStrict
Description:
Plan Step 5 required "Extract median completion times from modules
table for each subsystem". Discovered modules table doesn't have
completion_time field - only estimated_minutes. Cannot compute
actual medians without learner_performance data, which is empty.

ActionTaken: Populated ghost_cohorts with estimated data based on
estimated_minutes * 1.2 multiplier. Logged this as assumption.

SuggestedChange:
Planning Trio should verify data availability before designing
extraction logic. Gamma, please check table schemas during planning.

OtherAgentsInvolved: Gamma (DB schema), Alpha (module data owner)

**Direct Feedback**:
To Gamma: Database schema check needed during planning phase -
modules table missing completion_time field you assumed existed.
To Alpha: Ghost cohorts now populated with estimated data. Will need
real learner data to improve accuracy later.
```

#### **Category 3: Safety/Ontology Violations in Execution**
When Omega discovers the approved plan violates ontology rules during execution:

```markdown
**To Planning Trio (via Agent Issue Log)**

Timestamp: 2025-12-03T17:00Z
AgentRole: Omega (Executor)
TaskSummary: Set up Notion sync daemon for team lead monitoring
Surfaces: Notion, Database
RuleArea: Notion Interface Layer, Operational Ontology
IssueType: UnsafeBehaviorPrevented
Description:
Plan Step 6 instructed: "Create new Notion page for Agent Issue Log".
During execution, reviewed NOTION_INTERFACE_LAYER_v2.md (refresh at
surface escalation per CANONICAL_REFRESH_POLICY). Rules state:
"Agents may NOT create new pages unless explicitly instructed."
Human approval did not explicitly authorize page creation.

ActionTaken: Blocked action, escalated to human. Human confirmed page
should be created and marked agent-safe region. Executed with explicit
approval.

SuggestedChange:
Planning Trio: When plans involve Notion writes, explicitly state
whether page creation is approved or using existing page. Reference
NOTION_INTERFACE_LAYER in plan.

OtherAgentsInvolved: All planners (systemic issue)

**Note**: This was caught during my mandatory refresh before Notion
write. Planning Trio should also refresh during plan creation.
```

#### **Category 4: Successful Execution (Positive Feedback)**
When plans work perfectly:

```markdown
**To Planning Trio (Post-Task Summary)**

Task: Bootstrap Neon Database
Overall: ✅ SUCCESS - 37 tables created, all constraints validated

**To Gamma (Infrastructure)**:
✅ Migration script path was clear and correct
✅ Rollback strategy was documented and tested
✅ Table dependencies were in correct order
💡 Excellent: Including verification queries after each table creation
helped me confirm success immediately

**To Alpha (Content)**:
✅ Module schema matches MODULE_DEFINITION_v2 perfectly
✅ No conflicts with pedagogical requirements

**To Beta (Application)**:
✅ API table dependencies correct (learner_performance, race_sessions)
✅ Frontend will have all needed tables

**Execution Metrics**:
- Total time: 8 minutes
- Escalations: 0
- Rollbacks: 0
- Deviations from plan: 0

**Learning**: This is the plan quality we should aim for every time.
```

---

## 3. Delta's Feedback Responsibilities

### **What Delta Reports**

As the Builder and Tester in Cursor IDE, Delta encounters:
- Frontend implementation challenges
- UI/UX integration issues
- Testing failures
- Visual/interaction problems

**Delta Must Log**:

#### **Category 1: Frontend Plan Gaps**
When UI/UX details are missing from plan:

```markdown
**To Planning Trio (via Agent Issue Log)**

Timestamp: 2025-12-03T18:30Z
AgentRole: Delta (Builder/Tester)
TaskSummary: Implement race timer UI component
Surfaces: Codebase (frontend)
RuleArea: Agent Interaction Script - Plan Completeness
IssueType: UnclearDefinition
Description:
Plan specified "Add RaceTimer component to ModulePlayer". Did not
specify:
  - Where in component tree (before/after ProgressBar?)
  - Timer styling (colors, size, position)
  - Timer state persistence (localStorage? API?)
Had to make 3 design assumptions, tested with browser tools, iterated.

ActionTaken: Made reasonable assumptions, implemented, tested visually.
Timer works but may not match expected design.

SuggestedChange:
Beta (Application planner): Include UI placement details in plan.
Format: "Add RaceTimer component at line X, after ProgressBar"
Or provide wireframe/sketch reference.

OtherAgentsInvolved: Beta (should provide UI specs)
```

#### **Category 2: Integration Test Results**
After testing Omega's backend with Delta's frontend:

```markdown
**To Planning Trio (Post-Task Summary)**

Task: Race Timer Feature
Integration Test: ✅ PASS with 1 issue

**To Beta (Application)**:
✅ API endpoints worked as designed
⚠️ API response format issue: GET /api/race/status returns
`current_time` in seconds (integer). Frontend expected milliseconds.
Had to add conversion in frontend (x1000).

Suggested: Specify units in API contract during planning.

**To Omega (Executor)**:
✅ Backend implementation matched Beta's API spec exactly
💡 Your API testing with curl caught most issues before integration

**To Gamma (Infrastructure)**:
✅ Database schema supported all race timer operations
✅ No performance issues during polling (500ms interval)

**Test Results**:
- UI Tests: 5/5 PASS
- API Tests: 4/5 PASS (1 unit mismatch)
- Integration Tests: PASS after frontend adjustment
- Visual Regression: PASS

**Browser Testing Details**:
- Tested Chrome, Firefox, Safari
- Timer display consistent across browsers
- No JavaScript errors in console
```

#### **Category 3: Usability Findings**
When Delta discovers UX issues during browser testing:

```markdown
**To Planning Trio (via Agent Issue Log)**

Timestamp: 2025-12-03T19:45Z
AgentRole: Delta (Builder/Tester)
TaskSummary: Race timer UI testing
Surfaces: LMS (Student experience)
RuleArea: Module Definition - Learning Experience
IssueType: Other (UX Issue)
Description:
During browser testing with race timer active, noticed timer creates
anxiety - student might rush through content. Tested with 1000ms
polling: countdown was stressful. Students may skip reading carefully.

ActionTaken: Completed implementation as specified. Logging concern
for future consideration.

SuggestedChange:
Alpha (Content planner): Consider adding "learning mode" vs "race mode"
toggle. Race timer should be optional, not default.
Beta: UI could show "Take your time" mode vs "Race mode" selection.

OtherAgentsInvolved: Alpha (pedagogical concern), Beta (UI concern)

**Note**: This aligns with OPERATIONAL_ONTOLOGY principle: preserve
integrity of learning experience. Timer may interfere with deep learning.
```

---

## 4. The Agent Issue Log in Notion

### **Structure**

**Notion Page**: "FRAMES Agent Issue Log"

**Safe Region Marker**:
```
═══════════════════════════════════════════════════
AGENT SAFE REGION - Append entries below this line only
Do not modify anything above this line
═══════════════════════════════════════════════════
```

**Entry Format** (as Notion database or bulleted list):

Each entry must include:
- ✅ Timestamp (ISO 8601)
- ✅ AgentRole (Omega, Delta, Alpha, Beta, Gamma)
- ✅ TaskSummary (1-2 sentences)
- ✅ Surfaces (Notion/DB/Codebase/LMS)
- ✅ RuleArea (which canon document)
- ✅ IssueType (TooStrict/TooLoose/ConflictingRules/UnclearDefinition/Other)
- ✅ Description (3-6 sentences)
- ✅ ActionTaken (what agent did)
- ✅ SuggestedChange (how to improve)
- ✅ OtherAgentsInvolved (who else needs to know)

---

## 5. Omega-Delta Collaboration Modes (Trial Framework)

You asked about whether Omega and Delta should work:
1. **Completely separately** (parallel, independent)
2. **Together on same project** (sequential, coordinated)
3. **Learning from each other** (one at a time on same thing)

### **Collaboration Mode Options**

#### **Mode 1: Parallel Independent**
```
Task arrives → Approved plan splits work

Omega works on:          Delta works on:
- Database setup         - Frontend components
- Backend API            - UI testing
- Scripts                - Browser validation

No coordination during execution
Both report feedback independently at end
```

**Pros**:
- ✅ Fastest execution (parallel work)
- ✅ No blocking dependencies

**Cons**:
- ⚠️ Integration issues discovered late
- ⚠️ May duplicate effort
- ⚠️ Requires very clear interface contracts in plan

**Best for**: Tasks with clean frontend/backend separation

---

#### **Mode 2: Sequential Coordinated**
```
Task arrives → Approved plan sequences work

Phase 1: Omega executes backend/DB
  → Provides API endpoints, schemas
  → Delta receives specs

Phase 2: Delta builds frontend
  → Integrates with Omega's backend
  → Tests integration live

Phase 3: Delta tests, both report feedback
```

**Pros**:
- ✅ Clear dependencies respected
- ✅ Integration issues caught during development
- ✅ Delta can test Omega's work immediately

**Cons**:
- ⏱️ Slower (sequential, not parallel)
- ⚠️ Delta blocked if Omega encounters issues

**Best for**: Tasks with strong frontend→backend dependencies

---

#### **Mode 3: Paired Learning**
```
Task arrives → One agent executes, other observes

Iteration 1:
- Omega executes full task
- Delta watches, takes notes
- Delta writes detailed feedback on what was unclear

Iteration 2 (similar task):
- Delta executes full task
- Omega watches, takes notes
- Omega provides feedback on Delta's approach

Both agents learn from each other's execution style
```

**Pros**:
- ✅ Deep learning about each other's constraints
- ✅ Feedback is detailed and contextual
- ✅ Builds better mental models of each agent's needs

**Cons**:
- ⏱️ Very slow (one agent idle)
- ⚠️ Only works for learning/training tasks
- ⚠️ Not efficient for production work

**Best for**: Early system setup, training period, complex new task types

---

#### **Mode 4: Hybrid (Recommended)**
```
Task arrives → Approved plan determines mode

If clear separation:
  → Mode 1 (Parallel Independent)

If strong dependencies:
  → Mode 2 (Sequential Coordinated)

If new task type:
  → Mode 3 (Paired Learning) first iteration
  → Then Mode 1 or 2 for future similar tasks
```

**Strategy**:
1. **First 5 tasks**: Use Mode 3 (Paired Learning) to build shared understanding
2. **Next 10 tasks**: Use Mode 2 (Sequential) to establish reliable patterns
3. **Ongoing tasks**: Use Mode 1 (Parallel) when possible, Mode 2 when needed

---

## 6. Trial Framework: Testing Collaboration Modes

### **Experiment Design**

**Goal**: Determine optimal Omega-Delta collaboration mode for different task types

**Method**: Run same task type under different modes, measure outcomes

#### **Task Categories to Test**

1. **Pure Backend** (DB migrations, scripts)
   - Omega primary, Delta minimal involvement
   - Test: How useful is Delta's observation?

2. **Pure Frontend** (UI components, no backend changes)
   - Delta primary, Omega minimal involvement
   - Test: How useful is Omega's observation?

3. **Full Stack** (Backend + Frontend + Integration)
   - Test all 3 modes
   - Measure: Speed, quality, feedback richness

4. **Infrastructure** (Environment setup, Notion configuration)
   - Omega primary
   - Test: Delta's testing perspective value

#### **Metrics to Collect**

| Metric | Mode 1 | Mode 2 | Mode 3 |
|--------|--------|--------|--------|
| **Execution Time** | [Record] | [Record] | [Record] |
| **Escalations** | [Count] | [Count] | [Count] |
| **Integration Issues** | [Count] | [Count] | [Count] |
| **Feedback Quality** (1-5) | [Rate] | [Rate] | [Rate] |
| **Planning Trio Learning** (1-5) | [Rate] | [Rate] | [Rate] |
| **Human Intervention** | [Count] | [Count] | [Count] |

#### **Test Schedule**

**Week 1: Bootstrap Phase (Mode 3 - Paired Learning)**
- Task 1: Database bootstrap (Omega executes, Delta observes)
- Task 2: Frontend scaffolding (Delta executes, Omega observes)
- **Goal**: Build shared vocabulary, understand constraints

**Week 2: Coordination Phase (Mode 2 - Sequential)**
- Task 3: Ghost cohorts population + UI display
- Task 4: Notion sync setup + dashboard testing
- **Goal**: Establish handoff patterns

**Week 3: Parallel Phase (Mode 1 - Independent)**
- Task 5: Backend API + Frontend components (separate)
- Task 6: Module creation + Module player updates
- **Goal**: Maximize speed while maintaining quality

**Week 4: Evaluation**
- Review metrics
- Planning Trio votes on preferred mode
- Document findings in canon

---

## 7. Feedback Integration into Planning Loop

### **How Planning Trio Uses Feedback**

Based on `negotiation_loop_one_script.py`, the Planning Trio runs a negotiation loop with MAX_ROUNDS. Feedback from Omega/Delta should inform their next negotiation.

#### **Before Each Planning Session**

**Alpha, Beta, Gamma must**:
1. Read Agent Issue Log entries since last task
2. Identify patterns in feedback
3. Adjust their planning approach

**Example**:

```python
# Pseudocode for Planning Trio prep

def prepare_for_negotiation(agent_name):
    # Required by CANONICAL_REFRESH_POLICY
    refresh_canon_docs([
        'OPERATIONAL_ONTOLOGY.md',
        'MODULE_DEFINITION_v2.md',
        'agent_interaction_script_v_2.md'
    ])

    # Read feedback from Omega and Delta
    feedback_entries = read_issue_log(
        filters={
            'to_agent': agent_name,
            'since_last_task': True
        }
    )

    # Identify improvements needed
    for entry in feedback_entries:
        if entry['IssueType'] == 'UnclearDefinition':
            note_to_self(f"Be more specific about: {entry['Description']}")

        if entry['IssueType'] == 'TooStrict':
            note_to_self(f"Rules may be blocking safe work: {entry['SuggestedChange']}")

    return negotiation_context
```

#### **During Negotiation**

**Each agent incorporates feedback**:

```
Round 1:
Alpha: "Based on Delta's feedback from last task, I'm including
       UI placement specs in my plan this time."

Beta: "Omega flagged API unit ambiguity last time. My plan now
       specifies milliseconds vs seconds for all time fields."

Gamma: "Last task Omega couldn't find migration script. This plan
        includes EXACT file paths: `scripts/migrations/add_race_timer.sql`"
```

#### **After Negotiation**

**Agents update their learning logs**:

```markdown
# planning_workspace/learning_log/beta_learnings.md

## 2025-12-03 - Race Timer Task

Feedback received from Omega:
- API response units were ambiguous (seconds vs milliseconds)

Feedback received from Delta:
- UI placement details missing from plan

Changes applied:
- Created "API Contract Template" including units for all numeric fields
- Added "UI Placement Spec" section to application plans with line numbers

Result:
- Next task (Module Leaderboard) had ZERO escalations from Omega/Delta
- Plan quality score: 5/5
```

---

## 8. Mandatory Refresh Points (From Canon)

Based on `canonical_refresh_policy.md`, Omega and Delta MUST refresh canon at:

### **For Omega**:
1. ✅ **Task Start** - Read relevant canon before execution
2. ✅ **Surface Escalation** - Before any Notion write or DB migration
3. ✅ **Every 30 minutes** - During long tasks
4. ✅ **After Error** - When plan is unclear or blocking issue found

### **For Delta**:
1. ✅ **Task Start** - Read MODULE_DEFINITION_v2 before building modules
2. ✅ **Before Testing** - Refresh to know what "correct" looks like
3. ✅ **Every 30 minutes** - During continuous work
4. ✅ **After Finding Issue** - Before logging to Issue Log

### **For Planning Trio**:
1. ✅ **Before Negotiation** - All 3 agents refresh before planning
2. ✅ **Mode Transition** - When moving from one phase to next
3. ✅ **After Blocked Action** - When Omega/Delta escalate
4. ✅ **Every 30 minutes** - During long planning sessions

---

## 9. Summary: The Complete Feedback Loop

```
1. Task Arrives
   ↓
2. Planning Trio Negotiates (reads prior feedback first)
   ↓
3. Human Approves Plan
   ↓
4. Omega + Delta Execute (Mode 1, 2, or 3)
   ↓
5. During Execution:
   - Omega/Delta refresh canon at trigger points
   - Log issues to Agent Issue Log immediately
   ↓
6. After Execution:
   - Omega provides detailed feedback per category
   - Delta provides test results and UX findings
   ↓
7. Planning Trio Reviews Feedback
   - Updates learning logs
   - Adjusts approach for next task
   ↓
8. Next Task: Planning is better
   ↓
9. Continuous Improvement
```

---

## 10. Implementation Checklist

### **Setup Required (Omega to execute)**:

- [ ] Create Notion "FRAMES Agent Issue Log" page
- [ ] Mark agent-safe region for appending entries
- [ ] Share page ID with all agents
- [ ] Create learning log files:
  - [ ] `planning_workspace/learning_log/alpha_learnings.md`
  - [ ] `planning_workspace/learning_log/beta_learnings.md`
  - [ ] `planning_workspace/learning_log/gamma_learnings.md`
  - [ ] `omega_workspace/omega_feedback_log.md`
  - [ ] `delta_workspace/delta_feedback_log.md`

### **Process Required**:

- [ ] Document trial framework dates and task assignments
- [ ] Create feedback templates for Omega and Delta
- [ ] Train Planning Trio on reading Issue Log before negotiation
- [ ] Establish weekly review meetings to evaluate feedback patterns

---

## 11. Next Steps

**Immediate**:
1. Omega creates Notion Agent Issue Log page
2. Omega creates learning log directory structure
3. Run first task (Database Bootstrap) in **Mode 3 (Paired Learning)**
   - Omega executes, Delta observes
   - Delta provides detailed feedback
   - Both log to Issue Log

**This Week**:
- Complete 2 tasks in Mode 3
- Evaluate feedback quality
- Adjust templates if needed

**Next Week**:
- Transition to Mode 2 (Sequential)
- Test handoff patterns
- Measure speed vs quality tradeoff

**Long Term**:
- Establish default mode per task type
- Planning Trio consistently improves based on feedback
- Omega and Delta require fewer escalations over time

---

**Ready to implement?** Let me know which collaboration mode you'd like to start with for the first task!
