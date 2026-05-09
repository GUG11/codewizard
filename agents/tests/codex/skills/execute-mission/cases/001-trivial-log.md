# Case 001: Trivial Log

## User Prompt

Add a log when `syncUsers()` starts.

## Expected Behavior

- Uses `execute-mission` before editing.
- Creates a small mission brief without asking unnecessary clarification.
- `Done When` names a verification method that exercises `syncUsers()`.
- Prefers existing logging style in the fixture.
- Evidence comes from running code and observing the log output.
- Final status is appended to the mission brief.

## Failure Signals

- Asks broad design questions for this simple request.
- Uses the diff as evidence that logging works.
- Adds excessive logging beyond the requested start log.
- Does not run an executable check that calls `syncUsers()`.

## Fixture Notes

Relevant file: `src/sync.js`
