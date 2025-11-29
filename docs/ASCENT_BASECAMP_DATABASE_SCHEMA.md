# Ascent Basecamp + CADENCE Database Schema

**Created:** 2025-11-29  
**Agent:** Agent Gamma  
**Status:** ✅ Complete

## Overview

Complete database schema implementation for the Ascent Basecamp Learning System integrated with CADENCE CubeSat program data. The database is hosted on Neon PostgreSQL and contains 37 tables supporting:

- **CADENCE Program Data** - Historical team data from Notion export (1,416 records)
- **Ascent Basecamp Learning System** - Educational platform infrastructure
- **Student Learning Platform** - Existing student/module/team data

## Database Connection

**Provider:** Neon PostgreSQL  
**Database:** `frames`  
**Location:** us-west-2 AWS  
**Tables:** 37 total (15 new tables created in this session)

## CADENCE Tables (5 Core Tables)

### 1. cadence_people (27 records)
```sql
CREATE TABLE cadence_people (
    person_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(255),
    subsystem VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    notion_page_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Team members from CADENCE program  
**Source:** Extracted from content @mentions and assignee fields  
**Indexes:** email, subsystem

### 2. cadence_projects (69 records)
```sql
CREATE TABLE cadence_projects (
    project_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    subsystem VARCHAR(255),
    status VARCHAR(100),
    owner_id INTEGER REFERENCES cadence_people(person_id),
    notion_page_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Technical and program documentation projects  
**Source:** `cadence_raw_content` where `category IN ('documents_program', 'documents_technical')`  
**Status Values:** completed, in_progress, blocked, todo, active, unknown

### 3. cadence_tasks (443 records)
```sql
CREATE TABLE cadence_tasks (
    task_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(100),
    due_date DATE,
    assignee_id INTEGER REFERENCES cadence_people(person_id),
    project_id INTEGER REFERENCES cadence_projects(project_id),
    notion_page_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Work items and deliverables  
**Source:** `cadence_raw_content` where `category = 'tasks'`  
**Indexes:** assignee_id, project_id, status

### 4. cadence_meetings (440 records)
```sql
CREATE TABLE cadence_meetings (
    meeting_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    meeting_date TIMESTAMP,
    attendees TEXT,
    project_id INTEGER REFERENCES cadence_projects(project_id),
    notes TEXT,
    notion_page_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Team meetings and collaboration sessions  
**Source:** `cadence_raw_content` where `category = 'meetings'`

### 5. cadence_documents (71 records)
```sql
CREATE TABLE cadence_documents (
    doc_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url TEXT,
    doc_type VARCHAR(100),
    category VARCHAR(100),
    subsystem VARCHAR(255),
    notion_page_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Technical documentation and resources  
**Source:** `cadence_raw_content` where `category IN ('documents_technical', 'documents_program', 'documents_workflow')`  
**Doc Types:** technical, program, workflow  
**Indexes:** subsystem, category

## Ascent Basecamp Learning Tables (10 New Tables)

### 6. ghost_cohorts
Competition benchmarking from historical cohorts
```sql
CREATE TABLE ghost_cohorts (
    cohort_id SERIAL PRIMARY KEY,
    cohort_name VARCHAR(255) NOT NULL,
    semester VARCHAR(100),
    university VARCHAR(255),
    subsystem VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7. learner_performance
Student activity logs for adaptive learning
```sql
CREATE TABLE learner_performance (
    log_id SERIAL PRIMARY KEY,
    student_id VARCHAR(255) REFERENCES students(id),
    module_id INTEGER REFERENCES modules(id),
    attempt_number INTEGER,
    time_spent_seconds INTEGER,
    errors_count INTEGER,
    mastery_score DECIMAL(5,2),
    completed BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Indexes:** student_id, module_id

### 8. module_difficulty_calibrations
Adaptive difficulty system
```sql
CREATE TABLE module_difficulty_calibrations (
    calibration_id SERIAL PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),
    difficulty_level VARCHAR(50),
    average_time_seconds INTEGER,
    success_rate DECIMAL(5,2),
    sample_size INTEGER,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 9. ascent_basecamp_agent_log (2 records)
Multi-agent development tracking - **CRITICAL FOR AGENT CONTRACT**
```sql
CREATE TABLE ascent_basecamp_agent_log (
    log_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_name VARCHAR(100) NOT NULL,
    action_type VARCHAR(100) NOT NULL,
    subsystem VARCHAR(255),
    status VARCHAR(50),
    error TEXT,
    resolution TEXT,
    message TEXT,
    metadata JSONB
);
```
**Purpose:** Track all agent actions per 04_agents_and_dev_process.md  
**Indexes:** timestamp, agent_name

### 10. module_version_history
Spec tracking and versioning
```sql
CREATE TABLE module_version_history (
    version_id SERIAL PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),
    version_number VARCHAR(50),
    spec_json JSONB,
    change_description TEXT,
    created_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 11. simulation_environments
Tool/sandbox tracking (CircuitJS, LTSpice, FreeCAD, WebContainer)
```sql
CREATE TABLE simulation_environments (
    env_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    subsystem VARCHAR(255),
    config_json JSONB,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 12. module_prerequisites
Learning path graph
```sql
CREATE TABLE module_prerequisites (
    prereq_id SERIAL PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),
    prerequisite_module_id INTEGER REFERENCES modules(id),
    required BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 13. race_metadata
Competition/challenge data
```sql
CREATE TABLE race_metadata (
    race_id SERIAL PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),
    ghost_data JSONB,
    time_targets JSONB,
    checkpoints JSONB,
    leaderboard_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 14. subsystem_competency
Track student progress through subsystem learning paths
```sql
CREATE TABLE subsystem_competency (
    competency_id SERIAL PRIMARY KEY,
    student_id VARCHAR(255) REFERENCES students(id),
    subsystem VARCHAR(255) NOT NULL,
    competency_level VARCHAR(50),
    modules_completed INTEGER DEFAULT 0,
    last_activity TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
**Competency Levels:** orientation, competency, integration, autonomy  
**Indexes:** student_id, subsystem

### 15. notion_sync_metadata
Track Notion → Postgres sync operations
```sql
CREATE TABLE notion_sync_metadata (
    sync_id SERIAL PRIMARY KEY,
    sync_type VARCHAR(100),
    last_sync TIMESTAMP,
    records_synced INTEGER,
    errors INTEGER,
    status VARCHAR(50),
    error_details TEXT
);
```

## Existing Tables (22 tables, unchanged)

- **Student System:** students, teams, faculty, universities
- **Module System:** modules (69), module_sections (40), module_progress, module_assignments, module_feedback, module_analytics_events
- **Project System:** projects, sandboxes
- **Risk/Model System:** factor_models, factor_values, model_factors, risk_factors, model_validations, outcomes
- **Interface System:** interfaces, interface_factor_values
- **Audit System:** audit_logs
- **Raw Data:** cadence_raw_content (1,416 records - SOURCE TABLE)

## Data Population Summary

| Table | Records | Source |
|-------|---------|--------|
| cadence_people | 27 | Extracted from content |
| cadence_projects | 69 | documents_program + documents_technical |
| cadence_tasks | 443 | tasks category |
| cadence_meetings | 440 | meetings category |
| cadence_documents | 71 | documents_* categories |
| **TOTAL** | **1,050** | cadence_raw_content (1,416) |

## Subsystem Distribution

CADENCE data is organized by subsystem:
- avionics
- structures  
- mission_ops
- thermal
- power
- communications
- payload

## Migration Scripts Created

1. **scripts/create_ascent_basecamp_schema.py**
   - Creates all 15 new tables
   - Creates 13 indexes for performance
   - Validates schema creation
   - Handles data type compatibility with existing tables

2. **scripts/populate_cadence_tables.py**
   - Transforms raw content → structured tables
   - Extracts people, dates, status from markdown
   - Handles foreign key relationships
   - Logs all operations

3. **scripts/log_agent_gamma_work.py**
   - Logs agent actions to ascent_basecamp_agent_log
   - Provides audit trail per Agent Contract

## Architecture Alignment

This schema implements the **3-layer architecture** from Ascent Basecamp Core:

1. **Authoring Layer (Notion)**
   - CADENCE data imported via notion_page_id links
   - notion_sync_metadata tracks sync operations

2. **Transformation Layer (AI + Postgres)**
   - cadence_raw_content → structured tables
   - Agent logs track all transformations
   - Module specs stored with version history

3. **Runtime Layer (Student App)**
   - learner_performance logs all student activity
   - subsystem_competency tracks progress
   - ghost_cohorts provide competition benchmarks
   - module_prerequisites define learning paths

## Agent Contract Compliance

Per `04_agents_and_dev_process.md`:

✅ **All agent actions logged** to `ascent_basecamp_agent_log`  
✅ **Dashboard data in Postgres** (no direct Notion updates)  
✅ **Version control** via module_version_history  
✅ **Immutable dashboards** - data flows Postgres → Notion  

## Next Steps

1. **Data Import** - Import classified CADENCE files (868 keep, 549 exclude)
2. **Module Creation** - Convert CADENCE technical docs to learning modules
3. **Ghost Cohort Setup** - Populate ghost_cohorts from historical CADENCE data
4. **Competency Tracking** - Initialize subsystem_competency for current students
5. **Notion Sync** - Set up bidirectional sync for dashboards

## Database Access

```python
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Query CADENCE data
cur.execute("SELECT * FROM cadence_people LIMIT 10;")
```

## References

- `ascent_basecamp_core_full_docs/01_ascent_basecamp_philosophy.md`
- `ascent_basecamp_core_full_docs/02_learning_system_architecture.md`
- `ascent_basecamp_core_full_docs/03_data_and_dashboards.md`
- `ascent_basecamp_core_full_docs/04_agents_and_dev_process.md`
- `THREE_AGENT_INDEPENDENT_PLAN.md` (Agent Gamma tasks)

---

**Schema Status:** ✅ Production Ready  
**Data Status:** ✅ 1,050 records imported  
**Agent Compliance:** ✅ All actions logged  
**Documentation:** ✅ Complete
