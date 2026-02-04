# Greenfield Guide

Use this guide when you are starting a new project from scratch.

All prompts work through the `spider` skill — enable it with `spider on` and use natural language prompts.

## Goal

Create a validated baseline (PRD + architecture) before writing code.

## What You Will Produce

Spider artifacts registered in `.spider-adapter/artifacts.json` ([taxonomy](TAXONOMY.md)):

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
| `spider set artifacts_dir to docs/design/` | Changes default base directory for new artifacts |
| `spider move PRD to docs/requirements/PRD.md` | Moves artifact to new location |
| `spider register PRD at specs/product-requirements.md` | Registers existing file as PRD artifact |
| `spider show artifact locations` | Displays current paths from `artifacts.json` |

You can also edit `.spider-adapter/artifacts.json` directly:
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
spider make DESIGN for taskman
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
| `spider make PRD` | Creates PRD interactively |
| `spider make PRD for taskman` | Creates PRD with context |
| `spider draft PRD from README` | Extracts initial PRD from README |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spider update PRD` | Updates PRD interactively |
| `spider extend PRD with task labels` | Adds capability to existing PRD |
| `spider update PRD actors` | Updates actors section |
| `spider update PRD requirements` | Updates requirements section |

**Provide context:** product vision, target users, key capabilities, existing PRD/BRD.

**Example:**
```
spider make PRD for taskman
Context:
- Product: taskman - CLI task management tool
- Users: developers, solo users
- Key capabilities: create tasks, list tasks, mark done, due dates, priorities
- Storage: SQLite local database
```

### 2. Validate PRD

| Prompt | What happens |
|--------|--------------|
| `spider validate PRD` | Full validation (300+ criteria) |
| `spider validate PRD semantic` | Semantic only (content quality) |
| `spider validate PRD structural` | Structural only (format, IDs) |
| `spider validate PRD quick` | Fast check (critical issues) |

### 3. ADR + DESIGN

**Create DESIGN**

| Prompt | What happens |
|--------|--------------|
| `spider make DESIGN` | Creates DESIGN interactively |
| `spider make DESIGN from PRD` | Transforms PRD into architecture |

**Update DESIGN**

| Prompt | What happens |
|--------|--------------|
| `spider update DESIGN` | Updates DESIGN interactively |
| `spider extend DESIGN with sync-service` | Adds component to DESIGN |
| `spider update DESIGN components` | Updates components section |
| `spider update DESIGN data model` | Updates data model section |

**Create ADR**

| Prompt | What happens |
|--------|--------------|
| `spider make ADR for SQLite` | Creates ADR for technology choice |
| `spider make ADR for CLI vs TUI` | Creates ADR comparing approaches |

**Update ADR**

| Prompt | What happens |
|--------|--------------|
| `spider update ADR 0001` | Updates specific ADR |
| `spider supersede ADR 0001 with 0002` | Creates new ADR superseding old |

**Provide context:** architecture constraints, existing domain model, API contracts.

**Example:**
```
spider make DESIGN for taskman
Context:
- Tech: CLI tool, SQLite storage
- Constraints: offline-first, single binary, cross-platform
- Language: Go or Rust
```

### 4. Validate DESIGN + ADR

| Prompt | What happens |
|--------|--------------|
| `spider validate DESIGN` | Full validation (380+ criteria) |
| `spider validate DESIGN semantic` | Semantic only (consistency) |
| `spider validate DESIGN structural` | Structural only (format) |
| `spider validate DESIGN refs` | Cross-references to PRD |
| `spider validate ADR` | Validates all ADRs |
| `spider validate ADR 0001` | Validates specific ADR |
| `spider validate ADR semantic` | Semantic only (rationale quality) |

### 5. DECOMPOSITION

**Create**

| Prompt | What happens |
|--------|--------------|
| `spider decompose` | Creates DECOMPOSITION interactively |
| `spider decompose into specs` | Creates ordered spec list |
| `spider decompose by capability` | Groups by business capability |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spider add spec labels` | Adds new spec entry |
| `spider update spec task-crud status` | Updates spec status |
| `spider update spec task-crud priority` | Updates spec priority |
| `spider reorder specs` | Changes spec order |

**Provide context:** spec boundaries, grouping preferences.

**Example:**
```
spider decompose taskman into specs
Context:
- Split by capability: task-crud, task-list, task-search, labels, sync
```

### 6. Validate DECOMPOSITION

| Prompt | What happens |
|--------|--------------|
| `spider validate DECOMPOSITION` | Full validation (130+ criteria) |
| `spider validate DECOMPOSITION semantic` | Semantic only (coverage) |
| `spider validate DECOMPOSITION structural` | Structural only (format) |
| `spider validate DECOMPOSITION refs` | Cross-references to DESIGN |

### 7. SPEC

**Create**

| Prompt | What happens |
|--------|--------------|
| `spider make SPEC for task-crud` | Creates spec design |
| `spider make SPEC for task-list` | Creates detailed design |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spider update SPEC task-crud` | Updates spec design |
| `spider extend SPEC task-crud with bulk-delete` | Adds scenario to spec |
| `spider update SPEC task-crud flows` | Updates flows section |
| `spider update SPEC task-crud algorithms` | Updates algorithms section |

**Provide context:** spec slug, acceptance criteria, edge cases, error handling.

**Example:**
```
spider make SPEC for task-crud
Context:
- Include scenarios: create, update, delete, bulk operations
- Edge cases: duplicate titles, invalid dates, missing required fields
```

### 8. Validate SPEC

| Prompt | What happens |
|--------|--------------|
| `spider validate SPEC task-crud` | Full validation (380+ criteria) |
| `spider validate SPEC task-crud semantic` | Semantic only (flows, edge cases) |
| `spider validate SPEC task-crud structural` | Structural only (SDSL, IDs) |
| `spider validate SPEC task-crud refs` | Cross-references to DESIGN |

### 9. CODE

**Implement from scratch**

| Prompt | What happens |
|--------|--------------|
| `spider implement task-crud` | Generates code from SPEC |
| `spider implement spec task-crud` | Same, explicit spec keyword |
| `spider implement task-crud step by step` | Implements with user confirmation at each step |
| `spider implement task-crud tests first` | Generates tests first, then implementation |

**Implement specific parts**

| Prompt | What happens |
|--------|--------------|
| `spider implement task-crud flow create` | Implements specific flow only |
| `spider implement task-crud algorithm validate` | Implements specific algorithm only |
| `spider implement task-crud api` | Implements API layer only |
| `spider implement task-crud data layer` | Implements data/repository layer only |
| `spider implement task-crud tests` | Generates tests only |

**Continue / update**

| Prompt | What happens |
|--------|--------------|
| `spider continue implementing task-crud` | Continues partial implementation |
| `spider sync code with SPEC task-crud` | Updates code to match SPEC changes |
| `spider implement task-crud remaining` | Implements only unimplemented parts |
| `spider refactor task-crud` | Refactors implementation keeping markers |

**Add markers to existing code**

| Prompt | What happens |
|--------|--------------|
| `spider add markers to cmd/task.go` | Adds `@spider-*` markers to existing code |
| `spider add markers for task-crud` | Adds markers matching SPEC |
| `spider fix markers in cmd/` | Fixes incorrect/incomplete markers |

**Provide context:** spec slug, code paths if non-standard.

### 10. Validate Code

**Full validation**

| Prompt | What happens |
|--------|--------------|
| `spider validate code` | Validates all code markers |
| `spider validate code for task-crud` | Validates specific spec |
| `spider validate code in cmd/` | Validates code in specific path |

**Coverage**

| Prompt | What happens |
|--------|--------------|
| `spider validate code coverage` | Reports implementation coverage % |
| `spider validate code coverage for task-crud` | Coverage for specific spec |
| `spider show uncovered flows` | Lists flows without implementation |
| `spider show uncovered algorithms` | Lists algorithms without implementation |

**Traceability**

| Prompt | What happens |
|--------|--------------|
| `spider validate code orphans` | Finds markers referencing non-existent IDs |
| `spider validate code refs` | Validates all marker references |
| `spider validate code markers` | Checks marker format correctness |
| `spider list code markers` | Lists all markers in codebase |
| `spider list code markers for task-crud` | Lists markers for specific spec |

**Consistency**

| Prompt | What happens |
|--------|--------------|
| `spider compare code to SPEC task-crud` | Shows drift between code and spec |
| `spider validate code consistency` | Checks code matches SPECs |
| `spider find missing implementations` | Lists SPEC elements without code |

---

## Iteration Rules

- If a change impacts behavior, update the relevant design first (DESIGN or SPEC)
- Re-run validation for the modified artifact before continuing
- If code contradicts design, update design first, then re-validate

## Quick Reference

| Step | Generate | Validate |
|------|----------|----------|
| 1 | `spider make PRD for taskman` | `spider validate PRD` |
| 2 | `spider make DESIGN` | `spider validate DESIGN` |
| 3 | `spider make ADR for SQLite` | `spider validate ADR` |
| 4 | `spider decompose` | `spider validate DECOMPOSITION` |
| 5 | `spider make SPEC for task-crud` | `spider validate SPEC task-crud` |
| 6 | `spider implement task-crud` | `spider validate code for task-crud` |

**Validation modes** (append to any `validate` command):
- `semantic` — content quality, completeness, clarity
- `structural` — format, IDs, template compliance
- `refs` — cross-references to other artifacts
- `quick` — critical issues only (fast)
