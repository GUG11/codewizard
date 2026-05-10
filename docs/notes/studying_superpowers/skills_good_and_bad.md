# Studying Superpowers Skills: Good and Bad

## `systematic-debugging`

Source reviewed: `/Users/hyzhang/Project/superpowers/skills/systematic-debugging/SKILL.md`

### What the skill does well

The skill is valuable as an anti-thrashing mechanism. It pushes agents away from the common failure mode of reading the nearest error, applying a plausible patch, and then rationalizing the result. Its strongest parts are:

- insisting on root-cause investigation before proposing fixes
- requiring reproduction, error reading, and recent-change inspection
- encouraging evidence collection at component boundaries
- pushing agents to form one hypothesis at a time
- warning agents to stop after repeated failed fixes and reconsider their model

This is useful behavior shaping for agents because agents often look productive while merely trying random fixes.

### Main criticism

The skill looks professional, but it is not operational enough for hard bugs.

It mostly provides a disciplined to-do list: read errors, reproduce, check changes, compare patterns, form a hypothesis, test minimally, then implement. That is good engineering hygiene, but it does not provide much unique diagnostic insight.

The central issue is that debugging is not just a linear process. Debugging is search-space reduction. Each action should either increase information, eliminate a class of explanations, isolate the failing boundary, or force a smaller reproduction. If a step does none of those things, it becomes ritual.

### Why it may fail on hard bugs

If the bug is obvious, the checklist is heavier than needed.

If the bug is hard, the checklist may not help enough. An agent can follow every step and still fail to find an insight because the skill does not say how to choose the next high-yield experiment when the current path stalls.

Missing operational questions include:

- Did the process fail, or did a tool/test/environment fail?
- Which hypotheses have been eliminated?
- Which assumption is still untested?
- Is the failure likely in code, test harness, environment, tooling, data, or mental model?
- What experiment would split the search space most cleanly?
- When should the agent jump to a specialized tactic instead of continuing the generic sequence?

### Missing routing logic

The skill treats many different bug classes as if one four-phase flow applies to all of them. In practice, different symptoms should route to different tactics:

- flaky or nondeterministic failure: control clocks, randomness, concurrency, retries, and isolation
- regression: find last-known-good state, inspect recent diffs, bisect commits or artifacts
- state corruption: add invariants, watch mutation boundaries, trace ownership of the bad value
- distributed or integration bug: trace request identity, config propagation, serialization, auth context, and boundary contracts
- performance bug: profile first, then inspect hot paths
- UI bug: compare screenshots, DOM state, browser events, and viewport-specific behavior
- test-only bug: inspect mocks, cleanup, shared globals, ordering, temp files, and harness assumptions

The existing skill gestures at some of these, especially component-boundary evidence and root-cause tracing, but it does not route decisively based on symptom type.

### What would make it stronger

A better version would keep the current discipline, but add a diagnostic decision system:

- a bug-type routing table
- a stuck-state protocol
- a hypothesis ledger
- jump rules for specialized tactics
- guidance for distinguishing code failure from test/tool/environment failure
- explicit focus on choosing the next discriminating experiment

Example jump rules:

- If there is a last-known-good version, jump directly to regression bisection.
- If the failure is flaky, jump to nondeterminism controls before general code inspection.
- If the error appears deep in the stack, jump to backward tracing.
- If the symptom crosses process or service boundaries, instrument the boundaries first.
- If repeated hypotheses fail, question the reproduction, tooling, or mental model before changing architecture.

### Bottom line

The skill is good as an anti-guessing guardrail. It makes agents more disciplined and less likely to apply random patches.

But it does not yet make agents substantially better diagnosticians. For hard bugs, it needs more operational logic: symptom classification, search-space reduction, discriminating experiments, and explicit rules for when to change tactics.

## `receiving-code-review`

Source reviewed: `/Users/hyzhang/Project/superpowers/skills/receiving-code-review/SKILL.md`

### What the skill does well

The skill is trying to prevent a real agent failure mode: receiving external review feedback and immediately obeying it because it sounds authoritative.

Its useful parts are:

- verify review feedback against codebase reality before implementing
- ask for clarification when feedback is unclear
- push back when a suggestion is technically wrong or violates YAGNI
- avoid performative agreement
- implement multi-item feedback in a disciplined order

The strongest idea is not social tone. The strongest idea is technical skepticism: external feedback is input to evaluate, not an order to execute.

### Main criticism

The skill has the wrong role boundary.

It treats the agent as the party receiving and handling code review feedback. That is risky because code review is a human accountability loop. The reviewer is communicating concerns, standards, trust, and project judgment to the human author. If the human forwards review comments to the agent and lets the agent fix and reply, the human can stop understanding the feedback.

This creates the "lazy human mode" failure: the human becomes a supervisor of AI-to-reviewer communication instead of the person accountable for the change.

### Why it may fail in practice

The skill prevents one failure while enabling another.

It prevents blind compliance, but it can still normalize the agent as a proxy participant in review. Sections about external reviewers, GitHub thread replies, acknowledgments, and response style make the agent too socially present in a human review relationship.

If a human has already read review feedback, formed an opinion, and converted it into a task, the agent should not re-litigate the reviewer relationship. At that point the review feedback is just a human-owned implementation request.

### What would make it stronger

This should not be a standalone task-implementation skill.

The useful rule belongs in a general implementation workflow:

- treat the human's instruction as the source of intent
- implement the task with normal engineering rigor
- raise concrete red flags if code, tests, repo policy, security, compatibility, or feasibility conflict with the request
- do not communicate with reviewers or resolve review threads unless the human explicitly asks

For review-derived tasks, the right assumption is:

> The human has already evaluated the reviewer feedback. The agent should implement the human-rephrased task and surface only concrete technical conflicts.

### Bottom line

The skill has a valid concern but the wrong abstraction.

The abstraction should be human-owned task implementation, not agent-owned review reception.

## `requesting-code-review` / `code-reviewer.md`

Source reviewed: `/Users/hyzhang/Project/superpowers/skills/requesting-code-review/code-reviewer.md`

### What the skill does well

This prompt contains some strong review mechanics:

- reviews against requirements or a plan, not just local code style
- uses an explicit git range
- asks whether implementation matches planned behavior
- separates severity levels
- requires file and line evidence
- asks why each issue matters
- gives a clear readiness verdict
- allows the reviewer to say the plan itself is flawed

The best part is plan alignment. It asks whether the implementation actually did the thing it was supposed to do. That is more valuable than generic code-quality commentary.

### Main criticism

The skill is too broad and too subagent-shaped.

It frames code review as dispatching a senior reviewer subagent that checks architecture, scalability, security, production readiness, tests, docs, and strengths. That can be useful for large changes, but it is too heavy as a default loop after every implementation step.

It also mixes two different review goals:

- mission completion: did the implementation satisfy the requirement?
- code quality: is the implementation architecturally good, maintainable, secure, and ready to merge?

Those are related, but they should not always run at the same time.

### Why it may fail in practice

Subagent review is not automatically better review.

A subagent has less implementation context, which can help reduce anchoring, but it can also make it miss constraints, prior decisions, and tradeoffs. If the subagent is asked for broad code-quality review, it may generate generic findings that are wasted when the next implementation round removes the code anyway.

The "Strengths" section is also questionable for an internal verifier. It can produce review-shaped prose instead of high-signal defect detection.

### What would make it stronger

Split review into two stages:

1. Mission-completion review
   - compare diff against a saved mission brief
   - verify each formal requirement
   - report missing requirements, incorrect behavior, mission-breaking regressions, and missing evidence
   - do not invent new requirements

2. Code-quality review
   - run only after mission completion is stable
   - check architecture, maintainability, security, performance, error handling, and tests
   - use `code-review-expert`-style review if the user wants deeper review

Subagents should be optional, not default. They are most useful for large or risky missions, or when the human explicitly wants an independent pass.

### Bottom line

The prompt has good review primitives, especially requirement alignment and severity calibration.

But the default review loop should be narrower: first prove the mission is complete, then optionally do broader code-quality review.

## `writing-plans`

Source reviewed: `/Users/hyzhang/Project/superpowers/skills/writing-plans/SKILL.md`

### What the skill does well

The skill is strong at making implementation intent durable.

Its useful parts are:

- writing the plan to an external file
- forcing a goal, architecture, and file structure
- requiring concrete verification steps
- preventing placeholders and vague future work
- making the plan inspectable by both humans and agents

The strongest idea is not the exact step format. The strongest idea is that implementation should have a durable source of truth outside the agent's memory.

### Main criticism

The skill micromanages capable agents.

It assumes the implementer needs exact files, exact code, exact test code, exact commands, and tiny 2-5 minute steps. That may help a weak or isolated worker, but it can suppress a strong agent's ability to inspect the codebase and choose the best approach.

It can also freeze the wrong implementation path into the plan. Once the plan contains exact code, later review may check compliance with a bad plan instead of checking whether the user goal was achieved.

### Why it may fail in practice

The plan can become more authoritative than the user's intent.

If the agent invents constraints, chooses an approach too early, or writes detailed steps before understanding the codebase, the plan can look solid while encoding speculation. The more detailed the plan, the more convincing the speculation becomes.

This is especially risky when the user gave a simple desired outcome, not a full design.

### What would make it stronger

For mission-based implementation, replace the full implementation plan with a compact mission brief:

```markdown
# Mission Brief

## Source of Intent

**Initial User Request:** ...

**Clarifications:**
- ...

**Interpreted Intent:** ...

## Formal Requirements

| Requirement | Source | Done When | Evidence |
|---|---|---|---|
| ... | ... | ... | Pending |
```

The mission brief should define what success means, not how to implement it.

The agent should use the incomplete brief as the clarification instrument. If a requirement, source, or `Done When` cannot be filled without guessing, that gap triggers a focused question.

### Bottom line

`writing-plans` is right that intent must be durable and inspectable.

It is wrong to make the plan a micromanaged implementation script for every capable agent. The better abstraction is a source-traceable mission brief.

## `verification-before-completion`

Source reviewed: `/Users/hyzhang/Project/superpowers/skills/verification-before-completion/SKILL.md`

### What the skill does well

The skill attacks one of the most damaging agent behaviors: claiming success without evidence.

Its useful parts are:

- identify what proves the claim
- run the check fresh
- read the output
- verify exit codes, failures, and actual result
- distinguish tests, builds, lint, bug reproduction, and requirements completion
- reject "should work" language

The strongest idea is evidence before claims.

### Main criticism

The skill is rhetorically heavy and not specific enough about choosing verification.

It is full of moralized language and red-flag tables. That may be useful pressure in some contexts, but it consumes context and can feel like defensive scolding rather than operational guidance.

It also says to run verification, but it does not always tell the agent how to choose the right verification method for a specific requirement.

### Why it may fail in practice

Agents can satisfy the surface rule with weak evidence.

Examples:

- run a build and claim behavior is fixed
- run unrelated tests and claim requirements are met
- point at code or a diff as proof
- say "tests passed" without exercising the changed path
- use existing code as evidence that new behavior works

For mission work, verification must be tied to each formal requirement, not just to a general success claim.

### What would make it stronger

Verification should be part of the mission table.

Each requirement should have:

- `Done When`: the verification method planned before implementation
- `Evidence`: the observed facts collected after exercising changed behavior

Good evidence should come from real execution or observation:

- command output
- test output
- build output
- logs
- response bodies
- data changes
- rendered output
- generated files

Existing code or the diff itself is not satisfaction evidence.

For logging, the agent should not spam the codebase. It should:

- reuse existing logs when possible
- enhance an existing log if needed
- add the smallest new log only when necessary for verification

### Bottom line

The skill's principle is essential, but the implementation should be leaner and more requirement-specific.

Evidence should live next to the requirement it proves.

## `subagent-driven-development`

Source reviewed:

- `/Users/hyzhang/Project/superpowers/skills/subagent-driven-development/SKILL.md`
- `/Users/hyzhang/Project/superpowers/skills/subagent-driven-development/implementer-prompt.md`
- `/Users/hyzhang/Project/superpowers/skills/subagent-driven-development/spec-reviewer-prompt.md`

### What the skill does well

The skill has a valuable idea: separate implementation from review.

Its useful parts are:

- fresh worker per task
- explicit task text instead of relying on hidden context
- implementer status reporting
- spec-compliance review
- code-quality review
- escalation when the task is unclear or too hard

The strongest idea is context isolation. A fresh reviewer can be less anchored to the implementer's assumptions.

### Main criticism

It over-relies on subagents and plan compliance.

Subagents are useful tools, but they are not magic. A reviewer with less context may be less biased, but also less informed. If the plan is wrong, subagents can efficiently execute and review the wrong thing.

The skill also assumes a plan already decomposes work correctly. That makes sense for large subagent-driven execution, but it is too much machinery for normal task implementation.

### Why it may fail in practice

AI-to-AI loops can create review theater.

An implementer reports success. A reviewer checks the report and diff. Another reviewer checks quality. This can look rigorous while still missing the user's actual intent if the source of truth is weak.

The problem gets worse if reviewer findings become new requirements without human confirmation.

### What would make it stronger

Use subagents selectively.

For mission-based implementation:

- default to main-agent mission review
- reload the saved mission brief from disk before review
- verify each formal requirement with observed evidence
- allow at most three implementation-review rounds
- do not let reviewer findings become new requirements unless the human updates the mission
- use a subagent only for large, risky, or explicitly requested independent review

The loop should be bounded and grounded in the mission file, not in agent memory or broad reviewer imagination.

### Bottom line

Subagents are useful for independence, but they should not be the core abstraction.

The core abstraction should be a durable mission brief plus bounded evidence-based review.

## `using-git-worktrees` / `finishing-a-development-branch`

Source reviewed:

- `/Users/hyzhang/Project/superpowers/skills/using-git-worktrees/SKILL.md`
- `/Users/hyzhang/Project/superpowers/skills/finishing-a-development-branch/SKILL.md`
- `/Users/hyzhang/Project/superpowers/skills/executing-plans/SKILL.md`
- `/Users/hyzhang/Project/superpowers/skills/subagent-driven-development/SKILL.md`

### What the skills do well

The skills are trying to prevent dangerous branch and worktree mistakes.

Their useful parts are:

- detect whether the current checkout is already a linked worktree
- prefer harness-native worktree tools over raw `git worktree` commands
- create an isolated workspace before feature work when appropriate
- verify tests before offering finish options
- avoid removing a worktree needed for PR iteration
- require typed confirmation before discarding work
- distinguish Superpowers-owned worktrees from harness-owned workspaces

The strongest idea is operational caution around Git state. Worktree cleanup is easy to get wrong: deleting a branch before removing the worktree can fail, removing a harness-owned worktree can create phantom state, and discarding work without confirmation can destroy user-owned context.

### Main criticism

The lifecycle is fractured.

`using-git-worktrees` owns creation and branch attachment. `finishing-a-development-branch` owns merge, PR, keep, discard, and cleanup. The coordination between them mostly lives in orchestration skills such as `executing-plans` and `subagent-driven-development`.

That means the finish skill assumes context it does not guarantee. If an agent enters `finishing-a-development-branch` directly, it may not know whether the worktree was created by Superpowers, by the harness, manually by the human, or not at all.

The detached HEAD path exposes the gap most clearly. `using-git-worktrees` says branch creation is needed at finish time, and `finishing-a-development-branch` offers "Push as new branch and create a Pull Request," but the finish skill does not show the branch creation command:

```bash
git switch -c <feature-branch>
git push -u origin <feature-branch>
```

For named worktree branches, the happy path is mostly complete. For detached HEAD and missing-provenance cases, the process is underspecified.

### Why it may fail in practice

The skills mix two different layers:

- operational Git knowledge: inspect, create, attach, switch, push, remove, prune
- workflow authority: start an isolated branch, dispatch subagents, complete a development branch, create a PR, merge, discard

Those should not have the same authority level.

The human should initiate workflow phases. A worktree skill can teach the agent how to create and clean up worktrees, but it should not silently decide to enter an isolated-workspace workflow. A finishing skill can teach the agent how to safely finish a branch, but it should not independently decide whether to merge, PR, discard, or clean up.

This is the "lazy human mode" risk: the agent becomes the workflow owner, the human becomes a passive approver, and broad autonomous execution starts to look normal. That may feel convenient, but it weakens accountability. The human should remain active, choose transitions, and intervene when scope or tradeoffs appear.

### What would make them stronger

Separate command competence from workflow initiation.

`using-git-worktrees` should be framed as:

> How to inspect, create, and enter a worktree when the human has asked for isolation.

`finishing-a-development-branch` should be framed as:

> How to safely finish an existing branch or worktree when the human has asked to finish.

The handoff contract should be explicit. Creation should report:

- worktree path
- branch name or detached HEAD state
- base branch
- creation method: native tool, raw git, manual, or unknown
- cleanup owner: harness, Superpowers, human, or none

Finishing should reconstruct or validate that state before presenting options. If provenance is missing, it should stop and ask instead of assuming.

Workflow-composition skills should not silently require other skills. They should say which phases may be needed and ask before entering them:

- set up branch/worktree
- dispatch subagents
- create PR
- merge locally
- discard work
- clean up workspace

Subagents should also be small-task tools, not a default development engine. Each agent task should be bounded enough to produce one self-contained commit. If several commits seem necessary, the task is probably too large and should be decomposed by the human first.

### Bottom line

The worktree skills contain useful Git safety knowledge, but the lifecycle boundary is wrong.

They should not let agents silently compose a full development workflow. The human should initiate workflow phases, and the skills should provide precise operational procedures for the phase the human chose.

## Synthesis: mission-based implementation

### What our discussion converged on

The best parts of the Superpowers skills are real:

- durable intent from `writing-plans`
- requirement-alignment review from `requesting-code-review`
- evidence-before-claims from `verification-before-completion`
- skepticism toward unverified feedback from `receiving-code-review`
- context isolation from `subagent-driven-development`
- Git-state caution from `using-git-worktrees` and `finishing-a-development-branch`

But each skill also has a tendency to overgrow:

- `writing-plans` becomes micromanagement
- `requesting-code-review` becomes broad review theater
- `verification-before-completion` becomes rhetorical burden
- `receiving-code-review` gives the agent too much role ownership in human review
- `subagent-driven-development` makes subagents the default instead of a selective tool
- worktree and finishing skills blur command knowledge with workflow authority

### Improvement plan

The proposed replacement abstraction is an `execute-mission` workflow:

1. Create a mission brief before editing.
2. Use the incomplete mission brief to drive clarification.
3. Store the mission brief outside the repo by default, such as `/tmp/docs/missions/...`.
4. Let the agent choose the implementation approach.
5. Review by reloading the saved mission brief from disk, not memory.
6. Verify each requirement by exercising changed behavior.
7. Update the `Evidence` column with observed facts.
8. Iterate at most three rounds.
9. Append final mission status to the mission brief.
10. Keep broad code-quality review separate and optional.

### Bottom line

The best Superpowers pattern is not "more skills."

The better pattern is a smaller number of sharper skills with durable intent, source-backed requirements, observed evidence, and clear human ownership.
