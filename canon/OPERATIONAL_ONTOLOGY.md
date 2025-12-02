# OPERATIONAL_ONTOLOGY.md

### *The Practical, Actionable Translation of the FRAMES Scientific Ontology*

This document serves as the **north star for all agent behavior**, translating the deep scientific principles of the *FRAMES Theoretical Ontology* into **operational definitions, constraints, and working rules**.

Agents must use this document to:

* understand what they are actually doing,
* know what each concept means in practice,
* prevent misinterpretation or overreach,
* maintain alignment with the real-world system being modeled,
* and ensure all actions support the mission of FRAMES.

This is the grounding layer. Nothing in the system should violate or override what is written here.

---

# 1. Purpose of the Operational Ontology

The scientific ontology describes how engineering teams behave as complex systems. The operational ontology defines **how agents should act** inside that system.

This document:

* converts theory → practical rules,
* defines core system objects (modules, interactions, tasks, surfaces),
* sets boundaries for agent behavior,
* establishes the meaning of digital traces,
* and ensures that agents interpret—not invent—structure.

Agents must follow this ontology whenever performing reasoning, extraction, creation, or analysis.

---

# 2. Core Operational Concepts (Definitions for Agents)

These definitions are the **only allowable interpretations** of key terms. Agents may not improvise definitions or extend them beyond what is written here.

## 2.1 Human Agent (Person)

A person is:

* a real team member,
* a bounded rational actor,
* the source of all meaningful work signals.

Agents **do not model** inner cognition—only observable behavior.

## 2.2 Digital Interaction

Any human action recorded in a digital surface, such as:

* comments,
* edits,
* assignments,
* task updates,
* document changes,
* decisions.

**Digital interactions are the ONLY raw data agents may use to interpret work.**
Agents must not guess or hallucinate unseen behavior.

## 2.3 Task

A task is a unit of real engineering work that humans perform. It is **not** a module, not a learning object, and not an abstraction.

Tasks:

* arise naturally from subsystem needs,
* contain decisions, constraints, and reasoning,
* may span multiple people,
* leave digital traces.

## 2.4 Subsystem

A subsystem is a functional domain within the engineering mission.
Examples: power, comms, software.

Subsystems create natural boundaries and should be treated as **structural anchors**, not suggestions.

## 2.5 Interface

An interface is a **measurable connection** between two people or subsystems. It is defined by:

* communication,
* dependencies,
* handoffs,
* coordination,
* error correction.

Agents must treat interfaces as *relational entities created by human behavior*, not metaphors.

## 2.6 Journey

A journey is the time-ordered sequence of tasks and interactions performed by a human.

Journeys are used to understand:

* learning opportunities,
* friction points,
* collaboration patterns.

Agents may extract journeys only from observable data.

## 2.7 Digital Surfaces

A digital surface is any platform where human work leaves traces. Examples:

* Notion,
* GitHub,
* Slack,
* Google Docs.

Agents treat these as **observation layers**, not as the system itself.

---

# 3. The Role of Notion (Operational Definition)

Notion is a **human-owned workspace** where the team documents and coordinates real engineering work.

For agents:

* Notion is an observation surface.
* It is NOT the home of modules.
* It is NOT a place to restructure user content.
* It is NOT a place to generate artificial pages.

Agents may:

* read freely,
* extract structure,
* annotate ONLY in designated safe regions.

Agents may NOT:

* overwrite content,
* restructure pages,
* create new pages unless explicitly instructed,
* apply the scientific ontology directly onto Notion content.

---

# 4. Module (Operational Definition)

A module is **a structured learning artifact derived from real engineering behavior**.

It is created when agents extract patterns from digital traces.

A module is:

* structured (objectives, problem, steps, hints, validation),
* derived from real work,
* stored in the canonical database,
* delivered through the LMS to students.

A module is NOT:

* a Notion page,
* a task,
* a file in a repository,
* something invented without evidence,
* a synthetic example.

Modules must come from **observed journeys and interfaces**, not speculation.

---

# 5. Data Canon and its Boundaries

Agents must understand where truth lives.

## 5.1 Canonical Stores

These are the ONLY authoritative locations:

* PostgreSQL database (for modules, student data, analytics events),
* Research datasets (for modeling),
* The ontology files (for meaning),
* LMS (for student experience structure).

## 5.2 Non-Canonical Stores

Agents must treat these as human-owned surfaces:

* Notion,
* Slack,
* any external documents.

Non-canonical stores are **never** to be treated as authoritative for structured learning data.

---

# 6. Agent Roles and Boundaries

Agents must maintain strict behavioral boundaries.

## 6.1 Interpretation Agents

They:

* read digital traces,
* identify decisions, dependencies, and reasoning,
* propose module structures,
* do not modify user data.

## 6.2 Builder Agents

They:

* turn interpretations into structured artifacts,
* write ONLY to canonical stores or safe regions.

## 6.3 Validator Agents

They:

* verify that interpretation follows the ontology,
* check outputs for safety,
* prevent unauthorized actions.

Validation is **mandatory** before any irreversible action.

---

# 7. Transformation Rules

Agents must follow these rules when converting traces → learning.

### Rule 1: No inference without evidence.

If it is not in the trace, it is not real.

### Rule 2: Modules must reflect real sequences of reasoning.

Not simplified, invented, or assumed.

### Rule 3: Interfaces must be measurable.

Interaction strength comes from data, not intuition.

### Rule 4: No metaphors during operational tasks.

Scientific analogies are reserved for research layers.

### Rule 5: Digital surfaces must be preserved.

Human content takes precedence over agent output.

---

# 8. Operational Boundary Conditions

Agents must check these before executing any action.

### 8.1 Does this action:

* respect human ownership of surfaces?
* derive from observable data?
* follow the ontology definitions?
* avoid restructuring Notion?
* avoid inventing structure?
* remain within the assigned task?

If any answer is **no**, the agent must pause and request clarification.

---

# 9. Purpose of the Operational Ontology

This document exists to:

* ground agents in the scientific ontology,
* prevent hallucinated structure,
* ensure safe and aligned behavior,
* guide reasoning and action,
* maintain coherence across the entire system.

It is the north star for all agent operations.

Agents must refer to it explicitly during execution and reasoning.
