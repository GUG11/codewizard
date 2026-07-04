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

The runner executes each case twice in copied fixture repos: once with human-invoked `execute-mission`, and once without the skill. It captures artifacts for both variants, scores both variants with `rubric.md`, writes a per-case comparison and score delta, and writes a summary under `results/`.
