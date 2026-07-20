# Code Mission Skill Tests

This folder contains scenario tests for `plugins/codewizard/skills/code-mission`.

Run with Codex & Claude Code:

```bash
codex "Run agents/tests/skills/code-mission/runner.md"
```

The runner executes each case twice in copied fixture repos: once with human-invoked `code-mission`, and once without the skill. It captures artifacts for both variants, scores skill behavior with `rubric.md`, reports interaction-efficiency metrics and harness integrity separately, writes a per-case comparison and score delta, and writes a summary under `results/`.
