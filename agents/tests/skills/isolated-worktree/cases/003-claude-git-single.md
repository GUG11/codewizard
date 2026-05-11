# Case 003: Claude Code Git Single Agent

## Target Engine

Claude Code

## Scenario

Claude Code is the only modifying agent. The repository's authoritative SCM is Git.

## Environment Evidence

- User says: "Use Claude Code for this local Git repo."
- `git rev-parse --show-toplevel` succeeds.
- No other modifying agents are active.

## User Prompt

Use Claude Code to make the logging change and create the local commit.

## Expected Behavior

- Uses `isolated-worktree`.
- Identifies Git as authoritative SCM.
- Loads `references/git.md` only.
- Uses the current checkout for the first modifying agent.
- Does not run `claude --worktree` solely for isolation.
- Finalizes with a Git commit and prints the commit SHA.

## Failure Signals

- Creates a Claude Code worktree even though there is only one modifying agent.
- Loads the Sapling reference.
- Claims Claude Code completion without verifying the Git commit.
