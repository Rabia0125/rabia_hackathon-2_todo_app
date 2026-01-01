"""Todo manager for business logic and in-memory storage."""

from todo_model import Todo


class TodoManager:
    """Manages todo items with in-memory storage.

    Attributes:
        todos: Dictionary mapping todo IDs to Todo objects
        next_id: Counter for generating unique sequential IDs
    """

    def __init__(self):
        """Initialize empty todo storage."""
        self.todos: dict[int, Todo] = {}
        self.next_id: int = 1

    def add_todo(self, description: str) -> Todo:
        """Add new todo with auto-generated ID.

        Args:
            description: Non-empty text describing the task

        Returns:
            The newly created Todo object
        """
        todo_id = self.next_id
        self.next_id += 1
        new_todo = Todo(id=todo_id, description=description)
        self.todos[todo_id] = new_todo
        return new_todo

    def get_all_todos(self) -> list[Todo]:
        """Retrieve all todos sorted by ID.

        Returns:
            List of all Todo objects sorted by ID
        """
        return sorted(self.todos.values(), key=lambda t: t.id)

    def get_todo(self, todo_id: int) -> Todo | None:
        """Retrieve todo by ID.

        Args:
            todo_id: The ID of the todo to retrieve

        Returns:
            Todo object if found, None otherwise
        """
        return self.todos.get(todo_id)

    def update_todo(self, todo_id: int, new_description: str) -> bool:
        """Update todo description.

        Args:
            todo_id: The ID of the todo to update
            new_description: New description text

        Returns:
            True if successful, False if todo not found
        """
        todo = self.todos.get(todo_id)
        if todo is None:
            return False
        todo.description = new_description.strip()
        return True

    def delete_todo(self, todo_id: int) -> bool:
        """Delete todo by ID.

        Args:
            todo_id: The ID of the todo to delete

        Returns:
            True if successful, False if todo not found
        """
        if todo_id not in self.todos:
            return False
        del self.todos[todo_id]
        return True

    def mark_complete(self, todo_id: int) -> tuple[bool, bool]:
        """Mark todo as complete.

        Args:
            todo_id: The ID of the todo to mark complete

        Returns:
            Tuple of (success, was_already_complete)
            - (True, False): Successfully marked complete
            - (True, True): Was already complete (idempotent)
            - (False, False): Todo not found
        """
        todo = self.todos.get(todo_id)
        if todo is None:
            return (False, False)

        was_already_complete = todo.is_complete
        todo.is_complete = True
        return (True, was_already_complete)
