---
fdd: true
type: requirement
name: Overall Design Structure
version: 1.1
purpose: Define validation rules for DESIGN.md files
---

# Overall Design Structure Requirements

---

## Agent Instructions

**ALWAYS open and follow**: `../workflows/design.md` WHEN executing workflow

**ALWAYS open and follow**: `../templates/DESIGN.template.md` WHEN generating content

**ALWAYS open**: `../examples/requirements/overall-design/valid.md` WHEN reviewing valid artifact structure

**ALWAYS open and follow**: `requirements.md` WHEN extracting shared requirements

---

## Prerequisite Checklist

- [ ] Agent has read and understood this requirement
- [ ] Agent will follow the rules defined here
- [ ] Agent will use template for generation
- [ ] Agent will reference example for structure validation

---

## Overview

**This file defines**: Validation rules (WHAT must be valid)  
**Template defines**: Structure for generation (HOW to create)  
**Workflow defines**: Process (STEP by STEP)

**Size limits**:
- Recommended: ≤1500 lines
- Hard limit: ≤2000 lines

**Related**:
- `business-context-structure.md` — BUSINESS.md structure
- `adr-structure.md` — ADR directory structure

---

## File Overview

**Purpose**: Technical requirements, principles, and architecture

**Location**: `architecture/DESIGN.md`

**Contains**: 
- Section A: Architecture Overview
- Section B: Requirements & Principles
- Section C: Technical Architecture (C.1-C.4)
- Section D: Additional Context (optional)

---

## Content Boundaries

**Should contain**:
- System-level constraints and principles.
- Shared concepts/types/contracts that features must not redefine.
- References to domain model and API contract sources.

**Should not contain**:
- Feature-level flows/algorithms/states (use feature `DESIGN.md`).
- Implementation tasks (use feature `CHANGES.md`).
- Decision rationale debates (use ADRs).

---

## Validation Criteria

### File Validation

1. **File exists**
   - File `architecture/DESIGN.md` exists
   - File contains ≥200 lines (recommended: 500-2000 lines)

### Structure Validation

1. **All required sections present**
   - Section A: Architecture Overview
   - Section B: Requirements & Principles (B.1-B.3)
   - Section C: Technical Architecture (C.1-C.4)
   - Section D: Additional Context (optional)

2. **Section order correct**: A → B → C → D

3. **No prohibited sections**
   - Only A-D allowed at top level
   - Section C has exactly 4 subsections (C.1-C.4)

4. **Headers use proper levels**
   - `##` for sections A-D
   - `###` for subsections B.1-B.3, C.1-C.4
   - Subsection headers MUST use `:` or `.` after the number (examples: `### B.1: Functional Requirements`, `### C.3: API Contracts`)

### Content Boundaries Validation

**Check**:
- [ ] No feature-level flows/algorithms/states are authored here (those belong in feature `DESIGN.md`)
- [ ] No implementation tasks or task breakdowns are authored here (those belong in feature `CHANGES.md`)
- [ ] No ADR-style decision rationale debates are authored here (use ADR files for decision records)

### Section B Subsections

| Subsection | Content | Expected Content |
|------------|---------|------------------|
| B.1 | Functional Requirements | A list of requirement blocks written at overall-system scope (not feature-level FDL). Each requirement MUST have a stable requirement heading and include at least: `**ID**: \`fdd-{project}-req-{name}\`` plus traceability fields (e.g., `**Capabilities**:`, `**Actors**:`, optionally `**Use Cases**:` / `**ADRs**:`). Describe behavior and acceptance intent in plain language; avoid implementation tasks. |
| B.2 | Design Principles | A list of architectural/design principles that shape decisions across the system. Each principle should be expressed as a short rule with rationale and practical implications, and include `**ID**: \`fdd-{project}-principle-{name}\``. Principles should be stable, reusable, and not duplicate constraints or requirements. |
| B.3 | Constraints | A list of hard constraints that limit solution space (regulatory, platform, compatibility, vendor, data residency, legacy integration). Each constraint should include `**ID**: \`fdd-{project}-constraint-{name}\`` and a clear statement of what is NOT allowed / must be adhered to, plus any rationale and verification approach. |

### Section C Subsections

| Subsection | Content | Expected Content |
|------------|---------|------------------|
| C.1 | Component Model | High-level decomposition of the system into components/services/modules with responsibilities, boundaries, and key interactions. Include at least one diagram (image, Mermaid, or ASCII) and describe major data/control flows between components. |
| C.2 | Domain Model | The authoritative domain model: entities/aggregates/value objects and their relationships, core invariants, and how they map to schemas. MUST provide clickable links to machine-readable schema sources (e.g., JSON Schema, TypeScript types, OpenAPI schemas) and indicate where they live in the repo. |
| C.3 | API Contracts | The authoritative API contract surface (external and/or internal). MUST provide clickable links to machine-readable contracts (OpenAPI/CLISPEC/proto/GraphQL). For CLI tools, CLISPEC is the canonical and authoritative interface specification format and MUST be treated as machine-readable by validators and agents. Describe key endpoints/operations, request/response shapes at a high level, error handling expectations, authn/authz entry points, and versioning strategy if applicable. |
| C.4 | Non-Functional Requirements | A consolidated list of NFRs (including security and runtime/operations concerns). Each NFR should be stated as a measurable constraint/target (latency/throughput/SLO, availability, durability, auditability, access control, secrets handling, observability, rollout/rollback, cost). Use stable IDs like `**ID**: \`fdd-{project}-nfr-{name}\`` and link to supporting configs/docs where relevant. |

### Content Validation

1. **Domain Model accessible**
   - Files at specified location exist
   - Files are in machine-readable format (GTS, JSON Schema, OpenAPI, TypeScript)
   - References are clickable Markdown links

2. **API Contracts accessible**
   - Files at specified location exist
   - Files are in machine-readable format (OpenAPI, GraphQL, CLISPEC, proto)
   - For CLI tools, CLISPEC is the canonical machine-readable format and MUST be accepted as authoritative
   - References are clickable Markdown links

3. **Component diagram present**
   - At least one diagram in Section C.1
   - Can be embedded image, Mermaid code, or ASCII art

---

## FDD ID Format Validation

| ID Type | Format | Example |
|---------|--------|---------|
| Requirement | `fdd-{project}-req-{name}` | `fdd-analytics-req-multi-tenant` |
| NFR | `fdd-{project}-nfr-{name}` | `fdd-analytics-nfr-performance` |
| Principle | `fdd-{project}-principle-{name}` | `fdd-analytics-principle-plugin-based` |
| Constraint | `fdd-{project}-constraint-{name}` | `fdd-analytics-constraint-api-dep` |
| ADR | `fdd-{project}-adr-{name}` | `fdd-analytics-adr-event-sourcing` |

**ID Rules**:
- All IDs wrapped in backticks
- Names in kebab-case (2-4 words)
- Unique within their section
- `**ID**:` line MUST be first non-empty line after heading

---

## Traceability Field Requirements

Each Functional Requirement (FR) MUST include:

| Field | Format | Mandatory |
|-------|--------|-----------|
| **Capabilities** | `**Capabilities**: \`{cap-id}\`` | YES |
| **Actors** | `**Actors**: \`{actor-id}\`` | YES |
| **Use Cases** | `**Use Cases**: \`{uc-id}\`` | If applicable |
| **ADRs** | `**ADRs**: \`{adr-id}\`` | If applicable |

---

## Cross-Reference Validation

### BUSINESS.md → DESIGN.md Traceability

1. **Capability Coverage (MANDATORY)**
   - Every capability ID from BUSINESS.md Section C MUST be referenced
   - No orphaned capabilities

2. **Use Case Coverage (MANDATORY)**
   - Every use case ID from BUSINESS.md Section D MUST be referenced
   - No orphaned use cases

3. **Actor References (MANDATORY)**
   - Every FR MUST have `**Actors**:` field
   - Actor IDs MUST match capability actors from BUSINESS.md

4. **ADR Coverage (MANDATORY)**
   - All ADRs from `architecture/ADR/` MUST appear in at least one DESIGN.md requirement
   - No orphaned ADRs

### Validation Checks

- Every capability ID from BUSINESS.md appears in FR `**Capabilities**` field
- Every use case ID from BUSINESS.md appears in FR `**Use Cases**` field
- Every FR has Capabilities and Actors fields
- All referenced IDs are valid (exist in source documents)
- All ADRs from `architecture/ADR/` are referenced

---

## Scoring

| Category | Points |
|----------|--------|
| Structure | 30 |
| Domain Model | 25 |
| API Contracts | 25 |
| Content Quality | 20 |
| **Total** | **100** |

**Penalties**:
- Missing capability coverage: **-15 points** per orphaned capability
- Missing use case coverage: **-15 points** per orphaned use case
- Orphaned ADR: **-15 points** per ADR
- Missing Capabilities/Actors field: **-10 points** per FR
- Invalid ID reference: **-5 points** per invalid ID

---

## Common Issues

- Missing required top-level sections (A/B/C)
- Missing required C.1-C.4 subsections
- Missing functional requirement IDs
- Orphaned capabilities/use cases (not referenced in DESIGN.md)
- Domain model/API references not clickable links

---

## Validation Checklist (Final)

- [ ] Document follows required structure
- [ ] All validation criteria pass
- [ ] All traceability rules satisfied
- [ ] Agent used template for generation
- [ ] Agent referenced example for validation

---

## References

**Template**: `../templates/DESIGN.template.md`

**Example**: `../examples/requirements/overall-design/valid.md`

**Related**:
- `business-context-structure.md` — BUSINESS.md structure
- `adr-structure.md` — ADR directory structure
- `feature-design-structure.md` — Feature DESIGN.md structure
