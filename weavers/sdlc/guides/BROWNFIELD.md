# Brownfield Guide

Use this guide when you already have a codebase and want to adopt Spaider.

All prompts work through the `spaider` skill — enable it with `spaider on` and use natural language prompts.

## Goal

Adopt Spaider incrementally — start with what makes sense for your project, not a fixed sequence.

## Key Principle: Start Anywhere

Unlike greenfield projects, **brownfield has no required order**. You can:

- Start with **any artifact** — PRD, DESIGN, SPEC, or even just CODE
- Work **top-down** (PRD → DESIGN → CODE) or **bottom-up** (CODE → SPEC → DESIGN)
- Adopt **incrementally** — use only what you need, add more later
- Use **code-only mode** — just Spaider's code generation with checklist benefits

**Even with zero artifacts**, Spaider's code generation uses the `code-checklist` internally for quality guidance.

---

## Adoption Scenarios

### Scenario A: Code-Only

You just want better code generation. No artifacts needed.

| Prompt | What happens |
|--------|--------------|
| `spaider implement spec auth` | Generates code using code-checklist quality guidance |
| `spaider add markers to src/auth/` | Adds traceability markers to existing code |
| `spaider validate code` | Validates code quality and marker correctness |

**Benefits**: Quality-guided code generation, consistent patterns, marker-based traceability.

### Scenario B: Spec-First (Bottom-Up)

You want to document existing specs, then build up.

```
1. spaider reverse SPEC from src/auth/     → Creates SPEC spec from code
2. spaider reverse SPEC from src/billing/  → Creates another SPEC spec
3. spaider decompose from specs            → Creates DECOMPOSITION from SPECs
4. spaider make DESIGN from DECOMPOSITION     → Creates DESIGN from structure
5. spaider make PRD from DESIGN               → (optional) Creates PRD from DESIGN
```

**When to use**: You want to document what exists without changing code.

### Scenario C: Design-First (Middle-Out)

You want to capture architecture, then decompose into specs.

```
1. spaider reverse DESIGN from codebase       → Extracts architecture from code
2. spaider decompose                          → Creates spec breakdown
3. spaider make SPEC for {slug}            → Creates detailed specs
4. spaider implement {slug}                   → Implements with markers
```

**When to use**: You want architectural control before spec work.

### Scenario D: Full Top-Down

You want complete documentation from requirements to code.

```
1. spaider reverse PRD from codebase          → Extracts requirements
2. spaider make DESIGN from PRD               → Creates architecture
3. spaider decompose                          → Creates spec breakdown
4. spaider make SPEC for {slug}            → Creates detailed specs
5. spaider implement {slug}                   → Implements with markers
```

**When to use**: New team members, compliance requirements, or major refactoring.

### Scenario E: Gradual Adoption

Start minimal, add artifacts as needed.

```
Week 1: spaider implement {slug}              → Code-only, with checklist
Week 2: spaider make SPEC for {slug}       → Add specs for complex specs
Week 3: spaider decompose                     → Organize specs
Later:  spaider make DESIGN                   → Document architecture
```

**When to use**: You want low-friction adoption with growing benefits.

---

## What You Will Produce

Spaider artifacts registered in `.spaider-adapter/artifacts.json` ([taxonomy](TAXONOMY.md)):

| Artifact | Default Location |
|----------|------------------|
| PRD | `architecture/PRD.md` |
| ADR | `architecture/ADR/*.md` |
| DESIGN | `architecture/DESIGN.md` |
| DECOMPOSITION | `architecture/DECOMPOSITION.md` |
| SPEC | `architecture/specs/{slug}.md` |

## How to Provide Context

Brownfield work is context-heavy. Add context to control what the agent reads and how it maps existing reality into Spaider artifacts.

Recommended context:
- Source of truth (code vs docs)
- Existing code entry points (directories, modules)
- Existing docs you trust (paths)
- Constraints and invariants you must preserve

**Example format:**
```
spaider make DESIGN
Context:
- Source of truth: code
- Code areas: src/api/, src/domain/
- Existing docs: docs/architecture.md (may be outdated)
- Constraints: do not break public API
```

The agent will read inputs, ask targeted questions, propose answers, and produce artifacts.

---

## Workflow: Create Baseline

Goal: produce validated baseline artifacts before you add or refactor specs.

### 1. PRD

**Reverse-engineer from code**

| Prompt | What happens |
|--------|--------------|
| `spaider reverse PRD from codebase` | Extracts requirements from existing code |
| `spaider reverse PRD from src/` | Extracts from specific directory |
| `spaider make PRD from code` | Same, alternative phrasing |

**Create from existing docs**

| Prompt | What happens |
|--------|--------------|
| `spaider make PRD from README` | Creates PRD from project README |
| `spaider make PRD from docs/requirements.txt` | Extracts from existing requirements |
| `spaider make PRD from this conversation` | Creates PRD from stakeholder discussion |
| `spaider import user-stories.md as PRD` | Converts user stories to PRD |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spaider update PRD` | Updates PRD interactively |
| `spaider extend PRD with {capability}` | Adds capability to existing PRD |
| `spaider sync PRD from code` | Updates PRD to match current code |

**Provide context:** source of truth, code entry points, existing docs.

**Example:**
```
spaider reverse PRD from codebase
Context:
- Source of truth: code
- Code entry points: src/routes/, src/controllers/
- Existing docs: docs/api.md (partial)
```

### 2. Validate PRD

| Prompt | What happens |
|--------|--------------|
| `spaider validate PRD` | Full validation (300+ criteria) |
| `spaider validate PRD semantic` | Semantic only (content quality) |
| `spaider validate PRD structural` | Structural only (format, IDs) |
| `spaider validate PRD quick` | Fast check (critical issues) |

### 3. ADR + DESIGN

**Reverse-engineer DESIGN**

| Prompt | What happens |
|--------|--------------|
| `spaider reverse DESIGN from codebase` | Documents current architecture from code |
| `spaider reverse DESIGN from src/` | From specific directory |
| `spaider make DESIGN from code` | Same, alternative phrasing |

**Create from existing docs**

| Prompt | What happens |
|--------|--------------|
| `spaider make DESIGN from PRD` | Transforms PRD into architecture |
| `spaider import OpenAPI as DESIGN` | Converts API spec into DESIGN |
| `spaider import db-schema.sql as DESIGN data model` | Extracts data model from SQL |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spaider update DESIGN` | Updates DESIGN interactively |
| `spaider extend DESIGN with {component}` | Adds component to DESIGN |
| `spaider sync DESIGN from code` | Updates DESIGN to match current code |

**ADR**

| Prompt | What happens |
|--------|--------------|
| `spaider make ADR for PostgreSQL` | Creates ADR for technology choice |
| `spaider make ADR for REST vs GraphQL` | Creates ADR comparing approaches |
| `spaider draft ADR from discussion` | Extracts decision from conversation |
| `spaider update ADR 0001` | Updates specific ADR |

**Provide context:** source of truth, existing specs, constraints.

**Example:**
```
spaider reverse DESIGN from codebase
Context:
- Source of truth: code
- Existing specs: docs/openapi.yaml, docs/db-schema.md
- Constraints: do not break public API
```

### 4. Validate DESIGN + ADR

| Prompt | What happens |
|--------|--------------|
| `spaider validate DESIGN` | Full validation (380+ criteria) |
| `spaider validate DESIGN semantic` | Semantic only (consistency) |
| `spaider validate DESIGN structural` | Structural only (format) |
| `spaider validate DESIGN refs` | Cross-references to PRD |
| `spaider validate ADR` | Validates all ADRs |
| `spaider validate ADR 0001` | Validates specific ADR |
| `spaider validate ADR semantic` | Semantic only (rationale quality) |

### 5. DECOMPOSITION

**Create**

| Prompt | What happens |
|--------|--------------|
| `spaider decompose` | Creates DECOMPOSITION interactively |
| `spaider decompose from codebase` | Extracts specs from existing code structure |
| `spaider decompose by module` | Groups by code modules |
| `spaider decompose by capability` | Groups by business capability |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spaider add spec {slug}` | Adds new spec entry |
| `spaider update spec {slug} status` | Updates spec status |
| `spaider update spec {slug} priority` | Updates spec priority |

**Provide context:** module boundaries, spec grouping preferences.

**Example:**
```
spaider decompose from codebase
Context:
- Group specs by modules: billing, auth, reporting
- Code structure: src/modules/
```

### 6. Validate DECOMPOSITION

| Prompt | What happens |
|--------|--------------|
| `spaider validate DECOMPOSITION` | Full validation (130+ criteria) |
| `spaider validate DECOMPOSITION semantic` | Semantic only (coverage) |
| `spaider validate DECOMPOSITION structural` | Structural only (format) |
| `spaider validate DECOMPOSITION refs` | Cross-references to DESIGN |

---

## Workflow: Add a New Spec

Use when baseline exists and you want to add a new capability.

### 1. Add to DECOMPOSITION

| Prompt | What happens |
|--------|--------------|
| `spaider add spec {slug}` | Adds new spec to decomposition |
| `spaider add spec notifications` | Example: adds notifications spec |

### 2. SPEC spec

**Create**

| Prompt | What happens |
|--------|--------------|
| `spaider make SPEC for {slug}` | Creates spec spec |
| `spaider make SPEC spec for notifications` | Creates detailed design |

**Reverse-engineer from existing code**

| Prompt | What happens |
|--------|--------------|
| `spaider reverse SPEC from src/notifications/` | Creates spec from existing code |
| `spaider reverse SPEC {slug} from code` | Same, using spec slug |
| `spaider draft SPEC from code` | Same, alternative phrasing |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spaider update SPEC {slug}` | Updates spec spec |
| `spaider extend SPEC {slug} with {scenario}` | Adds scenario to spec |
| `spaider sync SPEC {slug} from code` | Updates spec to match code |

**Provide context:** spec slug, code boundaries, scenarios to include.

**Example:**
```
spaider make SPEC for notifications
Context:
- Include scenarios: retries, rate limits, provider outage
- Code boundaries: src/notifications/
```

### 3. Validate SPEC

| Prompt | What happens |
|--------|--------------|
| `spaider validate SPEC {slug}` | Full validation (380+ criteria) |
| `spaider validate SPEC {slug} semantic` | Semantic only (flows, edge cases) |
| `spaider validate SPEC {slug} structural` | Structural only (SDSL, IDs) |
| `spaider validate SPEC {slug} refs` | Cross-references to DESIGN |

### 4. CODE

**Implement from scratch**

| Prompt | What happens |
|--------|--------------|
| `spaider implement {slug}` | Generates code from SPEC spec |
| `spaider implement {slug} step by step` | Implements with user confirmation |
| `spaider implement {slug} tests first` | Generates tests first, then code |

**Implement specific parts**

| Prompt | What happens |
|--------|--------------|
| `spaider implement {slug} flow {flow-id}` | Implements specific flow only |
| `spaider implement {slug} api` | Implements API layer only |
| `spaider implement {slug} data layer` | Implements data/repository layer only |
| `spaider implement {slug} tests` | Generates tests only |

**Continue / update**

| Prompt | What happens |
|--------|--------------|
| `spaider continue implementing {slug}` | Continues partial implementation |
| `spaider implement {slug} remaining` | Implements only unimplemented parts |
| `spaider sync code with SPEC {slug}` | Updates code to match SPEC changes |

**Add markers to existing code**

| Prompt | What happens |
|--------|--------------|
| `spaider add markers to {path}` | Adds `@spaider-*` markers to existing code |
| `spaider add markers for {slug}` | Adds markers matching SPEC spec |
| `spaider fix markers in {path}` | Fixes incorrect/incomplete markers |

**Provide context:** spec slug, code paths.

**Example:**
```
spaider implement notifications
Context:
- Where to implement: src/notifications/
```

### 5. Validate Code

**Full validation**

| Prompt | What happens |
|--------|--------------|
| `spaider validate code` | Validates all code markers |
| `spaider validate code for {slug}` | Validates specific spec |
| `spaider validate code in {path}` | Validates code in specific path |

**Coverage**

| Prompt | What happens |
|--------|--------------|
| `spaider validate code coverage` | Reports implementation coverage % |
| `spaider validate code coverage for {slug}` | Coverage for specific spec |
| `spaider show uncovered flows` | Lists flows without implementation |
| `spaider show uncovered algorithms` | Lists algorithms without implementation |

**Traceability**

| Prompt | What happens |
|--------|--------------|
| `spaider validate code orphans` | Finds markers referencing non-existent IDs |
| `spaider validate code refs` | Validates all marker references |
| `spaider validate code markers` | Checks marker format correctness |
| `spaider list code markers` | Lists all markers in codebase |
| `spaider list code markers for {slug}` | Lists markers for specific spec |

**Consistency**

| Prompt | What happens |
|--------|--------------|
| `spaider compare code to SPEC {slug}` | Shows drift between code and spec |
| `spaider validate code consistency` | Checks code matches SPEC specs |
| `spaider find missing implementations` | Lists SPEC elements without code |

---

## Sync and Compare

When code and design drift apart:

| Prompt | What happens |
|--------|--------------|
| `spaider compare DESIGN to code` | Shows drift between design and implementation |
| `spaider compare SPEC {slug} to code` | Shows drift for specific spec |
| `spaider sync DESIGN from code` | Updates DESIGN to match current code |
| `spaider sync SPEC {slug} from code` | Updates SPEC to match current code |
| `spaider sync code with SPEC {slug}` | Updates code to match SPEC |
| `spaider diff SPEC {slug}` | Shows changes since last validation |

---

## Common Scenarios

### Requirements Changed

```
spaider update PRD
spaider validate PRD
spaider propagate PRD changes to DESIGN
spaider validate DESIGN
```

### Design Changed

```
spaider update DESIGN
spaider validate DESIGN
spaider propagate DESIGN changes to SPEC {slug}
spaider validate SPEC {slug}
```

### Spec Design Changed

```
spaider update SPEC {slug}
spaider validate SPEC {slug}
spaider sync code with SPEC {slug}
spaider validate code for {slug}
```

### Code Changed Without Design Update

```
spaider compare SPEC {slug} to code
spaider sync SPEC {slug} from code
spaider validate SPEC {slug}
```

---

## Quick Reference

### By Adoption Level

| Level | What you do | Benefits |
|-------|-------------|----------|
| **Code-only** | `spaider implement {slug}` | Code checklist, consistent patterns |
| **+ SPEC** | Add `spaider make SPEC` | Flows, algorithms, edge cases documented |
| **+ DECOMPOSITION** | Add `spaider decompose` | Spec organization, dependencies |
| **+ DESIGN** | Add `spaider make DESIGN` | Architecture, components, data model |
| **+ PRD** | Add `spaider make PRD` | Requirements, actors, full traceability |

### Top-Down (Full)

| Step | Generate | Validate |
|------|----------|----------|
| 1 | `spaider reverse PRD from codebase` | `spaider validate PRD` |
| 2 | `spaider reverse DESIGN from codebase` | `spaider validate DESIGN` |
| 3 | `spaider decompose` | `spaider validate DECOMPOSITION` |
| 4 | `spaider make SPEC for {slug}` | `spaider validate SPEC {slug}` |
| 5 | `spaider implement {slug}` | `spaider validate code for {slug}` |

### Bottom-Up (Spec-First)

| Step | Generate | Validate |
|------|----------|----------|
| 1 | `spaider reverse SPEC from src/{path}/` | `spaider validate SPEC {slug}` |
| 2 | `spaider decompose from specs` | `spaider validate DECOMPOSITION` |
| 3 | `spaider make DESIGN from DECOMPOSITION` | `spaider validate DESIGN` |

### Code-Only

| Prompt | What happens |
|--------|--------------|
| `spaider implement {slug}` | Generates code with checklist guidance |
| `spaider add markers to {path}` | Adds traceability to existing code |
| `spaider validate code` | Validates code quality |

**Validation modes** (append to any `validate` command):
- `semantic` — content quality, completeness, clarity
- `structural` — format, IDs, template compliance
- `refs` — cross-references to other artifacts
- `quick` — critical issues only (fast)

## Iteration Rules

- Start with what you need — add more artifacts as value becomes clear
- If code changes affect spec behavior, update SPEC first
- Re-validate the SPEC design
- Run `spaider validate code` to ensure design and code remain consistent
- If code contradicts design, decide: update design OR update code
