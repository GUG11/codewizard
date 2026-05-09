---
name: execute-mission
description: Use when modifying or creating code or code-adjacent project files, including tests, configs, scripts, and docs. Create a mission brief before editing, then implement, verify, and run bounded mission-completion review.
---

# Execute Mission

## Overview

Execute a coding mission from a human-owned request. Preserve the source of intent before coding, choose the implementation approach after inspecting the codebase, verify with evidence, and review the result against the mission brief.

This skill defines how to operate. It does not prescribe the implementation design.

## Workflow

### 1. Create the mission brief

Before editing code, create a mission brief with this structure:

```markdown
# Mission Brief: <short title>

## Source of Intent

**Initial User Request:** <verbatim request that triggered the mission>

**Clarifications:**
- <mission-shaping user clarification, or "None">

**Interpreted Intent:** <brief paraphrase, no new scope>

## Formal Requirements

| Requirement | Source | Done When | Evidence |
|---|---|---|---|
| ... | ... | ... | Pending |
```

Before writing the file, try to fill this structure from the user's request and available context.

Use the incomplete mission brief as the clarification instrument:

- Can you copy the original prompt verbatim?
- Can you capture only mission-shaping user clarifications, without copying the whole dialogue?
- Can you paraphrase the interpreted intent briefly without adding scope?
- Can each `Requirement` cite a real source: the initial user request, explicit human clarification, repo policy, existing public contract, existing tests, or existing docs?
- Can each `Done When` cell describe the verification method that proves the requirement?
- If verification needs logs, debug output, screenshots, response bodies, generated files, or other diagnostic evidence, does `Done When` say so explicitly?

If all fields can be filled without guessing, proceed directly to writing the brief. If any required field or table cell cannot be filled without guessing, ask the smallest focused clarification needed for that field.

Repeat this until the mission brief can be filled concretely. Let the incomplete mission brief reveal what needs to be asked.

When the brief can be filled concretely, write it to:

`MISSION_BRIEF_PATH=/tmp/docs/missions/YYYY-MM-DD-<short-slug>.md`

Keep `MISSION_BRIEF_PATH` as the exact path to the saved brief for review and final reporting.

### 2. Implement the mission

Work mission-first: use your judgment and available tools to achieve the mission brief.

If a `Done When` condition requires logs or other diagnostic evidence, prefer existing logs first. If existing logs are insufficient, enhance an existing log statement before adding a new one. Add new logging only when needed for verification, and keep it as small as possible.

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
