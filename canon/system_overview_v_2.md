# SYSTEM_OVERVIEW_v2.md
### *How FRAMES Sees, Structures, and Activates Real Engineering Work*

This document provides a high-level overview of the FRAMES system architecture, aligned with:
- `FRAMES_THEORETICAL_ONTOLOGY.md` (the scientific model),
- `OPERATIONAL_ONTOLOGY.md` (practical definitions and constraints),
- `NOTION_INTERFACE_LAYER_v2.md` (Notion as observation surface),
- `AGENT_INTERACTION_SCRIPT_v2.md` (how agents work together).

It explains:
- what the system is modeling,
- which layers exist,
- how data flows between them,
- how roles (humans + agents) interact,
- where autonomy is safe and where it is constrained.

---

## 1. System Purpose

FRAMES exists to:

1. **Observe real engineering teams** as complex systems.
2. **Extract structured learning** from authentic work (modules).
3. **Model interface patterns** to understand and predict mission outcomes.
4. **Deliver learning experiences** to students through a Student LMS.
5. **Provide analytics and research surfaces** to understand team dynamics and educational impact.

The central idea:
> Real engineering work is the primary data source.
> FRAMES turns that work into learning and insight without distorting it.

---

## 2. Conceptual Stack (Layers)

FRAMES is organized into layers. Each layer has a distinct purpose and risk profile.

### 2.1 Real-World Layer (Human System)
- Engineering team members (students, leads, mentors).
- Missions, subsystems, and tasks.
- Decisions, handoffs, troubleshooting, and learning.

This is the **true system**. All other layers observe or structure it.

### 2.2 Digital Observation Layer
- Tools where work leaves traces:
  - Notion (project workspace, decisions, documentation),
  - Git/GitHub (code history),
  - other collaboration tools as they are integrated.

These surfaces are **sensors**. They do not define the ontology; they reveal behavior.

### 2.3 Interpretation & Agent Layer
- Agents read digital traces.
- They use the Theoretical + Operational Ontology to:
  - interpret behavior,
  - identify tasks, interfaces, and journeys,
  - detect module candidates,
  - propose structured artifacts.
- They follow `AGENT_INTERACTION_SCRIPT_v2` to:
  - coordinate roles (Interpreter, Builder, Validator),
  - respect surface risk levels,
  - log grey-area issues.

### 2.4 Canonical Data Layer
- PostgreSQL database and associated storage.
- Holds the **authoritative structured data**, including:
  - modules and module sections,
  - module–student relationships and progress,
  - analytics events,
  - ghost cohorts and race mode data,
  - research datasets (or references to them).

This is where modules and learning structures live.

### 2.5 Application Layer
- **Student LMS**:
  - presents modules and sequences to learners,
  - tracks progress and performance,
  - supports race mode and ghost cohorts.
- **Researcher Platform**:
  - surfaces analytics about interfaces, journeys, and outcomes,
  - enables querying and visualization of patterns.

These applications read from the Canonical Data Layer.

### 2.6 Governance & Logging Layer
- Issue logs (especially in Notion) capturing:
  - rule ambiguities,
  - safety concerns,
  - agent corrections and blocked actions.
- Error logging and traceability.

This layer exists to **improve the system over time** and keep humans in the loop.

---

## 3. Human Roles

### 3.1 Team Members / Students
- Work on real missions in the space lab.
- Leave digital traces in Notion and other tools.
- Consume modules in the Student LMS.
- Their behavior is the primary source of data.

### 3.2 Team Leads / Mentors
- Coordinate missions and subsystems.
- Document decisions, procedures, and reasoning in Notion.
- Provide context and corrections to modules.

### 3.3 Researchers
- Use the Researcher Platform to:
  - analyze interface patterns,
  - study learning pathways,
  - correlate topology with mission outcomes.

### 3.4 System Operators / Architects
- Maintain the ontology and operational definitions.
- Review agent issue logs.
- Adjust rules, scripts, and schemas.

---

## 4. Agent Roles in the System

Agents are **interpreters and builders**, not owners of the system.

### 4.1 Interpreter Agents
- Read digital traces.
- Apply the ontology to identify:
  - tasks,
  - decisions,
  - interfaces,
  - journeys,
  - candidate modules.
- Produce Task Plans and designs.

### 4.2 Builder Agents
- Implement structured artifacts based on plans:
  - module definitions in the DB,
  - documentation and specs inside the repo,
  - code changes (via Cursor or equivalent),
  - safe annotations in Notion.

### 4.3 Validator (Governor) Agents
- Review plans and outputs.
- Enforce:
  - ontology alignment,
  - Notion rules,
  - data layer constraints.
- Log grey areas and conflicts.

Agents operate across modes (Exploration, Drafting, Execution, Commit) as defined in `AGENT_INTERACTION_SCRIPT_v2`.

---

## 5. Data Flows

### 5.1 From Real Work to Modules
1. Human work occurs in the lab and is recorded in Notion and other tools.
2. Interpreter Agent analyzes these traces and identifies module candidates.
3. Builder Agent drafts module structures (objectives, problems, steps, validation) in a non-canonical space.
4. Validator reviews drafts for:
   - fidelity to real work,
   - correctness of definitions,
   - alignment with ontology.
5. Once approved, modules are written into the Canonical Data Layer.
6. Modules are then available in the Student LMS.

### 5.2 From Real Work to Analytics
1. Digital interactions are logged or transformed into analytics events.
2. Canonical Data Layer stores events and relationships (e.g., who interacted with what, when).
3. Researcher Platform queries events and structures to:
   - compute interface strength,
   - map journeys,
   - analyze topology.
4. Insights feed back into:
   - system design,
   - learning design,
   - organizational practices.

### 5.3 Feedback to Notion (Minimal and Safe)
- Agents may add references from Notion pages to modules.
- They may annotate safe regions with:
  - “This section has been distilled into Module X,”
  - links to LMS artifacts,
  - status of extraction.
- They may not restructure content.

---

## 6. Surfaces and Risk Profiles

### 6.1 High-Risk Surfaces
- Notion (human-owned workspace).
- Canonical database.

Agents must:
- act with low autonomy,
- follow strict rules,
- require validation for writes.

### 6.2 Medium-Risk Surfaces
- Codebase.
- Repo documentation.

Agents may:
- operate with medium autonomy within scoped tasks,
- produce diffs and summaries,
- require validator oversight for complex or wide-reaching changes.

### 6.3 Low-Risk Surfaces
- Scratch spaces.
- Draft files.
- Non-canonical analysis artifacts.

Agents may:
- explore,
- cluster,
- propose,
- draft freely.

---

## 7. Non-Goals and Explicit Boundaries

FRAMES is **not**:
- a replacement for project management tools,
- a top-down workflow control system,
- a free-form content generator for Notion,
- a system that overrides human decision-making.

FRAMES does **not**:
- define how humans must collaborate,
- enforce rigid process templates on the lab,
- treat theoretical metaphors as operational commands.

FRAMES **does**:
- observe,
- interpret,
- structure,
- model,
- and enable learning and insight.

---

## 8. Evolution and Governance

The system is designed to evolve.

Mechanisms for evolution:
- Agent Issue Log (grey-area rules, conflicts, recurring friction).
- Updates to:
  - ontology files,
  - operational definitions,
  - Notion interface rules,
  - interaction scripts.
- Schema and API changes driven by explicit design, not ad-hoc edits.

Humans remain responsible for:
- interpreting issue patterns,
- revising core documents,
- approving major changes to architecture.

---

## 9. Summary

The FRAMES system:
- starts from real engineering work,
- captures its digital traces,
- interprets those traces using a clear ontology,
- creates structured modules and analytics,
- delivers learning and insight through dedicated applications,
- protects human-owned workspaces and data integrity,
- and improves over time through visible, logged friction.

This System Overview, together with the ontology and operational files, defines the stable backbone of the FRAMES ecosystem.