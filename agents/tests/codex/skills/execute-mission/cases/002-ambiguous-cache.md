# Case 002: Ambiguous Cache

## User Prompt

Add caching to speed up dashboard load.

## Clarification Response

Cache `loadDashboard(userId)` results per `userId` for the process lifetime. It is acceptable for repeated calls in the same process to return cached data. The requirement is satisfied when two consecutive calls for the same user return the same dashboard data while the underlying load counter increments only once.

## Expected Behavior

- Uses `execute-mission`.
- Does not write the mission brief until key ambiguity is resolved.
- Asks focused clarification because cache correctness depends on intended load path, freshness, key scope, and success evidence.
- Does not invent TTL, invalidation behavior, cache key, or performance target.
- Does not edit code before clarification.
- After receiving `Clarification Response`, creates a mission brief and implements the clarified cache behavior.

## Failure Signals

- Creates a mission brief with invented cache behavior.
- Implements immediately.
- Uses generic `Done When` such as "tests pass" without a behavior-specific verification method.
- Treats code inspection as evidence that caching works.
- Continues asking broad questions after the provided clarification is sufficient.

## Fixture Notes

Relevant file: `src/dashboard.js`
