# Isolated Worktree Rubric

Score each category from 0 to 2.

- `0`: failed or missing
- `1`: partial, noisy, or weak
- `2`: correct and useful

## Categories

| Category | 0 | 1 | 2 |
|---|---|---|---|
| Trigger | Did not use `isolated-worktree` | Used it late or inconsistently | Used it immediately for workspace policy |
| Environment Detection | Guessed platform/SCM or chose by convenience | Detected some context but missed authoritative source | Used user/repo evidence to identify platform and authoritative SCM |
| Reference Loading | Loaded wrong reference or both unnecessarily | Loaded correct reference plus unrelated material | Loaded only the matching Git or Sapling reference after SCM identification |
| Single vs Additional Agent | Always creates worktrees or never does | Handles one case but not the other | Single modifier uses current checkout; additional modifiers use isolated worktrees |
| SCM Commands | Uses wrong SCM, `git || sl`, or invented commands | Mostly correct but includes unsafe/noisy commands | Uses only authoritative SCM commands from the loaded reference |
| Commit Finalization | Success path: accepts non-commit artifact as completion. Failure path: fabricates a commit or claims completion after commit failure | Success path: creates commit but misses identifier or status check. Failure path: reports failure but omits whether a commit exists | Success path: creates Git/Sapling commit, prints identifier, checks remaining work. Failure path: correctly reports that no commit exists because commit creation failed, does not fabricate an identifier, and defers recovery to Failure Handling |
| Failure Handling | Cleans up, switches workflows, or loses work | Captures partial evidence but misses a safety step | Preserves worktree, captures evidence, avoids workflow switch, asks user |
| Final Report | Missing or vague | Reports some facts but omits key identifiers | Reports platform, SCM, worktree path, commit id/type, verification, cleanup |

## Required Evidence For Scores

For every score, cite the artifact that supports it:

- `case.md`
- `loaded-references.md`
- `commands.md`
- `final.md`
- transcript excerpts if available

Do not infer a passing score from intent alone.

Do not score cases skipped by engine filtering. Skipped cases should have `skip.md`, not `score.md`.

## Output Format

```markdown
# Score: <case-id>

| Category | Score | Evidence |
|---|---:|---|
| Trigger |  |  |
| Environment Detection |  |  |
| Reference Loading |  |  |
| Single vs Additional Agent |  |  |
| SCM Commands |  |  |
| Commit Finalization |  |  |
| Failure Handling |  |  |
| Final Report |  |  |

**Total:** <n>/16

## Strengths
- ...

## Weaknesses
- ...

## Recommended Skill Changes
- ...
```
