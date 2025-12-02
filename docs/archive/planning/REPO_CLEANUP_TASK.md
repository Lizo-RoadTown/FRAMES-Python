# Repository Cleanup & Documentation Structuring

**Task ID:** INFRA-001
**Assigned To:** Agent Gamma
**Priority:** Medium
**Estimated Duration:** 3-4 hours
**Status:** Pending

---

## 🎯 Goal

Organize the repository into a clean, professional structure separating:
- The **three product applications** (Researcher Dashboard, Team Lead Tool, Onboarding App)
- The **swarm/experimental system** (three-agent coordination)
- The **infrastructure/platform** (devcontainer, CI/CD, deployment)
- **Data, exports, and third-party libraries**

Ensure each of the three apps has basic documentation in place.

---

## 🚨 GLOBAL RULES (DO NOT SKIP)

### 1. Never Commit Secrets
**Do NOT commit:**
- `.env`, `.env.*`
- API keys, Notion tokens, DB URLs
- `.notion_db_id`

**If you see obvious secrets in tracked files:** STOP and add to a report for the user.

### 2. Do Not Delete Anything Irreversible
- Use `git mv` to preserve history
- Only delete:
  - Caches (`__pycache__`, `node_modules/`)
  - Regenerable temp files
- **Never delete:**
  - Source code
  - Documentation
  - Configuration files

### 3. Do Not Modify Third-Party Repos
- Especially: `react-notion-x-master/`
- Move it to `third_party/` but **do not edit internal code**

### 4. Explain Each Non-Trivial Change
- Use `platform/cleanup/CHANGE_LOG.md`
- Document reasoning for every move

### 5. Assume GitHub Codespaces
- Paths, environment, and commands are for Codespaces
- Working directory: `/workspaces/FRAMES-Python`

---

## 📁 Target Directory Structure

```
/ (repo root)
│
├── product/                          # Production applications
│   ├── backend/
│   │   ├── onboarding-lms/          # Student LMS backend
│   │   ├── team-lead-tool/          # PM tool backend
│   │   └── researcher-dashboard/    # Analytics backend
│   ├── frontend/
│   │   ├── onboarding-app/          # Student-facing React app
│   │   ├── team-lead-tool/          # Team lead PM interface
│   │   └── researcher-dashboard/    # Analytics dashboard
│   ├── docs/
│   │   ├── onboarding-app/          # LMS documentation
│   │   ├── team-lead-tool/          # PM tool docs
│   │   ├── researcher-dashboard/    # Analytics docs
│   │   └── shared/                  # Cross-app documentation
│   └── tests/                       # Integration tests
│
├── swarm-lab/                       # Three-agent experimental system
│   ├── agents/                      # Agent scripts & utilities
│   ├── scripts/                     # Automation scripts
│   ├── prompts/                     # Wake-up prompts & templates
│   ├── history/                     # Work queues, team chat logs
│   └── docs/                        # Agent system documentation
│
├── platform/                        # Infrastructure & tooling
│   ├── devcontainer/                # .devcontainer config
│   ├── ci-cd/                       # GitHub Actions workflows
│   ├── cleanup/                     # This cleanup project docs
│   └── infra/                       # Database, deployment scripts
│
├── data/                            # Data files & exports
│   ├── archives/                    # ZIP archives, backups
│   ├── logs/                        # Import logs, sync logs
│   ├── exports/                     # Module exports, JSON dumps
│   └── tmp/                         # Temporary files (gitignored)
│
├── third_party/                     # External dependencies
│   └── react-notion-x-master/       # Vendored React Notion renderer
│
└── README.md                        # Main repo README
```

---

## 🧠 Reasoning Protocol (Apply Before Moving ANY File)

For every file/folder, decide:

1. **Category:** product, swarm, platform, data, third_party, or junk
2. **Intended owner:** researcher dashboard, PM tool, onboarding app, agents, or infra
3. **Ambiguity:** If uncertain → put in shared docs or leave in place + log in `OPEN_QUESTIONS.md`
4. **Check imports:** Don't break Python or React imports silently
5. **Minimal safe change:** Prefer small, reversible steps

**Decision template:**
```md
### File/Folder: <path>
- **Contains:** <brief description>
- **Category guess:** product / swarm / platform / data / third_party
- **Confidence:** high / medium / low
- **Proposed action:** move to <destination> / leave in place / delete
- **Reasoning:** <why>
- **Import check:** <any dependencies?>
```

---

## 📋 Execution Phases

### PHASE 1 — Scan & Map (30 min)

**Objectives:**
- Generate initial directory tree
- Create cleanup tracking files
- Document current state

**Commands:**
```bash
# 1. Generate initial tree snapshot
tree -L 3 -I 'node_modules|__pycache__|.git' > platform/cleanup/INITIAL_TREE.txt

# Or if tree not available:
find . -type d -not -path '*/\.*' -not -path '*/node_modules/*' -not -path '*/__pycache__/*' | head -100 > platform/cleanup/INITIAL_TREE.txt

# 2. Create cleanup tracking files
mkdir -p platform/cleanup
touch platform/cleanup/CHANGE_LOG.md
touch platform/cleanup/OPEN_QUESTIONS.md
touch platform/cleanup/MOVED_FILES.txt
```

**Document each top-level folder:**

Create `platform/cleanup/INITIAL_AUDIT.md`:
```md
# Initial Repository Audit

## Folder: apps/
- Contains: Application code (onboarding-lms)
- Category: product
- Confidence: high
- Notes: Should move to product/

## Folder: docs/
- Contains: Mixed documentation
- Category: product + swarm
- Confidence: medium
- Notes: Need to split by application

## Folder: scripts/
- Contains: Python automation scripts
- Category: swarm + platform
- Confidence: medium
- Notes: Agent scripts vs infra scripts

...
```

**Deliverables:**
- `platform/cleanup/INITIAL_TREE.txt`
- `platform/cleanup/INITIAL_AUDIT.md`
- `platform/cleanup/CHANGE_LOG.md` (empty, ready)
- `platform/cleanup/OPEN_QUESTIONS.md` (empty, ready)

---

### PHASE 2 — Create Target Skeleton (15 min)

**Objectives:**
- Create all target directories
- Move existing infra to platform/

**Commands:**
```bash
# Create product structure
mkdir -p product/backend/{onboarding-lms,team-lead-tool,researcher-dashboard}
mkdir -p product/frontend/{onboarding-app,team-lead-tool,researcher-dashboard}
mkdir -p product/docs/{onboarding-app,team-lead-tool,researcher-dashboard,shared}
mkdir -p product/tests

# Create swarm-lab structure
mkdir -p swarm-lab/{agents,scripts,prompts,history,docs}

# Create platform structure
mkdir -p platform/{devcontainer,ci-cd,infra,cleanup}

# Create data structure
mkdir -p data/{archives,logs,exports,tmp}

# Create third_party
mkdir -p third_party

# Move existing infrastructure
if [ -d .devcontainer ]; then
  git mv .devcontainer platform/devcontainer
  echo "Moved .devcontainer to platform/devcontainer" >> platform/cleanup/CHANGE_LOG.md
fi

if [ -d .github/workflows ]; then
  git mv .github/workflows platform/ci-cd
  echo "Moved .github/workflows to platform/ci-cd" >> platform/cleanup/CHANGE_LOG.md
fi
```

**Log all moves in CHANGE_LOG.md:**
```md
# Repository Cleanup Change Log

## Phase 2: Infrastructure Moves (2025-11-29)

### Moved Files:
- `.devcontainer/` → `platform/devcontainer/`
  - Reason: Consolidate infrastructure
  - Impact: Codespace config may need update

- `.github/workflows/` → `platform/ci-cd/`
  - Reason: Separate CI/CD from code
  - Impact: GitHub Actions paths unchanged (relative)
```

---

### PHASE 3 — Classify & Move Major Blocks (60 min)

#### 3A. Onboarding App (Student LMS)

**What to move:**
- Frontend: `apps/onboarding-lms/frontend-react/` → `product/frontend/onboarding-app/`
- Backend: `backend/lms_routes.py` + related → `product/backend/onboarding-lms/`
- Docs: `docs/lms/`, `docs/onboarding-lms/` → `product/docs/onboarding-app/`

**Commands:**
```bash
# Move frontend
git mv apps/onboarding-lms/frontend-react product/frontend/onboarding-app

# Move backend (if not already structured)
# Check first: ls backend/
# Then move LMS-specific files

# Move docs
git mv docs/lms product/docs/onboarding-app/
git mv docs/onboarding-lms/* product/docs/onboarding-app/
```

**Log reasoning:**
```md
### Onboarding App Moves
- `apps/onboarding-lms/frontend-react/` → `product/frontend/onboarding-app/`
  - Reason: Student-facing LMS application
  - Contains: React app with module player, dashboard
  - Dependencies: backend/lms_routes.py

- `docs/lms/` → `product/docs/onboarding-app/`
  - Reason: LMS-specific documentation
  - Contains: API_REFERENCE.md, ARCHITECTURE.md
```

---

#### 3B. Team Lead PM Tool

**What to move:**
- Docs: `docs/*PM*`, `docs/*NOTION*` → `product/docs/team-lead-tool/`
- Scripts: `scripts/notion_*.py` → Consider if tool-specific or infra

**Commands:**
```bash
# Move PM-related docs
find docs -name "*PM*" -exec git mv {} product/docs/team-lead-tool/ \;
find docs -name "*NOTION*PROJECT*" -exec git mv {} product/docs/team-lead-tool/ \;

# Create app structure (empty for now)
mkdir -p product/frontend/team-lead-tool
mkdir -p product/backend/team-lead-tool
```

**Log:**
```md
### Team Lead PM Tool
- `docs/*PM*` → `product/docs/team-lead-tool/`
  - Reason: Notion project management tool docs
  - Contains: Workflow guides, integration docs

- Created structure for future:
  - `product/frontend/team-lead-tool/` (empty)
  - `product/backend/team-lead-tool/` (empty)
```

---

#### 3C. Researcher Dashboard (Analytics)

**What to move:**
- Docs: `docs/research-analytics/` → `product/docs/researcher-dashboard/`

**Commands:**
```bash
# Move analytics docs
git mv docs/research-analytics product/docs/researcher-dashboard

# Create app structure
mkdir -p product/frontend/researcher-dashboard
mkdir -p product/backend/researcher-dashboard
```

---

### PHASE 4 — Swarm / Agent Isolation (45 min)

**What to move:**
- Agent docs: `AGENT_*.md`, `START_THREE_AGENTS.md`, `AUTONOMOUS_*.md`
- Agent scripts: `scripts/*agent*.py`, `shared/agent_utils.py`
- Work queues: `agent_work_queues/`
- Wake-up prompts: `AGENT_*_WAKEUP_PROMPT.md`

**Commands:**
```bash
# Move agent documentation
git mv AGENT_TEAM_CHAT.md swarm-lab/docs/
git mv START_THREE_AGENTS.md swarm-lab/docs/
git mv AUTONOMOUS_AGENT_SYSTEM.md swarm-lab/docs/
git mv THREE_AGENT_PARALLEL_WORK_PLAN.md swarm-lab/docs/
git mv CURRENT_ARCHITECTURE_FILES.md swarm-lab/docs/

# Move wake-up prompts
git mv AGENT_ALPHA_WAKEUP_PROMPT.md swarm-lab/prompts/
git mv AGENT_BETA_WAKEUP_PROMPT.md swarm-lab/prompts/
git mv AGENT_GAMMA_WAKEUP_PROMPT.md swarm-lab/prompts/
git mv START_AGENTS_HERE.md swarm-lab/prompts/
git mv UPDATED_WAKEUP_INSTRUCTIONS.md swarm-lab/prompts/

# Move agent scripts
mkdir -p swarm-lab/agents
cp shared/agent_utils.py swarm-lab/agents/  # Keep copy in shared for now
find scripts -name "*agent*" -exec git mv {} swarm-lab/scripts/ \;

# Move work queues & history
git mv agent_work_queues swarm-lab/history/

# Move agent-specific scripts
git mv scripts/create_*_module.py swarm-lab/scripts/  # Alpha's module creation scripts
```

**IMPORTANT - Update Imports:**

After moving `agent_utils.py`, you may need to update imports in agent scripts. Log this:

```md
### Import Path Updates Needed:
- All files importing `shared.agent_utils` need updating if we move it
- **Decision:** Keep `shared/agent_utils.py` in place for now
- **Rationale:** Used by both swarm and product code

### Files That Import agent_utils:
- (List files after grep)
```

**Check imports:**
```bash
grep -r "from shared.agent_utils" . --include="*.py"
grep -r "import agent_utils" . --include="*.py"
```

---

### PHASE 5 — Data, Exports, Archives (30 min)

**What to move:**
- Archives: `*.zip`, `*.tar.gz`
- Logs: `*_log.txt`, `import_log.txt`
- Exports: `modules/exports/`

**Commands:**
```bash
# Move archives
find . -maxdepth 1 -name "*.zip" -exec git mv {} data/archives/ \;
find . -maxdepth 1 -name "*.tar.gz" -exec git mv {} data/archives/ \;

# Move logs
find . -maxdepth 1 -name "*_log.txt" -exec git mv {} data/logs/ \;

# Move module exports
if [ -d modules/exports ]; then
  git mv modules/exports data/exports/modules
fi

# Update .gitignore
cat >> .gitignore << 'EOF'

# Data directories (regenerable)
data/tmp/
data/logs/*.log
data/exports/*.json
!data/exports/README.md

# Large archives (don't commit)
data/archives/*.zip
data/archives/*.tar.gz

# Caches
__pycache__/
*.pyc
node_modules/
.pytest_cache/
EOF
```

---

### PHASE 6 — Third-Party Isolation (15 min)

**What to move:**
- `react-notion-x-master/` → `third_party/react-notion-x-master/`

**Commands:**
```bash
# Move third-party library
if [ -d react-notion-x-master ]; then
  git mv react-notion-x-master third_party/react-notion-x-master
fi

# Create third_party README
cat > third_party/README.md << 'EOF'
# Third-Party Dependencies

This directory contains vendored external libraries that are not available via package managers.

## react-notion-x-master

**Source:** https://github.com/NotionX/react-notion-x
**License:** MIT
**Purpose:** Render Notion pages in React
**DO NOT MODIFY:** This is a vendored copy. Changes should be contributed upstream.

**Usage:**
```javascript
import { NotionRenderer } from '../third_party/react-notion-x-master'
```
EOF

git add third_party/README.md
```

---

### PHASE 7 — Product Doc Templates (30 min)

**Objective:** Ensure each product has standard documentation

**Required docs for each app:**
1. `OVERVIEW.md` - What it is, who uses it
2. `ARCHITECTURE.md` - Technical design
3. `UX-FLOW.md` - User journeys
4. `API.md` - API reference

**For each app (onboarding-app, team-lead-tool, researcher-dashboard):**

```bash
# Check existing docs
ls product/docs/onboarding-app/

# If OVERVIEW.md missing, create template:
cat > product/docs/onboarding-app/OVERVIEW.md << 'EOF'
# Onboarding App Overview

## Purpose
Student-facing Learning Management System (LMS) for hands-on technical training.

## Users
- New students joining CubeSat teams
- Team members onboarding to new subsystems

## Key Features
- Interactive module player
- Progress tracking
- Competitive race mode (ghost cohorts)
- Subsystem-specific learning paths

## Technology
- Frontend: React (PWA)
- Backend: Flask (Python)
- Database: PostgreSQL (Neon)

## Related Docs
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical design
- [API.md](../../../backend/onboarding-lms/API.md) - API endpoints
EOF
```

**Repeat for other apps** (team-lead-tool, researcher-dashboard)

**If duplicates/conflicts exist:**
- Preserve both with suffixes: `ARCHITECTURE.md`, `ARCHITECTURE_OLD.md`
- Add TODO comment at top
- Log in OPEN_QUESTIONS.md

---

### PHASE 8 — Final Checks (30 min)

**Checklist:**

```bash
# 1. Review git status
git status

# 2. Check for accidentally tracked secrets
grep -r "DATABASE_URL=" . --include="*.py" --include="*.js" --exclude-dir=".git"
grep -r "NOTION_TOKEN" . --include="*.py" --include="*.js" --exclude-dir=".git"
grep -r "ntn_" . --include="*.py" --include="*.md" --exclude-dir=".git"

# If found in tracked files → STOP and report!

# 3. Validate doc paths
grep -r "docs/" README.md
grep -r "\[.*\](docs/" . --include="*.md"

# 4. Update .gitignore (if not done in Phase 5)

# 5. Review CHANGE_LOG.md
cat platform/cleanup/CHANGE_LOG.md

# 6. Review OPEN_QUESTIONS.md
cat platform/cleanup/OPEN_QUESTIONS.md
```

**Final Validation:**
- [ ] No `.env` files in git
- [ ] No API keys in tracked files
- [ ] All moves logged in CHANGE_LOG.md
- [ ] Ambiguities logged in OPEN_QUESTIONS.md
- [ ] Import paths updated (or logged as TODO)
- [ ] .gitignore updated
- [ ] README.md paths updated

---

## 🚧 Outlier Handling

### Mixed-Purpose Docs
**Example:** `MULTI_AGENT_SYSTEM_SETUP_GUIDE.md` (both swarm + platform)

**Options:**
1. Move to `swarm-lab/docs/` (if primarily agent-focused)
2. Move to `product/docs/shared/` (if cross-cutting)
3. Leave in root + add to `OPEN_QUESTIONS.md`

**Decision:** Log reasoning in CHANGE_LOG.md

---

### Old Drafts
**Example:** `docs/archive/ARCHITECTURE_DESIGN.md`

**Action:**
- Keep in `docs/archive/` (already archived)
- Add header: `<!-- ARCHIVED: Superseded by product/docs/.../ARCHITECTURE.md -->`
- Log in CHANGE_LOG.md

---

### Potential Secrets
**Example:** File contains `DATABASE_URL=postgresql://...`

**Action:**
1. **STOP immediately**
2. Log in `platform/cleanup/SECRETS_FOUND.md`:
   ```md
   # Secrets Found During Cleanup

   ## File: scripts/old_config.py
   - **Line 45:** Contains database URL
   - **Action:** DO NOT COMMIT. Report to user.
   - **Recommendation:** Add to .gitignore, remove from git history
   ```
3. Do NOT modify the file
4. Do NOT commit anything
5. Report to user

---

### Unclear Items
**Example:** `PROTOTYPE_ANALYSIS.md` - not clear which app

**Action:**
1. Leave in place
2. Add to `OPEN_QUESTIONS.md`:
   ```md
   ## PROTOTYPE_ANALYSIS.md
   - **Current location:** Root
   - **Ambiguity:** Not clear which product this belongs to
   - **Options:**
     1. Move to product/docs/shared/
     2. Delete if obsolete
     3. Ask user for clarification
   - **Recommendation:** Ask user
   ```

---

## 📝 Deliverables

After completion, you should have:

1. **Restructured repository** matching target structure
2. **platform/cleanup/CHANGE_LOG.md** - All moves documented
3. **platform/cleanup/OPEN_QUESTIONS.md** - Ambiguities logged
4. **platform/cleanup/MOVED_FILES.txt** - List of all git mv commands
5. **platform/cleanup/SECRETS_FOUND.md** - Any secrets discovered (if applicable)
6. **Updated .gitignore** - Covering data/, tmp/, caches
7. **Updated README.md** - Paths corrected
8. **Product docs** - Each app has OVERVIEW, ARCHITECTURE, etc.

---

## 🎯 Success Criteria

- [ ] All files categorized (product/swarm/platform/data/third_party)
- [ ] No tracked secrets in repository
- [ ] Git history preserved (used `git mv`)
- [ ] All moves logged and explained
- [ ] Ambiguities documented for user review
- [ ] Import paths verified or TODO logged
- [ ] .gitignore updated
- [ ] Documentation structure complete

---

## 📞 When to Ask for Help

**Stop and ask if:**
1. You find secrets in tracked files
2. Moving a file would break imports and you're unsure how to fix
3. A file's purpose is completely unclear after research
4. You're about to delete something that might be important
5. The task is taking >5 hours (re-scope with user)

---

**Assigned to:** Agent Gamma
**Created:** 2025-11-29
**Status:** Ready to execute
**Estimated effort:** 3-4 hours
**Risk level:** Medium (many file moves, potential for import breakage)
