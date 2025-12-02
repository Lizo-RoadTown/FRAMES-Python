# Student Onboarding LMS

## Purpose

Mobile-first progressive web app for **student engineering onboarding**.

This is the ONLY web application we're building - there is no separate Team Lead web app (Notion serves that purpose).

## Critical Understanding

### Engineering Onboarding vs Traditional Learning

Engineering learning follows **project workflow**, not traditional step-by-step sequences:

- **Traditional learning**: Linear progression, arbitrary order, step-by-step
- **Engineering onboarding**: Contextual to project phase, "what to know WHEN"

Students need to understand:

- What knowledge is required for each project phase
- When specific skills become necessary
- How subsystems interact in real missions
- Real constraints (power, mass, budget, schedule)

This is why **engineering learning curves are steep** and onboarding is difficult.

### How This LMS is Different

- **Content sourced from real missions** - Team Lead Notion documentation
- **OATutor scaffolding** - reduces steep learning curve through guided steps
- **Project-aligned sequencing** - modules match typical CubeSat project phases
- **Interactive validation** - check understanding constantly, not just final quizzes
- **Real context** - every module connects to actual engineering work

## Features

### Student-Facing

- **Module browsing** by subsystem, discipline, or project phase
- **OATutor-structured content** with scaffolding and hints
- **Interactive validation** at each step
- **Hint system** (graduated assistance without giving answers)
- **Progress tracking** (resume where you left off)
- **Race mode** (compete against ghost cohort benchmarks)
- **Time + engagement analytics** (scroll depth, time on task)
- **Assignments from Team Leads** (via Notion → Database → LMS)

### Behind the Scenes

- Consumes modules from database (sourced from Team Lead Notion)
- Tracks student interactions (hints used, steps completed, time spent)
- Syncs progress back to database → Notion for Team Lead visibility
- Uses OATutor pedagogical framework for all interactive content

## Architecture

### Frontend

- **React PWA** (mobile-first, offline-capable)
- **Located**: `apps/onboarding-lms/frontend-react/`

### Backend

- **Flask/FastAPI** routes
- **Located**: `backend/lms_routes.py`

### Database Tables

- `modules` - Module metadata and content
- `module_sections` - Individual sections within modules
- `module_progress` - Student completion tracking
- `module_assignments` - Team Lead assignments to students
- `module_analytics_events` - Detailed interaction tracking
- `ghost_cohorts` - Benchmark data for race mode

### Data Flow

```text
Team Lead Notion (real mission docs)
         ↓ (sync to database)
PostgreSQL Database
         ↓ (API fetch)
Student LMS Frontend (React)
         ↓ (progress tracking)
Database (student_progress)
         ↓ (sync back)
Notion (Team Lead visibility)
```

## OATutor Integration

### Why OATutor Framework Matters

OATutor provides **pedagogical methodology** for reducing steep learning curves:

- **Scaffolding**: Break complex engineering tasks into manageable steps
- **Hint pathways**: Provide help when stuck (without giving answers)
- **Interactive validation**: Check understanding at each step, not just end
- **Adaptive sequencing**: Adjust difficulty based on performance

### How Students Experience It

1. **Main problem**: Real engineering task in mission context
2. **Scaffolded steps**: Break complex problem into guided sequence
3. **Hints available**: Request help at each step (3 levels: gentle → specific → explicit)
4. **Validate answers**: Immediate feedback, learn from errors
5. **Build confidence**: Progress through validated steps

### Implementation Requirements

Beta must implement OATutor components:

- **Step navigation UI** - progress through scaffolded steps
- **Hint display system** - show/hide graduated hints
- **Validation feedback** - visual check/error indicators
- **Progress tracking** - which steps completed, which hints used
- **Adaptive pathways** - alternative routes based on performance

## What Beta Agent Builds

### Components Needed

From the analysis, Beta needs to create:

1. `ModuleCard.jsx` - Display module in grid/list view
2. `SubsystemNav.jsx` - Sidebar navigation by subsystem
3. `CompetencyBar.jsx` - Visual progress indicator
4. `ProgressStepper.jsx` - Step-by-step navigation (OATutor)
5. `CheckValidation.jsx` - Exercise validation UI (OATutor)
6. `HintTooltip.jsx` - Hint display system (OATutor)
7. `RaceTimer.jsx` - Race mode timer + ghost comparison
8. `CelebrationModal.jsx` - Success animations
9. `LoadingSpinner.jsx` - Loading states

### Data Integration

- Connect to PostgreSQL via backend API
- Fetch modules created by Alpha (OATutor-structured)
- Track student progress in real-time
- Handle offline mode (PWA capability)
- Sync when connection restored

### Testing

- Test with real student accounts
- Validate OATutor scaffolding works correctly
- Ensure hint pathways display properly
- Check progress tracking accuracy
- Mobile responsiveness critical (mobile-first)

## Success Criteria

- ✅ Students can browse and access modules
- ✅ OATutor scaffolding/hints work smoothly
- ✅ Progress tracked accurately
- ✅ Race mode functional with ghost cohorts
- ✅ Mobile-first experience (responsive, fast, offline-capable)
- ✅ Assignments from Team Leads appear correctly
- ✅ Analytics capture student engagement data

## What This LMS Does NOT Do

- ❌ Team Lead module creation (that happens in Notion)
- ❌ Direct Notion editing (read-only consumption via database)
- ❌ Admin functions (Team Leads work in Notion, researchers use separate platform)
- ❌ Content authoring (Alpha extracts/structures content from Notion)

This is purely a **student learning experience** - consume content, track progress, provide scaffolding.
