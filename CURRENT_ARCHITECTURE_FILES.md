# ✅ CURRENT Architecture Files - Reference Only These

**Updated:** 2025-11-29
**Purpose:** Definitive list of CURRENT architecture documentation (ignore everything else!)

---

## 🎯 **For ALL Agents - Start Here**

### **1. Agent System Orientation**
- ⭐ **[START_THREE_AGENTS.md](START_THREE_AGENTS.md)** - Agent roles, coordination, startup
- ⭐ **[AGENT_TEAM_CHAT.md](AGENT_TEAM_CHAT.md)** - Live communication log (scroll to bottom!)
- ⭐ **[AUTONOMOUS_AGENT_SYSTEM.md](AUTONOMOUS_AGENT_SYSTEM.md)** - Coordination protocols
- **[THREE_AGENT_PARALLEL_WORK_PLAN.md](THREE_AGENT_PARALLEL_WORK_PLAN.md)** - Work distribution

### **2. Work Queues (Agent-Specific)**
- **[agent_work_queues/alpha_queue.md](agent_work_queues/alpha_queue.md)** - Alpha's tasks
- **[agent_work_queues/beta_queue.md](agent_work_queues/beta_queue.md)** - Beta's tasks
- **[agent_work_queues/gamma_queue.md](agent_work_queues/gamma_queue.md)** - Gamma's tasks

### **3. Database Reference**
- ⭐ **[docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md](docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md)** - Master schema (37 tables)
  - Created by Agent Gamma: 2025-11-29
  - CADENCE tables (5): people, projects, tasks, meetings, documents
  - Ascent Basecamp tables (15): modules, agent coordination, race features
  - Student platform tables (17): existing student/team data

---

## 📚 **System-Specific Architecture (By Domain)**

### **Student Onboarding LMS System**
- ⭐ **[docs/onboarding-lms/ARCHITECTURE.md](docs/onboarding-lms/ARCHITECTURE.md)**
  - Technical design, database schema, API endpoints, React components
  - Updated: 2025-01-23
  - Status: ✅ CURRENT

### **Researcher Dashboard / Analytics Platform**
- ⭐ **[docs/research-analytics/ARCHITECTURE.md](docs/research-analytics/ARCHITECTURE.md)**
  - FRAMES complete system, Discord integration, AI model pipeline
  - Updated: 2025-11-19
  - Status: ✅ CURRENT

### **Team Lead / Content Management**
- **[docs/onboarding-lms/TEAM_LEAD_WORKFLOW.md](docs/onboarding-lms/TEAM_LEAD_WORKFLOW.md)**
  - Simplified content submission, AI-assisted, no Git required
- **[NOTION_DESIGN_BEST_PRACTICES.md](NOTION_DESIGN_BEST_PRACTICES.md)**
  - Workspace design, API integration

### **High-Level System Overview**
- **[system_overview_bundle/system_overview_for_ai_agents.md](system_overview_bundle/system_overview_for_ai_agents.md)**
  - What this system is, who it's for, educational goals
  - AI agent responsibilities and boundaries

---

## ❌ **OLD/ARCHIVED Files - DO NOT USE**

### **Superseded by Current Files:**
- ❌ **docs/archive/ARCHITECTURE_DESIGN.md** - Use docs/onboarding-lms/ARCHITECTURE.md instead
- ❌ **README_COMPLETE_SYSTEM.md** - Use START_THREE_AGENTS.md instead
- ❌ **docs/lms/MODULE-DATA-ARCHITECTURE.md** - Module flow now in ASCENT_BASECAMP_DATABASE_SCHEMA.md
- ❌ **Anything in docs/archive/** - Reference only, not operational

### **Files Needing Audit/Update:**
- ⚠️ **ARCHITECTURE_QUICK_REFERENCE.md** - Created today, may have old references
- ⚠️ **Various wake-up prompts** - Need to remove old architecture links

---

## 📋 **Reading Priority by Agent**

### **Agent Alpha (Module Creator)**
**Must Read:**
1. [START_THREE_AGENTS.md](START_THREE_AGENTS.md) - Your role
2. [AGENT_TEAM_CHAT.md](AGENT_TEAM_CHAT.md) - Team updates
3. [agent_work_queues/alpha_queue.md](agent_work_queues/alpha_queue.md) - Your tasks
4. [docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md](docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md) - Tables you write to

**Reference When Needed:**
- [docs/onboarding-lms/ARCHITECTURE.md](docs/onboarding-lms/ARCHITECTURE.md) - Module structure
- [system_overview_bundle/system_overview_for_ai_agents.md](system_overview_bundle/system_overview_for_ai_agents.md) - Educational framework

---

### **Agent Beta (Platform Developer)**
**Must Read:**
1. [START_THREE_AGENTS.md](START_THREE_AGENTS.md) - Your role
2. [AGENT_TEAM_CHAT.md](AGENT_TEAM_CHAT.md) - Team updates
3. [agent_work_queues/beta_queue.md](agent_work_queues/beta_queue.md) - Your tasks
4. [docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md](docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md) - API data models

**Reference When Needed:**
- [docs/onboarding-lms/ARCHITECTURE.md](docs/onboarding-lms/ARCHITECTURE.md) - React/Flask design
- [docs/lms/API_REFERENCE.md](docs/lms/API_REFERENCE.md) - Endpoints you built

---

### **Agent Gamma (Infrastructure)**
**Must Read:**
1. [START_THREE_AGENTS.md](START_THREE_AGENTS.md) - Your role
2. [AGENT_TEAM_CHAT.md](AGENT_TEAM_CHAT.md) - **Check help requests FIRST!**
3. [agent_work_queues/gamma_queue.md](agent_work_queues/gamma_queue.md) - Your tasks
4. [docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md](docs/ASCENT_BASECAMP_DATABASE_SCHEMA.md) - Schema you created!

**Reference When Needed:**
- [docs/research-analytics/ARCHITECTURE.md](docs/research-analytics/ARCHITECTURE.md) - Analytics pipeline
- [docs/onboarding-lms/TEAM_LEAD_WORKFLOW.md](docs/onboarding-lms/TEAM_LEAD_WORKFLOW.md) - Content flow
- [NOTION_DESIGN_BEST_PRACTICES.md](NOTION_DESIGN_BEST_PRACTICES.md) - Sync daemon design

---

## 🔄 **Data Flow (Current)**

```
CADENCE Historical Data (Notion Export)
    ↓
Agent Gamma Ingestion → cadence_* tables (1,416 records)
    ↓
Agent Alpha Module Creation → modules, module_sections tables
    ↓
Agent Beta Platform → React UI + Flask API
    ↓
Students → learner_performance, subsystem_competency tables
```

---

## ✅ **Quick Verification Checklist**

Before referencing ANY architecture file, check:

- [ ] Is it in the "CURRENT" section above? ✅ Use it
- [ ] Is it in the "OLD/ARCHIVED" section? ❌ Don't use it
- [ ] Is it in docs/archive/? ❌ Reference only, not operational
- [ ] Does it have a recent date (Nov 2025+)? ✅ Likely current
- [ ] Does it reference Azure instead of Neon? ❌ Outdated!

---

## 📞 **When in Doubt**

**Ask these questions:**
1. Does this file reference the **three-agent system** (Alpha/Beta/Gamma)? → Likely current
2. Does this file reference **Neon PostgreSQL**? → Current
3. Does this file reference **Azure** or old infrastructure? → Outdated
4. Is this file in the **docs/archive/** folder? → Reference only
5. When was this file last updated? → Nov 2025+ = current

**The Golden Rule:**
> If it's not listed in this file's "CURRENT" section, check with the team before using it as a reference!

---

## 🛠️ **TODO: Architecture Audit**

- [ ] Audit ARCHITECTURE_QUICK_REFERENCE.md - remove old refs
- [ ] Update all wake-up prompts to reference ONLY current files
- [ ] Add ASCENT_BASECAMP_DATABASE_SCHEMA.md to all agent prompts
- [ ] Mark README_COMPLETE_SYSTEM.md as deprecated
- [ ] Update START_HERE_AGENTS.md architecture section
- [ ] Remove MODULE-DATA-ARCHITECTURE.md from references (info now in DB schema)

---

**Status:** ✅ This file is the source of truth for what's current!
**Maintained by:** All agents (keep this updated!)
**Last Updated:** 2025-11-29
