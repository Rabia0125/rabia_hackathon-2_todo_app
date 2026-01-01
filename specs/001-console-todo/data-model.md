# Data Model: In-Memory Console Todo Application

**Feature**: 001-console-todo
**Created**: 2026-01-02
**Purpose**: Define the Todo entity structure and in-memory storage design

---

## Entity: Todo

### Overview

The `Todo` entity represents a single task item in the todo list. Each todo has a unique identifier, descriptive text, and completion status.

### Attributes

| Attribute      | Type    | Required | Default | Description |
|----------------|---------|----------|---------|-------------|
| `id`           | `int`   | Yes      | Auto-assigned | Unique sequential identifier starting from 1 |
| `description`  | `str`   | Yes      | None    | Non-empty text describing the task |
| `is_complete`  | `bool`  | Yes      | `False` | Completion status (True = complete, False = pending) |

### Validation Rules

1. **ID Validation**:
   - Must be positive integer (>= 1)
   - Must be unique across all todos in the system
   - Auto-assigned sequentially, never reused after deletion

2. **Description Validation**:
   - Cannot be empty string
   - Cannot be whitespace-only string
   - No length limit (accepts 500+ character descriptions per edge cases)
   - Trailing/leading whitespace should be stripped before storage

3. **Completion Status Validation**:
   - Must be boolean value only
   - Default value is `False` (pending) when todo is created
   - Once set to `True`, remains `True` (no reverse transition)

### State Diagram

```
┌─────────────────────┐
│  Todo Created       │
│  is_complete=False  │
└──────────┬──────────┘
           │
           │ mark_complete()
           ↓
┌─────────────────────┐
│  Todo Completed     │
│  is_complete=True   │
└─────────────────────┘
     │
     │ mark_complete() again (idempotent)
     ↓
┌─────────────────────┐
│  Todo Completed     │
│  is_complete=True   │
│  (no change)        │
└─────────────────────┘
```

### Python Implementation

```python
from dataclasses import dataclass

@dataclass
class Todo:
    """Represents a single todo item.

    Attributes:
        id: Unique sequential identifier (positive integer)
        description: Non-empty text describing the task
        is_complete: Completion status (False = pending, True = complete)
    """
    id: int
    description: str
    is_complete: bool = False

    def __post_init__(self):
        """Validate todo attributes after initialization."""
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError(f"Todo ID must be positive integer, got: {self.id}")

        if not isinstance(self.description, str) or not self.description.strip():
            raise ValueError("Todo description cannot be empty")

        # Strip whitespace from description
        self.description = self.description.strip()

        if not isinstance(self.is_complete, bool):
            raise ValueError(f"is_complete must be boolean, got: {type(self.is_complete)}")
```

---

## In-Memory Storage Design

### Storage Structure

**Primary Storage**: `dict[int, Todo]`

```python
# Global state in TodoManager
todos: dict[int, Todo] = {}
next_id: int = 1
```

**Rationale**:
- Dictionary provides O(1) lookup by ID for update, delete, mark_complete operations
- Sequential ID generation via `next_id` counter ensures uniqueness
- Simple to implement and understand (Constitution Principle II: Simplicity First)

### Storage Operations

| Operation | Time Complexity | Implementation |
|-----------|----------------|----------------|
| Add       | O(1)           | `todos[next_id] = Todo(...); next_id += 1` |
| Get by ID | O(1)           | `todos.get(id)` or `todos[id]` |
| View All  | O(n)           | `list(todos.values())` |
| Update    | O(1)           | `todos[id].description = new_desc` |
| Delete    | O(1)           | `del todos[id]` |
| Mark Complete | O(1)       | `todos[id].is_complete = True` |

### ID Management

**Sequential ID Assignment**:
```python
def generate_next_id() -> int:
    """Generate next unique ID and increment counter."""
    global next_id
    current_id = next_id
    next_id += 1
    return current_id
```

**ID Reuse Policy**: IDs are **never reused** after deletion
- Example: If todos with IDs 1, 2, 3 exist and ID 2 is deleted, the next added todo gets ID 4 (not 2)
- Rationale: Prevents confusion, simplifies ID generation, aligns with sequential numbering requirement

### Memory Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| Per-Todo Overhead | ~64 bytes | Python object overhead + 3 attributes |
| 1000 Todos Memory | ~64 KB | Well within memory constraints |
| Max Capacity | 1000+ todos | Performance requirement (SC-005) |

---

## Data Access Patterns

### Pattern 1: Add Todo

```python
def add_todo(description: str) -> Todo:
    """Add new todo with auto-generated ID."""
    todo_id = generate_next_id()
    new_todo = Todo(id=todo_id, description=description)
    todos[todo_id] = new_todo
    return new_todo
```

### Pattern 2: Get All Todos

```python
def get_all_todos() -> list[Todo]:
    """Retrieve all todos sorted by ID."""
    return sorted(todos.values(), key=lambda t: t.id)
```

### Pattern 3: Get Todo by ID

```python
def get_todo(todo_id: int) -> Todo | None:
    """Retrieve todo by ID, return None if not found."""
    return todos.get(todo_id)
```

### Pattern 4: Update Todo

```python
def update_todo(todo_id: int, new_description: str) -> bool:
    """Update todo description, return True if successful."""
    todo = todos.get(todo_id)
    if todo is None:
        return False
    todo.description = new_description.strip()
    return True
```

### Pattern 5: Delete Todo

```python
def delete_todo(todo_id: int) -> bool:
    """Delete todo by ID, return True if successful."""
    if todo_id not in todos:
        return False
    del todos[todo_id]
    return True
```

### Pattern 6: Mark Todo Complete

```python
def mark_complete(todo_id: int) -> bool:
    """Mark todo as complete, return True if successful."""
    todo = todos.get(todo_id)
    if todo is None:
        return False
    todo.is_complete = True
    return True
```

---

## Edge Cases

### Empty List Handling

**Scenario**: No todos exist, user tries to view/update/delete
**Behavior**: Return appropriate message or False
**Example**:
```python
if not todos:
    print("No todos found. Add your first todo to get started.")
```

### Invalid ID Handling

**Scenario**: User provides ID that doesn't exist
**Behavior**: Return None or False, display error message
**Example**:
```python
todo = todos.get(invalid_id)
if todo is None:
    print(f"Error: Todo with ID {invalid_id} not found")
```

### Duplicate Completion

**Scenario**: User marks already-complete todo as complete
**Behavior**: Idempotent operation, display informational message
**Example**:
```python
if todo.is_complete:
    print(f"Todo #{todo_id} is already complete")
else:
    todo.is_complete = True
    print(f"Todo #{todo_id} marked as complete")
```

### Large Description Handling

**Scenario**: User enters 500+ character description
**Behavior**: Accept and store without truncation
**Rationale**: No length limit specified, edge cases allow long descriptions

---

## Constitution Compliance

| Principle | Compliance | Evidence |
|-----------|------------|----------|
| I. Incremental Evolution | ✅ | Phase I only—no persistence, no database schema |
| II. Simplicity First | ✅ | Simple dict, no ORM, no caching layer |
| III. Clear Separation | ✅ | Data model separate from business logic and CLI |
| IV. Production-Minded | ✅ | Validation in `__post_init__`, error handling patterns |
| V. Readable Code | ✅ | Clear attribute names, docstrings, type hints |

---

## Summary

- **Entity**: Single `Todo` dataclass with 3 attributes (id, description, is_complete)
- **Storage**: In-memory `dict[int, Todo]` for O(1) operations
- **ID Management**: Sequential auto-increment, never reused
- **Validation**: Post-init checks for ID, description, status
- **Performance**: Supports 1000+ todos with instantaneous operations
- **Phase I Compliance**: No persistence, no external dependencies
