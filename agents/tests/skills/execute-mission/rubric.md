# Execute Mission Rubric

Score each category from 0 to 2.

- `0`: failed or missing
- `1`: partial, noisy, or weak
- `2`: correct and useful

## Categories

| Category | 0 | 1 | 2 |
|---|---|---|---|
| Trigger | Did not use `execute-mission` | Used it late or inconsistently | Used it before editing |
| Clarification | Invented answers or asked irrelevant questions | Asked some useful questions but missed a key ambiguity | Asked only necessary clarification before brief |
| Mission Brief | Missing, late, or vague | Present but too broad/noisy | Clear, concise, saved before editing |
| Source Traceability | Requirements lack sources | Some rows cite weak or inferred sources | Every requirement cites a valid source |
| Done When | Not verifiable | Partially verifiable or generic | Each row names a concrete verification method |
| Evidence | Uses code/diff/claims as proof | Some observed facts, but incomplete | Evidence comes from exercised behavior and observed facts |
| Iteration | No bounded review or endless loop | Review exists but weakly tied to mission | Review checks mission rows and respects 3-round cap |
| Final Status | Missing or duplicates evidence noisily | Status present but incomplete | Status appended to mission brief and chat is concise |

## Required Evidence For Scores

For every score, cite the artifact that supports it:

- `mission.md`
- `diff.patch`
- `commands.md`
- `final.md`
- transcript excerpts if available

Do not infer a passing score from implementation code alone.

## Output Format

```markdown
# Score: <case-id>

| Category | Score | Evidence |
|---|---:|---|
| Trigger |  |  |
| Clarification |  |  |
| Mission Brief |  |  |
| Source Traceability |  |  |
| Done When |  |  |
| Evidence |  |  |
| Iteration |  |  |
| Final Status |  |  |

**Total:** <n>/16

## Strengths
- ...

## Weaknesses
- ...

## Recommended Skill Changes
- ...
```
