# Ascent Basecamp Frontend - React Configuration

This directory contains pre-built React components and configuration files ready to be copied into the React app once `create-react-app` finishes installing.

## Created by Agent Beta - Session #1

**Date:** November 28, 2025  
**Purpose:** Frontend scaffolding for Ascent Basecamp student learning platform

---

## Files Included

### Configuration Files
- `package.json` - Dependencies (React Router, Axios, Tailwind CSS)
- `tailwind.config.js` - Custom theme with Ascent branding, competency colors, animations

### API Service Layer
- `lms-api-service.js` - Axios client with wrappers for all 8 LMS endpoints
  - Module lifecycle: startModule, logActivity, completeModule
  - Competitive: getGhostCohorts, getLeaderboard, getSubsystemCompetency
  - Race mode: startRace, completeRace
  - Helper utilities: formatTime, calculateProgress, getCompetencyColor, getCelebrationLevel

### Custom Hooks
- `useModulePlayer.js` - Comprehensive module player state management
  - Timer with pause/resume
  - Activity logging every 30 seconds
  - Check validation system
  - Race mode with ghost comparison
  - Progress tracking
  - Step navigation

### Core Components
- `Dashboard.jsx` - Main student dashboard
  - Subsystem navigation sidebar
  - Module browser (grid/list view)
  - Competency progress bars
  - Dark mode toggle
  
- `ModulePlayer.jsx` - Step-by-step module interface
  - Progress stepper
  - Check validation UI
  - Hint system
  - Quiz/reflection forms
  - Timer display (normal + race mode)
  - Race checkpoints
  - Celebration modal

---

## Installation Instructions

Once `npx create-react-app frontend-react` completes:

### 1. Copy Configuration Files
```powershell
# From workspace root
cp frontend-react-config/package.json frontend-react/
cp frontend-react-config/tailwind.config.js frontend-react/
```

### 2. Install Dependencies
```powershell
cd frontend-react
npm install
```

### 3. Set Up Tailwind CSS
```powershell
# Create postcss.config.js
npx tailwindcss init -p
```

### 4. Copy Source Files
```powershell
# API Service
mkdir frontend-react/src/api
cp frontend-react-config/lms-api-service.js frontend-react/src/api/lms.js

# Hooks
mkdir frontend-react/src/hooks
cp frontend-react-config/useModulePlayer.js frontend-react/src/hooks/

# Pages
mkdir frontend-react/src/pages
cp frontend-react-config/Dashboard.jsx frontend-react/src/pages/
cp frontend-react-config/ModulePlayer.jsx frontend-react/src/pages/
```

### 5. Create Supporting Components

Still needed (to be created):
- `src/components/ModuleCard.jsx` - Module display card
- `src/components/SubsystemNav.jsx` - Subsystem navigation menu
- `src/components/CompetencyBar.jsx` - Progress indicator
- `src/components/LoadingSpinner.jsx` - Loading state
- `src/components/ProgressStepper.jsx` - Step indicator
- `src/components/CheckValidation.jsx` - Check input/feedback
- `src/components/HintTooltip.jsx` - Hint display
- `src/components/RaceTimer.jsx` - Race timer with targets
- `src/components/CelebrationModal.jsx` - Completion celebration

### 6. Update Tailwind CSS Index
Edit `frontend-react/src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 7. Set Up Router
Edit `frontend-react/src/App.js`:
```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import ModulePlayer from './pages/ModulePlayer';

function App() {
  const studentId = 'student_001'; // TODO: Get from auth

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard studentId={studentId} />} />
        <Route path="/dashboard" element={<Dashboard studentId={studentId} />} />
        <Route path="/module/:moduleId" element={<ModulePlayer studentId={studentId} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
```

### 8. Environment Variables
Create `frontend-react/.env`:
```
REACT_APP_API_URL=http://localhost:5000/api/lms
```

---

## Features Implemented

### ✅ Complete
- API service layer for all 8 endpoints
- Module player state management hook
- Dashboard with subsystem navigation
- Module player with step-by-step UI
- Timer system (normal + race mode)
- Dark mode toggle
- Responsive design (grid/list views)

### ⏳ Pending
- Supporting component implementations
- Leaderboard component
- Ghost race visualization
- Achievement badges
- User authentication
- Module catalog integration

---

## API Endpoints Consumed

All endpoints from `docs/lms/API_REFERENCE.md`:

1. `POST /students/{id}/modules/{module_id}/start`
2. `POST /students/{id}/modules/{module_id}/log_activity`
3. `POST /students/{id}/modules/{module_id}/complete`
4. `GET /modules/{id}/ghost_cohorts`
5. `GET /students/{id}/leaderboard`
6. `GET /students/{id}/subsystem_competency`
7. `POST /students/{id}/race/start`
8. `POST /students/{id}/race/complete`

---

## Architecture Decisions

**State Management:** React hooks (Context API for future auth/user state)  
**Styling:** Tailwind CSS with custom theme  
**Routing:** React Router v6  
**API Client:** Axios with interceptors  
**Module Player:** Custom hook pattern for reusability  

**Design Patterns:**
- Component composition (Dashboard uses SubsystemNav, ModuleCard, etc.)
- Custom hooks for complex state (useModulePlayer)
- Controlled components for forms/checks
- Prop drilling minimized (will add Context for global state)

---

## Testing Strategy

**Unit Tests:**
- API service layer (mock axios)
- useModulePlayer hook (React Testing Library)
- Component rendering (snapshot tests)

**Integration Tests:**
- Dashboard → ModulePlayer flow
- Module completion → Competency update
- Race mode → Leaderboard update

**E2E Tests (Future):**
- Complete module flow with Cypress
- Race mode competitive experience

---

## Next Steps (Session #2)

1. Wait for React app installation to complete
2. Copy all files from this config directory
3. Create remaining supporting components
4. Test module player with real module data from Alpha
5. Implement leaderboard component
6. Add ghost race visualization
7. Connect to backend API (confirm endpoints work)

---

## Dependencies

```json
{
  "react": "^18.2.0",
  "react-router-dom": "^6.20.0",
  "axios": "^1.6.2",
  "tailwindcss": "^3.3.6"
}
```

---

## Notes for Other Agents

**To Alpha (Module Creator):**
- Dashboard expects modules with: `{id, title, estimated_minutes, subsystem}`
- ModulePlayer expects: `{steps: [{title, content, checks, quiz}]}`
- Checks need: `{id, validation, successMessage, errorMessage, hint}`

**To Gamma (Infrastructure):**
- All API calls go through axios client at `src/api/lms.js`
- Proxy configured in package.json: `"proxy": "http://localhost:5000"`
- Can add auth interceptors when authentication is ready

---

**Created by:** Agent Beta  
**Session ID:** beta_20251128_215253_03d2d02e  
**Status:** Phase 3 in progress - waiting for React installation
