# Artifact Changes Proposal

**Artifacts**:
- `architecture/BUSINESS.md`
- `architecture/DESIGN.md`

---

## ADD

**ID**: `fdd-taskflow-actor-admin`

<!-- fdd-id-content -->
**Role**: Manages system settings, user permissions, and workspace configuration.
<!-- fdd-id-content -->

---

## REPLACE

**ID**: `fdd-taskflow-capability-task-mgmt`

<!-- fdd-id-content -->
- Create, edit, and delete tasks
- Assign tasks to team members
- Set due dates and priorities
- **Bulk operations on multiple tasks**
- **Task templates for recurring work**

**Actors**: `fdd-taskflow-actor-member`, `fdd-taskflow-actor-lead`, `fdd-taskflow-actor-admin`
<!-- fdd-id-content -->

---

## REMOVE

**ID**: `fdd-taskflow-usecase-deprecated-workflow`

<!-- fdd-id-content -->
Removed: Legacy workflow replaced by new task assignment flow.
<!-- fdd-id-content -->
