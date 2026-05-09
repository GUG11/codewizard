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
