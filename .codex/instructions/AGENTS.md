# Multi-Agent Router

Default role: `planner`.

Routing rules:
- If user asks for planning, decomposition, or ambiguity resolution, use `planner`.
- If user asks for code changes, use `implementer`.
- If user asks for execution-backed verification, use `validator`.
- If user asks for audit trail, intermediate documentation, or process log, use `recorder`.
- If user intent is mixed, start with `planner` and then hand off.

Workflow:
1. `planner` creates an unambiguous plan.
2. `recorder` captures plan decisions and task decomposition.
3. `implementer` executes the plan.
4. `recorder` captures implementation deltas and run commands.
5. `validator` runs commands and returns evidence-backed findings.
6. `recorder` consolidates final audit log.

Handoff requirements:
- Include objective, file scope, acceptance criteria, commands, and blocking risks.
- Do not skip `validator` when runtime checks are required.
- Use `recorder` after each major handoff to preserve an auditable trail.
