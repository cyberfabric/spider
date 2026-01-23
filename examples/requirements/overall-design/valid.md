# Technical Design: TaskFlow

## A. Architecture Overview

TaskFlow uses a layered architecture: React SPA frontend, Node.js REST API, PostgreSQL database. WebSocket connections enable real-time updates.

## B. Requirements & Principles

### B.1: Functional Requirements

#### FR-001: Task CRUD Operations

**ID**: `fdd-taskflow-req-task-crud`

<!-- fdd-id-content -->
**Priority**: HIGH
**Capabilities**: `fdd-taskflow-capability-task-mgmt`
**Use Cases**: `fdd-taskflow-usecase-create-task`
**Actors**: `fdd-taskflow-actor-member`, `fdd-taskflow-actor-lead`
**ADRs**: `fdd-taskflow-adr-postgres-storage`

Users can create, read, update, and delete tasks. Each task has title, description, assignee, due date, priority, and status.
<!-- fdd-id-content -->

#### FR-002: Real-time Notifications

**ID**: `fdd-taskflow-req-notifications`

<!-- fdd-id-content -->
**Priority**: MEDIUM
**Capabilities**: `fdd-taskflow-capability-notifications`
**Use Cases**: `fdd-taskflow-usecase-create-task`
**Actors**: `fdd-taskflow-actor-notifier`

System sends push notifications on task assignment and email alerts for overdue tasks.
<!-- fdd-id-content -->

### B.2: Design Principles

#### Real-time First

**ID**: `fdd-taskflow-principle-realtime-first`

<!-- fdd-id-content -->
**ADRs**: `fdd-taskflow-adr-postgres-storage`

Prefer architectures that keep task state and notifications consistent and observable for all users.
<!-- fdd-id-content -->

#### Simplicity over Features

**ID**: `fdd-taskflow-principle-simplicity-over-features`

<!-- fdd-id-content -->
**ADRs**: `fdd-taskflow-adr-postgres-storage`

Simplicity is preferred over features.
<!-- fdd-id-content -->

#### Mobile-first Responsive Design

**ID**: `fdd-taskflow-principle-mobile-first`

<!-- fdd-id-content -->
**ADRs**: `fdd-taskflow-adr-postgres-storage`

Design for mobile devices first.
<!-- fdd-id-content -->

### B.3: Constraints

#### Supported Platforms

**ID**: `fdd-taskflow-constraint-supported-platforms`

<!-- fdd-id-content -->
**ADRs**: `fdd-taskflow-adr-postgres-storage`

Must run on Node.js 18+. PostgreSQL 14+ required. Browser support: last 2 versions.
<!-- fdd-id-content -->

## C. Technical Architecture

### C.1: Component Model

```
[React SPA] <--REST/WS--> [API Server] <---> [PostgreSQL]
                              |
                         [Redis PubSub]
```

### C.2: Domain Model

**Technology**: TypeScript
**Location**: [domain-model.ts](domain-model.ts)

- **Task**: id, title, description, status, priority, dueDate, assigneeId, createdBy
- **User**: id, email, name, role (MEMBER | LEAD)

### C.3: API Contracts

**Technology**: REST/OpenAPI
**Location**: [openapi.yaml](openapi.yaml)

- `POST /api/tasks` - Create task
- `GET /api/tasks` - List tasks with filters
- `PATCH /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task

### C.4: Non-Functional Requirements

#### NFR: Performance & Reliability

**ID**: `fdd-taskflow-nfr-performance-reliability`

<!-- fdd-id-content -->
- Response time <200ms for API calls
- Support 100 concurrent users
- 99.9% uptime SLA
<!-- fdd-id-content -->

#### NFR: Runtime & Operations

**ID**: `fdd-taskflow-nfr-runtime-operations`

<!-- fdd-id-content -->
- Node.js API server (Express)
- Background worker for email notifications
<!-- fdd-id-content -->

#### NFR: Security

**ID**: `fdd-taskflow-nfr-security`

<!-- fdd-id-content -->
- JWT-based authentication
- Role-based access (MEMBER, LEAD)
<!-- fdd-id-content -->
