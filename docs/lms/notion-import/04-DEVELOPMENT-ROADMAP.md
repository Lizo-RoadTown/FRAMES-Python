# FRAMES LMS - Development Roadmap

**Last Updated:** November 26, 2025
**Current Phase:** Phase 0 → Phase 1 Transition

---

## Phase 0: Foundation ✅ COMPLETE

**Timeline:** Completed November 26, 2025
**Goal:** Basic text-based module system operational

### Completed Tasks
- [x] Set up monorepo structure
- [x] Configure Neon PostgreSQL database
- [x] Create 6 LMS database tables
- [x] Build Flask REST API backend
- [x] Implement React frontend (Vision UI Dashboard)
- [x] Create module library page (card grid)
- [x] Create text module viewer (navigation, progress bar)
- [x] Add sample "Lab Safety 101" module
- [x] Implement basic progress tracking
- [x] Set up CORS for React ↔ Flask communication

### Deliverables
- ✅ Working LMS at http://localhost:3000
- ✅ Flask API at http://localhost:5001
- ✅ Sample module viewable
- ✅ Database schema documented

---

## Phase 1: Mobile Optimization & Module Types 🚧 IN PROGRESS

**Target:** Week of November 25, 2025
**Goal:** Clean mobile UI + infrastructure for interactive modules

### Priority Tasks

#### 1.1 Mobile UI Cleanup (High Priority)
**Estimate:** 2-3 hours

- [ ] Remove sidebar from module library page
- [ ] Remove sidebar from module viewer page
- [ ] Create fullscreen, touch-optimized layouts
- [ ] Test on tablet (iPad/Android 10-13")
- [ ] Ensure landscape + portrait work
- [ ] Optimize button sizes for touch (min 44px)

**Rationale:** Students use tablets at kiosks. Sidebar wastes space and adds navigation friction.

#### 1.2 Database Schema Extensions (High Priority)
**Estimate:** 1 hour + testing

```sql
-- Add module type system
ALTER TABLE modules ADD COLUMN module_type VARCHAR(50) DEFAULT 'text';
ALTER TABLE modules ADD COLUMN interaction_level VARCHAR(20);
ALTER TABLE modules ADD COLUMN required_components JSON DEFAULT '[]';

-- Add section configs
ALTER TABLE module_sections ADD COLUMN section_config JSON;
ALTER TABLE module_sections ADD COLUMN completion_criteria JSON;

-- Add struggle tracking
ALTER TABLE module_progress ADD COLUMN hint_count INTEGER DEFAULT 0;
ALTER TABLE module_progress ADD COLUMN retry_count INTEGER DEFAULT 0;
ALTER TABLE module_progress ADD COLUMN error_count INTEGER DEFAULT 0;
```

**Tasks:**
- [ ] Update `db_models.py` with new fields
- [ ] Create migration script
- [ ] Run migration on Neon database
- [ ] Update `to_dict()` methods in models
- [ ] Test with existing "Lab Safety 101" module

#### 1.3 Component Loader System (High Priority)
**Estimate:** 3-4 hours

- [ ] Create `ModuleRenderer` component that switches based on `section_type`
- [ ] Implement type registry: `{text: TextViewer, sandbox: SandboxViewer, ...}`
- [ ] Update module viewer to use dynamic renderer
- [ ] Create placeholder components for each type
- [ ] Test switching between types in one module

**Files to Create:**
- `src/components/ModuleRenderer.js`
- `src/components/viewers/TextViewer.js`
- `src/components/viewers/SandboxViewer.js` (placeholder)
- `src/components/viewers/GameViewer.js` (placeholder)
- `src/components/viewers/InteractiveViewer.js` (placeholder)

#### 1.4 Update API Endpoints (Medium Priority)
**Estimate:** 1 hour

- [ ] Modify `/api/modules` to return `module_type`
- [ ] Modify `/api/modules/<id>` to include `section_config`
- [ ] Add validation for type-specific configs
- [ ] Update sample module script to use new fields

**Deliverables by End of Phase 1:**
- Clean, mobile-first UI (no sidebar during modules)
- Database ready for all module types
- Component system that can load different viewers
- At least one test module of each type (even if placeholder)

---

## Phase 2: First Interactive Module 🎯 NEXT

**Target:** Early December 2025
**Goal:** One fully functional interactive module

### Priority: Interactive Module (Easiest to Implement)

#### 2.1 Choose First Interactive Module
**Options:**
1. **"Virtual Lab Tour"** (recommended)
   - 2D clickable image/map
   - Hotspots with tooltips
   - Simple tasks (click 5 areas)
   - Low tech complexity

2. **"Subsystem Explorer"**
   - Block diagram with clickable nodes
   - Info cards for each subsystem
   - Connection visualization

3. **"Equipment Assembly"**
   - Drag-and-drop simple items
   - Snap-to-grid mechanic
   - Check correct placement

**Decision needed:** Which to build first?

#### 2.2 Integrate Interactive Framework
**Estimate:** 4-6 hours (once framework chosen from GitHub)

**Tasks:**
- [ ] Install framework via npm (e.g., `react-dnd`, `framer-motion`)
- [ ] Create `InteractiveViewer.js` component
- [ ] Build hotspot/clickable system
- [ ] Add tooltip/popup functionality
- [ ] Implement task completion tracking
- [ ] Style for mobile/touch

#### 2.3 Create Interactive Module Content
**Estimate:** 3-4 hours

**Tasks:**
- [ ] Design lab layout or diagram
- [ ] Create assets (images, icons)
- [ ] Define hotspots and tasks
- [ ] Write instructional text
- [ ] Add to database with `section_type: 'interactive'`
- [ ] Test on tablet

#### 2.4 Analytics for Interactive Modules
**Estimate:** 2 hours

**Events to track:**
- `hotspot_click` - Which area clicked
- `task_complete` - Task finished
- `discovery` - Found hidden element
- `time_on_hotspot` - Engagement metric

**Tasks:**
- [ ] Add event emission to `InteractiveViewer`
- [ ] Update analytics API endpoint
- [ ] Test data collection

**Deliverables by End of Phase 2:**
- One complete interactive module
- Tested on tablet
- Analytics working
- Documented for replication

---

## Phase 3: Sandbox Module 💻 HIGH VALUE

**Target:** Mid-December 2025
**Goal:** Students can practice coding in browser

### Priority: Code Sandbox (Monaco Editor)

#### 3.1 Integrate Monaco Editor
**Estimate:** 6-8 hours

**Tasks:**
- [ ] Install `@monaco-editor/react`
- [ ] Create `SandboxViewer.js` component
- [ ] Configure Python syntax highlighting
- [ ] Add file browser (if multi-file)
- [ ] Implement "Run Code" button
- [ ] Display output/errors

#### 3.2 Backend Code Execution
**Estimate:** 8-10 hours (complex!)

**Options:**
1. **Client-side Python (Pyodide)**
   - Runs Python in browser via WebAssembly
   - No backend needed
   - Limited libraries
   - Slower startup

2. **Sandboxed Backend Execution**
   - Docker containers
   - Security sandboxing
   - Full Python capabilities
   - More infrastructure

**Decision needed:** Client-side (faster) or backend (more powerful)?

#### 3.3 Create Sandbox Modules
**Estimate:** 4-6 hours

**Example Modules:**
1. "Hello World in Python"
2. "Fix the Bug"
3. "Complete the Function"
4. "Write a Test"

**Tasks:**
- [ ] Write module content and instructions
- [ ] Create starter code
- [ ] Define expected output
- [ ] Add validation logic
- [ ] Test on tablet

#### 3.4 Sandbox Analytics
**Events:**
- `code_run` - Code executed
- `error_encountered` - Compilation/runtime error
- `code_change` - Edit made
- `hint_used` - Help requested
- `test_passed` - Correct solution

**Deliverables by End of Phase 3:**
- Working code sandbox
- 3-5 coding modules
- Error handling
- Progress tracking

---

## Phase 4: Game Module 🎮 MOTIVATION

**Target:** Late December 2025
**Goal:** Gamified drills for speed/accuracy

### Priority: Pattern Matching Game

#### 4.1 Integrate Game Framework
**Estimate:** 6-8 hours

**Options:**
- Phaser.js (full game engine)
- PixiJS (rendering library)
- Custom React + Canvas

**Tasks:**
- [ ] Install game framework
- [ ] Create `GameViewer.js` component
- [ ] Build timer system
- [ ] Add scoring logic
- [ ] Implement replay functionality
- [ ] Touch-optimize controls

#### 4.2 Create Game Modules
**Examples:**
1. "Subsystem Matching" - Match names to diagrams
2. "Fast Parameter Sort" - Sort items by category
3. "Error Code Memory" - Match codes to meanings

**Tasks:**
- [ ] Design game mechanics
- [ ] Create game assets (sprites, sounds)
- [ ] Implement difficulty levels
- [ ] Add scoring algorithm
- [ ] Test balance (not too hard/easy)

#### 4.3 Leaderboard (Optional)
**Estimate:** 3-4 hours

- [ ] Create leaderboard table
- [ ] Display top scores
- [ ] Add filters (by team, by university)
- [ ] Privacy settings

**Deliverables by End of Phase 4:**
- 2-3 working games
- Adjustable difficulty
- Score tracking
- Leaderboard (optional)

---

## Phase 5: AI Cohort Buddy 🤖 COMPLEX

**Target:** January 2026
**Goal:** Conversational AI peer coach

### Priority: Guided Struggle Integration

#### 5.1 Anthropic Claude API Setup
**Estimate:** 4-6 hours

**Tasks:**
- [ ] Get API key from Anthropic
- [ ] Add `anthropic` Python library
- [ ] Create `/api/buddy/chat` endpoint
- [ ] Implement conversation context management
- [ ] Add rate limiting
- [ ] Test responses

#### 5.2 Buddy Chat UI
**Estimate:** 6-8 hours

**Tasks:**
- [ ] Create chat component
- [ ] Add message history
- [ ] Implement typing indicator
- [ ] Style for mobile
- [ ] Add quick reply suggestions
- [ ] Test accessibility

#### 5.3 Context-Aware Prompts
**Estimate:** 8-10 hours

**Buddy needs to know:**
- Current module and section
- Student's progress history
- Recent errors/struggles
- Current task
- Personality mode

**Tasks:**
- [ ] Build context builder
- [ ] Write system prompts for different scenarios
- [ ] Implement personality modes
- [ ] Test coherence across conversation
- [ ] Add safety filters

#### 5.4 Create Guided Struggle Modules
**Examples:**
1. "Debug Your First Error"
2. "Choose the Right Tool"
3. "Diagnose System Behavior"

**Tasks:**
- [ ] Design problem scenarios
- [ ] Create hint progression
- [ ] Define success criteria
- [ ] Add buddy trigger points
- [ ] Test with students

**Deliverables by End of Phase 5:**
- Working AI chat interface
- Context-aware responses
- 2-3 guided struggle modules
- Analytics on buddy interactions

---

## Phase 6: Adaptive Difficulty 📈 ADVANCED

**Target:** February 2026
**Goal:** System adjusts to student struggle

### Components

#### 6.1 Struggle Signal Detection
**Estimate:** 10-12 hours

**Signals:**
- Long pauses (>60s)
- Multiple retries
- Hint usage frequency
- Error patterns
- Time vs. expected

**Tasks:**
- [ ] Implement signal calculators
- [ ] Create struggle score (0.00-1.00)
- [ ] Add to analytics events
- [ ] Test accuracy

#### 6.2 Adaptive Engine
**Estimate:** 12-15 hours

**Adjustments:**
- Difficulty level (easier/harder)
- Scaffolding (more/less help)
- Content path (skip/review)
- Pace (slow down/speed up)

**Tasks:**
- [ ] Design decision tree
- [ ] Implement adjustment logic
- [ ] Add config to modules
- [ ] Test with various struggle levels
- [ ] Prevent gaming the system

#### 6.3 Personalized Pathways
**Estimate:** 8-10 hours

**Tasks:**
- [ ] Create prerequisite system
- [ ] Implement skill tree
- [ ] Add branching logic
- [ ] Design UI for path visualization
- [ ] Test multiple pathways

**Deliverables by End of Phase 6:**
- Live adaptive difficulty
- Personalized module sequences
- Analytics dashboard showing adaptations
- A/B testing framework

---

## Phase 7: Module Builder Interface 🛠️ CONTENT CREATION

**Target:** March 2026
**Goal:** Instructors can create modules without coding

### Components

#### 7.1 Module Authoring UI
**Estimate:** 20-25 hours

**Features:**
- Module metadata form
- Section builder (drag-drop)
- Type selector (text, sandbox, game, etc.)
- Preview mode
- Save as draft/publish

**Tasks:**
- [ ] Design UI mockups
- [ ] Build form components
- [ ] Add validation
- [ ] Implement preview
- [ ] Test with real instructors

#### 7.2 Asset Management
**Estimate:** 8-10 hours

**Tasks:**
- [ ] Create asset upload system
- [ ] Organize asset library
- [ ] Add image/video preview
- [ ] Implement CDN integration (optional)

#### 7.3 Template Library
**Estimate:** 6-8 hours

**Templates:**
- Text module template
- Interactive tour template
- Sandbox challenge template
- Game template
- Guided struggle template

**Tasks:**
- [ ] Create reusable templates
- [ ] Add customization options
- [ ] Build template selector UI
- [ ] Test duplication and modification

**Deliverables by End of Phase 7:**
- Full module builder
- Template library
- Documentation for creators
- Video tutorial

---

## Future Phases (Post-Launch)

### Phase 8: Advanced Analytics
- Predictive modeling (who will struggle?)
- Cohort comparisons
- Intervention recommendations
- Export capabilities

### Phase 9: Social Features
- Peer discussion forums
- Collaborative modules
- Team challenges
- Study groups

### Phase 10: Mobile App
- Native iOS/Android apps
- Offline mode
- Push notifications
- Native camera/AR features

---

## Dependencies & Blockers

### External Dependencies
- GitHub repositories with interactive frameworks (awaiting selection)
- Anthropic API access (need API key)
- Team lead availability for testing
- Student cohort for pilot testing

### Technical Blockers
- None currently identified
- Mobile UI should be prioritized to unlock further work

### Resource Needs
- Designer for visual assets (optional, can use placeholders)
- Instructional designer for content (you can handle)
- Students for user testing (pilot cohort needed)

---

## Success Metrics by Phase

### Phase 1
- Mobile UI loads in <2s
- Component system works for all types
- No regressions on existing features

### Phase 2
- Interactive module completion rate >80%
- Average time on task 8-12 minutes
- Student feedback rating >4/5

### Phase 3
- Sandbox module completion rate >70%
- Error recovery rate >60% (students fix errors without skipping)
- Code submission count >3 per module

### Phase 4
- Game replay rate >40% (students want to improve score)
- Difficulty progression works (students advance levels)
- No rage quits (<5% abandon mid-game)

### Phase 5
- AI response time <3s
- Conversation coherence score >4/5
- Students use hints 2-4 times per module (sweet spot)

### Phase 6-7
- Adaptive adjustments improve completion rates by 15%
- Instructors can create module in <2 hours
- Module quality ratings improve over time
