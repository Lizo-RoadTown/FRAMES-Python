# Planning Template for Agentic Flow

**Task ID**: [Unique identifier]
**Task Description**: [What user requested]
**Date**: [YYYY-MM-DD]
**Planning Round**: [1, 2, or 3]

---

## Agent Plans (Round 1 - Parallel)

### Plan A: Interpreter (Gamma) - Technical Analysis

**Technical Breakdown**:
- [Infrastructure considerations]
- [Database operations needed]
- [API changes required]

**Risk Assessment**:
| Surface | Risk Level | Mitigation |
|---------|------------|------------|
| Notion  | [HIGH/MED/LOW] | [Strategy] |
| Database| [HIGH/MED/LOW] | [Strategy] |
| Codebase| [HIGH/MED/LOW] | [Strategy] |

**Execution Steps** (Technical Focus):
1. [Step 1]
2. [Step 2]
...

**Estimated Complexity**: [Low/Medium/High]

---

### Plan B: Validator (Alpha) - Safety & Ontology

**Ontology Alignment Check**:
- [ ] Task uses correct definition of "Module"
- [ ] Task respects canonical stores
- [ ] Task follows surface risk rules
- [ ] No hallucinated structure

**Safety Constraints**:
- MUST: [Required safety rules]
- MUST NOT: [Forbidden operations]
- REQUIRES VALIDATION: [What needs checking before commit]

**Execution Steps** (Safety Focus):
1. [Step 1 with safety notes]
2. [Step 2 with validation criteria]
...

**Quality Requirements**:
- [What "done" looks like]
- [Success criteria]

---

### Plan C: Optimizer (Desktop Claude) - Builder-Ready

**Builder Instructions** (Crystal Clear):

**Prerequisites**:
- [ ] Files that must exist
- [ ] Database state required
- [ ] Environment variables needed

**Step-by-Step Execution**:
1. [Action verb] [specific target] [expected outcome]
   - If unclear: [Escalation instruction]
   - Validation: [How to check success]

2. [Next step]
...

**Simplifications Made**:
- [What was complex in other plans]
- [How this plan reduces confusion]

**Dependencies & Sequencing**:
- Step X must complete before Step Y because [reason]

---

## Critiques (Round 2 - Cross-Review)

### Gamma Critiques Alpha & Desktop Claude:
**On Alpha's Plan**:
- ✅ Strengths: [What's good]
- ⚠️ Issues: [Technical problems]
- 💡 Suggestions: [Improvements]

**On Desktop Claude's Plan**:
- ✅ Strengths: [What's good]
- ⚠️ Issues: [Missing technical details]
- 💡 Suggestions: [Improvements]

### Alpha Critiques Gamma & Desktop Claude:
**On Gamma's Plan**:
- ✅ Strengths: [What's good]
- ⚠️ Issues: [Safety or ontology violations]
- 💡 Suggestions: [Improvements]

**On Desktop Claude's Plan**:
- ✅ Strengths: [What's good]
- ⚠️ Issues: [Quality concerns]
- 💡 Suggestions: [Improvements]

### Desktop Claude Critiques Gamma & Alpha:
**On Gamma's Plan**:
- ✅ Strengths: [What's good]
- ⚠️ Issues: [Too complex for Builder]
- 💡 Suggestions: [Simplifications]

**On Alpha's Plan**:
- ✅ Strengths: [What's good]
- ⚠️ Issues: [Unclear instructions]
- 💡 Suggestions: [Clarity improvements]

---

## Revised Plans (Round 3 - Post-Critique)

### Gamma's Revised Plan:
[Incorporating feedback from Alpha and Desktop Claude]

### Alpha's Revised Plan:
[Incorporating feedback from Gamma and Desktop Claude]

### Desktop Claude's Revised Plan:
[Incorporating feedback from Gamma and Alpha]

---

## Consensus Assessment

**Areas of Agreement**:
- [What all three plans agree on]

**Areas of Disagreement**:
| Aspect | Gamma Says | Alpha Says | Desktop Claude Says |
|--------|------------|------------|---------------------|
| [Topic] | [Position] | [Position] | [Position] |

**Recommended for Human Review**:
- [Decisions that need human input]

---

## Human Mediation Section

**Selected Plan**: [A / B / C / Merged]

**If Merged**:
- Infrastructure approach: [From Gamma's plan]
- Safety constraints: [From Alpha's plan]
- Execution sequencing: [From Desktop Claude's plan]

**Modifications**:
- [Any human adjustments]

**Approval**: ✅ APPROVED / ⏸️ NEEDS REVISION

---

## Builder Handoff

**Assigned to**: Agent Beta
**Plan Version**: [Final approved version]

**Builder Receives**:
1. Clear step-by-step instructions
2. Safety constraints (must-follow)
3. Validation criteria (what Delta will test)
4. Escalation protocol (when to ask for help)

**Builder Commits to**:
- [ ] Follow plan exactly
- [ ] No improvisation
- [ ] Escalate if unclear
- [ ] Provide diffs and summaries

---

## Testing & Feedback (Post-Execution)

**Delta's Test Results**:
- [UI tests: Pass/Fail]
- [API tests: Pass/Fail]
- [Integration tests: Pass/Fail]

**Feedback to Planning Trio**:

**To Gamma**:
- [Infrastructure plan effectiveness]
- [Database operations success]

**To Alpha**:
- [Ontology compliance results]
- [Safety constraint effectiveness]

**To Desktop Claude**:
- [Builder instruction clarity]
- [Sequencing effectiveness]

**Lessons Learned**:
- [What worked]
- [What to improve next time]

---

**End of Planning Document**
