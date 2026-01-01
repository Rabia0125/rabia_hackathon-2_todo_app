# In-Memory Console Todo Application

A simple, Phase I Python console application for managing todos. All data is stored in memory - no persistence, no external dependencies.

## Features

- ✅ **Add** new todo items
- 📋 **View** all todos with status indicators
- ✏️ **Update** todo descriptions
- ✓ **Mark** todos as complete
- 🗑️ **Delete** todos
- 🚪 **Exit** the application

## Requirements

- Python 3.13+
- UV package manager

## Installation

```bash
# Clone the repository
cd my_todo_app

# Initialize UV (if not already done)
uv init --python 3.13
```

## Usage

Run the application:

```bash
uv run src/todo_app.py
```

Or directly with Python:

```bash
python src/todo_app.py
```

## Menu Options

1. **Add Todo** - Create a new todo item
2. **View Todos** - Display all todos with their status
3. **Update Todo** - Modify a todo's description
4. **Mark Todo Complete** - Mark a todo as done
5. **Delete Todo** - Remove a todo permanently
6. **Exit** - Close the application

## Data Storage

⚠️ **Important**: This is an in-memory application. All todos are lost when you exit!

## Project Structure

```
my_todo_app/
├── src/
│   ├── todo_app.py      # Main CLI application
│   ├── todo_manager.py  # Business logic
│   └── todo_model.py    # Todo data model
├── specs/               # Feature specifications
├── pyproject.toml       # Project configuration
└── README.md           # This file
```

## Phase I Constraints

This Phase I implementation follows strict constraints:
- ✅ In-memory storage only (Python dict)
- ✅ No external dependencies
- ✅ Console interface only
- ❌ No file persistence
- ❌ No web interface
- ❌ No database

## Development

This project demonstrates the Agentic Dev Stack workflow:
- Spec → Plan → Tasks → Implementation

See `specs/001-console-todo/` for full documentation.

## License

MIT License
