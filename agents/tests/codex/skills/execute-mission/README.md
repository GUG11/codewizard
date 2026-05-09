# Execute Mission Skill Tests

This folder contains scenario tests for `agents/codex/skills/execute-mission`.

Run the harness by asking Codex:

```text
Run agents/tests/codex/skills/execute-mission/runner.md
```

The runner executes each case in a copied fixture repo, captures artifacts, scores the run with `rubric.md`, and writes a summary under `results/`.
