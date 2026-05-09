# Execute Mission Test Runner

Use this file as the single entry point for testing `execute-mission`.

## Goal

Evaluate whether `execute-mission` produces a source-traceable mission brief, implements the mission, verifies with observed facts, and reports final status without inventing requirements.

## Inputs

- Skill under test: `agents/codex/skills/execute-mission/SKILL.md`
- Rubric: `agents/tests/codex/skills/execute-mission/rubric.md`
- Cases: `agents/tests/codex/skills/execute-mission/cases/*.md`
- Fixture repo: `agents/tests/codex/skills/execute-mission/fixtures/tiny-repo`

## Run Procedure

1. Create a timestamped results directory:
   `agents/tests/codex/skills/execute-mission/results/YYYY-MM-DD-HHMMSS/`
2. Read the skill under test and the rubric.
3. For each case file, read the case completely.
4. Copy `fixtures/tiny-repo` to a fresh temp workspace under `/tmp/execute-mission-tests/<case-id>-<timestamp>/`.
5. Initialize the temp workspace as a git repo and commit the baseline:
   `git init && git add . && git -c user.name=Test -c user.email=test@example.com commit -m "baseline"`
6. In that temp workspace, run the case's `User Prompt` as the task, using `execute-mission`.
   If the case includes `Clarification Response`, provide that response only after the agent asks a focused clarification question.
7. Save artifacts under the case result directory:
   - `case.md`: copied test case
   - `transcript.md`: relevant implementation-agent conversation excerpts
   - `mission.md`: copied mission brief from `MISSION_BRIEF_PATH`
   - `diff.patch`: git diff after the run
   - `commands.md`: commands/checks run and notable output
   - `final.md`: final chat response/status
   - `score.md`: rubric score and evaluator notes
8. Score the run with `rubric.md`. If a separate evaluator agent is available, give it only the artifacts above and the rubric. If not, score from the artifacts after completing the run.
9. Write `summary.md` in the timestamped results directory with:
   - score table by case
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
