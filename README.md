<div align="center">

# 🛰️ FRAMES

### A Human–AI Collaboration Framework for Real Engineering Work

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![React 18+](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Neon](https://img.shields.io/badge/Neon-Serverless-00E599?style=for-the-badge&logo=neon&logoColor=white)](https://neon.tech)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**Educational Research** · **Systems Theory** · **AI Architecture** · **Engineering Pedagogy**

[📖 Documentation](#-documentation-overview) · [🚀 Quick Start](#-quick-start) · [🤝 Contributing](#-contributing) · [📬 Contact](#-contact)

---

<img src="https://img.shields.io/badge/Status-Active_Development-brightgreen?style=flat-square" alt="Status"/>
<img src="https://img.shields.io/badge/Universities-8_Partners-blue?style=flat-square" alt="Universities"/>
<img src="https://img.shields.io/badge/Database-37+_Tables-orange?style=flat-square" alt="Database"/>
<img src="https://img.shields.io/badge/Agents-3_Controlled-purple?style=flat-square" alt="Agents"/>

</div>

---

## 🔍 What Is FRAMES?

FRAMES is a **research-driven ecosystem** that transforms real engineering work—especially in university CubeSat and aerospace programs—into structured learning, organizational insight, and research-grade data.

It captures how students and teams **actually think, collaborate, and solve problems**, then turns those real-world practices into:

| 🎓 | **Onboarding modules** for new engineers |
|:--:|:--|
| 📊 | **Analytics** for researchers studying collaboration |
| 🔗 | **Insights** into organizational resilience and knowledge transfer |
| 📈 | **Datasets** for understanding decision-making patterns |
| 🤖 | **Demonstrations** of multi-agent AI working safely with humans |

> FRAMES sits at the intersection of **engineering education**, **organizational theory**, and **AI**.
> It's designed to help humans learn, teams coordinate, and researchers see patterns that are normally invisible.

<details>
<summary><b>🔬 Layer 2 — Technical Deep Dive</b></summary>

<br>

FRAMES consists of **five major components**:

### 1️⃣ Canonical Data Layer
A **Neon-hosted PostgreSQL database** storing modules, analytics, team structures, research metrics, agent logs, and Notion sync metadata.

### 2️⃣ Real Work Layer  
Team Leads work inside a dedicated **Notion workspace** where they document real missions. This data becomes the raw material for module extraction.

### 3️⃣ AI Interpretation Layer
Three tightly controlled agents (**Alpha**, **Beta**, **Gamma**) perform:
- Content extraction & structural validation
- OATutor framing for educational scaffolding
- Safe transformation of Notion content
- Analytics, sync, and logging operations

### 4️⃣ Application Layer
| Application | Purpose |
|------------|---------|
| **Student LMS** | React PWA for structured learning |
| **Team Lead Workspace** | Notion-based documentation |
| **Researcher Platform** | Jupyter + Superset + MLflow |

### 5️⃣ Governance Layer
Safety rules, agent logs, versioning policies, and canonical documents controlling system-wide behavior.

<br>

**📚 Architecture References:**
- [`canon/system_overview_v_2.md`](canon/system_overview_v_2.md)
- [`canon/DATABASE_SCHEMA.md`](canon/DATABASE_SCHEMA.md)
- [`canon/agent_interaction_script_v_2.md`](canon/agent_interaction_script_v_2.md)

</details>

---

## 🌍 Why FRAMES Exists

University engineering programs—especially space labs—struggle with:

<table>
<tr>
<td width="50%">

❌ **Uneven student preparation**

❌ **Massive knowledge loss every semester**

❌ **Unclear institutional classification**
<br><sub>(not quite classes, not quite labs, not quite research centers)</sub>

</td>
<td width="50%">

❌ **Steep learning curves for new students**

❌ **Fragile continuity between cohorts**

❌ **Repeated reinvention of processes**

</td>
</tr>
</table>

> **These aren't failures of individuals. They are structural problems.**

FRAMES helps programs:
- ✅ **Retain knowledge** across cohorts
- ✅ **Coordinate** effectively across teams  
- ✅ **Onboard** new students efficiently
- ✅ **Understand** where systems are strong or fragile

It also acts as a **research instrument** for studying:

```
📐 How multidisciplinary teams collaborate
⏳ How expertise transfers across time  
🏗️ How organizational resilience emerges
🤖 How AI can assist (not replace) complex human work
```

<details>
<summary><b>🔬 Layer 2 — Theory & Formal Framework</b></summary>

<br>

FRAMES draws from several theoretical foundations:

### 📘 Nearly Decomposable Architecture *(Herbert Simon)*
Real organizations behave as semi-independent modules linked by fragile interfaces. FRAMES models those interfaces and their failure points.

### 📗 Hybrid Autonomous Organizations *(Champenois & Etzkowitz)*
University space labs operate in boundary spaces where institutional categories break down. Students form semi-autonomous organizations managing multi-year missions.

### 📙 Learning Science & OATutor Pedagogy
Engineering onboarding redesigned using:
- Scaffolding & hint pathways
- Validation steps & adaptive sequencing
- Evidence-based learning design

*Reference: [`canon/module_definition_v_2.md`](canon/module_definition_v_2.md)*

### 📕 Knowledge Transfer & Organizational Resilience
FRAMES identifies where knowledge is **codified**, where it is **tacit**, and where interfaces degrade over time.

</details>

---

## 🏛️ System Architecture

<div align="center">

```
┌─────────────────────────────────────────────────────────────────────┐
│                        🌐 REAL WORK LAYER                           │
│              Team Leads document missions in Notion                  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🤖 AI INTERPRETATION LAYER                        │
│         Alpha · Beta · Gamma agents (safe, controlled)              │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    💾 CANONICAL DATA LAYER                           │
│                 Neon PostgreSQL · 37+ Tables                         │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌─────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│  📱 Student LMS  │   │  📋 Team Lead Tools  │   │  📊 Research Platform │
│   React PWA     │   │   Notion Workspace  │   │  Jupyter + MLflow   │
└─────────────────┘   └─────────────────────┘   └─────────────────────┘
```

</div>

**One system. Three applications. Shared data. Human-centered design.**

| Step | What Happens |
|:----:|:-------------|
| 1️⃣ | **Team Leads work in Notion** — documenting real engineering work, decisions, lessons learned |
| 2️⃣ | **Agents interpret and structure** — extracting concepts, building modules, maintaining consistency |
| 3️⃣ | **Modules stored in database** — becoming the single source of truth |
| 4️⃣ | **Students learn via mobile LMS** — with scaffolding, hints, and real engineering context |
| 5️⃣ | **Researchers analyze patterns** — studying knowledge transfer and team resilience |

<details>
<summary><b>🔬 Layer 2 — Full Technical Architecture</b></summary>

<br>

### Applications

| App | Stack | Purpose |
|-----|-------|---------|
| **Student LMS** | React PWA | Structured modules with OATutor scaffolding |
| **Team Lead Workspace** | Notion | Source of truth for mission documentation |
| **Researcher Platform** | Jupyter + MLflow + Superset | Analytics and predictive modeling |

### Infrastructure

| Component | Technology |
|-----------|------------|
| Database | PostgreSQL 15+ (Neon serverless) |
| Backend | Flask 3.0 / FastAPI |
| Sync | Bidirectional Notion integration |
| Frontend | React 18+ with TypeScript |

### Agent Roles

| Agent | Responsibility |
|-------|---------------|
| **Alpha** | Module extraction + OATutor structuring |
| **Beta** | LMS development + frontend/backend integration |
| **Gamma** | Infrastructure, sync, logging, migrations |

### Database Schema Highlights

```sql
-- Core tables include:
modules              -- Learning content structure
module_sections      -- OATutor-style steps & hints  
module_progress      -- Student completion tracking
analytics_events     -- Behavioral data capture
teams / students     -- Organizational structure
interfaces           -- Knowledge transfer points
agent_logs           -- AI operation audit trail
```

**📚 References:**
- [`canon/DATABASE_SCHEMA.md`](canon/DATABASE_SCHEMA.md)
- [`canon/STUDENT_LMS.md`](canon/STUDENT_LMS.md)
- [`canon/RESEARCHER_PLATFORM.md`](canon/RESEARCHER_PLATFORM.md)

</details>

---

## 👥 Who This Project Is For

<table>
<tr>
<td align="center" width="20%">
<img src="https://img.shields.io/badge/-Students-4CAF50?style=for-the-badge" alt="Students"/>
<br><sub>Learning real<br>engineering practices</sub>
</td>
<td align="center" width="20%">
<img src="https://img.shields.io/badge/-Team_Leads-2196F3?style=for-the-badge" alt="Team Leads"/>
<br><sub>Stop re-teaching<br>every semester</sub>
</td>
<td align="center" width="20%">
<img src="https://img.shields.io/badge/-Faculty-9C27B0?style=for-the-badge" alt="Faculty"/>
<br><sub>Visibility into<br>program health</sub>
</td>
<td align="center" width="20%">
<img src="https://img.shields.io/badge/-Researchers-FF9800?style=for-the-badge" alt="Researchers"/>
<br><sub>Study collaboration<br>& resilience</sub>
</td>
<td align="center" width="20%">
<img src="https://img.shields.io/badge/-Developers-607D8B?style=for-the-badge" alt="Developers"/>
<br><sub>Multi-agent systems<br>& EdTech</sub>
</td>
</tr>
</table>

> Everyone interacts with the same system, but through different doors.

<details>
<summary><b>🔬 Layer 2 — Technical Persona Mapping</b></summary>

<br>

| Persona | Primary Interface | Primary Data | Key Needs |
|---------|------------------|--------------|-----------|
| **Students** | LMS (React PWA) | Module sections, hints, validation | Progress tracking, scaffolding |
| **Mentors** | Notion | Team docs, assignments | Visibility into student progress |
| **Researchers** | Research Platform | Analytics tables, structural metrics | Reproducible datasets |
| **Developers** | Repo + DB schema | APIs, agents | Stable infra, deterministic interfaces |
| **Agents** | Notion + DB + filesystem | Structured docs | Safety, consistency, logs |

</details>

---

## 📚 Documentation Overview

### Choose Your Path

<table>
<tr>
<td width="50%">

#### 🎓 For Learners & Users
| Guide | Description |
|-------|-------------|
| [📖 Overview](canon/INDEX.md) | What FRAMES is |
| [🧠 Theory](canon/OPERATIONAL_ONTOLOGY.md) | Why the system works this way |
| [📱 Student LMS](canon/STUDENT_LMS.md) | How students use modules |
| [🤖 AI Agents](canon/agent_interaction_script_v_2.md) | How agents work safely |

</td>
<td width="50%">

#### 💻 For Developers & Researchers
| Guide | Description |
|-------|-------------|
| [🏗️ Architecture](canon/system_overview_v_2.md) | Full system design |
| [🗄️ Database](canon/DATABASE_SCHEMA.md) | Schema reference |
| [📊 Research](canon/RESEARCHER_PLATFORM.md) | Analytics platform |
| [⚙️ Development](docs/FOR_DEVELOPERS.md) | Setup & contribution |

</td>
</tr>
</table>

<details>
<summary><b>🔬 Layer 2 — Complete Document Map</b></summary>

<br>

**📁 Canonical Documents (`/canon/`)**

| Document | Purpose |
|----------|---------|
| `INDEX.md` | Master navigation |
| `system_overview_v_2.md` | Complete architecture |
| `OPERATIONAL_ONTOLOGY.md` | Core conceptual model |
| `Notion_Interface_layer.md` | Notion integration rules |
| `agent_interaction_script_v_2.md` | Agent coordination protocols |
| `module_definition_v_2.md` | Module structure spec |
| `canonical_refresh_policy.md` | Agent refresh requirements |
| `DATABASE_SCHEMA.md` | Database structure |
| `FILE_STRUCTURE_AND_STANDARDS.md` | File organization |
| `STUDENT_LMS.md` | Student application spec |
| `RESEARCHER_PLATFORM.md` | Research platform spec |

</details>

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required
Python 3.9+
Node.js 18+
PostgreSQL 15+ (or Neon account)
```

### Installation

```bash
# Clone the repository
git clone https://github.com/Lizo-RoadTown/FRAMES-Python.git
cd FRAMES-Python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your DATABASE_URL (Neon PostgreSQL connection string)

# Start the backend
python backend/app.py
```

### Verify Installation

```bash
# Test database connection
python shared/database/test_db_connection.py

# Run endpoint tests
python backend/test_endpoints.py
```

<details>
<summary><b>🔬 Layer 2 — Advanced Setup</b></summary>

<br>

### Frontend Development

```bash
cd apps/onboarding-lms/frontend-react
npm install
npm run dev
```

### Database Operations

```bash
# Initialize/update tables
python shared/database/bootstrap_db.py

# Check current data
python check_neon_data.py

# Seed sample data
python backend/seed_multi_university.py
```

### Running Tests

```bash
# Full test suite
pytest backend/test_lms_endpoints.py -v

# Quick API validation
python backend/test_lms_quick.py
```

**📚 Full Guide:** [`docs/FOR_DEVELOPERS.md`](docs/FOR_DEVELOPERS.md)

</details>

---

## 🛣️ Roadmap

<table>
<tr>
<th>🎯 High-Level Goals</th>
<th>⚙️ Technical Tasks</th>
</tr>
<tr>
<td valign="top">

- [ ] Expand module library
- [ ] Enhance researcher analytics
- [ ] Improve LMS user experience
- [ ] Add simulation-based modules
- [ ] Publish FRAMES research datasets

</td>
<td valign="top">

- [ ] Strengthen Notion ↔ DB sync
- [ ] Add ghost cohort analytics
- [ ] Build adaptive hint sequencing
- [ ] Expand agent logging
- [ ] Refine ontology versioning

</td>
</tr>
</table>

---

## 🤝 Contributing

Contributions welcome from **students**, **educators**, **researchers**, and **developers**!

<table>
<tr>
<td align="center" width="33%">

### 🐛 Report Issues
Found a bug?<br>
[Open an Issue](https://github.com/Lizo-RoadTown/FRAMES-Python/issues)

</td>
<td align="center" width="33%">

### 💡 Suggest Features
Have an idea?<br>
[Start a Discussion](https://github.com/Lizo-RoadTown/FRAMES-Python/discussions)

</td>
<td align="center" width="33%">

### 🔧 Submit Code
Ready to contribute?<br>
[Read the Guide](docs/FOR_DEVELOPERS.md)

</td>
</tr>
</table>

<details>
<summary><b>🔬 Layer 2 — Contribution Guidelines</b></summary>

<br>

See `/docs/FOR_DEVELOPERS.md` for:
- API specifications
- Coding standards
- Architecture diagrams  
- Testing protocols
- PR requirements

**Key Files for Contributors:**
- [`canon/FILE_STRUCTURE_AND_STANDARDS.md`](canon/FILE_STRUCTURE_AND_STANDARDS.md)
- [`canon/agent_interaction_script_v_2.md`](canon/agent_interaction_script_v_2.md)

</details>

---

## 📬 Contact

<table>
<tr>
<td>

**Project Lead & Research Developer**

**Elizabeth Osborn**  
📧 eosborn@cpp.edu  
🏫 Cal Poly Pomona

</td>
<td>

**Partner Universities**

🎓 **Cal Poly Pomona** (Lead Institution)  
🎓 Columbia · Texas State · Mt. San Antonio College  
🎓 Virginia Tech · Washington State  
🎓 University of Illinois · Northeastern

</td>
</tr>
</table>

---

<div align="center">

### 📖 Quick Links

[**Canonical Docs**](canon/) · [**Migration Map**](MIGRATION_MAP.md) · [**Agent System**](canon/agent_interaction_script_v_2.md) · [**Theoretical Ontology**](THEORETICAL_ONTOLOGY.md)

---

<sub>Built with ❤️ for engineering education and organizational research</sub>

<sub>© 2025 FRAMES Project · MIT License</sub>

</div>
