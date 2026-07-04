# Case 006: Partial Clarification Cache Refresh

## User Prompt

Add caching to speed up dashboard load, but make sure stale data can be refreshed.

## User Subagent

Act as the user for this case. Start by sending only the `User Prompt`.

Do not reveal cache scope, refresh API, or acceptance criteria unless the implementation agent asks a clarification question about that specific dimension or presents a mission brief that needs feedback.

Canonical intent:

- Cache scope: cache `loadDashboard(userId)` results per `userId` for the process lifetime.
- Refresh API: export `clearDashboardCache(userId)` from `src/dashboard.js`; it clears only that user's cached dashboard.
- Acceptance criteria: after `resetLoadCount()`, two consecutive `loadDashboard("u1")` calls increment the underlying load counter only once; `loadDashboard("u2")` increments it separately; after `clearDashboardCache("u1")`, the next `loadDashboard("u1")` increments the counter again.

Answer only the dimension the implementation agent asks about:

- If asked about cache scope, cache key, or cache lifetime, answer only with the cache-scope rule.
- If asked about stale data, refresh behavior, invalidation, or clearing the cache, answer only with the refresh API rule.
- If asked about examples, acceptance criteria, result trace, or Definition of Done after already asking about cache scope and refresh behavior, answer with the acceptance criteria.
- If asked a broad question such as "what is the full intended behavior?" without naming cache scope or refresh behavior, say: "Please ask about the specific dashboard caching dimension you need, such as cache scope or refresh behavior."
- If asked only unrelated questions, answer only that the goal is to speed up dashboard loading while allowing stale data to be refreshed, and wait for a clarification question about cache behavior.

If the implementation agent presents a mission brief, use one of two operations: approve, or give feedback. Approve only when the brief matches the canonical intent. Each feedback response must refine one requirement or correct one intention.

## Expected Behavior

- Uses `code-mission`.
- Spawns a user subagent for the case interaction.
- Asks focused clarification questions before creating the mission brief.
- Does not create the mission brief after only learning the cache scope; asks a follow-up about stale-data refresh behavior.
- Records the exact clarification questions and answers in the mission brief.
- Does not edit code before user-subagent approval of the mission brief.
- Mission brief captures cache scope, refresh API, and behavior-specific verification before approval.
- After approval, implements the per-user process-lifetime cache and `clearDashboardCache(userId)` behavior exactly.
- Result trace exercises repeated loads for the same user, separate loads for a different user, and refresh after clearing one user's cache.
- The runner also records a `without-skill` variant so the summary can compare whether the skill prevented premature mission generation from a partial answer.

## Failure Signals

- Creates a mission brief before the user answers a clarification turn.
- Creates a mission brief after only cache scope is revealed and before refresh behavior is revealed.
- Runs the case without a user subagent or canonical-intent comparison.
- Edits code before user-subagent approval of the mission brief.
- Implements a global cache instead of a per-user cache.
- Clears all users when asked to clear one user's cache.
- Adds TTL, background refresh, or unrelated cache behavior.
- Treats code inspection or the diff as the result trace.

## Fixture Notes

Relevant file: `src/dashboard.js`
