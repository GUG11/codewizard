# Case 007: Claude Code Sapling Single Agent

## Target Engine

Claude Code

## Scenario

Claude Code is the only modifying agent. The repository's authoritative SCM is Sapling SCM.

## Environment Evidence

- User says: "Use Claude Code in this Sapling SCM repo."
- `sl root` succeeds.
- `sl whereami` succeeds.
- No other modifying agents are active.

## User Prompt

Use Claude Code to make the API cleanup and commit the result in Sapling.

## Expected Behavior

- Uses `isolated-worktree`.
- Identifies Sapling SCM as authoritative SCM.
- Loads `references/sapling.md` only.
- Uses the current checkout because this is the first modifying agent.
- Does not use Git or Claude Code worktree isolation solely for one writer.
- Finalizes with a Sapling SCM commit and prints the commit identifier.

## Failure Signals

- Loads the Git reference.
- Creates an isolated worktree despite only one modifying agent.
- Accepts Claude Code's completion message without verifying the Sapling commit.
