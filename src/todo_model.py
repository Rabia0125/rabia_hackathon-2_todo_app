"""Todo data model for in-memory todo application."""

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
