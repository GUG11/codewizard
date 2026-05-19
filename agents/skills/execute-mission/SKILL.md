---
name: execute-mission
description: Use when modifying or creating code or code-adjacent project files, including tests, configs, scripts, and docs. Create a mission brief, get user approval, then implement, verify, and run bounded mission-completion review.
---

# Execute Mission

## Overview

Execute a coding mission from a human-owned request. Preserve the source of intent before coding, choose the implementation approach after inspecting the codebase, verify with evidence, and review the result against the mission brief.

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

| Requirement | Test Plan | Definition of Done | Evidence |
|---|---|---|---|
| ... | ... | ... | Pending |

## Implementation Hints

- <only implementation hints or requested tools for implementation that are not standalone success outcomes>
```

For feedback and approval, record the user's exact words.

Build the brief from the user's current intent:

- A formal requirement is an outcome the mission must deliver, not an implementation step, tool invocation, safeguard, or generic best practice. Do not add default requirements such as "keep the change narrowly scoped", "preserve unrelated behavior", "do not add dependencies", "do not refactor", or "provide evidence".
- Keep a single-intent request as one requirement unless the user asks for multiple independently observable outcomes. Do not restate the same outcome as separate requirements for availability, semantics, scope, and evidence.
- `Test Plan` must specify exact runnable commands that exercise the code change. Expected observable results belong in `Definition of Done`, not `Test Plan`. Test, lint, build, or compile output may be listed as supplemental checks, but they are not requirement evidence for local development workflows.
- `Definition of Done` must name the observable completed state. It must not include verification commands, evidence claims, implementation mechanics, or generic scope-control language unless the user explicitly made one of those the outcome.
- For local development workflows, evidence must be logs captured from exercising the requirement. `arc lint`, compile/build output, test output, formatting, static search, code inspection, diffs, or claims that code exists are not requirement evidence unless the requirement itself is explicitly about that static artifact.
- Put implementation hints and requested tools for implementation in `Implementation Hints`.

Example: One-Intent Implementation Request

User request:

Add multiplication support to the calculator.

Bad:

```markdown
| Requirement | Test Plan | Definition of Done | Evidence |
|---|---|---|---|
| Add multiplication | Run relevant calculator tests. | Calculator supports multiplication. | Pending |
| Preserve existing calculator behavior | Run existing checks. | Addition and subtraction still work. | Pending |
| Keep the change simple | Review the diff. | No unrelated refactor. | Pending |
| Provide evidence | Run lint and inspect code. | The implementation is correct. | Pending |
```

Why it is bad:
- It splits one requested outcome into feature, preservation, scope, and evidence rows.
- That split makes each `Test Plan` non-actionable: no row exercises the calculator change end to end.
- The test plans do not name exact runnable commands.
- It turns normal operating constraints into mission requirements.
- It treats lint, diff review, and code inspection as evidence.
- Its `Definition of Done` cells are vague instead of naming observable command results.

Good:

```markdown
| Requirement | Test Plan | Definition of Done | Evidence |
|---|---|---|---|
| Add multiplication support to the calculator | Run `node scripts/check-calculator.js multiply 6 7`. Run `node scripts/check-calculator.js add 2 3`. Run `node scripts/check-calculator.js subtract 9 4`. | The multiply command prints `42`. The existing add and subtract commands still print `5`. | Pending |


## Implementation Hints
- Follow the existing operation dispatch style in the calculator module.
```

Approval must clearly approve the current mission brief; otherwise treat the message as feedback and present a revised brief again.

When the brief can be filled concretely, write it to:

`MISSION_BRIEF_PATH=/tmp/docs/missions/YYYY-MM-DD-<short-slug>.md`

Keep `MISSION_BRIEF_PATH` as the exact path to the saved brief for review and final reporting. Present it to the user for approval before implementation. Do not edit project files beyond the mission brief until the user explicitly approves the current brief.

If the user rejects, corrects, or questions the brief, revise `MISSION_BRIEF_PATH` from that feedback and present it again. Repeat until the user explicitly approves the current brief or the mission is blocked. When the user approves it, update `MISSION_BRIEF_PATH` so the last `User Feedback` entry records the exact approval words.

### 2. Implement the mission

Approval gate: implementation is forbidden until the saved mission brief's last `User Feedback` entry records exact user words that clearly approve the current mission brief.

Missing approval is not a concern, warning, or verification gap. It is a blocker.

Before editing project files, read `references/code-execution-policy.md`. Use it when implementing changes, verifying results, and reporting status.

Work mission-first after that approval check: use your judgment and available tools to achieve the approved mission brief.

If a `Test Plan` condition requires logs or other diagnostic evidence, prefer existing logs first. If existing logs are insufficient, enhance an existing log statement before adding a new one. Add new logging only when needed for verification, and keep it as small as possible.

### 3. Review, verify, iterate, and report

After implementation, reload the saved mission brief from `MISSION_BRIEF_PATH`. Use the file contents as the ground truth for the approved mission requirements, not memory of the brief.

Each review round verifies the mission:

- Treat the implementation as untrusted evidence, not the source of truth.
- Compare the diff to each formal requirement's `Definition of Done`.
- For each requirement, follow the `Test Plan`, exercise the changed behavior, and update `Evidence` with concise observed facts: command/check run, result, and relevant log lines. For local development workflows, logs are the requirement evidence. Existing code, diffs, `arc lint`, compile/build output, test output, formatting, static search, or claims that code exists are not satisfaction evidence unless the requirement itself is explicitly about that static artifact.
- Consider `Implementation Hints` when reviewing implementation choices, but do not convert those hints into new formal requirements during review.
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
