---
name: technical-article-writing
description: Use when the agent is writing an article about code, an implementation, or completed engineering work. Provides the judgment needed to produce high-information-density technical articles grounded in precise code pointers and causal explanation.
---

# Technical Article Writing

## Format
Choose a format that supports engineering diagrams, such as DAGs and timelines, as well as SVGs and hyperlinks. Avoid plain text when richer structure is available.

## Judgment on Presenting Code
Never include code snippets or code blocks in the article. Explain the implementation in prose and point readers to exact code locations through remote source links.

Bad examples you should avoid:
- Creating a dedicated code section that reproduces key code. Detached code is difficult to connect to the exact explanation it supports.
- Linking an entire sentence when only one action is backed by the code. For example: [Print the block prompt and exit with status 2 when a second mission is attempted](https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_identity.py#L35-L36). Broad link spans make the prose feel covered in hyperlinks and obscure which action the source supports.
- Linking a broad function or block range when the article claims one action. For example, `https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_identity.py#L28-L36` makes the reader hunt for the specific line that proves the sentence.
- Packing several behaviors behind a one-line link. For example, do not claim that the hook reads the payload, detects an approved mission, resolves the target path, and [blocks](https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_identity.py#L35) a second mission; that line only prints the block prompt.

Good examples:
Hyperlink the shortest action-bearing verb or verb phrase supported by each code pointer. For example: [Prints](https://github.com/GUG11/codewizard/blob/df5d9efb684e60ee959281cd24b7b5e8f33e053f/plugins/codewizard/hooks/guard_mission_identity.py#L35) the block prompt.

Use one-line source links. This is non-negotiable.

For every source-backed sentence:
1. Identify each technical verb, such as `reads`, `filters`, `emits`, `maps`, `raises`, `returns`, or `prints`.
1. Link only that verb or its shortest verb phrase.
1. Point the link to the single source line that directly proves the verb.
1. If one line cannot prove the linked phrase, split the sentence into smaller claims until each link has one proving line.
1. Do not use `and`, `or`, comma lists, or `such as` inside a linked claim unless the same one line proves every listed item.
1. Do not use range anchors such as `#L28-L36`.

## Judgment on Organization
Do not organize the article as a linear inventory of code locations followed by an explanation of each location.

Bad example:
1. Lines 20-30 contain the main entry point.
2. Lines 30-45 initialize the server, set parameters, and start the loop.
3. Lines 45-100 define the `handleRequest` interface.
4. Lines 101-168 define the `ack` interface.

This is bad because it inflexibly narrates the code layout. It has low information density and does not explain how the parts combine to form a functioning service.

Instead, organize the article as a causal story that explains how the parts interact and why they produce the observed behavior.

Good example:

In `service_main.cpp`, the service exposes two interfaces:
- `handleRequest` processes requests and returns the results.
- `ack` acknowledges loopback signals posted by the client.

The service is initialized with the x, y, and z parameters and immediately starts the endless loop.

Once the causal story is clear, there is no need to identify the main entry point explicitly; its role is already evident.

## Avoid Defensive and Conservative Wording
When incorporating user feedback, do not protect the article from being wrong by adding low-value negations, hedges, apologies, or meta commentary. Make the article more correct, more direct, and more useful.

When the user points out an error in previous writing, treat the feedback as a correction to the article, instead of wording to copy into the article. Replace the wrong claim with the corrected claim.

Example: you wrote "A is the component for ads retrieval." The user points out: "A is deprecated and replaced by B."

Bad revision:
"A is not the component for ads retrieval. B is currently used for ads retrieval."

Good revision:
"B is the component for ads retrieval."

When the user challenges an overclaim, do not retreat into a weaker statement that is merely hard to dispute. Replace the overclaim with the direct useful answer to the same technical question.

Example: you wrote "A, B, and C are the prerequisites to achieve D." The user challenges: "I do not think A and B are prerequisites."

Bad revision:
"A and B are not prerequisites to achieve D."

This revision is safe but low value. It responds to the challenge, but it no longer answers the original question: what conditions are required to achieve D?

Good revision:
"C and E are the prerequisites to achieve D."

## Checklist before finishing
Check these items before claiming you finished it.

1. Are all action-bearing verbs or verb phrases in code explanations annotated with verified source links?
1. Are all hyperlinks pointed to a single line of code instead of a broad range?
1. Are all hyperlinks valid? Did you get the links from the correct source instead of forging it?
1. Did you turn user feedback into cleaner article prose instead of defensive negation?
1. Did you replace challenged overclaims with a direct useful answer instead of safe but inconclusive wording?
