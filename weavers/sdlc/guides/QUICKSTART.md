# Spaider SDLC Quick Start

**Learn Spaider SDLC in 10 minutes with real prompts and examples**

Spaider SDLC works through the `spaider` skill — enable it with `spaider on` and use natural language prompts prefixed with `spaider`. The skill handles artifact discovery, template loading, validation, and traceability automatically.

---

## What You'll Learn

1. **Exact prompts to type** — copy-paste into your AI chat
2. **Complete pipeline** — from requirements to validated code
3. **Reverse engineering** — create artifacts from existing code
4. **Working with existing docs** — import what you already have

---

## The Pipeline

Spaider SDLC = **Design First, Code Second**

```mermaid
flowchart LR
    PRD["**PRD**<br/>300+ criteria"]
    ADR["**ADR**<br/>270+ criteria"]
    DESIGN["**DESIGN**<br/>380+ criteria"]
    DECOMP["**DECOMPOSITION**<br/>130+ criteria"]
    SPEC["**SPEC**<br/>380+ criteria"]
    CODE["**CODE**<br/>200+ criteria"]

    PRD --> ADR --> DESIGN --> DECOMP --> SPEC --> CODE
```

| Artifact | Purpose |
|----------|---------|
| **PRD** | Product requirements — actors, capabilities, requirements, use cases, constraints |
| **ADR** | Architecture Decision Record — context, options, decision, consequences |
| **DESIGN** | Technical architecture — components, interfaces, data models, sequences |
| **DECOMPOSITION** | Spec breakdown — ordered implementation units with dependencies |
| **SPEC** | Spec acceptance criteria, flows, algorithms, edge cases, definitions of done |
| **CODE** | Implementation — tagged with `@spaider-*` markers for traceability |

**Key principle**: If code contradicts design, fix design first, then regenerate code.

Learn what each artifact means: [TAXONOMY.md](TAXONOMY.md)

---

## Getting Started

| Prompt | What happens |
|--------|--------------|
| `spaider on` | Enables Spaider mode, discovers adapter, loads project context |
| `spaider init` | Creates `.spaider-adapter/` with `artifacts.json` and domain specs |
| `spaider show pipeline` | Displays current artifact hierarchy and validation status |

**Customizing artifact locations:**

| Prompt | What happens |
|--------|--------------|
| `spaider set artifacts_dir to docs/design/` | Changes default base directory for new artifacts |
| `spaider register PRD at specs/product-requirements.md` | Registers existing file as PRD artifact |
| `spaider move PRD to docs/requirements/PRD.md` | Moves artifact and updates registry |
| `spaider show artifact locations` | Displays current paths from `artifacts.json` |

---

## Example Prompts — Greenfield Project

**PRD — Product Requirements**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider make PRD` | Generates PRD interactively, asking for context |
| `spaider make PRD for task management API` | Generates PRD with actors, requirements, flows |
| `spaider draft PRD from README` | Creates PRD draft from existing README |
| `spaider extend PRD with notifications` | Adds new capability to existing PRD |
| `spaider validate PRD` | Full validation (300+ criteria) |
| `spaider validate PRD semantic` | Semantic validation only (completeness, clarity) |
| `spaider validate PRD structural` | Structural validation only (format, IDs, template) |
| `spaider validate PRD refs` | Check cross-references to other artifacts |

**ADR — Architecture Decision Records**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider make ADR for PostgreSQL` | Creates ADR for technology choice |
| `spaider make ADR for REST vs GraphQL` | Creates ADR comparing approaches |
| `spaider draft ADR from discussion` | Extracts decision from conversation |
| `spaider list ADRs` | Shows all ADRs with status |
| `spaider validate ADR` | Validates all ADRs (270+ criteria each) |
| `spaider validate ADR 0001` | Validates specific ADR by number |
| `spaider validate ADR semantic` | Semantic validation (rationale quality) |
| `spaider validate ADR structural` | Structural validation (format, sections) |

**DESIGN — Technical Architecture**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider make DESIGN` | Creates DESIGN from PRD interactively |
| `spaider make DESIGN from PRD` | Transforms PRD into architecture |
| `spaider extend DESIGN with caching layer` | Adds new component to existing DESIGN |
| `spaider update DESIGN components` | Updates component section |
| `spaider validate DESIGN` | Full validation (380+ criteria) |
| `spaider validate DESIGN semantic` | Semantic validation (consistency, completeness) |
| `spaider validate DESIGN structural` | Structural validation (format, IDs) |
| `spaider validate DESIGN refs` | Check references to PRD/ADR |

**DECOMPOSITION — Spec Breakdown**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider decompose` | Creates DECOMPOSITION interactively |
| `spaider decompose into specs` | Creates ordered spec list with dependencies |
| `spaider decompose by capability` | Groups specs by business capability |
| `spaider decompose by layer` | Groups specs by technical layer |
| `spaider add spec to decomposition` | Adds new spec entry |
| `spaider validate DECOMPOSITION` | Full validation (130+ criteria) |
| `spaider validate DECOMPOSITION semantic` | Semantic validation (coverage, dependencies) |
| `spaider validate DECOMPOSITION structural` | Structural validation (format, IDs) |

**SPEC — Spec Specification**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider make SPEC for auth` | Creates spec spec for auth |
| `spaider make SPEC spec for task-crud` | Creates detailed spec design |
| `spaider draft SPEC from code` | Reverse-engineers spec from implementation |
| `spaider extend SPEC auth with MFA` | Adds scenario to existing spec |
| `spaider validate SPEC auth` | Full validation (380+ criteria) |
| `spaider validate SPEC auth semantic` | Semantic validation (flows, edge cases) |
| `spaider validate SPEC auth structural` | Structural validation (SDSL format, IDs) |
| `spaider validate SPEC auth refs` | Check references to DESIGN/DECOMPOSITION |

**CODE — Implementation**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider implement {slug}` | Generates code from SPEC spec |
| `spaider implement {slug} step by step` | Implements with user confirmation |
| `spaider implement {slug} tests first` | Generates tests first, then code |
| `spaider implement {slug} flow {flow-id}` | Implements specific flow only |
| `spaider implement {slug} api` | Implements API layer only |
| `spaider implement {slug} tests` | Generates tests only |
| `spaider continue implementing {slug}` | Continues partial implementation |
| `spaider implement {slug} remaining` | Implements only unimplemented parts |
| `spaider sync code with SPEC {slug}` | Updates code to match SPEC |
| `spaider add markers to {path}` | Adds markers to existing code |
| `spaider add markers for {slug}` | Adds markers matching SPEC |

**CODE — Validation**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider validate code` | Validates all code markers |
| `spaider validate code for {slug}` | Validates specific spec |
| `spaider validate code coverage` | Reports implementation coverage % |
| `spaider validate code coverage for {slug}` | Coverage for specific spec |
| `spaider validate code orphans` | Finds orphaned markers |
| `spaider validate code refs` | Validates marker references |
| `spaider validate code markers` | Checks marker format |
| `spaider list code markers` | Lists all markers |
| `spaider list code markers for {slug}` | Lists markers for spec |
| `spaider show uncovered flows` | Lists flows without code |
| `spaider compare code to SPEC {slug}` | Shows drift from spec |
| `spaider find missing implementations` | Lists unimplemented elements |

**Pipeline & Cross-Artifact**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider validate all` | Validates entire hierarchy |
| `spaider validate refs` | Checks all cross-references |
| `spaider show pipeline` | Displays artifact status |
| `spaider coverage report` | Summary of implementation coverage |

---

## Example Prompts — Brownfield Project

**Reverse-engineer from code**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider reverse PRD from codebase` | Extracts requirements from existing implementation |
| `spaider reverse DESIGN from src/` | Documents current architecture from code |
| `spaider reverse SPEC from src/auth/` | Creates SPEC spec from auth module |
| `spaider reverse SPEC auth from code` | Same, using spec slug |
| `spaider analyze src/api/` | Systematic code analysis with checklist |

**Import from existing docs**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider make PRD from docs/requirements.txt` | Extracts requirements into PRD format |
| `spaider make PRD from README` | Creates PRD from project README |
| `spaider make PRD from this conversation` | Creates PRD from stakeholder discussion |
| `spaider import OpenAPI as DESIGN` | Converts API spec into DESIGN |
| `spaider import db-schema.sql as DESIGN data model` | Extracts data model from SQL |
| `spaider convert user-stories.md to PRD` | Transforms user stories to PRD |

**Sync and compare**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider compare DESIGN to code` | Shows drift between design and implementation |
| `spaider sync DESIGN from code` | Updates DESIGN to match current code |
| `spaider diff SPEC auth` | Shows changes since last validation |

---

## Example Prompts — Evolution & Maintenance

**Extend artifacts**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider extend PRD with payments` | Adds capability to PRD |
| `spaider extend DESIGN with caching` | Adds component to DESIGN |
| `spaider extend SPEC auth with MFA` | Adds scenario to spec |
| `spaider add spec billing to decomposition` | Adds spec entry |

**Update and propagate**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider update PRD requirements` | Updates requirements section |
| `spaider propagate PRD changes to DESIGN` | Updates DESIGN from PRD changes |
| `spaider sync DESIGN from code` | Updates DESIGN to match implementation |

**Impact analysis**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider show impact of removing FR-AUTH-002` | Traces downstream references |
| `spaider show impact of changing component auth` | Shows affected artifacts |
| `spaider deprecate spec user-import` | Marks deprecated across artifacts |

**Refactoring**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider refactor component auth-service` | Updates DESIGN and SPECs |
| `spaider rename spec billing to payments` | Renames across all artifacts |
| `spaider split spec payments` | Creates sub-specs |
| `spaider merge specs billing and invoicing` | Combines specs |

---

## Example Prompts — Review & Quality

**Validation modes**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider validate {ARTIFACT}` | Full validation (structural + semantic) |
| `spaider validate {ARTIFACT} semantic` | Semantic only (content quality, completeness) |
| `spaider validate {ARTIFACT} structural` | Structural only (format, IDs, template compliance) |
| `spaider validate {ARTIFACT} refs` | Cross-reference validation only |
| `spaider validate {ARTIFACT} quick` | Fast check (critical issues only) |
| `spaider validate all` | Full validation of entire pipeline |
| `spaider validate all semantic` | Semantic validation across all artifacts |

**Traceability queries**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider trace FR-AUTH-001` | Shows path: PRD → DESIGN → SPEC → CODE |
| `spaider trace spec auth` | Shows all references to auth spec |
| `spaider find orphans` | Lists IDs with no upstream/downstream refs |
| `spaider find orphan code` | Code markers referencing non-existent IDs |
| `spaider find orphan requirements` | Requirements not covered by DESIGN |
| `spaider list unimplemented` | Specs without code coverage |
| `spaider coverage report` | Implementation coverage by artifact |
| `spaider show refs for DESIGN` | All references in DESIGN artifact |

**Review prompts**

| Prompt | What the agent does |
|--------|---------------------|
| `spaider review PRD` | Deep review with 300+ criteria |
| `spaider review DESIGN for consistency` | Checks for internal contradictions |
| `spaider review SPEC auth for completeness` | Validates edge cases and error handling |
| `spaider review PR #42 against SPEC` | Checks PR implements spec items |
| `spaider review code for auth` | Reviews implementation quality |

---

## Live Example

[Taskman (Spaider example project)](https://github.com/cyberfabric/spaider-examples-taskman) — a complete task management project with the full Spaider artifact set and implementation.

---

## Guides by Scenario

| Scenario | Guide | Key Point |
|----------|-------|-----------|
| **Greenfield** | [GREENFIELD.md](GREENFIELD.md) | Start from PRD, work down to code |
| **Brownfield** | [BROWNFIELD.md](BROWNFIELD.md) | Start anywhere — code-only, bottom-up, or full |
| **Modular monolith** | [MONOLITH.md](MONOLITH.md) | Project-level + module-level artifacts |

**Brownfield flexibility**: No required order. Start with code-only (checklist benefits), add SPEC specs for complex specs, add DESIGN later. Or go full top-down. Your choice.

## Reference

- Artifact taxonomy: [TAXONOMY.md](TAXONOMY.md)
- Full prompt reference: [README.md](../../../README.md#example-prompts)
