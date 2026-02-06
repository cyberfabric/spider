# Greenfield Guide

Use this guide when you are starting a new project from scratch.

All prompts work through the `spaider` skill — enable it with `spaider on` and use natural language prompts.

## Goal

Create a validated baseline (PRD + architecture) before writing code.

## What You Will Produce

Spaider artifacts registered in `.spaider-adapter/artifacts.json` ([taxonomy](TAXONOMY.md)):

| Artifact | Default Location |
|----------|------------------|
| PRD | `architecture/PRD.md` |
| ADR | `architecture/ADR/*.md` |
| DESIGN | `architecture/DESIGN.md` |
| DECOMPOSITION | `architecture/DECOMPOSITION.md` |
| SPEC | `architecture/specs/{slug}.md` |

**Customizing artifact locations:**

| Prompt | What happens |
|--------|--------------|
| `spaider set artifacts_dir to docs/design/` | Changes default base directory for new artifacts |
| `spaider move PRD to docs/requirements/PRD.md` | Moves artifact to new location |
| `spaider register PRD at specs/product-requirements.md` | Registers existing file as PRD artifact |
| `spaider show artifact locations` | Displays current paths from `artifacts.json` |

You can also edit `.spaider-adapter/artifacts.json` directly:
- `artifacts_dir` — Default base directory for new artifacts (default: `architecture`)
- Subdirectories for SPECs (`specs/`) and ADRs (`ADR/`) are defined by the weaver
- Artifact paths in `artifacts` array are FULL paths — you can place artifacts anywhere

## How to Provide Context

Each prompt can include additional context. Recommended:

- Current state (what exists, what is missing)
- Links/paths to existing docs (README, specs, diagrams)
- Constraints (security, compliance, performance)
- Non-goals and out-of-scope items

**Example format:**
```
spaider make DESIGN for taskman
Context:
- Repo: taskman - task management CLI tool
- Existing docs: README.md
- Constraints: SQLite storage, offline-first
```

The agent will read inputs, ask targeted questions, propose answers, and produce artifacts.

---

## Workflow Sequence

### 1. PRD

**Create**

| Prompt | What happens |
|--------|--------------|
| `spaider make PRD` | Creates PRD interactively |
| `spaider make PRD for taskman` | Creates PRD with context |
| `spaider draft PRD from README` | Extracts initial PRD from README |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spaider update PRD` | Updates PRD interactively |
| `spaider extend PRD with task labels` | Adds capability to existing PRD |
| `spaider update PRD actors` | Updates actors section |
| `spaider update PRD requirements` | Updates requirements section |

**Provide context:** product vision, target users, key capabilities, existing PRD/BRD.

**Example:**
```
spaider make PRD for taskman
Context:
- Product: taskman - CLI task management tool
- Users: developers, solo users
- Key capabilities: create tasks, list tasks, mark done, due dates, priorities
- Storage: SQLite local database
```

### 2. Validate PRD

| Prompt | What happens |
|--------|--------------|
| `spaider validate PRD` | Full validation (300+ criteria) |
| `spaider validate PRD semantic` | Semantic only (content quality) |
| `spaider validate PRD structural` | Structural only (format, IDs) |
| `spaider validate PRD quick` | Fast check (critical issues) |

### 3. ADR + DESIGN

**Create DESIGN**

| Prompt | What happens |
|--------|--------------|
| `spaider make DESIGN` | Creates DESIGN interactively |
| `spaider make DESIGN from PRD` | Transforms PRD into architecture |

**Update DESIGN**

| Prompt | What happens |
|--------|--------------|
| `spaider update DESIGN` | Updates DESIGN interactively |
| `spaider extend DESIGN with sync-service` | Adds component to DESIGN |
| `spaider update DESIGN components` | Updates components section |
| `spaider update DESIGN data model` | Updates data model section |

**Create ADR**

| Prompt | What happens |
|--------|--------------|
| `spaider make ADR for SQLite` | Creates ADR for technology choice |
| `spaider make ADR for CLI vs TUI` | Creates ADR comparing approaches |

**Update ADR**

| Prompt | What happens |
|--------|--------------|
| `spaider update ADR 0001` | Updates specific ADR |
| `spaider supersede ADR 0001 with 0002` | Creates new ADR superseding old |

**Provide context:** architecture constraints, existing domain model, API contracts.

**Example:**
```
spaider make DESIGN for taskman
Context:
- Tech: CLI tool, SQLite storage
- Constraints: offline-first, single binary, cross-platform
- Language: Go or Rust
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
| `spaider decompose into specs` | Creates ordered spec list |
| `spaider decompose by capability` | Groups by business capability |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spaider add spec labels` | Adds new spec entry |
| `spaider update spec task-crud status` | Updates spec status |
| `spaider update spec task-crud priority` | Updates spec priority |
| `spaider reorder specs` | Changes spec order |

**Provide context:** spec boundaries, grouping preferences.

**Example:**
```
spaider decompose taskman into specs
Context:
- Split by capability: task-crud, task-list, task-search, labels, sync
```

### 6. Validate DECOMPOSITION

| Prompt | What happens |
|--------|--------------|
| `spaider validate DECOMPOSITION` | Full validation (130+ criteria) |
| `spaider validate DECOMPOSITION semantic` | Semantic only (coverage) |
| `spaider validate DECOMPOSITION structural` | Structural only (format) |
| `spaider validate DECOMPOSITION refs` | Cross-references to DESIGN |

### 7. SPEC

**Create**

| Prompt | What happens |
|--------|--------------|
| `spaider make SPEC for task-crud` | Creates spec design |
| `spaider make SPEC for task-list` | Creates detailed design |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spaider update SPEC task-crud` | Updates spec design |
| `spaider extend SPEC task-crud with bulk-delete` | Adds scenario to spec |
| `spaider update SPEC task-crud flows` | Updates flows section |
| `spaider update SPEC task-crud algorithms` | Updates algorithms section |

**Provide context:** spec slug, acceptance criteria, edge cases, error handling.

**Example:**
```
spaider make SPEC for task-crud
Context:
- Include scenarios: create, update, delete, bulk operations
- Edge cases: duplicate titles, invalid dates, missing required fields
```

### 8. Validate SPEC

| Prompt | What happens |
|--------|--------------|
| `spaider validate SPEC task-crud` | Full validation (380+ criteria) |
| `spaider validate SPEC task-crud semantic` | Semantic only (flows, edge cases) |
| `spaider validate SPEC task-crud structural` | Structural only (SDSL, IDs) |
| `spaider validate SPEC task-crud refs` | Cross-references to DESIGN |

### 9. CODE

**Implement from scratch**

| Prompt | What happens |
|--------|--------------|
| `spaider implement task-crud` | Generates code from SPEC |
| `spaider implement spec task-crud` | Same, explicit spec keyword |
| `spaider implement task-crud step by step` | Implements with user confirmation at each step |
| `spaider implement task-crud tests first` | Generates tests first, then implementation |

**Implement specific parts**

| Prompt | What happens |
|--------|--------------|
| `spaider implement task-crud flow create` | Implements specific flow only |
| `spaider implement task-crud algorithm validate` | Implements specific algorithm only |
| `spaider implement task-crud api` | Implements API layer only |
| `spaider implement task-crud data layer` | Implements data/repository layer only |
| `spaider implement task-crud tests` | Generates tests only |

**Continue / update**

| Prompt | What happens |
|--------|--------------|
| `spaider continue implementing task-crud` | Continues partial implementation |
| `spaider sync code with SPEC task-crud` | Updates code to match SPEC changes |
| `spaider implement task-crud remaining` | Implements only unimplemented parts |
| `spaider refactor task-crud` | Refactors implementation keeping markers |

**Add markers to existing code**

| Prompt | What happens |
|--------|--------------|
| `spaider add markers to cmd/task.go` | Adds `@spaider-*` markers to existing code |
| `spaider add markers for task-crud` | Adds markers matching SPEC |
| `spaider fix markers in cmd/` | Fixes incorrect/incomplete markers |

**Provide context:** spec slug, code paths if non-standard.

### 10. Validate Code

**Full validation**

| Prompt | What happens |
|--------|--------------|
| `spaider validate code` | Validates all code markers |
| `spaider validate code for task-crud` | Validates specific spec |
| `spaider validate code in cmd/` | Validates code in specific path |

**Coverage**

| Prompt | What happens |
|--------|--------------|
| `spaider validate code coverage` | Reports implementation coverage % |
| `spaider validate code coverage for task-crud` | Coverage for specific spec |
| `spaider show uncovered flows` | Lists flows without implementation |
| `spaider show uncovered algorithms` | Lists algorithms without implementation |

**Traceability**

| Prompt | What happens |
|--------|--------------|
| `spaider validate code orphans` | Finds markers referencing non-existent IDs |
| `spaider validate code refs` | Validates all marker references |
| `spaider validate code markers` | Checks marker format correctness |
| `spaider list code markers` | Lists all markers in codebase |
| `spaider list code markers for task-crud` | Lists markers for specific spec |

**Consistency**

| Prompt | What happens |
|--------|--------------|
| `spaider compare code to SPEC task-crud` | Shows drift between code and spec |
| `spaider validate code consistency` | Checks code matches SPECs |
| `spaider find missing implementations` | Lists SPEC elements without code |

---

## Iteration Rules

- If a change impacts behavior, update the relevant design first (DESIGN or SPEC)
- Re-run validation for the modified artifact before continuing
- If code contradicts design, update design first, then re-validate

## Quick Reference

| Step | Generate | Validate |
|------|----------|----------|
| 1 | `spaider make PRD for taskman` | `spaider validate PRD` |
| 2 | `spaider make DESIGN` | `spaider validate DESIGN` |
| 3 | `spaider make ADR for SQLite` | `spaider validate ADR` |
| 4 | `spaider decompose` | `spaider validate DECOMPOSITION` |
| 5 | `spaider make SPEC for task-crud` | `spaider validate SPEC task-crud` |
| 6 | `spaider implement task-crud` | `spaider validate code for task-crud` |

**Validation modes** (append to any `validate` command):
- `semantic` — content quality, completeness, clarity
- `structural` — format, IDs, template compliance
- `refs` — cross-references to other artifacts
- `quick` — critical issues only (fast)
