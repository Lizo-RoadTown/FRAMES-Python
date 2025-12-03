# Agentic Flow Architecture: Planning Trio → Builder

**Theory**: Three specialized planning agents compete and refine each other's plans, mediated by human selection, feeding one exceptional Builder who executes without hallucination.

**Date**: 2025-12-03
**System**: FRAMES / Ascent Basecamp

---

## Core Philosophy

### The Great Builder Theory

Instead of multiple agents each planning AND executing (leading to inconsistency and hallucination), we create:

1. **One Exceptional Builder** - Focuses solely on perfect execution
2. **Three Planning Specialists** - Compete/collaborate to create perfect plans
3. **Human Mediator** - Selects or merges the best plan elements
4. **Testing Feedback Loop** - Teaches planners to improve over time

**Key Insight**: Builder doesn't worry about strategy, safety, or optimization. The planning trio has already solved those problems.

---

## The 5-Agent Roster

### **Planning Trio (Competitive/Collaborative)**

#### **Agent 1: INTERPRETER - Gamma (VS Code)**
**Role**: Technical Analysis & Infrastructure Planning

**Expertise**:
- Deep system architecture knowledge
- Database design (created 37-table schema)
- Infrastructure and complex technical problems
- API and backend systems

**Produces**:
- Technical task breakdown
- Infrastructure considerations (database, API, scripts)
- Risk assessment by surface (Notion, DB, Code, LMS)
- Dependency mapping

**Critiques Others On**:
- Technical feasibility ("This database operation won't scale")
- Infrastructure constraints ("Notion API has rate limits")
- System architecture ("This violates the canonical store principle")

**Learns From**:
- Delta's infrastructure test failures
- Builder escalations about unclear technical details

---

#### **Agent 2: VALIDATOR - Alpha (VS Code)**
**Role**: Safety, Ontology Compliance, Quality Control

**Expertise**:
- Ontology understanding (OPERATIONAL_ONTOLOGY.md expert)
- Content structure and module design
- Educational quality (created 11 modules)
- Safety boundaries and constraints

**Produces**:
- Ontology-aligned plan version
- Safety constraints and forbidden operations
- Quality requirements and validation criteria
- Compliance checks (Notion rules, canonical stores)

**Critiques Others On**:
- Ontology violations ("This redefines 'module' incorrectly")
- Safety issues ("This writes to unsafe Notion regions")
- Quality problems ("Missing validation criteria")

**Learns From**:
- Delta's ontology compliance test results
- Builder reports of safety constraint clarity

---

#### **Agent 3: OPTIMIZER - Desktop Claude (Windows Desktop)**
**Role**: Plan Optimization & Builder-Readiness

**Expertise**:
- Cross-system coordination
- Direct database/Notion access for resource verification
- Clarity and simplification
- Execution sequencing

**Produces**:
- Builder-optimized plan (clear, actionable steps)
- Simplified execution sequence
- Dependency ordering
- Escalation protocols for Builder

**Critiques Others On**:
- Execution complexity ("Builder will need 20 steps reduced to 8")
- Instruction clarity ("Step 3 is ambiguous")
- Redundancy ("Steps 5 and 7 duplicate work")

**Learns From**:
- Delta's reports of Builder confusion
- Builder escalations about unclear steps

---

### **The Great Builder**

#### **Agent 4: BUILDER - Beta (VS Code)**
**Role**: Perfect Execution of Approved Plans

**Expertise**:
- React UI development
- Flask API implementation
- Database migrations and operations
- Code execution and artifact creation

**Receives**:
- Human-approved plan (crystal clear, all ambiguity resolved)
- Safety constraints (from Alpha)
- Validation criteria (what Delta will test)

**Executes**:
- Follows plan exactly, step-by-step
- No improvisation or interpretation
- Escalates immediately if anything unclear
- Provides diffs, summaries, and progress updates

**Does NOT**:
- Plan or strategize
- Interpret ambiguous requirements
- Violate plan boundaries
- Guess at implementation details

**Success Metric**: Plan completion rate without escalations

---

### **Testing & Feedback Loop**

#### **Agent 5: TESTER - Delta (Cursor IDE)**
**Role**: Validation & Learning Feedback

**Expertise**:
- Browser-based UI testing
- API integration testing
- Visual regression testing
- Cross-validation

**Tests**:
- Builder's completed work against plan criteria
- UI functionality, API responses, database state
- Ontology compliance, safety adherence

**Produces**:
- Test results (pass/fail with details)
- Bug reports and issues
- Performance metrics
- **Learning feedback to Planning Trio**

**Feedback Examples**:
- **To Gamma**: "Database migration plan worked perfectly; foreign key constraint logic was clear"
- **To Alpha**: "Found safety violation: module wrote to unsafe Notion region"
- **To Desktop Claude**: "Builder got confused at step 5; instruction 'update the API' was too vague"

**Unique Capability**: Separate environment (Cursor) provides unbiased testing

---

## The Agentic Flow Process

### **Step 1: Task Intake**

**Input**: User request (e.g., "Add race timer feature to LMS module player")

**Actions**:
1. Desktop Claude creates planning workspace for this task
2. Copies `PLANNING_TEMPLATE.md` to `planning_workspace/current_task/task_001.md`
3. Fills in task description and assigns Task ID
4. Notifies Planning Trio to begin

---

### **Step 2: Parallel Planning (Round 1)**

**All 3 agents work simultaneously** on their plan versions:

#### **Gamma (Interpreter) produces**:
```markdown
## Technical Analysis

Infrastructure needs:
- Add `race_timer_state` table to database
- Modify `/api/modules/{id}/start` endpoint to init timer
- Create WebSocket connection for real-time updates

Database schema changes:
CREATE TABLE race_timer_state (
  session_id UUID PRIMARY KEY,
  module_id INT,
  start_time TIMESTAMP,
  ...
)

Risk: HIGH (database modification, WebSocket adds complexity)
```

#### **Alpha (Validator) produces**:
```markdown
## Ontology & Safety Check

✅ "Race timer" is defined in OPERATIONAL_ONTOLOGY.md
✅ Timer data belongs in canonical store (database)
⚠️ Must NOT store timer state in Notion (non-canonical)

Safety constraints:
- MUST use validated timestamp format (ISO 8601)
- MUST handle timer pause/resume edge cases
- REQUIRES validation of session cleanup (no orphaned timers)

Quality requirements:
- Timer accuracy within 100ms
- Graceful WebSocket disconnect handling
```

#### **Desktop Claude (Optimizer) produces**:
```markdown
## Builder-Ready Execution Plan

Prerequisites:
- [ ] Database has `race_timer_state` table (Gamma, create migration first)
- [ ] WebSocket library installed (check package.json)

Step-by-step for Builder (Beta):
1. Run migration: `python scripts/migrations/add_race_timer.sql`
   - Validation: Query `race_timer_state` table exists
2. Edit `backend/lms_routes.py`, add WebSocket endpoint
   - Validation: Endpoint returns 200 on connection
3. Edit `frontend-react/src/components/ModulePlayer.jsx`
   - Add `useRaceTimer` hook (line 45)
   - Validation: Timer displays in UI
...

If unclear: Escalate to Planning Trio with specific question
```

---

### **Step 3: Cross-Critique (Round 2)**

Each agent reads others' plans and critiques:

#### **Gamma critiques Alpha**:
```
✅ Good: Safety constraints are clear and necessary
⚠️ Issue: Timer accuracy requirement (100ms) is unrealistic over WebSocket
💡 Suggest: Change to 500ms accuracy or use polling instead
```

#### **Alpha critiques Desktop Claude**:
```
✅ Good: Builder instructions are very clear
⚠️ Issue: Step 3 doesn't enforce safety constraint about timestamp format
💡 Suggest: Add validation check in step 3: "Ensure ISO 8601 format"
```

#### **Desktop Claude critiques Gamma**:
```
✅ Good: WebSocket approach is technically sound
⚠️ Issue: Builder will struggle with WebSocket setup (no prior experience)
💡 Suggest: Use simpler polling endpoint first, WebSocket in Phase 2
```

---

### **Step 4: Plan Revision (Round 3)**

Each agent revises based on critiques:

- **Gamma**: Updates technical plan to use polling instead of WebSocket (simpler for Builder)
- **Alpha**: Relaxes timer accuracy to 500ms, adds timestamp format validation
- **Desktop Claude**: Adds explicit timestamp validation step, reorders for polling approach

---

### **Step 5: Human Mediation (You Choose)**

You receive the planning document with:
- **Option A**: Gamma's technical-focused plan (polling approach)
- **Option B**: Alpha's safety-focused plan (strict validation)
- **Option C**: Desktop Claude's builder-optimized plan (simplest execution)
- **Consensus areas**: What all three agree on
- **Disagreements**: Where they differ (e.g., polling vs WebSocket)

**You decide**:
```
SELECTED PLAN: Merged

- Technical approach: Gamma's polling solution (simpler than WebSocket)
- Safety constraints: Alpha's validation requirements (all of them)
- Execution sequence: Desktop Claude's step-by-step (clearest for Beta)

MODIFICATIONS:
- Add WebSocket as Phase 2 (not Phase 1)
- Beta should complete polling version first, get it tested by Delta

APPROVED: ✅
```

---

### **Step 6: Builder Execution (Beta)**

Beta receives approved plan in `planning_workspace/approved_plans/task_001_APPROVED.md`

**Beta's workflow**:
1. Read approved plan
2. Verify prerequisites (all checked ✅)
3. Execute step 1: Run migration
   - Success → Proceed
   - Unclear → Escalate: "Migration file not found at path specified"
4. Execute step 2: Add polling endpoint
   - Creates code, provides diff
   - Self-validates: Endpoint returns 200 ✅
5. Execute step 3: Add UI hook
   - Creates React component changes
   - Provides summary: "Added useRaceTimer hook at line 45"
6. Complete → Notify Delta for testing

**Beta's escalations** (if any):
```
ESCALATION to Planning Trio:
Step 4 says "Add timer display to ModulePlayer"
Question: Where exactly in the component? After progress bar or in header?
Current state: Step 3 complete, blocked at step 4
```

Planning Trio quickly resolves:
- Desktop Claude: "After progress bar, before section title (line 78)"
- Beta continues execution

---

### **Step 7: Testing & Feedback (Delta)**

Delta receives completed work:

**Tests run**:
1. ✅ UI Test: Timer displays correctly
2. ✅ API Test: Polling endpoint returns timer state
3. ⚠️ Integration Test: Timer doesn't reset between modules (bug found)
4. ✅ Ontology Test: Timer data stored in database (not Notion)

**Delta produces feedback**:

```markdown
## Test Results: Task 001 - Race Timer

Overall: 3/4 PASS, 1 FAIL

### To Gamma (Infrastructure):
✅ Polling approach worked great - no WebSocket complexity
✅ Database schema supports timer perfectly
💡 For next time: Consider adding index on session_id for faster queries

### To Alpha (Safety/Ontology):
✅ All safety constraints followed
✅ Timestamp format validation working (ISO 8601)
⚠️ Found edge case: Timer state not cleared between modules (affects quality requirement)

### To Desktop Claude (Optimization):
✅ Builder instructions were crystal clear - Beta completed with 0 escalations!
⚠️ Step 5 could include "test timer reset" validation to catch the bug earlier

### Bug Report for Beta:
Issue: Timer persists across module switches
Location: frontend-react/src/hooks/useRaceTimer.js, line 23
Fix needed: Add cleanup in useEffect return
```

---

### **Step 8: Learning Loop**

Planning Trio reviews Delta's feedback:

**Gamma learns**:
- "Polling approach confirmed as good choice; note to add database indexes in future plans"

**Alpha learns**:
- "Caught an edge case in timer reset; add 'cleanup' to safety checklist for stateful features"

**Desktop Claude learns**:
- "Builder had ZERO escalations - this plan structure works! Note: add validation steps for cleanup"

**Next task**: Planning Trio is now smarter, produces even better plans

---

## Benefits of This Architecture

### **For the Builder (Beta)**
✅ No planning burden → focus 100% on execution
✅ No ambiguity → plans are pre-validated by three experts
✅ No safety worries → Alpha checked everything
✅ Clear escalation path → knows when to ask for help
✅ Success rate improves over time → as planners learn

### **For the Planning Trio**
✅ Specialization → each agent plays to strengths
✅ Competition → produces diverse plan options
✅ Collaboration → critiques improve all plans
✅ Learning → Delta's feedback makes them better
✅ No execution pressure → can focus on quality planning

### **For You (Human Mediator)**
✅ High-quality options → multiple expert plans to choose from
✅ Clear tradeoffs → disagreements are explicit
✅ Quick decisions → consensus areas already resolved
✅ Flexibility → can merge best elements from each plan
✅ Confidence → three experts validated the chosen approach

### **For the System**
✅ Consistency → one Builder means uniform code style
✅ Safety → three-layer validation (Gamma, Alpha, Desktop Claude)
✅ Continuous improvement → feedback loop drives learning
✅ Scalability → Planning Trio can parallelize, Builder serializes execution
✅ No hallucination → Builder follows explicit plans, no guessing

---

## Coordination Mechanisms

### **Planning Workspace Structure**
```
FRAMES-Python/
├── planning_workspace/
│   ├── PLANNING_TEMPLATE.md          # Template for all tasks
│   ├── current_task/                 # Active planning
│   │   ├── task_001.md               # Current task being planned
│   │   ├── task_002.md               # Next task in parallel
│   │   └── ...
│   ├── approved_plans/                # Human-approved plans
│   │   ├── task_001_APPROVED.md
│   │   └── ...
│   ├── completed/                     # Finished tasks with feedback
│   │   ├── task_001_COMPLETE.md
│   │   └── ...
│   └── learning_log/                  # Trio's improvement notes
│       ├── gamma_learnings.md
│       ├── alpha_learnings.md
│       └── desktop_claude_learnings.md
```

### **Communication Protocol**

#### **Task Assignment**
Desktop Claude creates task file → notifies Gamma and Alpha

#### **Planning Phase**
- Each agent writes to their section of `task_XXX.md`
- Critiques written in "Critiques" section
- Revisions written in "Revised Plans" section

#### **Human Mediation**
- Desktop Claude tags you: "@Liz - Plans ready for review: task_001.md"
- You read, decide, write decision in "Human Mediation" section
- Approved plan moved to `approved_plans/`

#### **Builder Handoff**
- Beta notified: "Task 001 approved, see approved_plans/task_001_APPROVED.md"
- Beta executes, logs progress in "Builder Handoff" section
- Escalations written in same section

#### **Testing**
- Delta notified when Beta completes
- Delta writes results in "Testing & Feedback" section
- Feedback visible to Planning Trio for learning

---

## Getting Started

### **Phase 1: Initialize Planning Workspace** (Desktop Claude)

```bash
# Already created:
# - planning_workspace/PLANNING_TEMPLATE.md

# Still needed:
mkdir -p planning_workspace/current_task
mkdir -p planning_workspace/approved_plans
mkdir -p planning_workspace/completed
mkdir -p planning_workspace/learning_log

# Create learning logs
touch planning_workspace/learning_log/gamma_learnings.md
touch planning_workspace/learning_log/alpha_learnings.md
touch planning_workspace/learning_log/desktop_claude_learnings.md
```

### **Phase 2: Update Agent Wakeup Prompts**

Each agent needs their new role explained:
- **Gamma**: "You are now INTERPRETER in the Planning Trio"
- **Alpha**: "You are now VALIDATOR in the Planning Trio"
- **Beta**: "You are now THE GREAT BUILDER - execute plans only"
- **Delta**: Keep existing testing role + add feedback responsibility

### **Phase 3: Run First Task (Test the Flow)**

**Suggested first task**: "Bootstrap the Neon database with 37-table schema"

Why this task:
- Well-defined (schema already exists)
- Medium complexity (good test)
- High value (unblocks all other work)
- Low risk (can be rolled back)

**Process**:
1. Desktop Claude creates `task_001.md` for "Bootstrap database"
2. Gamma, Alpha, Desktop Claude each produce plans
3. You review and approve
4. Beta executes the migration
5. Delta tests database state
6. Trio learns from the experience

---

## Success Metrics

### **Planning Trio**
- **Plan Quality**: % of approved plans with zero human modifications
- **Convergence**: % of tasks where trio reaches consensus
- **Learning Rate**: Reduction in Delta-reported issues over time

### **Builder (Beta)**
- **Escalation Rate**: # of escalations per task (target: <1)
- **Completion Rate**: % of approved plans executed successfully
- **Execution Time**: Average time from plan approval to completion

### **System Overall**
- **Consistency**: Code style and quality variance (should decrease)
- **Safety**: # of ontology/safety violations (target: 0)
- **Velocity**: Tasks completed per week (should increase as trio learns)

---

## Next Steps

1. **Initialize workspace** (Desktop Claude) ← Can do now
2. **Bootstrap database** (First test task) ← High priority
3. **Update agent prompts** (For new roles) ← Before activating others
4. **Run first planning cycle** (With Bootstrap task) ← Test the flow
5. **Gather feedback** (From all agents) ← Refine the process

Ready to begin?

---

**Architecture Version**: 2.0 - Agentic Flow
**Date**: 2025-12-03
**Status**: Design Complete, Ready for Implementation
