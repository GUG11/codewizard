# Functions

Status: learning note, not repository policy.

Source: Robert C. Martin, *Clean Code*, Chapter 3, adapted for the agentic era.

## Top principle

A good function tells one local story clearly. It should have one purpose, stay at one
level of abstraction, be easy to call, and avoid hidden surprises.

In the agentic era, this matters because functions are not just read by humans. They are
also the units that AI tools search, rewrite, review, and compose.

## Principles

### 1. Make each function tell one local story.

Why: a function should decompose one idea into the next level of steps. If the function
bundles unrelated jobs, the reader cannot tell what story the function is responsible for.

Good:

```js
function submitOrder(order) {
  validateOrder(order);
  collectPayment(order);
  createShipment(order);
  sendOrderConfirmation(order);
}
```

Bad:

```js
function submitOrder(order) {
  validateOrder(order);
  collectPayment(order);
  createShipment(order);
  sendOrderConfirmation(order);
  syncMarketingProfile(order.customer);
  rebuildRecommendations(order.customer);
  warmRecommendationCache(order.customer);
}
```

Contrast: the good version tells one local story at the order-submission level. The bad
version stays at a high level but crosses into marketing and recommendation work, so it
bundles multiple local stories into one function.

### 2. Keep one level of abstraction inside the function.

Why: a function becomes hard to follow when high-level intent and low-level mechanics
appear in the same paragraph. The reader should be able to stay at one conceptual altitude
at a time.

Good:

```js
function renderPage(page) {
  includeSetupPages(page);
  includePageContent(page);
  includeTeardownPages(page);

  return page.getHtml();
}
```

Bad:

```js
function renderPage(page) {
  includeSetupPages(page);
  page.content.append(page.body);
  includeTeardownPages(page);

  return page.getHtml();
}
```

Contrast: the good version names each step at the same rendering level. The bad version
drops into content-buffer mechanics in the middle of otherwise high-level steps.

### 3. Make the function easy to call correctly.

Why: a function's story begins at the call site. Too many arguments, boolean flags, output
arguments, or loose parameter groups force the caller to decode implementation details
instead of reading intent.

Good:

```js
renderForSuite(pageData);
```

Bad:

```js
render(pageData, true, new Buffer(), pageData.getWikiPage().getPageCrawler());
```

Contrast: the good call exposes intent and keeps the argument count low. The bad call
mixes a boolean flag with low-level collaborators, so the caller must know too much about
the rendering implementation.

### 4. Separate asking from changing.

Why: a function should either answer a question or change state. Combining both makes
the call ambiguous and can hide unsafe side effects behind a question-shaped name.

Good:

```js
if (passwordMatches(user, password)) {
  initializeSession(user);
}
```

Bad:

```js
function checkPassword(user, password) {
  if (passwordMatches(user, password)) {
    Session.initialize(user);
    return true;
  }

  return false;
}
```

Contrast: the good version separates the query from the state change. The bad version
sounds like a pure check but also mutates session state.

### 5. Keep the happy path visible.

Why: error handling is part of the story, but it should not bury the main action. The book
prefers exceptions over returned error codes because exceptions let normal flow and error
flow separate more cleanly.

Good:

```js
function deletePage(page) {
  try {
    deletePageAndReferences(page);
  } catch (error) {
    logError(error);
  }
}

function deletePageAndReferences(page) {
  deletePageRecord(page);
  registry.deleteReference(page.name);
  configKeys.deleteKey(page.name.makeKey());
}
```

Bad:

```js
function deletePage(page) {
  if (deletePageRecord(page) === E_OK) {
    if (registry.deleteReference(page.name) === E_OK) {
      if (configKeys.deleteKey(page.name.makeKey()) === E_OK) {
        log("page deleted");
      }
    }
  }
}
```

Contrast: the good version keeps the deletion path readable and isolates error handling.
The bad version lets nested error checks dominate the structure of the function.

### 6. Extract repeated details into named concepts.

Why: duplication often means a concept has not been named yet. The duplication may be
identical text, a repeated control-flow shape, or the same policy expressed in several
places. A useful extraction gives that hidden idea one name and one implementation point.
A weak extraction only moves lines around or creates a helper whose name restates the
implementation.

Use extraction when the repeated code answers the same question, applies the same rule,
or follows the same algorithm. Do not extract merely because two or three lines look
similar. If the helper name has to describe syntax tokens instead of domain meaning, the
extraction probably has not found the real concept yet.

Good:

```js
function isEligibleForFreeShipping(order) {
  return order.totalCents >= FREE_SHIPPING_THRESHOLD_CENTS &&
    order.shippingCountry === "US" &&
    !order.hasRestrictedItems;
}

function applyShippingCharge(order) {
  if (isEligibleForFreeShipping(order)) {
    return 0;
  }

  return calculateShippingCharge(order);
}

function showFreeShippingBadge(order) {
  return isEligibleForFreeShipping(order);
}
```

Bad:

```js
function applyShippingCharge(order) {
  if (order.totalCents >= FREE_SHIPPING_THRESHOLD_CENTS &&
      order.shippingCountry === "US" &&
      !order.hasRestrictedItems) {
    return 0;
  }

  return calculateShippingCharge(order);
}

function showFreeShippingBadge(order) {
  return order.totalCents >= FREE_SHIPPING_THRESHOLD_CENTS &&
    order.shippingCountry === "US" &&
    !order.hasRestrictedItems;
}
```

Contrast: the good version names the repeated free-shipping policy once and keeps each
caller simple. The bad version repeats the same policy in multiple places, so future rule
changes can easily drift.

## Working takeaway

This chapter is best understood as a hierarchy, not a flat list.

The root idea is:

- make each function tell one local story clearly

The derived principles are:

- keep one level of abstraction inside the function
- make the function easy to call correctly
- separate asking from changing
- keep the happy path visible
- extract repeated details into named concepts

For the agentic era, the durable insight is that functions are not just execution units.
They are also editing, search, and review units. The clearer the story each function tells,
the safer it is for both humans and AI to work on it.
