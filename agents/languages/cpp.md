# C++ Guide

## Priorities

- Optimize for safety first: avoid crashes, leaks, use-after-free, data races, and undefined behavior.
- Optimize for performance second: keep the fast path lean, memory access cache-friendly, and parallel work scalable across CPU cores.
- Follow the project's existing C++ standard, toolchain, exception model, allocator choices, and concurrency primitives when they are already established.

## Ownership and Lifetimes

- Prefer stack allocation by default. If heap allocation is required, bind ownership to RAII immediately.
- Prefer `std::unique_ptr` for sole ownership. Use `std::shared_ptr` only for real shared lifetime, not as a convenience default.
- Avoid raw `new` and `delete` in normal code. Use `std::make_unique` and `std::make_shared` when ownership is needed.
- Use references for required non-null inputs. Use pointers for nullable or reseatable non-owning inputs.
- Keep ownership explicit in APIs. Do not hide lifetime transfer in raw pointers, implicit conventions, or side effects.
- Manage files, sockets, locks, threads, and other resources with types whose destructors perform cleanup.
- Do not return or store pointers, references, iterators, or views that may outlive the object they refer to.

## Interfaces and Types

- Make ownership, mutation, and thread-safety expectations obvious in function signatures.
- Prefer value types for small self-contained data. Pass large objects by `const&`, and move only when transferring ownership.
- Prefer non-owning views such as `std::string_view` or `std::span` when the project standard supports them and the source lifetime is clear.
- Use `const` aggressively to narrow mutation and make aliasing easier to reason about.
- Prefer constructors and small helper types that enforce invariants up front over objects that can drift through invalid intermediate states.
- Prefer composition over inheritance. Use virtual dispatch only when runtime polymorphism is actually required.
- Avoid flag-heavy APIs when an enum, strong type, or small parameter object would make valid states and intent clearer.

## Safety and Correctness

- Eliminate undefined behavior first, especially around bounds, lifetimes, null handling, integer overflow, aliasing, and concurrent access.
- Initialize objects immediately and keep them valid for their full lifetime.
- Prefer standard containers and algorithms over manual memory management or pointer arithmetic when they provide equivalent control.
- Validate preconditions at boundaries where invalid input can enter the system. Fail early rather than letting corrupted state spread.
- Keep error handling consistent with the project. Handle errors where the code can recover, translate the failure, or add useful context.
- Do not use `shared_ptr`, exceptions, atomics, or locks as substitutes for clear ownership and control flow.
- Treat data races as correctness bugs. Shared mutable state must have one explicit synchronization strategy.

## Headers and Build Hygiene

- Keep headers lean. Include only what declarations need, and avoid pulling implementation-heavy dependencies into widely used headers.
- Prefer forward declarations when they reduce coupling without obscuring ownership or correctness.
- Keep macros rare and localized. Prefer typed constants, enums, templates, and inline functions.
- Separate stable interfaces from volatile implementation details to reduce rebuild cost and accidental coupling.
- Avoid exposing expensive implementation choices in headers unless templates, `constexpr`, or inlining genuinely require it.

## Performance and Concurrency

- Avoid unnecessary allocations, copies, reference counting, and virtual indirection on hot paths.
- Prefer contiguous storage and simple layouts for cache locality. Reach for `std::vector` and `std::array` before node-based containers unless the access pattern justifies otherwise.
- Reserve capacity when sizes are known or can be estimated.
- Use `noexcept` when it is correct and materially improves API guarantees, move behavior, or optimization opportunities.
- Measure before tuning. Base performance work on profiling or workload evidence, not guesswork.
- Parallelize only work that is independent and large enough to amortize scheduling and synchronization costs.
- Minimize lock scope, contention, oversubscription, false sharing, and cross-thread coordination overhead.
- Prefer task or data parallelism over ad hoc thread creation when the project already provides an execution model.

## Maintainability

- Keep control flow straightforward. Do not trade readability for clever abstractions, dense templates, or speculative micro-optimizations.
- Favor small focused functions, explicit names, and predictable ownership over magic or hidden side effects.
- Comments should explain non-obvious lifetime constraints, invariants, or measured performance assumptions, not restate the code.
