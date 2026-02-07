---
cypilot: true
type: requirement
name: Markerless Template Specification
version: 1.0
purpose: Define how Cypilot validates and extracts IDs/CDSL from artifacts that do not contain `<!-- cpt:... -->` template markers
---

# Markerless Template Specification

## Table of Contents

- [Overview](#overview)
- [Non-Goals](#non-goals)
- [Definition: Markerless Artifact](#definition-markerless-artifact)
- [Detection](#detection)
- [Supported Signal Extraction](#supported-signal-extraction)
  - [ID Definitions](#id-definitions)
  - [ID References](#id-references)
  - [CDSL Instruction Extraction](#cdsl-instruction-extraction)
  - [Ignoring Code Fences](#ignoring-code-fences)
- [Validation Behavior](#validation-behavior)
  - [Template Structure Validation](#template-structure-validation)
  - [Cross-Artifact Consistency](#cross-artifact-consistency)
  - [Traceability Interaction](#traceability-interaction)
  - [Covered-By (Markerless Simplification)](#covered-by-markerless-simplification)
- [Content Scoping (Optional Helper)](#content-scoping-optional-helper)
- [Examples](#examples)
- [Consolidated Validation Checklist](#consolidated-validation-checklist)
- [References](#references)

---

## Overview

Cypilot’s primary validation mechanism is **marker-based templates** (see `requirements/template.md`), where artifacts include paired markers like:

```html
<!-- cpt:TYPE:NAME -->
...
<!-- cpt:TYPE:NAME -->
```

However, some repositories and legacy documents may not contain any `<!-- cpt:... -->` markers. This document defines the **markerless** mode:

- Cypilot **does not** attempt to enforce template block structure.
- Cypilot **does** attempt to extract **IDs**, **ID references**, and **CDSL instructions** using best-effort regex scanning.
- Cypilot continues to run **cross-artifact consistency** checks, and may run **code traceability** checks depending on registry settings.

---

## Non-Goals

Markerless mode is explicitly **not** intended to provide the same guarantees as marker-based templates.

- Markerless mode does **not** guarantee structural compliance.
- Markerless mode does **not** provide precise block boundaries for validation errors.
- Markerless mode does **not** replace the template system.

---

## Definition: Markerless Artifact

An artifact is **markerless** if it contains **no** Cypilot template markers.

In markerless mode, the artifact is treated as if it had a synthetic, single `free` block called `markerless` for the purpose of attaching extracted IDs/refs.

---

## Detection

Markerless detection is performed by checking whether the file contains any `<!-- cpt:` markers.

If a template is missing in the registry and a synthetic template is used, the artifact is also treated as markerless for structural purposes.

---

## Supported Signal Extraction

### ID Definitions

Markerless scanning recognizes **ID definitions** via the same human-facing formats used inside `id` blocks (see `requirements/template.md`), for example:

```markdown
- [ ] **ID**: `cpt-my-system-fr-login`
- [x] `p1` - **ID**: `cpt-my-system-flow-login`
```

The scanner emits hits with:

- `type: definition`
- `id: <cpt-id>`
- `line: <line number>`
- `checked: true|false` (when a checkbox is present)
- `priority: pN` (when present)

### ID References

Markerless scanning recognizes **references** in three ways:

- Standalone backticked IDs on list lines:
  - ``- `cpt-my-system-fr-login` ``
  - ``* `cpt-my-system-fr-login` ``
- Any inline backticked occurrence:
  - `... Inline `cpt-my-system-fr-login` here ...`

The scanner emits hits with:

- `type: reference`
- `id: <cpt-id>`
- `line: <line number>`

### CDSL Instruction Extraction

Markerless scanning can extract CDSL instructions (see `requirements/CDSL.md`) even if the document has no `<!-- cpt:cdsl:... -->` block.

The scanner identifies lines matching the CDSL step format, and emits:

- `type: cdsl_instruction`
- `phase: <int>`
- `inst: <string>` (without the `inst-` prefix)
- `line: <line number>`

#### Parent binding rule

Because markerless artifacts have no deterministic blocks, extracted CDSL instructions use a best-effort **parent binding** rule:

- The instruction’s `parent_id` is the **nearest preceding ID definition** found above the instruction.
- If no preceding ID definition exists, `parent_id` is omitted.

### Ignoring Code Fences

All markerless scanning MUST ignore content inside fenced code blocks:

```markdown
```
...ignored...
```
```

This prevents documentation examples from being interpreted as real IDs/instructions.

---

## Validation Behavior

### Template Structure Validation

If an artifact is markerless:

- Template block structure validation is skipped.
- No `required="true"` / `repeat=` enforcement occurs.
- Unknown marker checks do not apply (there are no markers).

### Cross-Artifact Consistency

Markerless artifacts still participate in cross-artifact checks:

- Orphaned references (a reference to an undefined ID) may be reported.
- Duplicate ID definitions may be reported (implementation-defined).
- Markerless artifacts contribute both definitions and references to the global index.

### Traceability Interaction

Markerless artifacts can still interact with code traceability (see `requirements/traceability.md`) depending on registry settings.

Key rule:

- If an artifact is markerless and its registry traceability mode is `FULL`, Cypilot may accept that code markers reference IDs defined in that markerless artifact.

### Covered-By (Markerless Simplification)

Marker-based templates can encode `covered_by="KIND,..."` semantics on `id` blocks.

In markerless mode there is no template metadata, so covered-by constraints are approximated:

- For markerless artifacts, each `**ID**: ...` definition SHOULD be referenced from at least one other artifact kind.
- If the project scope only contains one kind (no “other kinds” exist), Cypilot SHOULD emit a warning instead of an error.

---

## Content Scoping (Optional Helper)

Some tools may provide a helper for retrieving an approximate content “scope” for a given ID in a markerless document.

The scope heuristics are best-effort and may use:

- Heading-based scopes (e.g., a heading line containing an ID)
- Separator-based scopes (implementation-defined)

This is not a validation guarantee; it is intended for navigation and UX.

---

## Examples

### Markerless artifact with definitions and references

```markdown
# Login

- [x] `p1` - **ID**: `cpt-myapp-fr-login`

We need to implement `cpt-myapp-flow-login`.

- `cpt-myapp-fr-login`
```

### Markerless artifact with CDSL instructions

```markdown
- [ ] **ID**: `cpt-myapp-flow-login`

1. [ ] - `p1` - Receive request - `inst-receive`
2. [ ] - `p1` - Validate input - `inst-validate`
3. [ ] - `p1` - **RETURN** response - `inst-return`
```

---

## Consolidated Validation Checklist

### Detection

- [ ] File is correctly detected as markerless only when no `<!-- cpt:` markers exist

### Extraction

- [ ] ID definitions are extracted from `**ID**: `...`` patterns
- [ ] ID references are extracted from backticked inline IDs
- [ ] CDSL instructions are extracted from CDSL step lines
- [ ] Code fences are excluded from all scans

### Validation behavior

- [ ] Template structure validation is skipped for markerless artifacts
- [ ] Markerless artifacts participate in cross-artifact consistency checks
- [ ] Traceability integration follows registry’s traceability mode

---

## References

- `requirements/template.md` — marker-based template system
- `requirements/CDSL.md` — CDSL syntax
- `requirements/traceability.md` — code marker format and validation
- Implementation (reference): `skills/cypilot/scripts/cypilot/utils/document.py`, `skills/cypilot/scripts/cypilot/utils/template.py`, `skills/cypilot/scripts/cypilot/cli.py`
