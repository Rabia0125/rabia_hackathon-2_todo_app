"""Main CLI application for in-memory todo manager."""

import os
from todo_manager import TodoManager


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


def print_menu():
    """Display the main menu options."""
    print("=== Todo Application ===")
    print("1. Add Todo")
    print("2. View Todos")
    print("3. Update Todo")
    print("4. Mark Todo Complete")
    print("5. Delete Todo")
    print("6. Exit")
    print("========================")


def get_description(prompt: str = "Enter todo description: ") -> str | None:
    """Prompt for description and validate non-empty.

    Args:
        prompt: The prompt text to display

    Returns:
        Valid description (whitespace stripped), or None if validation failed
    """
    desc = input(prompt).strip()
    if not desc:
        print("Error: Todo description cannot be empty")
        return None
    return desc


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


def format_status(is_complete: bool) -> str:
    """Convert boolean status to visual indicator.

    Args:
        is_complete: True for complete, False for pending

    Returns:
        Visual indicator: ✓ (complete) or ✗ (pending)
    """
    return "✓" if is_complete else "✗"


def add_todo_interaction(manager: TodoManager):
    """Handle add todo user interaction.

    Args:
        manager: TodoManager instance
    """
    description = get_description()
    if description is None:
        return  # Validation failed

    todo = manager.add_todo(description)
    print(f"Todo added successfully (ID: {todo.id})")


def view_todos_interaction(manager: TodoManager):
    """Handle view todos user interaction.

    Args:
        manager: TodoManager instance
    """
    todos = manager.get_all_todos()

    if not todos:
        print("No todos found. Add your first todo to get started.")
        return

    print("\n=== Your Todos ===")
    for todo in todos:
        status_icon = format_status(todo.is_complete)
        print(f"{todo.id}. {status_icon} {todo.description}")
    print("==================\n")


def update_todo_interaction(manager: TodoManager):
    """Handle update todo user interaction.

    Args:
        manager: TodoManager instance
    """
    todo_id = get_todo_id()
    if todo_id is None:
        return  # Validation failed

    # Check if todo exists before asking for new description
    if manager.get_todo(todo_id) is None:
        print(f"Error: Todo with ID {todo_id} not found")
        return

    new_description = get_description("Enter new description: ")
    if new_description is None:
        return  # Validation failed

    success = manager.update_todo(todo_id, new_description)
    if success:
        print(f"Todo #{todo_id} updated successfully")
    else:
        print(f"Error: Todo with ID {todo_id} not found")


def mark_complete_interaction(manager: TodoManager):
    """Handle mark complete user interaction.

    Args:
        manager: TodoManager instance
    """
    todo_id = get_todo_id()
    if todo_id is None:
        return  # Validation failed

    success, was_already_complete = manager.mark_complete(todo_id)

    if not success:
        print(f"Error: Todo with ID {todo_id} not found")
    elif was_already_complete:
        print(f"Todo #{todo_id} is already complete")
    else:
        print(f"Todo #{todo_id} marked as complete")


def delete_todo_interaction(manager: TodoManager):
    """Handle delete todo user interaction.

    Args:
        manager: TodoManager instance
    """
    todo_id = get_todo_id()
    if todo_id is None:
        return  # Validation failed

    success = manager.delete_todo(todo_id)

    if success:
        print(f"Todo #{todo_id} deleted successfully")
    else:
        print(f"Error: Todo with ID {todo_id} not found")


def main():
    """Main application loop."""
    manager = TodoManager()

    while True:
        clear_screen()
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
                mark_complete_interaction(manager)
            case "5":
                delete_todo_interaction(manager)
            case "6":
                print("\nGoodbye! All todos will be lost (in-memory storage).")
                break
            case _:
                print("Invalid choice. Please enter a number between 1 and 6.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
