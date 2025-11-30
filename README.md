# FRAMES / Ascent Basecamp

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![JavaScript](https://img.shields.io/badge/javascript-ES6+-yellow.svg)
![React](https://img.shields.io/badge/react-18+-61dafb.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-000000.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-15+-316192.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## FRAMES (Predictive AI Modeling + Research Framework)

**Who it serves:**  
Researchers, faculty, system architects, and anyone studying how engineering teams behave and collaborate over long periods of time.

**What it is:**  
A research-driven analytical framework built on Non-Decomposable Architecture (NDA) principles.  
FRAMES models how knowledge moves through engineering programs, how teams interface with one another, and where structural friction points appear.  
It provides the foundation for predictive AI models that examine engagement, collaboration quality, onboarding effectiveness, and system resilience.

**Why it exists:**  
Because programs lose essential knowledge every semester as students graduate, and traditional onboarding can't capture the true patterns of collaboration beneath the surface.  
FRAMES makes those invisible patterns measurable so programs can improve continuity, reduce failure points, and understand how their systems behave as a whole.

---

## Ascent Basecamp (The Applications Built on FRAMES)

**Who it serves:**  
Students, mentors, team leads, and faculty actively participating in engineering projects across multiple universities.

**What it is:**  
The practical, user-facing suite of applications built on top of the FRAMES framework and database.  
Ascent Basecamp includes the student onboarding modules, team lead project management tools, the researcher analytics dashboard, and the AI-assisted content workflows.  
It translates the research foundations of FRAMES into tools people can use every day.

**Why it exists:**  
To provide a consistent, structured, and human-centered environment where students can learn, teams can coordinate, and faculty can monitor progress—while all data continually feeds back into the research framework that strengthens the program over time.

---

## System Architecture

```
                      ┌──────────────────────────┐
                      │          FRAMES          │
                      │  Research + Predictive   │
                      │    Modeling Framework     │
                      └──────────────┬───────────┘
                                     │
                          (Shared PostgreSQL DB)
                                     │
        ┌────────────────────────────┼──────────────────────────────┐
        │                            │                              │
┌───────▼────────┐        ┌──────────▼─────────┐         ┌──────────▼─────────┐
│ Student LMS     │        │ Team Lead Builder  │         │ Researcher Platform │
│ Onboarding App  │        │ Project Mgmt Tools │         │ Analytics + Models  │
└─────────────────┘        └────────────────────┘         └────────────────────┘
                                     │
                                     │
                           ┌─────────▼─────────┐
                           │  Agentic Swarm    │
                           │  (Guarded Tools)  │
                           └───────────────────┘
```

---

## The Five Components

### 1. Student Onboarding Modules

**Who it serves:**  
Students joining engineering teams who need a clear path into complex technical work.

**What it is:**  
A set of structured learning modules—short, focused, and standardized—that guide students through the tools, processes, and subsystem practices they need to participate effectively.

**Why it exists:**  
To remove confusion, reduce overwhelm, and give every new student a reliable way to build foundational knowledge without depending entirely on verbal explanations from busy mentors.

📄 **Learn more** → [`canon/STUDENT_LMS.md`](canon/STUDENT_LMS.md)

---

### 2. Team Lead Project Management & Module Builder

**Who it serves:**  
Team leads, mentors, and subsystem managers responsible for training new recruits.

**What it is:**  
A simplified workspace where team leads can organize tasks, create or refine training materials, and produce consistent modules using templates and controlled content workflows.

**Why it exists:**  
To eliminate repeated semester-to-semester re-teaching, preserve institutional knowledge, and standardize how training materials are created so consistency is maintained across teams and universities.

📄 **Learn more** → [`canon/TEAM_LEAD_MODULE_BUILDER.md`](canon/TEAM_LEAD_MODULE_BUILDER.md)

---

### 3. Researcher AI Predictive Modeling & Analytics

**Who it serves:**  
Faculty, program directors, systems engineers, and researchers studying learning, collaboration, and system resilience.

**What it is:**  
A set of analytical tools connected to the shared database that examine engagement patterns, team interactions, system structure, and long-term trends using NDA principles and predictive modeling.

**Why it exists:**  
To give researchers visibility into where learning breaks down, how knowledge flows through the program, and how multi-university engineering systems can be strengthened over time.

📄 **Learn more** → [`canon/RESEARCHER_PLATFORM.md`](canon/RESEARCHER_PLATFORM.md)

---

### 4. Centralized Data Management (The FRAMES Database)

**Who it serves:**  
All users of the system—students, mentors, researchers, administrators—and all three applications.

**What it is:**  
A Neon-hosted PostgreSQL database that stores modules, analytics, team structures, progress data, research metrics, and program-wide information in one unified, consistent schema.

**Why it exists:**  
To eliminate scattered documentation, version conflicts, and information loss, ensuring that every application draws from the same accurate source of truth.

📄 **Learn more** → [`canon/DATABASE_SCHEMA.md`](canon/DATABASE_SCHEMA.md)

---

### 5. Agentic Swarm (Controlled AI Layer)

**Who it serves:**  
Developers maintaining the system, team leads producing modules, and researchers who rely on consistent documentation.

**What it is:**  
A set of controlled AI agents that operate within strict guardrails to help format content, maintain files, support migrations, and preserve consistency without autonomously creating new structures or pages.

**Why it exists:**  
To accelerate development and documentation while preventing the uncontrolled creation of content, ensuring that AI supports human decisions rather than replacing or overriding them.

📄 **Learn more** → [`canon/AGENT_SYSTEM_OVERVIEW.md`](canon/AGENT_SYSTEM_OVERVIEW.md)

---

## Getting Started

### 👨‍💻 For Developers (Using the Code)

**You want to:** Run the system locally, understand the architecture, contribute code, or deploy your own instance.

**Start here:**
- 📄 **[System Overview](canon/SYSTEM_OVERVIEW.md)** — Overall architecture and how components connect
- 📄 **[Database Schema](canon/DATABASE_SCHEMA.md)** — Complete PostgreSQL schema with 37+ tables
- 📄 **[File Structure & Standards](canon/FILE_STRUCTURE_AND_STANDARDS.md)** — Repository organization and coding conventions

**Quick Start:**
```bash
git clone https://github.com/Lizo-RoadTown/FRAMES-Python.git
cd FRAMES-Python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Add your Neon PostgreSQL URL
python backend/app.py
```

---

### 🔬 For Researchers (Using the Platform for Research)

**You want to:** Access analytics, study collaboration patterns, run NDA models, or analyze learning data.

**Start here:**
- 📄 **[Researcher Platform](canon/RESEARCHER_PLATFORM.md)** — Analytics dashboards, NDA modeling, multi-university comparisons
- 📄 **[FRAMES Philosophy](canon/FRAMES_PHILOSOPHY.md)** — Research foundations and theoretical framework
- 📄 **[Database Schema](canon/DATABASE_SCHEMA.md)** — Understanding the data structure for analysis

**What you can do:**
- Access cross-university engagement metrics
- Model team interfaces and knowledge transfer friction
- Track student progression and time-on-task analytics
- Export data for custom analysis and predictive modeling

---

### 📚 For Students (Using the Platform to Learn)

**You want to:** Complete onboarding modules, learn mission-critical skills, and track your progress.

**Start here:**
- 📄 **[Student LMS](canon/STUDENT_LMS.md)** — How the learning modules work
- 📄 **[OATutor Adaptation](canon/OATUTOR_ADAPTATION.md)** — The pedagogical approach behind the modules

**What you get:**
- Structured learning paths tailored to your team's actual work
- Step-by-step modules created from real mission procedures
- Progress tracking without grades or tests
- Mobile-friendly PWA accessible anywhere

---

## Contact

**Project Lead & Research Developer:**  
Elizabeth Osborn  
📧 eosborn@cpp.edu  
Cal Poly Pomona

**Partner Universities:**  
Cal Poly Pomona • Cal Poly SLO • Arizona State University • University of Colorado Boulder • UCLA • USC • Stanford • UC Berkeley

---

<div align="center">

**[📖 Canonical Docs](canon/)** • **[🗺️ Migration Map](MIGRATION_MAP.md)** • **[🤖 Agent System](canon/AGENT_SYSTEM_OVERVIEW.md)** • **[🧠 FRAMES Philosophy](canon/FRAMES_PHILOSOPHY.md)**

</div>
