# DEPRECATED

**This file is no longer canonical.**

**Replaced by:** (Being rewritten for V2)
**Reason:** Part of old agent system structure

**Archived:** 2025-12-01

---

# Agent Error Logging

## Purpose
Capture issues, ambiguities, unsafe actions, and corrective steps.

## Logged Fields
- timestamp
- agent_id
- action_attempted
- error_type
- resolution
- requires_user_review (bool)

## Rules
- Never suppress errors
- Never repair silently
- Always log before reattempting
