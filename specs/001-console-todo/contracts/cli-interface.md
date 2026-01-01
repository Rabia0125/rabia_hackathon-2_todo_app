# CLI Interface Contracts: In-Memory Console Todo Application

**Feature**: 001-console-todo
**Created**: 2026-01-02
**Purpose**: Define input/output contracts for all CLI operations

---

## Menu Interface

### Main Menu Display

**Trigger**: After each operation completes (continuous loop per FR-010)

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

**Input**: Single digit string ("1" through "6")

**Validation**: Any input outside "1"-"6" displays error and re-prompts

**Invalid Input Handling**:
```
Invalid choice. Please enter a number between 1 and 6.
```

---

## Operation Contracts

### 1. Add Todo

**Menu Choice**: `1`

**Input Sequence**:
1. Prompt: `Enter todo description: `
2. User enters text and presses Enter

**Validation**:
- Empty input: Display error, re-prompt
- Whitespace-only input: Display error, re-prompt
- Valid input: Strip whitespace, proceed

**Success Flow**:
1. Generate unique sequential ID
2. Create Todo with `is_complete=False`
3. Store in memory
4. Display confirmation

**Success Output**:
```
Todo added successfully (ID: {id})
```

**Error Output** (empty/whitespace):
```
Error: Todo description cannot be empty
```

**Examples**:
```
Input: "Write unit tests"
Output: Todo added successfully (ID: 1)

Input: "   "
Output: Error: Todo description cannot be empty

Input: "  Review pull request  "
Output: Todo added successfully (ID: 2)
  (Stored as "Review pull request" with whitespace stripped)
```

**Acceptance Criteria**: Spec US1 scenarios 1-3

---

### 2. View Todos

**Menu Choice**: `2`

**Input**: None (immediate execution)

**Processing**:
1. Check if any todos exist
2. If empty, display empty state message
3. If not empty, display all todos sorted by ID

**Success Output** (todos exist):
```
=== Your Todos ===
{id}. {status} {description}
{id}. {status} {description}
...
==================
```

Where:
- `{id}`: Todo ID (integer)
- `{status}`: ✓ (complete) or ✗ (pending)
- `{description}`: Todo text

**Success Output** (no todos):
```
No todos found. Add your first todo to get started.
```

**Examples**:
```
# With 3 todos (IDs 1, 2, 3; ID 2 is complete)
=== Your Todos ===
1. ✗ Write unit tests
2. ✓ Review pull request
3. ✗ Fix authentication bug
==================

# Empty list
No todos found. Add your first todo to get started.
```

**Performance**: Display must be instantaneous (<100ms) for up to 1000 todos (SC-002)

**Acceptance Criteria**: Spec US2 scenarios 1-3

---

### 3. Update Todo

**Menu Choice**: `3`

**Input Sequence**:
1. Prompt: `Enter todo ID: `
2. User enters integer ID
3. Prompt: `Enter new description: `
4. User enters new description

**Validation**:
1. ID must be valid integer (try/except ValueError)
2. ID must exist in todos dict
3. New description cannot be empty/whitespace-only

**Success Flow**:
1. Validate ID input
2. Check todo exists
3. Validate new description
4. Update todo.description
5. Display confirmation

**Success Output**:
```
Todo #{id} updated successfully
```

**Error Outputs**:
```
# Non-integer ID input
Error: Please enter a valid number

# ID not found
Error: Todo with ID {id} not found

# Empty new description
Error: New description cannot be empty
```

**Examples**:
```
Input: ID=3, New description="Fix authentication bug in login module"
Output: Todo #3 updated successfully

Input: ID=10 (doesn't exist)
Output: Error: Todo with ID 10 not found

Input: ID="abc"
Output: Error: Please enter a valid number

Input: ID=1, New description="   "
Output: Error: New description cannot be empty
```

**Acceptance Criteria**: Spec US4 scenarios 1-3

---

### 4. Mark Todo Complete

**Menu Choice**: `5` (note: spec says option 5, but some acceptance scenarios reference this as operation 4)

**Input Sequence**:
1. Prompt: `Enter todo ID: `
2. User enters integer ID

**Validation**:
1. ID must be valid integer
2. ID must exist in todos dict

**Success Flow**:
1. Validate ID input
2. Check todo exists
3. Check if already complete (informational message, not error)
4. Set is_complete = True
5. Display confirmation

**Success Output** (newly completed):
```
Todo #{id} marked as complete
```

**Info Output** (already complete):
```
Todo #{id} is already complete
```

**Error Outputs**:
```
# Non-integer ID input
Error: Please enter a valid number

# ID not found
Error: Todo with ID {id} not found
```

**Examples**:
```
Input: ID=1 (currently pending)
Output: Todo #1 marked as complete

Input: ID=2 (already complete)
Output: Todo #2 is already complete

Input: ID=99 (doesn't exist)
Output: Error: Todo with ID 99 not found

Input: ID="test"
Output: Error: Please enter a valid number
```

**Idempotency**: Operation is safe to repeat—no error if already complete

**Acceptance Criteria**: Spec US3 scenarios 1-3

---

### 5. Delete Todo

**Menu Choice**: `4` (note: spec says option 4, but menu shows this as option 5)

**Input Sequence**:
1. Prompt: `Enter todo ID: `
2. User enters integer ID

**Validation**:
1. ID must be valid integer
2. ID must exist in todos dict

**Success Flow**:
1. Validate ID input
2. Check todo exists
3. Remove from todos dict
4. Display confirmation

**Success Output**:
```
Todo #{id} deleted successfully
```

**Error Outputs**:
```
# Non-integer ID input
Error: Please enter a valid number

# ID not found
Error: Todo with ID {id} not found
```

**Examples**:
```
Input: ID=2
Output: Todo #2 deleted successfully
(Todo with ID 2 removed; IDs 1, 3, 4, 5 remain if they existed)

Input: ID=7 (doesn't exist)
Output: Error: Todo with ID 7 not found

Input: ID="delete"
Output: Error: Please enter a valid number
```

**Side Effect**: ID is never reused—next added todo gets next sequential ID

**Acceptance Criteria**: Spec US5 scenarios 1-3

---

### 6. Exit

**Menu Choice**: `6`

**Input**: None (immediate execution)

**Processing**:
1. Display exit message
2. Break main loop
3. Program terminates

**Output**:
```
Goodbye! All todos will be lost (in-memory storage).
```

**Side Effect**: All todos in memory are lost (expected behavior per spec)

**No Error Cases**: Exit always succeeds

---

## Cross-Cutting Concerns

### Screen Clearing (Optional)

**Trigger**: After each operation completes, before redisplaying menu

**Implementation**:
```python
import os

def clear_screen():
    """Clear console screen (cross-platform)."""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        pass  # Fail silently if clearing not supported
```

**Rationale**: FR-011 specifies "optional based on platform support"

**Behavior**:
- Windows: Runs `cls` command
- Unix-like (Linux, macOS): Runs `clear` command
- Unsupported platforms: Fails silently, continues without clearing

---

### Input Validation Helpers

**Integer ID Validation**:
```python
def get_todo_id() -> int | None:
    """Prompt for todo ID and validate integer input."""
    try:
        id_input = input("Enter todo ID: ").strip()
        return int(id_input)
    except ValueError:
        print("Error: Please enter a valid number")
        return None
```

**Description Validation**:
```python
def get_description(prompt: str = "Enter todo description: ") -> str | None:
    """Prompt for description and validate non-empty."""
    desc = input(prompt).strip()
    if not desc:
        print("Error: Todo description cannot be empty")
        return None
    return desc
```

**Usage Pattern**:
```python
todo_id = get_todo_id()
if todo_id is None:
    return  # Validation failed, return to menu

description = get_description()
if description is None:
    return  # Validation failed, return to menu
```

---

## Error Message Guidelines

### Format

All error messages follow this pattern:
```
Error: {descriptive message explaining what went wrong}
```

### Clarity Requirements (FR-006)

1. **Specific**: Include the problematic value when helpful
   - ✅ "Error: Todo with ID 5 not found"
   - ❌ "Error: Not found"

2. **Actionable**: Suggest what user should do
   - ✅ "Error: Please enter a valid number"
   - ❌ "Error: Invalid input"

3. **User-Friendly**: Avoid technical jargon
   - ✅ "Error: Todo description cannot be empty"
   - ❌ "Error: ValueError: empty string not allowed"

### Response Time (SC-004)

All error messages must display within 1 second of invalid input (immediate validation, no I/O delays)

---

## Success Message Guidelines

### Format

Confirmation messages follow patterns:
```
{Action} {result} (additional info if needed)
```

Examples:
- "Todo added successfully (ID: 5)"
- "Todo #3 updated successfully"
- "Todo #7 deleted successfully"
- "Todo #2 marked as complete"

### Consistency (FR-007)

All successful operations provide confirmation messages—never silently succeed

---

## Performance Requirements

| Operation | Max Response Time | Success Criterion |
|-----------|------------------|-------------------|
| Add Todo | <10 seconds | SC-001 (includes user input time) |
| View Todos | <100ms | SC-002 (instantaneous display) |
| Update Todo | <1 second | SC-004 (validation + update) |
| Delete Todo | <1 second | SC-004 (validation + delete) |
| Mark Complete | <1 second | SC-004 (validation + update) |
| Error Display | <1 second | SC-004 (immediate feedback) |

**Note**: "Add Todo" includes time for user to type description, while other operations are system response times

---

## Contract Summary

| Operation | Inputs | Validation | Success Output | Error Outputs |
|-----------|--------|------------|----------------|---------------|
| Add | Description (str) | Non-empty | Confirmation + ID | Empty description |
| View | None | N/A | Formatted list or empty msg | N/A |
| Update | ID (int), Description (str) | ID exists, non-empty desc | Confirmation | Invalid ID, not found, empty desc |
| Delete | ID (int) | ID exists | Confirmation | Invalid ID, not found |
| Mark Complete | ID (int) | ID exists | Confirmation or already-complete | Invalid ID, not found |
| Exit | None | N/A | Goodbye message | N/A |

---

## Constitution Compliance

| Principle | Compliance | Evidence |
|-----------|------------|----------|
| IV. Production-Minded Engineering | ✅ | Comprehensive error handling, input validation, clear messages |
| VI. Clean CLI UX | ✅ | Predictable menu, helpful errors, consistent confirmations |

All contracts support FR-001 through FR-012 and success criteria SC-001 through SC-007.
