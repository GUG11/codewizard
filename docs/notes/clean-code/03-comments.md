# Comments

Status: learning note, not repository policy.

Source: Robert C. Martin, *Clean Code*, Chapter 4, adapted for the agentic era.

## Top principle

The best comment is usually no comment because the code already carries the meaning.
Prefer clear names, structure, and tests first. Add a comment only when the code cannot
express important rationale, constraints, public contracts, warnings, or temporary debt
clearly enough by itself.

In the agentic era, comments matter because agents read them as context. A useful comment
can prevent a wrong edit; a stale or redundant comment can mislead an agent at scale.

## Principles

### 1. Express intent in code before adding a comment.

Why: a comment that explains confusing code is usually weaker than code that carries the
same meaning directly. The comment and code can drift apart, while a better name or
function boundary stays attached to the executable behavior.

Good:

```js
if (employee.isEligibleForFullBenefits()) {
  enroll(employee);
}
```

Bad:

```js
// Check whether the employee is eligible for full benefits.
if ((employee.flags & HOURLY_FLAG) && employee.age > 65) {
  enroll(employee);
}
```

Contrast: the good version puts the business concept in the code. The bad version leaves
the reader to trust a comment while decoding flags and age logic.

### 2. Use comments for rationale, constraints, or warnings.

Why: some important information is not visible from the code shape alone. A comment earns
its place when it explains why a surprising choice exists, warns about a hidden constraint,
or preserves reasoning that future maintainers need before changing the code.

Good:

```js
function createHttpDateFormatter() {
  // DateFormatter is mutable and not thread-safe; create one per request.
  return new DateFormatter("EEE, dd MMM yyyy HH:mm:ss z", "GMT");
}
```

Bad:

```js
// Create formatter.
function createHttpDateFormatter() {
  return new DateFormatter("EEE, dd MMM yyyy HH:mm:ss z", "GMT");
}
```

Contrast: the good comment explains the concurrency constraint behind the allocation.
The bad comment repeats the function name and adds no decision-relevant information.

### 3. Keep comments local, accurate, and verifiable.

Why: comments become dangerous when they describe information owned somewhere else. The
farther a comment is from the behavior it describes, the more likely it is to become stale
or misleading.

Good:

```js
function waitForClose(timeoutMs) {
  if (closed) {
    return;
  }

  wait(timeoutMs);

  if (!closed) {
    throw new Error("Response did not close before timeout");
  }
}
```

Bad:

```js
/**
 * Returns when `closed` becomes true. Throws if the timeout is reached.
 */
function waitForClose(timeoutMs) {
  if (closed) {
    return;
  }

  wait(timeoutMs);

  if (!closed) {
    throw new Error("Response did not close before timeout");
  }
}
```

Contrast: the good version avoids a comment because the code and error message make the
actual behavior checkable. The bad comment overclaims: the function does not return as
soon as `closed` becomes true; it waits once, then checks. That inaccurate promise is worse
than no comment.

### 4. Do not preserve history, ownership, or dead code in comments.

Why: version control is better at preserving history than comments are. Commented-out
code, bylines, and change journals make readers wonder whether stale text still matters,
and agents may treat that stale text as live intent.

Good:

```js
writeHeader();
writeImageData();
writeEnd();
```

Bad:

```js
writeHeader();
// dataPos = bytePos;
writeImageData();
// this was added by Rick for the old encoder
writeEnd();
```

Contrast: the good version leaves only executable intent. The bad version keeps historical
debris that belongs in version control or an issue tracker.

### 5. Keep TODOs actionable and temporary.

Why: a TODO can be useful when it records known, bounded work that cannot be completed
now. It becomes noise when it is vague, ownerless, or used as permission to leave bad code
behind indefinitely.

Good:

```js
// TODO(checkout-v2): remove this adapter after the legacy checkout flow is deleted.
function buildLegacyCheckoutVersion() {
  return null;
}
```

Bad:

```js
// TODO: clean this up later
function buildCheckoutVersion() {
  return null;
}
```

Contrast: the good TODO states the trigger and scope for removal. The bad TODO gives no
owner, reason, or condition for action.

### 6. Document public contracts, not private obviousness.

Why: comments are more valuable at boundaries where callers cannot inspect every
implementation detail. Public APIs, generated docs, legal headers, and externally consumed
contracts can justify comments. Private code should usually rely on clear names and small
functions instead.

Good:

```js
/**
 * Returns orders visible to the caller.
 *
 * Excludes soft-deleted orders and orders outside the caller's tenant.
 */
export function listVisibleOrders(caller) {
  // ...
}
```

Bad:

```js
/**
 * Gets the user.
 *
 * @param id The id.
 * @returns The user.
 */
function getUser(id) {
  // ...
}
```

Contrast: the good public comment describes contract details that callers must know. The
bad comment is formal noise that repeats the function name and parameter names.

## Working takeaway

This chapter is best understood as a warning about comment trust.

The root idea is:

- make the code carry meaning first; no comment is the default best outcome

The derived principles are:

- use comments for rationale, constraints, warnings, and public contracts
- keep comments close to the code they explain
- remove stale history, bylines, and commented-out code
- make TODOs specific and temporary
- avoid comments that only restate names or obvious behavior

For the agentic era, the durable insight is that comments are part of the context agents
consume. A precise comment can guide a safe edit; a stale or redundant comment can
confidently guide the wrong edit.

## Adapted takeaway

My stricter takeaway is stronger than the book's allowance for "good comments":

- no comment is the default best outcome
- comments are a second source of truth and carry hidden maintenance burden
- subjective reasons like "this is non-obvious" are not enough to justify a comment
- historical rationale can become stale authority and mislead both humans and agents
- interface comments are not needed by default because agents can inspect types,
  implementation, tests, call sites, and surrounding context
- usage examples should live in tests, behavior should live in code, temporary work should
  live in issue tracking, and design rationale should live in external design docs when it
  must be preserved
- source comments should be tolerated only when required by external constraints or
  tooling, such as legal headers or generated-file warnings

The practical rule is:

```text
Do not write comments by default.
If the meaning can be carried by code, names, types, tests, assertions, or docs outside the
source file, use those instead.
Only tolerate source comments when an external requirement or tool requires them.
```
