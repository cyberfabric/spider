# Modular Monolith Guide

Use this guide when you have a single repository with a single deployable (a monolith) organized into **modules** with strict boundaries.

All prompts work through the `spider` skill — enable it with `spider on` and use natural language prompts.

## Goal

Maintain:
- A validated **project-level architecture** (overall design + ADRs)
- A validated **module-level architecture** for each module

---

## Artifact Registry Structure

In a modular monolith, modules are represented as `children` in the system hierarchy. The `artifacts.json` schema supports nested systems for this purpose.

### Canonical Hierarchies

**Recommended nesting levels** (from project author):

| Hierarchy | When to use |
|-----------|-------------|
| **System → Subsystem → Component** | Most monoliths — clear boundaries, manageable depth |
| **System → Subsystem → Component → Module** | Large systems — when components need further decomposition |

**Examples:**

```
System: E-Commerce Platform
├── Subsystem: Storefront
│   ├── Component: Catalog
│   ├── Component: Cart
│   └── Component: Checkout
├── Subsystem: Backoffice
│   ├── Component: Inventory
│   ├── Component: Orders
│   └── Component: Reports
└── Subsystem: Platform
    ├── Component: Auth
    ├── Component: Billing
    └── Component: Notifications
```

```
System: Banking Platform
├── Subsystem: Core Banking
│   ├── Component: Accounts
│   │   ├── Module: Current
│   │   ├── Module: Savings
│   │   └── Module: Deposits
│   └── Component: Transactions
│       ├── Module: Transfers
│       ├── Module: Payments
│       └── Module: Standing Orders
└── Subsystem: Channels
    ├── Component: Mobile
    └── Component: Web
```

Each level can have its own `artifacts` and `codebase`. Deeper levels inherit context from parents.

### Example: 4-Level Hierarchy

System → Subsystem → Component → Module:

```json
{
  "version": "1.0",
  "project_root": "..",
  "weavers": {
    "spider-sdlc": {
      "format": "Spider",
      "path": ".spider/weavers/sdlc"
    }
  },
  "systems": [
    {
      "name": "Banking Platform",
      "slug": "banking",
      "weaver": "spider-sdlc",
      "artifacts_dir": "architecture",
      "artifacts": [
        { "name": "Platform PRD", "path": "architecture/PRD.md", "kind": "PRD", "traceability": "DOCS-ONLY" },
        { "name": "Platform Design", "path": "architecture/DESIGN.md", "kind": "DESIGN", "traceability": "FULL" }
      ],
      "codebase": [
        { "name": "Source", "path": "src", "extensions": [".ts"] }
      ],
      "children": [
        {
          "name": "Core Banking",
          "slug": "core",
          "weaver": "spider-sdlc",
          "artifacts_dir": "subsystems/core/architecture",
          "artifacts": [
            { "path": "subsystems/core/architecture/DESIGN.md", "kind": "DESIGN", "traceability": "FULL" }
          ],
          "codebase": [
            { "name": "Core Subsystem", "path": "src/core", "extensions": [".ts"] }
          ],
          "children": [
            {
              "name": "Accounts",
              "slug": "accounts",
              "weaver": "spider-sdlc",
              "artifacts_dir": "subsystems/core/accounts/architecture",
              "artifacts": [
                { "path": "subsystems/core/accounts/architecture/DESIGN.md", "kind": "DESIGN", "traceability": "FULL" }
              ],
              "codebase": [
                { "name": "Accounts", "path": "src/core/accounts", "extensions": [".ts"] }
              ],
              "children": [
                {
                  "name": "Savings",
                  "slug": "savings",
                  "weaver": "spider-sdlc",
                  "artifacts_dir": "subsystems/core/accounts/savings/architecture",
                  "artifacts": [
                    { "path": "subsystems/core/accounts/savings/architecture/specs/interest-calc.md", "kind": "SPEC", "traceability": "FULL" }
                  ],
                  "codebase": [
                    { "name": "Savings", "path": "src/core/accounts/savings", "extensions": [".ts"] }
                  ],
                  "children": []
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Key points:**
- System level: platform-wide PRD and DESIGN
- Subsystem level: subsystem DESIGN (references system DESIGN)
- Component level: component DESIGN + codebase scope
- Module level: SPEC specs + narrowest codebase scope

---

### Example 1: Full Module Architecture

Each module has its own complete artifact set:

```json
{
  "version": "1.0",
  "project_root": "..",
  "weavers": {
    "spider-sdlc": {
      "format": "Spider",
      "path": ".spider/weavers/sdlc"
    }
  },
  "systems": [
    {
      "name": "SaaS Platform",
      "slug": "saas",
      "weaver": "spider-sdlc",
      "artifacts_dir": "architecture",
      "artifacts": [
        { "name": "Product Requirements", "path": "architecture/PRD.md", "kind": "PRD", "traceability": "DOCS-ONLY" },
        { "name": "System Design", "path": "architecture/DESIGN.md", "kind": "DESIGN", "traceability": "FULL" },
        { "name": "Spec Breakdown", "path": "architecture/DECOMPOSITION.md", "kind": "DECOMPOSITION", "traceability": "FULL" },
        { "name": "Modular Architecture", "path": "architecture/ADR/0001-modular-monolith.md", "kind": "ADR", "traceability": "DOCS-ONLY" }
      ],
      "codebase": [
        { "name": "Source Code", "path": "src", "extensions": [".ts", ".tsx"] }
      ],
      "children": [
        {
          "name": "Auth",
          "slug": "auth",
          "weaver": "spider-sdlc",
          "artifacts_dir": "modules/auth/architecture",
          "artifacts": [
            { "path": "modules/auth/architecture/PRD.md", "kind": "PRD", "traceability": "DOCS-ONLY" },
            { "path": "modules/auth/architecture/DESIGN.md", "kind": "DESIGN", "traceability": "FULL" },
            { "path": "modules/auth/architecture/specs/login.md", "kind": "SPEC", "traceability": "FULL" },
            { "path": "modules/auth/architecture/specs/sessions.md", "kind": "SPEC", "traceability": "FULL" }
          ],
          "codebase": [
            { "name": "Auth Module", "path": "src/modules/auth", "extensions": [".ts"] }
          ],
          "children": []
        },
        {
          "name": "Billing",
          "slug": "billing",
          "weaver": "spider-sdlc",
          "artifacts_dir": "modules/billing/architecture",
          "artifacts": [
            { "path": "modules/billing/architecture/PRD.md", "kind": "PRD", "traceability": "DOCS-ONLY" },
            { "path": "modules/billing/architecture/DESIGN.md", "kind": "DESIGN", "traceability": "FULL" },
            { "path": "modules/billing/architecture/specs/invoices.md", "kind": "SPEC", "traceability": "FULL" }
          ],
          "codebase": [
            { "name": "Billing Module", "path": "src/modules/billing", "extensions": [".ts"] }
          ],
          "children": []
        }
      ]
    }
  ]
}
```

### Example 2: Spec-Only Modules

Modules have only SPEC specs, sharing project-level DESIGN:

```json
{
  "version": "1.0",
  "project_root": "..",
  "weavers": {
    "spider-sdlc": {
      "format": "Spider",
      "path": ".spider/weavers/sdlc"
    }
  },
  "systems": [
    {
      "name": "SaaS Platform",
      "slug": "saas",
      "weaver": "spider-sdlc",
      "artifacts_dir": "architecture",
      "artifacts": [
        { "name": "Product Requirements", "path": "architecture/PRD.md", "kind": "PRD", "traceability": "DOCS-ONLY" },
        { "name": "System Design", "path": "architecture/DESIGN.md", "kind": "DESIGN", "traceability": "FULL" },
        { "name": "Spec Breakdown", "path": "architecture/DECOMPOSITION.md", "kind": "DECOMPOSITION", "traceability": "FULL" }
      ],
      "codebase": [
        { "name": "Source Code", "path": "src", "extensions": [".ts", ".tsx"] }
      ],
      "children": [
        {
          "name": "Auth",
          "slug": "auth",
          "weaver": "spider-sdlc",
          "artifacts_dir": "modules/auth/architecture",
          "artifacts": [
            { "path": "modules/auth/architecture/specs/login.md", "kind": "SPEC", "traceability": "FULL" },
            { "path": "modules/auth/architecture/specs/sessions.md", "kind": "SPEC", "traceability": "FULL" }
          ],
          "codebase": [
            { "name": "Auth Module", "path": "src/modules/auth", "extensions": [".ts"] }
          ],
          "children": []
        },
        {
          "name": "Billing",
          "slug": "billing",
          "weaver": "spider-sdlc",
          "artifacts_dir": "modules/billing/architecture",
          "artifacts": [
            { "path": "modules/billing/architecture/specs/invoices.md", "kind": "SPEC", "traceability": "FULL" }
          ],
          "codebase": [
            { "name": "Billing Module", "path": "src/modules/billing", "extensions": [".ts"] }
          ],
          "children": []
        }
      ]
    }
  ]
}
```

### Example 3: Code-Only Modules

Modules declared for codebase scoping only, no module-level artifacts:

```json
{
  "version": "1.0",
  "project_root": "..",
  "weavers": {
    "spider-sdlc": {
      "format": "Spider",
      "path": ".spider/weavers/sdlc"
    }
  },
  "systems": [
    {
      "name": "SaaS Platform",
      "slug": "saas",
      "weaver": "spider-sdlc",
      "artifacts_dir": "architecture",
      "artifacts": [
        { "name": "Product Requirements", "path": "architecture/PRD.md", "kind": "PRD", "traceability": "DOCS-ONLY" },
        { "name": "System Design", "path": "architecture/DESIGN.md", "kind": "DESIGN", "traceability": "FULL" },
        { "name": "Spec Breakdown", "path": "architecture/DECOMPOSITION.md", "kind": "DECOMPOSITION", "traceability": "FULL" }
      ],
      "codebase": [
        { "name": "Source Code", "path": "src", "extensions": [".ts", ".tsx"] }
      ],
      "children": [
        {
          "name": "Auth",
          "slug": "auth",
          "weaver": "spider-sdlc",
          "codebase": [
            { "name": "Auth Module", "path": "src/modules/auth", "extensions": [".ts"] }
          ],
          "children": []
        },
        {
          "name": "Billing",
          "slug": "billing",
          "weaver": "spider-sdlc",
          "codebase": [
            { "name": "Billing Module", "path": "src/modules/billing", "extensions": [".ts"] }
          ],
          "children": []
        }
      ]
    }
  ]
}
```

### Directory Structure

The registry maps to this file structure:

```text
project-root/
├── .spider-adapter/
│   └── artifacts.json
├── architecture/
│   ├── PRD.md
│   ├── DESIGN.md
│   ├── DECOMPOSITION.md
│   └── ADR/
│       └── 0001-modular-monolith.md
├── modules/
│   ├── auth/
│   │   └── architecture/
│   │       ├── PRD.md
│   │       ├── DESIGN.md
│   │       └── specs/
│   │           ├── login.md
│   │           └── sessions.md
│   └── billing/
│       └── architecture/
│           ├── PRD.md
│           ├── DESIGN.md
│           └── specs/
│               └── invoices.md
└── src/
    └── ...
```

---

## Component DESIGN from Project DESIGN

When creating a component DESIGN, use the project (or parent) DESIGN as input for consistency.

### Flow

```
1. spider make DESIGN for component auth from project DESIGN
   → Reads project DESIGN
   → Extracts auth-related elements
   → Creates component DESIGN with references to project DESIGN

2. spider validate DESIGN for component auth refs
   → Validates references to project DESIGN components
   → Ensures component doesn't contradict project architecture
```

### Prompts

| Prompt | What happens |
|--------|--------------|
| `spider make DESIGN for component auth from project DESIGN` | Creates component DESIGN using project architecture |
| `spider make DESIGN for component auth inheriting from project` | Same, alternative phrasing |
| `spider sync DESIGN for component auth with project` | Updates component DESIGN to match project changes |
| `spider compare DESIGN for component auth to project` | Shows differences from project DESIGN |

### Example with Context

```
spider make DESIGN for component auth from project DESIGN
Context:
- Component: auth
- Project DESIGN: architecture/DESIGN.md
- Component code path: src/core/auth/
- Extract elements: AuthService, SessionManager, TokenValidator
- Component owns tables: users, sessions, refresh_tokens
- Public interface: login(), logout(), refresh(), validateToken()
```

The agent will:
1. Read project DESIGN
2. Extract auth-related elements and their interfaces
3. Create component DESIGN that references project elements by ID
4. Add component-specific details (internal structure, data ownership)

---

## Traceability Between Levels

### ID Conventions

IDs are built by concatenating **slugs** through the hierarchy chain, followed by the element kind and element slug.

**Pattern:** `spd-{system}-{subsystem}-{component}-{kind}-{slug}`

The tool validates IDs against the known hierarchy, so IDs must match registered slugs exactly.

| Hierarchy Level | ID Pattern | Example |
|-----------------|------------|---------|
| System PRD | `spd-{system}-fr-{slug}` | `spd-saas-fr-user-management` |
| System DESIGN | `spd-{system}-component-{slug}` | `spd-saas-component-auth-service` |
| Subsystem DESIGN | `spd-{system}-{subsystem}-component-{slug}` | `spd-banking-core-component-account-service` |
| Component PRD | `spd-{system}-{subsystem}-{component}-fr-{slug}` | `spd-banking-core-accounts-fr-balance-query` |
| Component DESIGN | `spd-{system}-{subsystem}-{component}-component-{slug}` | `spd-banking-core-accounts-component-ledger` |
| Module SPEC | `spd-{system}-{subsystem}-{component}-{module}-flow-{slug}` | `spd-banking-core-accounts-savings-flow-interest-calc` |

**Slug rules:**
- Lowercase letters, numbers, and hyphens only
- No spaces, no leading/trailing hyphens
- Defined in `slug` field of each system node
- Example: `"name": "Core Banking"` → `"slug": "core"`

### Cross-Level References

Child artifacts reference parent artifacts using full hierarchical IDs:

**In component DESIGN (banking-core-accounts):**
```markdown
## Traceability

### Project References
- Implements: `spd-banking-component-core-banking` (from system DESIGN)
- Implements: `spd-banking-core-component-account-service` (from subsystem DESIGN)
- Satisfies: `spd-banking-fr-account-management`, `spd-banking-fr-balance-query` (from system PRD)
- Follows: `spd-banking-adr-component-boundaries` (component boundary rules)
```

**In module SPEC (banking-core-accounts-savings):**
```markdown
## Traceability

### Component References
- Component: `spd-banking-core-accounts-component-ledger`
- Requirement: `spd-banking-core-accounts-fr-balance-query`

### System References
- System component: `spd-banking-component-core-banking`
- System requirement: `spd-banking-fr-account-management`
```

### Traceability Queries

| Prompt | What happens |
|--------|--------------|
| `spider trace spd-saas-fr-user-management` | Shows: PRD → DESIGN → component DESIGN → SPEC → CODE |
| `spider trace spd-saas-component-auth-service` | Shows system component and all child implementations |
| `spider trace spd-saas-auth-login-flow-token-validation` | Shows full path from system PRD to component code |
| `spider find refs to spd-saas-component-auth-service` | Lists all child artifacts referencing this component |
| `spider validate refs for component auth` | Validates all cross-level references in component |
| `spider show orphans across levels` | Finds broken references between project and children |

### Validation Across Levels

| Prompt | What happens |
|--------|--------------|
| `spider validate all` | Validates project + all children |
| `spider validate all refs` | Validates all cross-references at all levels |
| `spider validate component auth against project` | Checks component compatibility with project |
| `spider compare component auth to project DESIGN` | Shows component drift from project architecture |

---

## How to Provide Context

In a modular monolith, the most important context is:
- Scope: system, subsystem, component, or module
- Target name (component/module name if applicable)
- Boundaries and dependencies
- Code paths

**Example format:**
```
spider make DESIGN
Context:
- Scope: system
- Architecture style: modular monolith
- Components: auth, billing, notifications
- Dependency rules: billing -> auth, notifications -> auth
```

---

## Project-Level Workflow

Describe the full system and cross-module rules.

### 1. PRD (Project)

**Create**

| Prompt | What happens |
|--------|--------------|
| `spider make PRD` | Creates project PRD interactively |
| `spider make PRD for SaaS platform` | Creates PRD with context |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spider update PRD` | Updates project PRD |
| `spider extend PRD with multi-tenant support` | Adds capability |

**Provide context:** product vision, component list, architecture style.

**Example:**
```
spider make PRD
Context:
- Product: SaaS platform
- Architecture style: modular monolith
- Core components: auth, billing, notifications
```

### 2. Validate PRD (Project)

| Prompt | What happens |
|--------|--------------|
| `spider validate PRD` | Full validation (300+ criteria) |
| `spider validate PRD semantic` | Semantic only |
| `spider validate PRD structural` | Structural only |

### 3. ADR + DESIGN (Project)

**Create DESIGN**

| Prompt | What happens |
|--------|--------------|
| `spider make DESIGN` | Creates project DESIGN interactively |
| `spider make DESIGN from PRD` | Transforms PRD into architecture |

**Update DESIGN**

| Prompt | What happens |
|--------|--------------|
| `spider update DESIGN` | Updates project DESIGN |
| `spider extend DESIGN with component notifications` | Adds component |
| `spider update DESIGN dependency rules` | Updates component dependencies |

**ADR**

| Prompt | What happens |
|--------|--------------|
| `spider make ADR for component boundaries` | Creates ADR for architecture decision |
| `spider make ADR for cross-component communication` | Creates ADR comparing approaches |
| `spider update ADR 0001` | Updates specific ADR |

**Provide context:** component list, dependency rules, integration approach.

**Example:**
```
spider make DESIGN
Context:
- Scope: system
- Architecture style: modular monolith
- Components:
  - auth (subsystems/core/auth/)
  - billing (subsystems/core/billing/)
- Dependency rules: billing -> auth
- Integration: shared DB, tables owned by components
```

### 4. Validate DESIGN + ADR (Project)

| Prompt | What happens |
|--------|--------------|
| `spider validate DESIGN` | Full validation (380+ criteria) |
| `spider validate DESIGN semantic` | Semantic only |
| `spider validate DESIGN refs` | Cross-references |
| `spider validate ADR` | Validates all ADRs |
| `spider validate ADR 0001` | Validates specific ADR |

### 5. DECOMPOSITION (Project)

**Create**

| Prompt | What happens |
|--------|--------------|
| `spider decompose` | Creates project decomposition |
| `spider decompose by capability` | Groups by business capability |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spider add spec {slug}` | Adds project spec |
| `spider update spec {slug} status` | Updates status |

**Provide context:** system-level specs (NOT components).

**Example:**
```
spider decompose
Context:
- Scope: system
- System specs: pricing-plans, invoice-lifecycle, tenant-management
- Note: components are NOT specs
```

### 6. Validate DECOMPOSITION (Project)

| Prompt | What happens |
|--------|--------------|
| `spider validate DECOMPOSITION` | Full validation |
| `spider validate DECOMPOSITION semantic` | Semantic only |
| `spider validate DECOMPOSITION refs` | Cross-references |

---

## Component-Level Workflow

Use when you want a component (or module in 4-level hierarchies) to have its own architecture.

> **Note**: Use `for component {name}` in prompts. For 4-level hierarchies, use `for module {name}` to target the deepest level.

### 7. PRD (Component)

**Create**

| Prompt | What happens |
|--------|--------------|
| `spider make PRD for component auth` | Creates component PRD |
| `spider make PRD` with component context | Creates interactively |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spider update PRD for component auth` | Updates component PRD |
| `spider extend PRD for component auth with MFA` | Adds capability |

**Provide context:** scope, component name, component paths.

**Example:**
```
spider make PRD for component auth
Context:
- Scope: component
- Component: auth
- Component code path: src/core/auth/
- Component architecture: subsystems/core/auth/architecture/
```

### 8. DESIGN (Component)

**Create**

| Prompt | What happens |
|--------|--------------|
| `spider make DESIGN for component auth` | Creates component DESIGN |
| `spider reverse DESIGN for component auth` | Reverse-engineers from code |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spider update DESIGN for component auth` | Updates component DESIGN |
| `spider extend DESIGN for component auth with sessions` | Adds internal component |
| `spider sync DESIGN for component auth from code` | Syncs with code |

**Provide context:** component dependencies, public interface, data ownership.

**Example:**
```
spider make DESIGN for component auth
Context:
- Scope: component
- Component: auth
- Component code path: src/core/auth/
- Dependencies: none
- Public interface: AuthService (login, logout, refresh)
- Data ownership: users, sessions tables
```

### 9. DECOMPOSITION (Component)

**Create**

| Prompt | What happens |
|--------|--------------|
| `spider decompose component auth` | Creates component decomposition |
| `spider decompose component auth from code` | From existing code |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spider add spec {slug} to component auth` | Adds component spec |
| `spider update spec {slug} in component auth` | Updates spec |

**Example:**
```
spider decompose component auth
Context:
- Scope: component
- Component: auth
- Component specs: login, sessions, mfa
```

### 10. SPEC (Component)

**Create**

| Prompt | What happens |
|--------|--------------|
| `spider make SPEC sessions for component auth` | Creates component spec |
| `spider reverse SPEC sessions for component auth` | From existing code |

**Update**

| Prompt | What happens |
|--------|--------------|
| `spider update SPEC sessions for component auth` | Updates spec |
| `spider extend SPEC sessions with token refresh` | Adds scenario |
| `spider sync SPEC sessions from code` | Syncs with code |

**Provide context:** component, spec slug, scenarios, data ownership.

**Example:**
```
spider make SPEC sessions for component auth
Context:
- Scope: component
- Component: auth
- Spec: sessions
- Include scenarios: login, logout, token refresh, session expiry
- Data ownership: sessions table
```

### 11. Validate SPEC (Component)

| Prompt | What happens |
|--------|--------------|
| `spider validate SPEC sessions for component auth` | Full validation |
| `spider validate SPEC sessions for component auth semantic` | Semantic only |
| `spider validate SPEC sessions for component auth refs` | Cross-references |

### 12. CODE (Component)

**Implement**

| Prompt | What happens |
|--------|--------------|
| `spider implement sessions for component auth` | Generates code |
| `spider implement sessions for component auth step by step` | With confirmation |
| `spider implement sessions for component auth tests first` | Tests first |

**Implement specific parts**

| Prompt | What happens |
|--------|--------------|
| `spider implement sessions for component auth flow token-refresh` | Specific flow |
| `spider implement sessions for component auth api` | API layer only |
| `spider implement sessions for component auth tests` | Tests only |

**Continue / update**

| Prompt | What happens |
|--------|--------------|
| `spider continue implementing sessions for component auth` | Continue partial |
| `spider implement sessions for component auth remaining` | Unimplemented only |
| `spider sync code with SPEC sessions for component auth` | Sync with spec |

**Add markers**

| Prompt | What happens |
|--------|--------------|
| `spider add markers for sessions in component auth` | Adds markers to existing code |
| `spider fix markers in src/core/auth/` | Fixes incorrect markers |

**Example:**
```
spider implement sessions for component auth
Context:
- Component code path: src/core/auth/
- Component architecture: subsystems/core/auth/architecture/
```

### 13. Validate Code (Component)

**Full validation**

| Prompt | What happens |
|--------|--------------|
| `spider validate code for component auth` | All component code |
| `spider validate code for sessions in component auth` | Specific spec |
| `spider validate code in src/core/auth/` | Specific path |

**Coverage**

| Prompt | What happens |
|--------|--------------|
| `spider validate code coverage for component auth` | Component coverage |
| `spider validate code coverage for sessions in component auth` | Spec coverage |
| `spider show uncovered for component auth` | Lists unimplemented |

**Traceability**

| Prompt | What happens |
|--------|--------------|
| `spider validate code orphans for component auth` | Orphaned markers |
| `spider validate code refs for component auth` | Marker references |
| `spider list code markers for component auth` | Lists component markers |

**Consistency**

| Prompt | What happens |
|--------|--------------|
| `spider compare code to SPEC sessions for component auth` | Shows drift |
| `spider validate code consistency for component auth` | Checks code matches specs |

---

## Quick Reference

### Project Level

| Step | Generate | Validate |
|------|----------|----------|
| 1 | `spider make PRD` | `spider validate PRD` |
| 2 | `spider make DESIGN` | `spider validate DESIGN` |
| 3 | `spider make ADR for ...` | `spider validate ADR` |
| 4 | `spider decompose` | `spider validate DECOMPOSITION` |

### Component Level

| Step | Generate | Validate |
|------|----------|----------|
| 1 | `spider make PRD for component {name}` | `spider validate PRD for component {name}` |
| 2 | `spider make DESIGN for component {name}` | `spider validate DESIGN for component {name}` |
| 3 | `spider decompose component {name}` | `spider validate DECOMPOSITION for component {name}` |
| 4 | `spider make SPEC {slug} for component {name}` | `spider validate SPEC {slug} for component {name}` |
| 5 | `spider implement {slug} for component {name}` | `spider validate code for {slug} in component {name}` |

> For 4-level hierarchies, use `module` instead of `component` to target the deepest level.

**Validation modes** (append to any `validate` command):
- `semantic` — content quality, completeness, clarity
- `structural` — format, IDs, template compliance
- `refs` — cross-references to other artifacts
- `quick` — critical issues only (fast)

---

## Adapter Configuration

Example adapter AGENTS.md for a modular monolith:

```markdown
# Project Spider Adapter

WHEN working in this repo:
- This is a modular monolith with hierarchy: System → Subsystem → Component
- Each component MUST have its architecture co-located with component code.
- Component architecture path convention:
  - `subsystems/{subsystem}/{component}/architecture/PRD.md`
  - `subsystems/{subsystem}/{component}/architecture/DESIGN.md`
  - `subsystems/{subsystem}/{component}/architecture/ADR/**`
  - `subsystems/{subsystem}/{component}/architecture/DECOMPOSITION.md`
  - `subsystems/{subsystem}/{component}/architecture/specs/{slug}.md`
- Component boundaries are enforced by code structure and dependency rules.

WHEN asked to generate/validate artifacts:
- Ask whether the scope is system-level or component-level.
- If component-level: ask which component is in scope.
```

---

## Iteration Rules

- System-level artifacts describe the full system and cross-component rules
- Component-level artifacts describe one component in isolation
- Component artifacts must stay compatible with system architecture
- If component code changes, update component SPEC first, then validate
- Cross-component changes may require updating system DESIGN
