# Case 004: Docs And Config Change

## User Prompt

Rename the `syncIntervalMs` config option to `userSyncIntervalMs` and update the docs.

## Expected Behavior

- Uses `execute-mission`.
- Mission brief includes both config behavior and docs update.
- `Done When` covers exercising config loading and inspecting docs output/content.
- Implementation updates code and docs consistently.
- Evidence includes observed config behavior, not only a diff.

## Failure Signals

- Updates code but misses docs.
- Updates docs but misses config loading.
- Treats search results or diff as satisfaction evidence.
- Does not run a check that loads the renamed option.

## Fixture Notes

Relevant files:

- `src/config.js`
- `README.md`
