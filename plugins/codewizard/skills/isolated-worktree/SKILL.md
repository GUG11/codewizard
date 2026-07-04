---
name: isolated-worktree
description: Use when Claude Code or local Codex may need isolated worktrees for concurrent work, finalized only as a Git commit or Sapling SCM commit.
---

# Isolated Worktree

Use this skill when modifying code and concurrent agents may touch the same codebase, the current checkout has unrelated user changes, or the task needs a separate execution workspace.

Scope:
- Agent platform: Claude Code or local Codex app/CLI only. Codex Cloud is out of scope.
- Source control: Git or Sapling SCM only.
- Durable artifact: Git commit or Sapling SCM commit only.

## Core Rules

1. The worktree is execution space; the commit is the artifact.
2. For one modifying agent, use the current checkout and commit there.
3. Each additional concurrent modifying agent must use its own isolated worktree.
4. Identify the authoritative source control first. Do not validate with `git || sl`; verify only the authoritative SCM.
5. Load only the matching reference after SCM identification:
   - Git: `references/git.md`
   - Sapling SCM: `references/sapling.md`
6. Do not create nested or duplicate worktrees when already inside the task worktree.
7. If final commit creation fails, preserve the worktree, capture evidence from the loaded reference, do not switch workflows, and ask the user.
8. Do not clean up a worktree until the commit exists and the user approves cleanup, or the user says the worktree is disposable.

## Detect

Use user instructions, repo policy, local docs, then metadata to identify the current platform and authoritative SCM.

```bash
pwd
rg -i "codex|claude|worktree|workspace|git|sapling|commit|source control" .
```

If Git is authoritative, load `references/git.md`.

If Sapling SCM is authoritative, load `references/sapling.md`.

If the authoritative SCM cannot be determined, stop and ask the user.

## Worktree Policy

Default:
- First modifying agent: stay in the current checkout.
- Additional concurrent modifying agents: create or enter isolated worktrees.

Use the worktree tool already provided by the environment:
- Claude Code: prefer native `claude --worktree <task-slug>`.
- Local Codex with Git and no native worktree: use Git worktree commands from `references/git.md`.
- Sapling SCM: use repo-documented Sapling worktree commands, or ask if none exist.

## Finish

Before reporting completion:
- inspect the diff using the loaded SCM reference
- create the Git or Sapling SCM commit
- print the commit identifier
- check for remaining uncommitted task work
- report platform, authoritative SCM, worktree path, commit type, commit identifier, verification, and cleanup status
