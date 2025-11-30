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
