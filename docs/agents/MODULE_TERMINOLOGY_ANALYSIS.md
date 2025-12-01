# Module Terminology Analysis
**Agent:** Alpha
**Date:** 2025-11-30
**Purpose:** Analyze existing modules against new canon terminology and schema

---

## Executive Summary

**Total modules analyzed:** 68 JSON files in `modules/enhanced/`

**Good news:**
- ✅ Categories already match canon schema
- ✅ All modules have basic metadata structure
- ✅ All modules have race_metadata framework (though empty ghost_data)
- ✅ Learning objectives present in all modules

**Major issues:**
- 🔴 **66/68 modules are STUBS** - Generic templated content, not real learning material
- 🔴 **66/68 modules missing prerequisites** - No learning pathways defined
- 🔴 **Content is placeholder text** - "Review the resources..." generic instructions
- 🔴 **Learning objectives are too vague** - Just repeat the module title
- 🔴 **No actual subsystem-specific content** - Modules claim to be about "Avionics" or "Power" but contain no technical depth

---

## Canon Alignment Analysis

### Categories (ALIGNED ✅)

Canon schema defines:
```
"Getting Started | Software Development | Hardware & Subsystems | Mission Design & Analysis | Systems Engineering"
```

Current usage (all valid):
- Software Development: 27 modules
- Hardware & Subsystems: 16 modules
- Getting Started: 10 modules
- Mission Design & Analysis: 9 modules
- Systems Engineering: 6 modules

**Assessment:** ✅ No changes needed

---

### Disciplines (NEEDS EXPANSION ⚠️)

Canon schema allows:
```
"Software | Electrical | Aerospace | Systems | General"
```

Current usage:
- General: 66 modules (97%)
- Software: 2 modules (3%)

**Assessment:** ⚠️ Most modules should have specific disciplines
- Avionics → Electrical
- EPS/Power → Electrical
- Structures → Aerospace
- Communications → Electrical
- Flight Software → Software

**Recommendation:** Re-tag modules with specific disciplines based on content

---

### Difficulty Levels (WELL-DISTRIBUTED ✅)

Current distribution:
- Advanced: 27 modules (40%)
- Intermediate: 27 modules (40%)
- Beginner: 14 modules (20%)

**Assessment:** ✅ Good distribution, but verify difficulty matches actual content depth

---

### Tags (CADENCE-FOCUSED ✅)

Top tags reflect CADENCE project:
- nasa: 15
- tools: 13
- github: 9
- cadence: 6
- testing: 6
- f-prime: 5
- onboarding: 4
- power: 4
- avionics: 3

**Assessment:** ✅ Tags align with CADENCE subsystems and tools

---

## Content Quality Analysis

### Stub Module Pattern (CRITICAL ISSUE 🔴)

**66 out of 68 modules** follow this generic template:

```json
{
  "title": "[Topic Name]",
  "sections": [
    {
      "title": "Overview",
      "content_markdown": "[Topic Name]"  // Just repeats title!
    },
    {
      "title": "Hands-on Practice",
      "steps": [
        {
          "instruction": "Review the resources associated with [Topic] and note key dependencies.",
          "check": "Did you capture the primary goals and blockers?",
          "hint": "Summarize the main objective in one sentence before proceeding."
        },
        {
          "instruction": "Apply the documented workflow on a realistic scenario related to [Topic].",
          "check": "Can you demonstrate the workflow end-to-end?",
          "hint": "Start with a simplified scenario before scaling up."
        }
      ]
    },
    {
      "title": "Knowledge Check",
      "questions": [
        {
          "question": "What is the primary objective of [Topic]?",
          "correct": "To apply procedures",
          "explanation": "Each CADENCE module focuses on actionable procedures..."
        },
        {
          "question": "Which artifact should you produce after completing [Topic]?",
          "correct": "A concise summary of actions, blockers, and next steps."
        }
      ]
    }
  ]
}
```

**Problem:** This is a **template shell**, not actual learning content. Students can't learn "Avionics Team Onboarding" from "Review the resources associated with Avionics Team Onboarding."

---

### Learning Objectives (TOO GENERIC 🔴)

Current pattern:
```json
{
  "learning_objectives": [
    {
      "statement": "[Module title]",  // Just repeats title
      "bloom_level": "Understand"  // Always "Understand"
    }
  ]
}
```

**Canon requirement** (from MODULE_SCHEMA.md):
```json
{
  "learning_objectives": [
    {"statement": "Identify avionics subsystems", "bloom_level": "Remember"},
    {"statement": "Configure F Prime dev environment", "bloom_level": "Apply"},
    {"statement": "Evaluate telemetry data for anomalies", "bloom_level": "Evaluate"}
  ]
}
```

**Assessment:** 🔴 All learning objectives need rewriting with:
- Specific, measurable outcomes
- Varied Bloom's taxonomy levels
- 2-5 objectives per module (currently only 1)

---

### Prerequisites (MISSING 🔴)

Only **2 out of 68 modules** have prerequisites defined.

**Canon expectation:** Clear learning pathways:
- Orientation modules first
- Build on prior knowledge
- Progressive difficulty

**Recommendation:**
1. Define prerequisite chains
2. Group modules by subsystem
3. Create learning pathways (Beginner → Intermediate → Advanced)

Example pathway for Power subsystem:
```
power-orientation (Beginner)
  ↓
battery-sizing-fundamentals (Intermediate)
  ↓
eps-characterization (Advanced)
```

---

### Race Metadata (FRAMEWORK PRESENT, DATA MISSING ⚠️)

All modules have:
```json
{
  "race_metadata": {
    "ghost_data": [],  // EMPTY
    "time_targets": {"beginner": 67.5, "intermediate": 45, "advanced": 33},
    "checkpoints": [
      {"name": "Plan", "order": 1},
      {"name": "Execute", "order": 2},
      {"name": "Document", "order": 3}
    ]
  }
}
```

**Assessment:** ⚠️ Structure is correct, but:
- ghost_data arrays are all empty (Gamma needs to populate)
- Checkpoints are generic ("Plan, Execute, Document") - should be module-specific
- Time targets seem automatically calculated (1.5x difficulty multiplier)

**Recommendation:** Keep framework, coordinate with Gamma to populate ghost_data

---

## Terminology Mapping

### Old vs. New Terms

After reviewing canon docs, **most terminology is already aligned**. No major name changes needed.

**Confirmed valid terms:**
- ✅ CADENCE (project name)
- ✅ Subsystems: Power, Avionics, Structures, Thermal, Communications, etc.
- ✅ "Ascent Basecamp" for platform name
- ✅ Module categories match canon exactly

**Minor adjustments needed:**
- Change "Discipline: General" → Specific disciplines (Electrical, Aerospace, Software, Systems)
- Add "Competency progression" metadata (Orientation → Competency → Integration → Autonomy)

---

## Salvageability Assessment

### Can modules be salvaged? YES ✅ with work

**Current state:**
- Metadata structure: ✅ Correct
- Categories/tags: ✅ Aligned
- JSON schema: ✅ Matches MODULE_SCHEMA.md
- Content depth: ❌ Stub/placeholder only
- Learning objectives: ❌ Too vague
- Prerequisites: ❌ Missing

**Salvage strategy:**

**TIER 1 - Keep metadata, rewrite content (52 modules)**
These have good titles and are on valid CADENCE topics:
- Avionics Team Onboarding
- Communications Subsystem
- EPS Design Presentation
- F' Prime Tutorials
- GitHub workflows
- Power subsystem modules
- Structures modules
- etc.

**Action:** Populate with actual CADENCE-specific content from source documents

**TIER 2 - Archive (16 modules)**
These are project-specific interim documents, not learning modules:
- "Add Github Tasks" (task, not module)
- "Check in and GitHub discussion" (meeting notes?)
- "Create new section on Github" (procedural task)
- "EAT Software Design Notes" (notes, not module)
- "Ella UML Diagrams Github" (artifact, not module)

**Action:** Move to `modules/archive/` or `docs/cadence/` as reference material

**TIER 3 - High priority for enhancement (12 modules)**
Well-scoped, high-value topics that students NEED:
- F' Prime LED Blinker Tutorial
- F' Prime Tutorials
- GitHub Guide
- GitHub Practice
- Software Testing Guides
- Subsystem orientation modules

**Action:** Enhance FIRST with detailed content

---

## Recommendation Summary

### Immediate Actions (Human decision required)

1. **Archive Tier 2 modules** (16 modules)
   - Move non-learning content to appropriate locations
   - Update module library to remove them

2. **Prioritize Tier 3 for enhancement** (12 modules)
   - Focus on high-value, well-scoped topics
   - Use CADENCE source documents for content
   - Human review of first 2-3 enhanced modules before scaling

3. **Define learning pathways**
   - Group remaining 52 modules by subsystem
   - Define prerequisite chains
   - Establish competency progression

### Medium-term Actions (Agent-executable with approval)

4. **Enhance all Tier 1 modules** (52 modules)
   - Replace stub content with real technical depth
   - Write specific learning objectives (2-5 per module)
   - Add prerequisite links
   - Create module-specific checkpoints

5. **Update disciplines**
   - Re-tag all modules with specific disciplines
   - Electrical: avionics, power, communications
   - Aerospace: structures, mission design
   - Software: F' Prime, GitHub, testing
   - Systems: integration, ConOps

6. **Coordinate with Gamma**
   - Request ghost_data population for race mode
   - Provide module timing estimates for ghost calculations

---

## Questions for Human

1. **Tier 2 modules:** Should I archive all 16 non-learning modules, or are some worth keeping?

2. **Content sources:** Where are the CADENCE subsystem documents I should use to populate real content?
   - Are they in Notion? (need page IDs)
   - Are they in GitHub? (which repos/paths?)
   - Are they PDFs? (where stored?)

3. **Enhancement priority:** Should I start with:
   - **Option A:** 3-5 flagship modules (deep, high-quality) for Beta to test
   - **Option B:** Breadth first (light enhancement of many modules)
   - **Option C:** Subsystem by subsystem (complete Power, then Avionics, etc.)

4. **Learning pathways:** Do you have a preferred competency progression model? Or should I propose one based on CADENCE project structure?

5. **Old database modules (IDs 71-82):** Should I:
   - **Option A:** Deprecate all (they don't match schema)
   - **Option B:** Migrate valuable ones to new JSON format
   - **Option C:** Keep for reference but mark as deprecated

---

## Next Steps (Pending Human Approval)

1. ✅ Complete this analysis (DONE)
2. ⏸️ Wait for human decisions on questions above
3. 📋 Create MODULE_VALIDATION_CHECKLIST.md (can do now)
4. 📋 Query database for old modules audit (can do now)
5. 📋 Generate final MODULE_AUDIT_REPORT.md combining all findings
6. ⏸️ Begin enhancement work on approved priority modules

---

## Files Referenced

- Canon: [MODULE_SCHEMA.md](../MODULE_SCHEMA.md)
- Canon: [SYSTEM_OVERVIEW.md](../../canon/SYSTEM_OVERVIEW.md)
- Source: `modules/enhanced/*.json` (68 files)
- Analysis script: Python analysis run 2025-11-30

---

**Agent Alpha - Session #3**
**Status:** Analysis complete, awaiting human guidance to proceed
