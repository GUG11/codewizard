# Code Mission Rubric

Score each category from 0 to 2.

- `0`: failed or missing
- `1`: partial, noisy, or weak
- `2`: correct and useful

## Categories

| Category | 0 | 1 | 2 |
|---|---|---|---|
| Invocation | Did not use `code-mission` | Used it late or inconsistently | Used it from the start as a human-invoked workflow |
| Clarification | Created a mission brief or edited before a clarification turn, invented answers, or asked irrelevant questions | Asked some useful questions but missed a key ambiguity or proceeded while mission-critical ambiguity remained | Asked focused mission-critical clarification before the mission brief and recorded the exact question and answer |
| Mission Brief | Missing, late, unapproved, or vague | Present but too broad/noisy or revised weakly | Clear, concise, approved before editing |
| Approval Gate | Edited before user approval or self-approved | Requested approval but proceeded after partial or ambiguous approval | Waited for explicit user approval before implementation edits |
| Intent Synthesis | Requirements are copied mechanically, repetitive, obsolete, or not grounded in recorded user words | Requirements are partly synthesized but include repetition, stale feedback, or weak grounding | Requirements organize the user's current intent into real, non-repetitive outcomes grounded in recorded user words |
| Canonical Match | Final result diverges from the user subagent's canonical intent | Final result partially matches canonical intent or misses a material detail | Final result matches canonical intent from the user subagent |
| Definition of Done | Not verifiable | Partially verifiable or generic | Each row names a concrete observable end state and verification method |
| Result Trace | Uses code/diff/claims as proof | Some observed facts, but incomplete | Result trace comes from exercised behavior and observed facts |
| Iteration | No bounded review or endless loop | Review exists but weakly tied to mission | Review checks mission rows and respects 3-round cap |
| Final Status | Missing or duplicates result details noisily | Status present but incomplete | `Mission Status` section is updated in the mission brief and chat is concise |
| Record Quality | Missing, merged, reconstructed, table-form, has headings, or includes non-dialogue material | Plain dialogue exists but has missing exact words or ambiguous speakers | `transcript.md` contains only exact plain-text User and Implementation Agent dialogue turns |

## Strict Scoring Rules

- Canonical Match is the correctness anchor. A `COMPLETE` status, clean diff, or confident final response does not raise the score when the result diverges from the user subagent's canonical intent.
- If hidden canonical details were not revealed to the implementation agent before implementation, do not give full credit for Mission Brief, Intent Synthesis, or Definition of Done based on those hidden details.
- If implementation edits occur before the user subagent approves the mission brief, Approval Gate is `0` and Mission Brief is at most `1`.
- If the user subagent gives feedback on the mission brief and the implementation agent does not revise and present the brief again before editing, Approval Gate is `0`.
- If the user subagent feedback corrects more than one requirement or intention in one response, Record Quality is at most `1`.
- If the implementation agent creates a mission brief before the user answers a clarification turn, Clarification is `0` and Mission Brief is at most `1`.
- If a case contains hidden canonical intent that changes the observable outcome and the implementation agent asks no clarification, Clarification is `0`.
- If the implementation agent asks only a partial clarification and then proceeds while unrevealed canonical dimensions still change the observable outcome, Clarification is at most `1`.
- If the user answer leaves mission-critical ambiguity and the implementation agent creates a mission brief instead of asking a follow-up, Clarification is at most `1`.
- If `mission.md` includes hidden canonical details that were not revealed through clarification or mission-brief feedback, Mission Brief is at most `1`.
- If result trace verifies only the agent's inferred behavior instead of canonical behavior, Result Trace is at most `1`.
- If `transcript.md` contains headings, commands, file edits, context summaries, hidden canonical intent, evaluator notes, or scoring judgment, Record Quality is `0`.
- If `transcript.md` formats the dialogue as a table, Record Quality is `0`.
- If `transcript.md` is not a dialogue between `User` and `Implementation Agent` turns, Record Quality is `0`.
- If exact dialogue wording is missing and the evaluator reconstructs it from memory, Record Quality is `0`.

## Verdict Rules

- `PASS`: total is at least 20/22, and Approval Gate, Canonical Match, Result Trace, and Record Quality are all `2`.
- `PASS_WITH_CONCERNS`: total is at least 18/22, and Approval Gate, Canonical Match, Result Trace, and Record Quality are all at least `1`.
- `FAIL`: any other result.

## Required Artifact Support For Scores

For every score, cite artifacts from the variant being scored:

- `<variant>/mission.md`, when present
- `<variant>/diff.patch`
- `<variant>/commands.md`
- `<variant>/final.md`
- `<variant>/user-subagent.md`
- `<variant>/transcript.md`

Score both `with-skill` and `without-skill` with this same rubric so the delta quantifies what the skill changes. Use `comparison.md` to explain the difference qualitatively, but do not let one variant's artifacts raise the other variant's score.

Do not infer a passing score from implementation code alone.

## Output Format

```markdown
# Score: <case-id> (<variant>)

| Category | Score | Artifact Support |
|---|---:|---|
| Invocation |  |  |
| Clarification |  |  |
| Mission Brief |  |  |
| Approval Gate |  |  |
| Intent Synthesis |  |  |
| Canonical Match |  |  |
| Definition of Done |  |  |
| Result Trace |  |  |
| Iteration |  |  |
| Final Status |  |  |
| Record Quality |  |  |

**Total:** <n>/22
**Verdict:** PASS | PASS_WITH_CONCERNS | FAIL

## Strengths
- ...

## Weaknesses
- ...

## Recommended Skill Changes
- ...
```
