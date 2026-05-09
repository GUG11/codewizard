# Formatting

Status: learning note, not repository policy.

Source: Robert C. Martin, *Clean Code*, Chapter 5, adapted for the agentic era.

## Top principle

Formatting is communication. Good formatting makes the structure of the code visible
before the reader understands every detail: boundaries, hierarchy, related concepts, and
flow should be visible at a glance.

In the agentic era, formatting also affects retrieval and review. Agents and humans both
reason better when nearby code is actually related, indentation reflects scope, and diffs are
not polluted by personal formatting choices.

## Principles

### 1. Separate different concepts with vertical space.

Why: blank lines are visual boundaries. They tell the reader where one thought ends and
the next one begins.

Good:

```js
import { compilePattern } from "./patterns";

const BOLD_TEXT_PATTERN = compilePattern("'''(.+?)'''");

export class BoldWidget {
  constructor(parent, text) {
    this.parent = parent;
    this.text = text;
  }

  render() {
    return `<b>${this.text}</b>`;
  }
}
```

Bad:

```js
import { compilePattern } from "./patterns";
const BOLD_TEXT_PATTERN = compilePattern("'''(.+?)'''");
export class BoldWidget {
  constructor(parent, text) {
    this.parent = parent;
    this.text = text;
  }
  render() {
    return `<b>${this.text}</b>`;
  }
}
```

Contrast: the good version separates import, constant, constructor, and rendering as
distinct concepts. The bad version compresses separate thoughts into one visual block.

### 2. Keep closely related code close together.

Why: related code should not force the reader to jump around. Variables should appear near
use, dependent functions should be nearby, and variations of the same operation should be
grouped together.

Good:

```js
function renderInvoice(invoice) {
  const subtotal = calculateSubtotal(invoice.items);
  const tax = calculateTax(subtotal, invoice.address);

  return formatInvoiceTotal(subtotal + tax);
}

function calculateSubtotal(items) {
  return items.reduce((total, item) => total + item.priceCents, 0);
}

function calculateTax(subtotal, address) {
  return taxTable.rateFor(address) * subtotal;
}
```

Bad:

```js
function calculateTax(subtotal, address) {
  return taxTable.rateFor(address) * subtotal;
}

function renderInvoice(invoice) {
  const subtotal = calculateSubtotal(invoice.items);
  const tax = calculateTax(subtotal, invoice.address);

  return formatInvoiceTotal(subtotal + tax);
}

function unrelatedCacheWarmup() {
  cache.warm("invoice");
}

function calculateSubtotal(items) {
  return items.reduce((total, item) => total + item.priceCents, 0);
}
```

Contrast: the good version keeps the caller and its helpers together. The bad version
separates related helpers with unrelated code, forcing the reader to search.

### 3. Order code from high-level story to lower-level detail.

Why: source files should read like a newspaper article: start with the headline and summary,
then descend into details. The reader should be able to skim the top of a file and understand
the main story before reading implementation details.

Good:

```js
export function makePageResponse(request) {
  const page = loadRequestedPage(request);

  if (!page) {
    return notFoundResponse(request);
  }

  return renderPageResponse(page);
}

function loadRequestedPage(request) {
  return pageStore.findByName(request.pageName || "FrontPage");
}

function renderPageResponse(page) {
  return new HtmlResponse(page.renderHtml());
}
```

Bad:

```js
function renderPageResponse(page) {
  return new HtmlResponse(page.renderHtml());
}

function loadRequestedPage(request) {
  return pageStore.findByName(request.pageName || "FrontPage");
}

export function makePageResponse(request) {
  const page = loadRequestedPage(request);

  if (!page) {
    return notFoundResponse(request);
  }

  return renderPageResponse(page);
}
```

Contrast: the good version starts with the public story and then reveals supporting
details. The bad version makes the reader assemble the story from helpers before seeing the
entry point.

### 4. Use horizontal space to reveal structure, not decorate it.

Why: horizontal spacing should help the reader see association and separation. It should
not create decorative alignment that hides the real shape of the code.

Good:

```js
const determinant = b * b - 4 * a * c;
const root = (-b + Math.sqrt(determinant)) / (2 * a);

const socket = connection.socket;
const request = parseRequest(socket);
const response = handleRequest(request);
```

Bad:

```js
const determinant=b*b-4*a*c;
const root=(-b+Math.sqrt(determinant))/(2*a);

const socket   = connection.socket;
const request  = parseRequest(socket);
const response = handleRequest(request);
```

Contrast: the good version uses spacing to separate meaningful parts of expressions. The
bad version either removes useful space or aligns columns decoratively, which makes future
edits noisy.

### 5. Preserve indentation so scope is visible.

Why: indentation is the visual map of scope. Collapsing scopes into one line saves vertical
space but makes structure harder to scan.

Good:

```js
class CommentWidget extends TextWidget {
  constructor(parent, text) {
    super(parent, text);
  }

  render() {
    return "";
  }
}
```

Bad:

```js
class CommentWidget extends TextWidget {
  constructor(parent, text) { super(parent, text); }
  render() { return ""; }
}
```

Contrast: the good version makes class, method, and method body scopes visible. The bad
version compresses scopes and makes every future change more likely to become noisy.

### 6. Let team tooling own formatting.

Why: formatting should not be a personal negotiation in every file. A shared formatter
keeps diffs small and makes the codebase feel like one system instead of a collage of
individual preferences.

Good:

```json
{
  "printWidth": 100,
  "singleQuote": false,
  "trailingComma": "all"
}
```

Bad:

```js
// File A
const user={id:1,name:"Ada"};

// File B
const user = {
    id: 1,
    name: "Ada"
};
```

Contrast: the good version makes style a shared tool-enforced decision. The bad version
lets formatting drift by file or author, creating unnecessary diff and review noise.

## Working takeaway

My takeaway is that this chapter is low importance in the agentic era.

The original point is valid:

- formatting should make code structure visible before details are fully understood

But most of this should no longer be a human reasoning burden. Formatting should be
delegated to shared tools such as formatters, linters, and editor settings. Humans and
agents should not spend much judgment on manual spacing, alignment, or layout
preferences.

The useful remainder is narrow:

- make formatting a team/tool rule, not a personal style debate
- avoid layout choices that hide structure or create noisy diffs

Compared with naming, functions, and comments, this chapter has much less leverage.
