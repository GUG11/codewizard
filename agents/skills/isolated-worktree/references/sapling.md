# Sapling SCM Worktree Reference

Use only after Sapling SCM is identified as the repository's authoritative source control. The command-line tool is `sl`.

## Detect

```bash
sl root
sl status
sl whereami
```

## Create Worktree

Use the repo-documented Sapling worktree command. If none exists and the current task is not already in a platform-provided isolated worktree, ask the user for the exact command before creating one.

## Inspect Changes

Sapling has no staging area. Files shown by `sl status` are pending commit changes except unknown files, which must be added first.

```bash
sl status
sl diff
```

Add task-owned unknown files:

```bash
sl add <files>
```

Use broad add/remove bookkeeping only after inspecting `sl status`:

```bash
sl addremove
```

## Finalize Commit

```bash
sl status
sl diff
sl add <files>
sl commit -m "[feat] <summary>"
sl whereami
sl status
```

Use `sl show` when the committed message or diff must be inspected:

```bash
sl show
```

Follow repo commit tag rules such as `[feat]`, `[fix]`, or `[chore]`.

## Commit Failure Evidence

```bash
sl status
sl diff
sl whereami
sl root
```
