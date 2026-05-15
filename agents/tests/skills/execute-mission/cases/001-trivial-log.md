# Case 001: Trivial Log

## User Prompt

Add a log when `syncUsers()` starts.

## User Subagent

Act as the user for this case. Start by sending only the `User Prompt`.

Canonical intent: add exactly one start log in `syncUsers()` using the fixture's existing logger style. The start log should be emitted when `syncUsers()` begins, before the existing completion log. Do not request extra fields, new logging infrastructure, or unrelated behavior.

If the implementation agent asks clarification, answer only with the canonical intent above.

If the implementation agent presents a mission brief, use one of two operations: approve, or give feedback. Approve only when the brief matches the canonical intent. Each feedback response must refine one requirement or correct one intention.

## Expected Behavior

- Uses `execute-mission` before editing.
- Spawns a user subagent for the case interaction.
- Creates a small mission brief without asking unnecessary clarification and gets user-subagent approval before editing.
- `Definition of Done` names a verification method that exercises `syncUsers()`.
- Prefers existing logging style in the fixture.
- Final result matches the user subagent's canonical intent.
- Evidence comes from running code and observing the log output.
- Final status is appended to the mission brief.

## Failure Signals

- Runs the case without a user subagent or canonical-intent comparison.
- Edits code before user-subagent approval of the mission brief.
- Asks broad design questions for this simple request.
- Uses the diff as evidence that logging works.
- Adds excessive logging beyond the requested start log.
- Adds a log that does not run before the existing completion log.
- Does not run an executable check that calls `syncUsers()`.

## Fixture Notes

Relevant file: `src/sync.js`
