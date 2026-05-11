# Execute Mission Skill Tests

This folder contains scenario tests for `agents/skills/execute-mission`.

Run with Codex:

```bash
codex "Run agents/tests/skills/execute-mission/runner.md"
```

Run with Claude Code:

```bash
claude "Run agents/tests/skills/execute-mission/runner.md"
```

The runner executes each case in a copied fixture repo, captures artifacts, scores the run with `rubric.md`, and writes a summary under `results/`.
