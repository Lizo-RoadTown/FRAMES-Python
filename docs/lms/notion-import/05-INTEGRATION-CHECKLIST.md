# Integration Checklist - External Frameworks & APIs

**Purpose:** Track frameworks to integrate from GitHub and external APIs needed for full LMS functionality.

---

## Framework Integration Status

### 1. Code Sandbox Integration

**Purpose:** Allow students to write and execute code in the browser.

#### Option A: Monaco Editor (Recommended)
**GitHub:** https://github.com/microsoft/monaco-editor
**React Wrapper:** https://github.com/suren-atoyan/monaco-react

**Status:** 🟡 Pending

**Installation:**
```bash
npm install @monaco-editor/react
```

**Features:**
- Full VS Code editor engine
- Syntax highlighting for 50+ languages
- IntelliSense (autocomplete)
- Error markers
- Multi-file support

**Integration Tasks:**
- [ ] Install package
- [ ] Create `SandboxViewer` component
- [ ] Configure language (Python, JavaScript)
- [ ] Add "Run Code" button
- [ ] Display output panel
- [ ] Handle errors gracefully
- [ ] Save/restore code state
- [ ] Mobile touch optimization

**Alternatives:**
- CodeMirror 6 (lighter weight)
- Ace Editor (older, still maintained)

---

#### Option B: Python Execution (Pyodide)
**GitHub:** https://github.com/pyodide/pyodide
**Purpose:** Run Python in the browser (no backend needed)

**Status:** 🟡 Pending

**Installation:**
```bash
npm install pyodide
```

**Features:**
- Full Python 3.11 in WebAssembly
- NumPy, Pandas, SciPy support
- No server needed
- Runs client-side

**Integration Tasks:**
- [ ] Install Pyodide
- [ ] Create Python runtime wrapper
- [ ] Handle async execution
- [ ] Capture stdout/stderr
- [ ] Display execution time
- [ ] Add loading indicator (slow first load)
- [ ] Cache WASM files

**Trade-offs:**
- **Pros:** No backend infrastructure, fast for simple code
- **Cons:** 5-10s initial load, limited libraries, memory constraints

---

### 2. 3D/Interactive Environments

**Purpose:** Create explorable virtual environments (lab tours, equipment visualization).

#### Option A: Three.js (Recommended)
**GitHub:** https://github.com/mrdoob/three.js
**React Wrapper:** https://github.com/pmndrs/react-three-fiber

**Status:** 🟡 Pending

**Installation:**
```bash
npm install three @react-three/fiber @react-three/drei
```

**Features:**
- Full 3D rendering
- Touch controls
- Physics (optional)
- Model loading (.gltf, .obj)
- Lighting, shadows, effects

**Integration Tasks:**
- [ ] Install packages
- [ ] Create `Interactive3DViewer` component
- [ ] Add camera controls (touch-friendly)
- [ ] Load 3D models
- [ ] Add clickable hotspots
- [ ] Implement raycasting (click detection)
- [ ] Optimize performance for mobile
- [ ] Add loading screen

**Use Cases:**
- Virtual lab walkthrough
- Equipment inspection
- Assembly visualization
- Spatial navigation

---

#### Option B: 2D Interactive Maps/Diagrams
**Purpose:** Simpler alternative for 2D clickable environments.

**Libraries:**
- React Image Hotspots (custom)
- Leaflet.js (for maps)
- Fabric.js (canvas manipulation)

**Status:** 🟡 Pending (decide based on content needs)

**Integration Tasks:**
- [ ] Choose library
- [ ] Create clickable image component
- [ ] Add hotspot markers
- [ ] Implement tooltips/popovers
- [ ] Track clicks for analytics
- [ ] Mobile touch optimization

---

### 3. Game Engine Integration

**Purpose:** Speed drills, pattern matching, score-based challenges.

#### Option A: Phaser 3 (Recommended)
**GitHub:** https://github.com/photonstorm/phaser
**React Integration:** Custom wrapper

**Status:** 🟡 Pending

**Installation:**
```bash
npm install phaser
```

**Features:**
- 2D game engine
- Physics system
- Sprite management
- Touch/mouse input
- Audio support
- Tilemaps

**Integration Tasks:**
- [ ] Install Phaser
- [ ] Create `GameViewer` component
- [ ] Initialize Phaser canvas
- [ ] Handle React lifecycle
- [ ] Build first game (matching)
- [ ] Add scoring system
- [ ] Implement timer
- [ ] Mobile touch controls
- [ ] Cleanup on unmount

**Use Cases:**
- Symbol matching drill
- Fast sorting game
- Reaction time tests
- Pattern recognition

---

#### Option B: PixiJS (Lighter Alternative)
**GitHub:** https://github.com/pixijs/pixijs

**Status:** 🟡 Pending

**Features:**
- 2D WebGL rendering
- Sprites and textures
- Particle effects
- Lightweight (~400KB)

**Trade-offs:**
- **Pros:** Faster load, smaller bundle
- **Cons:** Less built-in game logic (physics, tilemaps)

---

### 4. Drag-and-Drop Systems

**Purpose:** Interactive assembly, sorting, organization tasks.

#### React DnD (Recommended)
**GitHub:** https://github.com/react-dnd/react-dnd

**Status:** 🟡 Pending

**Installation:**
```bash
npm install react-dnd react-dnd-html5-backend react-dnd-touch-backend
```

**Features:**
- Drag-drop primitives
- Touch backend for mobile
- Drop zones
- Custom drag previews

**Integration Tasks:**
- [ ] Install packages
- [ ] Create draggable components
- [ ] Create drop zones
- [ ] Add touch backend for mobile
- [ ] Implement snap-to-grid (optional)
- [ ] Validate correct placements
- [ ] Add visual feedback
- [ ] Track for analytics

**Use Cases:**
- Equipment assembly
- Block diagram building
- Task sequencing
- Categorization drills

---

#### Alternative: dnd-kit
**GitHub:** https://github.com/clauderic/dnd-kit

**Features:**
- Modern, TypeScript-first
- Better performance
- Built-in accessibility

**Status:** 🟡 Consider if React DnD has issues

---

### 5. Animation & Transitions

**Purpose:** Smooth transitions, micro-interactions, visual polish.

#### Framer Motion (Recommended)
**GitHub:** https://github.com/framer/motion
**Already in Vision UI:** Check if included

**Status:** 🟡 Pending (may already be available)

**Installation:**
```bash
npm install framer-motion
```

**Features:**
- Declarative animations
- Gesture support
- Layout animations
- Scroll-triggered effects

**Integration Tasks:**
- [ ] Check if already installed
- [ ] Add to module transitions
- [ ] Animate progress bar
- [ ] Add hover/tap feedback
- [ ] Page transitions

---

## API Integration Status

### 1. Anthropic Claude API (AI Cohort Buddy)

**Purpose:** Conversational AI peer coach for guided struggle.

**Status:** 🔴 Not Started (need API key)

**Setup:**
```bash
pip install anthropic
```

**Integration Tasks:**
- [ ] Obtain API key from Anthropic
- [ ] Store in `.env` securely
- [ ] Create `/api/buddy/chat` endpoint
- [ ] Implement conversation context
- [ ] Add rate limiting (prevent abuse)
- [ ] Create chat UI component
- [ ] Test response quality
- [ ] Add fallback for API errors
- [ ] Monitor usage/costs

**Configuration:**
```python
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

**Estimated Cost:**
- ~$0.003 per message (Claude 3 Sonnet)
- 100 messages = $0.30
- 10,000 messages = $30

---

### 2. Neon PostgreSQL (Database)

**Status:** ✅ Complete

**Current:**
- Connection configured
- All tables created
- Sample data exists

**No further action needed.**

---

### 3. GitHub API (Optional)

**Purpose:** Sync documentation, pull repos, version control integration.

**Status:** 🟡 Future consideration

**Possible Uses:**
- Auto-import code examples from repos
- Link modules to GitHub issues
- Track module versions

---

### 4. Google Analytics or Mixpanel (Optional)

**Purpose:** User behavior analytics beyond custom system.

**Status:** 🟡 Future consideration

**Trade-offs:**
- **Pros:** Industry-standard, built-in dashboards
- **Cons:** Less granular than custom analytics

---

## Framework Selection Priority

### Immediate (Phase 1-2)
1. **Drag-Drop Library** (React DnD) - Easiest interactive module
2. **Framer Motion** - Polish existing UI

### Short-term (Phase 3)
3. **Monaco Editor** - Code sandbox
4. **Pyodide** - Python execution

### Medium-term (Phase 4-5)
5. **Phaser** - Game modules
6. **Anthropic API** - AI buddy

### Long-term (Phase 6+)
7. **Three.js** - Advanced 3D (if needed)

---

## Installation Order

Once you provide GitHub repos, we'll install in this order:

**Week 1:**
```bash
npm install framer-motion
npm install react-dnd react-dnd-html5-backend react-dnd-touch-backend
```

**Week 2:**
```bash
npm install @monaco-editor/react
npm install pyodide
```

**Week 3:**
```bash
npm install phaser
pip install anthropic
```

**Week 4:**
```bash
npm install three @react-three/fiber @react-three/drei
```

---

## Testing Requirements

Each integration needs:
- [ ] Installed without errors
- [ ] Works on desktop browser
- [ ] Works on mobile/tablet
- [ ] Touch controls functional
- [ ] Performance acceptable (<2s load)
- [ ] Bundle size impact measured
- [ ] Documented in code
- [ ] Example module created

---

## Bundle Size Considerations

**Current React App:** ~2-3 MB

**Impact of Additions:**
- Monaco Editor: +1.2 MB
- Pyodide: +6 MB (first load only, cached)
- Phaser: +800 KB
- Three.js: +600 KB
- React DnD: +100 KB
- Framer Motion: +150 KB

**Total Estimated:** ~11 MB (with all frameworks)

**Mitigation:**
- Lazy load modules (only load when needed)
- Code splitting by module type
- Cache aggressively
- Consider CDN for large libraries

---

## Security Considerations

### Code Execution (Sandbox)
- ⚠️ **Risk:** User-submitted code could be malicious
- **Mitigation:**
  - Use Pyodide (client-side, sandboxed)
  - If backend execution, use Docker containers
  - Limit execution time (5s max)
  - Restrict imports/APIs
  - No file system access

### AI API
- ⚠️ **Risk:** API key exposure, prompt injection
- **Mitigation:**
  - Store key in environment variables
  - Never send to frontend
  - Rate limit per student (10 messages/hour)
  - Filter sensitive content
  - Log all interactions

### Asset Uploads (Future)
- ⚠️ **Risk:** Malicious files (XSS, viruses)
- **Mitigation:**
  - Validate file types
  - Scan for malware
  - Serve from separate domain
  - Content Security Policy headers

---

## Next Steps

1. **You provide:** GitHub repos you've identified for each category
2. **I'll evaluate:** Suitability, bundle size, mobile support
3. **We'll install:** One at a time, starting with drag-drop
4. **We'll test:** Create example module for each type
5. **We'll document:** Best practices for each framework

**Ready to proceed once you have the GitHub repos!**
