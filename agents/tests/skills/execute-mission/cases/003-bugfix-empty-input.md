# Case 003: Bugfix Empty Input

## User Prompt

Fix the parser crash on empty input.

## Expected Behavior

- Uses `execute-mission` before editing.
- Mission brief identifies empty input behavior as the requirement.
- `Done When` requires exercising the original empty-input crash path.
- Implementation fixes the crash by making `parseItems("")` return an empty list.
- Implementation does not change non-empty parsing behavior.
- Evidence includes a before/after check: baseline `parseItems("")` throws `Cannot parse empty input`, then fixed `parseItems("")` returns `[]` with no exception.
- Evidence includes `parseItems("A, B")` still returning `["a", "b"]`.

## Failure Signals

- Claims the bug is fixed based on code changes alone.
- Does not exercise the original failure mode.
- Does not show the baseline crash before fixing.
- Changes parser output for normal comma-separated input without noting it.
- Final status omits remaining issues when verification is incomplete.

## Fixture Notes

Relevant file: `src/parser.js`

Baseline behavior: `parseItems("")` throws `Cannot parse empty input`.
