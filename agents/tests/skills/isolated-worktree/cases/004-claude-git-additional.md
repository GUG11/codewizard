# Case 004: Claude Code Git Additional Agent

## Target Engine

Claude Code

## Scenario

Claude Code is an additional modifying agent in a Git repo. Another agent owns the current checkout.

## Environment Evidence

- User says: "A Codex agent is already editing the current checkout. Start Claude Code on a separate task."
- `git rev-parse --show-toplevel` succeeds.
- `git worktree list` succeeds.
- Claude Code is available.

## User Prompt

Run the second task with Claude Code and keep it isolated from the current checkout.

## Expected Behavior

- Uses `isolated-worktree`.
- Identifies Git as authoritative SCM.
- Loads `references/git.md` only.
- Uses Claude Code native `claude --worktree <task-slug>` when available, or a Git worktree fallback.
- Finalizes with a Git commit inside the isolated worktree and prints the commit SHA.
- Does not clean up the worktree without user approval.

## Failure Signals

- Edits the current checkout as the additional modifying agent.
- Treats Claude Code's workspace or report as the durable artifact.
- Loads the Sapling reference.
- Deletes the worktree before commit capture.
