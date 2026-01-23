# Technical Design: {PROJECT_NAME}

## A. Architecture Overview

### Architectural Vision

{2-3 paragraphs describing the technical approach, key architectural decisions, and design philosophy}

### Architecture Layers

<!-- TODO: Add architecture diagram (draw.io, Mermaid, or embedded image) -->

| Layer | Responsibility | Technology |
|-------|---------------|------------|
| Presentation | {description} | {tech} |
| Application | {description} | {tech} |
| Domain | {description} | {tech} |
| Infrastructure | {description} | {tech} |

## B. Requirements & Principles

### B.1: Functional Requirements

#### FR-{NNN}: {Requirement Title}

**ID**: `fdd-{project-name}-req-{requirement-slug}`

<!-- fdd-id-content -->
**Priority**: {HIGH | MEDIUM | LOW}
**Capabilities**: `fdd-{project-name}-capability-{cap1}`, `fdd-{project-name}-capability-{cap2}`
**Use Cases**: `fdd-{project-name}-usecase-{uc1}`
**Actors**: `fdd-{project-name}-actor-{actor1}`, `fdd-{project-name}-actor-{actor2}`

{Description of what the system must do}
<!-- fdd-id-content -->

<!-- TODO: Add more functional requirements as needed -->

### B.2: Design Principles

#### {Principle Name}

**ID**: `fdd-{project-name}-principle-{principle-slug}`

<!-- fdd-id-content -->
**ADRs**: `fdd-{project-name}-adr-{adr-slug}`

{Description of the principle and why it matters}
<!-- fdd-id-content -->

<!-- TODO: Add more design principles as needed -->

### B.3: Constraints

#### {Constraint Name}

**ID**: `fdd-{project-name}-constraint-{constraint-slug}`

<!-- fdd-id-content -->
**ADRs**: `fdd-{project-name}-adr-{adr-slug}`

{Description of the constraint and its impact}
<!-- fdd-id-content -->

<!-- TODO: Add more constraints as needed -->

## C. Technical Architecture

### C.1: Component Model

<!-- TODO: Add component diagram (draw.io, Mermaid, or ASCII) -->

**Components**:
- **{Component 1}**: {Purpose and responsibility}
- **{Component 2}**: {Purpose and responsibility}

**Interactions**:
- {Component 1} → {Component 2}: {Description of interaction}

### C.2: Domain Model

**Technology**: {GTS | JSON Schema | OpenAPI | TypeScript}
**Location**: [{domain-model-file}]({path/to/domain-model})

**Core Entities**:
- [{EntityName}]({path/to/entity.schema}) - {Description}

**Relationships**:
- {Entity1} → {Entity2}: {Relationship description}

### C.3: API Contracts

**Technology**: {REST/OpenAPI | GraphQL | gRPC | CLISPEC}
**Location**: [{api-spec-file}]({path/to/api-spec})

**Endpoints Overview**:
- `{METHOD} {/path}` - {Description}

### C.4: Non-Functional Requirements

#### NFR: Performance

**ID**: `fdd-{project-name}-nfr-performance`

<!-- fdd-id-content -->
- {Performance requirement 1}
<!-- fdd-id-content -->

#### NFR: Scalability

**ID**: `fdd-{project-name}-nfr-scalability`

<!-- fdd-id-content -->
- {Scalability requirement 1}
<!-- fdd-id-content -->

#### NFR: Reliability

**ID**: `fdd-{project-name}-nfr-reliability`

<!-- fdd-id-content -->
- {Reliability requirement 1}
<!-- fdd-id-content -->

#### NFR: Runtime & Operations

**ID**: `fdd-{project-name}-nfr-runtime-operations`

<!-- fdd-id-content -->
- Deployment: {Local CLI | CI | Server | Desktop App}
- Execution context: {Where it runs, constraints}
- Observability: {Logs/metrics}
- Failure modes: {Common failure cases}
<!-- fdd-id-content -->

#### NFR: Security

**ID**: `fdd-{project-name}-nfr-security`

<!-- fdd-id-content -->
- Authentication: {Approach description}
- Authorization: {Approach description}
- Data protection: {Approach description}
- Security boundaries: {Description}
<!-- fdd-id-content -->

## D. Additional Context

<!-- TODO: Add any additional technical context, architect notes, rationale, etc. -->
<!-- This section is optional and not validated by FDD -->
