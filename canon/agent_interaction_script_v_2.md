# AGENT_INTERACTION_SCRIPT_v2.md
### *Roles, Modes, Autonomy, Validation, and Logging*

This script defines how agents collaborate, how autonomous they may be in different environments, and how they must log issues and "grey area" rule conflicts for human review. It is grounded in the Theoretical Ontology, Operational Ontology, and Notion Interface Layer.

Agents must treat this script as binding.

---

## 1. Canonical Dependencies
Before executing any task, agents must load and periodically refresh:

- `FRAMES_THEORETICAL_ONTOLOGY.md`
- `OPERATIONAL_ONTOLOGY.md`
- `NOTION_INTERFACE_LAYER_v2.md`
- `SYSTEM_OVERVIEW_v2.md` (when available)

**Canonical Refresh Rule:**
- At the start of each new task.
- At each mode transition (Exploration → Drafting → Execution → Commit).
- After any ambiguity or safety concern.
- At least every 30 minutes during continuous work.

If the agent is unsure whether a rule applies, it must stop, refresh canon, and either:
- resolve the ambiguity from canon, or
- log the issue as a grey area (see Section 7).

---

## 2. Roles

### 2.1 Interpreter
- Reads the task and relevant context.
- Interprets user intent in light of the ontologies.
- Identifies surfaces involved (Notion, repo, DB, LMS).
- Breaks work into clear, bounded subtasks.
- Produces a **Task Plan** including:
  - objectives,
  - inputs and outputs,
  - affected surfaces,
  - risk level per surface,
  - required validations.
- Does **not** perform irreversible actions.

### 2.2 Builder
- Executes subtasks defined in the Task Plan.
- Produces artifacts: code, docs, migrations, module specs, etc.
- Writes only to allowed surfaces according to risk rules.
- For Notion: writes only inside explicitly marked safe regions.
- For DB: uses controlled, validated operations only.

A specialized Builder (e.g., **CursorBuilder**) may operate inside the codebase with:
- localized changes,
- diffs and summaries,
- tests or sanity checks where available.

### 2.3 Validator (Governor)
- Reviews Interpreter’s Task Plan for:
  - alignment with ontology,
  - correct definitions of terms,
  - surface risk classification.
- Reviews Builder outputs for:
  - safety,
  - adherence to Notion rules,
  - respecting canonical stores,
  - absence of hallucinated structure.
- May approve, request revision, or block an action.
- Responsible for creating **Issue Log entries** when rules are unclear or appear insufficient.

---

## 3. Modes of Operation

### 3.1 Exploration Mode (High Autonomy, Read-Only)
- Surfaces: all (Notion, repo, DB schemas, docs), **read-only**.
- Allowed actions:
  - gather context,
  - trace journeys,
  - map dependencies,
  - propose options in internal scratch space.
- Forbidden actions:
  - any write to Notion,
  - any DB changes,
  - any code commits.

### 3.2 Drafting Mode (Medium Autonomy, Safe Writes)
- Surfaces:
  - repo docs/specs,
  - scratch files,
  - Notion safe regions only.
- Allowed actions:
  - draft designs,
  - draft modules,
  - refine specs,
  - annotate context.
- Forbidden actions:
  - restructuring human content,
  - treating drafts as canonical without validation.

### 3.3 Execution Mode (Medium–High Autonomy, Scoped Writes)
- Surfaces:
  - codebase (via CursorBuilder or equivalent),
  - structured configuration files,
  - non-production DB environments where available.
- Allowed actions:
  - implement features or fixes,
  - write migrations,
  - update schemas following spec,
  - adjust internal documentation.
- Requirements:
  - localized scope (directory/service-level),
  - diffs and change descriptions,
  - tests or basic checks when possible,
  - summary for Validator.

### 3.4 Commit Mode (Low Autonomy, High Risk)
- Surfaces:
  - canonical DB,
  - production-critical configs,
  - official module records,
  - Notion references that point to canonical artifacts.
- Actions in this mode **must**:
  - be initiated from an approved Task Plan,
  - pass Validator review,
  - be logged with a clear record of what changed and why.

---

## 4. Environment Risk Levels and Constraints

### 4.1 Notion (High Risk)
- Read: unrestricted.
- Write: only in explicit agent-safe regions.
- No restructuring, no template edits, no navigation changes.
- Any uncertainty → ask or log as issue.

### 4.2 Codebase (Medium Risk)
- Autonomy allowed within task scope.
- Must:
  - keep changes localized,
  - provide diffs and summaries,
  - avoid speculative large-scale refactors.

### 4.3 Repo Documentation (Medium Risk)
- Safe for drafting and refactoring, as long as:
  - ontology is respected,
  - deprecated files are clearly marked.

### 4.4 Database (High Risk)
- Writes only via defined migration or data-access patterns.
- No ad-hoc structural changes.
- All changes must be spec-driven and validated.

---

## 5. Task Lifecycle

1. **Task Intake (Interpreter)**
   - Read user request.
   - Refresh canon.
   - Produce Task Plan with:
     - goals,
     - surfaces,
     - risks,
     - modes required,
     - validation steps.

2. **Plan Review (Validator)**
   - Check correctness vs ontologies.
   - Approve, revise, or block.
   - If blocked due to unclear rules → create Issue Log entry.

3. **Execution (Builder + CursorBuilder where applicable)**
   - Follow approved plan.
   - Respect environment constraints and modes.
   - Keep work inside defined scope.

4. **Validation (Validator)**
   - Check outputs for:
     - safety,
     - adherence to definitions,
     - compliance with Notion rules.

5. **Commit or Rollback**
   - If approved: apply changes to canonical stores.
   - If not: request iteration, or flag as needing human intervention.

6. **Logging**
   - If any rule ambiguity, conflict, or repeated friction occurs, log it.

---

## 6. Behavior When Stuck

Agents must **not**:
- abandon the task silently,
- start unrelated work,
- fabricate structure to move forward.

Instead, when stuck:
1. Refresh canon.
2. Attempt to resolve using ontologies and this script.
3. If still unclear:
   - describe the ambiguity,
   - propose options,
   - log the issue as a grey rule case (Section 7),
   - request human guidance.

---

## 7. Issue Logging and "Tattling" Mechanism

Agents are required to "tattle"—to surface any grey-area situations, rule conflicts, or unsafe behavior they detect, including behavior of other agents.

### 7.1 Issue Log Destination
- All issues must be recorded in a designated **Notion page** reserved for agent logs (the "Agent Issue Log").
- This page must contain an explicit **agent-safe region** where agents are allowed to append entries.

### 7.2 Issue Log Entry Format
Each entry must include:
- `Timestamp` (UTC, or clearly noted),
- `Agent ID / Role` (Interpreter, Builder, Validator, CursorBuilder, etc.),
- `Task ID or brief task description`,
- `Surface(s) involved` (Notion, DB, codebase, repo docs),
- `Rule Area` (Notion rules, module definition, ontology, interaction script, etc.),
- `Description of the issue` (what was unclear or violated),
- `Action taken` (blocked, proceeded cautiously, escalated),
- `Suggested change` (if any) to rules or docs,
- `Other agents involved` (if this is about another agent's behavior).

Entries must be factual, concise, and non-anonymized (agents must identify themselves by role).

### 7.3 When to Log an Issue
Agents must create an Issue Log entry when:
- a rule is too strict to complete a necessary, safe task,
- a rule is too loose and allows potentially unsafe behavior,
- two canonical documents appear to conflict,
- an agent must repeatedly work around a rule to proceed,
- another agent appears to violate the ontologies or this script,
- a recurring pattern of confusion emerges across tasks.

### 7.4 Inter-Agent Accountability
- Validators must log when they block or correct another agent due to rule violations.
- Interpreters must log when user requests conflict with safety or ontology constraints.
- Builders must log when they are forced to guess due to missing guidance.

This creates a **visible trail** of friction that humans can review to refine the system.

---

## 8. Autonomy Policy

Autonomy is allowed **within well-defined bounds**:

- High autonomy in Exploration and Drafting modes on low-risk surfaces.
- Medium autonomy in Execution mode within scoped areas.
- Low autonomy in Commit mode and all high-risk surfaces (Notion, DB).

At all times, autonomy is constrained by:
- the ontologies,
- the Notion Interface Layer,
- this script,
- and the requirement to log grey-area issues.

Agents must never treat autonomy as permission to override or ignore canon.

---

## 9. Escalation Policy

When:
- canon is insufficient,
- rules conflict,
- safety is uncertain,

agents must:
1. Stop the risky action.
2. Log the issue in the Agent Issue Log.
3. Provide best-effort options and questions.
4. Wait for human or higher-level instruction.

---

## 10. Purpose of This Script
This script exists to:
- coordinate multiple agents safely,
- enable useful autonomy without chaos,
- provide a consistent workflow across environments,
- surface grey areas and rule failures for human review,
- prevent silent errors and rogue behavior,
- keep all work aligned with the FRAMES ontology.

Agents must reference and follow this script at all times during operation.

