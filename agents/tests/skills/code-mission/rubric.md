# Code Mission Rubric

Score each skill-behavior category from 0 to 2. Report harness integrity and interaction efficiency separately; neither changes the skill score.

- `0`: failed or missing
- `1`: partial, noisy, or weak
- `2`: correct and useful

## Categories

| Category | 0 | 1 | 2 |
|---|---|---|---|
| Invocation | Did not use `code-mission` | Used it late or inconsistently | Used it from the start as a human-invoked workflow |
| Clarification | Created a mission brief or edited before completing clarification, invented answers, or recorded questions that were not asked | Asked useful questions but left an applicable branch unresolved or lost context needed to reconstruct the user's intent | Asked one adaptive question at a time until every applicable branch was resolved and recorded the questions and answers in a recursive tree without losing intent |
| Mission Brief | Missing, late, unapproved, or vague | Present but too broad/noisy or revised weakly | Clear, concise, approved before editing |
| Mission Brief Format | Missing mission brief or invalid required structure, including extra sections, missing sections, invalid approval status, missing clarification tree, or malformed Formal Requirements table | Mostly follows the required structure but has minor template drift, weak placeholders, or incomplete required fields | Exactly follows the `code-mission` mission brief template, including section order, clarification tree, approval status, mission status, and Formal Requirements table with `Result` |
| Approval Gate | Edited before user approval or self-approved | Requested approval but proceeded after partial or ambiguous approval | Waited for explicit user approval before implementation edits |
| Intent Synthesis | Requirements are copied mechanically, repetitive, obsolete, or not grounded in recorded user words | Requirements are partly synthesized but include repetition, stale feedback, or weak grounding | Requirements organize the user's current intent into real, non-repetitive outcomes grounded in recorded user words |
| Canonical Match | Final result diverges from the user subagent's canonical intent | Final result partially matches canonical intent or misses a material detail | Final result matches canonical intent from the user subagent |
| Definition of Done | Not verifiable | Partially verifiable or generic | Each row names a concrete observable end state and verification method |
| Result Trace | Uses code/diff/claims as proof | Some observed facts, but incomplete | Result trace comes from exercised behavior and observed facts |
| Iteration | No bounded review or endless loop | Review exists but weakly tied to mission | Review checks mission rows and respects 3-round cap |
| Final Status | Missing or duplicates result details noisily | Status present but incomplete | `Mission Status` section is updated in the mission brief and chat is concise |

## Strict Scoring Rules

- Canonical Match is the correctness anchor. A `COMPLETE` status, clean diff, or confident final response does not raise the score when the result diverges from the user subagent's canonical intent.
- If hidden canonical details were not revealed to the implementation agent before implementation, do not give full credit for Mission Brief, Intent Synthesis, or Definition of Done based on those hidden details.
- Count only user-owned behavioral or design choices as canonical intent dimensions. A concrete probe or acceptance check derived from already clarified behavior is agent-owned verification, not an additional user-intent branch, and does not need a separate clarification question.
- If implementation edits occur before the user subagent approves the mission brief, Approval Gate is `0` and Mission Brief is at most `1`.
- If the user subagent gives feedback on the mission brief and the implementation agent does not revise and present the brief again before editing, Approval Gate is `0`.
- If Mission Brief Format is `0`, Mission Brief is at most `1` and Approval Gate is at most `1`.
- If `mission.md` contains sections outside the `code-mission` mission brief template, Mission Brief Format is `0`.
- If `mission.md` lacks `## Clarification`, `### Clarification Tree`, `### Clarified Intent`, a valid `## Approval Status`, or a Formal Requirements table with `Requirement` and `Result` columns, Mission Brief Format is `0`.
- If the Clarification Tree is not recursive, omits a required node field, or contains a leaf that does not end with `Follow-ups: none`, Mission Brief Format is at most `1` and Clarification is at most `1`.
- Formatting-only normalization of Markdown layout or punctuation does not reduce Clarification. Missing or summarized answer choices reduce Clarification only when their absence changes meaning, makes an answer such as `Option 2` uninterpretable, or otherwise loses context needed to reconstruct the user's intent. Do not deduct when the answer is self-contained and the complete intent is preserved.
- Score the Clarification Tree by causal parentage, not transcript chronology. Do not deduct when an independent question is recorded at the top level or a follow-up is moved beneath the question whose answer triggered it, provided every traversed node and its content are preserved.
- An exact, accessible canonical mission path or link counts as presenting the complete mission brief for approval. Do not deduct Mission Brief or Approval Gate points merely because the brief was not duplicated inline.
- If the implementation agent creates a mission brief before the adaptive clarification sequence is complete, Clarification is `0` and Mission Brief is at most `1`.
- If a case contains hidden canonical intent that changes the observable outcome and the implementation agent asks no clarification, Clarification is `0`.
- If the implementation agent asks only a partial clarification and then proceeds while unrevealed canonical dimensions still change the observable outcome, Clarification is at most `1`.
- If a user answer leaves an applicable clarification branch unresolved and the implementation agent creates a mission brief instead of asking a follow-up, Clarification is at most `1`.
- If `mission.md` includes hidden canonical details that were not revealed through clarification or mission-brief feedback, Mission Brief is at most `1`.
- If result trace verifies only the agent's inferred behavior instead of canonical behavior, Result Trace is at most `1`.

An alternate mission path, a non-identical `mission.md` copy, transcript capture defects, partial or rewritten message routing, coordinator-facing text mislabeled as user-facing dialogue, hidden-intent leakage by the harness or metadata such as `CTX:`, user-subagent disclosure violations, failure to save an artifact the agent produced, and reconstructed dialogue are harness-integrity defects. Report them separately and do not convert them into skill-score deductions. If the agent never produced a required mission artifact, score that absence normally as skill behavior. Authentic agent turns may contain headings, tables, commands, file-edit descriptions, status blocks, or `CTX:` lines. Missing or differently worded `CTX:` lines are irrelevant unless their content leaks intent.

## Verdict Rules

- `PASS`: total is at least 20/22, and Mission Brief Format, Approval Gate, Canonical Match, and Result Trace are all `2`.
- `PASS_WITH_CONCERNS`: total is at least 18/22, and Mission Brief Format, Approval Gate, Canonical Match, and Result Trace are all at least `1`.
- `FAIL`: any other result.

Harness integrity is a separate `VALID` or `INVALID` evaluation status. An `INVALID` evaluation keeps its provisional skill score and verdict for diagnosis but must be excluded from aggregate skill-effect claims until the harness defect is corrected.

## Required Artifact Support For Scores

For every score, cite artifacts from the variant being scored:

- `<variant>/mission.md`, when present
- `<variant>/mission-source.md`, for canonical path and copy verification when `mission.md` is present
- `<variant>/diff.patch`
- `<variant>/commands.md`
- `<variant>/final.md`
- `<variant>/user-subagent.md`
- `<variant>/transcript.md`
- `<variant>/metrics.md`, for the separate interaction-efficiency report

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
| Mission Brief Format |  |  |
| Approval Gate |  |  |
| Intent Synthesis |  |  |
| Canonical Match |  |  |
| Definition of Done |  |  |
| Result Trace |  |  |
| Iteration |  |  |
| Final Status |  |  |

**Total:** <n>/22
**Verdict:** PASS | PASS_WITH_CONCERNS | FAIL
**Evaluation Validity:** VALID | INVALID

## Harness Integrity
- <artifact completeness, canonical mission path, byte-identical mission copy, exact routing/capture, speaker attribution, intent isolation, and user-subagent compliance findings>

## Interaction Efficiency
- Metrics: `<variant>/metrics.md`

## Strengths
- ...

## Weaknesses
- ...

## Recommended Skill Changes
- ...
```
