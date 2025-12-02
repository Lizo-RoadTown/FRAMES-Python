# AGENT_ISSUE_LOG_SPEC.md
### *Specification for the Agent Issue Log in Notion*

This document defines how agents must use the **Agent Issue Log** in Notion.  
The log exists so that agents can "tattle" on:
- unclear or conflicting rules,
- too-strict or too-loose constraints,
- each other’s unsafe or off-canon behavior,
- recurring friction points in real tasks.

The goal is to give humans a clear view of systemic issues that need adjustment.

This spec assumes there is a dedicated Notion page called something like **"Agent Issue Log"**, with an explicit **agent-safe region** where agents are allowed to append entries.

---

## 1. Purpose of the Agent Issue Log

The log is used to:
- record grey-area situations (rules that are too strict, too loose, or unclear),
- capture conflicts between canonical documents,
- document blocked or unsafe actions that were prevented,
- surface patterns that require human system design changes,
- hold agents accountable to each other.

It is **not**:
- a general scratchpad,
- a place for long-form analysis,
- a replacement for error logs or technical traces.

---

## 2. Location and Safe Region

The Agent Issue Log must:
- live on a **single dedicated Notion page**,
- contain a clearly marked **"Agent Log Entries"** block or section,
- treat that block as the **only agent-safe write region** on the page.

Example safe region marker (human-created):

> ### Agent Log Entries (Safe Region)
> Agents may append issue entries **below this line only**. Do not modify content above.
> ---

Agents must:
- only append entries after the safe-region marker,
- never edit or delete previous entries,
- never modify anything above the safe-region marker.

---

## 3. Entry Format (Required Fields)

Each log entry must follow this structured format and be written as a single block (or bullet) to simplify parsing.

**Required fields:**

- `Timestamp` – ISO format or clearly labeled (e.g., `2025-12-01T21:30Z`).
- `AgentRole` – Interpreter, Builder, Validator, CursorBuilder, etc.
- `TaskSummary` – short description of the task (1–2 sentences).
- `Surfaces` – Notion, DB, Codebase, Repo Docs, LMS, etc.
- `RuleArea` – which document/area was involved:
  - Theoretical Ontology,
  - Operational Ontology,
  - Notion Interface Layer,
  - Agent Interaction Script,
  - Module Definition,
  - Canonical Refresh Policy,
  - Other (with description).
- `IssueType` – one of:
  - `TooStrict`,
  - `TooLoose`,
  - `ConflictingRules`,
  - `UnclearDefinition`,
  - `RefreshFailure`,
  - `UnsafeBehaviorPrevented`,
  - `Other`.
- `Description` – concise explanation of what happened (3–6 sentences max).
- `ActionTaken` – what the agent actually did:
  - blocked action,
  - proceeded cautiously,
  - asked for clarification,
  - stopped entirely.
- `SuggestedChange` – optional, but recommended:
  - how rules or docs could be improved.
- `OtherAgentsInvolved` – optional list of agents/roles this concerns.

---

## 4. Example Entry

```text
Timestamp: 2025-12-01T21:30Z
AgentRole: Validator
TaskSummary: Drafting a new module from EPS troubleshooting sequence.
Surfaces: Notion, Repo Docs
RuleArea: Module Definition, Notion Interface Layer
IssueType: TooStrict
Description: The Notion rules prevented the Builder from adding a short note in the same section where the troubleshooting steps live, even though it would have helped the Team Lead see which part of the page was already converted into a module. We had to create a separate log elsewhere, which may be hard for humans to discover.
ActionTaken: Blocked the write to Notion and proceeded with module drafting only in the repo. Logged this issue for human review.
SuggestedChange: Allow agents to add a one-line "Module created" annotation in a designated subsection of relevant Notion pages, still within a safe region.
OtherAgentsInvolved: Builder
```

---

## 5. When Agents MUST Log an Issue

Logging is **mandatory** when:

1. A rule is too strict to complete a safe, clearly useful task.
2. A rule is too loose and would allow potentially unsafe behavior.
3. Two canonical documents appear to conflict.
4. An agent repeatedly has to guess or work around missing guidance.
5. A Validator blocks or corrects another agent for violating canon.
6. A required canonical refresh was skipped or forgotten (RefreshFailure).
7. Ambiguity persists after refreshing canon and applying the interaction script.

If in doubt, agents should err on the side of **logging**.

---

## 6. Behavioral Expectations

Agents must:
- be factual and concise,
- avoid blameful or emotional language,
- identify themselves by role (no anonymous entries),
- focus on system-level issues, not personalities.

It is acceptable and encouraged for agents to:
- "tattle" on each other’s unsafe behavior,
- note recurring rule friction,
- point out unclear definitions or gaps.

This is not punitive—it is a mechanism for improving the system.

---

## 7. Human Use of the Log

Humans (system architects, maintainers, researchers) should:
- periodically review the log for patterns,
- cluster issues by RuleArea and IssueType,
- update ontologies, policies, and scripts accordingly,
- close the loop by noting major changes in a change-log.

Over time, the log becomes a **feedback channel** between:
- the live agent ecosystem,
- the evolving theory and rules,
- and the human designers of FRAMES.

---

## 8. Summary

The Agent Issue Log is a structured, append-only record in Notion where agents:
- report rule friction,
- surface grey areas,
- hold each other accountable,
- and provide signal for system evolution.

Agents must:
- write only in the safe region,
- use the required fields,
- log whenever rules are too strict, too loose, unclear, or violated.

Humans use this log to keep FRAMES aligned with reality as both the system and the lab evolve.

