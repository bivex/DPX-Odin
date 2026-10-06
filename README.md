<p align="center">
  <h1 align="center">🛡️ DPX-Odin</h1>
  <p align="center">
    <b>High-Performance Static Architecture Analyzer & Design Pattern Detection Engine for Odin</b>
  </p>
  <p align="center">
    <i>Powered by Hexagonal Architecture (Ports & Adapters), Domain-Driven Design (DDD), and ANTLR4 Grammar Parsing</i>
  </p>
  <p align="center">
    <a href="#-key-features">Key Features</a> •
    <a href="#-benchmarks">Benchmarks</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-interactive-dashboard">Dashboard</a> •
    <a href="#-architecture">Architecture</a> •
    <a href="#-rules-catalog">Rules Catalog</a> •
    <a href="#-dpx-family">DPX Family</a>
  </p>
  <p align="center">
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11%2B-blue.svg?style=flat&logo=python" alt="Python Version" /></a>
    <a href="https://odin-lang.org/"><img src="https://img.shields.io/badge/Odin-Systems%20Lang-1e66f5.svg?style=flat" alt="Odin Language" /></a>
    <a href="#"><img src="https://img.shields.io/badge/Architecture-Hexagonal%20%2B%20DDD-brightgreen.svg?style=flat" alt="Architecture" /></a>
    <a href="https://www.antlr.org/"><img src="https://img.shields.io/badge/Parser-ANTLR%204.13.2-red.svg?style=flat" alt="ANTLR4" /></a>
    <a href="#"><img src="https://img.shields.io/badge/Tests-59%20passed%20(100%25)-success.svg?style=flat" alt="Tests" /></a>
    <a href="#"><img src="https://img.shields.io/badge/Linter-Ruff%20%26%20Mypy%20Strict-black.svg?style=flat" alt="Code Quality" /></a>
    <a href="#"><img src="https://img.shields.io/badge/Rules-39%20(23%20GoF%20%2B%2010%20SOLID%20%2B%204%20Idioms%20%2B%202%20Arch)-orange.svg?style=flat" alt="Rules" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat" alt="License" /></a>
  </p>
</p>

---

> [!NOTE]
> **DPX-Odin** is a next-generation static analysis engine tailored specifically to the semantics, idioms, and data-oriented nature of the **Odin programming language**. It detects GoF design patterns, engineering clean code violations, and native Odin idioms (`bit_set`, `defer`, procedure overloading, result tuples) with Bayesian confidence scoring and actionable evidence trails.

---

## ⚡ Benchmarks

Thanks to multi-process parallelization (`ProcessPoolExecutor`) and content-addressed SHA-256 AST caching, DPX-Odin delivers near-instant analysis times on iterative scans:

| Project | Files | Cold Scan (No Cache) | Warm Scan (Cached) | Speedup Factor |
|:---|:---:|:---:|:---:|:---:|
| [**`laytan/odin-http`**](https://github.com/laytan/odin-http) *(HTTP 1.1 Client/Server)* | 39 | **9.0s** *(was 27.8s)* | **0.25s** | **~110x 🚀** |
| [**`karl-zylinski/karl2d`**](https://github.com/karl-zylinski/karl2d) *(2D Game Library)* | 99 | **27.6s** *(was 70.6s)* | **0.159s** | **~444x 🚀** |
| **Test Suite Execution** | 59 tests | **2.39s** *(was 3.06s)* | **0.19s** | **~16x ⚡** |

> [!TIP]
> Repeated CLI scans reuse cached AST representations automatically. Only modified `.odin` files trigger grammar parsing, making DPX-Odin blazing fast for pre-commit hooks and CI/CD pipelines.

---

## ✨ Key Features

- 🎯 **39 Comprehensive Rules:** 23 Gang of Four (GoF) patterns, 10 SOLID & Clean Code principles, 2 architectural structural checks, and 4 dedicated Odin systems idioms.
- 🦀 **Native Odin Idioms:** First-class detection for `bit_set[Enum]` type-safe bitmasks, `defer` scope guards, `proc{...}` procedure groups, and `(T, bool)` / `#optional_ok` result tuples.
- 🔬 **Bayesian Confidence & Evidence Trails:** Every detection produces a verifiable confidence score (from `0%` to `100%`) accompanied by an explicit multi-heuristic evidence trail.
- 📊 **Multi-Format Exporters:** Export results directly to interactive HTML dashboards, machine-readable JSON schemas, and GitHub-Flavored Markdown summaries.
- 📋 **Copy for LLM:** Single-click prompt export formatted specifically for Claude 3.7, GPT-4o, and Gemini 2.5 Pro code review workflows.
- 🏛️ **Pure Hexagonal Architecture:** Strict separation between driving CLI adapters, application services, domain models, and driven outbound parsers/repositories.

---

## 🚀 Quick Start

### Installation

Requires Python 3.11+. We recommend using [`uv`](https://github.com/astral-sh/uv) for zero-setup execution:

```bash
# Clone the repository
git clone https://github.com/bivex/DPX-Odin.git
cd DPX-Odin

# Sync dependencies
uv sync
```

### Running Scans

Use `dpx` (or alias `dpx-odin` / `pattern-detector`):

```bash
# 1. Quick terminal scan
uv run dpx scan path/to/odin/project

# 2. Export full multi-format bundle (JSON + Interactive HTML + Markdown)
uv run dpx scan path/to/odin/project \
  --json reports/report.json \
  --html reports/dashboard.html \
  --markdown reports/summary.md

# 3. Filter by pattern type or confidence threshold
uv run dpx scan path/to/odin/project --pattern command --min-confidence 0.80

# 4. Inspect registered rules catalog
uv run dpx rules

# 5. Display engine and parser runtime information
uv run dpx info
```

### CLI Terminal Output Preview

```text
#1 COMMAND on command_protocol 'Operation'
├── 📍 Location: /odin-http/old_nbio/nbio.odin:723:1-736:2
├── 🎯 Confidence: 99% [VERY_HIGH]
├── 📝 Summary: Command pattern: protocol 'Operation' implemented by 11 command records
└── 🔎 Evidence Trail (11 heuristics):
    ├── +50% (COMMAND_COMMAND_PROTOCOL) Protocol 'Operation' defines Command interface
    ├── +30% (COMMAND_COMMAND_RECORD) Record 'Op_Accept' encapsulates executable command
    ├── +30% (COMMAND_COMMAND_RECORD) Record 'Op_Connect' encapsulates executable command
    └── ... and 9 more command records

✔ Full JSON detection report exported to: reports/report.json
✔ Interactive HTML dashboard exported to: reports/dashboard.html
✔ Markdown report exported to: reports/summary.md
```

---

## 📊 Interactive Dashboard

Generate an interactive, production-ready dashboard using `--html reports/dashboard.html`:

- 🔍 **Live Search & Filter:** Instant real-time filtering by pattern name, category (`Creational`, `Structural`, `Behavioral`, `Principle`, `Idiom`), target element, and confidence level.
- 🧬 **Evidence Trail Inspector:** Expandable inspection cards displaying exact source locations, heuristic weights, and rule codes.
- 📋 **Copy for LLM Context:** Copies clean, token-efficient Markdown containing the entire scan summary directly to your clipboard for LLM-based refactoring sessions.
- 🌙 **High-Contrast Dark Theme:** Optimized for developer readability and screenshots.

---

## 🏛 Architecture

The engine strictly enforces **Hexagonal Architecture (Ports & Adapters)** and **Domain-Driven Design (DDD)** principles:

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

## 📐 Rules Catalog

<details open>
<summary><b>1. Odin & Systems Idioms (4 Rules)</b></summary>
<br>

| # | Idiom | Category | Detection Strategy & Odin Semantics |
|:---:|---|:---:|---|
| 1 | **Type-Safe Bitmask** | Idiom | Identifies `bit_set[Enum]` bitfields replacing error-prone integer flag arithmetic (`<<`, `&`, `|`). |
| 2 | **Scope Guard (Defer)** | Idiom | Identifies scoped cleanup expressions `defer cleanup()` and block scopes `defer { ... }` ensuring RAII-equivalent resource release. |
| 3 | **Result Tuple / Error Signaling** | Idiom | Identifies zero-cost multiple return values `proc(...) -> (T, bool)` and explicit `#optional_ok` directives. |
| 4 | **Procedure Overloading (Group)** | Idiom | Identifies compile-time procedure groups `proc{fn_a, fn_b}` providing ad-hoc dispatch without runtime vtable overhead. |

</details>

<details open>
<summary><b>2. SOLID & Clean Code Principles (10 Rules)</b></summary>
<br>

| # | Principle | Category | Detection Strategy & Odin Semantics |
|:---:|---|:---:|---|
| 5 | **Single Responsibility (SRP)** | Principle | Detects God Struct anti-patterns mixing disparate domain concerns (database persistence + HTTP handling + logic). |
| 6 | **Open/Closed (OCP)** | Principle | Identifies fragile `typeid` / `switch` cascades vs polymorphic extension points. |
| 7 | **Liskov Substitution (LSP)** | Principle | Detects subtyping structs breaking parent contracts (e.g. `panic("unsupported")`). |
| 8 | **Interface Segregation (ISP)** | Principle | Flags Fat VTables/Interfaces (>8 procedure pointers) and praises cohesive Role Interfaces (1-3 procedures). |
| 9 | **Dependency Inversion (DIP)** | Principle | Verifies procedure pointer injection and allocator parameterization (`allocator: mem.Allocator`) vs hardcoded globals. |
| 10 | **Composition Over Inheritance** | Principle | Flags deep struct embedding chains (`using base: ...` depth $\ge$ 3) and recommends explicit composition. |
| 11 | **Law of Demeter (LoD)** | Principle | Detects train-wreck chained calls (`a.get_b().get_c().run()`) while ignoring string literals and fluent builders. |
| 12 | **High Cohesion & Low Coupling** | Principle | Evaluates package fan-out efferent coupling metrics to enforce modularity. |
| 13 | **Keep It Simple, Stupid (KISS)** | Principle | Detects procedures with high cyclomatic complexity and long parameter lists ($\ge$ 6 parameters). |
| 14 | **Don't Repeat Yourself (DRY)** | Principle | Detects identical and near-duplicate non-trivial procedure bodies across modules. |

</details>

<details>
<summary><b>3. Gang of Four (GoF) Patterns (23 Rules)</b></summary>
<br>

| # | Pattern Type | Category | Detection Strategy & Odin Semantics |
|:---:|---|:---:|---|
| 15 | **Singleton** | Creational | Global pointer/struct (`instance: ^App_Config = nil`), `get_instance` accessor procedure. |
| 16 | **Factory Method** | Creational | Factory creator procedures (`create_*`, `make_*`, `new_*`) returning initialized structs. |
| 17 | **Abstract Factory** | Creational | Factory structs declaring families of product creation procedure pointers. |
| 18 | **Builder** | Creational | Step-by-step configuration struct returning `^Builder` and a terminal `.build()` operation. |
| 19 | **Prototype** | Creational | Clone procedures (`clone :: proc(self: ^Prototype) -> ^Prototype`) producing duplicate variants. |
| 20 | **Adapter** | Structural | Wrapper struct holding an `adaptee` reference and exposing a target vtable/interface or glue record. |
| 21 | **Decorator** | Structural | Struct embedding or wrapping an instance of the same interface type, augmenting behavior. |
| 22 | **Facade** | Structural | Subsystem coordinator struct or namespace coordinating multiple underlying subsystems. |
| 23 | **Composite** | Structural | Component vtable implemented by Leaf elements and Composite containers holding `[dynamic]^Component`. |
| 24 | **Bridge** | Structural | Abstraction struct holding an injected backend driver pointer (`driver: ^Database_Driver`). |
| 25 | **Proxy** | Structural | Surrogate struct controlling access, caching, or logging for a target struct pointer. |
| 26 | **Flyweight** | Structural | Object pools with `cache: map[string]^Resource` sharing fine-grained immutable instances. |
| 27 | **Observer** | Behavioral | Listener mechanisms (`listeners: [dynamic]proc(...)`), explicit subscription procedures, event dispatch. |
| 28 | **Strategy** | Behavioral | Strategy vtable structs with multiple interchangeable concrete implementations via `using base`. |
| 29 | **Chain of Responsibility** | Behavioral | Handler pipelines with `next: ^Handler` delegation. |
| 30 | **Template Method** | Behavioral | Algorithm skeleton procedure calling customizable procedure pointers/hooks in a struct. |
| 31 | **Command** | Behavioral | Command struct / union with `execute` and `undo` procedure pointers. |
| 32 | **State** | Behavioral | State machine struct holding state procedure pointers or state unions with transition contexts. |
| 33 | **Iterator** | Behavioral | Custom iterator struct with `has_next :: proc` and `next :: proc`. |
| 34 | **Mediator** | Behavioral | Centralized mediator / event broker struct decoupling multiple peers. |
| 35 | **Memento** | Behavioral | State snapshot struct (`Memento`) with `save_state` and `restore_state` procedures. |
| 36 | **Visitor** | Behavioral | Visitor struct with `visit_*` procedure pointers or type switch visitor procedures. |
| 37 | **Interpreter** | Behavioral | Expression structs/unions with `interpret :: proc(...)`. |

</details>

<details>
<summary><b>4. Architectural Rules (2 Rules)</b></summary>
<br>

| # | Pattern Type | Category | Detection Strategy |
|:---:|---|:---:|---|
| 38 | **Lifecycle Component** | Architectural | Stateful components managing deterministic lifecycles (`init`, `destroy`, `start`, `shutdown`). |
| 39 | **Circular Dependency** | Architectural | Package graph analysis detecting cyclic import dependencies (`package a ➔ package b ➔ package a`). |

</details>

---

## 🧪 Quality & Verification

Every rule, parser adapter, and exporter is covered by rigorous automated tests:

```bash
# Run unit & regression test suite
uv run pytest -v

# Run linter
uv run ruff check .

# Run static type checking
uv run mypy src/pattern_detector tests/
```

- **Test Suite:** `59 / 59 PASSED` (100% pass rate in `0.19s`).
- **Linter:** `ruff` (0 errors).
- **Static Typing:** `mypy` strict compliant (0 errors across 80 source files).

---

## 🌐 DPX Family

DPX-Odin is part of the **DPX Static Analysis Family** covering 34 programming languages:

| Language | Repository | Focus |
|---|---|---|
| **Odin** | [`bivex/DPX-Odin`](https://github.com/bivex/DPX-Odin) | Systems Architecture, Data-Oriented Design, Allocators, VTables |
| **Rust** | [`bivex/DPX-Rust`](https://github.com/bivex/DPX-Rust) | Zero-Cost Abstractions, Borrow Checker, Traits |
| **Go** | [`bivex/DPX-Go`](https://github.com/bivex/DPX-Go) | Goroutines, Channels, Composition, Interfaces |
| **Zig** | [`bivex/DPX-Zig`](https://github.com/bivex/DPX-Zig) | Comptime, Manual Memory Allocators, C ABI |
| **C++** | [`bivex/DPX-Cpp`](https://github.com/bivex/DPX-Cpp) | RAII, CRTP, Concepts, Modern C++20/23 |
| **C** | [`bivex/DPX-C`](https://github.com/bivex/DPX-C) | Memory Safety, Struct VTables, Idiomatic C11/C23 |
| **Python** | [`bivex/DPX-Py`](https://github.com/bivex/DPX-Py) | Metaprogramming, Protocols, Hexagonal DDD |
| **TypeScript** | [`bivex/DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript) | Generics, Conditional Types, Clean Architecture |
| **C#** | [`bivex/DPX-CSharp`](https://github.com/bivex/DPX-CSharp) | .NET 9, Roslyn AST, Linq, Records |
| **Java** | [`bivex/DPX-Java`](https://github.com/bivex/DPX-Java) | Enterprise Java, Spring Boot, JVM Invariants |
| **Swift** | [`bivex/DPX-Swift`](https://github.com/bivex/DPX-Swift) | Protocol-Oriented Programming, Actors |
| **Kotlin** | [`bivex/DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin) | Coroutines, Multiplatform, Functional DSLs |
| *... and 22 more* | | *Ada, Cairo, Clojure, Dart, Elixir, Erlang, Gleam, Haskell, Huff, Idris 2, Julia, Lua, Mojo, Move, OCaml, PHP, Prolog, Puppet, Ruby, Solidity, SQL, Yul* |

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.
