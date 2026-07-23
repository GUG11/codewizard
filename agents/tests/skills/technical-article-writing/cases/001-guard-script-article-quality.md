# Case 001: Guard Script Article Quality

## User Prompt

Write a concise technical article describing how `plugins/codewizard/hooks/guard_mission_brief.py` works, focusing on how it turns mission-brief validation failures into recovery guidance.

## Source Link Inventory

Evaluator-only. Do not reveal this section to the implementation agent. The article may use only these source links unless it independently verifies another real remote source URL:

| Source URL | Supports |
|---|---|
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L25` | `approval_status` maps to its recovery action |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L30` | `title` maps to its recovery action |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L32` | `unresolved_clarification` maps to its recovery action |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L76` | `main` collects validation failures |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L78` | `main` detects nonempty validation failures |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L79` | `main` prints the blocked-action output |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L80` | `main` exits with status 2 |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L85` | `print_blocked_action` prints the guard-blocked banner |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L86` | `print_blocked_action` prints the `Next action:` header |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L88` | `print_blocked_action` prints each recovery action |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L89` | `print_blocked_action` prints the skill-reference sentence |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L90` | `print_blocked_action` prints the `Failures:` header |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L92` | `print_blocked_action` prints each failure message |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L96` | `recovery_actions` derives failure codes from failures |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L101` | `recovery_actions` iterates failure-code actions in mapping order |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L102` | `recovery_actions` selects matching actions and avoids duplicates |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L103` | `recovery_actions` appends each selected action |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L159` | mission brief validation emits the `title` failure |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L164` | mission brief validation emits the `top_sections` failure code |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L185` | mission brief validation emits the `approval_status` failure |
| `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_brief.py#L189` | mission brief validation emits the `formal_requirements` failure |

## Expected Behavior

- Organizes the article around the causal path: validation emits failures, failure codes select recovery actions, the guard prints next actions plus failure details, and the hook blocks with status 2.
- Uses source links from the inventory instead of fake placeholders.
- Links action-bearing verbs or verb phrases such as `detects`, `prints`, and `derives` to exactly one source line.
- Splits compound claims so each link has one proving line.
- Does not include code blocks or copied code.
- Uses lists only to support the causal story.
- Avoids a line-by-line inventory of the file.
- Does not explicitly identify the main entry point unless it matters to the causal explanation.

## Failure Signals

- The article is organized as a sequence of code locations: "lines 24-34", "lines 76-80", "lines 84-92".
- The article explains each source block independently without explaining how they combine.
- Uses `github.com/org/repo`, `COMMIT`, `path/to`, branch guesses, or invented line anchors.
- Uses range anchors such as `#L24-L34`, `#L76-L80`, `#L84-L92`, `#L95-L104`, or `#L155-L191`.
- Links an entire sentence such as "prints recovery guidance when validation fails".
- Links a list of behaviors to one line when that line does not prove every listed behavior.
- Mentions source-backed behavior without a source link on the action verb or verb phrase.
- Includes a code snippet or code block.
