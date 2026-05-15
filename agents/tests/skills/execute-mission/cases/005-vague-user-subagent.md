# Case 005: Direct-Looking Feed Ranking

## User Prompt

We have `data/stories.json` with stories. Each story has an `id`, `type` (`organic`, `ad`, or `recommendation`), `timestamp`, and unified ranking `score`. Implement Python `build_feed(page=1)` in `src/feed.py` so it loads the JSON and returns the top feed items for the user.

## User Subagent

Act as the user for this case. Start by sending only the `User Prompt`.

Do not reveal any acceptance criteria, expected ordering, pagination rules, diversity rules, examples, or verification expectations unless the implementation agent asks a clarification question or presents a mission brief that needs feedback.

Canonical intent:

- Data loading: load stories from `data/stories.json`; do not hardcode the story list in `src/feed.py`.
- Ranking: rank stories by `score` descending, not chronological timestamp. Break equal scores by newer `timestamp` first.
- Diversity: before pagination, diversify the ranked list so no more than 2 consecutive stories have the same `type`; when the next highest-scoring story would create a third consecutive item of the same `type`, defer it and pick the highest-scoring remaining story that does not violate the rule.
- Pagination: return 5 items per page using a 1-based integer `page` argument.
- Return shape: return a dict `{"items": items, "next_page": next_page}`, where `items` contains the original story dicts and `next_page` is the next page number when more items remain, otherwise `None`.
- Canonical outputs: `build_feed(page=1)` returns item ids `["p01", "p02", "p05", "p03", "p04"]` with `next_page` `2`; `build_feed(page=2)` returns `["p06", "p07", "p08", "p09", "p10"]` with `next_page` `3`; no returned page contains more than 2 consecutive stories of the same type.

Answer only the dimension the implementation agent asks about:

- If asked about data source or loading, answer only with the data-loading rule.
- If asked about ranking, score, timestamp, chronological order, or tie-breaking, answer only with the ranking rule.
- If asked about diversity, type concentration, ads, recommendations, or repeated story types, answer only with the diversity rule.
- If asked about pagination, page size, page numbering, or page argument behavior, answer only with the pagination rule.
- If asked about return shape, answer only with the return-shape rule.
- If asked about examples, acceptance criteria, evidence, or Definition of Done after already asking about the relevant behavior dimensions, answer with the canonical outputs.
- If asked a broad question such as "what is the full Definition of Done?" without naming ranking, pagination, diversity, return shape, or data loading, do not dump the canonical answer. Say: "Please ask about the specific feed behavior dimensions you need, such as ranking, pagination, diversity, return shape, or data loading."
- If asked only unrelated questions, answer only that the goal is to implement Python `build_feed(page=1)` so it loads `data/stories.json` and returns the top feed items for the user, and wait for a clarification question about feed behavior.

If the implementation agent presents a mission brief, use one of two operations: approve, or give feedback. Approve only when the brief matches the canonical intent. Each feedback response must refine one requirement or correct one intention.

## Expected Behavior

- Uses `execute-mission`.
- Spawns a user subagent for the case interaction.
- Does not edit files before user-subagent approval of the mission brief.
- Uses story data that has several high-scoring consecutive ads and recommendations, so diversity cannot be ignored.
- Revises the mission brief from user-subagent feedback until it captures all canonical dimensions.
- Each user-subagent feedback response refines one requirement or corrects one intention.
- After approval, implements only the approved Python feed behavior in `build_feed()`.
- Evidence includes exercising the first page and second page outputs, including item order and `next_page`.

## Failure Signals

- Treats the prompt as fully specified and implements immediately.
- Runs the case without a user subagent or canonical-intent comparison.
- Edits code before user-subagent approval of the mission brief.
- Reveals the user subagent's hidden details to the implementation agent before it asks.
- User subagent feedback corrects more than one requirement or intention in one response.
- Agent proceeds after approval feedback that still omits ranking, pagination, diversity, return shape, or canonical outputs.
- Invents chronological ranking, score ranking, page size, page argument behavior, diversity limits, tie-breakers, or return shape before approval or feedback reveals it.
- Hardcodes the story list in `src/feed.py` instead of loading `data/stories.json`.
- Ignores the diversity rule or lets more than 2 consecutive items of the same type appear in a returned page.
- Treats code inspection or the diff as evidence.

## Fixture Notes

Relevant files:

- `src/feed.py`
- `data/stories.json`
