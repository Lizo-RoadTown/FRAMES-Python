# FRAMES Theoretical Ontology
## Herbert Simon–Aligned Scientific Canon

> *"The central task of a natural science is to make the wonderful commonplace: to show that complexity, correctly viewed, is only a mask for simplicity."*  
> — Herbert A. Simon, *The Sciences of the Artificial*

---

## Introduction

This document captures the **scientific, theoretical, and research-facing ontology** that underlies the FRAMES system. It draws directly from Herbert Simon's foundational work in organizational theory, bounded rationality, hierarchical systems, and near-decomposable structures. This ontology provides the conceptual backbone for interpreting team behavior, extracting learning from real engineering work, and modeling mission outcomes.

A separate file—**OPERATIONAL_ONTOLOGY.md**—will translate this theory into actionable definitions for agents, developers, and system components.

---

## 1. The System Being Modeled

FRAMES models an engineering team as a **complex adaptive system** composed of:

* bounded rational human agents,
* interacting subsystems,
* evolving task structures,
* and dynamic interfaces.

The goal is to understand and predict how coordination patterns, collaboration structures, and interface strengths influence mission success.

This model is grounded in scientific regularities observed across complex systems.

---

## 2. Fundamental Theoretical Assumptions

Derived from Simon's work on complex organizations:

### 2.1 Bounded Rationality

Humans make decisions under:

* limited information,
* limited attention,
* limited computational capacity.

They construct **satisficing** (not optimal) strategies.

### 2.2 Near-Decomposability

Large systems self-organize into **loosely coupled subsystems**.

* Strong interactions within subsystems
* Weak interactions across subsystems

This structure reduces cognitive and coordination load.

### 2.3 Interfaces as Governing Mechanisms

System behavior is governed by the **interfaces** between agents and subsystems, not the units themselves.

Interfaces transmit:

* constraints,
* information,
* dependencies,
* errors,
* problem-solving signals.

### 2.4 Digital Traces as Behavioral Surface

Digital interactions serve as **observable signatures** of underlying cognitive and coordination processes.

They allow indirect measurement of:

* decision sequences,
* communication patterns,
* dependency resolution,
* emergent topology.

### 2.5 Hierarchical Decision Processes

Engineering work unfolds across multiple temporal scales:

* **micro-decisions** (edits, comments, assignments)
* **meso-decisions** (design choices, troubleshooting steps)
* **macro-decisions** (mission direction, architecture)

These nested levels form a **hierarchical decision system**.

---

## 3. Ontological Primitives (Entities)

These are the foundational units FRAMES uses to represent organizational reality.

### 3.1 Human Agents (Nodes)

Team members modeled as:

* decision-making units,
* holders of localized knowledge,
* generators of behavioral traces,
* contributors to system-level outcomes.

**Key Insight:** No single agent has global knowledge of the mission.

### 3.2 Tasks (Problem-Solving Units)

A task is a **localized problem-solving event** unfolding over time.

It consists of:

* constraints,
* actions,
* decisions,
* errors,
* corrections,
* completion conditions.

### 3.3 Subsystems (Structural Units)

Subsystems provide **functional boundaries** and reduce system complexity.

They are highly coherent internally and loosely coupled externally.

### 3.4 Interfaces (Interaction Units)

An interface is a **connection that carries constraints and information** between two agents or subsystems.

**Interface strength** is a measurable construct based on:

* frequency
* reciprocity
* bandwidth of information
* latency
* error recovery
* shared outcomes

### 3.5 Journeys (Temporal Paths)

Journeys capture the **sequence of work** an agent performs across time:

* tasks touched
* collaborations
* subsystem crossings
* problem escalations
* knowledge acquisition events

### 3.6 Organizational Topology

At any moment, the team forms a network whose structure predicts:

* resilience,
* coordination cost,
* failure propagation,
* speed of adaptation.

---

## 4. Observables

FRAMES cannot observe cognition directly; it observes **behavioral traces**.

These include:

| Observable Type | Examples |
|----------------|----------|
| **Textual** | comments, edits, document updates |
| **Temporal** | timing data, sequence patterns |
| **Structural** | assignments, handoffs, co-edit patterns |
| **Topological** | cross-subsystem interactions, collaboration networks |

These traces form the measurable surface of organizational behavior.

---

## 5. Digital Surfaces: Observation Layers

Notion and related tools are **not the system**. They are **observation layers**—external memory surfaces that stabilize and reveal coordination.

These surfaces:

* externalize cognitive processes,
* reduce coordination cost,
* record decision sequences,
* render interfaces visible.

**They function as measurement instruments.**

---

## 6. Transformations Performed by FRAMES

FRAMES applies three high-level transformations.

### 6.1 Interpretation

Conversion of raw digital traces into structured representations of:

* decisions,
* dependencies,
* conflicts,
* resolutions,
* problem-solving progressions.

### 6.2 Distillation (Module Formation)

A **module** is a structured representation of real engineering reasoning.

It captures:

* problem framing
* constraints
* intermediate reasoning
* dead ends
* successful strategy
* validation conditions

**Modules are extracted, not authored.**

### 6.3 Modeling

FRAMES builds predictive models of:

* interface strength dynamics
* subsystem coordination
* failure precursors
* resilient topology patterns
* learning pathways

---

## 7. Boundary Conditions

### This ontology applies to:

✅ behavioral interpretation  
✅ module extraction  
✅ research modeling  
✅ understanding coordination

### This ontology does *not* apply to:

❌ UI decisions  
❌ database schemas  
❌ API protocols  
❌ Notion editing rules  
❌ CRUD operations

---

## 8. Purpose

The goal of this ontology is to:

1. **Provide a stable scientific foundation** for the FRAMES research platform
2. **Guide interpretation** of real engineering behavior
3. **Support module extraction** from authentic work artifacts
4. **Enable predictive modeling** of mission success
5. **Stabilize reasoning** across all agents and system components

---

## References

This ontology is grounded in:

* Simon, H. A. (1962). *The Architecture of Complexity*. Proceedings of the American Philosophical Society.
* Simon, H. A. (1969). *The Sciences of the Artificial*. MIT Press.
* Simon, H. A. (1973). *The Organization of Complex Systems*. In Pattee, H. H. (Ed.), Hierarchy Theory.
* Simon, H. A. (1991). *Bounded Rationality and Organizational Learning*. Organization Science.

---

## Relation to Other Documents

| Document | Relationship |
|----------|-------------|
| **OPERATIONAL_ONTOLOGY.md** | Translates theory into operational definitions |
| **canon/SYSTEM_OVERVIEW.md** | Describes system architecture implementing this theory |
| **canon/FRAMES_PHILOSOPHY.md** | Articulates philosophical foundations |
| **canon/RESEARCHER_PLATFORM.md** | Tools for investigating these theoretical constructs |

---

<p align="center">
  <i>This ontology serves as the scientific bedrock of FRAMES—guiding observation, interpretation, and prediction of complex engineering collaboration.</i>
</p>
