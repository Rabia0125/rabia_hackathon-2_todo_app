"""Test script for todo application functionality."""

import sys
sys.path.insert(0, 'src')

from todo_model import Todo
from todo_manager import TodoManager


def test_todo_model():
    """Test Todo dataclass validation."""
    print("Testing Todo model...")

    # Test valid todo
    todo = Todo(id=1, description="Test todo", is_complete=False)
    assert todo.id == 1
    assert todo.description == "Test todo"
    assert todo.is_complete == False
    print("[OK] Valid todo creation works")

    # Test description stripping
    todo = Todo(id=2, description="  Spaces  ", is_complete=False)
    assert todo.description == "Spaces"
    print("[OK]Description whitespace stripping works")

    # Test empty description validation
    try:
        Todo(id=3, description="", is_complete=False)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "empty" in str(e).lower()
        print("[OK]Empty description validation works")

    # Test invalid ID validation
    try:
        Todo(id=0, description="Test", is_complete=False)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "positive" in str(e).lower()
        print("[OK]Invalid ID validation works")

    print()


def test_todo_manager():
    """Test TodoManager business logic."""
    print("Testing TodoManager...")
    manager = TodoManager()

    # Test add_todo
    todo1 = manager.add_todo("First todo")
    assert todo1.id == 1
    assert todo1.description == "First todo"
    assert not todo1.is_complete
    print("[OK]Add todo works")

    todo2 = manager.add_todo("Second todo")
    assert todo2.id == 2
    print("[OK]Sequential ID assignment works")

    # Test get_all_todos
    all_todos = manager.get_all_todos()
    assert len(all_todos) == 2
    assert all_todos[0].id == 1
    assert all_todos[1].id == 2
    print("[OK]Get all todos works")

    # Test mark_complete
    success, was_complete = manager.mark_complete(1)
    assert success and not was_complete
    assert manager.get_todo(1).is_complete
    print("[OK]Mark complete works")

    # Test idempotent mark_complete
    success, was_complete = manager.mark_complete(1)
    assert success and was_complete
    print("[OK]Idempotent mark complete works")

    # Test mark_complete with invalid ID
    success, _ = manager.mark_complete(999)
    assert not success
    print("[OK]Mark complete with invalid ID returns False")

    # Test update_todo
    success = manager.update_todo(2, "Updated second todo")
    assert success
    assert manager.get_todo(2).description == "Updated second todo"
    print("[OK]Update todo works")

    # Test update_todo with invalid ID
    success = manager.update_todo(999, "Nonexistent")
    assert not success
    print("[OK]Update with invalid ID returns False")

    # Test delete_todo
    success = manager.delete_todo(2)
    assert success
    assert manager.get_todo(2) is None
    assert len(manager.get_all_todos()) == 1
    print("[OK]Delete todo works")

    # Test delete_todo with invalid ID
    success = manager.delete_todo(999)
    assert not success
    print("[OK]Delete with invalid ID returns False")

    # Test ID not reused after deletion
    todo3 = manager.add_todo("Third todo")
    assert todo3.id == 3  # Not 2!
    print("[OK]IDs not reused after deletion")

    print()


def test_edge_cases():
    """Test edge cases from specification."""
    print("Testing edge cases...")
    manager = TodoManager()

    # Empty list handling
    todos = manager.get_all_todos()
    assert len(todos) == 0
    print("[OK]Empty list handling works")

    # Long description (500+ characters)
    long_desc = "A" * 600
    todo = manager.add_todo(long_desc)
    assert len(todo.description) == 600
    print("[OK]Long descriptions (500+ chars) accepted")

    # Whitespace-only description rejected by Todo model
    try:
        Todo(id=1, description="   ", is_complete=False)
        assert False, "Should reject whitespace-only"
    except ValueError:
        print("[OK]Whitespace-only description rejected")

    # Multiple operations
    for i in range(10):
        manager.add_todo(f"Todo {i}")
    assert len(manager.get_all_todos()) == 11  # 1 + 10
    print("[OK]Multiple operations work correctly")

    print()


def test_1000_todos():
    """Test performance with 1000 todos (SC-005)."""
    print("Testing with 1000 todos (performance requirement)...")
    manager = TodoManager()

    import time

    # Add 1000 todos
    start = time.time()
    for i in range(1000):
        manager.add_todo(f"Todo {i}")
    add_time = time.time() - start
    print(f"[OK]Added 1000 todos in {add_time:.3f}s")

    # View all todos
    start = time.time()
    todos = manager.get_all_todos()
    view_time = time.time() - start
    assert len(todos) == 1000
    print(f"[OK]Retrieved 1000 todos in {view_time:.3f}s")
    assert view_time < 0.1, f"View should be <100ms, got {view_time:.3f}s"

    # Update a todo
    start = time.time()
    manager.update_todo(500, "Updated todo 500")
    update_time = time.time() - start
    print(f"[OK]Updated todo in {update_time:.3f}s")
    assert update_time < 0.001, f"Update should be <1ms, got {update_time:.3f}s"

    # Mark complete
    start = time.time()
    manager.mark_complete(750)
    complete_time = time.time() - start
    print(f"[OK]Marked complete in {complete_time:.3f}s")
    assert complete_time < 0.001, f"Complete should be <1ms, got {complete_time:.3f}s"

    # Delete a todo
    start = time.time()
    manager.delete_todo(250)
    delete_time = time.time() - start
    print(f"[OK]Deleted todo in {delete_time:.3f}s")
    assert delete_time < 0.001, f"Delete should be <1ms, got {delete_time:.3f}s"

    print()


if __name__ == "__main__":
    print("=" * 60)
    print("TESTING IN-MEMORY TODO APPLICATION")
    print("=" * 60)
    print()

    try:
        test_todo_model()
        test_todo_manager()
        test_edge_cases()
        test_1000_todos()

        print("=" * 60)
        print("[PASS] ALL TESTS PASSED")
        print("=" * 60)
        print()
        print("Application is ready to use!")
        print("Run: uv run src/todo_app.py")
        print()

    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"[FAIL] TEST FAILED: {e}")
        print("=" * 60)
        sys.exit(1)
    except Exception as e:
        print()
        print("=" * 60)
        print(f"[ERROR] ERROR: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        sys.exit(1)
