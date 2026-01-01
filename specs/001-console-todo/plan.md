# Implementation Plan: In-Memory Console Todo Application

**Branch**: `001-console-todo` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-console-todo/spec.md`

## Summary

Build a Phase I in-memory Python console application for CRUD todo management. The application provides an interactive CLI menu for adding, viewing, updating, deleting, and marking todos as complete. All data stored in memory using Python dictionaries—no persistence, no external dependencies beyond Python standard library. Designed to demonstrate Agentic Dev Stack workflow (spec → plan → tasks → implementation) with clean, readable code for beginner-to-intermediate Python developers.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (no external packages for core functionality)
**Storage**: In-memory only (Python dict for todo storage by ID)
**Testing**: pytest (for unit tests if requested)
**Target Platform**: Cross-platform console (Windows, macOS, Linux)
**Project Type**: Single project (simple console application)
**Performance Goals**: Instantaneous response (<100ms) for operations on up to 1000 todos
**Constraints**: No files, no databases, no web frameworks, no persistence, no external APIs
**Scale/Scope**: Single-user console app, <500 lines of code, 5 CRUD operations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase I Constraints (from Constitution)

| Constraint | Status | Notes |
|------------|--------|-------|
| Pure in-memory storage (Python dict/list) | ✅ PASS | Using Python dict to store todos by ID |
| CRUD operations: Add, View, Update, Delete, Mark Complete | ✅ PASS | All 5 operations specified in requirements |
| CLI interface only (no web, no GUI) | ✅ PASS | Console menu with text input/output |
| Python standard library + minimal dependencies | ✅ PASS | No external dependencies required for core functionality |
| **MUST NOT**: External storage (files, DBs, cache) | ✅ PASS | Explicitly excluded in spec |
| **MUST NOT**: Web frameworks or HTTP servers | ✅ PASS | Console-only application |
| **MUST NOT**: AI/ML integrations | ✅ PASS | No AI features |
| **MUST NOT**: Container orchestration | ✅ PASS | Simple Python script |
| **MUST NOT**: Cloud service dependencies | ✅ PASS | Runs locally |

### Core Principles Compliance

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Incremental Evolution | ✅ PASS | Phase I implementation only—no Phase II features |
| II. Simplicity First, Scalability Later | ✅ PASS | Simple dict storage, no ORM, no database abstraction |
| III. Clear Separation of Concerns | ✅ PASS | Business logic only—no persistence, web, or infrastructure layers |
| IV. Production-Minded Engineering | ✅ PASS | Error handling (FR-006), validation (FR-005, FR-012), clear messages (FR-007) |
| V. Readable, Modular, Well-Documented Code | ✅ PASS | Success criteria SC-007 requires clean code for beginner-intermediate developers |
| VI. Clean CLI UX | ✅ PASS | FR-001 menu, FR-006 error messages, FR-007 confirmations, FR-008 clear formatting |

**Gate Result**: ✅ **PASS** - All Phase I constraints satisfied, no violations requiring justification

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo/
├── spec.md              # Feature specification
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technical decisions)
├── data-model.md        # Phase 1 output (Todo entity definition)
├── quickstart.md        # Phase 1 output (how to run the app)
└── contracts/           # Phase 1 output (CLI command contracts)
    └── cli-interface.md # Menu options and input/output contracts
```

### Source Code (repository root)

```text
src/
├── todo_app.py          # Main entry point with CLI loop
├── todo_manager.py      # Todo business logic (add, view, update, delete, complete)
└── todo_model.py        # Todo data class definition

tests/
└── unit/
    ├── test_todo_model.py       # Tests for Todo entity
    └── test_todo_manager.py     # Tests for business logic

pyproject.toml           # UV project configuration
README.md                # Project overview and usage
```

**Structure Decision**: Single project layout (Option 1) is appropriate for a simple console application. Three modules provide clear separation:
- `todo_model.py`: Data structure (Todo class with id, description, status)
- `todo_manager.py`: Business logic (CRUD operations, validation)
- `todo_app.py`: CLI interface (menu, user input, output formatting)

This structure supports Constitution Principle V (Readable, Modular Code) while avoiding over-engineering (Principle II: Simplicity First).

## Complexity Tracking

No violations detected. The simple three-module structure with in-memory dict storage satisfies all constitution constraints without introducing unnecessary complexity.

---

# Phase 0: Research & Technical Decisions

## Research Questions

1. **Python 3.13+ Environment Setup**: How to initialize UV-based Python project?
2. **In-Memory Data Structure**: Best Python structure for storing todos (dict vs list)?
3. **CLI Menu Pattern**: Best practices for console menu loops in Python?
4. **Input Validation**: How to validate integer IDs and non-empty strings?
5. **Screen Clearing**: Cross-platform approach for clearing console (FR-011)?
6. **Status Representation**: Boolean vs string for completion status?

## Research Findings

### Decision 1: UV Project Initialization

**Decision**: Use `uv init` to create Python 3.13+ project with `pyproject.toml`

**Rationale**:
- UV is specified in spec assumptions
- Creates standardized project structure
- Manages Python version and dependencies
- Faster than traditional pip/venv workflow

**Implementation**:
```bash
uv init --python 3.13
uv add --dev pytest  # Only if testing requested
```

**Alternatives Considered**:
- `python -m venv`: Standard but slower, requires manual dependency management
- `poetry`: More features than needed, violates Simplicity First principle

---

### Decision 2: In-Memory Storage Structure

**Decision**: Use `dict[int, Todo]` where key is todo ID, value is Todo object

**Rationale**:
- O(1) lookup by ID for update, delete, mark complete operations
- Sequential ID generation via counter variable
- Efficient for requirement FR-003 (unique integer ID assignment)
- Simple to implement and understand (Principle II)

**Implementation**:
```python
todos: dict[int, Todo] = {}
next_id: int = 1
```

**Alternatives Considered**:
- List of todos: O(n) lookup, requires scanning for ID matches
- Todo IDs as indices: Fragile after deletions, violates FR-003 (sequential but not reused)

---

### Decision 3: CLI Menu Loop Pattern

**Decision**: Infinite while loop with match/case for menu selection

**Rationale**:
- FR-010 requires continuous running until Exit
- Python 3.10+ match/case provides clean menu dispatch
- Readable for beginner-intermediate developers (SC-007)
- Easy error handling for invalid choices

**Implementation**:
```python
while True:
    print_menu()
    choice = input("Enter choice: ").strip()
    match choice:
        case "1": add_todo()
        case "2": view_todos()
        case "3": update_todo()
        case "4": delete_todo()
        case "5": mark_complete()
        case "6": break  # Exit
        case _: print("Invalid choice. Try again.")
```

**Alternatives Considered**:
- Dict mapping choices to functions: Less readable for beginners
- If/elif chain: Verbose and repetitive

---

### Decision 4: Input Validation Strategy

**Decision**: Validate at input time with try/except for integers, strip() + check for empty strings

**Rationale**:
- Satisfies FR-005 (non-empty descriptions), FR-012 (validate before processing)
- Clear error messages per FR-006
- Prevents crashes (Constitution: Production-Minded Engineering)

**Implementation**:
```python
def get_todo_id() -> int | None:
    try:
        id_input = input("Enter todo ID: ").strip()
        return int(id_input)
    except ValueError:
        print("Error: Please enter a valid number")
        return None

def get_description() -> str | None:
    desc = input("Enter todo description: ").strip()
    if not desc:
        print("Error: Todo description cannot be empty")
        return None
    return desc
```

**Alternatives Considered**:
- Regex validation: Overkill for simple integer/string validation
- Type hints without runtime checks: Doesn't satisfy error handling requirements

---

### Decision 5: Screen Clearing (Cross-Platform)

**Decision**: Use `os.system('cls' if os.name == 'nt' else 'clear')` wrapped in try/except

**Rationale**:
- FR-011 requires screen clearing "optional based on platform support"
- Works on Windows (cls) and Unix-like (clear)
- Graceful fallback if command fails

**Implementation**:
```python
import os

def clear_screen():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        pass  # Fail silently if clearing not supported
```

**Alternatives Considered**:
- ANSI escape codes: Not universally supported on Windows
- Skip screen clearing: Reduces readability (FR-011 benefit)

---

### Decision 6: Completion Status Representation

**Decision**: Boolean `is_complete: bool` with display conversion to ✓/✗

**Rationale**:
- Simple and memory-efficient (Principle II: Simplicity First)
- Easy logic for mark_complete operation
- FR-008 requires visual indicators—convert at display time

**Implementation**:
```python
@dataclass
class Todo:
    id: int
    description: str
    is_complete: bool = False

def format_status(is_complete: bool) -> str:
    return "✓" if is_complete else "✗"
```

**Alternatives Considered**:
- String status ("pending"/"complete"): More memory, string comparison overhead
- Enum: Over-engineering for binary state

---

## Research Summary

All technical decisions prioritize:
1. **Simplicity**: No external dependencies, standard library only
2. **Readability**: Clear patterns for beginner-intermediate developers
3. **Performance**: O(1) dict lookups, instantaneous for <1000 items (SC-002, SC-005)
4. **Constitution Compliance**: Phase I constraints satisfied, no premature abstractions

**Dependencies**: None beyond Python 3.13 standard library (pytest optional for testing)

**Risks**: None identified—straightforward implementation with well-understood patterns

---

# Phase 1: Design & Contracts

## Data Model

### Entity: Todo

**Purpose**: Represents a single todo item with unique ID, description, and completion status

**Attributes**:
- `id: int` — Unique identifier, auto-assigned sequentially starting from 1 (FR-003)
- `description: str` — Non-empty text describing the task (FR-004, FR-005)
- `is_complete: bool` — Completion status, defaults to False (FR-004)

**Validation Rules**:
- `id`: Must be positive integer, unique across all todos
- `description`: Cannot be empty or whitespace-only (FR-005)
- `is_complete`: Boolean only (True = complete, False = pending)

**State Transitions**:
```
[Created: is_complete=False]
    ↓
[Mark Complete: is_complete=True]
    (No reverse transition—idempotent if already complete)
```

**Implementation** (see `data-model.md` for full details):
```python
from dataclasses import dataclass

@dataclass
class Todo:
    id: int
    description: str
    is_complete: bool = False
```

---

## CLI Interface Contracts

### Menu Display

**Output Format**:
```
=== Todo Application ===
1. Add Todo
2. View Todos
3. Update Todo
4. Mark Todo Complete
5. Delete Todo
6. Exit
========================
Enter choice (1-6):
```

**Contract**: Display menu after each operation completes (FR-010 continuous loop)

---

### Operation 1: Add Todo

**Input**: User enters todo description (non-empty string)

**Process**:
1. Prompt: `Enter todo description: `
2. Validate: Reject empty/whitespace-only input (FR-005)
3. Assign unique sequential ID (FR-003)
4. Store in memory with `is_complete=False`
5. Display confirmation (FR-007)

**Success Output**: `Todo added successfully (ID: {id})`

**Error Output**: `Error: Todo description cannot be empty`

**Acceptance**: Spec US1 scenarios 1-3

---

### Operation 2: View Todos

**Input**: None (menu selection only)

**Process**:
1. Check if todos exist
2. Display all todos with ID, description, status (FR-008)
3. Format status as ✓ (complete) or ✗ (pending)

**Success Output** (todos exist):
```
=== Your Todos ===
1. ✗ Write unit tests
2. ✓ Review pull request
3. ✗ Fix authentication bug
==================
```

**Success Output** (no todos):
```
No todos found. Add your first todo to get started.
```

**Acceptance**: Spec US2 scenarios 1-3

---

### Operation 3: Update Todo

**Input**: Todo ID (integer), new description (non-empty string)

**Process**:
1. Prompt: `Enter todo ID: `
2. Validate ID is integer and exists (FR-009, FR-012)
3. Prompt: `Enter new description: `
4. Validate description non-empty (FR-005)
5. Update todo description in memory
6. Display confirmation (FR-007)

**Success Output**: `Todo #{id} updated successfully`

**Error Outputs**:
- `Error: Please enter a valid number` (invalid ID input)
- `Error: Todo with ID {id} not found` (FR-009)
- `Error: New description cannot be empty` (FR-005)

**Acceptance**: Spec US4 scenarios 1-3

---

### Operation 4: Delete Todo

**Input**: Todo ID (integer)

**Process**:
1. Prompt: `Enter todo ID: `
2. Validate ID is integer and exists (FR-009, FR-012)
3. Remove todo from memory
4. Display confirmation (FR-007)

**Success Output**: `Todo #{id} deleted successfully`

**Error Outputs**:
- `Error: Please enter a valid number` (invalid ID input)
- `Error: Todo with ID {id} not found` (FR-009)

**Acceptance**: Spec US5 scenarios 1-3

---

### Operation 5: Mark Todo Complete

**Input**: Todo ID (integer)

**Process**:
1. Prompt: `Enter todo ID: `
2. Validate ID is integer and exists (FR-009, FR-012)
3. Check if already complete (idempotent operation)
4. Set `is_complete = True`
5. Display confirmation (FR-007)

**Success Output**: `Todo #{id} marked as complete`

**Info Output** (already complete): `Todo #{id} is already complete`

**Error Outputs**:
- `Error: Please enter a valid number` (invalid ID input)
- `Error: Todo with ID {id} not found` (FR-009)

**Acceptance**: Spec US3 scenarios 1-3

---

### Operation 6: Exit

**Input**: Menu selection only

**Process**:
1. Display exit message
2. Break main loop
3. Program terminates

**Output**: `Goodbye! All todos will be lost (in-memory storage).`

**Side Effect**: All data lost (expected behavior per spec assumptions)

---

## Quickstart Guide

See [quickstart.md](./quickstart.md) for:
- Installation (UV setup, Python 3.13+)
- Running the application (`uv run src/todo_app.py`)
- Example usage walkthrough (add → view → mark complete → delete)
- Troubleshooting common issues

---

## Architecture Diagram

```
┌─────────────────────────────────────────────┐
│         User (Terminal/Console)              │
└──────────────────┬──────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────┐
│  todo_app.py (CLI Interface)                 │
│  - Display menu                              │
│  - Get user input                            │
│  - Format output                             │
│  - Call TodoManager methods                  │
└──────────────────┬──────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────┐
│  todo_manager.py (Business Logic)            │
│  - add_todo(description) → Todo              │
│  - get_all_todos() → list[Todo]              │
│  - update_todo(id, description) → bool       │
│  - delete_todo(id) → bool                    │
│  - mark_complete(id) → bool                  │
│  - Validation logic                          │
│  - In-memory storage (dict[int, Todo])       │
└──────────────────┬──────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────┐
│  todo_model.py (Data Structure)              │
│  - Todo dataclass                            │
│    - id: int                                 │
│    - description: str                        │
│    - is_complete: bool                       │
└─────────────────────────────────────────────┘
```

**Design Rationale**:
- **Separation of Concerns**: CLI (presentation) → Manager (business logic) → Model (data)
- **Testability**: TodoManager can be tested independently of CLI
- **Simplicity**: Three modules, clear responsibilities, no over-abstraction
- **Phase I Compliance**: No persistence layer, no external services, in-memory only

---

## Success Criteria Validation

| Criterion | Design Support |
|-----------|----------------|
| SC-001: Add todo in <10 seconds | Simple input prompts, minimal steps |
| SC-002: Instant view (<1000 items) | Dict iteration, no I/O delays |
| SC-003: 100% CRUD functionality | All 5 operations designed with contracts |
| SC-004: Error messages <1 second | Immediate validation, no network/disk I/O |
| SC-005: Handle 1000 items | Dict performance O(1) lookups, O(n) iteration |
| SC-006: Clear menu labels | Explicit menu text, numbered choices |
| SC-007: Readable code | Three-module structure, clear naming, docstrings |

---

## Phase 1 Summary

**Artifacts Created**:
1. ✅ `research.md` — Technical decisions documented
2. ✅ `data-model.md` — Todo entity specification
3. ✅ `contracts/cli-interface.md` — CLI operation contracts
4. ✅ `quickstart.md` — Installation and usage guide
5. ✅ This plan updated with design details

**Constitution Re-Check**: ✅ **PASS** — Design maintains Phase I constraints, no violations introduced

**Next Steps**: Run `/sp.tasks` to generate task breakdown from this plan

**Readiness**: ✅ Ready for task generation and implementation
