# FRAMES / Ascent Basecamp

*A unified learning + research ecosystem for multi-year student space missions.*

FRAMES (Framework for Resilience Assessment in Modular Engineering Systems) / **Ascent Basecamp** is:

- A way to **onboard students** into complex engineering projects  
- A way for **team leads** to turn real work into reusable training  
- A way for **researchers** to study how space mission teams actually function  
- A home for a **controlled agent swarm** that helps maintain the system

Everything runs on a **single PostgreSQL database** shared by three applications:
- Student onboarding LMS  
- Team lead module builder  
- Research analytics platform  

This README is a **map** to that world, not the whole world.

---

## 1. What Lives in This Repository?

Think of this repo as one system with three faces:

1. **Student Onboarding LMS**  
   - React-based PWA for students  
   - Delivers hands-on modules based on real mission work  
   - Tracks time, scroll, revisit patterns (no grades, no tests)

2. **Team Lead Module Builder**  
   - Web admin tools for creating and maintaining modules  
   - Takes Notion content, OAtutor-style structuring, and agent help  
   - Keeps team leads out of Git and JSON as much as possible  

3. **Researcher Analytics Platform**  
   - Flask-based analytics and APIs  
   - Models collaboration using Non-Decomposable Architecture (NDA)  
   - Supports multi-university, multi-cohort analysis

All three talk to a **single Postgres schema** that already includes CADENCE program data, Ascent Basecamp tables, and student learning tables.  
For the full schema, see:  
👉 `canon/DATABASE_SCHEMA.md`

---

## 2. Where to Start (Depending on Who You Are)

### 🧑‍🎓 New Student / Curious Reader  
You want: *"What is this and why does it exist?"*

Start here:  
- **System overview**  
  👉 `canon/SYSTEM_OVERVIEW.md`  

This explains:
- Why FRAMES exists  
- How modules relate to real missions  
- What "onboarding engine" actually means  

---

### 🛠️ Team Lead / Content Owner  
You want: *"How do I get my training materials into this system?"*

Start here:  
- **Team Lead Module Builder**  
  👉 `canon/TEAM_LEAD_MODULE_BUILDER.md`  

Then see:
- **Student LMS technical design** (how modules are stored and played)  
  👉 `canon/STUDENT_LMS.md`  

This pair explains:
- How you submit content (Notion, forms, or AI-assisted)  
- How modules are structured in the database  
- What the student experience looks like end-to-end  

---

### 🔭 Researcher / Architect  
You want: *"How does this tie into NDA, interfaces, and analytics?"*

Start here:  
- **Researcher Platform**  
  👉 `canon/RESEARCHER_PLATFORM.md`  

Then:
- **Complete system architecture**  
  👉 `canon/SYSTEM_OVERVIEW.md`  

This covers:
- Multi-university architecture  
- NDA diagnostics and modeling  
- Research analytics capabilities  

---

### 🤖 Agent Developer / AI Integrator  
You want: *"What are these three agents and how are they supposed to behave?"*

Start here:  
- **Agent system overview**  
  👉 `canon/AGENT_SYSTEM_OVERVIEW.md`  

Then:  
- **Agent safety rules**  
  👉 `canon/AGENT_SAFETY_RULES.md`  

Also important:
- **Agent work queues**  
  👉 `agent_work_queues/alpha_queue.md`  
  👉 `agent_work_queues/beta_queue.md`  
  👉 `agent_work_queues/gamma_queue.md`  

These explain:
- Roles for Alpha (modules), Beta (platform), Gamma (infrastructure)  
- How agents claim work, log actions, and ask for help  
- How they are supposed to respect the architecture instead of inventing a new one

---

## 3. The Core Shape of the System

At the highest level:

```text
          One PostgreSQL Database (Neon)
        ───────────────────────────────────
        • CADENCE historical program data
        • Ascent Basecamp learning tables
        • Student performance + cohorts
        • Agent logs + technical decisions
```

Three major applications share this database:

**Student Onboarding LMS**
- Modules, sections, analytics events, learner performance
- Designed for mobile / PWA consumption
- No live AI during runtime (deterministic student experience)

**Team Lead / Content Management**
- Uses Notion as the authoring surface
- Imports structured module specs from CSV, forms, or AI-structured text
- Produces modules that the LMS can run, versioned in the DB

**Researcher Dashboard / Analytics**
- Pulls from the same DB
- Computes NDA metrics, interface loads, performance patterns
- Future: prediction models, pgvector-based search, exploration tools

For a deeper, line-by-line breakdown, use:  
👉 `canon/STUDENT_LMS.md`  
👉 `canon/RESEARCHER_PLATFORM.md`

---

---

## 4. AI & Agents (What They Are Actually Allowed to Do)

The agentic layer is not a mysterious swarm. It has explicit rules:

- Agents operate against the same Postgres database as humans.
- They have startup protocols (read chat logs, check queues, inspect help requests).
- They must log all significant actions to `ascent_basecamp_agent_log`.
- They are **not allowed** to create new Notion structures unless:
  - A template exists, **and**
  - There is an explicit directive, **or**
  - You've approved the pattern.

You'll find patterns and examples in:
- `canon/AGENT_SYSTEM_OVERVIEW.md`
- `docs/agents/AGENT_TEAM_CHAT.md` (running coordination log)
- `docs/notion/NOTION_DESIGN_BEST_PRACTICES.md`

Use these as **contracts**, not suggestions.

---

## 5. Teaching Model: From Notion + OAtutor Principles → Engineering Modules

The student LMS is not a quiz engine. It's built around:

- **Team lead content** (real lab / mission work) from Notion
- **AI-assisted structuring** (short sections, clear goals, estimated time)
- **Concepts borrowed from OAtutor** (gradual progression, stepwise explanation), adapted for hands-on engineering instead of pure math.

The pipeline looks like:

```
Notion content / Slides / SOPs
          ↓
AI helps team lead structure content
          ↓
Module specs (JSON / DB)
          ↓
Student LMS (React PWA)
          ↓
Analytics → Researcher Platform
```

Details for the LMS module system live in:  
👉 `canon/STUDENT_LMS.md`  
👉 `canon/TEAM_LEAD_MODULE_BUILDER.md`  
👉 `canon/OATUTOR_ADAPTATION.md`

---

## 6. For Developers: Minimal Quick Start

**Goal:** Get a backend running and see that the stack is alive.  
This is not the full dev guide; it just proves the project is wired.

```bash
# Clone repository
git clone https://github.com/Lizo-RoadTown/FRAMES-Python.git
cd FRAMES-Python

# Set up Python environment
python -m venv venv
# Windows:
#   venv\Scripts\activate
# Mac/Linux:
#   source venv/bin/activate

pip install -r requirements.txt

# Copy and edit environment
cp .env.example .env
# Edit .env to add your Neon PostgreSQL URL

# Run Flask backend
python backend/app.py
```

Then open:  
👉 http://localhost:5000

Frontends (Student LMS, Team Lead UI) have their own READMEs in their respective subfolders (for example `apps/onboarding-lms/frontend-react/` if present).

---

---

## 7. Repository Organization (Conceptual)

Rather than list every folder, here's how to think about the structure:

**`canon/`**  
All authoritative documentation lives here. 14 files that define system architecture, database schema, agent rules, application specs. When in doubt, start with `canon/INDEX.md`.

**`backend/`**  
Flask app, database access, APIs for LMS, analytics, and agent coordination.

**`apps/` or `frontend/`**  
React-based student and admin interfaces (when present).

**`docs/`**  
Additional documentation organized by topic (agents, notion, cadence, guides).  
When in doubt, prefer canonical docs in `canon/` over anything in `docs/archive/`.

**Agent working files**  
- `docs/agents/AGENT_TEAM_CHAT.md`
- `agent_work_queues/`

These are used by autonomous agents and should stay machine-friendly but human-legible.

**CADENCE / legacy content**  
Source data, markdown exports, and Notion-derived artifacts that feed module creation and research.

Over time, older documents are moved into `archive/` and indexed in `MIGRATION_MAP.md` so agents and humans know what is current.

---

---

## 8. Contact

**Project Lead & Research Developer:**  
Elizabeth Osborn, Ph.D.  
📧 eosborn@cpp.edu  
Cal Poly Pomona

---

<div align="center">

**[📖 Canonical Docs](canon/)** • **[🗺️ Migration Map](MIGRATION_MAP.md)** • **[🤖 Agent System](canon/AGENT_SYSTEM_OVERVIEW.md)**

</div>
