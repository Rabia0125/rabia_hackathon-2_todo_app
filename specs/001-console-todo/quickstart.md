# Quickstart Guide: In-Memory Console Todo Application

**Feature**: 001-console-todo
**Created**: 2026-01-02
**Purpose**: Get up and running with the todo application in under 5 minutes

---

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.13+** installed
   - Check version: `python --version` or `python3 --version`
   - Download from: https://www.python.org/downloads/

2. **UV Package Manager** installed
   - Check: `uv --version`
   - Install: `pip install uv` or follow https://github.com/astral-sh/uv

3. **Terminal/Command Prompt** access
   - Windows: Command Prompt, PowerShell, or Windows Terminal
   - macOS/Linux: Terminal app

---

## Installation

### Step 1: Clone or Navigate to Project

```bash
cd path/to/my_todo_app
```

### Step 2: Initialize UV Project

If not already initialized:

```bash
uv init --python 3.13
```

This creates:
- `pyproject.toml` — Project configuration
- `.python-version` — Python version lock

### Step 3: Install Dependencies (Optional)

For testing only (not required for core functionality):

```bash
uv add --dev pytest
```

---

## Running the Application

### Standard Launch

```bash
uv run src/todo_app.py
```

**Expected Output**:
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

### Alternative Launch (without UV)

If UV is not available:

```bash
python src/todo_app.py
```

or

```bash
python3 src/todo_app.py
```

---

## Basic Usage Walkthrough

### Example Session: Complete Todo Workflow

```
=== Todo Application ===
1. Add Todo
2. View Todos
3. Update Todo
4. Mark Todo Complete
5. Delete Todo
6. Exit
========================
Enter choice (1-6): 1

Enter todo description: Write unit tests
Todo added successfully (ID: 1)

=== Todo Application ===
[Menu displays...]
Enter choice (1-6): 1

Enter todo description: Review pull request
Todo added successfully (ID: 2)

Enter choice (1-6): 1

Enter todo description: Fix authentication bug
Todo added successfully (ID: 3)

Enter choice (1-6): 2

=== Your Todos ===
1. ✗ Write unit tests
2. ✗ Review pull request
3. ✗ Fix authentication bug
==================

Enter choice (1-6): 5

Enter todo ID: 2
Todo #2 marked as complete

Enter choice (1-6): 2

=== Your Todos ===
1. ✗ Write unit tests
2. ✓ Review pull request
3. ✗ Fix authentication bug
==================

Enter choice (1-6): 3

Enter todo ID: 3
Enter new description: Fix authentication bug in login module
Todo #3 updated successfully

Enter choice (1-6): 4

Enter todo ID: 1
Todo #1 deleted successfully

Enter choice (1-6): 2

=== Your Todos ===
2. ✓ Review pull request
3. ✗ Fix authentication bug in login module
==================

Enter choice (1-6): 6

Goodbye! All todos will be lost (in-memory storage).
```

---

## Common Operations

### Add a Todo

1. Select option `1`
2. Enter description (non-empty text)
3. Press Enter
4. Receive confirmation with assigned ID

**Tips**:
- Whitespace is automatically trimmed
- No length limit—long descriptions are supported
- Empty input prompts error and re-asks

### View All Todos

1. Select option `2`
2. See list of all todos with IDs and status icons
   - ✗ = Pending
   - ✓ = Complete

**Tips**:
- Empty list shows helpful message
- Todos sorted by ID
- Instant display (no delays)

### Update a Todo

1. Select option `3`
2. Enter todo ID (must exist)
3. Enter new description (non-empty)
4. Receive confirmation

**Tips**:
- Only description changes—ID and status unchanged
- Original description completely replaced

### Mark Todo Complete

1. Select option `5`
2. Enter todo ID (must exist)
3. Receive confirmation

**Tips**:
- Safe to mark already-complete todos (informational message)
- No reverse operation (cannot mark as pending)

### Delete a Todo

1. Select option `4`
2. Enter todo ID (must exist)
3. Receive confirmation

**Tips**:
- Todo is permanently removed
- ID is never reused for new todos

### Exit Application

1. Select option `6`
2. Application closes
3. **All todos are lost** (in-memory storage only)

---

## Troubleshooting

### Problem: "Python not found" or "uv not found"

**Solution**:
- Ensure Python 3.13+ is installed: `python --version`
- Ensure UV is installed: `uv --version`
- Add Python and UV to system PATH
- Try `python3` or `py` instead of `python`

### Problem: "ModuleNotFoundError" when running

**Solution**:
- Ensure you're in the project root directory
- Check that `src/todo_app.py` exists
- Try: `uv run src/todo_app.py` instead of direct Python execution

### Problem: "Error: Please enter a valid number"

**Cause**: You entered non-integer value for todo ID

**Solution**:
- Enter only digits (e.g., `1`, `23`, `456`)
- Do not enter letters or special characters

### Problem: "Error: Todo with ID X not found"

**Cause**: The todo ID you entered doesn't exist

**Solution**:
- First run option `2` (View Todos) to see valid IDs
- Use one of the displayed IDs
- Remember: Deleted IDs are gone permanently

### Problem: "Error: Todo description cannot be empty"

**Cause**: You pressed Enter without typing text, or entered only spaces

**Solution**:
- Type at least one non-whitespace character
- Example valid inputs: "a", "Buy milk", "Write tests"

### Problem: Screen doesn't clear between operations

**Cause**: Your terminal doesn't support clear commands (rare)

**Solution**:
- This is expected behavior (FR-011: optional screen clearing)
- Application still functions correctly
- Manually scroll up to see previous output

### Problem: Unicode characters (✓, ✗) don't display correctly

**Cause**: Terminal encoding doesn't support Unicode

**Solution**:
- Windows: Use Windows Terminal instead of Command Prompt
- Or: Update code to use ASCII characters ([ ], [X])
- Application still functions—purely cosmetic issue

---

## Performance Expectations

| Operation | Expected Speed |
|-----------|----------------|
| Add todo | Instant (<10 seconds including typing) |
| View todos | Instant (even with 1000 items) |
| Update todo | Instant (<1 second) |
| Delete todo | Instant (<1 second) |
| Mark complete | Instant (<1 second) |

If operations feel slow:
- Check if another process is consuming CPU
- Ensure you're not over 1000 todos (design limit)

---

## Data Persistence Notice

⚠️ **IMPORTANT**: This is an **in-memory application**

- All todos exist only in RAM while the program runs
- When you exit (option 6) or close the terminal, **all data is lost**
- No files are saved, no databases are used
- This is Phase I design per project constitution

**If you need persistence**: Wait for Phase II (Next.js + FastAPI + Neon DB)

---

## Testing (Optional)

If you installed pytest:

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/unit/test_todo_manager.py
```

**Test Coverage**:
- `test_todo_model.py` — Todo dataclass validation
- `test_todo_manager.py` — Business logic (add, view, update, delete, complete)

---

## Next Steps

### After Using the Application

1. **Generate Tasks**: Run `/sp.tasks` to create implementation task list
2. **Implement Features**: Follow task breakdown to build the application
3. **Run Tests**: Verify each feature works per acceptance criteria
4. **Commit Code**: Use git to track changes

### Moving to Phase II

Once Phase I is complete and validated:
1. Review Phase II requirements (Next.js + FastAPI + Neon DB)
2. Run `/sp.specify` for Phase II feature
3. Migrate business logic to API layer
4. Add persistent storage with database

---

## Support

### Documentation

- **Specification**: `specs/001-console-todo/spec.md` — User stories and requirements
- **Implementation Plan**: `specs/001-console-todo/plan.md` — Architecture and design decisions
- **Data Model**: `specs/001-console-todo/data-model.md` — Todo entity definition
- **CLI Contracts**: `specs/001-console-todo/contracts/cli-interface.md` — Input/output specifications

### Constitution

See `.specify/memory/constitution.md` for:
- Project principles and constraints
- Phase I requirements (in-memory only, no external dependencies)
- Quality standards (testing, performance, security)

---

## Quick Reference

| Menu Option | Action | Requires Input |
|-------------|--------|----------------|
| 1 | Add Todo | Description (text) |
| 2 | View Todos | None |
| 3 | Update Todo | ID (int), New Description (text) |
| 4 | Delete Todo | ID (int) |
| 5 | Mark Complete | ID (int) |
| 6 | Exit | None |

**Status Icons**: ✗ = Pending, ✓ = Complete

**Common Errors**:
- "Please enter a valid number" → Use digits only for IDs
- "Todo with ID X not found" → Check View Todos for valid IDs
- "Todo description cannot be empty" → Type at least one character

**Remember**: All data is lost when you exit! 🚨
