# For Developers — Getting Started with FRAMES/Ascent Basecamp

**Target Audience:** Software engineers, system architects, developers who want to run, modify, or contribute to the codebase.

---

## What You're Looking At

FRAMES/Ascent Basecamp is a **full-stack learning management and research platform** designed for multi-university engineering programs. Think of it as:

- **A learning platform** (like Canvas or Moodle) but built specifically for hands-on engineering training
- **A research tool** for studying how knowledge moves through complex teams
- **A content management system** that preserves institutional knowledge across student generations

The entire system runs on **one shared PostgreSQL database** with three front-end applications serving different user groups.

---

## Technical Stack Overview

### Backend
- **Python 3.9+** with Flask (REST API)
- **PostgreSQL 15+** (Neon-hosted, 37+ tables)
- **SQLAlchemy** for ORM
- **Notion API** for content integration

### Frontend
- **React 18+** (Progressive Web App)
- **Tailwind CSS** for styling
- **Axios** for API calls
- **React Router** for navigation

### Infrastructure
- **Neon PostgreSQL** (serverless, branching databases)
- **GitHub** for version control
- **3 autonomous AI agents** for content/platform/infrastructure work (strictly controlled)

### Development Tools
- **pytest** for backend testing
- **Jest/React Testing Library** for frontend testing
- **MLflow** for ML experiment tracking (research features)

---

## System Architecture (The Real Picture)

```
┌─────────────────────────────────────────────────────────────────────┐
│                     FRAMES Research Layer                            │
│  - Non-Decomposable Architecture (NDA) modeling                     │
│  - Team interface analysis                                           │
│  - Knowledge transfer predictions                                    │
│  - Cross-university comparison metrics                               │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                  ┌────────▼────────┐
                  │  PostgreSQL DB  │  ← Single source of truth
                  │  (Neon-hosted)  │     37 tables, 1 schema
                  └────────┬────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼─────┐    ┌──────▼──────┐   ┌─────▼──────┐
    │ Student  │    │ Team Lead   │   │ Researcher │
    │   LMS    │    │   Builder   │   │  Platform  │
    └──────────┘    └─────────────┘   └────────────┘
    React PWA       React Dashboard    Jupyter + ML
    (Mobile-first)  (Module authoring) (Analytics)
```

**Key insight:** All three apps read/write to the same database. Changes in one app are immediately visible in others.

---

## Repository Structure

```
FRAMES-Python/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── lms_routes.py       # LMS API endpoints (8 core routes)
│   ├── analytics.py        # Research analytics endpoints
│   ├── models.py           # SQLAlchemy ORM models
│   └── database.py         # Database connection utilities
│
├── frontend-react/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx      # Student module browser
│   │   │   └── ModulePlayer.jsx   # Interactive module viewer
│   │   ├── api/
│   │   │   └── lms.js             # API client with all endpoints
│   │   └── hooks/
│   │       └── useModulePlayer.js # Module state management
│   └── package.json
│
├── modules/
│   └── enhanced/           # 68 module JSON files (OATutor format)
│
├── scripts/
│   ├── notion_continuous_sync.py  # Notion ↔ Database sync
│   └── create_ascent_basecamp_schema.py
│
├── canon/                  # 14 authoritative documentation files
│   ├── SYSTEM_OVERVIEW.md
│   ├── DATABASE_SCHEMA.md
│   ├── STUDENT_LMS.md
│   └── ... (11 more)
│
└── docs/
    ├── onboarding-lms/     # LMS technical specs
    ├── research-analytics/ # Analytics architecture
    └── shared/             # Database setup guides
```

---

## Database Schema (What You Need to Know)

The database has **37 tables** organized into logical groups:

### Core Tables (Students, Teams, Faculty)
- `students`, `teams`, `faculty`, `universities`
- Standard user/org management

### Learning Management System (LMS)
- `modules` — Learning modules (69 existing, JSON schema-based)
- `module_sections` — Individual steps within modules
- `module_progress` — Student completion tracking
- `learner_performance` — Time-on-task analytics, mastery scoring
- `subsystem_competency` — Progress through subsystems (Power, Avionics, etc.)
- `ghost_cohorts` — Historical benchmark data for "race mode"
- `race_metadata` — Competitive learning features

### Research/Analytics
- `cadence_people`, `cadence_projects`, `cadence_tasks`, `cadence_meetings`
- Historical team data from CADENCE CubeSat program (1,416+ records)
- Used for NDA modeling and knowledge transfer analysis

### Agent Coordination (Development)
- `ascent_basecamp_agent_log` — Real-time agent status
- `technical_decisions` — Architecture decision log
- `error_log` — Agent error tracking

**Full schema:** See [`docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md`](ASCENT_BASECAMP_DATABASE_SCHEMA.md)

---

## Quick Start (Local Development)

### Prerequisites
- Python 3.9+
- Node.js 16+ (for React frontend)
- PostgreSQL access (we use Neon, but local Postgres works too)
- Git

### 1. Clone and Setup Backend

```bash
git clone https://github.com/Lizo-RoadTown/FRAMES-Python.git
cd FRAMES-Python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database
cp .env.example .env
# Edit .env and add your DATABASE_URL (Neon connection string)
```

### 2. Run Backend

```bash
python backend/app.py
# Backend runs on http://localhost:5000
```

**Test API:**
```bash
curl http://localhost:5000/api/modules
```

### 3. Setup Frontend

```bash
cd frontend-react
npm install

# Configure API endpoint
echo "REACT_APP_API_URL=http://localhost:5000" > .env

# Start development server
npm start
# Frontend runs on http://localhost:3000
```

---

## Key API Endpoints (What the Frontend Uses)

### Student Learning Flow
```
POST   /students/{id}/modules/{module_id}/start
       → Log when student starts a module

POST   /students/{id}/modules/{module_id}/log_activity
       → Track time spent, progress through sections

POST   /students/{id}/modules/{module_id}/complete
       → Mark module complete, update competency levels

GET    /students/{id}/subsystem_competency
       → Get student's progress through subsystems
```

### Module Data
```
GET    /modules/{id}
       → Fetch module content (sections, checks, quizzes)

GET    /modules/{id}/ghost_cohorts
       → Get historical benchmark data for race mode
```

### Competition Features
```
POST   /students/{id}/race/start
       → Start timed race mode against historical cohorts

POST   /students/{id}/race/complete
       → Submit race results, calculate ranking

GET    /students/{id}/leaderboard
       → Get student's ranking vs peers and ghost cohorts
```

**Full API docs:** [`docs/lms/API_REFERENCE.md`](lms/API_REFERENCE.md)

---

## Module Format (JSON Schema)

Modules use an **OATutor-compatible JSON structure** for adaptive learning:

```json
{
  "id": "avionics_firmware_001",
  "title": "Firmware Flashing Fundamentals",
  "subsystem": "avionics",
  "difficulty": "beginner",
  "estimated_minutes": 75,
  "learning_objectives": [
    "Understand firmware vs software",
    "Flash firmware to development board",
    "Troubleshoot common flashing errors"
  ],
  "steps": [
    {
      "step_id": "intro",
      "title": "What is Firmware?",
      "content_type": "reading",
      "content": "Markdown text here...",
      "hints": ["Optional scaffolding hints"],
      "checks": [
        {
          "check_id": "check_1",
          "validation": "Student confirms understanding",
          "success_message": "Great!",
          "error_message": "Review the section again",
          "hint": "Think about bootloaders..."
        }
      ]
    },
    {
      "step_id": "hands_on",
      "title": "Flash Your First Board",
      "content_type": "exercise",
      "content": "Step-by-step instructions...",
      "checks": [...]
    }
  ],
  "prerequisites": ["avionics_orientation_001"],
  "race_metadata": {
    "enabled": true,
    "checkpoints": [{"step_id": "intro", "target_seconds": 300}],
    "ghost_data": [...]
  }
}
```

**Why this format?**
- **Adaptive:** Hints and checks enable scaffolded learning
- **Measurable:** Time-on-task data for every step
- **Competitive:** Ghost cohorts enable friendly competition
- **Reusable:** Same format across all subsystems

---

## Testing

### Backend Tests
```bash
# Install test dependencies
pip install pytest

# Run all tests
pytest backend/test_lms_endpoints.py

# Run with coverage
pytest --cov=backend backend/
```

### Frontend Tests
```bash
cd frontend-react
npm test
```

---

## Development Workflow

### Making Changes to LMS Features

1. **Backend changes** → `backend/lms_routes.py`
2. **Add tests** → `backend/test_lms_endpoints.py`
3. **Update API docs** → `docs/lms/API_REFERENCE.md`
4. **Frontend integration** → `frontend-react/src/api/lms.js`
5. **Test end-to-end** → Manual testing in browser

### Creating New Modules

1. Use existing module JSON as template (`modules/enhanced/*.json`)
2. Follow schema in `canon/STUDENT_LMS.md`
3. Validate learning objectives match subsystem competencies
4. Add prerequisite chains
5. Test in ModulePlayer component

### Database Changes

1. **Never modify production schema directly**
2. Create migration script in `scripts/`
3. Test on local database first
4. Document in `docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md`
5. Coordinate with Agent Gamma (if using agent system)

---

## Agent System (Optional — Advanced)

FRAMES uses **3 autonomous AI agents** for parallel development:

- **Agent Alpha:** Module content creation
- **Agent Beta:** Platform/frontend development
- **Agent Gamma:** Infrastructure and database work

**Key rules:**
- Agents coordinate via database tables (`ascent_basecamp_agent_log`)
- Agents CANNOT create Notion pages without approval
- Agents work asynchronously, log all actions
- Human oversight required for architecture changes

**See:** [`canon/AGENT_SYSTEM_OVERVIEW.md`](../canon/AGENT_SYSTEM_OVERVIEW.md)

---

## Common Development Tasks

### Add a new LMS endpoint
1. Define route in `backend/lms_routes.py`
2. Add database queries (use SQLAlchemy)
3. Write test in `backend/test_lms_endpoints.py`
4. Document in `docs/lms/API_REFERENCE.md`
5. Add frontend wrapper in `frontend-react/src/api/lms.js`

### Create a new React component
1. Add file to `frontend-react/src/components/`
2. Import in parent component
3. Use Tailwind classes for styling
4. Connect to API via `lms.js` service
5. Add to React Router if it's a page

### Modify database schema
1. Create migration script in `scripts/`
2. Test locally first
3. Update `docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md`
4. Notify team (or log in `technical_decisions` table)

---

## Environment Variables

Create `.env` file in project root:

```bash
# Required
DATABASE_URL=postgresql://user:pass@host/dbname

# Optional (for Notion integration)
NOTION_API_KEY=secret_xxx
NOTION_DATABASE_ID=xxx

# Flask config
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
```

---

## Deployment Considerations

### Database (Neon)
- Serverless PostgreSQL with branching
- Free tier: 0.5GB storage, 3 branches
- Branching allows dev/staging/prod separation
- Connection pooling built-in

### Backend (Flask)
- Deploy to any Python-compatible host (Heroku, Railway, Render)
- Use `gunicorn` for production
- Set `FLASK_ENV=production`

### Frontend (React)
- Build: `npm run build`
- Deploy static files to Netlify, Vercel, GitHub Pages
- Set `REACT_APP_API_URL` to production backend

---

## Contributing

1. **Read the canon docs first** → [`canon/`](../canon/)
2. **Check existing issues** → GitHub Issues
3. **Follow file structure standards** → [`canon/FILE_STRUCTURE_AND_STANDARDS.md`](../canon/FILE_STRUCTURE_AND_STANDARDS.md)
4. **Write tests for new features**
5. **Document API changes**
6. **Submit PR with clear description**

---

## Troubleshooting

### Backend won't start
- Check `DATABASE_URL` in `.env`
- Verify PostgreSQL is accessible
- Check for import errors in `backend/app.py`

### Frontend can't connect to backend
- Verify backend is running (`http://localhost:5000`)
- Check `REACT_APP_API_URL` in `frontend-react/.env`
- Check CORS settings in `backend/app.py`

### Database connection errors
- Test connection: `psql $DATABASE_URL`
- Check Neon dashboard for database status
- Verify firewall/network access

### Module not displaying
- Check JSON schema validity
- Verify module exists in database `modules` table
- Check frontend console for errors

---

## Resources

- **Full System Architecture:** [`canon/SYSTEM_OVERVIEW.md`](../canon/SYSTEM_OVERVIEW.md)
- **Database Schema:** [`docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md`](ASCENT_BASECAMP_DATABASE_SCHEMA.md)
- **LMS API Reference:** [`docs/lms/API_REFERENCE.md`](lms/API_REFERENCE.md)
- **Frontend Architecture:** [`docs/onboarding-lms/ARCHITECTURE.md`](onboarding-lms/ARCHITECTURE.md)

---

**Questions?** Open an issue or contact [eosborn@cpp.edu](mailto:eosborn@cpp.edu)
