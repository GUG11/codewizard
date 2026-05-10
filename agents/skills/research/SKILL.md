---
name: research
description: Use for ambiguous, open-ended problems where the correct answer is not already known and the main task is to search, evaluate, decompose, and synthesize before execution.
---

# Research

## Core Loop
Follow this loop until the question is understood well enough to produce a reliable answer or until the remaining unknowns must be surfaced explicitly:
- Search for candidate answers, prior work, experiments, papers, documents, and technical writeups relevant to the current question or sub-question.
- Validate each source before relying on it.
- Evaluate what part of the question each result actually answers.
- Identify what remains unanswered, weakly supported, or inconsistent.
- Break the unresolved part into smaller sub-questions.
- Reuse validated partial answers as inputs, constraints, or building blocks for those sub-questions.
- Synthesize the accepted pieces into a candidate overall answer.
- Re-evaluate the synthesized answer against the original question, not just the sub-questions.

## Source Validation
- Reject answers that are not fact-based.
- Reject answers that overclaim beyond their evidence.
- Reject answers that rely on partial facts or partial reasoning when those gaps materially weaken the claim.
- Prefer real-world facts and realistic experiments over toy problems or artificial conditions.

## Cross-Checking
- Cross-check multiple sources instead of relying on the first plausible answer.
- Identify where sources agree, partially overlap, or directly conflict.
- For inconsistencies, reason about which source is more credible for the current question and why.
- Consider differences in assumptions, metrics, baselines, workload, environment, scale, dataset, hardware, and scope before deciding whether two sources are truly inconsistent.
- Do not average conflicting claims together. Resolve the conflict when the evidence supports doing so. If it cannot be resolved confidently, state that plainly.

## Coverage Evaluation
- Evaluate each source or candidate answer against the actual question, not against keyword similarity.
- For each candidate, determine:
  - what exact part of the question it answers
  - how completely it answers that part
  - what assumptions, constraints, or prerequisites it depends on
  - what remains unanswered
  - whether it composes cleanly with other partial answers
- Keep partial answers that fully support the part they answer.
- Reject answers that attempt to answer more than their facts or reasoning can support.
- Use valid partial answers to map coverage and drive decomposition of the remaining gaps.

## Decomposition and Recombination
- If no single candidate answers the question fully, break down the unresolved parts into smaller sub-questions.
- Use partial answers from earlier search and evaluation as inputs to the relevant sub-questions whenever they remain valid.
- Keep decomposition purposeful. Stop when sub-questions are specific enough to investigate effectively or when further decomposition stops producing better understanding.
- After resolving sub-questions, synthesize the validated pieces and test whether the overall answer satisfies the original question, constraints, and tradeoffs.
- Do not assume that individually valid partial answers are compatible. Check the synthesized result at the whole-question level.

## Output
- Present the final result as a structured reasoning summary, not as a chronological search log or raw chain-of-thought.
- The output should give a clear, well-supported answer and explain:
  - how the original question was framed
  - how the question was broken down
  - which source categories and evidence were trusted or rejected
  - which partial answers were accepted, rejected, or revised
  - where sources conflicted and how the conflict was resolved
  - how the final answer was synthesized
  - what answer, explanation, or recommendation follows from that analysis
- Keep the summary high-compression and decision-oriented. Show the reasoning path clearly without narrating every iteration.
- If important gaps remain unresolved, state them plainly instead of overstating confidence.
