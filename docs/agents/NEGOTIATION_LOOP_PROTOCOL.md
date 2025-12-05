# NEGOTIATION_LOOP_PROTOCOL.md

## Continuous Negotiation Loop for 3 Agents (VS Code / Cursor)

**Version:** 1.0  
**Date:** 2025-12-03  
**Purpose:** Enable 3 AI agents to collaborate on a problem through file-based negotiation

---

## Overview

You are one of three AI agents collaborating on a problem given by the user.

The sequence for this agent is:

1. The user gives you a problem and tells you which agent you are (Alpha, Beta, or Gamma).
2. You create your own initial plan and write it into the Team Chat file.
3. Then you begin using this file to run the negotiation phase:
   - Wait for the other two agents to post their initial plans
   - Compare all three plans
   - Negotiate toward the best pathway
   - Stop when there is a shared agreement OR when you have disagreed up to 5 times
   - Then report back to the user and stop

You are running in a continuous session (e.g., VS Code), so you can:
- Repeatedly open and read files
- Check for updates
- Loop until the negotiation is complete

---

## Files

There are two key files:

### 1. This file (the negotiation loop instructions)
`NEGOTIATION_LOOP_PROTOCOL.md`

### 2. Team Chat file (shared by all 3 agents)
A markdown file given by the user, e.g., `team_chat_<topic>.md`

All agent messages should be written there with numbered entries:

```markdown
## [1] Agent Alpha - HH:MM
[Content]

## [2] Agent Beta - HH:MM
[Content]

## [3] Agent Gamma - HH:MM
[Content]
```

---

## Important Assumptions

Before you start following this file:

1. The user has given you a problem.
2. The user has told you which agent you are (Alpha, Beta, or Gamma).
3. You have already written your initial plan into the Team Chat.
4. The other two agents will also:
   - Read the same problem
   - Write their own initial plans into the Team Chat

This file only controls the **negotiation phase** after the initial plans exist.

---

## Key Definitions

### What is a "Disagreement"?
A disagreement is when you **cannot accept a proposed plan as-is** and require changes before agreeing. Minor suggestions or clarifications do not count as disagreements.

### Message Numbering
Each message in the Team Chat must be numbered sequentially:
```markdown
## [N] Agent <Name> - HH:MM
```
This makes it easy to identify "messages after my last message" (any message numbered higher than your last).

---

## Global Behavior

During negotiation:

1. You wait for the other agents by repeatedly re-reading the Team Chat.
2. Once all three initial plans are present, you:
   - Compare plans
   - Propose a best or merged pathway
   - Respond to further messages from the others
3. You keep a textual counter: `MyDisagreementsSoFar: N`
4. You keep a polling counter: `MyPollCount: N`

**You must stop and go to the user when:**
- A clear shared plan is agreed, OR
- `MyDisagreementsSoFar` reaches 5, OR
- `MyPollCount` reaches 30 (no response from other agents)

---

## STEP 0 — Initial Setup (Run Once)

1. Confirm the user has told you:
   - Which agent you are (Alpha, Beta, or Gamma)
   - The Team Chat file path (e.g., `team_chat_bootstrap.md`)

2. Open the Team Chat file.

3. Confirm that your own initial plan is already present, clearly labeled with your agent identifier and a message number.

4. Initialize your counters:
   - Search for your last `MyDisagreementsSoFar:` in the Team Chat. If none exists, start at 0.
   - Set `MyPollCount: 0`

5. After this, move to **STEP 1**.

---

## STEP 1 — Wait for Both Other Initial Plans

**Goal:** Do not start negotiation until both other agents have posted their own initial plans.

You will loop inside STEP 1 until that is true.

### STEP 1A — Go Back to the Team Chat

1. Re-open the Team Chat file.
2. Read it from top to bottom.
3. Identify:
   - Your own initial plan message
   - Whether there is at least one initial plan from each of the two other agents
4. Use the `## [N] Agent <Name>` labels to distinguish messages.

### STEP 1B — Check If All Initial Plans Exist

**If** any of the other two agents has not yet posted an initial plan:
1. Increment `MyPollCount` by 1.
2. If `MyPollCount` reaches 30:
   - Stop and report to the user: "Waiting for other agents — no response after 30 checks."
3. Otherwise, do not write anything.
4. Go back to **STEP 1A** and re-read the Team Chat again.

**If** both other agents have posted their initial plans:
- Reset `MyPollCount: 0`
- Move to **STEP 2**.

---

## STEP 2 — First Comparison of Plans

**Goal:** Now all three initial plans exist. You must compare them and provide your first negotiation response.

1. Re-open the Team Chat file (if not already open).

2. Read all three initial plans:
   - Yours
   - Other Agent 1's
   - Other Agent 2's

3. Compare the plans and decide:
   - Is there one plan you think is clearly best?
   - Is there a way to merge ideas into a better combined plan?
   - Are there parts you cannot accept as-is (disagreements)?

4. Note the highest message number currently in the file. Your new message will be that number + 1.

5. Append a new message to the Team Chat that:
   - Uses the format `## [N] Agent <YourName> - HH:MM`
   - Clearly states your position:
     - What parts you agree with
     - What parts you disagree with, and why
   - Proposes a best pathway (either one plan, or a merged plan)

6. If you disagreed with any part of the others' plans:
   - Increase your `MyDisagreementsSoFar` by 1
   - Include in your message: `MyDisagreementsSoFar: <updated N>`

7. After writing this comparison message, check the **Stopping Conditions** (see below).
   - If a stopping condition is met: mark the Team Chat as DONE and go to **FINAL REPORT**.
   - If not, move to **STEP 3**.

---

## STEP 3 — Ongoing Negotiation Loops

After the initial comparison, negotiation proceeds in cycles:
- Other agents read your comparison
- They respond
- You then respond to their updates
- Repeat until agreement or 5 disagreements

You will alternate between:
- **STEP 3A** – Wait for others to respond to you
- **STEP 3B** – Respond to their updates

### STEP 3A — Wait for Team Response to Your Last Message

1. Note your last message number (from when you last wrote).
2. Re-open the Team Chat file.
3. Check if there are any messages with numbers higher than your last message.

**If** no new messages from other agents since your last message:
1. Increment `MyPollCount` by 1.
2. If `MyPollCount` reaches 30:
   - Stop and report to the user: "Waiting for other agents — no response after 30 checks."
3. Otherwise, do not write anything.
4. Go back to the beginning of **STEP 3A** and re-read the Team Chat again.

**If** there are new messages from other agents after your last message:
- Reset `MyPollCount: 0`
- Move to **STEP 3B**.

### STEP 3B — Respond to New Team Updates

1. Re-open the Team Chat file (if needed).

2. Read all messages written after your last message.

3. Decide:
   - How do these updates change your view of the best plan?
   - Do you still disagree with anything? New disagreements?
   - Is there now a clear shared plan emerging?

4. Note the highest message number. Your new message will be that number + 1.

5. Append a new message to the Team Chat that:
   - Uses the format `## [N] Agent <YourName> - HH:MM`
   - Responds directly to the latest messages
   - States clearly what you agree with
   - States clearly what you disagree with (if anything), using phrases like:
     - "I disagree with Agent X on <point> because <reason>."
     - "I cannot accept this plan as-is because <reason>."

6. If you disagreed this turn:
   - Increase your `MyDisagreementsSoFar` by 1
   - Include: `MyDisagreementsSoFar: <updated N>`

7. **Write Collision Check:** After writing, re-read the file and confirm your message appears correctly with the expected number. If the numbering is wrong (another agent wrote at the same time), re-read the file and adjust your message number, then re-append.

8. After writing this message, check the **Stopping Conditions**.
   - If a stopping condition is met: mark the Team Chat as DONE and go to **FINAL REPORT**.
   - If not, go back to **STEP 3A** and repeat the negotiation cycle.

---

## Stopping Conditions

You must exit the negotiation loop and report to the user when any of these occur:

### 1. Agreement is Reached

You should treat the negotiation as agreed when:
- There is one clear plan in the Team Chat (may be one of the original plans or a merged plan), AND
- Both other agents have either:
  - Explicitly stated agreement (e.g., "I agree with this plan."), OR
  - Restated the plan positively with no remaining objections

**If so:**

Append a final message to the Team Chat:
```
## [N] Agent <YourName> - HH:MM

NegotiationStatus: DONE
AgreementReached: true
FinalPlan: <brief summary of the agreed plan>
MyDisagreementsSoFar: N
```

Then go to **FINAL REPORT**.

### 2. You Have Disagreed 5 Times

If your `MyDisagreementsSoFar` reaches 5:

Append a final message to the Team Chat:
```
## [N] Agent <YourName> - HH:MM

NegotiationStatus: DONE
AgreementReached: false
MyDisagreementsSoFar: 5
UnresolvedIssues: <brief summary of main disagreements>
```

Then go to **FINAL REPORT**.

### 3. Polling Timeout (No Response)

If your `MyPollCount` reaches 30:

Report to user directly (no Team Chat message needed):
> "Negotiation paused: Waiting for other agents — no response after 30 checks. Please verify other agents are running."

### 4. Negotiation Already Marked DONE

At any time, if you re-open the Team Chat and see:
```
NegotiationStatus: DONE
```
written by any agent:

- Treat the negotiation as finished.
- Go directly to **FINAL REPORT**.

---

## Final Report to User

When the negotiation is done (you see or write `NegotiationStatus: DONE`):

1. Re-open and re-read the entire Team Chat file one last time.

2. Prepare a short, clear summary for the user, including:
   - Whether `AgreementReached: true` or `false`
   - The final plan (if agreed)
   - OR the main unresolved disagreements (if not agreed)
   - Your final `MyDisagreementsSoFar: N`

3. Present this summary to the user in your final output.

4. **Stop the loop and end this run.**

---

## Summary of Flow (In Human Words)

1. You've already posted your plan.
2. **Step 1:** Keep going back to the Team Chat until both other agents have posted theirs (max 30 checks).
3. **Step 2:** Once all three plans exist, compare them and post your first negotiation message.
4. **Step 3:** Then loop:
   - Go back to chat
   - If no new messages → keep re-reading (max 30 checks)
   - If others replied → respond
   - Count disagreements as you go
5. If you reach 5 disagreements, or you all clearly agree on a plan, or you timeout waiting → mark DONE and go to the user with a report.

---

## Quick Reference Card

| Counter | Purpose | Limit | Action at Limit |
|---------|---------|-------|-----------------|
| `MyDisagreementsSoFar` | Track fundamental disagreements | 5 | End negotiation, report unresolved issues |
| `MyPollCount` | Track re-reads without new content | 30 | Pause and ask user to check other agents |

| Message Format | Example |
|----------------|---------|
| Normal message | `## [4] Agent Beta - 14:32` |
| Agreement | `NegotiationStatus: DONE` + `AgreementReached: true` |
| Disagreement limit | `NegotiationStatus: DONE` + `AgreementReached: false` |

---

## Example Team Chat Flow

```markdown
## [1] Agent Alpha - 14:00
**Initial Plan:** I propose we start by bootstrapping the database schema...

## [2] Agent Beta - 14:05
**Initial Plan:** I suggest we focus on the API endpoints first...

## [3] Agent Gamma - 14:08
**Initial Plan:** Infrastructure should come first - database, then API...

## [4] Agent Alpha - 14:15
I've reviewed both plans. I agree with Gamma that infrastructure should come first.
I disagree with Beta on starting with API - we need the database schema first.
**Proposed merge:** Database → API → Frontend
MyDisagreementsSoFar: 1

## [5] Agent Beta - 14:20
Fair point. I can accept database first. Revised position: Database → API → Frontend.
I agree with Alpha's merged proposal.

## [6] Agent Gamma - 14:22
I agree with the merged proposal: Database → API → Frontend.

## [7] Agent Alpha - 14:25
NegotiationStatus: DONE
AgreementReached: true
FinalPlan: Database schema first, then API endpoints, then Frontend components
MyDisagreementsSoFar: 1
```

---

**End of Protocol**
