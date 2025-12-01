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

## Open Source Philosophy

**Who:**  
Students, researchers, educators, engineering programs, and collaborators who benefit from shared tools and transparent systems.

**What:**  
FRAMES and Ascent Basecamp are developed as open-source, research-aligned tools. The architecture, documentation, and core methods are intentionally public so others can learn from, build on, or adapt the work.

**Why:**  
Complex engineering programs improve when knowledge is shared, not siloed. Making the system open-source supports academic collaboration, accelerates innovation, and ensures that students and faculty at any institution can benefit from consistent, reliable tools.

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
A systems-diagnostic and analytics environment that examines engagement patterns, team interfaces, and structural fragility using NDA principles. This is a real, data-driven research platform—not just theory—providing system-wide analytics, predictive indicators of mission resilience, and longitudinal datasets across multiple cohorts and universities.

**Why it exists:**
To give researchers visibility into where learning breaks down, how knowledge flows through programs, and how multi-university engineering systems can be strengthened over time. Traditional approaches fail to capture invisible patterns of team decomposition, knowledge decay, and structural friction—FRAMES makes these measurable.

📄 **Learn more** → [Full research platform details below](#-for-researchers--study-the-data) • [`docs/FOR_RESEARCHERS.md`](docs/FOR_RESEARCHERS.md) • [`docs/FOR_RESEARCH_PLATFORM.md`](docs/FOR_RESEARCH_PLATFORM.md)

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

### 👨‍💻 For Developers & Engineering Teams

> **You want to:** Run the system locally, understand the architecture, contribute code, or deploy your own instance.

**→ [Complete Developer Guide](docs/FOR_DEVELOPERS.md)** ← Full technical details, API reference, deployment instructions
**→ [Engineering Teams Platform](docs/FOR_ENGINEERING_TEAMS.md)** ← Integration layer, workflow automation, team continuity

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

**What's in the guide:** Technical stack • Database schema (37 tables) • API endpoints • Testing • Deployment

---

### 🔬 For Researchers — Study the Data

<div align="center">

**Systems Researchers • Education Researchers • Organizational Scientists • Faculty**

</div>

> **A systems-diagnostic and analytics environment for studying continuity, turnover, and resilience in modular organizations.**

**→ [Complete Research Guide](docs/FOR_RESEARCHERS.md)** ← Full NDA theory, analytics workflows, Python/SQL examples
**→ [Research Platform Overview](docs/FOR_RESEARCH_PLATFORM.md)** ← Quick start, integration layer, structural metrics

**What you get:**

- ✅ **System-wide analytics** from real engineering programs (not synthetic data)
- ✅ **NDA-based structural mapping** — identify fragile interfaces before they break
- ✅ **Continuously updating database** — team behavior, knowledge flow, turnover patterns
- ✅ **AI-assisted data extraction** — convert messy workflows into analyzable datasets
- ✅ **Predictive indicators** — forecast mission resilience and program stability
- ✅ **Longitudinal datasets** — compare cohorts across semesters and universities

#### 📐 Architecture (Research Layer)

```
                    ┌──────────────────────────────┐
                    │            FRAMES             │
                    │  NDA-Based Diagnostic Model   │
                    └───────────────┬──────────────┘
                                    │ Metrics + Features
                      ┌─────────────┴─────────────┐
                      │  Researcher Analytics API │
                      └─────────────┬─────────────┘
                                    │
                   ┌────────────────┴────────────────┐
                   │                                  │
         Structural Metrics                   Program Continuity
        (interfaces, fragility)             (knowledge retention)
```

#### 🧪 Research Questions You Can Answer

<details>
<summary><b>📊 Structural Questions</b></summary>

- What subsystem interfaces are most fragile?
- Where does knowledge consistently disappear?
- How many handoffs occur before information decays?
- Which team structures predict project failure?

</details>

<details>
<summary><b>👥 Behavioral/Engagement Questions</b></summary>

- How long does it take new members to become productive?
- Which modules correlate with team performance?
- What learning patterns predict student success?
- Where do students struggle in technical onboarding?

</details>

<details>
<summary><b>🔮 Predictive Questions</b></summary>

- Can we forecast structural failure using NDA indicators?
- Which factors correlate with mission success or long-term stability?
- How effective are different pedagogical approaches?
- What turnover levels trigger program instability?

</details>

#### 📊 Example Research Workflow

```python
from frames_api import FRAMESClient

client = FRAMESClient(api_key="YOUR_KEY")

# Pull structural metrics for a team over 4 semesters
metrics = client.get_structure_profile(team_id="eps", semesters=4)

# Visualize fragility score over time
metrics.plot("interface_fragility")
```

#### 📚 What You Can Query

**Structural Data:** Decomposition maps • Continuity indices • Interface fragility scores
**Behavioral Data:** Module engagement logs • Onboarding performance • Time-on-task analytics
**Multi-University:** Cross-institutional comparisons • Subsystem turnover • Collaboration metrics

#### 🚀 Getting Started

```bash
pip install frames-research-tools
```

Generate an API key, query structural data, and use built-in visualization tools.

**Full documentation:** [Research Platform Guide](docs/FOR_RESEARCHERS.md) • [Platform Overview](docs/FOR_RESEARCH_PLATFORM.md)

---

### 📚 For Students — Learn Technical Skills

> **You want to:** Complete onboarding modules, learn mission-critical skills, and track your progress.

**→ [Complete Student Guide](docs/FOR_STUDENTS.md)** ← How the learning platform works, mobile access, race mode
**→ [Student Platform Overview](docs/FOR_STUDENT_PLATFORM.md)** ← Quick start, module generation, workflow-based learning

**What you'll learn:**
- **Power:** Battery sizing, EPS characterization, solar panel testing
- **Avionics:** Firmware flashing, sensor integration, telemetry debugging
- **Structures:** CAD modeling, 3D printing, vibration testing
- **Thermal, Communications, Payload:** Mission-specific technical skills

**What's in the guide:** Module structure • Progress tracking • Race mode (competitive learning) • Mobile PWA access

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
