# Implementation Plan: Task CRUD

**Feature**: `task-crud`

**Version**: 1.0

**Last Updated**: 2025-01-15

**Status**: 🔄 IN_PROGRESS

**Feature DESIGN**: [DESIGN.md](DESIGN.md)

---

## Summary

**Total Changes**: 2

**Completed**: 1

**In Progress**: 1

**Not Started**: 0

**Estimated Effort**: 5 story points

---

## Change 1: Task API Endpoints

**ID**: `fdd-taskflow-feature-task-crud-change-api`

<!-- fdd-id-content -->
**Status**: ✅ COMPLETED

**Priority**: HIGH

**Effort**: 3 story points

**Implements**: `fdd-taskflow-feature-task-crud-req-create`

**Phases**: `ph-1`

### Objective

Implement REST API endpoints for task CRUD operations.

### Requirements Coverage

**Implements**:
- **`fdd-taskflow-feature-task-crud-req-create`**: Task creation with validation

**References**:
- Actor Flow: `fdd-taskflow-feature-task-crud-flow-create`
- Algorithm: `fdd-taskflow-feature-task-crud-algo-validate`

### Tasks

- [x] 1.1 Create `Task` model in `src/models/task.ts` - validate: model exists
- [x] 1.2 Add POST `/api/tasks` endpoint - validate: returns 201
- [x] 1.3 Add GET `/api/tasks` with filters - validate: returns task list
- [x] 1.4 Add PATCH `/api/tasks/:id` endpoint - validate: returns updated task

### Specification

**Domain Model Changes**:
- Type: `Task { id, title, description, status, priority, dueDate, assigneeId }`

**API Changes**:
- `POST /api/tasks` - Create task
- `GET /api/tasks?status=&assignee=` - List with filters
- `PATCH /api/tasks/:id` - Update task

**Database Changes**:
- Table: `tasks` with columns matching Task model

**Code Changes**:
- **Code Tagging**: MUST wrap code with `@fdd-change:fdd-taskflow-feature-task-crud-change-api:ph-1` comment

### Dependencies

**Depends on**: None

**Blocks**: `fdd-taskflow-feature-task-crud-change-status`

### Testing

**Unit Tests**:
- `task.model.test.ts` - validation logic
**Integration Tests**:
- `task.api.test.ts` - endpoint responses

### Validation Criteria

- [ ] POST `/api/tasks` returns 201 with created task
- [ ] GET `/api/tasks` supports basic filtering
- [ ] PATCH `/api/tasks/:id` rejects invalid payloads
<!-- fdd-id-content -->

---

## Change 2: Status Transitions

**ID**: `fdd-taskflow-feature-task-crud-change-status`

<!-- fdd-id-content -->
**Status**: 🔄 IN_PROGRESS

**Priority**: MEDIUM

**Effort**: 2 story points

**Implements**: `fdd-taskflow-feature-task-crud-req-create`

**Phases**: `ph-1`, `ph-2`

### Objective

Implement task status state machine (BACKLOG → IN_PROGRESS → DONE).

### Requirements Coverage

**Implements**:
- **`fdd-taskflow-feature-task-crud-req-create`**: Status transitions

**References**:
- State: `fdd-taskflow-feature-task-crud-state-status`

### Tasks

- [x] 2.1 Add status enum to `src/models/task.ts` - validate: enum defined
- [ ] 2.2 Implement transition validation in `src/services/task.ts` - validate: invalid transitions rejected
- [ ] 2.3 Add PATCH `/api/tasks/:id/status` endpoint - validate: returns 200

### Specification

**Domain Model Changes**:
- Enum: `TaskStatus { BACKLOG, IN_PROGRESS, DONE }`

**API Changes**:
- `PATCH /api/tasks/:id/status` - Transition status

**Database Changes**:
- Column: `status` enum in `tasks` table

**Code Changes**:
- **Code Tagging**: MUST wrap code with `@fdd-change:fdd-taskflow-feature-task-crud-change-status:ph-1` comment

### Dependencies

**Depends on**: `fdd-taskflow-feature-task-crud-change-api`

**Blocks**: None

### Testing

**Unit Tests**:
- `task.status.test.ts` - transition validation

### Validation Criteria

- [ ] Status enum defined in Task model
- [ ] Invalid transitions return 400 error
- [ ] Valid transitions update task and return 200
<!-- fdd-id-content -->
