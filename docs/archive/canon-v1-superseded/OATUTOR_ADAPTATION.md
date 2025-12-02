# DEPRECATED

**This file is no longer canonical.**

**Replaced by:** (Will be rewritten for V2)
**Reason:** Old structure conflicts with V2 ontology

**Archived:** 2025-12-01

---

# OATutor Adaptation for Engineering Modules

## Critical Understanding

**OATutor provides the PEDAGOGICAL FRAMEWORK** - not just a JSON format.

OATutor is a math education platform that embodies a specific teaching methodology:

- **Scaffolding**: Breaking complex problems into manageable steps
- **Hint pathways**: Providing graduated assistance without giving away answers
- **Interactive validation**: Checking understanding at each step
- **Adaptive sequencing**: Adjusting difficulty based on student performance

## Why OATutor Matters for FRAMES

### The Theory We're Adapting

OATutor has proven pedagogical theory for:

- How to structure learning content (step-by-step reasoning)
- When to provide hints (after struggle, before frustration)
- How to validate understanding (interactive checks, not just quizzes)
- How to scaffold difficult concepts (graduated assistance)

### Adapting Math Theory to Engineering

Engineering learning is different from math:

- **Math**: Abstract problem-solving, step-by-step derivations
- **Engineering**: Real-world constraints, project-based context, multi-disciplinary

We are **upgrading OATutor's theory to fit engineering** by:

- Keeping: Scaffolding, hint pathways, interactive validation
- Adding: Real project context, hardware constraints, troubleshooting flows
- Changing: From abstract problems to real CubeSat mission tasks

## What OATutor Provides

### Core Pedagogical Components

1. **Problem Structure**
   - Main problem statement with real engineering context
   - Sub-problems (steps) that scaffold to solution
   - Each step has validation logic

2. **Hint System**
   - Multi-level hints (gentle → specific → explicit)
   - Hints guide thinking, don't give answers
   - Context-aware based on student errors

3. **Interactive Validation**
   - Check answers at each step
   - Provide feedback on errors
   - Allow multiple attempts with guidance

4. **Adaptive Pathways**
   - Alternative solution paths
   - Easier/harder variants based on performance
   - Skip-ahead for advanced students

### NOT Just JSON Format

Common misunderstanding: "OATutor is a content format we copy"

**Wrong**: OATutor is a teaching methodology we adapt

- The JSON structure reflects pedagogical principles
- Each field serves a specific learning purpose
- The format enforces good teaching practices

## Engineering Extensions

### What We Add to OATutor Framework

- **Simulation tasks**: Interactive hardware/software simulations
- **Troubleshooting flows**: Diagnostic tree navigation
- **Hardware diagrams**: Visual component identification
- **Procedural walk-throughs**: Real mission task sequences
- **Constraint checking**: Engineering limits (power, mass, budget)
- **Multi-disciplinary context**: How subsystems interact

### What We Keep from OATutor

- Scaffolding approach (complex → manageable steps)
- Hint pathway design (graduated assistance)
- Interactive validation (check understanding constantly)
- Adaptive sequencing (adjust to student level)
- Error analysis (learn from mistakes)

## Module Creation Using OATutor Framework

### The Process

1. **Extract content** from Team Lead Notion pages (real mission context)
2. **Identify learning objectives** (what students must understand)
3. **Apply OATutor scaffolding** (break into steps with hints)
4. **Add engineering context** (real constraints, hardware, procedures)
5. **Validate structure** (does it follow pedagogical principles?)
6. **Store in database** (structured for Student LMS consumption)

### Example: Power Budgeting Module

**Team Lead Notion Content** (raw):
> "We had to calculate total power consumption for all subsystems. Battery capacity is 40 Wh. We need 20% margin for safety."

**After OATutor Framework Applied**:

```json
{
  "problem": "Calculate if CubeSat power budget meets mission requirements",
  "steps": [
    {
      "step_id": 1,
      "prompt": "List all subsystems and their power draw",
      "hints": [
        "Review the subsystem diagram",
        "Check each component's datasheet",
        "Don't forget avionics and communications"
      ],
      "validation": "sum_of_subsystems"
    },
    {
      "step_id": 2,
      "prompt": "Calculate total power consumption",
      "hints": [
        "Add all subsystem power draws",
        "Consider duty cycles (not all run simultaneously)",
        "Use worst-case scenario"
      ]
    },
    {
      "step_id": 3,
      "prompt": "Apply safety margin and compare to battery capacity",
      "hints": [
        "Engineering rule: always include margin",
        "20% margin is standard for CubeSats",
        "Battery capacity: 40 Wh"
      ]
    }
  ]
}
```

### What Changed

- **Raw content** → Structured learning experience
- **Static info** → Interactive validation
- **Single explanation** → Scaffolded steps with hints
- **No guidance** → Multiple hint levels

## Integration with Student LMS

### How Students Experience OATutor-Structured Content

1. See main problem in real mission context
2. Work through scaffolded steps
3. Request hints when stuck (graduated assistance)
4. Validate answers at each step (immediate feedback)
5. Learn from errors (adaptive hints based on mistakes)
6. Build understanding incrementally (not overwhelmed)

### Why This Reduces Engineering Learning Curve

Traditional engineering onboarding:

- ❌ Throw students into deep end
- ❌ Sink or swim approach
- ❌ Steep learning curve, high failure rate

OATutor-based onboarding:

- ✅ Scaffold complex tasks into manageable steps
- ✅ Provide help when stuck (without giving answers)
- ✅ Build confidence through validated progress
- ✅ Gentler learning curve, better retention

## Implications for Each Agent

### Alpha (Module Content)

- **Study OATutor repository** to understand pedagogical framework
- **Apply framework** when extracting Team Lead content
- **Don't just copy JSON format** - understand WHY each field exists
- **Validate pedagogical quality** - does it scaffold well? Are hints graduated?

### Beta (Applications)

- **Implement OATutor components** in Student LMS:
  - Step-by-step navigation
  - Hint display system
  - Interactive validation UI
  - Progress tracking per step
- **Focus on UX** - make scaffolding feel natural, not burdensome

### Gamma (Infrastructure)

- **Store OATutor-structured modules** in database
- **Track student interactions** with hints, steps, validations
- **Analytics on scaffolding effectiveness** - which hints are most used?

## Required Next Steps

Before creating modules, Alpha must:

1. **Study OATutor repository** (https://github.com/Lizo-RoadTown/OATutor)
2. **Understand pedagogical principles** - not just JSON structure
3. **Learn hint pathway design** - how to write effective hints
4. **Practice scaffolding** - break complex tasks into steps
5. **Review Team Lead Notion** - understand real content to extract

This is foundational work - can't create good modules without understanding the teaching methodology.
