# Isolated Worktree Test Runner

Use this file as the single entry point for testing `isolated-worktree`.

## Goal

Evaluate whether `isolated-worktree` keeps the main workflow concise while enforcing:

- one modifying agent uses the current checkout
- each additional concurrent modifying agent uses a separate worktree
- authoritative SCM is identified before command-reference loading
- only the Git or Sapling SCM reference matching the authoritative SCM is loaded
- completion requires a Git commit or Sapling SCM commit
- failed commit creation preserves the worktree and asks the user

## Inputs

- Skill under test: `agents/skills/isolated-worktree/SKILL.md`
- Git reference: `agents/skills/isolated-worktree/references/git.md`
- Sapling reference: `agents/skills/isolated-worktree/references/sapling.md`
- Rubric: `agents/tests/skills/isolated-worktree/rubric.md`
- Cases: `agents/tests/skills/isolated-worktree/cases/*.md`

## Run Procedure

1. Create a timestamped results directory:
   `agents/tests/skills/isolated-worktree/results/YYYY-MM-DD-HHMMSS/`
2. Identify the current engine as Codex or Claude Code from the process running this runner.
3. Read the skill under test and the rubric.
4. For each case file, read the case completely.
5. Read the case's `Target Engine` section.
6. If the current engine is Codex and the case targets only Claude Code, skip it.
7. If the current engine is Claude Code and the case targets only Codex, skip it.
8. If the case targets the current engine or targets both engines, run the case as a transcript evaluation task. Do not modify this repository while evaluating a case.
9. If a case provides `Environment Evidence`, use it as the only simulated environment. Do not invent hidden context.
10. Save artifacts under the case result directory:
   - `case.md`: copied test case
   - `transcript.md`: relevant evaluator/agent reasoning excerpts or simulated command plan
   - `loaded-references.md`: which skill references were loaded and why
   - `commands.md`: commands the agent would run or avoid, with rationale
   - `final.md`: expected final report or failure report
   - `score.md`: rubric score and evaluator notes
11. For skipped cases, save:
   - `case.md`: copied test case
   - `skip.md`: current engine, target engine, and skip reason
12. Score only the cases that target the current engine with `rubric.md`. If a separate evaluator agent is available, give it only the artifacts above and the rubric.
13. Write `summary.md` in the timestamped results directory with:
   - score table by case
   - skipped case table
   - repeated strengths
   - repeated weaknesses
   - recommended skill changes, if any

## Rules

- Do not grade from memory. Use saved artifacts.
- Do not score skipped cases.
- Do not load both SCM references unless the case says the authoritative SCM is ambiguous.
- Do not accept `git || sl` fallback validation as passing behavior.
- Do not accept pull requests, branches, shelves, patches, platform task pages, or worktree paths as durable artifacts.
- Treat "CloudCode" in legacy prompts as Claude Code.
- Leave this repository's unrelated worktree changes untouched.
