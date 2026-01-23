# Feature: Task CRUD

## A. Feature Context

**Feature ID**: `fdd-taskflow-feature-task-crud`
**Status**: IN_PROGRESS

### 1. Overview
Core task management functionality for creating, viewing, updating, and deleting tasks.
### 2. Purpose
Enable team members to manage their work items with full lifecycle tracking.
### 3. Actors
- `fdd-taskflow-actor-member`
- `fdd-taskflow-actor-lead`
### 4. References
- Overall Design: [DESIGN](../../DESIGN.md)

## B. Actor Flows (FDL)
### Create Task

- [ ] **ID**: `fdd-taskflow-feature-task-crud-flow-create`

<!-- fdd-id-content -->
1. [x] - `ph-1` - User fills task form (title, description, priority) - `inst-fill-form`
2. [x] - `ph-1` - System validates required fields - `inst-validate`
3. [ ] - `ph-2` - User optionally assigns to team member - `inst-assign`
4. [x] - `ph-1` - System saves task with status BACKLOG - `inst-save`
<!-- fdd-id-content -->

## C. Algorithms (FDL)
### Validate Task

- [x] **ID**: `fdd-taskflow-feature-task-crud-algo-validate`

<!-- fdd-id-content -->
1. [x] - `ph-1` - **IF** title is empty **RETURN** error "Title required" - `inst-check-title`
2. [x] - `ph-1` - **IF** priority not in [LOW, MEDIUM, HIGH] **RETURN** error - `inst-check-priority`
3. [x] - `ph-1` - **RETURN** valid - `inst-return-valid`
<!-- fdd-id-content -->

## D. States (FDL)
### Task Status

- [ ] **ID**: `fdd-taskflow-feature-task-crud-state-status`

<!-- fdd-id-content -->
1. [x] - `ph-1` - **FROM** BACKLOG **TO** IN_PROGRESS **WHEN** user starts work - `inst-start`
2. [ ] - `ph-2` - **FROM** IN_PROGRESS **TO** DONE **WHEN** user completes - `inst-complete`
3. [ ] - `ph-2` - **FROM** DONE **TO** BACKLOG **WHEN** user reopens - `inst-reopen`
<!-- fdd-id-content -->

## E. Technical Details
- API: REST endpoints at `/api/tasks`
- Storage: PostgreSQL `tasks` table
- Validation: Server-side with Zod schemas

## F. Requirements
### Task Creation

- [ ] **ID**: `fdd-taskflow-feature-task-crud-req-create`

<!-- fdd-id-content -->
**Status**: 🔄 IN_PROGRESS
**Description**: Users can create tasks with title, description, priority, and due date.
**References**:
- [Create Task](#create-task)
**Implements**:
- `fdd-taskflow-feature-task-crud-flow-create`
- `fdd-taskflow-feature-task-crud-algo-validate`
**Phases**:
- [x] `ph-1`: basic creation
- [ ] `ph-2`: assignment support
**Tests Covered**:
- `fdd-taskflow-feature-task-crud-test-create`
**Acceptance Criteria**:
- Task saved with all required fields
- Validation errors shown for invalid input
<!-- fdd-id-content -->

## G. Testing Scenarios
### Create Task Validation

- [x] **ID**: `fdd-taskflow-feature-task-crud-test-create`

<!-- fdd-id-content -->
**Validates**: `fdd-taskflow-feature-task-crud-req-create`
1. [x] - `ph-1` - Submit form with valid data, verify task created - `inst-valid-create`
2. [x] - `ph-1` - Submit empty title, verify error message - `inst-empty-title`
<!-- fdd-id-content -->
