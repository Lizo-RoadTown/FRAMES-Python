# Canonical Documentation

**⚠️ AUTHORITATIVE SOURCES OF TRUTH ⚠️**

These 14 documents are the official, canonical references for FRAMES/Ascent Basecamp. They override all other documentation.

## Never Modify Without Approval

These documents define:
- System architecture
- Database schemas
- Agent rules and protocols
- Application specifications
- Integration standards

## The 14 Canonical Documents

### Core System
- **INDEX.md** - Master index linking all canonical documentation
- **SYSTEM_OVERVIEW.md** - Complete system architecture (3 apps, database, agents)
- **DATABASE_SCHEMA.md** - Authoritative database structure (37 tables)
- **FILE_STRUCTURE_AND_STANDARDS.md** - Repository organization and coding standards
- **ARCHIVE_INDEX.md** - Master list of archived/deprecated files

### Application Specifications
- **STUDENT_LMS.md** - Student onboarding app specification
- **TEAM_LEAD_MODULE_BUILDER.md** - Team lead PM tool specification
- **RESEARCHER_PLATFORM.md** - Faculty analytics platform specification

### Integration
- **NOTION_INTEGRATION.md** - Notion workspace architecture and API rules
- **NOTION_PAGE_RULES.md** - Rules for AI agents editing Notion pages
- **OATUTOR_ADAPTATION.md** - OATutor integration for interactive problems

### Agent System
- **AGENT_SYSTEM_OVERVIEW.md** - Three-agent system architecture with implementation details
- **AGENT_SAFETY_RULES.md** - Safety protocols for autonomous agents
- **AGENT_ERROR_LOGGING.md** - Error handling and troubleshooting protocols

## Usage

When conflicts arise between documents:
1. Canonical documents (this folder) always win
2. If canonical docs conflict internally, ask human for resolution
3. Update other docs to match canonical truth

## Updates

To update canonical docs:
1. Get explicit human approval
2. Document reason for change
3. Update affected downstream documentation
4. Notify all agents via AGENT_TEAM_CHAT.md
