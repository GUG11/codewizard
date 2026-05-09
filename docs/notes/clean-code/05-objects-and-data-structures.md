# Objects and Data Structures

Status: learning note, not repository policy.

Source: Robert C. Martin, *Clean Code*, Chapter 6, adapted for the agentic era.

## Top principle

Choose whether a type is an object or a data structure, and make that choice clear.
Objects hide data behind behavior. Data structures expose data and keep behavior outside.
The worst design is a hybrid that exposes internal data while pretending to protect it.

In the agentic era, this matters because agents often generate shallow getters, setters,
DTOs, and service functions quickly. If the codebase does not make the object/data
boundary explicit, agents can easily spread feature envy, mutation, and hybrid designs.

## Principles

### 1. Choose one shape: object or data structure.

Why: objects and data structures optimize for different kinds of change. An object owns
behavior and protects its data. A data structure carries data across a boundary and does not
pretend to own domain behavior.

Good:

```ts
class Cart {
  private items: CartItem[] = [];

  addItem(product: Product, quantity: number) {
    this.items.push(new CartItem(product, quantity));
  }

  totalCents() {
    return this.items.reduce((total, item) => total + item.totalCents(), 0);
  }
}

type CartRow = {
  cartId: string;
  productId: string;
  quantity: number;
};
```

Bad:

```ts
class Cart {
  private items: CartItem[] = [];

  getItems() {
    return this.items;
  }

  setItems(items: CartItem[]) {
    this.items = items;
  }

  totalCents() {
    return this.items.reduce((total, item) => total + item.totalCents(), 0);
  }
}

function removeOutOfStockItems(cart: Cart) {
  cart.setItems(cart.getItems().filter(item => item.isInStock()));
}
```

Contrast: the good version uses a clear object for cart behavior and a clear row type for
transport data. The bad version is a hybrid: it has behavior, but it also exposes mutable
internals through getters and setters.

### 2. Expose object meaning, not object representation.

Why: getters and setters do not automatically create encapsulation. If callers have to know
which fields combine into a concept, the object has leaked its representation.

Good:

```ts
class FuelTank {
  constructor(
    private capacityLiters: number,
    private remainingLiters: number,
  ) {}

  percentRemaining() {
    return this.remainingLiters / this.capacityLiters;
  }
}

if (tank.percentRemaining() < 0.1) {
  scheduleRefuel();
}
```

Bad:

```ts
class FuelTank {
  constructor(
    private capacityLiters: number,
    private remainingLiters: number,
  ) {}

  getCapacityLiters() {
    return this.capacityLiters;
  }

  getRemainingLiters() {
    return this.remainingLiters;
  }
}

if (tank.getRemainingLiters() / tank.getCapacityLiters() < 0.1) {
  scheduleRefuel();
}
```

Contrast: the good version exposes the domain meaning callers need. The bad version
forces callers to reconstruct that meaning from internal representation.

### 3. Choose the structure based on the direction of change.

Why: object-oriented code makes it easier to add new data variants without changing
existing operations. Procedural code over data structures makes it easier to add new
operations without changing existing data shapes. Neither is universally superior.

Good:

```ts
interface Shape {
  area(): number;
}

class Circle implements Shape {
  constructor(private radius: number) {}

  area() {
    return Math.PI * this.radius * this.radius;
  }
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}

  area() {
    return this.width * this.height;
  }
}
```

Bad:

```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number };

function area(shape: Shape) {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius * shape.radius;
    case "rectangle":
      return shape.width * shape.height;
  }
}

function draw(shape: Shape) {
  switch (shape.kind) {
    case "circle":
      return drawCircle(shape.radius);
    case "rectangle":
      return drawRectangle(shape.width, shape.height);
  }
}
```

Contrast: if the system expects many new shape kinds, the good version localizes each new
variant. The bad version forces every operation with a `switch` to change when a new shape
is added. If the system instead expects many new operations over stable data, the tradeoff
can reverse.

### 4. Tell objects to do work; do not navigate through their internals.

Why: call chains reveal knowledge of internal structure. If a caller has to walk through
several objects to assemble a result, the caller probably knows too much.

Good:

```ts
const stream = buildContext.createScratchFileStream(classFileName);
```

Bad:

```ts
const outputDir = buildContext.options.scratchDir.absolutePath;
const outputPath = `${outputDir}/${classFileName.replace(".", "/")}.class`;
const stream = openOutputStream(outputPath);
```

Contrast: the good version asks the context object for the operation the caller needs. The
bad version navigates through options, scratch directory, path formatting, and file creation
details outside the object that owns that knowledge.

### 5. Keep boundary data separate from domain behavior.

Why: DTOs and records are useful at boundaries such as databases, APIs, queues, and files.
They become muddy when business behavior is attached directly to those transport shapes.

Good:

```ts
type UserRow = {
  id: string;
  email: string;
  status: "active" | "disabled";
};

class User {
  constructor(
    private id: string,
    private email: string,
    private status: "active" | "disabled",
  ) {}

  canLogin() {
    return this.status === "active";
  }
}

function toUser(row: UserRow) {
  return new User(row.id, row.email, row.status);
}
```

Bad:

```ts
class UserRecord {
  id: string;
  email: string;
  status: "active" | "disabled";

  save() {
    db.users.save(this);
  }

  canLogin() {
    return this.status === "active";
  }
}
```

Contrast: the good version treats the database row as data and moves behavior into a
domain object. The bad version turns an active record into a hybrid that mixes persistence
shape and business rules.

## Working takeaway

This chapter is best understood as a warning against muddled type shapes.

The root idea is:

- choose object or data structure deliberately

The derived principles are:

- objects should expose behavior and hide representation
- data structures should carry data without pretending to own behavior
- choose the shape based on the direction of change
- avoid navigating through object internals
- keep boundary data separate from domain behavior

For the agentic era, the durable insight is that agents need explicit design boundaries.
If a codebase blurs objects, DTOs, active records, and service functions together, agents
will amplify that muddle quickly.
