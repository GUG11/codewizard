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
- non-functional requirements: scale, availability, latency, throughput, durability, security, observability, operability, cost, resource efficiency

Do not finalize these requirements yourself. If anything is unclear, ask for clarification. Present the proposed set to the user and wait for explicit approval before moving forward. Prioritize only after approval, because a design cannot optimize every dimension at once.

### 3. Define APIs and system boundaries

Define the API before sizing the system. Capture:

- the main APIs
- request and response shape
- idempotency, retry, and error behavior
- sync vs async interaction
- ownership boundaries between services
- what the caller can assume and what the service guarantees

Without a clear API, architecture and scale discussions drift.

### 4. Draw the end-to-end flow

Describe the path through the system in the form that fits it:

- user request path for online systems
- job, stage, and dependency flow for offline systems
- data ingestion, transformation, storage, and consumption flow for data systems
- training, evaluation, checkpoint, and serving handoff flow for ML systems

Start with one primary flow. Add secondary flows only if they change the design. If there is more than one critical workflow, separate them clearly instead of blending them in prose.

### 5. Deep dive the design

This is the main design step. Do not stop at component listing. Defend the design across scale, data lifecycle, bottlenecks, consistency, failure handling, and tradeoffs.

Cover scale where it changes the design:

- requests per second
- jobs per day or per hour
- read/write ratio
- peak vs average load
- storage volume and growth
- object sizes
- retention period
- regional distribution
- compute footprint such as CPU, GPU, memory, disk, or network pressure

Tie estimates to the API and workflow you already defined. Use order-of-magnitude estimates when exact numbers are unavailable, but prefer real constraints, observed bottlenecks, and known operating conditions over hypothetical scale theater. If no numbers are available, state which assumptions would most change the design.

Define the core entities and data lifecycle:

- where each object is created
- how it is read and updated
- whether it is mutable or append-only
- retention and deletion rules
- consistency requirements

Use this to drive storage and caching choices.

Choose the architecture around bottlenecks:

- identify the dominant bottlenecks in throughput, latency, coordination, storage, and team ownership
- identify whether the main pressure is online latency, offline throughput, scheduling, data locality, model training time, resource contention, or recovery cost
- pick components based on those bottlenecks, not habit
- for every major component, explain why it exists, what problem it solves, and what breaks if it is omitted

Address partitioning, replication, and consistency:

- partition key or sharding strategy
- replication model
- leader/follower or multi-writer behavior
- consistency guarantees needed by each workflow
- conflict handling if writes can race

State where eventual consistency is acceptable and where it is not. For offline and ML systems, also cover dataset versioning, checkpoint lineage, reproducibility, and backfill behavior when relevant.

Design for failures first, not last:

- service instance loss
- zone or region failure
- queue backlog
- cache stampede
- database hotspot
- duplicate delivery
- partial writes
- downstream timeout
- retry storms
- scheduler failure
- job retry corruption
- partial backfill
- bad model or bad data rollout

For each important failure, note detection, mitigation, and user-visible impact. Do not claim reliability without naming the failure-handling path.

Evaluate tradeoffs and alternatives:

- consistency vs availability
- latency vs cost
- simplicity vs flexibility
- write amplification vs read efficiency
- operational burden vs feature velocity

Compare the chosen design against at least one credible alternative when the decision is non-obvious or materially affects cost, reliability, team velocity, or future change. Recommend one option and explain why it best fits the stated priorities.

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
2. Requirements and assumptions
3. APIs and system boundaries
4. End-to-end flow
5. Deep design analysis
6. Operations and observability

For an article or design note aimed at mixed business and technical readers:

- start with a short outcome-oriented summary before the detailed sections
- keep the architecture explanation readable without removing the technical mechanism
- separate facts, assumptions, interpretation, and recommendation
- explain why this design fits the actual organization, constraints, and operating environment

## Review Mode

Review the design in the same progression as the main workflow:

1. Problem framing
Is the design solving the right problem, with clear scope, constraints, and success conditions?

2. Requirements
Are the functional and non-functional requirements explicit, prioritized, and approved by the user?

3. APIs and system boundaries
Are the APIs clear, ownership boundaries explicit, and responsibilities placed in the right systems?

4. End-to-end flow
Is the main flow coherent, complete, and free of handoff ambiguity or hidden complexity?

5. Deep design analysis
Does the design go deep enough on scale, bottlenecks, data lifecycle, consistency, failure handling, and tradeoffs? Are major components justified by real pressure rather than habit?

6. Operations and observability
Can the system actually be deployed, monitored, rolled back, migrated, and recovered safely?

Be highly critical. Keep challenging the design until every important part is defended with clear reasoning, explicit constraints, and concrete mechanisms. Do not accept shallow coverage across all sections. Focus on the dimensions that carry real system risk.

Prioritize correctness, resilience, operability, and fit for the real environment over novelty. If a design is underspecified, say exactly what missing information blocks a confident judgment.
