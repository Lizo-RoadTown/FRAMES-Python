# Technical Decisions Log - FRAMES LMS

**Purpose:** Document key technical decisions, rationale, and alternatives considered.

---

## Decision 1: Monorepo vs. Separate Repositories

**Date:** November 25, 2025
**Status:** ✅ Decided - Monorepo

### Context
Initially considered creating separate GitHub repositories for each application:
- `frames-onboarding-lms`
- `frames-research-analytics`
- `frames-ai-core`

### Decision
Use a **single monorepo** with apps organized under `apps/` folder.

### Rationale
**Pros of Monorepo:**
- Shared database schema in one place (`shared/database/`)
- Easier to keep schema changes synchronized
- Single source of truth for models
- Unified documentation
- One deployment pipeline
- Simpler dependency management

**Cons:**
- Larger repository size
- Potential merge conflicts across apps
- Tighter coupling

**Alternatives Considered:**
- Separate repos with shared database package (via npm/pip)
  - Rejected: Sync issues, versioning complexity
- Git branches for each app
  - Rejected: Branches are temporary, not for permanent separation

### Outcome
All applications live in `apps/` folder, share `shared/` utilities.

**Repository Structure:**
```
Frames-App/
├── apps/
│   ├── onboarding-lms/
│   ├── research-analytics/
│   └── ai-core/
├── shared/
│   └── database/
├── docs/
└── scripts/
```

---

## Decision 2: Database Provider (Neon vs. Alternatives)

**Date:** November 25, 2025
**Status:** ✅ Decided - Neon PostgreSQL

### Context
Needed a PostgreSQL database for development and production.

### Decision
Use **Neon PostgreSQL** (cloud-hosted, serverless).

### Rationale
**Pros of Neon:**
- Serverless (auto-scales)
- No infrastructure management
- Fast setup
- Built-in backups
- Connection pooling

**Cons:**
- External dependency
- Potential cold starts
- Data sovereignty concerns (hosted in US/EU)

**Alternatives Considered:**
1. **Local PostgreSQL**
   - Rejected: Each developer needs to install, hard to share data
2. **Docker PostgreSQL**
   - Rejected: Adds Docker dependency, slower on Windows
3. **SQLite**
   - Rejected: Not production-ready, no concurrent writes, limited scale

### Outcome
Neon connection string stored in `.env`:
```
DATABASE_URL=postgresql://user:pass@ep-...neon.tech/frames_db?sslmode=require
```

---

## Decision 3: Frontend Framework (React vs. Vue vs. Svelte)

**Date:** November 26, 2025
**Status:** ✅ Decided - React 18

### Context
Needed a modern frontend framework for interactive, mobile-first LMS.

### Decision
Use **React 18** with **Material-UI** (Vision UI Dashboard theme).

### Rationale
**Pros of React:**
- Largest ecosystem (more libraries for sandbox, games, 3D)
- Excellent TypeScript support
- Material-UI mature and well-documented
- Team familiarity (assumed)
- Best mobile performance
- React Native path for future native apps

**Cons:**
- Larger bundle size than Svelte
- More verbose than Vue
- Hooks learning curve

**Alternatives Considered:**
1. **Vue 3**
   - Pros: Simpler syntax, smaller bundle
   - Cons: Fewer game/3D libraries, smaller ecosystem
2. **Svelte**
   - Pros: Smallest bundle, fastest runtime
   - Cons: Immature ecosystem for complex interactions
3. **Vanilla JavaScript**
   - Rejected: Too much boilerplate, hard to maintain

### Outcome
React app created with Vision UI Dashboard template for professional look.

---

## Decision 4: Vision UI Dashboard vs. Custom UI

**Date:** November 26, 2025
**Status:** ✅ Decided - Vision UI Dashboard (with modifications)

### Context
Needed a polished UI quickly. Could build from scratch or use template.

### Decision
Use **Vision UI Dashboard React** template, customize for LMS needs.

### Rationale
**Pros:**
- Professional design out of the box
- Material-UI components ready
- Dark theme (modern, less eye strain)
- Responsive (works on mobile)
- Saves ~40 hours of UI development
- Charts/analytics components included

**Cons:**
- Some unused features (billing, RTL, etc.)
- Sidebar not ideal for mobile modules
- Need to customize heavily

**Plan:**
- Keep dashboard structure for admin/instructor views
- Remove sidebar for student module viewing (fullscreen)
- Reuse components (cards, buttons, typography)

### Outcome
Template copied to `apps/onboarding-lms/frontend-react/`, customizations in progress.

---

## Decision 5: Sidebar for Module Viewing (Keep vs. Remove)

**Date:** November 26, 2025
**Status:** 🚧 In Progress - Leaning toward Remove

### Context
Vision UI Dashboard has persistent sidebar. Students use tablets for onboarding.

### Decision
**Remove sidebar during module viewing** for fullscreen, immersive experience.

### Rationale
**Why Remove:**
- Tablets have limited screen space (10-13")
- Sidebar wastes 200-250px on every page
- Students don't need navigation during modules (linear flow)
- Touch targets easier with more space
- Reduces cognitive load (fewer distractions)
- Kiosk mode: students shouldn't skip modules

**Why Keep:**
- Easy access to other modules
- Progress overview visible
- Consistent with dashboard

**Compromise:**
- Keep sidebar on module library (browsing)
- Remove sidebar during module viewing
- Add "Back to Modules" button in module header

### Status
**To be implemented in Phase 1.**

---

## Decision 6: Flask vs. FastAPI for Backend

**Date:** November 25, 2025
**Status:** ✅ Decided - Flask

### Context
Needed Python web framework for REST API.

### Decision
Use **Flask** with SQLAlchemy ORM.

### Rationale
**Pros of Flask:**
- Simpler for straightforward CRUD APIs
- Team likely familiar
- Extensive documentation
- SQLAlchemy integration mature
- Easier to debug

**Cons:**
- Slower than FastAPI (not async)
- Less modern
- No automatic API docs (unlike FastAPI's Swagger)

**Alternatives Considered:**
1. **FastAPI**
   - Pros: Async, automatic docs, type hints
   - Cons: More complex, overkill for current needs
   - **Reconsider if:** AI buddy needs async, many concurrent users
2. **Django REST Framework**
   - Rejected: Too heavy, includes ORM and admin (not needed)

### Outcome
Flask API at `http://localhost:5001`, serves JSON for React.

**Future:** May migrate to FastAPI in Phase 5 for AI buddy async handling.

---

## Decision 7: Text Modules First, Interactive Later

**Date:** November 26, 2025
**Status:** ✅ Decided - Phased Approach

### Context
Could build all module types simultaneously or incrementally.

### Decision
**Phase 0:** Text modules only (orientation, safety, policies)
**Phase 1:** Add infrastructure for other types
**Phase 2+:** Add interactive, sandbox, game, guided struggle

### Rationale
**Why Phased:**
- Text modules have immediate value (policies, safety)
- Proves core system (progress tracking, navigation, analytics)
- Reduces complexity for initial launch
- Lets us test with real students before investing in complex features
- Easier to debug if only one type exists

**Risk:**
- Students might find text-only boring
- Team leads might not see value until interactive modules exist

**Mitigation:**
- Launch with 5-7 well-designed text modules (not just walls of text)
- Add one interactive prototype in Phase 2 to show potential
- Use text modules to collect baseline data for adaptive system

### Outcome
"Lab Safety 101" created as first text module. Infrastructure for types planned.

---

## Decision 8: Client-Side vs. Server-Side Code Execution

**Date:** November 26, 2025
**Status:** 🔴 Not Yet Decided - Needs Discussion

### Context
For sandbox modules, students will write and run code. Need to decide where code executes.

### Options

#### Option A: Client-Side (Pyodide)
**How:** Python runs in browser via WebAssembly.

**Pros:**
- No backend infrastructure
- No security concerns (sandboxed by browser)
- Fast execution (after initial load)
- Works offline

**Cons:**
- 5-10s initial load (WASM download)
- Limited libraries (only what Pyodide includes)
- Memory constraints
- Large bundle size (~6 MB)

#### Option B: Server-Side (Docker Containers)
**How:** Student code sent to Flask, executed in isolated Docker container.

**Pros:**
- Full Python capabilities
- All libraries available
- No client performance impact
- Smaller frontend bundle

**Cons:**
- Complex infrastructure (Docker, orchestration)
- Security risk (need sandboxing)
- Latency (network round trip)
- Costs (server compute)

#### Option C: Hybrid
**How:** Simple scripts run client-side, complex ones run server-side.

**Decision Needed:**
- What types of code will students write?
  - Simple scripts (10-20 lines)? → Client-side
  - Data analysis (NumPy, Pandas)? → Server-side
  - Web scraping, file I/O? → Server-side

**Recommendation:**
Start with **Pyodide (client-side)** for Phase 3:
- Simpler to implement
- Good for intro Python modules
- Can add server-side in Phase 6+ if needed

**Action:** Decide based on curriculum needs.

---

## Decision 9: AI Buddy Implementation (Claude API vs. Open Source)

**Date:** November 26, 2025
**Status:** 🟡 Tentative - Claude API

### Context
Need conversational AI for guided struggle modules.

### Decision (Tentative)
Use **Anthropic Claude API** (Claude 3 Sonnet or Haiku).

### Rationale
**Pros of Claude:**
- Best-in-class conversational ability
- Follows complex instructions well
- Context window (200K tokens)
- Reliable, low hallucination
- Easy API integration
- Cost-effective (~$0.003/message)

**Cons:**
- Requires API key
- Ongoing costs ($30-100/month estimated)
- Internet dependency
- Data sent to third party

**Alternatives Considered:**
1. **OpenAI GPT-4**
   - Similar quality, slightly more expensive
   - More mainstream, easier to explain
2. **Open Source (Llama 3, Mistral)**
   - Pros: No API costs, full control
   - Cons: Need GPU server, worse quality, harder to maintain
3. **No AI Buddy**
   - Rejected: Misses core value prop of adaptive coaching

### Plan
1. Start with Claude API in Phase 5
2. Monitor costs and quality
3. Reconsider self-hosted if costs exceed $200/month

**Budget Estimate:**
- 10,000 messages/month = $30
- 50,000 messages/month = $150
- Typical: 2-5 messages per struggle module per student

---

## Decision 10: Analytics Approach (Custom vs. Third-Party)

**Date:** November 26, 2025
**Status:** ✅ Decided - Custom Analytics

### Context
Need detailed interaction tracking for adaptive system.

### Decision
Build **custom analytics system** with `module_analytics_events` table.

### Rationale
**Why Custom:**
- Need granular control (track specific interactions)
- Adaptive engine needs real-time access to data
- Can log anything (clicks, pauses, errors, retries)
- No privacy concerns (data stays in our database)
- No recurring costs

**Why Not Google Analytics:**
- Too coarse-grained (page views, sessions)
- Real-time querying difficult
- Privacy concerns (sends data to Google)
- Can't feed into adaptive engine easily

**Compromise:**
- Custom analytics for adaptive system
- *Optional* Google Analytics for overall traffic (later)

### Outcome
Every interaction emits event to `/api/analytics/event`, stored in `module_analytics_events` table.

**Example Events:**
- `section_view`, `section_complete`, `pause`, `resume`
- `code_run`, `error_encountered`, `hint_used`
- `hotspot_click`, `game_start`, `buddy_message`

---

## Decision 11: Progressive Web App (PWA) vs. Native Apps

**Date:** November 26, 2025
**Status:** 🟡 Tentative - PWA First, Native Later

### Context
Students use tablets and phones. Need mobile strategy.

### Decision
**Phase 1-7:** Progressive Web App (PWA)
**Phase 10:** Consider native iOS/Android apps

### Rationale
**Why PWA First:**
- One codebase (React)
- Works on all devices (iOS, Android, desktop)
- No app store approval
- Instant updates
- Can install to home screen
- Offline capable (service workers)
- Touch-optimized React works great

**Why Not Native First:**
- Double development (iOS + Android)
- App store friction (reviews, updates)
- Not needed for kiosk tablets
- PWA sufficient for MVP

**When to Consider Native:**
- Need device features (camera, AR, NFC)
- Offline mode critical
- App store discovery important
- Push notifications essential

### Plan
1. Build PWA with React
2. Test on iPads at kiosk stations
3. Add to home screen for easy access
4. Evaluate native app need after 6 months

---

## Open Questions / Undecided

### Question 1: Hosting Strategy
**Options:**
- Vercel (frontend) + Heroku (backend)
- AWS (EC2 + S3 + RDS)
- Google Cloud Run
- Render (full-stack)

**Status:** Not decided yet. Current: localhost only.
**Timeline:** Decide by Phase 2 for pilot testing.

### Question 2: Authentication System
**Options:**
- University SSO (SAML, OAuth)
- Email/password (custom)
- Magic links (passwordless)
- No auth (kiosk mode)

**Status:** Not decided yet. Current: no authentication.
**Timeline:** Decide by Phase 3 if tracking individual students.

### Question 3: Content Management
**Options:**
- Build custom module builder (Phase 7)
- Use headless CMS (Strapi, Contentful)
- Markdown files + Git

**Status:** Leaning toward custom builder.
**Timeline:** Decide by Phase 6.

---

## Decision Review Schedule

**Quarterly Reviews:**
- Q1 2026: Review Phase 1-3 decisions
- Q2 2026: Review Phase 4-5 decisions
- Q3 2026: Review hosting, auth, scaling decisions

**Criteria for Revision:**
- User feedback contradicts assumptions
- Technology becomes unavailable
- Costs exceed budget
- Better alternative emerges
