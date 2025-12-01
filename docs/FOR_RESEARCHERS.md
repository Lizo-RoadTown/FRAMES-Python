# For Researchers — Understanding FRAMES as a Research Platform

**Target Audience:** Faculty, program directors, learning scientists, and researchers studying team dynamics, knowledge transfer, and engineering education.

---

## What FRAMES Actually Is

**FRAMES** (Framework for Resilient Architecture and Multi-university Engineering Systems) is not just a learning platform—it's a **research infrastructure** designed to make invisible patterns visible.

If you study:
- How knowledge moves through engineering teams
- Where students get stuck in technical learning
- How collaboration quality affects project outcomes
- How institutional knowledge vanishes when students graduate
- How to predict team resilience before failures occur

...then FRAMES gives you the data architecture and analytical tools to answer those questions empirically.

---

## The Core Research Question

**How do complex engineering programs maintain continuity across student generations while scaling across multiple universities?**

Traditional approaches fail because:
- Knowledge lives in individuals, not systems
- Onboarding is inconsistent and undocumented
- Team interfaces create friction points that aren't measured
- Programs lack baseline data to understand "normal" vs "at-risk"

FRAMES addresses this by:
1. **Capturing** learning interactions at granular detail (time-on-task, pause points, prerequisite chains)
2. **Modeling** team structures using Non-Decomposable Architecture (NDA) principles
3. **Predicting** failure points before they cause problems
4. **Preserving** institutional knowledge in structured, reusable modules

---

## Theoretical Foundations

### 1. Non-Decomposable Architecture (NDA)

**Core idea:** Complex systems can't be understood by examining parts in isolation. You must model the *interfaces* between components.

In molecular chemistry, atoms bond through specific interaction rules. In engineering programs:
- **Subsystems** = Student teams (Power, Structures, Avionics, etc.)
- **Interfaces** = Where teams exchange data, decisions, physical components
- **Bonds** = Communication patterns, dependencies, shared resources

**FRAMES Implementation:**
- `interfaces` table tracks cross-team dependencies
- `interface_factor_values` measures communication quality
- `factor_models` defines what makes a "good" interface
- Analytics identify where interfaces are weak (friction points)

**Research output:** Predict which team interfaces will fail based on historical patterns.

---

### 2. Learning Analytics & Time-on-Task

**Core idea:** Time spent ≠ learning achieved. The *pattern* of engagement matters more than total time.

**FRAMES captures:**
- **Granular timing:** How long on each module section (not just whole modules)
- **Pause points:** Where students stop and don't return
- **Scroll depth:** How much content they actually consume
- **Revisit patterns:** When they return to review (indicates it's useful)
- **Error patterns:** Which checks they fail repeatedly

**Research output:**
- Identify content that's too difficult (high dropout at specific sections)
- Find optimal module length (when engagement drops off)
- Compare learning patterns across universities/cohorts
- Predict mastery based on engagement patterns, not just completion

**Database tables:**
- `learner_performance` — Individual student activity logs
- `module_analytics_events` — Every scroll, pause, click
- `module_progress` — Section-level completion tracking

---

### 3. Knowledge Transfer Theory

**Core idea:** Expertise doesn't transfer automatically. It requires structured processes.

Traditional problem:
- Senior students graduate → knowledge disappears
- New students ask same questions every semester
- Mentors repeat explanations verbally (inconsistent quality)

**FRAMES solution:**
- Convert tacit knowledge (procedures, troubleshooting) into **explicit modules**
- Track which modules are **actually used** vs created but ignored
- Measure **prerequisite chains** to ensure proper scaffolding
- Use **ghost cohorts** to preserve historical performance benchmarks

**Research output:**
- Which types of knowledge are easiest/hardest to transfer
- Optimal prerequisite structures for complex technical skills
- How long institutional knowledge remains relevant before becoming obsolete

---

### 4. Adaptive Learning (OATutor Framework)

**Core idea:** Learning is maximized when difficulty matches student readiness.

FRAMES adapts OATutor (originally for math) to engineering:
- **Scaffolded hints:** Progressive support when students struggle
- **Checks/validation:** Immediate feedback on understanding
- **Step-based reasoning:** Break complex tasks into verifiable sub-tasks
- **Adaptive sequencing:** Recommend next module based on mastery

**Research output:**
- Compare scaffolded vs non-scaffolded learning outcomes
- Identify which engineering topics benefit most from adaptive support
- Measure hint usage patterns (when students ask for help)

---

## Data You Can Access

### 1. Student Learning Data

**What's captured:**
```
For every student, for every module:
- Start time, completion time, total time spent
- Time spent per section
- Where they paused and for how long
- Which hints they used
- Which checks they failed (and how many attempts)
- Scroll position when they left
- Device type (mobile vs desktop)
- Session count (how many times they returned)
```

**Research questions you can answer:**
- What's the optimal module length before engagement drops?
- Which subsystems have the steepest learning curves?
- Do mobile learners have different patterns than desktop?
- Which prerequisite chains are most effective?

**Tables:**
- `learner_performance` — 1 row per module attempt
- `module_analytics_events` — All interaction events
- `module_progress` — Current state per student/module
- `subsystem_competency` — Progress through subsystems

---

### 2. Team Collaboration Data (CADENCE Program)

**What's captured:**
```
Historical data from CADENCE CubeSat program (2020-2024):
- 1,416 records from Notion workspace
- Tasks completed, meeting notes, project documentation
- Team member assignments and roles
- Cross-subsystem dependencies
```

**Research questions you can answer:**
- How do team structures evolve over semesters?
- Which subsystems have the most cross-team dependencies?
- How long does it take new students to contribute meaningfully?
- What's the relationship between meeting frequency and project success?

**Tables:**
- `cadence_people` (27 team members)
- `cadence_projects` (69 projects)
- `cadence_tasks` (443 tasks)
- `cadence_meetings` (440 meetings)
- `cadence_documents` (71 technical docs)

---

### 3. NDA Interface Modeling

**What's captured:**
```
For every team-to-team interface:
- Communication frequency
- Dependency type (data, physical, decision)
- Interface quality metrics (from factor models)
- Friction points (delays, miscommunications)
```

**Research questions you can answer:**
- Which interfaces are weakest (predict failures)?
- How does interface quality correlate with project success?
- Can we predict which teams will struggle based on interface patterns?
- How do interface patterns differ across universities?

**Tables:**
- `interfaces` — All team-to-team connections
- `interface_factor_values` — Quality measurements
- `factor_models` — Definition of "good" interface

---

### 4. Ghost Cohort Benchmarks (Competitive Learning)

**What's captured:**
```
Historical performance data from previous semesters:
- Fast/medium/slow completion times per module
- Subsystem-specific benchmarks
- University-specific patterns
- Semester-to-semester trends
```

**Research questions you can answer:**
- Does competitive learning (race mode) improve engagement?
- How do current students compare to historical cohorts?
- Which universities have strongest performance in which subsystems?
- Are benchmarks stable over time or do they drift?

**Tables:**
- `ghost_cohorts` — Historical cohort metadata
- `race_metadata` — Competitive learning configurations

---

## Analytics Platform Architecture

```
┌─────────────────────────────────────────────────────┐
│           PostgreSQL Database (Neon)                │
│  - 37 tables with learning, team, and NDA data     │
└──────────────────┬──────────────────────────────────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
┌─────▼─────┐ ┌───▼────┐ ┌─────▼──────┐
│ Jupyter   │ │ Custom │ │  MLflow    │
│ Notebooks │ │ Dashbd │ │ Experiment │
│           │ │        │ │  Tracking  │
└───────────┘ └────────┘ └────────────┘
Analytics      Realtime     ML Models
(Python/R)     (Metabase)   (Training)
```

### Jupyter Notebooks (Exploratory Analysis)
- Direct database access via `psycopg2` or `SQLAlchemy`
- Python libraries: pandas, numpy, matplotlib, seaborn
- R support for statistical modeling
- Export results to CSV, PDF, or notebooks

### Custom Dashboards (Real-Time Monitoring)
- Built with Metabase or Superset
- Pre-configured views for common queries
- Team lead dashboards show student progress
- Faculty dashboards show program-wide trends

### MLflow (Experiment Management)
- Track machine learning experiments
- Version models and datasets
- Compare model performance
- Deploy models as prediction APIs

---

## Example Research Workflows

### Workflow 1: Analyze Learning Drop-Off Points

**Question:** Where do students abandon modules?

```python
import psycopg2
import pandas as pd

# Connect to database
conn = psycopg2.connect(DATABASE_URL)

# Query drop-off data
query = """
SELECT
    m.title,
    ms.section_number,
    ms.title as section_title,
    COUNT(DISTINCT mp.student_id) as students_started,
    COUNT(DISTINCT CASE WHEN mp.status = 'completed'
          THEN mp.student_id END) as students_completed,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN mp.status = 'completed'
          THEN mp.student_id END) / COUNT(DISTINCT mp.student_id), 2) as completion_rate
FROM modules m
JOIN module_sections ms ON m.id = ms.module_id
JOIN module_progress mp ON ms.id = mp.section_id
GROUP BY m.id, m.title, ms.section_number, ms.title
ORDER BY completion_rate ASC
LIMIT 20;
"""

df = pd.read_sql(query, conn)
print(df)

# Result: Sections with lowest completion rates = drop-off points
```

**Research output:** Identify which content needs redesign or additional scaffolding.

---

### Workflow 2: NDA Interface Analysis

**Question:** Which team interfaces are weakest?

```python
query = """
SELECT
    i.interface_name,
    i.from_team,
    i.to_team,
    AVG(ifv.factor_value) as avg_quality,
    COUNT(ifv.id) as measurements
FROM interfaces i
JOIN interface_factor_values ifv ON i.id = ifv.interface_id
GROUP BY i.id, i.interface_name, i.from_team, i.to_team
HAVING AVG(ifv.factor_value) < 3.0  -- Weak threshold
ORDER BY avg_quality ASC;
"""

weak_interfaces = pd.read_sql(query, conn)

# Visualize as network graph
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
for _, row in weak_interfaces.iterrows():
    G.add_edge(row['from_team'], row['to_team'],
               weight=row['avg_quality'],
               label=row['interface_name'])

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=2000, font_size=10, arrows=True)
plt.title("Weak Team Interfaces (Quality < 3.0)")
plt.show()
```

**Research output:** Network diagram showing which teams have communication problems.

---

### Workflow 3: Time-on-Task Patterns

**Question:** How long do students actually spend on modules vs. estimates?

```python
query = """
SELECT
    m.title,
    m.estimated_minutes,
    AVG(lp.time_spent_seconds / 60.0) as avg_actual_minutes,
    STDDEV(lp.time_spent_seconds / 60.0) as stddev_minutes,
    COUNT(lp.student_id) as sample_size
FROM modules m
JOIN learner_performance lp ON m.id = lp.module_id
WHERE lp.completed = TRUE
GROUP BY m.id, m.title, m.estimated_minutes
HAVING COUNT(lp.student_id) >= 5  -- Minimum sample size
ORDER BY ABS(m.estimated_minutes - AVG(lp.time_spent_seconds / 60.0)) DESC;
"""

time_comparison = pd.read_sql(query, conn)

# Visualize
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.scatter(time_comparison['estimated_minutes'],
            time_comparison['avg_actual_minutes'],
            s=time_comparison['sample_size']*10,
            alpha=0.6)
plt.plot([0, 120], [0, 120], 'r--', label='Perfect Estimate')
plt.xlabel('Estimated Time (minutes)')
plt.ylabel('Actual Average Time (minutes)')
plt.title('Module Time Estimates vs Reality')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

**Research output:** Identify which modules have inaccurate time estimates (need recalibration).

---

## Multi-University Comparison

FRAMES supports **8 partner universities**, enabling cross-institution research:

```python
query = """
SELECT
    u.name as university,
    COUNT(DISTINCT s.id) as students,
    COUNT(DISTINCT m.id) as modules_completed,
    AVG(lp.mastery_score) as avg_mastery,
    AVG(lp.time_spent_seconds / 60.0) as avg_time_minutes
FROM universities u
JOIN students s ON u.id = s.university_id
JOIN learner_performance lp ON s.id = lp.student_id
JOIN modules m ON lp.module_id = m.id
WHERE lp.completed = TRUE
GROUP BY u.id, u.name
ORDER BY avg_mastery DESC;
"""

university_comparison = pd.read_sql(query, conn)
print(university_comparison)
```

**Research questions:**
- Do some universities have higher mastery scores?
- Are time patterns consistent across institutions?
- Which universities excel in which subsystems?

---

## Predictive Modeling Opportunities

### 1. Student Success Prediction

**Input features:**
- Time-on-task patterns in first 3 modules
- Hint usage frequency
- Error rates on checks
- Revisit frequency

**Prediction target:**
- Will student complete all modules in subsystem?
- Probability of mastery (score > 80%)
- Time to completion

**Use case:** Early intervention for at-risk students.

---

### 2. Team Resilience Prediction

**Input features:**
- Interface quality scores
- Meeting frequency
- Task completion rates
- Cross-subsystem dependencies

**Prediction target:**
- Likelihood of project delays
- Risk of team member turnover
- Interface failure probability

**Use case:** Proactive team restructuring or support.

---

### 3. Content Effectiveness Prediction

**Input features:**
- Drop-off rates
- Time per section
- Error patterns
- Prerequisite chain structure

**Prediction target:**
- Which modules need redesign?
- Optimal prerequisite ordering
- Ideal module length

**Use case:** Data-driven curriculum improvement.

---

## Data Export and Privacy

### Data Access Levels

**Level 1 (Public):**
- Aggregated statistics (no individual students)
- Module completion rates
- Average time-on-task

**Level 2 (IRB-Approved Research):**
- De-identified student data
- Individual learning patterns
- Team collaboration data

**Level 3 (Institution-Specific):**
- Identifiable student data
- Only accessible to home institution faculty
- Requires FERPA compliance

### Export Formats

```bash
# CSV export
psql $DATABASE_URL -c "COPY (SELECT * FROM learner_performance) TO STDOUT CSV HEADER" > data.csv

# JSON export
psql $DATABASE_URL -t -c "SELECT json_agg(row_to_json(t)) FROM (SELECT * FROM modules) t" > modules.json

# Pandas DataFrame
import pandas as pd
df = pd.read_sql("SELECT * FROM learner_performance", conn)
df.to_csv('learning_data.csv')
df.to_excel('learning_data.xlsx')
```

---

## Research Outputs Enabled by FRAMES

### Published Research Areas

1. **Learning Analytics**
   - Optimal module design patterns
   - Prerequisite chain effectiveness
   - Adaptive hint usage patterns

2. **Knowledge Transfer**
   - Institutional knowledge preservation
   - Cross-generational learning effectiveness
   - Mentor-student interaction patterns

3. **Team Dynamics (NDA)**
   - Interface quality prediction
   - Team resilience modeling
   - Cross-subsystem collaboration patterns

4. **Multi-University Studies**
   - Comparative program effectiveness
   - Cultural/institutional differences
   - Scalability of training approaches

---

## Getting Started as a Researcher

### 1. Database Access

Contact [eosborn@cpp.edu](mailto:eosborn@cpp.edu) for:
- Read-only database credentials
- IRB approval coordination (if needed)
- Data dictionary and schema documentation

### 2. Analysis Environment

**Option A: Jupyter Notebooks (Recommended)**
```bash
pip install jupyterlab pandas numpy matplotlib seaborn psycopg2
jupyter lab
```

**Option B: R/RStudio**
```r
install.packages(c("RPostgreSQL", "dplyr", "ggplot2"))
library(RPostgreSQL)
```

**Option C: Direct SQL (pgAdmin, DBeaver)**
- Download pgAdmin or DBeaver
- Connect using provided credentials
- Run SQL queries directly

### 3. Documentation

- **Database Schema:** [`docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md`](ASCENT_BASECAMP_DATABASE_SCHEMA.md)
- **FRAMES Philosophy:** [`canon/FRAMES_PHILOSOPHY.md`](../canon/FRAMES_PHILOSOPHY.md)
- **Analytics Architecture:** [`docs/research-analytics/ARCHITECTURE.md`](research-analytics/ARCHITECTURE.md)

---

## Collaboration Opportunities

**Interested in collaborating?** We welcome research partnerships on:
- Learning analytics in engineering education
- NDA modeling and team dynamics
- Predictive models for student success
- Multi-university comparative studies

**Contact:** Elizabeth Osborn ([eosborn@cpp.edu](mailto:eosborn@cpp.edu)), Cal Poly Pomona

**Partner Universities:**
Cal Poly Pomona • Cal Poly SLO • Arizona State • CU Boulder • UCLA • USC • Stanford • UC Berkeley

---

## Resources

- **FRAMES Philosophy:** [`canon/FRAMES_PHILOSOPHY.md`](../canon/FRAMES_PHILOSOPHY.md)
- **System Architecture:** [`canon/SYSTEM_OVERVIEW.md`](../canon/SYSTEM_OVERVIEW.md)
- **Database Schema:** [`docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md`](ASCENT_BASECAMP_DATABASE_SCHEMA.md)
- **Analytics Platform:** [`docs/research-analytics/ARCHITECTURE.md`](research-analytics/ARCHITECTURE.md)
- **API Reference:** [`docs/lms/API_REFERENCE.md`](lms/API_REFERENCE.md)
