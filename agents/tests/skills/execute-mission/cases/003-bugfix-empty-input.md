# Case 003: Bugfix Empty Input

## User Prompt

Fix the parser crash on empty input.

## User Subagent

Act as the user for this case. Start by sending only the `User Prompt`.

Canonical intent: `parseItems("")` should stop throwing `Cannot parse empty input` and should return an empty list `[]`. Existing non-empty parsing behavior should stay the same.

If the implementation agent asks clarification, answer only with the canonical intent above.

If the implementation agent presents a mission brief, use one of two operations: approve, or give feedback. Approve only when the brief matches the canonical intent. Each feedback response must refine one requirement or correct one intention.

## Expected Behavior

- Uses `execute-mission` before editing.
- Spawns a user subagent for the case interaction.
- Mission brief identifies empty input behavior as the requirement and is approved before editing.
- `Definition of Done` requires exercising the original empty-input crash path.
- Implementation fixes the crash by making `parseItems("")` return an empty list.
- Implementation does not change non-empty parsing behavior.
- Final result matches the user subagent's canonical intent.
- Evidence includes a before/after check: baseline `parseItems("")` throws `Cannot parse empty input`, then fixed `parseItems("")` returns `[]` with no exception.
- Evidence includes `parseItems("A, B")` still returning `["a", "b"]`.

## Failure Signals

- Runs the case without a user subagent or canonical-intent comparison.
- Edits code before user-subagent approval of the mission brief.
- Claims the bug is fixed based on code changes alone.
- Does not exercise the original failure mode.
- Does not show the baseline crash before fixing.
- Changes parser output for normal comma-separated input without noting it.
- Fixes the crash with a return value other than `[]`.
- Final status omits remaining issues when verification is incomplete.

## Fixture Notes

Relevant file: `src/parser.js`

Baseline behavior: `parseItems("")` throws `Cannot parse empty input`.
