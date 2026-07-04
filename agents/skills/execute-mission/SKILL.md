---
name: execute-mission
description: Human-invoked only. Use for non-trivial coding missions where the user wants deliberate clarification, a mission brief, approval, implementation, verification, and bounded mission-completion review.
---

# Execute Mission

## Overview

Execute a coding mission from a human-owned request. Preserve the source of intent before coding, choose the implementation approach after inspecting the codebase, verify with evidence, and review the result against the mission brief.

## Workflow

### 1. Clarification

This skill is human-invoked only. When invoked, treat the request as non-trivial and ambiguity-prone.

Before creating the mission brief, complete a clarification turn with the user. Follow [How to Clarify](references/how-to-clarify.md). Record the exact clarification question and user answer for the mission brief.

Do not create the mission brief while the Clarification Tree contains mission-critical `Remaining ambiguity`. Ask the next focused clarification question first.

### 2. Create and approve the mission brief

Create a mission brief and present it to the user for approval. If the user gives feedback, revise the brief and present it again. Proceed only after the user explicitly approves the current brief.

Use this structure:

```markdown
# Mission Brief: <short title>

## Initial User Request

<verbatim request that triggered the mission>

## Formal Requirements

| Requirement | Definition of Done (DoD) | Customized Fields ... | Result |
|---|---|---|---|
| ... | ... | ... | Pending |

## Approval Status
Pending

## Mission Status
Pending. Filled when the mission is complete.

## Clarification

### Clarification Tree
- <mission-critical ambiguity>: <why this must be clarified before the mission brief>
  - Asked: <verbatim clarification question>
  - Answered: <verbatim user answer>
  - Updated understanding: <what this answer makes clearer>
  - Remaining ambiguity: <none, or the next follow-up question needed before the mission brief>

### Clarified Intent
<concise synthesis of the current mission intent after clarification>

## User Feedback

- Round <n>: <verbatim user feedback or explicit approval of the mission brief>
```

For feedback and approval, record the user's exact words.

Build the brief from the user's current intent:

- Requirements are user-requested outcomes only; do not invent requirements. For example, do not add "keep the change narrow", "preserve unrelated behavior", "do not add dependencies", or "provide evidence".
- Keep a single-intent request as one requirement unless the user asks for multiple independently observable outcomes. Do not restate the same outcome as separate requirements for availability, semantics, scope, and evidence.
- `Definition of Done` is outcome-oriented: state the observable completed behavior or artifact. Code changes, compilation, and implementation steps are not Definition of Done.
- `Customized Fields ...` is a placeholder for user-requested or expert-skill fields. Replace or expand it with concrete columns required by the active work.
- `Result` is the trace pointer for each row. Before execution, set it to `Pending`.

Approval status values:

- `Pending`: the current mission brief has not been explicitly approved.
- `Approved`: the user explicitly approved the current mission brief.
- `Rejected`: the user rejected, questioned, or requested changes to the current mission brief. After revising the brief, reset `Approval Status` to `Pending`.


Example: One-Intent Implementation Request

User request:

Add multiplication support to the calculator.

Bad:

```markdown
| Requirement | Definition of Done (DoD) | Test Plan | Result |
|---|---|---|---|
| Add multiplication | Calculator supports multiplication. | Run relevant calculator checks. | Pending |
| Preserve existing calculator behavior | Addition and subtraction still work. | Run existing checks. | Pending |
| Keep the change simple | No unrelated refactor. | Review the diff. | Pending |
| Provide evidence | The implementation is correct. | Run lint and inspect code. | Pending |
```

Why it is bad:
- It splits one requested outcome into feature, preservation, scope, and evidence rows.
- That split makes each check non-actionable: no row exercises the calculator change end to end.
- The test plans do not name exact runnable commands.
- It turns normal operating constraints into mission requirements.
- It treats lint, diff review, and code inspection as evidence.
- Its `Definition of Done` cells are vague instead of naming observable command results. Never use "code was changed" or "code looks correct" as `Definition of Done`.

Good:

```markdown
| Requirement | Definition of Done (DoD) | Test Plan | Result |
|---|---|---|---|
| Add multiplication support to the calculator | The multiply command prints `42`. Existing add and subtract commands still print `5`. | Run `node scripts/check-calculator.js multiply 6 7`. Run `node scripts/check-calculator.js add 2 3`. Run `node scripts/check-calculator.js subtract 9 4`. | Pending |
```

Approval must clearly approve the current mission brief; otherwise treat the message as feedback, set `Approval Status` to `Rejected`, and present a revised brief with `Approval Status` reset to `Pending`.

When the brief can be filled concretely, write it to:

`MISSION_BRIEF_PATH=/tmp/docs/missions/YYYY-MM-DD-<short-slug>.md`

Keep `MISSION_BRIEF_PATH` as the exact path to the saved brief for review and final reporting. Present it to the user for approval before implementation. Do not edit project files beyond the mission brief until the user explicitly approves the current brief.

If the user rejects, corrects, or questions the brief, revise `MISSION_BRIEF_PATH` from that feedback, set `Approval Status` to `Pending`, and present it again. Repeat until the user explicitly approves the current brief or the mission is blocked. When the user approves it, update `MISSION_BRIEF_PATH` so `Approval Status` is `Approved` and the last `User Feedback` entry records the exact approval words.

### 3. Implement the mission

Missing approval is not a concern, warning, or verification gap. It is a blocker.

Before editing project files, read `references/code-execution-policy.md`. Use it when implementing changes, verifying results, and reporting status.

Work mission-first after that approval check: use your judgment and available tools to achieve the approved mission brief.

If a planned check requires logs or other diagnostic evidence, prefer existing logs first. If existing logs are insufficient, enhance an existing log statement before adding a new one. Add new logging only when needed for verification, and keep it as small as possible.

### 4. Review, verify, iterate, and report

After implementation, reload the saved mission brief from `MISSION_BRIEF_PATH`. Use the file contents as the ground truth for the approved mission requirements, not memory of the brief.

Each review round verifies the mission:

- Treat the implementation as untrusted evidence, not the source of truth.
- Compare the completed work to each formal requirement's `Definition of Done`.
- For each requirement, follow the relevant custom fields or skill-owned report format, exercise or investigate the row's completion condition, and update `Result` with the file path, link, section name, or concise observed result that shows where completion is demonstrated. Do not duplicate a detailed report or evidence block when another skill owns that format; point to it from `Result`. Prefer behavior logs or source data. Final command output is acceptable only when it directly shows the required result. Existing code, diffs, `arc lint`, compile/build output, generic test output, formatting, static search, or claims that code exists are not satisfaction results unless the mission explicitly asks for those artifacts.
- If a result cannot be produced, update the `Result` cell with what remains unverified and why.
- Report only mission-completion issues: missing requirements, incorrect behavior, regressions that violate the mission, or missing result links/artifacts.
- Do not invent new requirements during review.
- If a concern depends on missing context, label it as a question.

Maximum loop: 3 review rounds.

For each round:

1. Review against the mission brief.
2. If review passes, stop.
3. If review finds issues traceable to the mission, address them and verify again.
4. If review finds ambiguity, scope change, or a non-trivial design question, stop and ask the human.
5. After the third review, stop no matter what and report final status.

After the loop ends, replace the `Mission Status` section in `MISSION_BRIEF_PATH` with this format:

```markdown
## Mission Status

**Status:** COMPLETE | COMPLETE_WITH_CONCERNS | INCOMPLETE | BLOCKED
**Review Rounds:** <n>/3

**Remaining Issues:**
- <none or concise list>

**Human Decision Needed:**
- <none or concrete decision>
```

Status meanings:

- `COMPLETE`: Formal requirements satisfied and verified.
- `COMPLETE_WITH_CONCERNS`: Mission is completed, but some risk or verification gap remains.
- `INCOMPLETE`: Some formal requirements are not satisfied.
- `BLOCKED`: Cannot proceed without human decision or missing external information.

In the chat response, report only the status, `MISSION_BRIEF_PATH`, remaining issues, and human decision needed. Do not duplicate detailed reports or evidence; the mission brief's `Result` column points to where completion is demonstrated.
