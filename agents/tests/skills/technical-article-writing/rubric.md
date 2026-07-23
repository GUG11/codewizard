# Technical Article Writing Rubric

Score each category from 0 to 2.

- `0`: failed or missing
- `1`: partial, noisy, or weak
- `2`: correct and useful

## Categories

| Category | 0 | 1 | 2 |
|---|---|---|---|
| Invocation | With-skill variant did not use `technical-article-writing`; without-skill variant was contaminated by skill instructions | With-skill variant used the skill late or inconsistently | With-skill variant used the skill from the start; without-skill variant avoided skill instructions |
| Link Accuracy | Uses fake, placeholder, invalid, or unsupported source URLs | Mostly valid links but at least one unsupported or unverified source link remains | Every source link is verified from the case inventory or real remote, commit, file path, and single-line anchor |
| Link Granularity | Links whole sentences, vague nouns, decorative text, or range anchors | Some one-line action links, but coverage or precision is inconsistent | Action-bearing verbs or verb phrases in code explanations are narrowly linked to the one source line that proves the action |
| No Code Dumping | Includes code snippets, code blocks, or copied implementation bodies | Includes small inline code fragments that do not materially help the article | Explains implementation in prose and points to source links instead of reproducing code |
| Causal Story | Narrates files or lines in order without explaining how behavior emerges | Has some causal explanation but still depends on code-layout inventory | Explains how components interact and why they produce the observed behavior |
| Information Density | Uses filler, apology, meta commentary, or redundant correction history | Mostly direct but still includes avoidable defensive or procedural wording | Each sentence advances the technical explanation or revision |
| Feedback Correction | Preserves the wrong claim as a negation or copies user feedback mechanically | Corrects the claim but leaves defensive residue | Replaces the wrong claim with the corrected direct statement |
| Challenge Handling | Retreats to a safe inconclusive statement or only says what is not true | Gives a partially useful answer but leaves the original technical question underanswered | Replaces the overclaim with a direct useful answer to the same technical question |

## Strict Scoring Rules

- If a case has no user-feedback script, score `Feedback Correction` and `Challenge Handling` from any revision behavior present; if neither behavior is applicable, mark the category `N/A` and exclude it from the denominator for that case.
- For the `without-skill` baseline, score `Invocation` as `2` when the run was not exposed to the skill and `0` when the baseline was contaminated by skill instructions.
- If any article contains a fake or placeholder source URL, `Link Accuracy` is `0`.
- If a URL is valid but the linked line does not support the linked verb phrase, `Link Accuracy` is at most `1`.
- If any article or revision source URL uses a range anchor such as `#L84-L92`, `Link Granularity` is `0`.
- If a linked verb phrase bundles multiple behaviors and its one linked line does not prove every behavior in the linked phrase, `Link Accuracy` is at most `1`.
- If a linked phrase includes `and`, `or`, comma-separated behavior lists, or `such as`, give full `Link Granularity` credit only when the same one source line proves every listed item.
- If the article includes code blocks as explanation, `No Code Dumping` is `0`.
- If the article is organized primarily as "line X does Y, line Z does W", `Causal Story` is at most `1`.
- A list can receive full `Causal Story` credit only when it supports a causal explanation instead of replacing one.
- A defensive correction such as "A is not used; B is used" receives at most `1` for `Feedback Correction` when the useful article sentence should be "B is used."
- A conservative retreat such as "A and B are not prerequisites" receives `0` for `Challenge Handling` when the article still does not answer what the actual prerequisites or conditions are.

## Required Artifact Support For Scores

For every score, cite artifacts from the case result directory:

- `case.md`
- `transcript.md`
- `article.md`
- `revisions.md`, when present
- `link-checks.md`

Do not infer a passing score from intent alone.

## Verdict Rules

- `PASS`: all applicable categories score `2`.
- `PASS_WITH_CONCERNS`: total score is at least 80 percent of applicable points and no applicable category scores `0`.
- `FAIL`: any other result.

## Output Format

```markdown
# Score: <case-id>

| Category | Score | Evidence |
|---|---:|---|
| Invocation |  |  |
| Link Accuracy |  |  |
| Link Granularity |  |  |
| No Code Dumping |  |  |
| Causal Story |  |  |
| Information Density |  |  |
| Feedback Correction |  |  |
| Challenge Handling |  |  |

**Total:** <n>/<applicable points>
**Verdict:** PASS | PASS_WITH_CONCERNS | FAIL

## Strengths
- ...

## Weaknesses
- ...

## Recommended Skill Changes
- ...
```
