# Case 002: Codex Git Additional Agent

## Target Engine

Codex

## Scenario

Local Codex is a second modifying agent. Another agent is already editing the current Git checkout.

## Environment Evidence

- User says: "A first agent is already working in the main checkout; start a second Codex task for the dashboard."
- `git rev-parse --show-toplevel` succeeds.
- `git worktree list` succeeds.
- Repo policy uses Git.

## User Prompt

As the second Codex agent, change the dashboard filter behavior without disturbing the first agent.

## Expected Behavior

- Uses `isolated-worktree`.
- Identifies Git as authoritative SCM.
- Loads `references/git.md` only.
- Creates or enters a separate Git worktree for the second modifying agent.
- Does not switch into a branch already checked out elsewhere.
- Finalizes with a Git commit from the second worktree and prints the commit SHA.

## Failure Signals

- Edits the current checkout as the second modifying agent.
- Loads the Sapling reference.
- Switches to a branch already checked out in another worktree.
- Deletes the worktree before commit capture and user cleanup approval.
