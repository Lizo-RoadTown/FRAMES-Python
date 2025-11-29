# System Overview for AI Agents

## 1. What This System Is

We are building an Onboarding & Training Engine for big, complex student projects (e.g., multi-year NASA-style missions).

Team leads already manage their work in Notion dashboards.

We do not replace their process.

We read what they’re already doing and turn it into interactive onboarding modules for new students.

New students:

- Use these modules (mostly solo; sometimes in collaborative or competitive modes).
- Get up to speed on tools, processes, and subsystems.
- Compete on leaderboards, race old cohorts, and occasionally “race” scripted AI classmates to keep the experience fun and less intimidating.

AI’s role:

- AI helps build and maintain the system.
- AI transforms Notion content into structured modules.
- AI does NOT run the learning experience live (runtime should be deterministic and testable).

## 2. Who the System Is For

### Team Leads / Project Leads
- Use Notion dashboards to manage real work.
- Do not have time to hand-hold every new student.
- Need a way to bring new cohorts onboard without losing momentum.

### New Students / Cohort Members
- Join big, ongoing projects (multi-year builds).
- Often feel lost and overwhelmed.
- Need structured, hands-on, “do this in the real environment” training.

### Program Owners / Faculty / Lab Directors
- Need evidence that onboarding is working.
- Need the system to survive across semesters and student turnover.

### AI agents:
Backend assistants and “compilers” that:

- keep Notion organized as a source of truth,
- extract and normalize information,
- build and update onboarding modules,
- maintain consistency with system rules.

## 3. High-Level Architecture (Three Layers)

### 3.1 Authoring Layer (Notion)
Humans work in Notion normally. We add:
- Module Sources DB
- Key documentation
- SOPs
- Decision logs
- Subsystem pages

### 3.2 Transformation Layer (AI + Backend)
AI reads Module Sources → produces structured modules → stores module specs.

This layer:
- enforces educational framework
- ensures module schema consistency
- tags modules with concepts/difficulty
- attaches race/leaderboard metadata

### 3.3 Runtime Layer (Student Experience)
- Students run modules
- Interact with real tools
- Race cohorts or AI classmates
- Scores + progress logged

No live AI. Deterministic.

## 4. What a Module Is

A module is a hands-on structured learning experience based on real project work.

Includes:
- clear goal
- defined steps
- checks
- quizzes
- reflection
- optional race/competition/humor layer

Everything revolves around modules.

## 5. Module Types

- Solo Core Modules
- Challenge / Race Modules
- Collaborative Modules
- Mood-Lightening / Humorous Modules

All share:
- objectives
- steps
- checks
- metadata

## 6. How Notion Fits In

- Notion dashboards must stay clean + structured.
- Not used as a training environment.
- Mark source content via Module Sources or tags.
- Agents extract structured data only.

## 7. Educational Goals

- Ease onboarding
- Turn real work into structured modules
- Preserve institutional knowledge
- Provide foundation + practice + challenge + humor

Non-goals:
- Replace Notion
- Replace team leads
- Build a full LMS at this stage
- Use live AI tutoring during modules

## 8. AI Agent Responsibilities

- Maintain consistency with system architecture
- Enforce module schema + educational framework
- Keep Notion organized
- Create/update modules from content
- Respect scope boundaries
- Document decisions clearly

## 9. Typical Flows

### Flow A: Team Lead Adds Content → New Module
- Tag Module Source
- AI reads content
- AI builds module spec
- Runtime picks it up

### Flow B: Hard Concept → Challenge Module
- AI clones core module
- Adds timers, race metadata, ghosts, AI classmates

### Flow C: Cohort Performance → Updates
- Runtime logs attempts
- AI analyzes performance
- Updates ghost data
- Improves modules
