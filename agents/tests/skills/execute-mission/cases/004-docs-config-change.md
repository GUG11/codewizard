# Case 004: Docs And Config Change

## User Prompt

Rename the `syncIntervalMs` config option to `userSyncIntervalMs` and update the docs.

## User Subagent

Act as the user for this case. Start by sending only the `User Prompt`.

Canonical intent: rename the returned config object property from `syncIntervalMs` to `userSyncIntervalMs`, keep reading the same `SYNC_INTERVAL_MS` environment variable, and update the README documentation to use `userSyncIntervalMs`. Do not add aliases, new environment variables, or unrelated config behavior.

If the implementation agent asks clarification, answer only with the canonical intent above.

If the implementation agent presents a mission brief, use one of two operations: approve, or give feedback. Approve only when the brief matches the canonical intent. Each feedback response must refine one requirement or correct one intention.

## Expected Behavior

- Uses `execute-mission`.
- Spawns a user subagent for the case interaction.
- Mission brief includes both config behavior and docs update, and is approved before editing.
- `Definition of Done` covers exercising config loading and inspecting docs output/content.
- Implementation updates code and docs consistently.
- Final result matches the user subagent's canonical intent.
- Evidence includes observed config behavior, not only a diff.

## Failure Signals

- Runs the case without a user subagent or canonical-intent comparison.
- Edits code before user-subagent approval of the mission brief.
- Updates code but misses docs.
- Updates docs but misses config loading.
- Treats search results or diff as satisfaction evidence.
- Does not run a check that loads the renamed option.
- Adds aliases, changes the environment variable name, or changes unrelated config behavior.

## Fixture Notes

Relevant files:

- `src/config.js`
- `README.md`
