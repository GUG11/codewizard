# Isolated Worktree Skill Tests

This folder contains scenario tests for `agents/skills/isolated-worktree`.

Run with Codex:

```bash
codex "Run agents/tests/skills/isolated-worktree/runner.md"
```

Run with Claude Code:

```bash
claude "Run agents/tests/skills/isolated-worktree/runner.md"
```

The runner evaluates whether the skill selects the current checkout or an isolated worktree correctly, loads only the authoritative SCM reference, finalizes with a source-control commit, and preserves work on commit failure.
