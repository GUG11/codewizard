# Code Mission Test Runner

Use this file as the single entry point for testing `code-mission`.

## Goal

Evaluate whether human-invoked `code-mission` clarifies before creating a mission brief, produces a source-traceable mission brief, implements the mission, verifies with observed facts, and reports final status without inventing requirements. Also run each case without the skill to show the behavioral difference introduced by the skill. Measure interaction efficiency separately from behavioral quality and harness integrity.

## Inputs

- Skill under test: `plugins/codewizard/skills/code-mission/SKILL.md`
- Rubric: `agents/tests/skills/code-mission/rubric.md`
- Cases: `agents/tests/skills/code-mission/cases/*.md`
- Fixture repo: `agents/tests/skills/code-mission/fixtures/tiny-repo`

## Run Procedure

1. Create a timestamped results directory:
   `agents/tests/skills/code-mission/results/YYYY-MM-DD-HHMMSS/`
2. Read the skill under test and the rubric.
3. For each case file, read the case completely.
4. For each case, run two variants:
   - `with-skill`: explicitly invoke `code-mission`.
   - `without-skill`: do not load or mention `code-mission`; give the implementation agent only the case's `User Prompt` and unavoidable harness setup.
5. For each variant, copy `fixtures/tiny-repo` to a fresh temp workspace under `/tmp/code-mission-tests/<case-id>-<variant>-<timestamp>/`.
   For each `with-skill` variant, reserve `/tmp/code-mission-tests/<case-id>-with-skill-<timestamp>.mission-env` as an out-of-band harness record. Do not place this file inside the fixture workspace or the dialogue transcript.
6. Initialize the temp workspace as a git repo and commit the baseline:
   `git init && git add . && git -c user.name=Test -c user.email=test@example.com commit -m "baseline"`
7. In that temp workspace, spawn a separate user subagent for every case and variant.
   Give the user subagent only the case's `User Prompt` and `User Subagent` section.
   If repository instructions require a `CTX:` line, tell the user subagent to keep it non-disclosing; `CTX: simulate test user | FILES: none | CONSTRAINTS: answer only the requested dimension` is a safe default.
   Treat any trailer as part of the answer for exact capture. Its presence, absence, or wording does not affect validity unless it reveals hidden canonical intent, files implied only by that intent, or constraints not already stated in the answer body or previously revealed dialogue.
   Do not include the `User Subagent`, `Expected Behavior`, `Failure Signals`, or fixture notes in the implementation agent's prompt.
8. For the `with-skill` variant, start the implementation agent with only the case's `User Prompt` as the task, explicitly invoking `code-mission`.
   Do not add clarification hints, expected behavior, scoring criteria, or meta-coaching to the implementation-agent prompt.
   The implementation-agent prompt may include only unavoidable harness setup: the skill path, the temp workspace, the mission-environment record path, and the exact `User Prompt`.
   Before the dialogue begins, have the implementation agent record the resolved mission directory and thread ID without overriding either variable:
   `printf '%s\n%s\n' "${CODE_MISSION_DIR:-/tmp/docs/missions}" "$CODEX_THREAD_ID" > /tmp/code-mission-tests/<case-id>-with-skill-<timestamp>.mission-env`
   The implementation agent must use the skill's designated path exactly: `${CODE_MISSION_DIR:-/tmp/docs/missions}/${CODEX_THREAD_ID}.md`. Do not give it an alternate mission path, redirect the mission into the fixture workspace, or let it write the result artifact directly.
   Tell the implementation agent to address every response directly to the user. It must not give the coordinator instructions such as "ask the user" or wrap the user-facing message in relay directions.
   Relay the implementation agent's entire user-facing response verbatim. Do not extract, rewrite, or summarize a quoted question from a coordinator-facing response.
   If the implementation agent asks for clarification, route that entire response to the user subagent and pass back only the user subagent's exact answer.
   If the implementation agent presents a mission brief for approval, route that entire response verbatim to the user subagent. The response may present the brief through its exact canonical path or link; do not require the brief to be duplicated inline.
   The user subagent has two operations: approve, or give feedback.
   The user subagent approves only when the brief matches its canonical intent.
   Each feedback response must refine one requirement or correct one intention.
   The implementation agent must ask one clarification question at a time until every applicable branch is resolved before presenting a mission brief.
   The user subagent must answer only the specific dimension asked, or give only one mission-brief feedback item, and must not reveal unrelated canonical details.
   Continue the dialogue until the implementation agent completes, asks for more clarification, presents another brief for approval, or gets stuck.
9. For the `without-skill` variant, start the implementation agent with only the case's `User Prompt` as the task and without the skill path.
   Apply the same direct-address and whole-response verbatim relay rules as the `with-skill` variant.
   Route clarification questions to the user subagent if the implementation agent asks them.
   Do not route mission-brief approval unless the implementation agent independently asks for approval.
   Continue until the implementation agent completes, asks for more clarification, asks for approval, or gets stuck.
10. Save artifacts under the case result directory, grouped by variant:
   - `with-skill/case.md`: copied test case
   - `with-skill/transcript.md`: exact routed User/Implementation Agent dialogue, using the format below
   - `with-skill/user-subagent.md`: structured user-subagent record, using the format below
   - `with-skill/mission.md`: byte-for-byte copy of the completed brief from `MISSION_BRIEF_PATH`, created by the harness only after the run
   - `with-skill/mission-source.md`: canonical source path, observed `CODEX_THREAD_ID`, copy command, and byte-comparison result
   - `with-skill/diff.patch`: git diff after the run
   - `with-skill/commands.md`: commands/checks run, notable output, and the count and exact reason for every explicit hook block (`0` when none occurred)
   - `with-skill/final.md`: final chat response/status
   - `with-skill/metrics.md`: interaction-efficiency measurements, using the format below
   - `with-skill/score.md`: rubric score and evaluator notes
   - `without-skill/case.md`: copied test case
   - `without-skill/transcript.md`: exact routed User/Implementation Agent dialogue, using the format below
   - `without-skill/user-subagent.md`: structured user-subagent record, using the format below
   - `without-skill/diff.patch`: git diff after the run
   - `without-skill/commands.md`: commands/checks run, notable output, and the count and exact reason for every explicit hook block (`0` when none occurred)
   - `without-skill/final.md`: final chat response/status
   - `without-skill/metrics.md`: interaction-efficiency measurements, using the format below
   - `without-skill/score.md`: rubric score and evaluator notes
   - `comparison.md`: concise comparison of clarification, interaction efficiency, approval gate, canonical match, result trace quality, and final behavior between the two variants
11. Score both variants with `rubric.md`.
   For `with-skill`, full score requires the final mission brief, implementation, and result trace to match the canonical intent stated by the user subagent.
   For `without-skill`, use the same rubric as a baseline measurement; it is expected to lose workflow points when it lacks clarification, mission brief, approval gate, or mission status.
   Score `Mission Brief Format` directly from `<variant>/mission.md`. Check exact `code-mission` template structure: title, required section order, no extra sections, Formal Requirements table with `Requirement` and `Result`, valid `Approval Status`, `Mission Status`, `### Clarification Tree`, `### Clarified Intent`, and a recursive Clarification Tree whose leaves end with `Follow-ups: none`.
   For clarification fidelity, evaluate whether the saved tree preserves enough context to reconstruct the user's intent. Do not deduct for omitted choices when each answer is self-contained and no meaning is lost; deduct when an omitted choice makes the answer ambiguous or removes a material constraint. Evaluate tree structure by causal parentage rather than transcript chronology: independent questions belong at the top level, and follow-ups belong beneath the question whose answer triggered them.
   If a separate evaluator agent is available, score each variant from only that variant's artifacts and the rubric. If not, score from the artifacts after completing the run.
   Before scoring `with-skill`, read the recorded mission directory and thread ID, construct the expected source path as `<recorded-mission-directory>/<recorded-thread-id>.md`, and require the implementation agent's reported `MISSION_BRIEF_PATH` to match it exactly. Copy that source file to `with-skill/mission.md` and run a byte-for-byte comparison between source and copy. Record both environment values, expected and reported paths, copy command, and comparison result in `with-skill/mission-source.md`. A missing environment record, mismatched path, alternate path, or non-identical copy is a harness-integrity failure.
   Assess harness integrity separately from the skill score. Harness integrity checks artifact completeness, canonical mission-path use, exact mission copying, exact dialogue capture, exact whole-message routing, speaker attribution, hidden-intent isolation, and compliance by the user subagent. It does not score the implementation agent's skill behavior and must not change the skill score or verdict. If harness integrity fails, mark the evaluation invalid and exclude it from aggregate skill-effect claims until the harness defect is corrected.
   Authentic dialogue may contain Markdown headings, tables, commands, file-edit descriptions, status blocks, or `CTX:` lines. These are part of the captured turn and are not harness-integrity failures.
12. Write `summary.md` in the timestamped results directory with:
   - score table by case
   - with-skill score, without-skill score, and score delta by case
   - verdict by case for both variants: `PASS`, `PASS_WITH_CONCERNS`, or `FAIL`
   - one-line `with-skill` vs `without-skill` comparison by case
   - interaction-efficiency metrics and deltas by case
   - harness-integrity status by variant; exclude invalid variants from aggregate skill-effect claims
   - repeated strengths
   - repeated weaknesses
   - recommended skill changes, if any

## Rules

- Do not grade from memory. Use saved artifacts.
- Do not count source code or the diff as the satisfaction result.
- Do not fix the skill while running cases. Record failures first.
- Prefer direct fixture commands (`node scripts/test.js`, `node scripts/build.js`) so the harness does not depend on `npm` being available.
- Keep fixture changes inside `/tmp/code-mission-tests/`.
- Leave this repository's unrelated worktree changes untouched.
- The implementation agent writes only the canonical mission brief. The harness, not the implementation agent, creates `with-skill/mission.md` after execution.
- Do not accept a workspace-local `.code-mission/` file, a result-directory file, or any other alternate path as `MISSION_BRIEF_PATH`.
- Each variant's `transcript.md` must contain only authentic dialogue turns with explicit `User:` or `Implementation Agent:` speaker labels.
- Preserve every turn exactly and in order. Do not restructure the dialogue as a summary or as a table of speakers and messages.
- Text under `Implementation Agent:` must be the complete response delivered to the user subagent, not an internal response to the coordinator. Text under `User:` must be the complete response delivered back to the implementation agent.
- Do not extract only a quoted question, omit a mission brief, or relabel coordinator-facing relay instructions as an `Implementation Agent:` turn.
- Authentic turn content may contain Markdown headings, tables, commands, file-edit descriptions, status blocks, or context summaries such as `CTX:`.
- Do not add harness notes, evaluator notes, hidden canonical intent, or scoring judgment to `transcript.md` unless that text was actually sent to the implementation agent.
- If exact dialogue wording is unavailable, write `MISSING`; do not reconstruct it from memory.

## Required Transcript Format

Each variant's `transcript.md` must contain only the original words exchanged with the implementation agent. User-subagent answers count as `User` turns because they are the words returned to the implementation agent.

```markdown
User:
<exact initial `User Prompt` sent to the implementation agent, or MISSING>

Implementation Agent:
<exact agent words, or MISSING>

User:
<exact user-subagent answer returned to the implementation agent, or MISSING>
```

Content beneath either speaker label is unrestricted when it is authentic. Consecutive turns from the same speaker are allowed when they reflect the actual exchange.

`user-subagent.md` must separate hidden canonical intent from answers actually revealed:

```markdown
# User Subagent: <case-id>

## User Prompt
<exact `User Prompt` given to the user subagent>

## Hidden Canonical Intent
<canonical intent from the case's `User Subagent` section>

## Disclosure Rules
<rules the user subagent was told to follow>

## Answers Actually Revealed
| Turn | Agent Question Or Mission Brief | User-Subagent Response |
|---:|---|---|
| 1 | <exact question> | <exact answer returned to implementation agent> |

## Canonical Dimensions Not Revealed
- <canonical detail not revealed before implementation, or "None">
```

`metrics.md` must report interaction efficiency without changing the rubric score:

```markdown
# Interaction Metrics: <case-id> (<variant>)

| Metric | Value | Artifact Source |
|---|---:|---|
| Clarification questions | <n> | `transcript.md` |
| Applicable intent dimensions resolved before implementation | <n>/<total> | `transcript.md`, `user-subagent.md` |
| Redundant clarification questions | <n> | `transcript.md` |
| Mission brief presentations | <n> | `transcript.md` |
| Mission feedback rounds | <n> | `user-subagent.md` |
| Implementation Agent turns | <n> | `transcript.md` |
| Review rounds | <n> | `mission.md` or `final.md` |
```

Count only observable turns and rounds. A redundant question asks for information already established in the prompt or a prior answer. Do not treat one focused question with answer choices as multiple questions. Count mission feedback separately from approval; approval is not a feedback round.

`comparison.md` must summarize the skill effect without re-scoring the no-skill run:

```markdown
# Comparison: <case-id>

| Dimension | With Skill | Without Skill | Difference |
|---|---|---|---|
| Clarification |  |  |  |
| Interaction Efficiency |  |  |  |
| Mission Brief / Approval |  |  |  |
| Canonical Match |  |  |  |
| Result Trace |  |  |  |
| Final Behavior |  |  |  |

## Takeaway
<one concise paragraph explaining what the skill changed, if anything>
```
