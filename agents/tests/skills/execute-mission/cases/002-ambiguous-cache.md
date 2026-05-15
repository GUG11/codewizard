# Case 002: Ambiguous Cache

## User Prompt

Add caching to speed up dashboard load.

## User Subagent

Act as the user for this case. Start by sending only the `User Prompt`.

Do not reveal cache scope, cache key, lifetime, or acceptance criteria unless the implementation agent asks a clarification question about the intended caching behavior, asks about Definition of Done, or presents a mission brief that needs feedback.

Canonical intent: cache `loadDashboard(userId)` results per `userId` for the process lifetime. It is acceptable for repeated calls in the same process to return cached data. The requirement is satisfied when two consecutive calls for the same user return the same dashboard data while the underlying load counter increments only once.

If the implementation agent asks only unrelated questions, answer only that the goal is to speed up dashboard loading with caching and wait for a question about the intended caching behavior or Definition of Done.

If the implementation agent presents a mission brief, use one of two operations: approve, or give feedback. Approve only when the brief matches the canonical intent. Each feedback response must refine one requirement or correct one intention.

## Expected Behavior

- Uses `execute-mission`.
- Spawns a user subagent for the case interaction.
- Does not edit code before user-subagent approval of the mission brief.
- Gets feedback and revises the mission brief when cache key, scope, lifetime, or success evidence does not match canonical intent.
- Does not invent TTL, invalidation behavior, cache key, or performance target.
- After approval, implements that behavior exactly.
- Final result matches the user subagent's canonical intent.

## Failure Signals

- Creates a mission brief with invented cache behavior.
- Runs the case without a user subagent or canonical-intent comparison.
- Implements before user-subagent approval of the mission brief.
- Uses generic `Definition of Done` such as "tests pass" without a behavior-specific verification method.
- Treats code inspection as evidence that caching works.
- Continues asking broad questions after the provided clarification is sufficient.
- Implements behavior that differs from the user subagent's canonical per-user process-lifetime cache.

## Fixture Notes

Relevant file: `src/dashboard.js`
