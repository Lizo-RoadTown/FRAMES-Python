# Documentation Migration Map

**Date:** November 30, 2025  
**Purpose:** Guide for finding relocated documentation after repository cleanup

## Quick Reference

| If you're looking for... | It moved to... |
|--------------------------|----------------|
| Canonical/authoritative docs | `/canon/` |
| Agent wake-up prompts | `/docs/agents/` |
| Notion setup guides | `/docs/notion/` |
| CADENCE documentation | `/docs/cadence/` |
| Quick start guides | `/docs/guides/` |
| Historical/deprecated docs | `/archive/` |

## Detailed Migration Table

### Canonical Documents (14) → /canon/

| Old Location | New Location |
|--------------|--------------|
| `INDEX.md` | `canon/INDEX.md` |
| `SYSTEM_OVERVIEW.md` | `canon/SYSTEM_OVERVIEW.md` |
| `DATABASE_SCHEMA.md` | `canon/DATABASE_SCHEMA.md` |
| `STUDENT_LMS.md` | `canon/STUDENT_LMS.md` |
| `TEAM_LEAD_MODULE_BUILDER.md` | `canon/TEAM_LEAD_MODULE_BUILDER.md` |
| `RESEARCHER_PLATFORM.md` | `canon/RESEARCHER_PLATFORM.md` |
| `NOTION_INTEGRATION.md` | `canon/NOTION_INTEGRATION.md` |
| `NOTION_PAGE_RULES.md` | `canon/NOTION_PAGE_RULES.md` |
| `AGENT_SYSTEM_OVERVIEW.md` | `canon/AGENT_SYSTEM_OVERVIEW.md` ⭐ *merged with implementation details* |
| `AGENT_SAFETY_RULES.md` | `canon/AGENT_SAFETY_RULES.md` |
| `AGENT_ERROR_LOGGING.md` | `canon/AGENT_ERROR_LOGGING.md` |
| `OATUTOR_ADAPTATION.md` | `canon/OATUTOR_ADAPTATION.md` |
| `FILE_STRUCTURE_AND_STANDARDS.md` | `canon/FILE_STRUCTURE_AND_STANDARDS.md` |
| `ARCHIVE_INDEX.md` | `canon/ARCHIVE_INDEX.md` |

### Active Agent Documentation → /docs/agents/

| Old Location | New Location |
|--------------|--------------|
| `AGENT_ALPHA_WAKEUP_PROMPT.md` | `docs/agents/AGENT_ALPHA_WAKEUP_PROMPT.md` |
| `AGENT_BETA_WAKEUP_PROMPT.md` | `docs/agents/AGENT_BETA_WAKEUP_PROMPT.md` |
| `AGENT_GAMMA_WAKEUP_PROMPT.md` | `docs/agents/AGENT_GAMMA_WAKEUP_PROMPT.md` |
| `AGENT_TEAM_CHAT.md` | `docs/agents/AGENT_TEAM_CHAT.md` |
| `UPDATED_WAKEUP_INSTRUCTIONS.md` | `docs/agents/UPDATED_WAKEUP_INSTRUCTIONS.md` |

### Notion Documentation → /docs/notion/

| Old Location | New Location |
|--------------|--------------|
| `NOTION_API_SETUP.md` | `docs/notion/NOTION_API_SETUP.md` |
| `NOTION_DESIGN_BEST_PRACTICES.md` | `docs/notion/NOTION_DESIGN_BEST_PRACTICES.md` |
| `NOTION_GITHUB_INTEGRATION_SETUP.md` | `docs/notion/NOTION_GITHUB_INTEGRATION_SETUP.md` |
| `NOTION_IMPORT_GUIDE.md` | `docs/notion/NOTION_IMPORT_GUIDE.md` |
| `NOTION_RENDERING_ARCHITECTURE.md` | `docs/notion/NOTION_RENDERING_ARCHITECTURE.md` |
| `NOTION_WORKSPACE_ENHANCEMENT.md` | `docs/notion/NOTION_WORKSPACE_ENHANCEMENT.md` |
| `NOTION_WORKSPACE_SETUP.md` | `docs/notion/NOTION_WORKSPACE_SETUP.md` |

### CADENCE Documentation → /docs/cadence/

| Old Location | New Location |
|--------------|--------------|
| `CADENCE_EXTRACTION_SUMMARY.md` | `docs/cadence/CADENCE_EXTRACTION_SUMMARY.md` |
| `CADENCE_HUB_IMPLEMENTATION_PLAN.md` | `docs/cadence/CADENCE_HUB_IMPLEMENTATION_PLAN.md` |
| `ALPHA_MANUAL_INSTRUCTIONS.md` | `docs/cadence/ALPHA_MANUAL_INSTRUCTIONS.md` |

### Guides → /docs/guides/

| Old Location | New Location |
|--------------|--------------|
| `QUICK_START_CODESPACE.md` | `docs/guides/QUICK_START_CODESPACE.md` |
| `START_HERE_AGENTS.md` | `docs/guides/START_HERE_AGENTS.md` |
| `THREE_AGENT_PARALLEL_WORK_PLAN.md` | `docs/guides/THREE_AGENT_PARALLEL_WORK_PLAN.md` |

### Archived Files → /archive/

#### Agent Setup (Superseded)
| Old Location | New Location | Why Archived |
|--------------|--------------|--------------|
| `AGENT_COORDINATION_README.md` | `archive/agent-setup/` | Superseded by canonical |
| `AUTONOMOUS_AGENT_SETUP_COMPLETE.md` | `archive/agent-setup/` | Setup complete |
| `MULTI_AGENT_SYSTEM_SETUP_GUIDE.md` | `archive/agent-setup/` | Setup complete |
| `AGENT_WAKEUP_PROMPTS_SUMMARY.md` | `archive/agent-setup/` | Redundant with detailed prompts |
| `README_AGENT_WAKEUP.md` | `archive/agent-setup/` | Duplicate wake-up guide |

#### Early Development
| Old Location | New Location | Why Archived |
|--------------|--------------|--------------|
| `START_HERE.md` | `archive/early-development/` | HTML migration phase complete |
| `SETUP_COMPLETE.md` | `archive/early-development/` | Historical Neon setup |
| `README_COMPLETE_SYSTEM.md` | `archive/early-development/` | Outdated status metrics |
| `NEXT_STEPS_SUMMARY.md` | `archive/early-development/` | Time-sensitive, now outdated |
| `CADENCE_TO_NEON_PLAN.md` | `archive/early-development/` | Migration complete |

#### Notion Superseded
| Old Location | New Location | Why Archived |
|--------------|--------------|--------------|
| `NOTION_PAGE_INTERACTION_RULES.md` | `archive/notion-superseded/` | V2 in canonical |
| `NOTION_GITHUB_SETUP_CHECKLIST.md` | `archive/notion-superseded/` | Duplicate of setup guide |
| `NOTION_QUICK_REFERENCE.md` | `archive/notion-superseded/` | Redundant summary |

#### Proposals
| Old Location | New Location | Why Archived |
|--------------|--------------|--------------|
| `NOTION_PROJECT_MANAGEMENT_PROPOSAL.md` | `archive/proposals/` | Draft, not implemented |
| `THREE_BRANCH_WORK_PLAN_PROPOSAL.md` | `archive/proposals/` | Awaiting approval |

#### Analysis
| Old Location | New Location | Why Archived |
|--------------|--------------|--------------|
| `PROTOTYPE_ANALYSIS.md` | `archive/analysis/` | One-time snapshot |
| `ARCHITECTURE_QUICK_REFERENCE.md` | `archive/analysis/` | No unique content |

#### High-Risk (Dangerous/Conflicting)
| Old Location | New Location | Why Archived |
|--------------|--------------|--------------|
| `AUTONOMOUS_AGENT_SYSTEM.md` | `archive/high-risk/` | ⚠️ Duplicated canonical, merged and archived |
| `START_AGENTS_HERE.md` | `archive/high-risk/` | ⚠️ Outdated environment assumptions |

### Deleted Files

| Old Location | Action | Reason |
|--------------|--------|--------|
| `QUICK_START_NOTION_INTEGRATION.md` | **DELETED** | Empty/corrupted file |

### Stayed in Root (High-Use Files)

| File | Why It Stayed |
|------|---------------|
| `README.md` | Main project README - always in root |
| `MONOREPO_STRUCTURE.md` | Repository structure - frequently referenced |
| `CURRENT_ARCHITECTURE_FILES.md` | Navigation doc - helps find canonical sources |
| `REPO_CLEANUP_TASK.md` | This cleanup specification |

## Using This Map

### For Humans
- Bookmark `/canon/INDEX.md` as your starting point
- Most active docs are now in `/docs/` subfolders
- Root directory is cleaner with only essential files

### For Agents
- Update import paths if you reference moved files
- Check `/canon` first for authoritative information
- `/archive` is read-only historical reference
- Never implement from `/archive/high-risk` without human approval

### For Scripts/Automation
If you have scripts with hardcoded paths, update:
```python
# Old
with open('AGENT_SYSTEM_OVERVIEW.md') as f:

# New
with open('canon/AGENT_SYSTEM_OVERVIEW.md') as f:
```

## Transition Period

This migration map will remain in root for **30 days** to help with adjustment.  
After that, it will move to `/docs/` as a permanent reference.

## Questions?

- Can't find a file? Check `/archive/` subfolders
- Need info from archived doc? Check if it's in `/canon` first
- Unsure if something is canonical? Look in `/canon/INDEX.md`

---

**Last Updated:** November 30, 2025  
**Cleanup Completed By:** AI Agent (Safe Archive Mode)
