# CANONICAL_REFRESH_POLICY.md
### *When and How Agents Must Re-Read Canonical Documents*

This policy defines **explicit rules** for when agents must refresh their understanding of the FRAMES canon. It exists to prevent drift, conflicting behaviors, and unsafe autonomy during long or complex tasks.

Agents must treat this policy as binding.

---

## 1. Purpose

Language model agents do not have stable, long-term internal memory. Over time, their effective context drifts away from:
- the Theoretical Ontology,
- the Operational Ontology,
- the Notion Interface Layer,
- the Agent Interaction Script,
- the System Overview,
- the Module Definition.

Without periodic refresh, agents will:
- improvise rules,
- forget constraints,
- reintroduce deprecated patterns,
- and behave inconsistently across tasks.

This policy defines *when* and *how* to prevent that.

---

## 2. Canonical Set (What Must Be Refreshed)

The **canonical set** for refresh includes:

- `FRAMES_THEORETICAL_ONTOLOGY.md`
- `OPERATIONAL_ONTOLOGY.md`
- `NOTION_INTERFACE_LAYER_v2.md`
- `AGENT_INTERACTION_SCRIPT_v2.md`
- `SYSTEM_OVERVIEW_v2.md`
- `MODULE_DEFINITION_v2.md`

Additional domain-specific docs may be added over time, but these are the core.

Agents may refresh selectively (only the relevant documents) when appropriate, but must be aware of the whole set.

---

## 3. Mandatory Refresh Triggers

Agents must re-read relevant canonical documents at the following times:

### 3.1 Task Start
At the beginning of **every new task**:
- Interpreter must refresh the canonical set before creating a Task Plan.

### 3.2 Mode Transitions
Whenever the agent transitions between modes as defined in `AGENT_INTERACTION_SCRIPT_v2`:
- Exploration → Drafting,
- Drafting → Execution,
- Execution → Commit,

the responsible agent must refresh at least the Operational Ontology and the Interaction Script.

### 3.3 Time-Based Refresh
During continuous work on a task, agents must refresh:
- at least every **30 minutes** of active operation, and
- at any point of uncertainty or confusion.

If a task exceeds **2 hours** of elapsed time, Interpreter and Validator must both refresh the full canonical set.

### 3.4 Surface Escalation
Before interacting with high-risk surfaces:
- Notion (any write operation),
- Canonical database (any write or migration),
- Production-critical configuration,

agents must refresh:
- Operational Ontology,
- Notion Interface Layer (for Notion),
- relevant sections of System Overview and Module Definition (for DB/module writes).

### 3.5 After Error or Blocked Action
Whenever:
- Validator blocks an action due to rule violation or ambiguity,
- an error arises from unclear rules,
- an Issue Log entry is created,

involved agents must refresh the canonical set before continuing.

---

## 4. Refresh Procedure

When a refresh is triggered, the agent must:

1. **Identify which canonical docs are relevant** to the task and surface.
2. **Re-read those documents carefully**, focusing on:
   - definitions,
   - constraints,
   - risk levels,
   - allowed vs forbidden actions.
3. **Update their internal interpretation** of:
   - the task,
   - the surfaces involved,
   - the appropriate mode of operation.
4. **Adjust the Task Plan or current action** if any inconsistency is discovered.

If, after refresh, ambiguity persists:
- the agent must log the issue in the Agent Issue Log,
- and request human guidance.

---

## 5. Integration with the Agent Interaction Script

The `AGENT_INTERACTION_SCRIPT_v2.md` must:
- reference this policy explicitly,
- treat refresh steps as part of the Task Lifecycle,
- prevent any irreversible action from occurring without a prior refresh when required by this policy.

Interpreters, Builders, and Validators share responsibility for enforcing refresh behavior.

---

## 6. Responsibilities by Role

### 6.1 Interpreter
- Ensures refresh at task start and major re-interpretations.
- Checks that the Task Plan reflects current canon.

### 6.2 Builder
- Ensures refresh before high-risk writes.
- Confirms that execution matches the latest definitions and rules.

### 6.3 Validator
- Ensures refresh before validation decisions.
- Blocks actions when agents have not refreshed appropriately.
- Logs repeated failures to refresh as issues.

---

## 7. Logging Failures to Refresh

If an agent:
- acts in a way that clearly violates canon,
- or admits to having not refreshed when required,

Validators must:
- treat this as a **process failure**,
- create an entry in the Agent Issue Log,
- include:
  - which trigger was missed,
  - which surface was affected,
  - what harm was prevented or could have occurred.

This enables humans to see patterns in where refresh requirements are insufficient, unclear, or difficult to follow.

---

## 8. Evolution of this Policy

As the system matures, this policy may be updated to:
- add or remove canonical documents,
- tune time intervals,
- refine role responsibilities.

Any change must be documented and:
- propagated to `AGENT_INTERACTION_SCRIPT_v2.md`,
- announced via the Agent Issue Log or equivalent change-log mechanism.

---

## 9. Summary

Agents must **not** rely on one-time reading of the canon.  
They must **periodically re-anchor** to the current ontology, operational rules, and interaction protocols.

This policy:
- defines the required triggers,
- sets expectations by role and surface,
- prevents drift during long tasks,
- and strengthens safety and coherence across the FRAMES ecosystem.

All agents are required to follow this policy as part of normal operation.

