# Becoming a Super IC in the Agentic Era

*A Practical Roadmap*

## Definition

A **Super IC in the agentic era** is an engineer who:

* defines technical problems
* designs system architectures
* directs AI agents to execute work
* validates outputs and detects errors
* makes final technical decisions

Agents perform execution.
The engineer retains **judgment and direction**.

---

# Scope

This roadmap is for building an engineering operating model where agents handle bounded execution and the engineer owns problem framing, architecture, validation, and decision-making.

The goal is not full autonomy.
The goal is high-leverage supervised execution with clear controls.

---

# Core Responsibilities

### Problem Definition

Convert high-level goals into precise technical problems with clear constraints, interfaces, and success criteria.

### System Architecture

Design the system structure, select technical approaches, and define trade-offs before execution begins.

### Agent Orchestration

Route work to specialized agents for research, implementation, testing, profiling, and review.

### Validation and Debugging

Verify agent outputs, detect mistakes quickly, and isolate root causes.

### Technical Decision-Making

Choose architecture, experiments, and engineering direction based on evidence rather than agent confidence.

---

# Prerequisites

Before scaling agent usage, establish a shared execution platform:

* repository access, shell access, and file edit permissions
* reproducible local or remote execution environments
* test and benchmark harnesses that agents can invoke safely
* logging, trace collection, and artifact storage
* task history, prompts, and result tracking for auditability
* rollback paths for code, configs, and experiments
* approval gates for high-risk actions such as production changes or broad refactors

If these foundations are weak, agent quality will appear worse than it is because the environment is unstable.

---

# Operating Principles

* keep agents specialized rather than building one general agent too early
* prefer supervised automation before bounded autonomy
* measure reliability with task success rates, correction rates, and turnaround time
* treat validation as a first-class capability, not a cleanup step
* keep humans responsible for architecture, prioritization, and irreversible decisions

---

# Phase 1 — Build Core Execution Agents (Month 1)

## Goal

Establish reliable agents that remove routine engineering work without weakening code quality.

## Deliverables

* stabilize the **code agent** so it can read repositories, edit files, run commands, and execute tests consistently
* build the **research agent** for targeted technical investigation
* build the **writer agent** for recurring engineering communication
* define a standard task contract for all agents: inputs, expected outputs, tools, and human review points

## Agent Boundaries

### Research Agent

Responsibilities:

* discover existing solutions
* compare trade-offs
* validate assumptions against the current stack
* recommend approaches suitable for the environment

Outputs:

* short recommendation memo
* source references
* explicit trade-off summary

### Code Agent

Responsibilities:

* implement scoped features
* fix bugs
* write tests
* run benchmarks

Outputs:

* code changes
* test updates
* execution summary with known risks

The code agent should not own broad refactors or ambiguous product decisions in this phase.

### Writer Agent

Responsibilities:

* write weekly reports
* draft implementation plans
* draft design documents
* write launch posts

Outputs:

* status summaries
* structured plans
* design drafts
* release communication drafts

The writer agent should focus on drafting and synthesis, not final approval of strategy or technical correctness.

## Exit Criteria

* agent completes common repository tasks end-to-end without manual environment repair
* task success rate is consistently measurable
* test execution is reliable enough to use as a quality gate
* human review time per routine task is materially reduced

## Success Metrics

* task completion rate for routine engineering tasks
* percentage of outputs requiring human correction
* median turnaround time from task assignment to validated result
* percentage of code changes accompanied by passing relevant tests

---

# Phase 2 — Expand Analysis and Connect Workflows (Month 2)

## Goal

Automate experiment analysis and connect specialized agents into repeatable pipelines.

## Deliverables

* build the **data / profiling agent**
* standardize logs, traces, benchmark outputs, and experiment artifacts so they are machine-readable
* connect research, code, and analysis agents into sequential workflows

## Data / Profiling Agent

Responsibilities:

* analyze experiment logs
* interpret profiling traces
* summarize results
* identify performance bottlenecks
* flag regressions against a baseline

Outputs:

* performance summary
* bottleneck diagnosis
* recommended next action

## Workflow Pattern

A typical supervised pipeline in this phase:

research → implementation → test → profiling → review

Each stage should emit artifacts that the next stage can consume directly.

## Exit Criteria

* profiling and experiment analysis can run without manual data cleanup
* agent handoffs are structured and reproducible
* performance regressions are detected before final human approval
* common multi-step tasks can be executed through a standard workflow

## Success Metrics

* percentage of experiment reports generated automatically
* time required to diagnose a regression
* percentage of pipeline runs that complete without handoff failure
* reduction in manual analysis time for profiling and experiment review

---

# Phase 3 — Introduce Planning and Bounded Autonomy (Month 3)

## Goal

Coordinate agents through a planner and enable bounded autonomous execution loops under explicit control.

## Deliverables

* introduce a **planner agent**
* orchestrate multi-agent pipelines with task decomposition and routing
* enable bounded autonomous loops for safe classes of engineering work

## Planner Agent

Responsibilities:

* decompose complex tasks
* assign work to specialized agents
* coordinate execution order
* collect outputs into a decision-ready summary

Outputs:

* task graph
* execution plan
* consolidated status and blockers

## Default Workflow

planner → research → implementation → profiling → review

## Bounded Autonomous Loop

Allowed pattern:

* detect issue
* propose solution
* implement scoped change
* run tests or experiments
* evaluate results
* stop for approval or iterate within preset limits

Boundaries:

* no production changes without human approval
* no large refactors without explicit approval
* no repeated retries beyond a fixed limit
* no autonomous execution when validation signals conflict

## Exit Criteria

* planner-generated workflows are understandable and auditable
* bounded autonomous loops improve speed without increasing defect rates
* failure conditions trigger safe stop behavior
* humans review fewer intermediate steps while still controlling key decisions

## Success Metrics

* percentage of complex tasks decomposed correctly on first pass
* percentage of autonomous loops that terminate successfully within limits
* defect rate of agent-driven changes versus human-only baseline
* number of interventions required per multi-agent workflow

---

# Governance and Risk Controls

To prevent automation from increasing hidden risk, enforce the following controls:

* human approval for architecture changes, production operations, and wide-scope code modifications
* required validation artifacts for code, performance, and experiment outcomes
* rollback procedures for every automated change path
* logging of prompts, actions, outputs, and approvals
* periodic review of failure cases, hallucinations, and unnecessary agent coordination overhead

Common failure modes:

* plausible but incorrect implementation
* missing edge-case validation
* degraded performance hidden behind functional correctness
* context loss across agent handoffs
* wasted effort from poor task decomposition

---

# Final Operating Model

Engineer:

* defines problems
* sets architecture
* approves high-impact decisions
* interprets ambiguous results

Agents:

* research
* implement
* test
* analyze
* summarize

System:

* executes repeatable engineering workflows
* tracks artifacts and decisions
* enforces control boundaries

A Super IC becomes the architect and operating lead of an AI-assisted engineering organization.
