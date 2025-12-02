# MODULE_DEFINITION_v2.md
### *Formal, Scientific, Operational Definition of a Module in the FRAMES System*

This document defines **exactly** what a module is, where it comes from, how it must be structured, what data it contains, and how it relates to the FRAMES ontology and application architecture.

A module is one of the most important objects in the entire system. This definition removes all ambiguity and prevents agents from:
- treating Notion pages as modules,
- inventing synthetic examples,
- confusing tasks with modules,
- rewriting human content to "fit" a module shape,
- interpreting modules as mere documents.

This is the **only canonical definition** of a module.

---

# 1. Core Definition
A **module** is a *structured learning artifact* created by distilling **real engineering problem-solving behavior** into a formal, teachable representation.

A module:
- originates from **observable digital traces**,
- encodes **authentic reasoning sequences**,
- is structured for **student learning**,
- is stored in the **canonical database**,
- is delivered through the **Student LMS**,
- never exists inside Notion as a first-class object.

A module is **not** authored from imagination or theory. It is **extracted** from real work.

---

# 2. Ontological Foundations
Modules are derived from ontological primitives defined in:
- `FRAMES_THEORETICAL_ONTOLOGY.md`,
- `OPERATIONAL_ONTOLOGY.md`.

Specifically, modules are constructed from:
- **Tasks** (real problem-solving events),
- **Journeys** (temporal sequences of human actions),
- **Interfaces** (collaboration and dependency points),
- **Decisions and constraints** captured in digital traces.

A module represents *one coherent reasoning unit* that can be taught.

---

# 3. Sourcing and Evidence Requirements
Every module must originate from **verifiable evidence**. Acceptable evidence sources include:
- Notion task descriptions and updates,
- comments, questions, and discussions,
- subsystem decisions and trade-offs,
- troubleshooting logs,
- code review sequences,
- Git commit reasoning (when integrated),
- problem escalations and resolutions,
- cross-team interactions.

Agents may not create a module unless:
- the underlying reasoning steps are visible in digital traces,
- the problem is real and grounded in the team's work,
- the sequence of steps can be reconstructed faithfully.

Modules must preserve the integrity of the real work they distill.

---

# 4. Module Structure (Canonical Fields)
Each module must contain the following structured elements. These correspond directly to FRAMES' pedagogical and analytical goals.

## 4.1 Metadata
- **module_id** (canonical, DB-generated)
- **title** (derived from real task/problem)
- **subsystem** (power, comms, etc.)
- **difficulty_level** (beginner, intermediate, advanced)
- **source_references** (links to Notion pages, Git commits, or other traces used to extract the module)
- **created_from_journey_ids** (references to journeys used as evidence)

## 4.2 Learning Objectives
- concise statements of what the student will understand or be able to do
- based on actual reasoning used by the team

## 4.3 Problem Statement
- the real engineering question addressed by the team
- framed in a way a student can attempt
- must not fictionalize or simplify away key constraints

## 4.4 Context and Constraints
- subsystem context
- design constraints
- environmental or mission-specific constraints
- known limitations

## 4.5 Reasoning Sequence (Core of the Module)
This is the heart of the structure.

A sequence of steps that reflect the team’s real reasoning:
1. framing the problem,
2. generating hypotheses or partial solutions,
3. identifying risks or uncertainties,
4. performing calculations or evaluations,
5. encountering errors or dead-ends,
6. correcting course,
7. arriving at resolution.

Each step must be grounded in traceable evidence.

## 4.6 Hints (Scaffolding)
Hints derived from the team’s intermediate reasoning. These help students move through the problem step-by-step.

## 4.7 Validation Logic
- expected outputs or conditions for correctness,
- derived from the real resolution the team reached.

Validation logic must reflect *authentic engineering criteria*.

## 4.8 Wrap-Up / Key Insights
A short summary highlighting:
- what the team learned,
- what patterns emerged,
- what the student should take away.

---

# 5. Module Life Cycle

## 5.1 Extraction
Interpreter Agent identifies a candidate module from:
- task sequences,
- reasoning paths,
- troubleshooting logs,
- subsystem interactions.

## 5.2 Drafting
Builder Agent constructs a draft module in a **non-canonical file**.
- no changes to Notion content,
- all content must cite evidence.

## 5.3 Validation
Validator Agent checks:
- fidelity to real work,
- alignment with ontology,
- correct structure,
- appropriate constraints and reasoning steps.

If unclear rules are encountered → log in Agent Issue Log.

## 5.4 Canonicalization
After approval:
- module is written to canonical database tables,
- LMS surfaces are updated automatically via API.

## 5.5 Feedback to Notion (Optional, Limited)
Agents may:
- add a link in a Notion safe region acknowledging that a module was created,
- never overwrite or restructure human content.

---

# 6. What a Module Is **Not**
To prevent drift, agents must treat the following as explicit prohibitions.

A module is **not**:
- a Notion page,
- a task,
- a simple write-up,
- a checklist,
- a synthetic or fictional example,
- a document written without evidence,
- an agent-invented scenario,
- a collection of random facts.

Modules must be:
- structured,
- grounded,
- evidence-based,
- derived from real engineering behavior.

---

# 7. Relationship to Other FRAMES Components

### 7.1 Notion (Observation Layer)
Provides raw signals.  
Does **not** contain modules.  
May only hold safe-region backlinks to modules.

### 7.2 LMS (Delivery Layer)
The official student interface for consuming modules.  
Displays:
- sections,
- steps,
- hints,
- validation results.

### 7.3 Database (Canonical Store)
The authoritative location of:
- module metadata,
- module sections,
- module progress,
- analytics events.

### 7.4 Research Layer
Modules contribute to:
- understanding learning pathways,
- correlating reasoning with performance,
- modeling how expertise forms.

---

# 8. Requirements for Autonomous Behavior Around Modules
Agents must:
- refresh ontology before drafting or interpreting modules,
- cite evidence for each reasoning step,
- validate before canonical writes,
- never generate hypothetical modules,
- log ambiguous rules in the Agent Issue Log.

Modules are **high-risk artifacts** because they affect:
- student learning,
- research integrity,
- system-wide consistency.

Therefore:
- autonomy is medium during extraction,
- medium-high during drafting,
- low during canonicalization.

---

# 9. Summary
A module is:
- a structured, evidence-backed learning artifact,
- extracted from authentic engineering behavior,
- validated and stored in the canonical database,
- delivered through the Student LMS,
- governed by strict ontological and operational rules.

A module is **never**:
- a Notion page,
- a synthetic exercise,
- invented content,
- or restructured human material.

This definition must govern all agent behavior involving modules.

