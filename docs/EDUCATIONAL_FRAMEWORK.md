# Educational Framework for CADENCE Modules

## Why This Framework Exists
- Translate CADENCE project knowledge into structured, measurable learning experiences.
- Ensure non-linear onboarding: recruits can start anywhere, yet every module follows the same anatomy.
- Support automation: enhancement scripts, analytics, OAtutor integration, and race/leaderboard features require consistent JSON fields.

## Module Philosophy
1. **Mission Context First** – Every module relates back to a CADENCE subsystem or workflow so learners connect the dots.
2. **Hands-on Practice** – Learners must apply what they read; practice steps always include validation checks and hints.
3. **Immediate Feedback** – Knowledge checks and practice steps include checks/explanations to close the loop.
4. **Reflection & Retention** – Modules end with reflection prompts; insights feed progress analytics and team discussions.
5. **Competition as Motivation** – Race metadata enables optional time-based challenges that energize advanced learners.

## Module Anatomy
| Component | Purpose | Automation Notes |
|-----------|---------|-------------------|
| Metadata | Category, difficulty, estimated minutes, tags | Mandatory; used by dashboards and analytics |
| Learning Objectives | 2–5 measurable statements w/ Bloom levels | Used for enhancement QA and future assessments |
| Sections | Reading, practice, quiz, reflection (minimum) | Each section has `type` + specific subfields |
| Practice Steps | Workflow instructions + checks/hints | Steps feed React/OAtutor practice components |
| Knowledge Check | Quiz items to confirm mastery | Generates analytics events + leaderboard deltas |
| Reflection Prompts | Retrospective questions | Stored for future mentoring/responses |
| Race Metadata | Optional timed challenges | Drives race/ghost features in the app |

## Authoring Guide
1. **Start from Existing Content**
   - Pull raw text from Notion exports or PDF rebuilds (`modules/exports/`).
   - Identify the key objective(s) and who benefits (target audience).

2. **Define Learning Objectives**
   - Use Bloom’s verbs (Remember, Understand, Apply, Analyze, Evaluate, Create).
   - Make objectives concrete and measurable.

3. **Structure Sections**
   - **Overview**: Summarize the mission context, include any prerequisites.
   - **Hands-on Practice**: Break tasks into steps with `instruction`, `check`, `hint`, `expected_duration_minutes`.
   - **Knowledge Check**: Include at least two questions; provide explanations for each correct answer.
   - **Reflection**: Ask learners what they would repeat/improve.

4. **Add Metadata**
   - `category` from the Module Library select options.
   - `difficulty` approximate complexity.
   - `estimated_minutes` = honest effort estimate for first-time learners.
   - `tags` / `concepts` for analytics/search.

5. **Optional Features**
   - **Race Metadata**: Provide `time_targets` and `checkpoints` when modules involve timed tasks.
   - **Collaborative Elements**: Use a practice step to request peer review or joint documentation.

## Automation Alignment
- `scripts/audit_module_library.py` ? identifies stubs/missing fields.
- `scripts/enhance_modules.py` ? generates baseline objectives/sections per module.
- Future enhancements can swap in generative content, but must preserve schema fields defined in `docs/MODULE_SCHEMA.md`.

## Quality Checklist
- [ ] Objectives align with content and Bloom’s taxonomy.
- [ ] Practice steps include validations (`check`) and hints.
- [ ] Knowledge check questions cover critical concepts and include explanations.
- [ ] Reflection prompts encourage actionable insight.
- [ ] Metadata (category, difficulty, estimated minutes, tags) populated.
- [ ] Race metadata populated (if the module involves timed execution).
- [ ] JSON validates and lives under `modules/enhanced/`.

## File Locations
- Enhanced modules: `modules/enhanced/*.json`
- Templates: `templates/modules/*.json`
- Schema reference: `docs/MODULE_SCHEMA.md`
- Audit report: `module_library_audit.json`

## Future Work
- Expand quiz generation with context-aware prompts.
- Capture learner responses for analytics loops.
- Add collaborative and race modules directly within Notion for preview before export.

This framework ensures Alpha’s module enhancements stay consistent and automation-friendly while still feeling human and mission-aligned.
