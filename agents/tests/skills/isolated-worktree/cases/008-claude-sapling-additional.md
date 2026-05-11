# Case 008: Claude Code Sapling Additional Agent

## Target Engine

Claude Code

## Scenario

Claude Code is an additional modifying agent. The repository's authoritative SCM is Sapling SCM.

## Environment Evidence

- User says: "Another agent is already working in the Sapling main checkout. Start Claude Code separately."
- `sl root` succeeds.
- `sl status` succeeds.
- Local docs describe how Claude Code should create or enter the Sapling worktree.

## User Prompt

Use Claude Code for the second task in a separate Sapling worktree and commit the result.

## Expected Behavior

- Uses `isolated-worktree`.
- Identifies Sapling SCM as authoritative SCM.
- Loads `references/sapling.md` only.
- Uses the local documented Sapling/Claude Code worktree command instead of inventing one.
- Finalizes with a Sapling SCM commit and prints the commit identifier.
- Preserves the worktree until user-approved cleanup.

## Failure Signals

- Uses Git worktree commands.
- Invents a Sapling worktree command when local docs are missing.
- Treats Claude Code's platform workspace as completion without a Sapling commit.
- Deletes or abandons the worktree before commit capture.
