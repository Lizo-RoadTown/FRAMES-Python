# OAtutor-Compatible Module Schema

## Purpose
Provide a canonical structure for CADENCE learning modules so they can flow through every surface: Notion, GitHub, Neon/PostgreSQL, React (react-notion-x), and OAtutor-style learning experiences. Every module JSON must follow this schema to enable automated enhancement, analytics, and race/leaderboard features.

## Root Object
```jsonc
{
  "module_id": "uuid-v5",
  "title": "String",
  "slug": "kebab-case-identifier",
  "description": "Markdown summary",
  "category": "Getting Started | Software Development | Hardware & Subsystems | Mission Design & Analysis | Systems Engineering",
  "discipline": "Software | Electrical | Aerospace | Systems | General",
  "target_audience": "Undergraduate | Graduate | Mixed",
  "estimated_minutes": 60,
  "difficulty": "Beginner | Intermediate | Advanced",
  "status": "Draft | Review | Published",
  "source_type": "Markdown | PDF | External Resource",
  "source_file": "Original filename or URL",
  "tags": ["concept", "tool"],
  "prerequisites": ["module-slug-1", "module-slug-2"],
  "learning_objectives": [
    {
      "statement": "Describe X",
      "bloom_level": "Remember | Understand | Apply | Analyze | Evaluate | Create"
    }
  ],
  "concepts": ["avionics", "github"],
  "sections": [],
  "reflection_prompts": [],
  "race_metadata": {},
  "notion_page_id": "UUID",
  "github_file": "modules/exports/module-slug.json",
  "record_source": {
    "type": "cadence-notion-export | cadence-pdf-rebuild | manual",
    "archive": "path or URL",
    "entry_name": "original filename"
  },
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp"
}
```

## Learning Objectives
- `learning_objectives` array must contain 2–5 entries.
- Every objective is measurable and tagged with Bloom’s taxonomy level.
- Example:
```json
{
  "learning_objectives": [
    {"statement": "Identify avionics subsystems", "bloom_level": "Remember"},
    {"statement": "Configure F Prime dev environment", "bloom_level": "Apply"},
    {"statement": "Evaluate telemetry data for anomalies", "bloom_level": "Evaluate"}
  ]
}
```

## Sections Array
Each section captures a coherent learning activity. Types supported:
- `reading`: narrative content with Markdown.
- `practice`: procedural steps (`steps` array) with checks/hints.
- `quiz`: knowledge check (`questions` array).
- `reflection`: prompts/questions for retrospection.
- `reference`: link bundle or document references.
- `race`: timed challenge metadata.

Base schema:
```json
{
  "sections": [
    {
      "title": "Introduction",
      "type": "reading",
      "content_markdown": "Markdown text...",
      "assets": []
    },
    {
      "title": "Hands-on Practice",
      "type": "practice",
      "steps": [
        {
          "instruction": "Clone repository ...",
          "check": "Verify `git status` shows clean working tree.",
          "hint": "Use `git branch` to confirm you are on `main`.",
          "expected_duration_minutes": 10
        }
      ]
    },
    {
      "title": "Knowledge Check",
      "type": "quiz",
      "questions": [
        {
          "question": "Which command initializes F Prime environment?",
          "type": "multiple_choice",
          "options": ["fprime-util new", "cmake ..", "npm start"],
          "correct": "fprime-util new",
          "explanation": "F Prime projects bootstrap via `fprime-util new`.",
          "concept_tags": ["fprime", "setup"]
        }
      ]
    }
  ]
}
```

### Practice Step Schema
```json
{
  "instruction": "Perform action ...",
  "check": "What validates success?",
  "hint": "Optional hint text",
  "resources": ["URL", "Notion link"],
  "expected_duration_minutes": 5,
  "requires_review": false
}
```

### Quiz Question Schema
Supported `type`: `multiple_choice`, `multi_select`, `short_answer`, `true_false`.
```json
{
  "question": "Explain ...",
  "type": "short_answer",
  "options": [],
  "correct": "Expected answer or array of values",
  "explanation": "Why the answer matters",
  "concept_tags": ["telemetry"],
  "difficulty": "Beginner | Intermediate | Advanced"
}
```

## Reflection Prompts
Array of open-ended prompts:
```json
{
  "reflection_prompts": [
    "What was the most challenging subsystem?",
    "How will you apply this workflow in your team?"
  ]
}
```

## Race Metadata (Optional)
Used for competition/race modules.
```json
{
  "race_metadata": {
    "ghost_data": [
      {"time_seconds": 420, "notes": "Standard track"},
      {"time_seconds": 360, "notes": "Advanced track"}
    ],
    "time_targets": {"beginner": 600, "intermediate": 420, "advanced": 300},
    "checkpoints": [
      {"name": "Environment setup", "order": 1},
      {"name": "Telemetry decode", "order": 2}
    ]
  }
}
```

## Metadata Requirements
| Field | Required? | Notes |
|-------|-----------|-------|
| `module_id` | Yes | Deterministic UUID (v5) from title |
| `slug` | Yes | Lowercase, hyphen-separated |
| `category` | Yes | Must match select options |
| `difficulty` | Yes | Beginner/Intermediate/Advanced |
| `estimated_minutes` | Yes | Integer |
| `learning_objectives` | Yes | ≥2 entries |
| `sections` | Yes | ≥3 entries: intro, practice, quiz |
| `reflection_prompts` | Recommended | At least 1 |
| `race_metadata` | Optional | For challenge variants |
| `tags` | Recommended | Concept keywords |
| `prerequisites` | Recommended | Slugs of earlier modules |
| `notion_page_id` | Optional | For back-reference |
| `github_file` | Optional | Path to JSON in repo |
| `record_source` | Yes | Track provenance |
| `created_at / updated_at` | Yes | Timestamps (UTC) |

## Validation Checklist
- [ ] Title + slug present
- [ ] At least 3 learning objectives
- [ ] At least 3 sections with required types
- [ ] Practice section includes steps with checks/hints
- [ ] Quiz section includes ≥2 questions
- [ ] Metadata fields populated (category, difficulty, estimated_minutes)
- [ ] Reflection prompts provided
- [ ] Tags/prerequisites set
- [ ] Race metadata included if module involves timed challenge
- [ ] JSON validates against schema (run `scripts/enhance_modules.py --validate`)

## Enhancement Workflow Alignment
The enhancement pipeline (`scripts/enhance_modules.py`) will:
1. Read `module_library_audit.json` to detect stubs.
2. Pull raw content from `module["sections"]` or `raw_markdown`.
3. Generate missing objectives, steps, and quizzes per schema.
4. Output enhanced modules to `modules/enhanced/` following this document.
5. Validate against schema before committing.

## Storage & Sync
- **GitHub**: `modules/enhanced/*.json` is canonical module content.
- **Neon/Postgres**: stores metadata + sections; API feeds React + OAtutor renderer.
- **Notion**: presentation layer and coordination hub; no schema enforcement.
- **React App**: consumes API JSON, renders via `react-notion-x` + custom components.
- **Analytics/Leaderboard**: rely on consistent metadata (difficulty, estimated_minutes, tags).

## References
- `system_overview_for_ai_agents.md` – pipeline context
- `cadence_spec_full/` – CADENCE data contract
- `NOTION_WORKSPACE_ENHANCEMENT.md` – Notion layout
- `NOTION_DESIGN_BEST_PRACTICES.md` – design aesthetics
- `THREE_AGENT_INDEPENDENT_PLAN.md` – execution plan for Alpha/Beta/Gamma

This schema is the authoritative contract for module JSON. Any automation (enhancement, analytics, deployment) must adhere to it. All new modules should be authored against this structure to ensure compatibility across FRAMES services.
