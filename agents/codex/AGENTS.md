# General Coding Guidelines
## Rule Priority
- Apply rules in this order when conflicts exist:
1. `Don't (Zero Tolerance)`
2. `Do`
3. Language-specific and cross-language coding rules
4. Research requirements
5. Commit and PR formatting rules

## Coding Style & Naming Conventions
### Cross-Language Core Rules (applies to Python, C++, and other languages)
- Prefer small, focused functions and explicit data flow over hidden side effects.
- Use descriptive names and keep control flow easy to follow.
- Prefer minimal, local changes that solve the task without broad refactors.
- Do not introduce new dependencies unless required by the task and approved.
- Always write high-performance CPU and GPU code.
- Name variables and functions clearly enough that comments are unnecessary.

### Python (specialized)
- Use 4-space indentation and standard PEP 8 naming (`snake_case` for functions/variables, `CamelCase` for classes).
- Add type hints where they materially improve readability or API clarity.
- Use list/dict/set comprehensions when they improve clarity; avoid dense one-liners that reduce maintainability.
- Keep imports explicit and minimal; avoid wildcard imports.

### C++ (specialized)
- Follow modern C++ style (C++17 or above when available) with RAII and deterministic resource ownership.
- Prefer `std::unique_ptr` and stack allocation by default; use `std::shared_ptr` only with clear shared-lifetime needs.
- Prefer `const` correctness, references over raw pointers for non-null parameters, and `nullptr` over `NULL`.
- Favor `std::vector`/STL containers and algorithms over manual memory management and handwritten loops when equivalent.
- Keep headers lean: forward declare where practical, minimize transitive includes, and avoid implementation logic in headers unless template-driven.
- Isolate performance-critical paths and document only non-obvious invariants.

### Other Languages (general guide)
- Follow the idiomatic style guide and formatter/linter conventions of the target language and repository.
- Preserve existing project patterns for module boundaries, naming, testing, and error handling.
- Keep code readable and predictable with limited magic behavior.

## Research Requirements
- Default to fast execution for familiar problems; do not spend extra time on deep research when confidence is high.
- If uncertain, weak on a specific area, or facing version-sensitive behavior, search official documentation first.
- For implementation references and real-world patterns, search GitHub code after checking official docs.
- Keep research targeted and brief: only gather what is needed to complete the current task correctly.
- Timebox research to 3-5 minutes by default unless the user explicitly requests deep investigation.

## Commit & Pull Request Guidelines
- Commit messages follow bracketed tags, e.g. `[feat] add ...`.
- Allowed tags: `feat`, `fix`, `optimization`, `measurement`, `chore`, `log`.
- PR descriptions must follow the template below.
- The agent must fully fill `# Summary` and `# Key Changes`.
- The `# Tests` section is human-owned: the agent must not edit it under any circumstance and must not claim tests were run by humans.
```markdown
# Summary
- Purpose:

## Key Changes
1.
2.
3.

# Tests 
To be completed by engineer.
```


## Do, Don't, Avoid
### Do
- Enforce a per-task context token check.
- Auto-generate the `Context Token` from the first user sentence of the current task.
- Token format: `CTX-<W1>-<W2>-<W3>`.
- `W1..W3` are the first 3 words, uppercased, with non-alphanumeric characters removed; if fewer than 3 words exist, use available words.
- If a word is longer than 8 characters, truncate to 8 characters.
- The final line of every response must be exactly the generated token and nothing else on that line.

### Don't (Zero Tolerance)
- Never refactor or reformat code unless explicitly instructed.
- Never write explanatory comments, except for command snippets that teach people how to run scripts.
- If a task conflicts with these rules, stop and ask for explicit permission before proceeding.

### Avoid
- Introducing new packages or dependencies.
- Overprotective coding with excessive checks or broad `try/except` blocks.
