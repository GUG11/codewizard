# Case 001: Codex Git Single Agent

## Target Engine

Codex

## Scenario

Local Codex app is the only modifying agent. The repository's authoritative SCM is Git.

## Environment Evidence

- User says: "Use Codex locally for this change."
- `git rev-parse --show-toplevel` succeeds.
- Repo policy uses Git commit tags such as `[fix]`.
- No other modifying agents are active.

## User Prompt

Fix the parser bug in the current repo and commit it locally.

## Expected Behavior

- Uses `isolated-worktree`.
- Identifies Git as authoritative SCM.
- Loads `references/git.md` only.
- Uses the current checkout; does not create a worktree for the first modifying agent.
- Finalizes with a Git commit and prints the commit SHA.
- Reports cleanup as not applicable because no extra worktree was created.

## Failure Signals

- Creates a Git worktree despite being the only modifying agent.
- Loads the Sapling reference.
- Uses `git || sl` fallback validation.
- Treats a branch, PR, patch, or worktree path as completion.
