# Coding Mode

## Technical Priorities
- Prefer correctness first, then performance, then simplicity, then convenience unless the task says otherwise.
- Preserve existing repository patterns for module boundaries, naming, testing, and error handling unless the task requires otherwise.
- Check for broader impact before changing interfaces, data flow, state transitions, concurrency, persistence, security, performance, or backward compatibility.

## Coding Style & Naming Conventions
- Prefer small, focused functions and explicit data flow over hidden side effects.
- Use descriptive names and straightforward control flow.
- Name variables and functions clearly enough that comments are unnecessary.
- Keep one main return path per function. Use extra returns only for simple top-of-function guard clauses.
- Keep branch depth shallow in new or changed code by flattening conditions early.
- Catch errors only at boundaries that can recover, translate, retry, or add context. Do not use `try`/`catch` for normal control flow.
- Keep hierarchies shallow. Prefer composition, delegation, or explicit interfaces over deeper inheritance.

## Language-Specific Guides
- Load language-specific guidance on demand from `~/.codex/languages/` when the task materially involves that language.

## Testing Policy
- Do not create new tests unless the user explicitly asks for them.
- If a change would benefit from new or updated tests, recommend the smallest useful test coverage and wait for user approval before adding it.
- When correctness needs verification, run the lightest existing targeted checks that are sufficient for the change unless the user says not to.
- Ask before running broad, slow, destructive, or expensive test suites.
- When tests are requested, follow the repository's existing testing style and structure.
- Always report what was verified and what was not.

## Commit & Pull Request Guidelines
- Commit messages follow bracketed tags such as `[feat] add ...`.
- Allowed tags: `feat`, `fix`, `optimization`, `measurement`, `chore`, `log`.
- Use the local `commit-and-pr-summary` skill when the user asks to draft commit messages or pull request descriptions.
- Keep only policy here. Keep drafting workflow and output format in the skill.
- The `# Test` or `# Tests` section is human-owned. Do not fill it and do not claim tests were run by humans.

## Non-Negotiables
- Never refactor or reformat code unless explicitly instructed.
- Never introduce new dependencies unless they are necessary and the user explicitly approves them first.
- Never write explanatory comments except for command snippets that teach how to run scripts.
