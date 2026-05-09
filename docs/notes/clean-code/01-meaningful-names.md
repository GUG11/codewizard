# Meaningful Names

Status: learning note, not repository policy.

Source: Robert C. Martin, *Clean Code*, Chapter 2, adapted for the agentic era.

## Top principle

A good name carries the meaning needed to use a symbol correctly, and omits facts the
language, type system, or editor already tells you. In the agentic era, this matters twice:
names guide both human reading and AI retrieval, editing, and review.

## Principles

### 1. Name by meaning, not by representation.

Why: keep semantic information; drop type, member, or interface markers that are already
visible elsewhere.

| Good | Bad | Contrast |
| --- | --- | --- |
| `userId` | `strUserId` | Semantic role vs type encoding |
| `order` | `m_order` | Domain term vs member marker |
| `UserService` | `IUserService` | Role name vs interface prefix |

### 2. Name by domain role, not by generic placeholder.

Why: generic names force the reader to inspect implementation before they can understand
intent.

| Good | Bad | Contrast |
| --- | --- | --- |
| `billingAddress` | `addressData` | Domain role vs generic container name |
| `parseRequestBody` | `handleData` | Specific action vs vague action |
| `invoiceTotalCents` | `value` | Business meaning vs placeholder |

### 3. Put important distinctions into the name.

Why: if boundary, state, lifecycle, or units change how the symbol should be used, that
distinction belongs in the name.

| Good | Bad | Contrast |
| --- | --- | --- |
| `rawPayload` | `payload` | Boundary/state distinction vs collapsed name |
| `dbUserRow` | `user` | Storage-layer distinction vs ambiguous term |
| `priceCents` | `price` | Unit-carrying name vs unitless name |

### 4. Use one stable word for one concept.

Why: stable vocabulary preserves the conceptual map of the repo and prevents semantic
drift.

| Good | Bad | Contrast |
| --- | --- | --- |
| one consistent `fetchUser` | mixed `getUser` or `loadUser` or `resolveUser` | Stable repo vocabulary vs synonym drift |
| `parseConfig` | `transformConfig` when both mean parsing | Accurate verb vs unnecessary variation |

### 5. Make names easy to recognize and verify.

Why: names should read clearly in code, logs, diffs, and search results; booleans should
read like predicates.

| Good | Bad | Contrast |
| --- | --- | --- |
| `isArchived` | `archived` | Predicate form vs unclear boolean shape |
| `hasAccess` | `accessFlag` | Readable predicate vs awkward flag name |
| `orderTotalCents` | `total` | Searchable, specific name vs vague label |

### 6. Use enough words to preserve meaning, but no more.

Why: a name should be the shortest form that still preserves the meaning needed for
correct use.

| Good | Bad | Contrast |
| --- | --- | --- |
| `retryDelayMs` | `x` | Compact meaning vs no meaning |
| `customerEmail` | `emailData` | Specific role vs loose container term |
| `submittedOrder` | `orderObjectForSubmittedCheckoutFlow` | Proportional name vs bloated prose |

## Working takeaway

This chapter is more useful when each principle keeps its good and bad examples together
instead of scattering them into separate rules. The durable takeaway is:

- preserve semantic meaning
- remove representational noise
- keep repo vocabulary stable
- make distinctions visible when they affect correctness

For future work, this note can later be distilled into repo principles or agent guidance,
but it is not yet policy.
