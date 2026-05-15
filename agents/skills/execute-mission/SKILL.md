---
name: execute-mission
description: Use when modifying or creating code or code-adjacent project files, including tests, configs, scripts, and docs. Create a mission brief, get user approval, then implement, verify, and run bounded mission-completion review.
---

# Execute Mission

## Overview

Execute a coding mission from a human-owned request. Preserve the source of intent before coding, choose the implementation approach after inspecting the codebase, verify with evidence, and review the result against the mission brief.

This skill defines how to operate. It does not prescribe the implementation design.

## Workflow

### 1. Create and approve the mission brief

Create a mission brief and present it to the user for approval. If the user gives feedback, revise the brief and present it again. Proceed only after the user explicitly approves the current brief.

Use this structure:

```markdown
# Mission Brief: <short title>

## Initial User Request

<verbatim request that triggered the mission>

## User Feedback

- Round <n>: <verbatim user feedback or explicit approval of the mission brief>

## Formal Requirements

| Requirement | User's original word | Definition of Done | Evidence |
|---|---|---|---|
| ... | ... | ... | Pending |
```

For feedback and approval, record the user's exact words. Do not summarize, reinterpret, or convert them into your own intent. Approval must clearly approve the current mission brief; otherwise treat the message as feedback and present a revised brief again.

When the brief can be filled concretely, write it to:

`MISSION_BRIEF_PATH=/tmp/docs/missions/YYYY-MM-DD-<short-slug>.md`

Keep `MISSION_BRIEF_PATH` as the exact path to the saved brief for review and final reporting. Present it to the user for approval before implementation. Do not edit project files beyond the mission brief until the user explicitly approves the current brief.

If the user rejects, corrects, or questions the brief, revise `MISSION_BRIEF_PATH` from that feedback and present it again. Repeat until the user explicitly approves the current brief or the mission is blocked. When the user approves it, update `MISSION_BRIEF_PATH` so the last `User Feedback` entry records the exact approval words.

### 2. Implement the mission

Approval gate: implementation is forbidden until the saved mission brief's last `User Feedback` entry records exact user words that clearly approve the current mission brief.

Missing approval is not a concern, warning, or verification gap. It is a blocker.

Work mission-first after that approval check: use your judgment and available tools to achieve the approved mission brief.

If a `Definition of Done` condition requires logs or other diagnostic evidence, prefer existing logs first. If existing logs are insufficient, enhance an existing log statement before adding a new one. Add new logging only when needed for verification, and keep it as small as possible.

### 3. Review, verify, iterate, and report

After implementation, reload the saved mission brief from `MISSION_BRIEF_PATH`. Use the file contents as the ground truth for review, not memory of the brief.

Each review round verifies the mission:

- Treat the implementation as untrusted evidence, not the source of truth.
- Compare the diff to each formal requirement.
- For each requirement, exercise the changed behavior and update `Evidence` with concise observed facts: command/check run, result, and relevant data/logs/output. Existing code or the diff itself is not satisfaction evidence.
- If evidence cannot be produced, update the `Evidence` cell with what remains unverified and why.
- Report only mission-completion issues: missing requirements, incorrect behavior, regressions that violate the mission, or missing evidence.
- Do not invent new requirements during review.
- If a concern depends on missing context, label it as a question.

Maximum loop: 3 review rounds.

For each round:

1. Review against the mission brief.
2. If review passes, stop.
3. If review finds issues traceable to the mission, fix them and verify again.
4. If review finds ambiguity, scope change, or a non-trivial design question, stop and ask the human.
5. After the third review, stop no matter what and report final status.

After the loop ends, append the final status to `MISSION_BRIEF_PATH` using this format:

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
- `COMPLETE_WITH_CONCERNS`: Mission is implemented, but some risk or verification gap remains.
- `INCOMPLETE`: Some formal requirements are not satisfied.
- `BLOCKED`: Cannot proceed without human decision or missing external information.

In the chat response, report only the status, `MISSION_BRIEF_PATH`, remaining issues, and human decision needed. Do not duplicate the verification evidence; it lives in the mission brief's `Evidence` column.
