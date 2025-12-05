# FRAMES System Implementation Report
## Agent Delta Analysis & Recommendations

**Date:** December 5, 2025  
**Prepared by:** Agent Delta (Cursor IDE)  
**For:** Liz (System Architect)  
**Report Type:** User Needs Assessment & Implementation Recommendations

---

## Executive Summary

This report analyzes the FRAMES multi-agent system architecture, documents user requirements gathered through conversation, and provides implementation recommendations for both the immediate build phase and the long-term ML-powered module generation system.

**Key Finding:** The current 5-agent architecture is well-designed and aligns with industry best practices (LangGraph, DeepAgents patterns). The planned pivot to a specialized ML model for module generation is architecturally sound and will provide long-term cost efficiency and quality improvements.

---

## Table of Contents

1. [User Needs Assessment](#1-user-needs-assessment)
2. [Current System Architecture](#2-current-system-architecture)
3. [Framework Analysis](#3-framework-analysis)
4. [Implementation Recommendations](#4-implementation-recommendations)
5. [Phase 1: Build Phase Priorities](#5-phase-1-build-phase-priorities)
6. [Phase 2: ML Integration Plan](#6-phase-2-ml-integration-plan)
7. [Technical Specifications](#7-technical-specifications)
8. [Risk Assessment](#8-risk-assessment)
9. [Next Steps](#9-next-steps)

---

## 1. User Needs Assessment

### 1.1 Primary Requirements

| Requirement | Priority | Status |
|-------------|----------|--------|
| Multi-agent coordination system | HIGH | ✅ Designed |
| Agent tracking and observability | HIGH | 🔲 Needs implementation |
| Persistent memory across sessions | HIGH | 🔲 Needs implementation |
| Feedback loop for continuous improvement | HIGH | ✅ Designed (Omega system) |
| Database integration (Neon PostgreSQL) | HIGH | ✅ Connected |
| Notion integration for tracking | MEDIUM | ✅ MCP configured |
| Version control for agent work | MEDIUM | 🔲 Needs implementation |
| ML model for module generation (future) | HIGH | 🔲 Phase 2 |
| Student feedback data collection | HIGH | 🔲 Needs implementation |

### 1.2 Stated User Goals

1. **Immediate:** Have agents build a working system with proper tracking
2. **Short-term:** Implement memory/feedback systems that enable learning
3. **Long-term:** Replace LLM-based module creation with specialized ML model
4. **Ongoing:** Create replicable patterns that can scale

### 1.3 User Constraints

| Constraint | Impact |
|------------|--------|
| Multiple IDEs (VS Code + Cursor) | Agents need robust file-based coordination |
| Windows environment | Some tooling differences from Unix |
| Learning new frameworks | Prefer simpler approaches initially |
| Cost consciousness | ML model preferred over ongoing LLM API costs |

---

## 2. Current System Architecture

### 2.1 Agent Roles

```
┌─────────────────────────────────────────────────────────────────┐
│                     PLANNING TRIO                                │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
│  │  ALPHA   │◄──►│   BETA   │◄──►│  GAMMA   │                   │
│  │ Content  │    │ Frontend │    │ Infra    │                   │
│  │ Planning │    │ Planning │    │ Planning │                   │
│  └──────────┘    └──────────┘    └──────────┘                   │
│                        │                                         │
│                        ▼                                         │
│              ┌─────────────────┐                                 │
│              │  NEGOTIATION    │                                 │
│              │  (MAX_ROUNDS)   │                                 │
│              └────────┬────────┘                                 │
│                       │                                          │
│                       ▼                                          │
│              ┌─────────────────┐                                 │
│              │  3 PLAN OPTIONS │                                 │
│              └────────┬────────┘                                 │
└───────────────────────┼─────────────────────────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │   HUMAN (Liz)   │
              │  Selects Plan   │
              └────────┬────────┘
                       │
                       ▼
┌──────────────────────┴──────────────────────────────────────────┐
│                     EXECUTION DUO                                │
│                                                                  │
│  ┌──────────────────┐         ┌──────────────────┐              │
│  │      OMEGA       │         │      DELTA       │              │
│  │   (Codespace)    │         │    (Cursor)      │              │
│  │                  │         │                  │              │
│  │ • Backend/DB     │         │ • Frontend test  │              │
│  │ • Scripts        │         │ • Browser tools  │              │
│  │ • Infrastructure │         │ • Cross-validate │              │
│  └──────────────────┘         └──────────────────┘              │
│                                                                  │
│                        │                                         │
│                        ▼                                         │
│              ┌─────────────────┐                                 │
│              │    FEEDBACK     │                                 │
│              │  (Issue Log)    │                                 │
│              └────────┬────────┘                                 │
└───────────────────────┼─────────────────────────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │ LEARNING LOOP   │
              │ (Back to Trio)  │
              └─────────────────┘
```

### 2.2 Current File Structure

```
FRAMES-Python/
├── FRAMES-Python/
│   ├── docs/
│   │   ├── agents/
│   │   │   ├── AGENT_ALPHA_WAKEUP_PROMPT.md
│   │   │   ├── AGENT_BETA_WAKEUP_PROMPT.md
│   │   │   ├── AGENT_GAMMA_WAKEUP_PROMPT.md
│   │   │   ├── AGENT_DELTA_WAKEUP_PROMPT.md
│   │   │   ├── AGENT_TEAM_CHAT.md
│   │   │   └── UPDATED_WAKEUP_INSTRUCTIONS.md
│   │   ├── agent_work_queues/
│   │   │   ├── alpha_queue.md
│   │   │   ├── beta_queue.md
│   │   │   ├── gamma_queue.md
│   │   │   └── delta_queue.md
│   │   └── canon/
│   │       ├── OPERATIONAL_ONTOLOGY.md
│   │       ├── agent_interaction_script_v_2.md
│   │       └── Notion_Interface_layer.md
│   ├── backend/
│   ├── frontend-react/
│   ├── modules/
│   ├── scripts/
│   ├── shared/
│   │   └── agent_utils.py
│   └── requirements.txt
├── langgraph/          # Framework source (just added)
├── llama_index/        # Framework source (just added)
└── deepagents/         # Framework source (just added)
```

### 2.3 Coordination Mechanisms

| Mechanism | Purpose | Status |
|-----------|---------|--------|
| `AGENT_TEAM_CHAT.md` | Real-time coordination log | ✅ Active |
| `agent_work_queues/*.md` | Task assignments | ✅ Active |
| Wake-up prompts | Session initialization | ✅ Active |
| Database `ascent_basecamp_agent_log` | Structured tracking | ✅ Schema exists |
| Notion Issue Log | Feedback collection | 🔲 Not created |
| Learning logs | Accumulated learnings | 🔲 Not created |

---

## 3. Framework Analysis

### 3.1 Available Frameworks

User has cloned full source repositories for three frameworks:

| Framework | Files | Primary Use Case | Relevance to FRAMES |
|-----------|-------|------------------|---------------------|
| **LangGraph** | ~500+ | Agent orchestration, state machines | HIGH - Multi-agent coordination |
| **LlamaIndex** | ~8000+ | RAG, document retrieval | MEDIUM - CADENCE doc queries |
| **DeepAgents** | ~80 | High-level multi-agent (built on LangGraph) | HIGH - Simplest path to adoption |

### 3.2 Framework Comparison

| Feature | LangGraph | DeepAgents | LlamaIndex |
|---------|-----------|------------|------------|
| Multi-agent | ✅ Manual setup | ✅ Built-in | ❌ Not focus |
| State persistence | ✅ Checkpoints | ✅ Via LangGraph | ❌ Different focus |
| Human-in-the-loop | ✅ Native | ✅ Native | ❌ N/A |
| Todo/Planning tool | ❌ Manual | ✅ Built-in | ❌ N/A |
| Subagent spawning | ✅ Manual | ✅ Built-in | ❌ N/A |
| Document RAG | ❌ Via integration | ❌ Via integration | ✅ Core strength |
| Learning curve | Medium | Low | Medium |

### 3.3 Recommendation

**Primary:** Use **DeepAgents** patterns for multi-agent coordination
- Built-in TodoListMiddleware aligns with your work queue approach
- SubAgentMiddleware matches your Planning Trio → Execution Duo pattern
- FilesystemMiddleware matches your file-based memory approach

**Secondary:** Use **LlamaIndex** for CADENCE document retrieval
- When Alpha needs to query source documents
- For future ML training data preparation

**Optional:** Drop to **LangGraph** when you need lower-level control
- Custom state machines
- Complex conditional workflows

### 3.4 Package Management

| Tool | Status | Use |
|------|--------|-----|
| Poetry | ✅ Installed (v2.2.1) | Optional |
| **uv** | ✅ Installed (v0.9.15) | **Primary** - Used by all frameworks |
| pip | ✅ Available | Fallback |

**Recommendation:** Use `uv` for all package management
```powershell
uv sync              # Install dependencies
uv add <package>     # Add new package
uv run python X      # Run in environment
```

---

## 4. Implementation Recommendations

### 4.1 Wake-Up File Structure (Revised)

Split each wake-up file into static and dynamic sections:

```markdown
# Agent [Name] Wake-Up Prompt

## ═══════════════════════════════════════════════════
## SECTION 1: IDENTITY (Static - rarely changes)
## ═══════════════════════════════════════════════════
[Role, capabilities, resource ownership]

## ═══════════════════════════════════════════════════
## SECTION 2: PROTOCOLS (Static - rarely changes)
## ═══════════════════════════════════════════════════
[Startup sequence, communication protocol, canon docs]

## ═══════════════════════════════════════════════════
## SECTION 3: CURRENT STATE (Dynamic - every session)
## Last Updated: [TIMESTAMP]
## ═══════════════════════════════════════════════════
[Session status, memory state, blockers, immediate priority]

## ═══════════════════════════════════════════════════
## SECTION 4: LEARNINGS (Semi-Dynamic - when learnings occur)
## ═══════════════════════════════════════════════════
[What I've learned, patterns to follow, patterns to avoid]

## ═══════════════════════════════════════════════════
## SECTION 5: QUICK REFERENCE (Static)
## ═══════════════════════════════════════════════════
[Files to read, code snippets]
```

**Alternative:** Separate memory file per agent
```
AGENT_[NAME]_WAKEUP_PROMPT.md  (static, ~150 lines)
AGENT_[NAME]_MEMORY.md         (dynamic, ~30 lines)
```

### 4.2 Omega-Delta Feedback System

**Recommendation:** Adopt Omega's proposed system with simplifications

**Core components to implement:**
1. ✅ Agent Issue Log (Notion page)
2. ✅ Feedback categories (Plan Ambiguity, Technical Feasibility, Safety, Success)
3. ✅ Learning logs per agent
4. ⚠️ Simplify collaboration modes (skip Mode 3 initially)

**Simplified collaboration modes:**
- **Mode 1 (Parallel):** Default for independent tasks
- **Mode 2 (Sequential):** For tasks with dependencies

### 4.3 Database Schema Additions

For ML training data collection, add these tables:

```sql
-- Student interaction events
CREATE TABLE learner_events (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    module_id INTEGER REFERENCES modules(id),
    section_id INTEGER REFERENCES module_sections(id),
    event_type VARCHAR(50),  -- 'section_start', 'section_complete', 'hint_used', etc.
    duration_seconds INTEGER,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Module feedback
CREATE TABLE module_feedback (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    module_id INTEGER REFERENCES modules(id),
    clarity_rating INTEGER CHECK (clarity_rating BETWEEN 1 AND 5),
    difficulty_rating INTEGER CHECK (difficulty_rating BETWEEN 1 AND 5),
    relevance_rating INTEGER CHECK (relevance_rating BETWEEN 1 AND 5),
    comments TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Module versions (for A/B testing)
CREATE TABLE module_versions (
    id SERIAL PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),
    version_number VARCHAR(20),
    created_by VARCHAR(50),  -- 'alpha', 'ml_model_v1', etc.
    content_hash VARCHAR(64),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- A/B test assignments
CREATE TABLE ab_test_assignments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    module_id INTEGER REFERENCES modules(id),
    variant_id INTEGER REFERENCES module_versions(id),
    assigned_at TIMESTAMP DEFAULT NOW()
);
```

### 4.4 Agent Tracking Infrastructure

**Recommended first task for agents:** Bootstrap their own tracking system

```
Bootstrap Task: Agent Self-Infrastructure
├── Gamma: Create database tables for agent tracking
├── Omega: Create Notion Agent Issue Log page
├── Beta: Build agent dashboard UI (optional)
├── Alpha: Define feedback templates
└── Delta: Validate all systems work together
```

---

## 5. Phase 1: Build Phase Priorities

### 5.1 Immediate Priorities (This Week)

| Priority | Task | Owner | Deliverable |
|----------|------|-------|-------------|
| 1 | Complete agent tracking database schema | Gamma | SQL tables created |
| 2 | Create Notion Agent Issue Log | Omega | Notion page with safe region |
| 3 | Implement memory file structure | All | `AGENT_[NAME]_MEMORY.md` files |
| 4 | Test feedback loop | Delta | End-to-end validation |

### 5.2 Short-Term Priorities (Next 2 Weeks)

| Priority | Task | Owner | Deliverable |
|----------|------|-------|-------------|
| 1 | Add `learner_events` table | Gamma | Schema + API endpoints |
| 2 | Build feedback capture UI | Beta | React component |
| 3 | Create module versioning system | Alpha + Gamma | Version tracking |
| 4 | Implement A/B test infrastructure | Gamma + Beta | Assignment system |

### 5.3 Medium-Term Priorities (Month 1)

| Priority | Task | Owner | Deliverable |
|----------|------|-------|-------------|
| 1 | Collect baseline student data | System | 100+ module completions |
| 2 | Define ML training data format | Alpha + Gamma | Data schema |
| 3 | Build data export pipeline | Gamma | ML-ready datasets |
| 4 | Research ML model options | Delta (research) | Recommendation report |

---

## 6. Phase 2: ML Integration Plan

### 6.1 Architecture Vision

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 2: ML-POWERED SYSTEM                   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              SPECIALIZED ML MODEL                        │   │
│  │                                                          │   │
│  │  Input:                    Output:                       │   │
│  │  • Source material         • Module structure            │   │
│  │  • Learning objectives     • Section content             │   │
│  │  • Difficulty target       • Quiz questions              │   │
│  │  • Historical outcomes     • Difficulty calibration      │   │
│  │                                                          │   │
│  │  Training signals:                                       │   │
│  │  • Completion rates                                      │   │
│  │  • Quiz scores                                           │   │
│  │  • Time-to-complete                                      │   │
│  │  • Student feedback                                      │   │
│  │  • A/B test results                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          ▲                                      │
│                          │                                      │
│  ┌───────────────────────┴───────────────────────┐             │
│  │            DATA COLLECTION LAYER               │             │
│  │                                                │             │
│  │  Omega: Ingest new CADENCE docs               │             │
│  │  Beta: Capture student interactions            │             │
│  │  Gamma: Pipeline data to training              │             │
│  │  Alpha: Curate/validate training examples      │             │
│  │  Delta: QA generated modules                   │             │
│  └────────────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 ML Model Options

| Approach | Pros | Cons | Complexity |
|----------|------|------|------------|
| **Fine-tuned LLM** (Llama, Mistral) | Good text generation, can start with few examples | Still needs API/GPU, expensive to train | Medium |
| **Seq2Seq** (T5, BART) | Structured output, efficient | Needs more training data | Medium |
| **Retrieval + Generation** | Uses existing content, less hallucination | Complex pipeline | High |
| **Reinforcement Learning** | Optimizes for outcomes | Needs lots of interaction data | High |
| **Template + Ranking** | Simple, interpretable | Limited creativity | Low |

**Recommendation:** Start with **Template + Ranking** approach:
1. Create module templates from successful modules
2. Train ranking model to score/select best content
3. Graduate to fine-tuned model when you have enough data

### 6.3 Minimum Viable Data

| Data Type | Minimum for Training | Target |
|-----------|---------------------|--------|
| Completed modules | 50+ | 200+ |
| Student completions | 500+ events | 5000+ |
| Feedback responses | 100+ | 1000+ |
| A/B test comparisons | 20+ module pairs | 100+ |

### 6.4 Agent Role Evolution

| Agent | Phase 1 (Build) | Phase 2 (Operate) |
|-------|-----------------|-------------------|
| Alpha | Create modules manually | Curate training data, validate ML output |
| Beta | Build UI | Maintain feedback capture, A/B testing |
| Gamma | Database + infra | ML pipeline operations, model training |
| Delta | Testing + QA | QA generated modules, anomaly detection |
| Omega | Execution + backend | Data ingestion, pipeline orchestration |

---

## 7. Technical Specifications

### 7.1 Environment Configuration

**Required environment variables (.env):**
```env
# Database
DATABASE_URL=postgresql://user:password@host/frames?sslmode=require

# Notion
NOTION_API_KEY=secret_xxx

# Optional: LLM APIs (for current phase)
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx

# Future: ML Model
ML_MODEL_ENDPOINT=http://localhost:8000/generate
```

### 7.2 MCP Server Configuration

**Current Cursor MCP setup:**
```json
{
  "mcpServers": {
    "Notion": {
      "configured": true,
      "capabilities": ["search", "fetch", "create-pages", "update-page"]
    }
  }
}
```

**Recommended addition:**
```json
{
  "mcpServers": {
    "Notion": { "configured": true },
    "docs-langchain": {
      "url": "https://docs.langchain.com/mcp"
    }
  }
}
```

### 7.3 Python Dependencies

**Current (`requirements.txt`):**
```
Flask==3.0.0
Flask-CORS==4.0.0
Flask-SQLAlchemy==3.0.3
psycopg2-binary>=2.9.9
python-dotenv==1.0.0
SQLAlchemy==2.0.44
```

**Recommended additions:**
```
# Agent frameworks (when ready to adopt)
langgraph>=0.2.0
deepagents>=0.2.8

# For RAG (Alpha's CADENCE queries)
llama-index>=0.10.0

# For ML data collection
pandas>=2.0.0
numpy>=1.24.0

# For future ML model
torch>=2.0.0  # or tensorflow
transformers>=4.30.0
```

---

## 8. Risk Assessment

### 8.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Agent coordination failures | Medium | High | File-based fallback, clear protocols |
| Memory loss between sessions | High | Medium | Structured memory files, database backup |
| Framework complexity | Medium | Medium | Start simple, adopt incrementally |
| ML data insufficiency | Medium | High | Longer data collection period, synthetic data |

### 8.2 Process Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Agent drift from canon | Medium | Medium | Regular canon refresh checkpoints |
| Feedback loop not closing | Medium | High | Omega's system with explicit triggers |
| Human bottleneck (approvals) | High | Medium | Batch approvals, trust building |

### 8.3 Dependencies

| Dependency | Risk Level | Fallback |
|------------|------------|----------|
| Neon PostgreSQL | Low | Local SQLite |
| Notion API | Medium | File-based logging |
| LLM APIs | Medium | Local models (Ollama) |
| Cursor MCP | Low | Manual operations |

---

## 9. Next Steps

### 9.1 Immediate Actions (Today/Tomorrow)

1. **Create memory file structure**
   - Create `AGENT_[NAME]_MEMORY.md` for each agent
   - Define update protocol

2. **Implement bootstrap task**
   - Assign to agents: "Build your own tracking infrastructure"
   - Let this be the first coordinated task

3. **Set up uv environment**
   ```powershell
   cd C:\Users\LizO5\Frames-Python\FRAMES-Python
   uv init  # or uv sync if pyproject.toml exists
   ```

### 9.2 This Week

1. **Gamma:** Create `learner_events` and `module_feedback` tables
2. **Omega:** Create Notion Agent Issue Log page
3. **Beta:** Start planning feedback capture UI
4. **Alpha:** Define module versioning approach
5. **Delta:** Validate end-to-end tracking

### 9.3 Decision Points

| Decision | When | Options |
|----------|------|---------|
| Adopt DeepAgents framework? | After bootstrap task | Yes (simplify code) / No (stay file-based) |
| Add LlamaIndex for RAG? | When Alpha needs doc queries | Yes / Manual queries |
| ML model architecture | After 500+ learner events | Fine-tune / Template / Hybrid |

---

## Appendix A: Key Documents Referenced

| Document | Location | Purpose |
|----------|----------|---------|
| OMEGA_DELTA_FEEDBACK_SYSTEM.md | `FRAMES-Python/` | Feedback architecture |
| AGENT_*_WAKEUP_PROMPT.md | `docs/agents/` | Agent initialization |
| UPDATED_WAKEUP_INSTRUCTIONS.md | `docs/agents/` | Coordination guide |
| agent_interaction_script_v_2.md | `canon/` | Role definitions |
| OPERATIONAL_ONTOLOGY.md | `canon/` | Core concepts |

## Appendix B: Framework Resources

| Resource | Path | Key Content |
|----------|------|-------------|
| LangGraph Plan-and-Execute | `langgraph/docs/docs/tutorials/plan-and-execute/` | Planning patterns |
| LangGraph Multi-Agent | `langgraph/examples/multi_agent/` | Coordination examples |
| DeepAgents README | `deepagents/libs/deepagents/README.md` | TodoList, Subagents, Filesystem |
| LlamaIndex Agents | `llama_index/docs/examples/agent/` | 31 agent notebooks |

## Appendix C: Database Schema (Agent Tracking)

```sql
-- Recommended additions to existing schema

-- Agent session tracking
CREATE TABLE agent_sessions (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(20),
    session_number INTEGER,
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    summary TEXT,
    tasks_completed INTEGER DEFAULT 0,
    issues_logged INTEGER DEFAULT 0
);

-- Agent learnings (from feedback)
CREATE TABLE agent_learnings (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(20),
    learning_type VARCHAR(50),  -- 'pattern_to_follow', 'pattern_to_avoid', 'insight'
    description TEXT,
    source_task_id INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Cross-agent messages
CREATE TABLE agent_messages (
    id SERIAL PRIMARY KEY,
    from_agent VARCHAR(20),
    to_agent VARCHAR(20),
    message_type VARCHAR(50),  -- 'status', 'request', 'blocker', 'completion'
    content TEXT,
    acknowledged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

**Report Generated:** December 5, 2025  
**Agent:** Delta  
**Environment:** Cursor IDE  
**Next Review:** After bootstrap task completion

