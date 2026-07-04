# Git Worktree Reference

Use only after Git is identified as the repository's authoritative source control.

## Detect

```bash
git rev-parse --show-toplevel
git worktree list
git branch --show-current
git status --short
```

## Create Worktree

```bash
git worktree add ../<repo>-<task-slug> -b <branch-name>
cd ../<repo>-<task-slug>
```

If the target branch is already checked out elsewhere, do not `git switch` to it in another checkout. Inspect with:

```bash
git show <sha>
git worktree add --detach ../inspect-<task-slug> <sha>
```

## Finalize Commit

```bash
git status --short
git diff
git add <files>
git commit -m "[feat] <summary>"
git rev-parse HEAD
git status --short
```

Follow repo commit tag rules such as `[feat]`, `[fix]`, or `[chore]`.

## Commit Failure Evidence

```bash
git status --short
git diff
git diff --cached
git branch --show-current
git rev-parse --show-toplevel
```

## Cleanup

```bash
git worktree list
git worktree remove ../<repo>-<task-slug>
```

Do not remove a worktree until the commit exists and the user approves cleanup.
