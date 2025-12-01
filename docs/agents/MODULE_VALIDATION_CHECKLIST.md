# Module Validation Checklist
**Agent:** Alpha
**Date:** 2025-11-30
**Purpose:** Quality control checklist for all module creation/enhancement
**Based on:** [MODULE_SCHEMA.md](../MODULE_SCHEMA.md)

---

## How to Use This Checklist

**Before committing any module:**
1. Open the module JSON file
2. Go through each section below
3. Check ✅ or fix ❌ each item
4. Only commit when ALL items are ✅

**For validation script:**
```bash
python scripts/enhance_modules.py --validate modules/enhanced/[module-name].json
```

---

## 1. Required Metadata Fields

### Basic Information
- [ ] `module_id` exists and is valid UUID (v5 from title)
- [ ] `title` is descriptive and specific (not generic)
- [ ] `slug` is lowercase, hyphen-separated, matches title
- [ ] `description` is 1-2 sentences explaining what students will learn
- [ ] `category` is one of: `Getting Started | Software Development | Hardware & Subsystems | Mission Design & Analysis | Systems Engineering`
- [ ] `discipline` is one of: `Software | Electrical | Aerospace | Systems | General`
  - ⚠️ Use "General" only if truly cross-disciplinary
- [ ] `target_audience` is one of: `Undergraduate | Graduate | Mixed`
- [ ] `estimated_minutes` is realistic integer (15-120 typical range)
- [ ] `difficulty` is one of: `Beginner | Intermediate | Advanced`
- [ ] `status` is one of: `Draft | Review | Published`

### Provenance
- [ ] `source_type` indicates origin: `Markdown | PDF | External Resource | Template`
- [ ] `source_file` points to original file or URL
- [ ] `record_source.type` is one of: `cadence-notion-export | cadence-pdf-rebuild | manual | enhanced`
- [ ] `created_at` is ISO timestamp (UTC)
- [ ] `updated_at` is ISO timestamp (UTC)

### Optional but Recommended
- [ ] `tags` array has 2-5 relevant keywords
- [ ] `prerequisites` array lists module slugs (if applicable)
- [ ] `concepts` array has 2-5 concept keywords
- [ ] `notion_page_id` if synced with Notion
- [ ] `github_file` path to this JSON in repo

---

## 2. Learning Objectives (CRITICAL)

Canon requirement: **2-5 objectives** per module

- [ ] Has **at least 2** learning objectives
- [ ] Has **at most 5** learning objectives
- [ ] Each objective follows this structure:
  ```json
  {
    "statement": "Action verb + specific outcome",
    "bloom_level": "Remember|Understand|Apply|Analyze|Evaluate|Create"
  }
  ```

### Bloom's Taxonomy Guide

**Remember** (recall facts):
- Verbs: List, Define, Identify, Name, Recall, State
- Example: "Identify the five CADENCE subsystems"

**Understand** (explain concepts):
- Verbs: Describe, Explain, Summarize, Classify, Compare
- Example: "Explain how F' Prime components communicate"

**Apply** (use in new situations):
- Verbs: Demonstrate, Execute, Implement, Solve, Use, Configure
- Example: "Configure a GitHub Actions workflow"

**Analyze** (examine relationships):
- Verbs: Analyze, Differentiate, Examine, Test, Troubleshoot
- Example: "Troubleshoot I2C communication errors"

**Evaluate** (make judgments):
- Verbs: Assess, Critique, Evaluate, Justify, Recommend
- Example: "Evaluate power budget options for mission constraints"

**Create** (produce new work):
- Verbs: Design, Develop, Construct, Create, Formulate
- Example: "Design a custom F' Prime component for sensor data"

### Quality Checks
- [ ] Objectives are **specific** (not "Understand [module title]")
- [ ] Objectives are **measurable** (student can demonstrate success)
- [ ] Objectives use **varied Bloom levels** (not all "Understand")
- [ ] Objectives progress from lower to higher cognitive levels
- [ ] At least one objective at "Apply" or higher

❌ **BAD Example:**
```json
{
  "statement": "Avionics Team Onboarding",
  "bloom_level": "Understand"
}
```

✅ **GOOD Example:**
```json
[
  {"statement": "Identify the three avionics subsystems in CADENCE", "bloom_level": "Remember"},
  {"statement": "Configure the F' Prime development environment", "bloom_level": "Apply"},
  {"statement": "Analyze telemetry data to diagnose sensor issues", "bloom_level": "Analyze"}
]
```

---

## 3. Sections (CRITICAL)

Canon requirement: **At least 3 sections** with specific types

- [ ] Has **at least 3 sections**
- [ ] Includes at minimum:
  - [ ] One `reading` section (intro/overview)
  - [ ] One `practice` or `quiz` section
  - [ ] One `reflection` section (or integrated into main sections)

### Section Type Requirements

#### `reading` Section
- [ ] Has `title`
- [ ] Has `type: "reading"`
- [ ] Has `content_markdown` with substantive content (>100 words)
  - ❌ NOT just the module title repeated
  - ❌ NOT generic "Review the resources..." placeholder
  - ✅ Actual technical explanation
- [ ] `assets` array present (even if empty)

#### `practice` Section
- [ ] Has `title`
- [ ] Has `type: "practice"`
- [ ] Has `steps` array with at least 2 steps
- [ ] Each step has:
  - [ ] `instruction` - specific, actionable task
  - [ ] `check` - how student verifies success
  - [ ] `hint` - guidance if stuck
  - [ ] `expected_duration_minutes` - realistic estimate
  - [ ] `requires_review` - boolean (true for complex tasks)

❌ **BAD Practice Step:**
```json
{
  "instruction": "Review the resources associated with [Topic] and note key dependencies.",
  "check": "Did you capture the primary goals and blockers?",
  "hint": "Summarize the main objective in one sentence before proceeding."
}
```

✅ **GOOD Practice Step:**
```json
{
  "instruction": "Clone the F' Prime repository and run `fprime-util new` to create a new component named 'LedBlinker'.",
  "check": "Verify you see the new component directory with Component.hpp, Component.cpp, and Component.fpp files.",
  "hint": "If the command fails, ensure you're in the project root directory and have sourced the F' Prime environment.",
  "expected_duration_minutes": 10,
  "requires_review": false
}
```

#### `quiz` Section
- [ ] Has `title`
- [ ] Has `type: "quiz"`
- [ ] Has `questions` array with at least 2 questions
- [ ] Each question has:
  - [ ] `question` - clear, specific question text
  - [ ] `type` - `multiple_choice | multi_select | short_answer | true_false`
  - [ ] `options` - array of choices (for multiple choice/multi-select)
  - [ ] `correct` - correct answer(s)
  - [ ] `explanation` - why the answer is correct
  - [ ] `concept_tags` - related concepts
  - [ ] `difficulty` - Beginner | Intermediate | Advanced

#### `reflection` Section
- [ ] Has `title`
- [ ] Has `type: "reflection"`
- [ ] Has `prompts` array with 1-3 open-ended questions
- [ ] Prompts encourage metacognition:
  - "What was most challenging?"
  - "How will you apply this?"
  - "What would you do differently?"

### Content Depth Check
- [ ] Reading sections have **substantive technical content** (not placeholders)
- [ ] Practice steps are **specific to the module topic** (not generic)
- [ ] Quiz questions test **actual learning objectives** (not generic "what's the purpose?")
- [ ] Reflection prompts are **thought-provoking** (not rote)

---

## 4. Reflection Prompts

- [ ] `reflection_prompts` array exists at root level
- [ ] Has at least 1 prompt
- [ ] Prompts are open-ended questions
- [ ] Prompts encourage application/transfer

Examples:
- "How will you apply this workflow in your CADENCE subsystem?"
- "What questions will you bring to your team lead?"
- "Which step was most challenging, and how did you overcome it?"

---

## 5. Race Metadata

- [ ] `race_metadata` object exists
- [ ] Has `ghost_data` array (can be empty initially - Gamma will populate)
- [ ] Has `time_targets` with `beginner`, `intermediate`, `advanced` keys
- [ ] Time targets are realistic (advanced < intermediate < beginner)
- [ ] Has `checkpoints` array with module-specific milestones
- [ ] Each checkpoint has:
  - [ ] `name` - specific milestone (not generic "Plan, Execute, Document")
  - [ ] `order` - integer sequence

❌ **BAD Checkpoints:**
```json
{
  "checkpoints": [
    {"name": "Plan", "order": 1},
    {"name": "Execute", "order": 2},
    {"name": "Document", "order": 3}
  ]
}
```

✅ **GOOD Checkpoints:**
```json
{
  "checkpoints": [
    {"name": "Environment setup complete", "order": 1},
    {"name": "Component created and compiling", "order": 2},
    {"name": "Telemetry verified in Ground System", "order": 3}
  ]
}
```

---

## 6. Prerequisites & Learning Pathways

- [ ] If module assumes prior knowledge, `prerequisites` array is populated
- [ ] Prerequisites reference valid module slugs (check they exist)
- [ ] Prerequisite chain doesn't create circular dependencies
- [ ] Module difficulty aligns with prerequisite difficulty
  - Beginner modules should have few/no prerequisites
  - Advanced modules should build on Intermediate modules

---

## 7. JSON Validation

- [ ] Valid JSON syntax (no trailing commas, proper quotes)
- [ ] No placeholder/TODO text like "[Topic]", "TBD", "Coming soon"
- [ ] No broken/empty fields:
  - No empty strings for required fields
  - No null values where objects/arrays expected
  - No "Unknown" or "N/A" in metadata
- [ ] All URLs (if any) are valid and accessible
- [ ] File paths (if any) use forward slashes (not Windows backslashes)

---

## 8. CADENCE-Specific Quality

- [ ] Content references actual CADENCE subsystems/tools where appropriate
- [ ] Examples use realistic CADENCE scenarios (not generic placeholders)
- [ ] If module is subsystem-specific:
  - [ ] Title clearly indicates subsystem (Power, Avionics, etc.)
  - [ ] Content includes subsystem-specific technical details
  - [ ] Prerequisites include subsystem orientation module
- [ ] If module is tool-specific (GitHub, F' Prime, etc.):
  - [ ] Instructions are step-by-step and testable
  - [ ] Examples use CADENCE project structure where possible

---

## 9. Accessibility & Inclusivity

- [ ] Language is clear and jargon is explained
- [ ] Instructions don't assume prior expertise (unless prerequisites defined)
- [ ] Examples are diverse (not always same scenario)
- [ ] No unnecessary cultural references that might exclude
- [ ] Content is respectful and professional

---

## 10. Final Validation

### Automated Check
```bash
python scripts/enhance_modules.py --validate modules/enhanced/[module-name].json
```

### Manual Check
- [ ] Read through the entire module as if you're a student
- [ ] Can you complete the practice steps with the information provided?
- [ ] Do the quiz questions test what the objectives promised?
- [ ] Would this module prepare someone for its dependent modules?
- [ ] Is the estimated_minutes realistic for the content depth?

### Peer Review (Recommended)
- [ ] Have another agent or human review the module
- [ ] Test practice steps in actual environment
- [ ] Verify all links/resources are accessible

---

## Validation Script Output

When running `--validate`, expect:
```
✅ Valid JSON syntax
✅ All required fields present
✅ 3 learning objectives (target: 2-5)
✅ 4 sections (target: ≥3)
✅ Practice section has 5 steps
✅ Quiz section has 3 questions
✅ Race metadata complete
⚠️ Prerequisites array empty (consider adding if applicable)
✅ MODULE PASSES VALIDATION
```

---

## Common Errors to Avoid

### 1. Stub Content
❌ "Review the resources associated with [Topic]"
✅ "Clone the repository at github.com/cadence/power-analysis and navigate to the battery-sizing directory"

### 2. Vague Objectives
❌ {"statement": "Communications Subsystem", "bloom_level": "Understand"}
✅ {"statement": "Configure a UHF radio link budget for LEO operations", "bloom_level": "Apply"}

### 3. Untestable Practice Steps
❌ "Think about how you would approach this problem"
✅ "Run `pytest tests/test_battery.py` and verify all 5 tests pass"

### 4. Generic Quizzes
❌ "What is the primary objective of this module?"
✅ "What is the minimum power requirement for CADENCE's avionics suite during eclipse?"

### 5. Missing Prerequisites
❌ Advanced module has `prerequisites: []`
✅ `prerequisites: ["power-subsystem-orientation", "battery-chemistry-basics"]`

---

## Checklist Summary

Before marking module as "Published":
- [ ] All required metadata fields ✅
- [ ] 2-5 specific, measurable learning objectives ✅
- [ ] At least 3 sections with substantive content ✅
- [ ] Practice steps are specific and testable ✅
- [ ] Quiz questions test actual learning outcomes ✅
- [ ] Reflection prompts encourage metacognition ✅
- [ ] Race metadata has module-specific checkpoints ✅
- [ ] Prerequisites defined (if applicable) ✅
- [ ] JSON validates with script ✅
- [ ] Manual review complete ✅

---

**Agent Alpha - Quality Assurance Tool**
**Last updated:** 2025-11-30
