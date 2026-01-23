# ADR-0001: Use PostgreSQL for Task Storage

**Date**: 2025-01-10

**Status**: Accepted

**ADR ID**: `fdd-taskflow-adr-postgres-storage`

## Context and Problem Statement

TaskFlow needs persistent storage for tasks, users, and audit history. We need to choose between SQL and NoSQL databases considering query patterns, data relationships, and team expertise.

## Considered Options

* **PostgreSQL** — Relational database with strong ACID guarantees
* **MongoDB** — Document store with flexible schema
* **SQLite** — Embedded database for simpler deployment

## Decision Outcome

Chosen option: **PostgreSQL**, because:
- Tasks have relational data (users, assignments, comments) that benefit from joins
- Strong consistency needed for status transitions and assignments
- Team has existing PostgreSQL expertise
- Supports JSON columns for flexible metadata if needed later

### Consequences

**Good**:
- ACID transactions ensure data integrity during concurrent updates
- Efficient queries for filtering tasks by status, assignee, due date

**Bad**:
- Requires separate database server (vs embedded SQLite)
- Schema migrations needed for model changes

## Related Design Elements

* `fdd-taskflow-req-task-crud` — Primary requirement for task storage
* `fdd-taskflow-feature-task-crud` — Feature implementing task persistence
