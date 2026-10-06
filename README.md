# 🛡️ DPX-Odin: Architectural Analyzer & Pattern Radar for Odin

> **Automated architectural auditing, code health verification, and design pattern detection for the Odin programming language.**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![Odin](https://img.shields.io/badge/Odin-Systems%20Lang-1e66f5.svg?style=flat)](https://odin-lang.org/)
[![Architecture](https://img.shields.io/badge/Design-Hexagonal%20%2B%20DDD-brightgreen.svg?style=flat)]()
[![Rules](https://img.shields.io/badge/Detection%20Rules-39%20Built--in-orange.svg?style=flat)]()
[![Tests](https://img.shields.io/badge/Tests-59%20passed%20(100%25)-success.svg?style=flat)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](LICENSE)

---

## 🎯 Why DPX-Odin?

Odin is a modern, data-oriented systems programming language designed for high performance, control, and joy. Because Odin intentionally omits traditional OOP classes and inheritance hierarchies, developers structure complex systems using:

- **Structs with procedure pointers** (vtable interfaces)
- **Subtyping via composition** (`using base: ...`)
- **Tagged unions and pattern matching** (`union`, `switch in`)
- **Custom memory allocators** (`allocator: mem.Allocator`)
- **First-class language idioms** (`bit_set`, `defer`, `proc{...}`, result tuples)

As Odin projects grow from single-file experiments into large-scale game engines, compilers, servers, and graphical applications, teams inevitably encounter **architectural debt**:

- 🚨 **God Structs:** Massive structs accumulating dozens of procedures spanning OS glue, memory allocation, network I/O, and business logic.
- 🚨 **Hidden Tight Coupling:** Package cycles, leaky abstractions, and "train-wreck" procedure chains that make refactoring dangerous.
- 🚨 **Fragile Dispatch:** Brittle cascaded `switch` statements that break silently when new variants are added.
- 🚨 **Missed Zero-Cost Idioms:** Re-implementing C-style raw integer bitmasks, manual error propagation, or missing `defer` cleanup scopes.

**DPX-Odin solves this problem.** It inspects your entire Odin codebase, maps out its architectural relationships, detects intentional patterns, flags design principle violations, and produces actionable evidence trails with zero guesswork.

---

## 💡 Practical Benefits

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   CORE VALUE PILLARS                                   │
├──────────────────────┬──────────────────────┬───────────────────┬──────────────────────┤
│  🔍 Architecture     │  🩺 Code Health &    │  🦀 Odin Idioms   │  🤖 LLM-Assisted     │
│     Discovery        │     Debt Prevention  │     Verification  │     Refactoring      │
├──────────────────────┼──────────────────────┼───────────────────┼──────────────────────┤
│ Uncover intentional  │ Identify God Structs,│ Validate safe     │ Export structured    │
│ patterns (Command,   │ cyclomatic monsters, │ bit_set flags,    │ architectural context│
│ Strategy, Facade,    │ circular imports, and│ defer guards, and │ directly to Claude,  │
│ Observer, State) in  │ tight coupling before│ allocator injection│ GPT, or Gemini for  │
│ idiomatic Odin code. │ code becomes rigid.  │ idioms.           │ guided refactoring.  │
└──────────────────────┴──────────────────────┴───────────────────┴──────────────────────┘
```

### 1. Reverse-Engineer Project Architecture in Seconds
Understand how an unfamiliar Odin codebase is put together. DPX-Odin discovers:
- Which subsystems are decoupled behind **Façades** or **Adapters**.
- Where state machines, command pipelines, and strategy dispatches are concentrated.
- How cross-file packages communicate and exchange dependencies.

### 2. Prevent Architectural Erosion in CI/CD
Catch architectural drift before code reaches production:
- Enforce the **Single Responsibility Principle** to keep core structs focused.
- Detect **Cyclic Package Dependencies** that kill modularity and parallel compilation.
- Enforce **Dependency Inversion** by requiring explicit allocator parameters rather than hardcoded global allocators.

### 3. Supercharge AI Coding Assistants (LLM Refactoring)
LLMs hallucinate when asked to refactor code without architectural context. DPX-Odin includes a **"Copy for LLM"** engine:
- Summarizes the structural findings, evidence trails, and file locations in clean, token-efficient Markdown.
- Feed the report directly into Claude, ChatGPT, or Gemini with prompts like: *"Refactor the identified KISS violation in `window_manager.odin` using the existing strategy pattern."*

### 4. Interactive Visual Dashboards
Export your codebase analysis into a standalone, presentation-ready HTML dashboard complete with:
- Live search by pattern, category, and source file.
- Detailed Evidence Trail cards explaining **why** a pattern or violation was flagged.
- Bayesian confidence breakdown (`VERY_HIGH`, `HIGH`, `MEDIUM`, `LOW`).

---

## 🚀 Quick Start

### Installation

Requires Python 3.11+. We recommend [`uv`](https://github.com/astral-sh/uv) for fast, zero-configuration execution:

```bash
# Clone the repository
git clone https://github.com/bivex/DPX-Odin.git
cd DPX-Odin

# Sync environment
uv sync
```

### Basic Audits

Analyze any Odin repository or folder with the `dpx` CLI:

```bash
# 1. Run a quick terminal scan
uv run dpx scan path/to/odin-project

# 2. Generate the full report bundle (HTML Dashboard + Markdown + JSON)
uv run dpx scan path/to/odin-project \
  --html reports/dashboard.html \
  --markdown reports/summary.md \
  --json reports/report.json

# 3. Open the visual dashboard in your browser
open reports/dashboard.html
```

### Targeted Filtering

```bash
# Filter by pattern name
uv run dpx scan path/to/odin-project --pattern command

# Only show high-confidence detections (confidence >= 80%)
uv run dpx scan path/to/odin-project --min-confidence 0.80

# List all 39 supported architectural rules
uv run dpx rules
```

---

## 🔎 Real-World Output Example

When running on an Odin codebase (such as a network library or game engine), DPX-Odin produces an explicit, evidence-backed breakdown:

```text
#1 COMMAND on command_protocol 'Operation'
├── 📍 Location: /odin-http/old_nbio/nbio.odin:723:1-736:2
├── 🎯 Confidence: 99% [VERY_HIGH]
├── 📝 Summary: Command pattern: protocol 'Operation' implemented by 11 command records
└── 🔎 Evidence Trail (11 heuristics):
    ├── +50% (COMMAND_COMMAND_PROTOCOL) Protocol 'Operation' defines Command interface
    ├── +30% (COMMAND_COMMAND_RECORD) Record 'Op_Accept' encapsulates executable command parameters
    ├── +30% (COMMAND_COMMAND_RECORD) Record 'Op_Connect' encapsulates executable command parameters
    ├── +30% (COMMAND_COMMAND_RECORD) Record 'Op_Close' encapsulates executable command parameters
    └── ... and 8 more command records

#2 TYPE_SAFE_BITMASK on bit_set_definition 'IORing_Poll_Flags'
├── 📍 Location: /odin-http/old_nbio/_io_uring/sys.odin:247:1-247:52
├── 🎯 Confidence: 85% [VERY_HIGH]
├── 📝 Summary: Type-Safe Bitmask: 'IORing_Poll_Flags' encapsulates bit flags in type-checked bit_set[IORing_Poll_Bits;u32]
└── 🔎 Evidence Trail (2 heuristics):
    ├── +70% (TYPE_SAFE_BITMASK_BIT_SET_TYPE_DECLARATION) Type is declared as bit_set enum
    └── +25% (TYPE_SAFE_BITMASK_BIT_SET_TYPE_SAFETY) Replaces raw integer flag shifting

#3 KISS on kiss_cyclomatic_complexity 'window_event_dispatcher'
├── 📍 Location: /engine/window_events.odin:112:1-260:2
├── 🎯 Confidence: 88% [VERY_HIGH]
├── 📝 Summary: KISS Violation (High Complexity): Method has 24 control flow branches
└── 🔎 Evidence Trail (2 heuristics):
    ├── +70% (KISS_KISS_HIGH_CYCLOMATIC_COMPLEXITY) High branch complexity (24 points)
    └── +35% (KISS_KISS_DECOMPOSITION_NEEDED) Needs decomposition into sub-handlers
```

---

## 📐 Catalog of 39 Built-in Checks

DPX-Odin audits your code across four distinct architectural dimensions:

### 1. Odin Systems Idioms (4 Rules)
*Validate that your team leverages Odin's native, zero-cost language mechanisms:*

| Rule | Category | What It Verifies |
|---|:---:|---|
| **Type-Safe Bitmask** | Idiom | Flags raw integer bit shifting (`1 << 3`, `&`, `\|`) and praises idiomatic `bit_set[Enum]` types that guarantee compile-time safety. |
| **Scope Guard (`defer`)** | Idiom | Identifies scoped cleanup blocks (`defer cleanup()`, `defer { ... }`) ensuring deterministic resource and memory releases. |
| **Result Tuple / Error Signaling** | Idiom | Validates explicit multiple-return error signatures `proc(...) -> (T, bool)` and `#optional_ok` directives for zero-cost error propagation without exceptions. |
| **Procedure Overloading (`proc{}`)** | Idiom | Identifies compile-time procedure groups `proc{fn_int, fn_str}` providing zero-overhead ad-hoc polymorphic dispatch without vtable indirection. |

### 2. SOLID & Clean Code Principles (10 Rules)
*Identify technical debt, untestable modules, and maintainability bottlenecks:*

| Principle | Category | What It Flags & Enforces |
|---|:---:|---|
| **Single Responsibility (SRP)** | Principle | Detects "God Structs" that combine database persistence, network protocols, and core domain logic in a single record. |
| **Open/Closed (OCP)** | Principle | Identifies brittle, cascading type switches that require modifications across multiple files whenever a new variant is introduced. |
| **Liskov Substitution (LSP)** | Principle | Detects subtyping structs that panic or stub out operations expected by consumers of the base struct. |
| **Interface Segregation (ISP)** | Principle | Flags bloated vtables (>8 procedure pointers) in favor of focused, cohesive role interfaces. |
| **Dependency Inversion (DIP)** | Principle | Verifies that procedures accept explicit `allocator: mem.Allocator` parameters or procedure pointers instead of relying on global state. |
| **Composition Over Inheritance** | Principle | Flags excessive embedding chains (`using base: ...` depth $\ge$ 3) that create fragile hierarchies. |
| **Law of Demeter (LoD)** | Principle | Detects tight-coupling chained method calls (`a.get_b().get_c().run()`) across module boundaries. |
| **High Cohesion & Low Coupling** | Principle | Measures efferent package fan-out to detect overly coupled modules. |
| **Keep It Simple, Stupid (KISS)** | Principle | Detects procedures with dangerous cyclomatic complexity ($\ge$ 10 branches) or parameter bloat ($\ge$ 6 parameters). |
| **Don't Repeat Yourself (DRY)** | Principle | Flags non-trivial duplicate logic and identical procedure implementations across files. |

### 3. Gang of Four (GoF) Patterns (23 Rules)
*Map and document intentional architectural patterns:*

| Pattern | Category | Odin Implementation Strategy |
|---|:---:|---|
| **Singleton** | Creational | Global struct pointers with dedicated accessor procedures (`get_instance`). |
| **Factory Method** | Creational | Factory constructors (`create_*`, `make_*`, `new_*`) producing initialized records. |
| **Abstract Factory** | Creational | Factory records declaring families of related product constructor pointers. |
| **Builder** | Creational | Method-chained configuration records terminating in a `.build()` procedure. |
| **Prototype** | Creational | Dedicated clone procedures (`clone :: proc(self: ^T) -> ^T`). |
| **Adapter** | Structural | Wrapper records adapting alien OS/C subsystems into uniform project interfaces. |
| **Decorator** | Structural | Structs augmenting existing vtables while conforming to the same interface contract. |
| **Facade** | Structural | High-level coordinator records and namespaces simplifying multi-subsystem workflows. |
| **Composite** | Structural | Tree structures where composite nodes manage collections of `[dynamic]^Component`. |
| **Bridge** | Structural | Structs decoupling high-level abstractions from platform drivers (`driver: ^Render_Driver`). |
| **Proxy** | Structural | Intermediary structs managing access control, lazy initialization, or caching. |
| **Flyweight** | Structural | Resource caches (`map[string]^Resource`) sharing immutable instances. |
| **Observer** | Behavioral | Listener arrays (`[dynamic]proc(...)`), event dispatchers, and subscription hooks. |
| **Strategy** | Behavioral | Swappable algorithm vtables with multiple interchangeable concrete implementations. |
| **Chain of Responsibility** | Behavioral | Request pipelines delegating to sequential `next: ^Handler` references. |
| **Template Method** | Behavioral | Algorithm skeletons invoking customizable hook procedure pointers. |
| **Command** | Behavioral | Action records or tagged unions encapsulating parameters with `execute`/`undo` methods. |
| **State** | Behavioral | State machine records transitioning between explicit state union variants. |
| **Iterator** | Behavioral | Custom traversal records exposing `has_next` and `next` procedures. |
| **Mediator** | Behavioral | Centralized message brokers and event buses decoupling peer components. |
| **Memento** | Behavioral | State capture and restore records (`save_state` / `restore_state`). |
| **Visitor** | Behavioral | Double-dispatch operations traversing heterogeneous data structures. |
| **Interpreter** | Behavioral | AST expression evaluators implementing `interpret :: proc(...)`. |

### 4. Architectural System Integrity (2 Rules)
*Enforce high-level component lifecycles and clean module boundaries:*

| Rule | Category | What It Enforces |
|---|:---:|---|
| **Lifecycle Component** | Architectural | Verifies that stateful subsystems implement deterministic `init` and `destroy`/`shutdown` procedures. |
| **Circular Dependency** | Architectural | Analyzes package import graphs to detect forbidden circular dependencies (`A -> B -> A`). |

---

## 🏛️ Engine Architecture

DPX-Odin is engineered following **Hexagonal Architecture (Ports & Adapters)** and **Domain-Driven Design (DDD)**:

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
                    │   • ANTLR4 Odin Parser Adapter (Multi-Process AST)     │
                    │   • Recursive FileSystem Source Provider               │
                    │   • Interactive HTML Dashboard Formatter & Repository  │
                    │   • GitHub-Flavored Markdown Formatter & Repository    │
                    │   • Machine-Readable JSON Result Repository            │
                    │   • Rich Console Terminal Formatter                    │
                    └────────────────────────────────────────────────────────┘
```

The domain core has **zero dependencies** on ANTLR, grammar tokens, file paths, or CLI libraries. It operates entirely on an agnostic, immutable `CodeModel` consisting of protocols, records, procedure signatures, and dependencies.

---

## 🧪 Quality & Test Suite

The engine is built with strict typing and 100% automated test coverage across all rules, parser edge-cases, and false-positive guards:

```bash
# Run full test suite (59 tests)
uv run pytest -v

# Run linter
uv run ruff check .

# Run static type checking
uv run mypy src/pattern_detector tests/
```

- **Test Suite:** `59 / 59 PASSED` (100% pass rate).
- **Linter:** `ruff` (0 errors).
- **Static Typing:** strict `mypy` compliant (0 errors across 80 source files).

---

## 🌐 The DPX Static Analysis Family

DPX-Odin is part of the **DPX Static Analysis Family** covering 34 programming languages:

| Ecosystem | Languages |
|---|---|
| **Systems & Native** | [Odin](https://github.com/bivex/DPX-Odin) • [Rust](https://github.com/bivex/DPX-Rust) • [Zig](https://github.com/bivex/DPX-Zig) • [C](https://github.com/bivex/DPX-C) • [C++](https://github.com/bivex/DPX-Cpp) • [Ada](https://github.com/bivex/DPX-Ada) • [Mojo](https://github.com/bivex/DPX-Mojo) |
| **Backend & Enterprise** | [Go](https://github.com/bivex/DPX-Go) • [Java](https://github.com/bivex/DPX-Java) • [C#](https://github.com/bivex/DPX-CSharp) • [Python](https://github.com/bivex/DPX-Py) • [TypeScript](https://github.com/bivex/DPX-TypeScript) • [PHP](https://github.com/bivex/DPX-Php) • [Ruby](https://github.com/bivex/DPX-Ruby) |
| **Mobile & Functional** | [Swift](https://github.com/bivex/DPX-Swift) • [Kotlin](https://github.com/bivex/DPX-Kotlin) • [Dart](https://github.com/bivex/DPX-Dart) • [Elixir](https://github.com/bivex/DPX-Elixir) • [Erlang](https://github.com/bivex/DPX-Erlang) • [Haskell](https://github.com/bivex/DPX-Haskell) • [Clojure](https://github.com/bivex/DPX) • [OCaml](https://github.com/bivex/DPX-OCaml) • [Gleam](https://github.com/bivex/DPX-Gleam) |
| **Web3 & Domain-Specific** | [Solidity](https://github.com/bivex/DPX-Solidity) • [Cairo](https://github.com/bivex/DPX-Cairo) • [Move](https://github.com/bivex/DPX-Move) • [Yul](https://github.com/bivex/DPX-Yul) • [Huff](https://github.com/bivex/DPX-Huff) • [SQL](https://github.com/bivex/DPX-SQL) • [Prolog](https://github.com/bivex/DPX-Prolog) |

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.
