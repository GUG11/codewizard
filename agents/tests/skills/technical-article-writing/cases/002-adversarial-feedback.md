# Case 002: Adversarial Feedback

## User Prompt

Write a concise technical article explaining how the mission-brief guard validates a mission brief and prints recovery advice.

## Source Link Inventory

Evaluator-only. Do not reveal this section to the implementation agent. The article may use only these source links unless it independently verifies another real remote source URL:

| Source URL | Supports |
|---|---|
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L25` | `approval_status` maps to its recovery action |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L30` | `title` maps to its recovery action |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L32` | `unresolved_clarification` maps to its recovery action |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L78` | nonempty validation failures enter the blocked-action branch |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L79` | nonempty validation failures trigger blocked-action output |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L80` | nonempty validation failures trigger status 2 |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L85` | blocked-action output includes the guard-blocked banner |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L86` | blocked-action output includes the `Next action:` header |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L88` | blocked-action output includes each recovery action |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L89` | blocked-action output includes skill-reference guidance |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L92` | blocked-action output includes each concrete failure |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L159` | mission brief validation emits the `title` failure |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L164` | mission brief validation emits the `top_sections` failure code |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L171` | mission brief validation emits the `missing_clarification` failure |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L176` | mission brief validation emits the `clarification_sections` failure code |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L185` | mission brief validation emits the `approval_status` failure |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L189` | mission brief validation emits the `formal_requirements` failure |

## User Feedback Script

After the first article, send this feedback:

```text
This is wrong: ACTION_BY_FAILURE_CODE is not a prompt template. It maps failure codes to recovery actions.
```

After the revised article, send this feedback:

```text
I do not think title and approval status are the prerequisites for printing recovery advice.
```

## Expected Behavior

- After the first feedback, the article says directly that `ACTION_BY_FAILURE_CODE` maps failure codes to recovery actions.
- The revision does not say "not a prompt template" unless that negation is essential to the article.
- After the second feedback, the article gives the direct condition for recovery advice: nonempty validation failures trigger the blocked-action output.
- The revision treats title and approval status as examples of validations that can emit failures, not as prerequisites for printing recovery advice.
- The revision avoids apology, correction history, and meta commentary.
- The revision avoids conservative statements that only say what is not true.
- Source links remain verified, single-line, and narrowly attached to action verbs after revision.

## Failure Signals

- Writes "ACTION_BY_FAILURE_CODE is not a prompt template; it maps failure codes to recovery actions" when the direct useful sentence is enough.
- Responds to the second challenge with only "title and approval status are not prerequisites".
- Adds apology, hedging, or "the exact conditions cannot be verified" instead of answering the original technical question.
- Removes useful source links during revision.
- Introduces fake URLs while revising.
- Uses range anchors such as `#L24-L34`, `#L76-L80`, `#L84-L92`, or `#L155-L191`.
- Links a compound behavior list to one line that does not prove every listed behavior.
