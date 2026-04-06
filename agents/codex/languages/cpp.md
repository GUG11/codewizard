# C++ Guide

- Write modern, safe, and effective C++. Effective means human-readable and measurable.

## Modern
- Prefer RAII, value semantics, and rule-of-zero design.
- Prefer stack allocation and standard library types and algorithms when they fit the problem.
- Use `std::unique_ptr` for exclusive ownership and `std::shared_ptr` only when shared lifetime is truly required.
- Avoid raw `new` and `delete` in application logic.
- Keep classes small and focused. Prefer free functions or small helpers when behavior does not need object state.

## Safe
- Make ownership, lifetime, nullability, and mutation obvious at interface boundaries.
- Prefer `const` correctness, references for required parameters, and `nullptr` over `NULL`.
- Prefer constructors and types that establish valid state and make misuse hard.
- Use `std::string_view`, references, and other non-owning views only when the referenced lifetime is clearly safe.
- Keep error-handling strategy consistent with the surrounding codebase.

## Effective
- Prefer clear control flow and data flow over clever abstractions or surprising language tricks.
- Avoid hidden work in constructors, destructors, overloaded operators, and implicit conversions.
- Write code with a measurable cost model: avoid unnecessary allocations, indirection, and copying, but optimize only after profiling identifies a real bottleneck.
- Prefer code that is easy to profile, reason about, and improve from evidence.
- Keep headers lean and dependencies local.
