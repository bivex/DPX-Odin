# 🛡️ DPX-Odin: Pattern Scanner & Software Architecture Analyzer for Odin

> **Hexagonal Architecture (Ports & Adapters) + Domain-Driven Design (DDD)** static analysis and software design pattern detection engine for the **Odin programming language** powered by **ANTLR4** grammar parsing.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![Odin](https://img.shields.io/badge/Odin-Systems%20Lang-1e66f5.svg?style=flat)](https://odin-lang.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Hexagonal%20%2B%20DDD-brightgreen.svg?style=flat)]()
[![ANTLR](https://img.shields.io/badge/Parser-ANTLR%204.13.2-red.svg?style=flat)](https://www.antlr.org/)
[![Tests](https://img.shields.io/badge/Tests-59%20passed%20(100%25)-success.svg?style=flat)]()
[![Code Style](https://img.shields.io/badge/Linter-Ruff%20%26%20Mypy%20Strict-black.svg?style=flat)]()
[![Rules](https://img.shields.io/badge/Supported%20Rules-39%20(23%20GoF%20%2B%2010%20SOLID%20%2B%204%20Idioms%20%2B%202%20Arch)-orange.svg?style=flat)]()

---

## 🏛 Architecture Overview

The system strictly follows **Domain-Driven Design (DDD)** and **Hexagonal Architecture (Ports & Adapters)**. The domain layer has **zero knowledge** of ANTLR, grammar tokens, AST implementation details, filesystem, or CLI frameworks.

```text
                    ┌────────────────────────────────────────────────────────┐
                    │                    Driving Adapters                    │
                    │                                                        │
                    │   Typer + Rich CLI (dpx)   /       Python SDK API      │
                    └───────────────────────────┬────────────────────────────┘
                                                │
                                                ▼
                    ┌────────────────────────────────────────────────────────┐
                    │                   Application Layer                    │
                    │                                                        │
                    │     ScanningService (Pipeline Coordinator & Use Cases) │
                    └───────────────────────────┬────────────────────────────┘
                                                │
                                      ┌─────────▼─────────┐
                                      │    DOMAIN CORE    │
                                      │                   │
                                      │  CodeModel        │
                                      │  39 AnalysisRules │
                                      │  Confidence Model │
                                      │  Evidence Trail   │
                                      │  Dependency Graph │
                                      └─────────┬─────────┘
                                                │
                    ┌───────────────────────────▼────────────────────────────┐
                    │                      Ports / SPI                       │
                    │                                                        │
                    │   Inbound:  ScannerPort, DetectorPort, ScanOptions     │
                    │   Outbound: ParserPort, SourceProviderPort,            │
                    │             ResultRepositoryPort, ReportFormatterPort  │
                    └───────────────────────────┬────────────────────────────┘
                                                │
                    ┌───────────────────────────▼────────────────────────────┐
                    │                    Driven Adapters                     │
                    │                                                        │
                    │   • ANTLR4 Odin Parser (OdinLexer.g4 / OdinParser.g4)  │
                    │   • FileSystem Source Provider (.odin recursive)       │
                    │   • Interactive HTML Dashboard Formatter & Repository  │
                    │   • GitHub-Flavored Markdown Formatter & Repository    │
                    │   • JSON Result Repository                             │
                    │   • Rich Console Terminal Formatter                    │
                    └────────────────────────────────────────────────────────┘
```

---

## 📐 Supported Rules Catalog (39 Rules)

### 1. Odin & Systems Idioms (4 Rules)
| # | Idiom / Pattern | Category | Detection Strategy & Odin Idioms |
|---|---|---|---|
| 1 | **Type-Safe Bitmask** | Idiom | Detects type-safe `bit_set[Enum]` bitfields replacing fragile raw integer bitmasks (`<<`, `&`, `|`). |
| 2 | **Scope Guard (Defer)** | Idiom | Identifies scoped resource cleanup via `defer cleanup()` and block expressions `defer { ... }` ensuring deterministic lifecycle release. |
| 3 | **Result Tuple / Error Signaling** | Idiom | Detects zero-cost multiple return values `proc(...) -> (T, bool)` and explicit `#optional_ok` directives for robust error signaling without exceptions. |
| 4 | **Procedure Overloading (Group)** | Idiom | Identifies compile-time procedure groups `proc{fn_a, fn_b}` providing ad-hoc polymorphic dispatch without runtime vtable overhead. |

### 2. SOLID & Clean Code Principles (10 Rules)
| # | Principle | Category | Detection Strategy & Odin Idioms |
|---|---|---|---|
| 5 | **Single Responsibility (SRP)** | Principle | Detects God Struct anti-patterns mixing disparate concerns (>10 methods, high field counts, combining DB + HTTP + business logic). |
| 6 | **Open/Closed (OCP)** | Principle | Identifies fragile `instanceof` / `typeid` / `switch` cascades vs praises polymorphic interface extension points. |
| 7 | **Liskov Substitution (LSP)** | Principle | Detects subtyping structs breaking parent contracts (e.g. `panic("unsupported")` or `UnsupportedOperationException`). |
| 8 | **Interface Segregation (ISP)** | Principle | Flags Fat VTables/Interfaces (>8 procedure pointers) and praises fine-grained Role Interfaces (1-3 cohesive procedures). |
| 9 | **Dependency Inversion (DIP)** | Principle | Verifies procedure pointer / vtable injection and explicit allocator parameters (`allocator: mem.Allocator`) vs hardcoded low-level concrete instantiations. |
| 10 | **Composition Over Inheritance** | Principle | Flags deep struct embedding chains (`using base: ...` depth $\ge$ 3) and recommends composition. |
| 11 | **Law of Demeter (LoD)** | Principle | Detects train-wreck chained calls (`a.get_b().get_c().get_d().run()`) while ignoring string literals and fluent builders. |
| 12 | **High Cohesion & Low Coupling** | Principle | Evaluates package fan-out efferent coupling metrics to enforce modularity. |
| 13 | **Keep It Simple, Stupid (KISS)** | Principle | Detects high cyclomatic complexity and procedures with long parameter lists ($\ge$ 6 parameters). |
| 14 | **Don't Repeat Yourself (DRY)** | Principle | Detects identical and near-duplicate non-trivial procedure bodies across modules. |

### 3. Gang of Four (GoF) Patterns (23 Rules)
| # | Pattern Type | Category | Detection Strategy & Odin Idioms |
|---|---|---|---|
| 15 | **Singleton** | Creational | Global pointer/struct (`instance: ^App_Config = nil`), `get_instance` accessor procedure. |
| 16 | **Factory Method** | Creational | Factory creator procedures (`create_button`, `make_service`, `new_client`) returning initialized structs. |
| 17 | **Abstract Factory** | Creational | Factory structs (`GUI_Factory`) declaring families of product creation procedure pointers. |
| 18 | **Builder** | Creational | Builder struct with step procedures (`server_builder_with_host`) returning `^Builder` and terminal `build()`. |
| 19 | **Prototype** | Creational | Clone procedures (`clone :: proc(self: ^Prototype) -> ^Prototype`) producing duplicate variants. |
| 20 | **Adapter** | Structural | Wrapper struct holding an `adaptee` reference and exposing the target vtable/interface or glue records. |
| 21 | **Decorator** | Structural | Struct embedding or wrapping an instance of the same interface type, augmenting behavior. |
| 22 | **Facade** | Structural | Subsystem coordinator struct or package coordinating multiple subsystem dependencies (`Audio_System`, `Physics_System`). |
| 23 | **Composite** | Structural | Component vtable struct implemented by Leaf elements and Composite container structs with `[dynamic]^Component`. |
| 24 | **Bridge** | Structural | Abstraction struct holding an injected backend driver pointer (`driver: ^Database_Driver`). |
| 25 | **Proxy** | Structural | Surrogate struct controlling access / caching / logging for a target struct pointer. |
| 26 | **Flyweight** | Structural | Object pools with `cache: map[string]^Resource` sharing fine-grained immutable instances. |
| 27 | **Observer** | Behavioral | Listener/subscriber mechanisms (`listeners: [dynamic]proc(...)`), subscription calls (`subscribe`), event dispatch. |
| 28 | **Strategy** | Behavioral | Strategy vtable structs with 2+ interchangeable concrete implementations via `using base`. |
| 29 | **Chain of Responsibility** | Behavioral | Handler pipelines with `next: ^Handler` delegation (`next.handle(...)`). |
| 30 | **Template Method** | Behavioral | Algorithm skeleton procedure calling customizable procedure pointers/hooks in a struct. |
| 31 | **Command** | Behavioral | Command struct with `execute` and `undo` procedure pointers. |
| 32 | **State** | Behavioral | State machine struct holding current state procedure pointer or state union and transitioning contexts. |
| 33 | **Iterator** | Behavioral | Custom iterator struct with `has_next :: proc` and `next :: proc`. |
| 34 | **Mediator** | Behavioral | Centralized mediator / event broker struct (`Event_Broker`) decoupling components. |
| 35 | **Memento** | Behavioral | State snapshot struct (`Memento`) with `save_state` and `restore_state` procedures. |
| 36 | **Visitor** | Behavioral | Visitor struct with `visit_*` procedure pointers or type switch visitor procedures. |
| 37 | **Interpreter** | Behavioral | Expression structs/unions with `interpret :: proc(...)`. |

### 4. Architectural Rules (2 Rules)
| # | Pattern Type | Category | Detection Strategy |
|---|---|---|---|
| 38 | **Lifecycle Component** | Architectural | Deterministic component lifecycles (`start()`, `stop()`, `init()`, `destroy()`). |
| 39 | **Circular Dependency** | Architectural | Package graph analysis detecting cyclic dependencies (`package a ➔ package b ➔ package a`). |

---

## 💻 CLI Usage Guide

The tool provides the `dpx` command (along with aliases `dpx-odin` and `pattern-detector`):

```bash
# 1. Scan an Odin project directory
uv run dpx scan path/to/odin/project

# 2. Export full multi-format report (JSON + Interactive HTML + Markdown)
uv run dpx scan path/to/odin/project \
  --json reports/report.json \
  --html reports/dashboard.html \
  --markdown reports/summary.md

# 3. Open interactive color-coded HTML dashboard
open reports/dashboard.html

# 4. Filter by minimum confidence threshold or specific pattern
uv run dpx scan path/to/odin/project --min-confidence 0.70 --pattern strategy

# 5. View registered rules catalog (all 39 rules)
uv run dpx rules

# 6. View system info & active parser
uv run dpx info

# 7. Run test suite
uv run pytest -v
```

### 📊 Interactive Dashboard Features

- **Search & Filter:** Instant live filtering by pattern name, category, target element, or confidence level.
- **Evidence Trail Modal:** Inspect individual heuristics, source line references, and Bayesian confidence contributions.
- **📋 Copy for LLM:** Single-click copy of the structured Markdown report directly to clipboard, optimized as prompt context for LLMs (Claude, GPT, Gemini).
- **Dark Mode & Responsive Design:** High-contrast, presentation-ready UI.

---

## 🧪 Quality & Verification

```bash
uv run pytest --cov=pattern_detector -v
uv run ruff check .
uv run mypy src/pattern_detector tests/
```

* **Test Suite:** `59 / 59 PASSED` (100% pass rate).
* **Linter:** `ruff` (0 errors).
* **Static Typing:** strict `mypy` compliant (0 errors across 80 source files).

---

## 🌐 The DPX Multi-Language Static Analysis Family (34 Languages)

| # | Language | Repository | Ecosystem & Focus |
|:---:|---|---|---|
| 1 | **Ada** | [`bivex/DPX-Ada`](https://github.com/bivex/DPX-Ada) | Ada 2012/2022, SPARK Contracts, Ravenscar Tasking, DO-178C Safety |
| 2 | **Clojure** | [`bivex/DPX`](https://github.com/bivex/DPX) | Lisp S-Expressions, Protocols, Multimethods |
| 3 | **C** | [`bivex/DPX-C`](https://github.com/bivex/DPX-C) | Memory Safety, Struct VTables, Idiomatic C11/C23 |
| 4 | **Cairo** | [`bivex/DPX-Cairo`](https://github.com/bivex/DPX-Cairo) | Starknet Smart Contracts, ZK-Rollup Invariants |
| 5 | **C++** | [`bivex/DPX-Cpp`](https://github.com/bivex/DPX-Cpp) | RAII, CRTP, Concepts, Modern C++20/23 |
| 6 | **C#** | [`bivex/DPX-CSharp`](https://github.com/bivex/DPX-CSharp) | .NET 9, Roslyn AST, Linq, Records |
| 7 | **Dart** | [`bivex/DPX-Dart`](https://github.com/bivex/DPX-Dart) | Dart 3.x, Flutter, BLoC, Riverpod, Isolates |
| 8 | **Elixir** | [`bivex/DPX-Elixir`](https://github.com/bivex/DPX-Elixir) | BEAM OTP, GenServer, Supervisors |
| 9 | **Erlang** | [`bivex/DPX-Erlang`](https://github.com/bivex/DPX-Erlang) | Fault Tolerance, Actor Model, OTP Behaviors |
| 10 | **Gleam** | [`bivex/DPX-Gleam`](https://github.com/bivex/DPX-Gleam) | Type-Safe BEAM, Actor Concurrency |
| 11 | **Go** | [`bivex/DPX-Go`](https://github.com/bivex/DPX-Go) | Goroutines, Channels, Composition, Interfaces |
| 12 | **Haskell** | [`bivex/DPX-Haskell`](https://github.com/bivex/DPX-Haskell) | Pure Functional, Monads, Typeclasses, Arrows |
| 13 | **Huff** | [`bivex/DPX-Huff`](https://github.com/bivex/DPX-Huff) | Low-Level EVM Bytecode & Opcodes |
| 14 | **Idris 2** | [`bivex/DPX-Idris2`](https://github.com/bivex/DPX-Idris2) | Dependent Types, QTT Linear Protocols, Totality, Proofs |
| 15 | **Java** | [`bivex/DPX-Java`](https://github.com/bivex/DPX-Java) | Spring Boot, Enterprise Java, JVM Invariants |
| 16 | **Julia** | [`bivex/DPX-Julia`](https://github.com/bivex/DPX-Julia) | Multiple Dispatch, Scientific Computing |
| 17 | **Kotlin** | [`bivex/DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin) | Coroutines, Multiplatform, Functional DSLs |
| 18 | **Lua** | [`bivex/DPX-Lua`](https://github.com/bivex/DPX-Lua) | Metatables, Coroutines, LuaJIT, Neovim |
| 19 | **Mojo** | [`bivex/DPX-Mojo`](https://github.com/bivex/DPX-Mojo) | SIMD Hardware, Memory Lifetimes, AI Systems |
| 20 | **Move** | [`bivex/DPX-Move`](https://github.com/bivex/DPX-Move) | Aptos & Sui Resource Safety, Linear Types |
| 21 | **OCaml** | [`bivex/DPX-OCaml`](https://github.com/bivex/DPX-OCaml) | Algebraic Data Types, Functors, Polymorphism |
| 22 | **Odin** | [`bivex/DPX-Odin`](https://github.com/bivex/DPX-Odin) | Data-Oriented Design, Custom Allocators, VTables, Struct Subtyping |
| 23 | **PHP** | [`bivex/DPX-Php`](https://github.com/bivex/DPX-Php) | Modern PHP 8.4, Attributes, Traits, Laravel |
| 24 | **Prolog** | [`bivex/DPX-Prolog`](https://github.com/bivex/DPX-Prolog) | ISO Prolog, SWI-Prolog, DCG, CLP(FD/R/Q), CHR, Meta-Interpreters |
| 25 | **Puppet** | [`bivex/DPX-Puppet`](https://github.com/bivex/DPX-Puppet) | Puppet DSL, Roles/Profiles, IaC Security, Hiera |
| 26 | **Python** | [`bivex/DPX-Py`](https://github.com/bivex/DPX-Py) | Metaprogramming, Protocols, Hexagonal DDD |
| 27 | **Ruby** | [`bivex/DPX-Ruby`](https://github.com/bivex/DPX-Ruby) | Ruby 3.x, Rails, Metaprogramming, Dry-RB, Security |
| 28 | **Rust** | [`bivex/DPX-Rust`](https://github.com/bivex/DPX-Rust) | Zero-Cost Abstractions, Borrow Checker, Traits |
| 29 | **Solidity** | [`bivex/DPX-Solidity`](https://github.com/bivex/DPX-Solidity) | DeFi Security, Reentrancy, EVM Yul/Assembly |
| 30 | **SQL** | [`bivex/DPX-SQL`](https://github.com/bivex/DPX-SQL) | PostgreSQL, MySQL, SQLite, T-SQL, PL/SQL |
| 31 | **Swift** | [`bivex/DPX-Swift`](https://github.com/bivex/DPX-Swift) | Protocol-Oriented Programming, Actors |
| 32 | **TypeScript** | [`bivex/DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript) | Generics, Conditional Types, Clean Architecture |
| 33 | **Yul** | [`bivex/DPX-Yul`](https://github.com/bivex/DPX-Yul) | EVM Intermediate Representation Optimization |
| 34 | **Zig** | [`bivex/DPX-Zig`](https://github.com/bivex/DPX-Zig) | Comptime, Manual Memory Allocators, C ABI |

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
