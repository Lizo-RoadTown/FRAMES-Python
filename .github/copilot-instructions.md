# FRAMES AI Agent Instructions

⚠️ **CANONICAL DOCUMENTATION**: All authoritative documentation is now in `/canon/`. Start with `canon/INDEX.md` for navigation.

## Project Overview
FRAMES is a multi-university research platform for space mission programs combining:
- **Research Analytics**: Faculty tools analyzing team dynamics and knowledge transfer using NDA (Non-Decomposable Architecture) theory
- **Onboarding LMS**: AI-powered student training system (in development)
- **AI Prediction Core**: ML engine for mission success prediction (planned)

All apps share a **Neon PostgreSQL database** with 20+ tables tracking 8 universities, teams, students, faculty, projects, interfaces, and outcomes.

**Key Documentation:**
- System architecture: `canon/SYSTEM_OVERVIEW.md`
- Database schema: `canon/DATABASE_SCHEMA.md`
- Agent protocols: `canon/AGENT_SYSTEM_OVERVIEW.md`
- Migration map: `MIGRATION_MAP.md` (if files moved)

## Architecture

### Monorepo Structure
```
apps/
  research-analytics/    # Active: Flask + React analytics dashboard
  onboarding-lms/        # In dev: Student training modules
  ai-core/               # Planned: ML prediction engine
backend/                 # Main Flask API (2000+ lines)
shared/database/         # SQLAlchemy models shared across apps
frontend/                # Legacy vanilla JS templates
frontend-react/          # React frontends
```

### Database Connection
- **Required**: `DATABASE_URL` in `.env` (Neon PostgreSQL connection string)
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Models**: `backend/db_models.py` (20+ tables)
- **Key tables**: `teams`, `faculty`, `projects`, `interfaces`, `students`, `universities`, `risk_factors`, `outcomes`

### Multi-University Data Model
- Each entity has `university_id` field (nullable for shared resources like PROVES project)
- Interfaces track `from_university`/`to_university` with `is_cross_university` flag
- Permission system: users can only modify their university's data (unless researcher role)
- PROVES project (`university_id=NULL`) is shared collaborative nucleus

## Development Workflows

### Starting the Backend
```bash
# Activate environment (if using venv)
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run Flask (development server)
python backend/app.py  # Starts on http://localhost:5000

# Test database connection
python shared/database/test_db_connection.py
```

### Testing
```bash
# Run endpoint tests
python backend/test_endpoints.py

# Run LMS-specific tests
pytest backend/test_lms_endpoints.py -v

# Quick API test
python backend/test_lms_quick.py  # Requires Flask running
```

### Database Operations
```bash
# Initialize/update tables
python shared/database/bootstrap_db.py

# Check current data
python check_neon_data.py

# Seed multi-university sample data
python backend/seed_multi_university.py
```

## Key Patterns & Conventions

### API Route Structure
- **CRUD patterns**: All entities follow `GET /api/<resource>`, `POST /api/<resource>`, `GET /api/<resource>/<id>`, `PUT /api/<resource>/<id>`, `DELETE /api/<resource>/<id>`
- **Filtering**: Query params like `?university_id=CalPolyPomona` for scoping
- **Dashboards**: `/api/dashboard/comparative` returns aggregated multi-university data
- **Analytics**: `/api/analytics/data` accepts flexible POST body for dynamic metric queries

### Database Model Conventions
```python
class MyModel(db.Model):
    __tablename__ = 'my_table'
    id = db.Column(db.String, primary_key=True)  # String IDs, not auto-increment
    university_id = db.Column(db.String, nullable=True, index=True)
    created_at = db.Column(db.String, default=lambda: datetime.now().isoformat())
    meta = db.Column(db.JSON, nullable=True)  # Flexible metadata field
    
    def to_dict(self):
        return {
            'id': self.id,
            'university_id': self.university_id,
            # ... all fields
        }
```

### Audit Logging
Critical operations use `_log_audit(actor, action, entity_type, entity_id, before, after)` to track changes in `audit_logs` table.

### Energy Loss Calculation
- NDA theory: Interfaces have "energy loss" representing knowledge transfer friction
- **Legacy system**: Direct `energy_loss` integer field (0-100)
- **New system**: `energy_engine.py` with configurable `RiskFactor`/`FactorValue` tables allowing researchers to test different models
- Use `EnergyCalculationEngine` class for dynamic calculations

## Critical Files

### Backend Core
- `backend/app.py` (2071 lines): Main Flask app with 50+ routes
- `backend/db_models.py` (446 lines): All SQLAlchemy models
- `backend/energy_engine.py` (414 lines): Risk factor calculation engine
- `backend/database.py`: SQLAlchemy db instance (import from here to avoid circular imports)

### Frontend
- `frontend/templates/dashboard.html`: 3D molecular visualization (Force Graph 3D)
- `frontend/templates/comparative_dashboard.html`: Multi-university comparison table
- `frontend/static/api.js`: JavaScript API client wrapper

### Documentation
- `README.md`: High-level project overview
- `MONOREPO_STRUCTURE.md`: Repository organization
- `docs/EDUCATIONAL_FRAMEWORK.md`: LMS module structure philosophy
- `backend/LMS_API_README.md`: Complete API documentation

## Common Tasks

### Adding a New Entity Type
1. Create model in `backend/db_models.py` with `to_dict()` method
2. Add CRUD routes in `backend/app.py` following existing patterns
3. Include `university_id` field and permission checks
4. Add audit logging for create/update/delete
5. Run `python shared/database/bootstrap_db.py` to create table

### Working with Multi-University Data
```python
# Filter by university
teams = TeamModel.query.filter_by(university_id='CalPolyPomona').all()

# Cross-university queries
interfaces = InterfaceModel.query.filter_by(is_cross_university=True).all()

# Permission check pattern
actor_university = request.headers.get('X-University-ID', 'CalPolyPomona')
is_researcher = request.headers.get('X-Is-Researcher', 'false').lower() == 'true'
if not is_researcher and team.university_id != actor_university:
    return jsonify({'error': 'Unauthorized'}), 403
```

### Adding Analytics Endpoints
See `/api/analytics/data` POST endpoint for flexible aggregation pattern using SQLAlchemy `func.count()`, `func.avg()`, and `.group_by()`.

## Important Context

### NDA Theory Foundation
FRAMES uses molecular chemistry metaphors:
- **Molecules (nodes)**: Teams, faculty, projects
- **Bonds (edges)**: Interfaces between entities
- **Energy Loss**: Knowledge transfer friction (0-100 scale)
- **Bond Types**: `codified-strong` (documented), `institutional-weak` (tacit knowledge), `fragile-temporary`

### Student Lifecycle Management
Students have `terms_remaining` field that decrements via `/api/university/<id>/advance-term` endpoint. Status auto-calculates:
- `incoming`: ≥6 terms remaining
- `established`: 3-5 terms
- `outgoing`: ≤2 terms

### Module System (LMS)
Modules stored as JSON in `modules/enhanced/` with schema defining sections, practice steps, knowledge checks. See `docs/MODULE_SCHEMA.md`.

## Dependencies
- Flask 3.0.0 + Flask-CORS + Flask-SQLAlchemy
- psycopg2-binary (PostgreSQL driver)
- python-dotenv (environment variables)
- SQLAlchemy 2.0.44

No pytest in main requirements - install separately for testing.

## Gotchas
- **Import order**: Always import `db` from `backend.database`, not `backend.app`, to avoid circular imports
- **ID generation**: Use timestamps (`f"team_{int(datetime.now().timestamp() * 1000)}"`) not UUIDs
- **String IDs**: Primary keys are strings, not integers
- **Neon SSL**: Connection string must include `?sslmode=require`
- **PROVES project**: Special case with `university_id=NULL` for collaborative work
- **Legacy HTML**: `frontend/templates/index_original.html` is 2400+ line monolith being migrated

## When Stuck
1. Check if `.env` has valid `DATABASE_URL`
2. Run `python check_neon_data.py` to inspect current DB state
3. Review `backend/test_endpoints.py` for working API examples
4. Check existing models in `db_models.py` for pattern reference
