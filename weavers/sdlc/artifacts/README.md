# Spaider SDLC Rule Package

**ID**: `spaider-sdlc`
**Purpose**: Software Development Lifecycle artifacts for Spaider projects

---

## Artifact Kinds

| Kind | Description | Template | Checklist | Example |
| --- | --- | --- | --- | --- |
| PRD | Product Requirements Document | `artifacts/PRD/template.md` | `artifacts/PRD/checklist.md` | `artifacts/PRD/examples/example.md` |
| DESIGN | Overall System Design | `artifacts/DESIGN/template.md` | `artifacts/DESIGN/checklist.md` | `artifacts/DESIGN/examples/example.md` |
| ADR | Architecture Decision Record | `artifacts/ADR/template.md` | `artifacts/ADR/checklist.md` | `artifacts/ADR/examples/example.md` |
| DECOMPOSITION | Design Decomposition | `artifacts/DECOMPOSITION/template.md` | `artifacts/DECOMPOSITION/checklist.md` | `artifacts/DECOMPOSITION/examples/example.md` |
| SPEC | Spec Design | `artifacts/SPEC/template.md` | `artifacts/SPEC/checklist.md` | `artifacts/SPEC/examples/example.md` |

---

## Structure

```text
weavers/sdlc/
├── README.md           # This file
├── artifacts/
│   ├── PRD/
│   │   ├── template.md     # PRD template with Spaider markers
│   │   ├── checklist.md    # Expert review checklist
│   │   └── examples/
│   │       └── example.md  # Valid PRD example
│   ├── DESIGN/
│   │   ├── template.md
│   │   ├── checklist.md
│   │   └── examples/
│   │       └── example.md
│   ├── ADR/
│   │   ├── template.md
│   │   ├── checklist.md
│   │   └── examples/
│   │       └── example.md
│   ├── DECOMPOSITION/
│   │   ├── template.md
│   │   ├── checklist.md
│   │   └── examples/
│   │       └── example.md
│   └── SPEC/
│       ├── template.md
│       ├── checklist.md
│       └── examples/
│           └── example.md
└── codebase/
    ├── rules.md            # Code generation/validation rules
    └── checklist.md        # Weaver-specific code checklist
```

---

## Usage

### In execution-protocol.md

Dependencies resolved as:

```text
template:  weavers/sdlc/artifacts/{KIND}/template.md
checklist: weavers/sdlc/artifacts/{KIND}/checklist.md
example:   weavers/sdlc/artifacts/{KIND}/examples/example.md
```

### In artifacts.json

```json
{
  "rules": {
    "spaider-sdlc": {
      "path": "weavers/sdlc",
      "artifacts": ["PRD", "DESIGN", "ADR", "DECOMPOSITION", "SPEC"]
    }
  }
}
```

---

## Artifact Hierarchy

```text
PRD
 └── DESIGN
      ├── ADR (optional, per decision)
      └── DECOMPOSITION
           └── SPEC (per spec)
```

Each child artifact references IDs from parent artifacts for traceability.
