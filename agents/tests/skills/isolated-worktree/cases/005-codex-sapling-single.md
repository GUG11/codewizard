# Case 005: Codex Sapling Single Agent

## Target Engine

Codex

## Scenario

Local Codex is the only modifying agent. The repository's authoritative SCM is Sapling SCM.

## Environment Evidence

- User says: "This repo uses Sapling SCM."
- `sl root` succeeds.
- `sl status` succeeds.
- No other modifying agents are active.

## User Prompt

Use local Codex to update the config behavior and commit it.

## Expected Behavior

- Uses `isolated-worktree`.
- Identifies Sapling SCM as authoritative SCM.
- Loads `references/sapling.md` only.
- Uses the current checkout for the first modifying agent.
- Does not run Git detection as a fallback validator after Sapling is identified.
- Finalizes with a Sapling SCM commit and prints the `sl whereami` identifier.

## Failure Signals

- Loads the Git reference.
- Uses Git commands because `.git` metadata is also present.
- Creates a worktree for the only modifying agent.
- Treats a shelf, patch, or workspace path as completion.
