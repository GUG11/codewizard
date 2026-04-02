---
name: system-design
description: Use this skill when the user wants structured system design help, including requirement framing, architecture decomposition, tradeoff analysis, scaling decisions, reliability design, and clear design writeups.
---

# System Design

Use this skill to design, review, or explain real software systems, including online services, offline pipelines, data platforms, training infrastructure, and distributed systems.

## Goal

Produce a design writeup explicit about:

- requirements
- constraints
- scale
- architecture
- data flow
- execution flow
- failure modes
- tradeoffs
- rollout and operations

Do not jump to components before the problem is framed.
Write for decision-making, review, implementation, and operations.

## Default Workflow

### 1. Frame the problem

Start by defining:

- what the system must do
- who uses it
- the main user flows
- hard constraints such as latency, consistency, compliance, cost, or deadline
- what is out of scope

Do not make assumptions in this step. If anything is unclear, keep asking until the problem, constraints, and scope are clear enough to design correctly.

### 2. Separate functional and non-functional requirements

Capture:

- functional requirements: behaviors, APIs, workflows, data operations
- non-functional requirements: scale, availability, latency, throughput, durability, security, observability, operability, cost, resource efficiency, each expressed with clear metrics, measurement, and forecast when future demand matters

Do not finalize these requirements yourself. If anything is unclear, ask for clarification until the requirements are measurable. If the needed metrics do not exist yet, state what initial data must be collected, how it should be measured, and how future demand should be forecast from that data before locking the design. Present the proposed requirements, metrics, forecasts, and priorities to the user and wait for explicit approval before moving forward, because a design cannot optimize every dimension at once.

### 3. Define interfaces and interactions

Define the interfaces and interaction patterns before detailed sizing. Capture:

- the main interfaces and the systems they connect
- the request, response, event, or data contract for each interface
- whether each interaction is synchronous or asynchronous
- idempotency, retry, timeout, and error behavior
- ownership boundaries and responsibilities across systems
- what each interface guarantees and what its consumers can assume

### 4. Draw the end-to-end flow

Describe the path through the system in the form that fits it:

- user request path for online systems
- job, stage, and dependency flow for offline systems
- data ingestion, transformation, storage, and consumption flow for data systems
- training, evaluation, checkpoint, and serving handoff flow for ML systems

Start with one primary flow. Add secondary flows only if they change the design. If there is more than one critical workflow, separate them clearly instead of blending them in prose.

### 5. Deep dive the design

This is the main design step. Do not stop at component listing. Answer one question directly: how does the design meet the prioritized non-functional requirements with the least overall cost?

Treat cost broadly:

- infrastructure and resource cost
- engineering and migration cost
- operational burden
- reliability risk
- complexity and future change cost

Push hard on tradeoffs. For every major design choice:

- state which non-functional requirement it serves
- state what cost it introduces
- identify the credible solution space for the decision and try to exhaust it before narrowing
- compare their pros, cons, and tradeoffs against the stated priorities
- choose one solution and explain why it is the best fit
- state the main drawbacks of the selected solution and how to mitigate them

Compare solutions only when the alternatives are genuinely credible. Do not pad the comparison with obviously bad options that fail the requirements or would be immediately rejected by competent engineers. If only one solution is credible, say so directly and explain why.

Prefer the minimum architecture that satisfies the requirements. Add replication, caching, queues, coordination, partitioning, or extra services only when they buy a concrete non-functional benefit that a simpler design cannot provide.

Cover scale, storage, consistency, bottlenecks, and failure handling only where they materially affect the tradeoff or the recommendation. Do not turn this section into a checklist.

Use measured traffic, latency, throughput, storage, growth, and failure data to support design decisions. When future demand matters, derive forecasts from real initial data and state the forecast basis and validation plan. If the required metrics are missing, call out the gap and specify what should be instrumented or measured before finalizing the design. Do not invent traffic assumptions without a measured basis.

### 6. Plan operations and observability

Include:

- service-level indicators and objectives if relevant
- logs, metrics, and traces
- alert triggers
- backpressure or rate limiting
- deployment and rollback strategy
- capacity planning knobs
- job scheduling, priority, quota, and admission control where relevant
- dataset, model, or artifact version tracking where relevant

If the design cannot be operated safely, it is incomplete. If the system will evolve, call out migration and backfill paths.

## Output Structure

When presenting a design, follow the same progression as the workflow:

1. Problem framing
2. Requirements, metrics, and priorities
3. Interfaces and interactions
4. End-to-end flow
5. Deep design analysis
6. Operations and observability

For an article or design note aimed at mixed business and technical readers:

- start with a short outcome-oriented summary before the detailed sections
- keep the architecture explanation readable without removing the technical mechanism
- separate facts, measurement gaps, interpretation, and recommendation
- explain why this design fits the actual organization, constraints, and operating environment

## Review Mode

Review the design against one question: does it satisfy the prioritized, measurable requirements with the least overall cost?

Focus the review on the few decisions that dominate cost, risk, and system behavior. Do not grade the design by checklist coverage.

Check:

- whether the problem, scope, constraints, and success conditions are clear enough to judge the design
- whether the functional and non-functional requirements are explicit, measurable, and prioritized
- whether each major component is justified by a concrete requirement or constraint rather than habit, fashion, or premature scaling
- whether major decisions identify the credible solution space, try to exhaust it before narrowing, compare real pros and cons, make a clear choice, and explain why that choice wins
- whether the comparison avoids obviously bad alternatives that exist only to make the chosen design look good
- whether the tradeoff analysis is grounded in measured traffic, latency, throughput, storage, growth, and failure data and, when future demand matters, forecasts derived from real initial data
- whether the design states the main drawbacks of the selected solution and explains how they are mitigated
- whether the system can be deployed, monitored, rolled back, recovered, and evolved safely in the real environment

Treat cost broadly: infrastructure and resource cost, engineering and migration cost, operational burden, reliability risk, and complexity or future change cost.

Be highly critical. Focus on the decisions that materially affect the recommendation. If the design is underspecified, say exactly what information or metrics are missing and what must be measured before a confident judgment is possible.
