# FRAMES / Ascent Basecamp

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-316192.svg)](https://www.postgresql.org/)

> **Multi-university research platform for space mission programs with AI-powered student training.**

## 🎯 What is FRAMES?

FRAMES (Framework for Resilience Assessment in Modular Engineering Systems) / Ascent Basecamp is a unified ecosystem built on:

- **One PostgreSQL database** (Neon hosted)
- **Three user-facing applications**
- **Embedded agent swarm** for autonomous development
- **Notion integration** for content management

### Three Applications

1. **Student Onboarding LMS** - Mobile-first PWA for student training
2. **Team Lead Module Builder** - Admin workspace for creating training content  
3. **Researcher Platform** - Analytics dashboards + AI predictions

**Status:** Student LMS in active development, Research analytics operational

```
┌──────────────────────────────────────┐
│      PostgreSQL Database (Neon)      │
│   37 tables • 8 universities         │
└────────┬──────────────┬──────────────┘
         │              │              
    ┌────▼────┐   ┌────▼────┐   ┌──────────┐
    │ Student │   │  Team   │   │Researcher│
    │   LMS   │   │  Lead   │   │ Platform │
    │ (React) │   │ Builder │   │ (Flask)  │
    └─────────┘   └─────────┘   └──────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for React frontends)
- PostgreSQL database (Neon recommended)

### Get Started in 3 Steps

1. **[📖 Start Here: Canon Index](canon/INDEX.md)** - Master documentation index
2. **[🏗️ System Overview](canon/SYSTEM_OVERVIEW.md)** - Complete architecture guide
3. **[🗂️ Monorepo Structure](MONOREPO_STRUCTURE.md)** - Repository organization

### For Developers

```bash
# Clone repository
git clone https://github.com/Lizo-RoadTown/FRAMES-Python.git
cd FRAMES-Python

# Set up Python environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

pip install -r requirements.txt

# Configure database connection
cp .env.example .env
# Edit .env with your Neon PostgreSQL connection string

# Run Flask backend
python backend/app.py

# Open browser: http://localhost:5000
```

---

## 📚 Documentation

> **📍 Start Here:** All authoritative documentation is in [`/canon`](canon/) directory

### 🎯 Canonical Documentation
**Official source of truth** - Always check these first:
- **[INDEX.md](canon/INDEX.md)** - Master navigation
- **[SYSTEM_OVERVIEW.md](canon/SYSTEM_OVERVIEW.md)** - Complete architecture
- **[DATABASE_SCHEMA.md](canon/DATABASE_SCHEMA.md)** - Database structure
- **[STUDENT_LMS.md](canon/STUDENT_LMS.md)** - Student onboarding app
- **[TEAM_LEAD_MODULE_BUILDER.md](canon/TEAM_LEAD_MODULE_BUILDER.md)** - Team lead tools
- **[RESEARCHER_PLATFORM.md](canon/RESEARCHER_PLATFORM.md)** - Research analytics
- **[AGENT_SYSTEM_OVERVIEW.md](canon/AGENT_SYSTEM_OVERVIEW.md)** - AI agent protocols

[See all 14 canonical docs →](canon/)

### 📂 Active Documentation
- **[Agent Operations](docs/agents/)** - Agent wake-up prompts, coordination
- **[Notion Integration](docs/notion/)** - Workspace setup, API guides
- **[CADENCE Modules](docs/cadence/)** - Module extraction, hub setup
- **[Quick Start Guides](docs/guides/)** - Development workflows

### 🗺️ Finding Documentation
- **Lost a file?** Check [MIGRATION_MAP.md](MIGRATION_MAP.md)
- **Historical docs?** See [archive/](archive/)
- **Repository structure?** See [MONOREPO_STRUCTURE.md](MONOREPO_STRUCTURE.md)

---

## 🌟 Key Features

- **Mobile-first student training** - Progressive web app with offline support
- **AI-assisted module creation** - Three autonomous agents building content
- **Multi-university analytics** - NDA diagnostics across 8 institutions
- **Race mode learning** - Competitive training with ghost cohorts
- **Progress tracking** - Time + scroll analytics
- **Notion integration** - 68 modules imported from CADENCE knowledge base

---

## 🛠️ Technology Stack

- **Backend:** Flask, SQLAlchemy, PostgreSQL (Neon)
- **Frontend:** React (PWA), Chart.js
- **AI:** Anthropic Claude API (three autonomous agents)
- **Integration:** Notion API, react-notion-x
- **ML (Planned):** MLflow, NetworkX, Scikit-learn

---

## 📊 Current Status

### ✅ Completed
- [x] Multi-university database schema (37 tables)
- [x] Research analytics backend (NDA diagnostics, interfaces)
- [x] Comparative dashboard
- [x] Student/team/faculty management
- [x] Custom risk factor modeling
- [x] Three-agent autonomous development system
- [x] Canonical documentation system
- [x] Notion workspace integration

### 🚧 In Progress
- [ ] **Student Onboarding LMS** (Active Development)
  - [x] 11+ training modules created
  - [x] 8 LMS API endpoints
  - [x] React scaffolding (Dashboard, ModulePlayer)
  - [ ] Team lead AI assistant
  - [ ] Module analytics dashboard
  - [ ] Race mode & competency tracking

### 📅 Planned
- [ ] React research analytics frontend
- [ ] AI prediction core development
- [ ] Multi-language support
- [ ] Mobile native apps

---

## 🎓 Research Background

FRAMES uses **Non-Decomposable Architecture (NDA)** theory to analyze space mission programs with molecular modeling metaphors:

- **Molecules (nodes)** = Teams, Faculty, Projects
- **Bonds (edges)** = Interfaces between entities
- **Energy Loss** = Knowledge transfer friction (0-100 scale)

**Lead Institution:** California State Polytechnic University, Pomona  
**Partner Universities:** 8 universities collaborating on space missions

---

## 📞 Contact

**Principal Investigator:** Elizabeth Osborn, Ph.D.  
**Email:** eosborn@cpp.edu  
**Institution:** Cal Poly Pomona

---

<div align="center">

**[📖 Canon Docs](canon/)** • **[🗺️ Migration Map](MIGRATION_MAP.md)** • **[🏗️ Monorepo Structure](MONOREPO_STRUCTURE.md)** • **[🤖 Agent System](canon/AGENT_SYSTEM_OVERVIEW.md)**

Built for space mission research and student success 🚀

</div>
