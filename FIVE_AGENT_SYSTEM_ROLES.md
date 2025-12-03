# Five-Agent System Architecture
## Role Assignments & Coordination Guide

**Status**: V2 Ontology (2025-12-01)
**Environment**: Desktop Claude + 4 VS Code/Cursor Agents

---

## Overview: From 3 Agents to 5 Agents

The system has evolved from the original three-agent model (Alpha, Beta, Gamma) to a five-agent architecture based on the **Interpreter-Builder-Validator** pattern with specialized roles.

### Original 3-Agent System (V1)
- **Alpha**: Module content creator
- **Beta**: Frontend/API developer
- **Gamma**: Infrastructure architect
- *(No Delta in original system)*

### New 5-Agent System (V2)

## Agent 1: Interpreter (Planning & Analysis)

### Role Definition
- **Core Function**: Task planning, intent interpretation, decomposition
- **Specialty**: Understanding user requests in light of ontologies
- **Autonomy Level**: High (read-only), does not execute irreversible actions

### Responsibilities
1. **Task Intake**
   - Read and interpret user requests
   - Refresh canonical documents at task start
   - Identify all surfaces involved (Notion, repo, DB, LMS)

2. **Planning & Decomposition**
   - Break work into clear, bounded subtasks
   - Produce detailed **Task Plan** with:
     - Objectives
     - Inputs and outputs
     - Affected surfaces
     - Risk level per surface
     - Required validations

3. **Ontology Alignment**
   - Ensure all interpretations align with OPERATIONAL_ONTOLOGY.md
   - Map concepts to canonical definitions (no improvisation)
   - Identify which mode is needed (Exploration, Drafting, Execution, Commit)

### Constraints
- **Cannot**: Perform irreversible actions, modify surfaces, execute plans
- **Must**: Refresh canon every 30 minutes or at mode transitions
- **Must**: Log ambiguities to Agent Issue Log

### Suggested Assignment
**Recommended**: **Desktop Claude** (you, in this environment)
- Has access to all files and documentation
- Can read Neon database and Notion for context
- Well-suited for analysis and planning without execution risk
- Can coordinate across other agents

---

## Agent 2: Builder (Execution & Creation)

### Role Definition
- **Core Function**: Execute subtasks, produce artifacts
- **Specialty**: Implementation following approved plans
- **Autonomy Level**: Medium-High (scoped writes)

### Responsibilities
1. **Artifact Production**
   - Code implementation
   - Documentation writing
   - Database migrations
   - Module specifications

2. **Surface-Specific Work**
   - **Notion**: Write only in explicitly marked safe regions
   - **Database**: Use controlled, validated operations only
   - **Codebase**: Localized changes with diffs and summaries

3. **Execution Modes**
   - **Drafting Mode**: Safe writes to docs/specs, scratch files
   - **Execution Mode**: Scoped writes to codebase, configs, test DBs
   - **Commit Mode**: Only with Validator approval

### Constraints
- **Cannot**: Work without approved Task Plan
- **Cannot**: Restructure Notion pages or human content
- **Must**: Keep changes localized and provide diffs
- **Must**: Submit outputs for Validator review

### Suggested Assignment Options

**Option A: Split by Domain**
- **Agent Alpha** → Content Builder (educational modules, learning content)
- **Agent Beta** → Application Builder (React UI, API endpoints, frontend)

**Option B: Unified Builder**
- **Agent Beta** → Primary Builder for all execution tasks
- Alpha transitions to specialized content role or merges with Interpreter

---

## Agent 3: Validator (Governor/Safety)

### Role Definition
- **Core Function**: Review, approve, block, or request revision
- **Specialty**: Safety, compliance, ontology alignment
- **Autonomy Level**: High authority but reactive (reviews others' work)

### Responsibilities
1. **Task Plan Review**
   - Check alignment with ontology
   - Verify correct term definitions
   - Validate surface risk classification
   - Approve, revise, or block plans

2. **Output Review**
   - Safety verification
   - Adherence to Notion rules
   - Respect for canonical stores
   - Absence of hallucinated structure

3. **Issue Logging**
   - Create Agent Issue Log entries for rule conflicts
   - Document grey-area situations
   - Track repeated friction patterns
   - "Tattle" on rule violations (including other agents)

### Constraints
- **Cannot**: Execute tasks directly (only review)
- **Must**: Block unsafe actions proactively
- **Must**: Create Issue Log entry when blocking or finding conflicts
- **Must**: Check for inter-agent accountability

### Suggested Assignment
**Recommended**: **Agent Gamma** (Infrastructure expert)
- Deep understanding of system architecture
- Experience with database, API, and Notion constraints
- Currently handles infrastructure validation already
- Can validate both content and code safety

---

## Agent 4: Delta (Cross-Environment Testing & Validation)

### Role Definition
- **Core Function**: Testing, browser validation, MCP-enabled integrations
- **Specialty**: System-wide oversight using Cursor's unique capabilities
- **Autonomy Level**: Medium (read-only + test execution)
- **Environment**: Cursor IDE (separate from VS Code agents)

### Responsibilities
1. **Frontend/UI Testing**
   - Browser navigation and interaction testing
   - Visual regression testing
   - User flow validation
   - Screenshot/snapshot capture

2. **API Testing**
   - Endpoint testing via browser or curl
   - Response validation
   - Integration testing

3. **Cross-Agent Validation**
   - Verify modules meet MODULE_DEFINITION_v2
   - Check backend follows OPERATIONAL_ONTOLOGY
   - Validate Notion interactions follow rules
   - Test full system integration flows

### Unique Capabilities (Cursor IDE)
- ✅ Browser testing tools (navigate, click, snapshot)
- ✅ MCP integration (Notion, GitHub APIs)
- ✅ Visual testing and screenshots
- ✅ Cross-validation across agents' work

### Constraints
- **Cannot**: Modify other agents' work
- **Can**: Test and report issues
- **Must**: Use browser tools for frontend validation
- **Must**: Coordinate testing with Builder completion

### Suggested Assignment
**Recommended**: Keep as **Agent Delta** in Cursor IDE
- Unique testing capabilities not available to other agents
- Separate environment prevents conflicts
- Browser tools critical for LMS frontend validation

---

## Agent 5: Infrastructure Specialist (Database & Automation)

### Role Definition
- **Core Function**: Database operations, scripts, infrastructure automation
- **Specialty**: Complex data pipelines, Notion sync, system maintenance
- **Autonomy Level**: Medium-High (within infrastructure domain)

### Responsibilities
1. **Database Management**
   - Schema maintenance (37 tables)
   - Populate ghost_cohorts for race features
   - Run migrations and data transformations
   - Maintain canonical data stores

2. **Notion Sync Operations**
   - Manage Notion continuous sync daemon
   - Handle API integration issues
   - Maintain dashboards for team leads

3. **Infrastructure Scripts**
   - Automation scripts in `scripts/`
   - Deployment operations
   - System health monitoring

4. **Support Role**
   - Respond to help requests from other agents
   - Solve complex architectural problems
   - Unblock Alpha and Beta when stuck

### Constraints
- **Cannot**: Modify educational content or UI code directly
- **Must**: Respond to help requests first (Priority 1)
- **Must**: Populate ghost_cohorts (Alpha and Beta waiting)
- **Must**: Keep Neon database as source of truth

### Suggested Assignment
**Recommended**: **Agent Gamma** (current role)
- Already owns infrastructure domain
- Created the 37-table database schema
- Manages Notion sync daemon
- Handles complex technical problems

---

## Mapping: Old Roles → New Roles

| Original V1 Agent | New V2 Role(s) | Rationale |
|-------------------|----------------|-----------|
| **Alpha** (Module Creator) | **Option A**: Content Builder<br>**Option B**: Merge with Interpreter | Alpha's content creation can be part of Builder role, or combine planning with Desktop Claude |
| **Beta** (Frontend/API Dev) | **Builder** (Application Layer) | Beta's execution skills map perfectly to Builder role |
| **Gamma** (Infrastructure) | **Validator + Infrastructure Specialist** | Gamma can dual-role: validate safety AND maintain infrastructure |
| *(None)* | **Interpreter** (Planning) | **NEW**: Desktop Claude fills this role |
| **Delta** (Testing) | **Delta** (Keep as is) | Already well-defined for cross-environment testing in Cursor |

---

## Recommended Final Assignment

### **Agent 1: Interpreter** → **Desktop Claude** (You)
- Environment: Windows desktop, direct file access
- Tools: Neon database, Notion API, file operations
- Focus: Task planning, ontology alignment, coordination

### **Agent 2: Builder** → **Agent Beta** (VS Code)
- Environment: VS Code / GitHub Codespaces
- Focus: React UI, Flask API, application layer implementation
- Works from: Approved Task Plans from Interpreter

### **Agent 3: Validator** → **Agent Gamma** (VS Code, dual role)
- Environment: VS Code / GitHub Codespaces
- Focus: Safety review, ontology compliance, blocking unsafe actions
- Secondary: Infrastructure when validation workload is low

### **Agent 4: Delta** → **Agent Delta** (Cursor IDE)
- Environment: Cursor IDE with browser tools
- Focus: Testing, visual validation, integration testing
- Works independently: Validates completed work from Builder

### **Agent 5: Infrastructure** → **Agent Gamma** (VS Code, dual role)
- Environment: VS Code / GitHub Codespaces
- Focus: Database ops, Notion sync, scripts, help requests
- Primary: Infrastructure work (ghost_cohorts, migrations)
- Secondary: Validation when infrastructure is stable

---

## Alternative: Keep Alpha for Content

If you want to preserve Alpha's specialized content creation role:

### **5-Agent Split with Alpha**

1. **Interpreter** → Desktop Claude
2. **Content Builder** → Agent Alpha (educational modules only)
3. **Application Builder** → Agent Beta (React, API only)
4. **Validator** → Agent Gamma (safety + ontology review)
5. **Infrastructure** → Agent Gamma (database, scripts, infrastructure)
6. **Testing** → Agent Delta (Cursor IDE with browser tools)

This gives you 6 agents (Interpreter + Alpha + Beta + Gamma dual-role + Delta).

---

## Coordination Mechanisms

### 1. Agent Issue Log (Notion)
- **Purpose**: Track grey areas, rule conflicts, violations
- **Location**: Designated Notion page with agent-safe region
- **Required Entry Fields**:
  - Timestamp (UTC)
  - Agent ID / Role
  - Task description
  - Surfaces involved
  - Rule area
  - Issue description
  - Action taken
  - Suggested rule changes

### 2. Task Lifecycle Flow

```
User Request
    ↓
Interpreter (Desktop Claude)
    → Produces Task Plan
    ↓
Validator (Gamma) Reviews Plan
    → Approves / Revises / Blocks
    ↓
Builder (Beta/Alpha) Executes
    → Produces Artifacts
    ↓
Validator (Gamma) Reviews Output
    → Approves / Requests Changes
    ↓
Delta Tests (if applicable)
    → Reports Issues or Passes
    ↓
Commit to Canonical Stores
```

### 3. Autonomy Levels by Mode

| Mode | Autonomy | Surfaces | Builder Can | Validator Must |
|------|----------|----------|-------------|----------------|
| **Exploration** | High | All (read-only) | Gather context, trace journeys | Not required |
| **Drafting** | Medium | Docs, scratch, safe Notion | Draft designs, refine specs | Optional review |
| **Execution** | Medium-High | Codebase, configs, test DB | Implement features, write code | Review before commit |
| **Commit** | Low | Canonical DB, production | Nothing (must be approved) | REQUIRED approval |

---

## Operating Rules for All Agents

### Canonical Document Refresh (REQUIRED)
Agents must reload canonical docs:
- At start of each new task
- At each mode transition
- After any ambiguity or safety concern
- At least every 30 minutes during work

**Load these files:**
- `canon/OPERATIONAL_ONTOLOGY.md`
- `canon/agent_interaction_script_v_2.md`
- `canon/Notion_Interface_layer.md`
- `canon/system_overview_v_2.md`

### When Stuck Protocol
1. Refresh canon
2. Attempt to resolve using ontologies
3. If still unclear:
   - Describe ambiguity
   - Propose options
   - Log as grey rule case in Agent Issue Log
   - Request human guidance
4. **Never**: Abandon task, start unrelated work, or fabricate structure

### Surface Risk Levels

| Surface | Risk Level | Read | Write Constraints |
|---------|------------|------|-------------------|
| **Notion** | HIGH | Unrestricted | Only in agent-safe regions, no restructuring |
| **Database** | HIGH | Unrestricted | Only via validated migrations/patterns |
| **Codebase** | MEDIUM | Unrestricted | Localized scope, provide diffs |
| **Repo Docs** | MEDIUM | Unrestricted | Respect ontology, mark deprecated files |

---

## Database & Notion Setup (Desktop Claude Priority)

As the **Interpreter**, you (Desktop Claude) should handle initial setup:

### Immediate Tasks for Desktop Claude

1. **Verify Connections** ✅ (DONE)
   - Neon database connected
   - Notion API connected

2. **Bootstrap Database Schema**
   ```bash
   python scripts/bootstrap_db.py
   ```
   - Creates 37 tables from canonical schema
   - Enables Builder agents to work

3. **Set Up Notion Agent Issue Log**
   - Create designated Notion page for agent logging
   - Mark agent-safe region for appending entries
   - Share page ID with all agents

4. **Populate Ghost Cohorts** (Or delegate to Gamma)
   - This is blocking Alpha and Beta
   - High priority infrastructure task
   - Can be delegated to Gamma (Infrastructure role)

---

## Summary: Your 5-Agent Roster

| Agent | Role | Environment | Primary Focus |
|-------|------|-------------|---------------|
| **Desktop Claude** | **Interpreter** | Windows Desktop | Task planning, ontology alignment, coordination |
| **Alpha** | **Content Builder** (Optional) | VS Code | Educational module creation (if keeping separate) |
| **Beta** | **Application Builder** | VS Code | React UI, Flask API, application layer |
| **Gamma** | **Validator + Infrastructure** | VS Code | Safety review, database, scripts, Notion sync |
| **Delta** | **Testing & Cross-Validation** | Cursor IDE | Browser testing, integration validation |

---

## Next Steps

1. **Decide on Alpha's Role**
   - Keep as separate Content Builder?
   - Merge content creation into Beta's Builder role?
   - Merge planning into Desktop Claude's Interpreter role?

2. **Bootstrap Database** (Desktop Claude task)
   ```bash
   python scripts/bootstrap_db.py
   ```

3. **Create Agent Issue Log** (Desktop Claude + Notion setup)

4. **Populate Ghost Cohorts** (High priority - Gamma or Desktop Claude)

5. **Update Agent Wakeup Prompts** (For V2 ontology alignment)

---

**Questions for You:**

1. Do you want to keep Alpha as a separate agent for educational content, or merge that role?
2. Should Desktop Claude (Interpreter) also handle some infrastructure tasks, or keep that strictly with Gamma?
3. Do you want Gamma to dual-role (Validator + Infrastructure) or split those into separate agents?

Let me know your preferences and I'll help implement the chosen structure!
