# FRAMES / Ascent Basecamp

*A unified system to support student learning, team continuity, and research on complex engineering programs.*

---

## 🌱 What FRAMES Is

FRAMES (Framework for Resilience Assessment in Modular Engineering Systems) is a connected ecosystem designed to help multi-university engineering programs run more smoothly.

It brings together three groups — **students**, **team leads**, and **researchers** — into one shared data environment, so learning, mentoring, and program analysis all support each other rather than existing in isolated silos.

---

## 💡 Why FRAMES Exists

Engineering programs — especially multi-university ones — face predictable, recurring challenges:

- Students join with uneven preparation
- Knowledge lives in scattered documents, chats, and memories
- Teams rely heavily on verbal explanations
- When seniors graduate, essential information leaves with them
- Faculty have limited visibility into what students actually understand
- Mentors lose time reteaching the same fundamentals every semester

FRAMES addresses these pressure points by making **learning clear**, **progress visible**, and **program memory persistent**.

It doesn't replace human instruction —  
it reinforces it by making foundational knowledge consistent across semesters and campuses.

---

## 🧩 The Three Applications

All three applications connect to one shared PostgreSQL database, ensuring continuity and reducing duplication.

### 1. Student Onboarding LMS

- Mobile-first React PWA
- Structured modules
- Time + scroll analytics
- Adaptive learning paths based on team needs

📄 **Learn more** → [`canon/STUDENT_LMS.md`](canon/STUDENT_LMS.md)

### 2. Team Lead Module Builder

- Create structured modules
- Import and refine content from Notion
- Standardize onboarding
- Reduce repetitive mentoring load

📄 **Learn more** → [`canon/TEAM_LEAD_MODULE_BUILDER.md`](canon/TEAM_LEAD_MODULE_BUILDER.md)

### 3. Researcher & Faculty Platform

- Cross-university analytics dashboards
- Longitudinal learning & collaboration patterns
- NDA-based interface modeling
- Tools for program resilience research

📄 **Learn more** → [`canon/RESEARCHER_PLATFORM.md`](canon/RESEARCHER_PLATFORM.md)

---

## 🧭 How It Works (High-Level)

Everything runs from a single **Neon-hosted PostgreSQL database**.

```
┌───────────────────────────────────┐
│          PostgreSQL (Neon)        │
│     Shared by all applications    │
└───────────┬───────────┬───────────┘
            │           │
    ┌───────▼──────┐  ┌─▼───────────┐
    │ Student LMS   │  │ Module      │
    │ (React PWA)   │  │ Builder     │
    └───────────────┘  └─────────────┘
            │
    ┌───────▼────────────┐
    │ Researcher Tools    │
    │ & Analytics         │
    └─────────────────────┘
```

A carefully controlled **AI agent layer** assists with formatting, documentation upkeep, and structured updates — operating inside strict guardrails.

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

---

## 🚀 Getting Started (Development)

```bash
# Clone repository
git clone https://github.com/Lizo-RoadTown/FRAMES-Python.git
cd FRAMES-Python

# Python environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure database
cp .env.example .env
# Add your Neon PostgreSQL connection string

# Run backend
python backend/app.py
```

Frontend setup instructions are in:  
`/student-lms/README.md` and `/module-builder/README.md`

---

---

## 🧭 Who FRAMES Serves

**Students**  
Clear, structured pathways that reduce confusion and make it easier to join complex engineering teams.

**Mentors / Team Leads**  
Less repetitive teaching, more time for real engineering.

**Faculty**  
Visibility into engagement, gaps, and onboarding effectiveness.

**Researchers**  
Clean datasets for studying collaboration, learning, and long-term program resilience.

---

## 🌍 Universities Involved

FRAMES works in partnership with:

- **Bronco Space & Bronco Star** at California State Polytechnic University, Pomona *(Lead Institution)*
- 8 collaborating universities participating in joint space mission programs

---

---

## 📞 Contact

**Project Lead & Research Developer:** Elizabeth Osborn  
📧 eosborn@cpp.edu

*Cal Poly Pomona*

---

<div align="center">

**[📖 Canonical Docs](canon/)** • **[🗺️ Migration Map](MIGRATION_MAP.md)** • **[🧠 Philosophy](canon/FRAMES_PHILOSOPHY.md)**

</div>
