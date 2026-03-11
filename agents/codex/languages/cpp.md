# C++ Style Guide

- Follow modern C++ style with RAII and deterministic ownership.
- Prefer stack allocation and `std::unique_ptr`; use `std::shared_ptr` only when shared lifetime is required.
- Prefer `const` correctness, references for non-null parameters, and `nullptr` over `NULL`.
- Favor STL containers and algorithms over manual memory management when equivalent.
- Keep headers lean and minimize unnecessary includes.
