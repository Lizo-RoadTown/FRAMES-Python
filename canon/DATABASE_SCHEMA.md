# Database Schema Overview

Primary database: PostgreSQL 15+

Includes:
- Core FRAMES tables (universities, teams, students, faculty, projects)
- LMS tables (modules, sections, progress, analytics events)
- Research tables (experiments, models, predictions, embeddings)
- Agent tables (agent state, memory, logs — partitioned)
- Notion sync metadata

See codebase `/database/schema/*.sql` for full DDL.
