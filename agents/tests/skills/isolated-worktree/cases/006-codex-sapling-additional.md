# Case 006: Codex Sapling Additional Agent

## Target Engine

Codex

## Scenario

Local Codex is an additional modifying agent. The repository's authoritative SCM is Sapling SCM.

## Environment Evidence

- User says: "This is a Sapling repo; one agent is already changing the main checkout."
- `sl root` succeeds.
- `sl status` succeeds.
- Local docs mention a Sapling worktree command.

## User Prompt

As the second local Codex agent, implement the metrics change in an isolated workspace and commit it.

## Expected Behavior

- Uses `isolated-worktree`.
- Identifies Sapling SCM as authoritative SCM.
- Loads `references/sapling.md` only.
- Uses the repo-documented Sapling worktree command or asks for it if absent.
- Finalizes with a Sapling SCM commit and prints the `sl whereami` identifier.
- Does not use Git worktree commands.

## Failure Signals

- Uses Git commands in the Sapling repo.
- Proceeds to invent a Sapling worktree command when local docs are absent.
- Edits the current checkout as an additional modifying agent.
- Treats a non-commit artifact as completion.
