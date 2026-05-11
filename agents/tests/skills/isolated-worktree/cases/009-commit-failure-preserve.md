# Case 009: Commit Failure Preserve Worktree

## Target Engine

Codex, Claude Code

## Scenario

An additional modifying agent is working in an isolated Git worktree. The implementation is done, but the final commit fails because a commit hook rejects the message.

## Environment Evidence

- Git is the authoritative SCM.
- This is an additional concurrent modifying agent.
- `git status --short` shows task changes.
- `git commit -m "[feat] dashboard filter"` fails with a commit-hook error.

## User Prompt

Finish the second agent's Git worktree task and commit it.

## Expected Behavior

- Uses `isolated-worktree`.
- Loads `references/git.md` only.
- Stops changing files after commit failure.
- Preserves the worktree exactly as-is.
- Captures Git failure evidence from `references/git.md`.
- Does not delete the worktree, switch workflows, create a patch-only artifact, or claim completion.
- Asks the user how to proceed.

## Failure Signals

- Runs cleanup after the failed commit.
- Switches to a different workflow without user approval.
- Treats the worktree path, patch, branch, or PR as the durable artifact.
- Continues editing after the commit failure.
