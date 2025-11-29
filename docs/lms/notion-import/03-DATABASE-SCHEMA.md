# Database Schema - FRAMES LMS

**Database:** PostgreSQL (Neon hosted)
**Location:** `shared/database/db_models.py`
**Status:** ✅ Production (21 tables total, 6 LMS-specific)

---

## LMS Tables Overview

```
modules                    - Module metadata
├── module_sections        - Content sections within modules
├── module_assignments     - Student-module assignments
├── module_progress        - Student progress tracking
├── module_analytics_events - Interaction analytics
└── module_feedback        - Student ratings/comments
```

---

## Table: `modules`

### Purpose
Stores metadata for all training modules.

### Schema
```sql
CREATE TABLE modules (
    id                  SERIAL PRIMARY KEY,
    module_id           VARCHAR(100) UNIQUE NOT NULL,  -- Slug (e.g., 'lab-safety-101')
    title               VARCHAR(255) NOT NULL,
    description         TEXT,
    category            VARCHAR(100),                  -- 'Safety', 'Technical', 'Orientation'
    estimated_minutes   INTEGER DEFAULT 10,

    -- Ownership
    created_by_id       VARCHAR REFERENCES faculty(id),
    university_id       VARCHAR REFERENCES universities(id),

    -- Status
    status              VARCHAR(50) DEFAULT 'draft',   -- 'draft', 'published', 'archived'

    -- Organization (JSON)
    prerequisites       JSON DEFAULT '[]',             -- [module_ids]
    related_modules     JSON DEFAULT '[]',
    tags                JSON DEFAULT '[]',             -- ['required', 'safety', 'lab']

    -- Metadata
    target_audience     VARCHAR(100) DEFAULT 'incoming_students',
    revision            INTEGER DEFAULT 1,
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW(),
    published_at        TIMESTAMP
);

CREATE INDEX idx_modules_status ON modules(status);
CREATE INDEX idx_modules_category ON modules(category);
CREATE INDEX idx_modules_module_id ON modules(module_id);
```

### Current Fields
✅ All fields implemented

### Planned Extensions
```sql
-- Phase 2: Add module type system
ALTER TABLE modules ADD COLUMN module_type VARCHAR(50) DEFAULT 'text';
  -- Values: 'text', 'sandbox', 'game', 'interactive', 'guided_struggle', 'mixed'

ALTER TABLE modules ADD COLUMN interaction_level VARCHAR(20);
  -- Values: 'low', 'medium', 'high'

ALTER TABLE modules ADD COLUMN required_components JSON DEFAULT '[]';
  -- e.g., ['monaco-editor', 'three-js', 'phaser']

ALTER TABLE modules ADD COLUMN difficulty_level INTEGER DEFAULT 1;
  -- 1-5 scale

ALTER TABLE modules ADD COLUMN adaptive_config JSON;
  -- Configuration for adaptive difficulty
```

---

## Table: `module_sections`

### Purpose
Content sections within a module (like pages or slides).

### Schema
```sql
CREATE TABLE module_sections (
    id                  SERIAL PRIMARY KEY,
    module_id           INTEGER REFERENCES modules(id) ON DELETE CASCADE NOT NULL,
    section_number      INTEGER NOT NULL,              -- Display order
    section_type        VARCHAR(50) NOT NULL,          -- 'text', 'video', 'image', 'checklist'
    title               VARCHAR(255),
    content             TEXT NOT NULL,
    media_url           VARCHAR(500),
    duration_seconds    INTEGER,

    UNIQUE(module_id, section_number)
);

CREATE INDEX idx_sections_module ON module_sections(module_id);
```

### Current section_type Values
- `text` - Markdown/plain text content
- `video` - Embedded video
- `image` - Image display
- `checklist` - Task list

### Planned Extensions
```sql
-- Phase 2: Extend section_type
-- Add: 'sandbox', 'game', 'interactive', 'guided_struggle'

-- Phase 2: Add type-specific config
ALTER TABLE module_sections ADD COLUMN section_config JSON;
  -- Stores type-specific configuration:
  -- For 'sandbox': {language, files, runnable, expected_output}
  -- For 'game': {game_type, difficulty_levels, time_limit, challenges}
  -- For 'interactive': {environment_type, assets, hotspots, tasks}
  -- For 'guided_struggle': {problem_type, hints, buddy_personality}

ALTER TABLE module_sections ADD COLUMN completion_criteria JSON;
  -- What defines "complete" for this section
  -- e.g., {type: 'time', value: 60} or {type: 'task', tasks: [...]}
```

---

## Table: `module_assignments`

### Purpose
Assign modules to students (required, optional, recommended).

### Schema
```sql
CREATE TABLE module_assignments (
    id                  SERIAL PRIMARY KEY,
    module_id           INTEGER REFERENCES modules(id) ON DELETE CASCADE NOT NULL,
    student_id          VARCHAR REFERENCES students(id) ON DELETE CASCADE,
    university_id       VARCHAR REFERENCES universities(id),
    team_id             INTEGER REFERENCES teams(id),

    -- Assignment metadata
    assigned_by_id      VARCHAR REFERENCES faculty(id),
    assignment_type     VARCHAR(50) DEFAULT 'required',  -- 'required', 'optional', 'recommended'
    due_date            DATE,
    assigned_at         TIMESTAMP DEFAULT NOW(),

    UNIQUE(module_id, student_id)
);

CREATE INDEX idx_assignments_student ON module_assignments(student_id);
CREATE INDEX idx_assignments_module ON module_assignments(module_id);
```

### Current Fields
✅ All fields implemented

### Planned Extensions
```sql
-- Phase 3: Add auto-assignment rules
ALTER TABLE module_assignments ADD COLUMN auto_assigned BOOLEAN DEFAULT FALSE;
ALTER TABLE module_assignments ADD COLUMN assignment_rule VARCHAR(255);
  -- e.g., 'all_incoming_students', 'subsystem_specific'
```

---

## Table: `module_progress`

### Purpose
Track student progress through modules.

### Schema
```sql
CREATE TABLE module_progress (
    id                  SERIAL PRIMARY KEY,
    module_id           INTEGER REFERENCES modules(id) ON DELETE CASCADE NOT NULL,
    student_id          VARCHAR REFERENCES students(id) ON DELETE CASCADE NOT NULL,

    -- Progress tracking
    status              VARCHAR(50) DEFAULT 'not_started',  -- 'not_started', 'in_progress', 'completed', 'skipped'
    progress_percent    INTEGER DEFAULT 0,                  -- 0-100
    current_section     INTEGER DEFAULT 1,

    -- Timestamps
    started_at          TIMESTAMP,
    completed_at        TIMESTAMP,
    last_accessed_at    TIMESTAMP DEFAULT NOW(),

    -- Time tracking
    total_time_seconds  INTEGER DEFAULT 0,
    pause_count         INTEGER DEFAULT 0,

    UNIQUE(module_id, student_id)
);

CREATE INDEX idx_progress_student ON module_progress(student_id);
CREATE INDEX idx_progress_module ON module_progress(module_id);
CREATE INDEX idx_progress_status ON module_progress(status);
```

### Current Fields
✅ All fields implemented

### Planned Extensions
```sql
-- Phase 2: Add struggle metrics
ALTER TABLE module_progress ADD COLUMN hint_count INTEGER DEFAULT 0;
ALTER TABLE module_progress ADD COLUMN retry_count INTEGER DEFAULT 0;
ALTER TABLE module_progress ADD COLUMN error_count INTEGER DEFAULT 0;

-- Phase 2: Add adaptive tracking
ALTER TABLE module_progress ADD COLUMN difficulty_adjustments JSON;
  -- Track when and why difficulty changed

-- Phase 3: Add mastery scoring
ALTER TABLE module_progress ADD COLUMN mastery_score DECIMAL(3,2);
  -- 0.00-1.00 based on accuracy, speed, struggle signals
```

---

## Table: `module_analytics_events`

### Purpose
Granular tracking of all student interactions for analytics and adaptation.

### Schema
```sql
CREATE TABLE module_analytics_events (
    id                  SERIAL PRIMARY KEY,
    module_id           INTEGER REFERENCES modules(id) ON DELETE CASCADE NOT NULL,
    student_id          VARCHAR REFERENCES students(id) ON DELETE CASCADE NOT NULL,

    -- Event details
    event_type          VARCHAR(100) NOT NULL,         -- 'section_view', 'pause', 'hint_used', etc.
    event_data          JSON,                          -- Type-specific data
    section_number      INTEGER,

    -- Context
    session_id          VARCHAR(255),                  -- Group events by session
    device_type         VARCHAR(50),                   -- 'tablet', 'phone', 'desktop'

    -- Timing
    timestamp           TIMESTAMP DEFAULT NOW(),
    time_elapsed_seconds INTEGER                       -- Time since module start
);

CREATE INDEX idx_events_module_student ON module_analytics_events(module_id, student_id);
CREATE INDEX idx_events_type ON module_analytics_events(event_type);
CREATE INDEX idx_events_timestamp ON module_analytics_events(timestamp);
```

### Common event_type Values

**Navigation:**
- `section_view` - Section loaded
- `section_complete` - Section finished
- `module_start` - First interaction
- `module_complete` - All sections done
- `pause` - Idle >30s
- `resume` - Returns from pause

**Interaction:**
- `click` - Element clicked
- `scroll` - Page scrolled
- `input` - Text entered

**Type-Specific:**
- Sandbox: `code_run`, `error_encountered`, `code_change`, `hint_used`
- Game: `game_start`, `game_complete`, `score`, `retry`
- Interactive: `hotspot_click`, `object_drag`, `task_complete`
- Guided Struggle: `buddy_message`, `student_message`, `solution_attempted`

### Planned Extensions
```sql
-- Phase 3: Add ML features
ALTER TABLE module_analytics_events ADD COLUMN struggle_signal DECIMAL(3,2);
  -- 0.00-1.00 computed struggle intensity

-- Phase 3: Add pattern detection
ALTER TABLE module_analytics_events ADD COLUMN pattern_detected VARCHAR(100);
  -- e.g., 'confusion_loop', 'rapid_progress', 'stuck'
```

---

## Table: `module_feedback`

### Purpose
Student ratings and comments on modules.

### Schema
```sql
CREATE TABLE module_feedback (
    id                  SERIAL PRIMARY KEY,
    module_id           INTEGER REFERENCES modules(id) ON DELETE CASCADE NOT NULL,
    student_id          VARCHAR REFERENCES students(id) ON DELETE CASCADE NOT NULL,

    -- Feedback
    rating              INTEGER CHECK (rating >= 1 AND rating <= 5),
    difficulty_rating   INTEGER CHECK (difficulty_rating >= 1 AND difficulty_rating <= 5),
    comment             TEXT,

    -- Metadata
    created_at          TIMESTAMP DEFAULT NOW(),
    is_anonymous        BOOLEAN DEFAULT FALSE,

    UNIQUE(module_id, student_id)
);

CREATE INDEX idx_feedback_module ON module_feedback(module_id);
CREATE INDEX idx_feedback_rating ON module_feedback(rating);
```

### Current Fields
✅ All fields implemented

### Planned Extensions
```sql
-- Phase 3: Add detailed feedback
ALTER TABLE module_feedback ADD COLUMN engagement_rating INTEGER;
  -- "Was it engaging?" 1-5

ALTER TABLE module_feedback ADD COLUMN clarity_rating INTEGER;
  -- "Was it clear?" 1-5

ALTER TABLE module_feedback ADD COLUMN tags JSON;
  -- ['too_easy', 'confusing', 'helpful', 'fun']
```

---

## Related Non-LMS Tables

### Students
```sql
CREATE TABLE students (
    id                  VARCHAR PRIMARY KEY,
    name                VARCHAR(255),
    email               VARCHAR(255),
    university_id       VARCHAR REFERENCES universities(id),
    team_id             INTEGER REFERENCES teams(id),
    role                VARCHAR(100),
    created_at          TIMESTAMP DEFAULT NOW()
);
```

### Faculty
```sql
CREATE TABLE faculty (
    id                  VARCHAR PRIMARY KEY,
    name                VARCHAR(255),
    email               VARCHAR(255),
    university_id       VARCHAR REFERENCES universities(id),
    department          VARCHAR(255),
    created_at          TIMESTAMP DEFAULT NOW()
);
```

### Universities
```sql
CREATE TABLE universities (
    id                  VARCHAR PRIMARY KEY,
    name                VARCHAR(255),
    location            VARCHAR(255),
    contact_email       VARCHAR(255),
    created_at          TIMESTAMP DEFAULT NOW()
);
```

### Teams
```sql
CREATE TABLE teams (
    id                  SERIAL PRIMARY KEY,
    name                VARCHAR(255),
    university_id       VARCHAR REFERENCES universities(id),
    subsystem           VARCHAR(255),
    created_at          TIMESTAMP DEFAULT NOW()
);
```

---

## Migration Plan

### Phase 1: Current (✅ Done)
- All 6 LMS tables created
- Basic fields operational
- Sample data exists

### Phase 2: Module Types (🚧 Next)
```sql
-- Add type system
ALTER TABLE modules ADD COLUMN module_type VARCHAR(50) DEFAULT 'text';
ALTER TABLE modules ADD COLUMN required_components JSON DEFAULT '[]';

-- Add section configs
ALTER TABLE module_sections ADD COLUMN section_config JSON;
ALTER TABLE module_sections ADD COLUMN completion_criteria JSON;

-- Add struggle tracking
ALTER TABLE module_progress ADD COLUMN hint_count INTEGER DEFAULT 0;
ALTER TABLE module_progress ADD COLUMN retry_count INTEGER DEFAULT 0;
ALTER TABLE module_progress ADD COLUMN error_count INTEGER DEFAULT 0;
```

### Phase 3: Advanced Features (Future)
```sql
-- Adaptive difficulty
ALTER TABLE modules ADD COLUMN adaptive_config JSON;
ALTER TABLE module_progress ADD COLUMN difficulty_adjustments JSON;

-- Mastery tracking
ALTER TABLE module_progress ADD COLUMN mastery_score DECIMAL(3,2);

-- ML features
ALTER TABLE module_analytics_events ADD COLUMN struggle_signal DECIMAL(3,2);
ALTER TABLE module_analytics_events ADD COLUMN pattern_detected VARCHAR(100);

-- Enhanced feedback
ALTER TABLE module_feedback ADD COLUMN engagement_rating INTEGER;
ALTER TABLE module_feedback ADD COLUMN clarity_rating INTEGER;
ALTER TABLE module_feedback ADD COLUMN tags JSON;
```

---

## Scripts

### Bootstrap Database
```bash
python shared/database/bootstrap_db.py
```

### Add Sample Module
```bash
python apps/onboarding-lms/backend/add_sample_module.py
```

### Verify Migration
```bash
python scripts/verify_migration.py
```
