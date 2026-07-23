# Technical Article Writing Test Runner

Use this file as the single entry point for testing `technical-article-writing`.

## Goal

Evaluate whether `technical-article-writing` makes an agent write rigorous code-related articles that:

- use accurate, valid, source-backed hyperlinks
- annotate action-bearing code explanation with one-line, verb-level source links
- avoid code snippets and code blocks
- explain the implementation as a causal story instead of a line inventory
- absorb user corrections without defensive negation
- answer user challenges with direct useful claims instead of conservative retreat

## Inputs

- Skill under test: `plugins/codewizard/skills/technical-article-writing/SKILL.md`
- Rubric: `agents/tests/skills/technical-article-writing/rubric.md`
- Cases: `agents/tests/skills/technical-article-writing/cases/*.md`

## Run Procedure

1. Create a timestamped results directory:
   `agents/tests/skills/technical-article-writing/results/YYYY-MM-DD-HHMMSS/`
2. Read the skill under test and the rubric.
3. For each case file, read the case completely.
4. For each case, run two variants:
   - `with-skill`: load `technical-article-writing` before writing the article.
   - `without-skill`: do not load, mention, summarize, or paraphrase `technical-article-writing`.
5. Give each implementation agent only:
   - the case's `User Prompt`
   - unavoidable harness setup, such as the repository path
6. For `with-skill`, also give the implementation agent the skill under test. For `without-skill`, do not give any skill instructions or hints derived from the skill.
7. Do not reveal the case's `Source Link Inventory`, full `User Feedback Script`, `Expected Behavior`, or `Failure Signals` to either implementation agent. `Source Link Inventory` is evaluator-only; exposing it makes link accuracy untestable. Individual scripted feedback messages are sent only at the scheduled feedback turns below.
8. For cases with a `User Feedback Script`, send the same scripted feedback to both variants, one message at a time after the implementation agent produces the article or revision targeted by that feedback.
   - Wrap each scripted feedback message in the neutral revision contract below. This contract is harness setup, not skill guidance, and must be identical for `with-skill` and `without-skill`.
   - Do not reveal the case's evaluator-only expected behavior or failure signals.
   - Feedback message format:

     ```text
     <exact scripted feedback>

     Revise the article. Return only the revised article text, with no acknowledgement, apology, correction label, meta commentary, or explanation of what changed.
     ```
9. Save artifacts under the case result directory, grouped by variant:
   - `with-skill/case.md`: copied test case
   - `with-skill/transcript.md`: exact user and implementation-agent messages
   - `with-skill/article.md`: first article produced by the implementation agent
   - `with-skill/revisions.md`: article revisions after scripted feedback, when present
   - `with-skill/link-checks.md`: every article URL, its source, whether it appears in the case inventory, whether it uses exactly one source line, and whether that line supports the linked verb phrase
   - `with-skill/score.md`: rubric score and evaluator notes
   - `without-skill/case.md`: copied test case
   - `without-skill/transcript.md`: exact user and implementation-agent messages
   - `without-skill/article.md`: first article produced by the implementation agent
   - `without-skill/revisions.md`: article revisions after scripted feedback, when present
   - `without-skill/link-checks.md`: every article URL, its source, whether it appears in the case inventory, whether it uses exactly one source line, and whether that line supports the linked verb phrase
   - `without-skill/score.md`: rubric score and evaluator notes
   - `comparison.md`: concise comparison of with-skill and without-skill behavior
10. Validate links from artifacts, not memory:
   - A URL listed in the case's evaluator-only `Source Link Inventory` satisfies remote, commit, file-path, and line-anchor verification for the case; the linked phrase must still be checked against that one line.
   - A URL not listed in the inventory must be verified from the real remote, commit, file path, and single-line anchor before it can receive credit.
   - Placeholder URLs such as `github.com/org/repo`, `COMMIT`, `path/to`, or invented branch/file anchors receive no credit.
   - Range anchors such as `#L84-L92` receive no link-granularity credit, even when the range is real.
11. Score both variants with `rubric.md`. The `without-skill` variant is a baseline measurement; do not penalize it for not invoking the skill.
12. Write `summary.md` in the timestamped results directory with:
   - score table by case and variant
   - score delta by case
   - one-line with-skill vs without-skill comparison by case
   - repeated strengths
   - repeated weaknesses
   - recommended skill changes, if any

## Rules

- Do not grade from memory. Use saved artifacts.
- Do not fix the skill while running cases. Record failures first.
- Do not let the without-skill variant see the skill, its checklist, or case expectations.
- Do not accept code blocks as article explanation.
- Do not accept broad sentence hyperlinks when only a verb or verb phrase is source-backed.
- Do not accept range anchors. Source links must point to exactly one proving line.
- Do not accept linked claims that bundle several behaviors unless the one linked line proves every behavior in the linked phrase.
- Do not accept line-by-line code inventory as causal storytelling.
- Do not give credit for fake, placeholder, or unverified URLs.
- Do not treat apology, meta commentary, or negating the previous wrong claim as useful article revision.
- Leave this repository's unrelated worktree changes untouched.

## Required Transcript Format

Each variant's `transcript.md` must contain only the original words exchanged with the implementation agent:

```markdown
User:
<exact initial prompt sent to the implementation agent>

Implementation Agent:
<exact article response>

User:
<exact scripted feedback plus neutral revision contract, when present>

Implementation Agent:
<exact revised article response>
```

## Required Comparison Format

Each case's `comparison.md` must compare the two variants without re-scoring from memory:

```markdown
# Comparison: <case-id>

| Dimension | With Skill | Without Skill | Difference |
|---|---|---|---|
| Link Accuracy |  |  |  |
| Link Granularity |  |  |  |
| Causal Story |  |  |  |
| Code Dumping |  |  |  |
| Feedback Correction |  |  |  |
| Challenge Handling |  |  |  |

## Takeaway
<one concise paragraph explaining what the skill changed, if anything>
```
