# Code Mission Test Runner

Use this file as the single entry point for testing `code-mission`.

## Goal

Evaluate whether human-invoked `code-mission` clarifies before creating a mission brief, produces a source-traceable mission brief, implements the mission, verifies with observed facts, and reports final status without inventing requirements. Also run each case without the skill to show the behavioral difference introduced by the skill.

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
6. Initialize the temp workspace as a git repo and commit the baseline:
   `git init && git add . && git -c user.name=Test -c user.email=test@example.com commit -m "baseline"`
7. In that temp workspace, spawn a separate user subagent for every case and variant.
   Give the user subagent only the case's `User Prompt` and `User Subagent` section.
   Do not include the `User Subagent`, `Expected Behavior`, `Failure Signals`, or fixture notes in the implementation agent's prompt.
8. For the `with-skill` variant, start the implementation agent with only the case's `User Prompt` as the task, explicitly invoking `code-mission`.
   Do not add clarification hints, expected behavior, scoring criteria, or meta-coaching to the implementation-agent prompt.
   The implementation-agent prompt may include only unavoidable harness setup: the skill path, the temp workspace, and the exact `User Prompt`.
   If the implementation agent asks for clarification, route the exact question to the user subagent and pass back only the user subagent's answer.
   If the implementation agent presents a mission brief for approval, route the exact brief text to the user subagent.
   The user subagent has two operations: approve, or give feedback.
   The user subagent approves only when the brief matches its canonical intent.
   Each feedback response must refine one requirement or correct one intention.
   The implementation agent must ask at least one clarification question before presenting a mission brief.
   The user subagent must answer only the specific dimension asked, or give only one mission-brief feedback item, and must not reveal unrelated canonical details.
   Continue the dialogue until the implementation agent completes, asks for more clarification, presents another brief for approval, or gets stuck.
9. For the `without-skill` variant, start the implementation agent with only the case's `User Prompt` as the task and without the skill path.
   Route clarification questions to the user subagent if the implementation agent asks them.
   Do not route mission-brief approval unless the implementation agent independently asks for approval.
   Continue until the implementation agent completes, asks for more clarification, asks for approval, or gets stuck.
10. Save artifacts under the case result directory, grouped by variant:
   - `with-skill/case.md`: copied test case
   - `with-skill/transcript.md`: exact implementation-agent dialogue only, using the format below
   - `with-skill/user-subagent.md`: structured user-subagent record, using the format below
   - `with-skill/mission.md`: copied mission brief from `MISSION_BRIEF_PATH`
   - `with-skill/diff.patch`: git diff after the run
   - `with-skill/commands.md`: commands/checks run and notable output
   - `with-skill/final.md`: final chat response/status
   - `with-skill/score.md`: rubric score and evaluator notes
   - `without-skill/case.md`: copied test case
   - `without-skill/transcript.md`: exact implementation-agent dialogue only, using the format below
   - `without-skill/user-subagent.md`: structured user-subagent record, using the format below
   - `without-skill/diff.patch`: git diff after the run
   - `without-skill/commands.md`: commands/checks run and notable output
   - `without-skill/final.md`: final chat response/status
   - `without-skill/score.md`: rubric score and evaluator notes
   - `comparison.md`: concise comparison of clarification, approval gate, canonical match, result trace quality, and final behavior between the two variants
11. Score both variants with `rubric.md`.
   For `with-skill`, full score requires the final mission brief, implementation, and result trace to match the canonical intent stated by the user subagent.
   For `without-skill`, use the same rubric as a baseline measurement; it is expected to lose workflow points when it lacks clarification, mission brief, approval gate, or mission status.
   If a separate evaluator agent is available, score each variant from only that variant's artifacts and the rubric. If not, score from the artifacts after completing the run.
12. Write `summary.md` in the timestamped results directory with:
   - score table by case
   - with-skill score, without-skill score, and score delta by case
   - verdict by case for both variants: `PASS`, `PASS_WITH_CONCERNS`, or `FAIL`
   - one-line `with-skill` vs `without-skill` comparison by case
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
- Each variant's `transcript.md` must contain only authentic dialogue text: user turn, implementation-agent turn, user turn, implementation-agent turn.
- Write each `transcript.md` as plain text dialogue, not as a table.
- Do not put headings, commands, file edits, context summaries, evaluator notes, hidden canonical intent, or scoring judgment in any `transcript.md`.
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

`comparison.md` must summarize the skill effect without re-scoring the no-skill run:

```markdown
# Comparison: <case-id>

| Dimension | With Skill | Without Skill | Difference |
|---|---|---|---|
| Clarification |  |  |  |
| Mission Brief / Approval |  |  |  |
| Canonical Match |  |  |  |
| Result Trace |  |  |  |
| Final Behavior |  |  |  |

## Takeaway
<one concise paragraph explaining what the skill changed, if anything>
```
