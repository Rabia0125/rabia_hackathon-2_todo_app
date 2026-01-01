# Research & Technical Decisions: In-Memory Console Todo Application

**Feature**: 001-console-todo
**Created**: 2026-01-02
**Purpose**: Document all technical research and decision rationale

---

## Overview

This document captures the technical research conducted during Phase 0 of the implementation planning process. All decisions prioritize Constitution Principle II (Simplicity First, Scalability Later) and Phase I constraints (in-memory only, no external dependencies).

---

## Decision 1: UV Project Initialization

### Question
How should we initialize a Python 3.13+ project with UV package manager?

### Decision
Use `uv init --python 3.13` to create standardized project structure with `pyproject.toml`

### Rationale
- **Spec Requirement**: UV is explicitly specified in project assumptions
- **Speed**: UV is significantly faster than traditional pip/venv workflow (10-100x)
- **Standardization**: Creates consistent project structure with version locking
- **Dependency Management**: Built-in dependency resolution and virtual environment handling
- **Future-Proof**: Prepares for Phase II when external dependencies will be needed

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| `python -m venv` | Standard library, universally available | Slow, manual dependency management, no automatic version locking | Doesn't meet spec requirement for UV |
| `poetry` | Rich feature set, popular in community | Heavier than needed, more complexity than required for Phase I | Violates Principle II (Simplicity First) |
| Manual `pyproject.toml` | Full control, minimal tooling | Error-prone, no dependency resolution, more work | Doesn't leverage UV as specified |

### Implementation
```bash
# Initialize project
uv init --python 3.13

# Add dev dependencies (only if testing requested)
uv add --dev pytest

# Run application
uv run src/todo_app.py
```

### Impact
- **Constitution Compliance**: ✅ Uses specified tooling without over-engineering
- **Phase I Constraints**: ✅ No external runtime dependencies (pytest is dev-only)
- **Developer Experience**: Faster setup, consistent environment

---

## Decision 2: In-Memory Storage Structure

### Question
What Python data structure should store todos: list or dictionary?

### Decision
Use `dict[int, Todo]` where key is todo ID, value is Todo object

### Rationale
- **Performance**: O(1) lookup by ID for update, delete, mark_complete operations vs O(n) for list
- **ID Management**: Keys naturally enforce unique IDs
- **Simplicity**: Direct mapping from ID to todo object is intuitive
- **Requirement Alignment**: FR-003 mandates unique integer IDs—dict keys provide this guarantee
- **Scale**: Efficient for SC-005 requirement (handle 1000 items)

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| `list[Todo]` | Simple, ordered by default | O(n) lookup for ID operations, need separate ID tracking | Poor performance for update/delete/complete |
| List with ID as index | O(1) access by index | IDs can't be reused after deletion (sparse list), fragile | Violates FR-003 (sequential but not reused) |
| `dict[int, dict]` | No class needed | Loses type safety, no validation | Violates Principle V (readable code) and SC-007 (clean code) |

### Implementation
```python
# Storage
todos: dict[int, Todo] = {}
next_id: int = 1

# Operations
def add_todo(description: str) -> Todo:
    todo_id = next_id
    next_id += 1
    todo = Todo(id=todo_id, description=description)
    todos[todo_id] = todo
    return todo

def get_todo(todo_id: int) -> Todo | None:
    return todos.get(todo_id)  # O(1)

def delete_todo(todo_id: int) -> bool:
    if todo_id not in todos:
        return False
    del todos[todo_id]  # O(1)
    return True
```

### Performance Analysis

| Operation | List | Dict | Winner |
|-----------|------|------|--------|
| Add | O(1) | O(1) | Tie |
| Get by ID | O(n) | O(1) | **Dict** |
| View all | O(n) | O(n) | Tie |
| Update | O(n) | O(1) | **Dict** |
| Delete | O(n) | O(1) | **Dict** |
| Mark Complete | O(n) | O(1) | **Dict** |

### Impact
- **Constitution Compliance**: ✅ Simple structure, no over-engineering
- **Performance**: Meets SC-002 (instant view), SC-005 (1000 items)
- **Code Quality**: Clear and readable (Principle V)

---

## Decision 3: CLI Menu Loop Pattern

### Question
What control flow pattern should implement the continuous menu loop (FR-010)?

### Decision
Infinite `while True` loop with Python 3.10+ `match/case` for menu dispatch

### Rationale
- **Requirement**: FR-010 mandates "run continuously until user selects Exit"
- **Readability**: `match/case` is cleaner than if/elif chains for beginners (SC-007)
- **Error Handling**: Default case (`case _:`) naturally handles invalid choices
- **Python Version**: Match/case available in Python 3.10+, we're using 3.13+
- **Exit Strategy**: `break` statement cleanly exits loop on choice "6"

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| If/elif chain | Works in all Python versions | Verbose, repetitive, less readable | Match/case is cleaner for Python 3.10+ |
| Dict mapping to functions | Compact, functional style | Less intuitive for beginners, more abstraction | Violates SC-007 (beginner-intermediate readability) |
| Recursive function calls | Functional programming style | Stack overflow risk, harder to debug | Over-engineered for simple menu |

### Implementation
```python
def main():
    manager = TodoManager()

    while True:
        clear_screen()  # Optional per FR-011
        print_menu()
        choice = input("Enter choice (1-6): ").strip()

        match choice:
            case "1":
                add_todo_interaction(manager)
            case "2":
                view_todos_interaction(manager)
            case "3":
                update_todo_interaction(manager)
            case "4":
                delete_todo_interaction(manager)
            case "5":
                mark_complete_interaction(manager)
            case "6":
                print("Goodbye! All todos will be lost (in-memory storage).")
                break
            case _:
                print("Invalid choice. Please enter a number between 1 and 6.")

        input("\nPress Enter to continue...")  # Pause before clearing screen
```

### Impact
- **Constitution Compliance**: ✅ Clear, readable pattern (Principle V)
- **User Experience**: Predictable flow, clear error handling (Principle VI)
- **Maintainability**: Easy to add/modify menu options

---

## Decision 4: Input Validation Strategy

### Question
How should we validate user inputs (integer IDs, non-empty strings)?

### Decision
Validate at input time using:
- `try/except ValueError` for integer parsing
- `str.strip() + truthiness check` for non-empty strings
- Return `None` on validation failure to signal error to caller

### Rationale
- **Requirements**: FR-005 (non-empty descriptions), FR-012 (validate before processing)
- **Error Messages**: FR-006 requires clear, user-friendly errors
- **Crash Prevention**: Constitution Principle IV (Production-Minded Engineering)
- **Pythonic**: Uses standard library features, no regex overkill
- **Readability**: Clear validation logic for beginner-intermediate developers (SC-007)

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Regex validation | Powerful pattern matching | Overkill for simple int/string checks, harder to read | Violates Principle II (Simplicity First) |
| Type hints only | Clean type annotations | No runtime validation, doesn't prevent crashes | Doesn't satisfy FR-006, FR-012 |
| Exception raising | Pythonic error handling | Harder control flow for CLI interactions | Less intuitive for menu-driven app |
| Assert statements | Compact | Disabled with `-O` flag, not for input validation | Inappropriate for user input |

### Implementation

**Integer ID Validation**:
```python
def get_todo_id() -> int | None:
    """Prompt for todo ID and validate integer input.

    Returns:
        Valid integer ID, or None if validation failed
    """
    try:
        id_input = input("Enter todo ID: ").strip()
        return int(id_input)
    except ValueError:
        print("Error: Please enter a valid number")
        return None
```

**String Description Validation**:
```python
def get_description(prompt: str = "Enter todo description: ") -> str | None:
    """Prompt for description and validate non-empty.

    Returns:
        Valid description (whitespace stripped), or None if validation failed
    """
    desc = input(prompt).strip()
    if not desc:
        print("Error: Todo description cannot be empty")
        return None
    return desc
```

**Usage Pattern**:
```python
def add_todo_interaction(manager: TodoManager):
    """Handle add todo user interaction."""
    description = get_description()
    if description is None:
        return  # Validation failed, return to menu

    todo = manager.add_todo(description)
    print(f"Todo added successfully (ID: {todo.id})")
```

### Error Message Examples

| Input | Output | Requirement Met |
|-------|--------|-----------------|
| ID: "abc" | "Error: Please enter a valid number" | FR-006 (clear error) |
| ID: "  5  " | Accepts 5 (strips whitespace) | FR-012 (validate) |
| Description: "" | "Error: Todo description cannot be empty" | FR-005 (non-empty) |
| Description: "   " | "Error: Todo description cannot be empty" | FR-005 (reject whitespace-only) |

### Impact
- **Constitution Compliance**: ✅ Production-minded error handling (Principle IV)
- **User Experience**: Clear, actionable error messages (Principle VI)
- **Code Quality**: Readable validation logic (Principle V)

---

## Decision 5: Screen Clearing (Cross-Platform)

### Question
How should we implement screen clearing (FR-011) that works on Windows, macOS, and Linux?

### Decision
Use `os.system('cls' if os.name == 'nt' else 'clear')` wrapped in try/except for graceful fallback

### Rationale
- **Requirement**: FR-011 specifies "optional based on platform support"
- **Cross-Platform**: `cls` for Windows, `clear` for Unix-like systems
- **Graceful Degradation**: Try/except allows app to continue if clearing fails
- **Standard Library**: No external dependencies (os module is built-in)
- **User Experience**: Improves readability by clearing clutter between operations

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| ANSI escape codes | Pure Python, no system calls | Not universally supported on Windows | Compatibility issues |
| Colorama library | Cross-platform ANSI support | External dependency | Violates Phase I constraints (no external deps) |
| Skip screen clearing | Simplest approach | Cluttered output, harder to read | Reduces UX quality (FR-011 benefit) |
| Print newlines | Works everywhere | Doesn't truly clear, just scrolls | Doesn't meet "clear screen" intent |

### Implementation
```python
import os

def clear_screen():
    """Clear console screen (cross-platform).

    Works on:
    - Windows: Uses 'cls' command
    - Unix-like (Linux, macOS): Uses 'clear' command
    - Unsupported platforms: Fails silently
    """
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        pass  # Fail silently per FR-011 (optional support)
```

**Usage**:
```python
while True:
    clear_screen()  # Clear before each menu display
    print_menu()
    # ... handle user input
```

### Platform Compatibility

| Platform | os.name | Command | Support |
|----------|---------|---------|---------|
| Windows | 'nt' | cls | ✅ Native |
| macOS | 'posix' | clear | ✅ Native |
| Linux | 'posix' | clear | ✅ Native |
| WSL | 'posix' | clear | ✅ Native |
| Other Unix | 'posix' | clear | ⚠️ Usually works |

### Impact
- **Constitution Compliance**: ✅ Standard library only, simple implementation
- **User Experience**: Cleaner interface, easier to focus on current operation
- **Robustness**: Graceful fallback prevents crashes on unsupported platforms

---

## Decision 6: Completion Status Representation

### Question
Should completion status be boolean (`is_complete: bool`) or string (`status: str`)?

### Decision
Boolean `is_complete: bool` with display-time conversion to visual indicators (✓/✗)

### Rationale
- **Simplicity**: Binary state (complete/pending) naturally maps to boolean (Principle II)
- **Memory Efficiency**: 1 byte vs ~8+ bytes for string
- **Logic Clarity**: Simple boolean checks vs string comparisons
- **Display Flexibility**: Convert to any visual format (✓/✗, [ ]/[X], emoji) at display time
- **Requirement**: FR-008 specifies visual indicators—implemented in presentation layer, not data model

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| String status ("pending"/"complete") | Human-readable in data | More memory, string comparison overhead, typo risk | Violates Principle II (Simplicity First) |
| Enum (Status.PENDING, Status.COMPLETE) | Type-safe, explicit values | Over-engineered for binary state | Overkill for two states |
| Integer (0=pending, 1=complete) | Compact | Less readable than boolean | Boolean is more Pythonic |

### Implementation

**Data Model**:
```python
from dataclasses import dataclass

@dataclass
class Todo:
    id: int
    description: str
    is_complete: bool = False  # Defaults to pending
```

**Display Conversion**:
```python
def format_status(is_complete: bool) -> str:
    """Convert boolean status to visual indicator.

    Args:
        is_complete: True for complete, False for pending

    Returns:
        Visual indicator: ✓ (complete) or ✗ (pending)
    """
    return "✓" if is_complete else "✗"

def display_todo(todo: Todo):
    """Display a single todo with visual status."""
    status_icon = format_status(todo.is_complete)
    print(f"{todo.id}. {status_icon} {todo.description}")
```

**Business Logic**:
```python
def mark_complete(todo_id: int) -> bool:
    """Mark todo as complete."""
    todo = todos.get(todo_id)
    if todo is None:
        return False
    todo.is_complete = True  # Simple assignment
    return True
```

### Visual Indicator Options

If Unicode (✓/✗) doesn't display correctly on some terminals, easy to change:

```python
# Option 1: ASCII brackets (fallback)
def format_status(is_complete: bool) -> str:
    return "[X]" if is_complete else "[ ]"

# Option 2: Text (most compatible)
def format_status(is_complete: bool) -> str:
    return "DONE" if is_complete else "TODO"

# Option 3: Emoji (modern terminals)
def format_status(is_complete: bool) -> str:
    return "✅" if is_complete else "⬜"
```

### Impact
- **Constitution Compliance**: ✅ Simplest representation (Principle II)
- **Performance**: Minimal memory, fast boolean operations
- **Code Quality**: Clear intent, easy to understand (Principle V)
- **Flexibility**: Easy to change visual representation without touching data model

---

## Cross-Cutting Decisions

### Logging Strategy
**Decision**: No logging for Phase I
**Rationale**:
- Console output serves as logging
- No file persistence allowed (Phase I constraint)
- No errors expected that require debugging logs
- Keep implementation minimal (Principle II)

**Future**: Phase II will add structured logging when external dependencies allowed

---

### Error Handling Philosophy
**Decision**: Validate early, fail gracefully, display clear messages
**Implementation Pattern**:
```python
# Validate input
value = get_input()
if value is None:
    return  # Validation failed, error already displayed

# Perform operation
success = operation(value)
if not success:
    print(f"Error: Operation failed because...")
    return

# Success path
print("Success message")
```

**Rationale**: Satisfies FR-006 (clear errors), FR-007 (confirmations), Principle IV (production-minded)

---

### Testing Strategy (Optional)
**Decision**: Unit tests for business logic (TodoManager), optional for Phase I
**Scope**:
- Test `TodoManager` methods (add, get, update, delete, mark_complete)
- Test `Todo` validation in `__post_init__`
- Skip CLI interaction tests (hard to test input/output)

**Rationale**:
- Constitution specifies unit tests for business logic
- TDD is optional unless explicitly requested
- Focus on testable components (manager, not CLI)

---

## Research Summary

### Technologies Chosen
- **Language**: Python 3.13+
- **Package Manager**: UV
- **Project Structure**: pyproject.toml
- **Testing** (optional): pytest

### Key Patterns
- **Storage**: `dict[int, Todo]` for O(1) operations
- **Menu**: `while True` with `match/case` dispatch
- **Validation**: Early validation with None return on failure
- **Screen Clearing**: Cross-platform with graceful fallback
- **Status**: Boolean with display-time conversion

### Dependencies
- **Runtime**: None (Python standard library only)
- **Development**: pytest (optional, dev-only)

### Constitution Compliance Summary

| Principle | Status | Key Decisions Supporting |
|-----------|--------|--------------------------|
| I. Incremental Evolution | ✅ | Phase I only, no Phase II features |
| II. Simplicity First | ✅ | Dict storage, boolean status, no external deps |
| III. Clear Separation | ✅ | Model → Manager → CLI layering |
| IV. Production-Minded | ✅ | Input validation, error handling, clear messages |
| V. Readable Code | ✅ | Match/case, clear naming, type hints, docstrings |
| VI. Clean CLI UX | ✅ | Clear menu, helpful errors, status indicators |

### Performance Validation

| Success Criterion | Design Support | Confidence |
|-------------------|----------------|------------|
| SC-001: Add <10s | Simple prompts, minimal steps | ✅ High |
| SC-002: View instant | Dict iteration, no I/O | ✅ High |
| SC-003: 100% CRUD | All operations designed | ✅ High |
| SC-004: Errors <1s | Immediate validation | ✅ High |
| SC-005: 1000 items | Dict O(1) lookups | ✅ High |
| SC-006: Clear labels | Explicit menu text | ✅ High |
| SC-007: Readable code | Three-module structure | ✅ High |

---

## Risks & Mitigation

### Risk 1: Unicode Display Issues
**Risk**: ✓/✗ characters may not display on all terminals
**Likelihood**: Low (most modern terminals support Unicode)
**Impact**: Cosmetic only, app still functions
**Mitigation**: Easy to switch to ASCII ([X]/[ ]) in format_status()

### Risk 2: Large Description Performance
**Risk**: 500+ character descriptions could slow display
**Likelihood**: Very Low (string operations fast in Python)
**Impact**: Minimal (would need 100,000+ character descriptions)
**Mitigation**: No limit imposed, accept long descriptions per edge cases

### Risk 3: Screen Clearing Failure
**Risk**: os.system() may fail on some platforms
**Likelihood**: Low (Windows/macOS/Linux all supported)
**Impact**: Minor (clutter, but app works)
**Mitigation**: Try/except catches failure, app continues

**Overall Risk Level**: ✅ **LOW** — All risks are cosmetic or unlikely

---

## Next Phase Preparation

### Phase II Considerations (Future)
When moving to Next.js + FastAPI + Neon DB:
- **Data Model**: Todo dataclass can migrate to SQLModel with minimal changes
- **Business Logic**: TodoManager can become FastAPI service layer
- **Storage**: Replace dict with database queries
- **CLI**: Replaced by web frontend and REST API

**Migration Strategy**: The three-layer design (Model → Manager → Interface) allows clean transition—just replace CLI and dict storage while keeping business logic intact.

---

## Conclusion

All research questions resolved with decisions that:
1. ✅ Satisfy Phase I constitution constraints
2. ✅ Meet all functional requirements (FR-001 through FR-012)
3. ✅ Support success criteria (SC-001 through SC-007)
4. ✅ Prioritize simplicity and readability
5. ✅ Use only Python standard library (no external runtime deps)

**Status**: Ready for Phase 1 (Design & Contracts) and task generation
