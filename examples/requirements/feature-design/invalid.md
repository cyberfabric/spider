# Feature: Task CRUD

## A. Feature Context

Basic task management.

## C. Algorithms (FDL)

### Validate Task

**ID**: `fdd-taskflow-feature-task-crud-algo-validate`

Check if task is valid.

This is intentionally invalid:
- Section A missing required fields: Feature ID, Status, subsections 1-4
- Missing Section B (Actor Flows)
- Section ordering wrong (jumped from A to C)
- Algorithm ID missing backticks and `- [ ]` checkbox prefix
- Algorithm content missing `<!-- fdd-id-content -->` markers
- Missing Sections D (States), E (Technical Details), F (Requirements), G (Testing)
