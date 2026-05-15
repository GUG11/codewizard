# Execute Mission Test Runner

Use this file as the single entry point for testing `execute-mission`.

## Goal

Evaluate whether `execute-mission` produces a source-traceable mission brief, implements the mission, verifies with observed facts, and reports final status without inventing requirements.

## Inputs

- Skill under test: `agents/skills/execute-mission/SKILL.md`
- Rubric: `agents/tests/skills/execute-mission/rubric.md`
- Cases: `agents/tests/skills/execute-mission/cases/*.md`
- Fixture repo: `agents/tests/skills/execute-mission/fixtures/tiny-repo`

## Run Procedure

1. Create a timestamped results directory:
   `agents/tests/skills/execute-mission/results/YYYY-MM-DD-HHMMSS/`
2. Read the skill under test and the rubric.
3. For each case file, read the case completely.
4. Copy `fixtures/tiny-repo` to a fresh temp workspace under `/tmp/execute-mission-tests/<case-id>-<timestamp>/`.
5. Initialize the temp workspace as a git repo and commit the baseline:
   `git init && git add . && git -c user.name=Test -c user.email=test@example.com commit -m "baseline"`
6. In that temp workspace, spawn a separate user subagent for every case.
   Give the user subagent only the case's `User Prompt` and `User Subagent` section.
   Do not include the `User Subagent`, `Expected Behavior`, `Failure Signals`, or fixture notes in the implementation agent's prompt.
7. Start the implementation agent with only the case's `User Prompt` as the task, using `execute-mission`.
   Do not add clarification hints, expected behavior, scoring criteria, or meta-coaching to the implementation-agent prompt.
   The implementation-agent prompt may include only unavoidable harness setup: the skill path, the temp workspace, and the exact `User Prompt`.
   If the implementation agent asks for clarification, route the exact question to the user subagent and pass back only the user subagent's answer.
   If the implementation agent presents a mission brief for approval, route the exact brief text to the user subagent.
   The user subagent has two operations: approve, or give feedback.
   The user subagent approves only when the brief matches its canonical intent.
   Each feedback response must refine one requirement or correct one intention.
   For simple cases, the implementation agent may proceed through approval without asking clarification; full credit still requires its final result to match the user subagent's canonical intent.
   For complex cases, the user subagent must answer only the specific dimension asked, or give only one mission-brief feedback item, and must not reveal unrelated canonical details.
   Continue the dialogue until the implementation agent completes, asks for more clarification, presents another brief for approval, or gets stuck.
8. Save artifacts under the case result directory:
   - `case.md`: copied test case
   - `transcript.md`: exact implementation-agent dialogue only, using the format below
   - `user-subagent.md`: structured user-subagent record, using the format below
   - `mission.md`: copied mission brief from `MISSION_BRIEF_PATH`
   - `diff.patch`: git diff after the run
   - `commands.md`: commands/checks run and notable output
   - `final.md`: final chat response/status
   - `score.md`: rubric score and evaluator notes
9. Score the run with `rubric.md`. If a separate evaluator agent is available, give it only the artifacts above and the rubric. If not, score from the artifacts after completing the run.
   Full score requires the final mission brief, implementation, and evidence to match the canonical intent stated by the user subagent.
10. Write `summary.md` in the timestamped results directory with:
   - score table by case
   - verdict by case: `PASS`, `PASS_WITH_CONCERNS`, or `FAIL`
   - repeated strengths
   - repeated weaknesses
   - recommended skill changes, if any

## Rules

- Do not grade from memory. Use saved artifacts.
- Do not count source code or the diff as satisfaction evidence.
- Do not fix the skill while running cases. Record failures first.
- Prefer direct fixture commands (`node scripts/test.js`, `node scripts/build.js`) so the harness does not depend on `npm` being available.
- Keep fixture changes inside `/tmp/execute-mission-tests/`.
- Leave this repository's unrelated worktree changes untouched.
- `transcript.md` must contain only authentic dialogue text: user turn, implementation-agent turn, user turn, implementation-agent turn.
- Write `transcript.md` as plain text dialogue, not as a table.
- Do not put headings, commands, file edits, context summaries, evaluator notes, hidden canonical intent, or scoring judgment in `transcript.md`.
- If exact dialogue wording is unavailable, write `MISSING`; do not reconstruct it from memory.

## Required Transcript Format

`transcript.md` must contain only the original words exchanged with the implementation agent. User-subagent answers count as `User` turns because they are the words returned to the implementation agent.

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
