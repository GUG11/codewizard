# How to Clarify

Usually the user's initial ask has ambiguity, so proactively ask for clarification to narrow the scope and avoid back and forth during execution. Ask in a way that makes the user think less because you have thought ahead.

## Organize your questions

Think hierarchically, but ask and record selectively. Identify the mission-critical ambiguities that would change the mission brief if answered differently. Ask the smallest question that resolves the highest-impact ambiguity first.

Use a clarification tree to structure the result:

- <mission-critical ambiguity>: <why this must be clarified before the mission brief>
  - Asked: <verbatim clarification question>
  - Answered: <verbatim user answer>
  - Updated understanding: <what this answer makes clearer>
  - Remaining ambiguity: <none, or the next follow-up question needed before the mission brief>

Do not record private reasoning or a reconstructed reasoning tree in the mission brief. Record the ambiguity, exact question, exact user answer, updated understanding, and any remaining ambiguity. If a mission-critical ambiguity remains, ask a follow-up question before creating the mission brief.

## Ask good question

Ask only one question each time. Think ahead for the user and reduce the effort needed to answer. Prefer easy answer shapes in this order:

- Binary judgment: the user replies yes or no.
- Single choice: the user makes one decision from a few choices.
- Multiple choice: the user chooses multiple candidates.
- Description: the user needs to articulate the thought.

Ask as small a question as possible. Big questions usually require long descriptions to address all ambiguity. Use small answers to synthesize the larger mission intent.

### Questions Example
| What you want to clarify | Bad Question | Why bad | Convert to Good Question |
|---|---|---|---|
| Whether a troubleshooting prompt has enough concrete input to start. | `Please approve the current brief before I edit project files or start the local service run.` | It asks for workflow approval before clarifying the symptom anchor or request scope. It can turn an ambiguous debugging request into a plan that looks concrete but contains invented defaults. | `For bypassAllowed=false, what is the best anchor you have: original log line, DB query row, request shape, or only a general observation?` |
| Which part of a troubleshooting prompt blocks execution first. | `1. What request shape produces the symptom? 2. What concrete anchor should I reproduce? 3. Should the final diff keep production logging?` | Each question may be valid, but asking all of them at once makes the user manage the conversation structure. It also mixes symptom, reproduction, and final-diff decisions. | `What is the best starting clue for bypassAllowed=false? A useful answer can be as small as: android request, a DB query row, or "I only saw it while reading local logs."` |
| Whether the user wants root-cause debugging or an implementation action. | `Should I add diagnostic logging?` | It asks about an action while the user's real intent is to debug why the value changed. Logging may be a tool, but it is not the goal. | `Is your goal to find why the value becomes false, or to design a logging/product change around that value?` |
| The test plan | `I will start with the android request and keep trying other request shapes if it misses.` | `Yes, start with that` authorizes the starter query. It does not authorize inventing the next traffic slice after a miss. | `If the starter android request does not reproduce bypassAllowed=false, should I stop with artifacts, or may I expand to another request family?` |
| How broad the parameter search may be after the user says to try different requests. | `I will try different parameters until I find one.` | It accepts broad discretion without naming which parameters may vary. That can silently cross the user's intended scope. | `A concrete option is: vary platform across android, ios, web; vary item count across 5, 10, 20; run freshload followed by continuous requests using cursors; keep the rest empty unless evidence points to a specific parameters. Is that search space ok?` |


## Thoroughly clarify every ambiguity before move to the next one

Proactively identify ambiguity. Do not guess user intent. Check the user's words, code, docs, and data, and use verified facts where available. If the user's reply is still ambiguous, keep asking follow-up questions until the current mission-critical ambiguity is clear. Ask good questions instead of bombarding users with many low-quality questions.
