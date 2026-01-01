# Tasks: In-Memory Console Todo Application

**Input**: Design documents from `/specs/001-console-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/cli-interface.md

**Tests**: Not explicitly requested in specification - test tasks are OPTIONAL and not included

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below use single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize UV project with Python 3.13+ using `uv init --python 3.13`
- [x] T002 Create src directory for application code
- [x] T003 [P] Create pyproject.toml with project metadata (name: my-todo-app, requires-python: >=3.13)
- [x] T004 [P] Create README.md with project overview and usage instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create Todo dataclass in src/todo_model.py with id, description, is_complete attributes
- [x] T006 Add validation to Todo.__post_init__ for non-empty description and positive ID
- [x] T007 Create TodoManager class in src/todo_manager.py with empty dict storage and next_id counter
- [x] T008 [P] Create main CLI loop skeleton in src/todo_app.py with while True and menu display
- [x] T009 [P] Implement clear_screen() function in src/todo_app.py using os.system for cross-platform support
- [x] T010 [P] Implement print_menu() function in src/todo_app.py displaying 6 options (Add, View, Update, Mark Complete, Delete, Exit)
- [x] T011 Implement menu dispatch using match/case in src/todo_app.py main loop with handlers for choices 1-6

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Todo Items (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo items with validation and confirmation

**Independent Test**: Launch app, add multiple todos with various descriptions (valid and invalid), verify storage and confirmation messages

### Implementation for User Story 1

- [x] T012 [P] [US1] Implement get_description() helper in src/todo_app.py with strip() and empty validation
- [x] T013 [P] [US1] Implement add_todo() method in src/todo_manager.py that creates Todo with auto-assigned ID
- [x] T014 [US1] Implement add_todo_interaction() in src/todo_app.py calling get_description() and manager.add_todo()
- [x] T015 [US1] Add success confirmation message "Todo added successfully (ID: {id})" in add_todo_interaction()
- [x] T016 [US1] Add error handling for empty description with message "Error: Todo description cannot be empty"
- [x] T017 [US1] Connect menu choice "1" to add_todo_interaction() in main loop

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Todo Items (Priority: P1)

**Goal**: Display all todos with IDs, descriptions, and status indicators in clear format

**Independent Test**: Add several todos (some complete, some pending), view list, verify all display correctly with ✓/✗ icons

### Implementation for User Story 2

- [x] T018 [P] [US2] Implement format_status() helper in src/todo_app.py returning "✓" for complete, "✗" for pending
- [x] T019 [P] [US2] Implement get_all_todos() method in src/todo_manager.py returning sorted list of todos by ID
- [x] T020 [US2] Implement view_todos_interaction() in src/todo_app.py calling manager.get_all_todos()
- [x] T021 [US2] Add empty state handling in view_todos_interaction() displaying "No todos found. Add your first todo to get started."
- [x] T022 [US2] Add todo display loop in view_todos_interaction() formatting as "{id}. {status} {description}"
- [x] T023 [US2] Add header "=== Your Todos ===" and footer "==================" to view output
- [x] T024 [US2] Connect menu choice "2" to view_todos_interaction() in main loop

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (MVP complete)

---

## Phase 5: User Story 3 - Mark Todo as Complete (Priority: P2)

**Goal**: Allow users to mark todos as complete by ID with idempotent behavior

**Independent Test**: Add todos, mark specific ones as complete, verify status updates in view, test idempotency and error cases

### Implementation for User Story 3

- [x] T025 [P] [US3] Implement get_todo_id() helper in src/todo_app.py with try/except ValueError for integer validation
- [x] T026 [P] [US3] Implement mark_complete() method in src/todo_manager.py setting is_complete=True if todo exists
- [x] T027 [US3] Implement mark_complete_interaction() in src/todo_app.py calling get_todo_id() and manager.mark_complete()
- [x] T028 [US3] Add success message "Todo #{id} marked as complete" in mark_complete_interaction()
- [x] T029 [US3] Add idempotent handling for already-complete todos displaying "Todo #{id} is already complete"
- [x] T030 [US3] Add error handling for invalid ID with message "Error: Please enter a valid number"
- [x] T031 [US3] Add error handling for non-existent ID with message "Error: Todo with ID {id} not found"
- [x] T032 [US3] Connect menu choice "5" to mark_complete_interaction() in main loop

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Todo Description (Priority: P3)

**Goal**: Enable users to update todo descriptions by ID with validation

**Independent Test**: Add todos, update descriptions with valid and invalid inputs, verify changes persist in view

### Implementation for User Story 4

- [x] T033 [P] [US4] Implement update_todo() method in src/todo_manager.py updating description if todo exists
- [x] T034 [US4] Implement update_todo_interaction() in src/todo_app.py calling get_todo_id() and get_description()
- [x] T035 [US4] Call manager.update_todo() in update_todo_interaction() with validated ID and description
- [x] T036 [US4] Add success message "Todo #{id} updated successfully" in update_todo_interaction()
- [x] T037 [US4] Add error handling for invalid ID with message "Error: Please enter a valid number"
- [x] T038 [US4] Add error handling for non-existent ID with message "Error: Todo with ID {id} not found"
- [x] T039 [US4] Add error handling for empty new description with message "Error: New description cannot be empty"
- [x] T040 [US4] Connect menu choice "3" to update_todo_interaction() in main loop

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Delete Todo Items (Priority: P3)

**Goal**: Allow users to delete todos by ID with permanent removal

**Independent Test**: Add todos, delete specific ones, verify removal in view, test error cases

### Implementation for User Story 5

- [x] T041 [P] [US5] Implement delete_todo() method in src/todo_manager.py removing todo from dict if exists
- [x] T042 [US5] Implement delete_todo_interaction() in src/todo_app.py calling get_todo_id() and manager.delete_todo()
- [x] T043 [US5] Add success message "Todo #{id} deleted successfully" in delete_todo_interaction()
- [x] T044 [US5] Add error handling for invalid ID with message "Error: Please enter a valid number"
- [x] T045 [US5] Add error handling for non-existent ID with message "Error: Todo with ID {id} not found"
- [x] T046 [US5] Connect menu choice "4" to delete_todo_interaction() in main loop

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Exit and Polish

**Purpose**: Complete exit functionality and final touches

- [x] T047 Implement exit handling for menu choice "6" displaying "Goodbye! All todos will be lost (in-memory storage)."
- [x] T048 Add break statement in exit case to terminate main loop
- [x] T049 [P] Add "Press Enter to continue..." pause after each operation before clearing screen
- [x] T050 [P] Add invalid menu choice handling in default case displaying "Invalid choice. Please enter a number between 1 and 6."
- [x] T051 [P] Add if __name__ == "__main__": guard to src/todo_app.py main() call
- [x] T052 Review all error messages for clarity and consistency with spec requirements
- [x] T053 Test all edge cases from spec: empty list, invalid IDs, whitespace-only input, 500+ char descriptions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P2 → P3 → P3)
- **Exit & Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories (uses US1 todos for testing but independent implementation)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Helper functions marked [P] can run in parallel (different files or independent functions)
- Manager methods before interaction handlers (interaction calls manager)
- Interaction implementation before menu connection (menu calls interaction)
- Error handling can be added in parallel with success path

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T003, T004)
- All Foundational tasks marked [P] can run in parallel (T008, T009, T010)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Within each story, tasks marked [P] can run in parallel:
  - US1: T012, T013 (helper and manager method)
  - US2: T018, T019 (helper and manager method)
  - US3: T025, T026 (helper and manager method)
  - US4: T033 only one [P]
  - US5: T041 only one [P]
- Polish phase: T049, T050, T051, T052 can all run in parallel

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch these in parallel:
Task T012: "Implement get_description() helper in src/todo_app.py"
Task T013: "Implement add_todo() method in src/todo_manager.py"

# Then sequentially:
Task T014: "Implement add_todo_interaction() in src/todo_app.py" (depends on T012, T013)
Task T015: "Add success confirmation message" (depends on T014)
Task T016: "Add error handling for empty description" (can parallel with T015)
Task T017: "Connect menu choice to interaction" (depends on T014)
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T011) - CRITICAL blocker
3. Complete Phase 3: User Story 1 (T012-T017) - Add functionality
4. Complete Phase 4: User Story 2 (T018-T024) - View functionality
5. **STOP and VALIDATE**: Test adding and viewing todos independently
6. Add exit handling (T047-T048) for clean shutdown
7. Deploy/demo if ready - you now have an MVP!

### Incremental Delivery (Full Feature Set)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Add only)
3. Add User Story 2 → Test independently → Deploy/Demo (MVP: Add + View)
4. Add User Story 3 → Test independently → Deploy/Demo (Add + View + Complete)
5. Add User Story 4 → Test independently → Deploy/Demo (Add + View + Complete + Update)
6. Add User Story 5 → Test independently → Deploy/Demo (Full CRUD)
7. Add Polish → Final validation → Production deployment

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done (after T011):
   - Developer A: User Story 1 (T012-T017)
   - Developer B: User Story 2 (T018-T024)
   - Developer C: User Story 3 (T025-T032)
   - Developer D: User Story 4 (T033-T040)
   - Developer E: User Story 5 (T041-T046)
3. Stories complete and integrate independently
4. Team collaborates on Polish phase

---

## Notes

- [P] tasks = different files/functions, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group (e.g., after each user story phase)
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Constitution compliance: All tasks respect Phase I constraints (in-memory only, no external deps)

---

## Task Count Summary

- **Total Tasks**: 53
- **Setup (Phase 1)**: 4 tasks
- **Foundational (Phase 2)**: 7 tasks (BLOCKING)
- **User Story 1 (Phase 3)**: 6 tasks
- **User Story 2 (Phase 4)**: 7 tasks
- **User Story 3 (Phase 5)**: 8 tasks
- **User Story 4 (Phase 6)**: 8 tasks
- **User Story 5 (Phase 7)**: 6 tasks
- **Exit & Polish (Phase 8)**: 7 tasks

**Parallelizable Tasks**: 15 tasks marked with [P]

**MVP Scope**: Phases 1-4 (25 tasks) delivers Add + View functionality

**File Structure**:
- `src/todo_model.py` - 2 tasks (T005-T006)
- `src/todo_manager.py` - 6 tasks (T007, T013, T019, T026, T033, T041)
- `src/todo_app.py` - 35 tasks (main CLI implementation)
- `pyproject.toml` - 1 task (T003)
- `README.md` - 1 task (T004)

---

## Success Criteria Validation

Each user story's tasks satisfy spec requirements:

| User Story | Tasks | Spec Requirements Met |
|------------|-------|----------------------|
| US1: Add | T012-T017 | FR-001, FR-003, FR-005, FR-007, validation, confirmation |
| US2: View | T018-T024 | FR-008, visual indicators, empty state, formatted output |
| US3: Mark Complete | T025-T032 | FR-007, idempotency, error handling, status update |
| US4: Update | T033-T040 | FR-005, FR-007, validation, error handling |
| US5: Delete | T041-T046 | FR-007, permanent removal, error handling |
| Polish | T047-T053 | FR-010 (exit), FR-006 (error messages), edge cases |

All tasks together satisfy:
- ✅ SC-001: Add todo <10 seconds
- ✅ SC-002: View instant display
- ✅ SC-003: 100% CRUD functionality
- ✅ SC-004: Error messages <1 second
- ✅ SC-005: Handle 1000 items
- ✅ SC-006: Clear menu labels
- ✅ SC-007: Readable code (3 modules, clean structure)
