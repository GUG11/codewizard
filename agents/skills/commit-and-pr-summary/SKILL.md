---
name: commit-and-pr
description: Draft commit messages and pull request descriptions from the current git changes while following repository-specific commit conventions, PR templates, and submission rules. Use when the user asks to write a commit message, prepare a PR description, summarize a diff for review or submission, or turn local changes into merge-ready text.
---

# Commit And PR

## Overview

Inspect the current git changes, infer the real scope of the work, and produce commit or pull request text that matches the repository's rules. Prefer repository instructions over generic conventions when they conflict.

## Workflow

### 1. Read the change and infer intent

- Read `git status -sb` to confirm the working set.
- Read `git diff --stat` and the relevant `git diff` or `git diff --cached` output before drafting anything.
- Read repository guidance that governs commit or PR text, such as `AGENTS.md`, contribution docs, or `.github` templates, if they exist.
- If the change spans unrelated concerns, call that out and draft text for only the scoped portion the user asked about.
- Identify the user-visible purpose, the technical mechanism, and the main risk or behavior change.
- Avoid inventing outcomes that are not supported by the diff.

### 2. Write commit messages

- Follow the repository's commit tag or subject format exactly when one is defined.
- Write a one-line message that captures the most critical change.
- If the diff contains multiple logical commits, say so and propose a split instead of forcing one vague message.

### 3. Write pull request descriptions

- Use this format unless the repository requires a stricter template:

```markdown
# Summary
Purpose:

Changes:
<several sentences to describe the key changes>

# Test
```

- Output raw markdown, don't render it.
- Fill `Purpose:` with one succinct sentence.
- Fill `Changes` with flowing prose, not bullet points. Describe what changed and how it works in plain language a non-expert reviewer could follow.
- Base the summary on the diff, not on assumptions about product intent.
- Leave the `# Test` section for the user to fill.

### 4. Validate before returning

- Check that every claim can be supported by the observed diff or repository instructions.
- Check that the output is concise and ready to paste without cleanup.

## Output rules

- If the user asks for both, return a commit message first and the PR description second.
- If the user asks for only one artifact, return only that artifact.
- When uncertainty remains because the diff is incomplete or ambiguous, state the gap briefly before drafting.
- Do not claim tests were run by humans.
- Do not include filler text, praise, or process narration inside the drafted artifact.
