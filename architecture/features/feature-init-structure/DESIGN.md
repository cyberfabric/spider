# Feature Design: Initial Structure

## A. Feature Context

**Feature ID**: `fdd-fdd-feature-init-structure`

**Status**: IMPLEMENTED

**Feature Directory**: `architecture/features/feature-init-structure/`

**References**:
- `architecture/features/FEATURES.md` entry: `fdd-fdd-feature-init-structure`
- Overall Design: `architecture/DESIGN.md`

### 1. Overview

The Initial Structure feature defines the FDD project skeleton and base templates for all file types. It establishes where files are located, what common elements they must contain, and provides pytest validation for structural compliance.

### 2. Purpose

To establish:
- Project directory structure (where things go)
- Base file templates with common elements (headers, overview, validation criteria)
- Common requirements across all file categories
- Pytest tests validating file existence and structure

This feature creates the foundation upon which specific file type requirements are built.

### 3. Actors

- `fdd-fdd-actor-architect` - Defines and validates project structure

### 4. References

**Overall Design References**:
- Section B.1: FR-004 Design-First Development (`fdd-fdd-req-design-first`)
- Section B.3: Principle 1 Technology Agnostic Core (`fdd-fdd-principle-tech-agnostic`)
- Section B.4: Constraint 2 Markdown-Only Artifacts (`fdd-fdd-constraint-markdown`)

**Dependencies**: None (foundation layer)

**Blocks**: 
- `fdd-fdd-feature-adapter-system`
- `fdd-fdd-feature-workflow-engine`
- `fdd-fdd-feature-validation-engine`

---

## B. Actor Flows

**N/A** - This feature defines specifications only. No actor flows required.

---

## C. Algorithms

**N/A** - This feature defines specifications only. Implementation algorithms belong to `feature-validation-engine`.

---

## D. States

**N/A** - This feature defines specifications only. State machines belong to `feature-workflow-engine`.

---

## E. Technical Details

### Directory Structure

**ID**: `fdd-fdd-feature-init-structure-td-directory-structure`

<!-- fdd-id-content -->
 FDD project root directory structure (skeleton).

```
FDD/
├── AGENTS.md                    # Root navigation
├── README.md                    # Project overview
├── QUICKSTART.md                # Bootstrap guide
├── Makefile                     # Build commands
├── requirements/                # Structure specifications
│   └── *-structure.md           # Artifact structure specs
├── workflows/                   # Executable procedures
│   ├── *.md                     # Operation workflows
│   └── *-validate.md            # Validation workflows
├── skills/                      # CLI tools
│   └── fdd/
├── tests/                       # Pytest tests
└── examples/                    # Reference examples
```

<!-- fdd-id-content -->

### Base File Template

**ID**: `fdd-fdd-feature-init-structure-td-base-file-template`

<!-- fdd-id-content -->
 Base file template shared by all FDD specification files.

```markdown
---
fdd: true                                    # FDD framework marker
type: {requirement|workflow|agents|example}  # REQUIRED
name: {human-readable name}                  # REQUIRED
version: {MAJOR.MINOR}                       # REQUIRED
purpose: {brief description}                 # REQUIRED
scope: {what this applies to}                # optional
extends: {path to base file}                 # optional
status: {draft|stable|deprecated}            # optional
---

# FDD: {Title}

## Prerequisite Checklist

- [ ] {prerequisite 1}
- [ ] {prerequisite 2}

---

## Overview

{What this file defines}

---

## {Content Sections}

{Category-specific content}

---

## Validation Criteria

{How to validate content application}

## Validation Checklist

- [ ] {validation item 1}
- [ ] {validation item 2}
```

**YAML frontmatter fields**:
- `type`, `name`, `version`, `purpose` — REQUIRED
- `scope`, `extends`, `status` — optional
- `version` format: `MAJOR.MINOR` (MAJOR = breaking, MINOR = additions)

<!-- fdd-id-content -->

### Integration Points

**ID**: `fdd-fdd-feature-init-structure-td-integration-points`

<!-- fdd-id-content -->
Integration points for validation and developer workflows.
- **Pytest**: Tests in `tests/` validate structure
- **fdd validate**: CLI validates individual artifacts
- **Makefile**: `make test` runs all validations

<!-- fdd-id-content -->

---

## F. Requirements

### Project Directory Structure

- [x] **ID**: `fdd-fdd-feature-init-structure-req-directory-structure`

<!-- fdd-id-content -->

**Status**: IMPLEMENTED

**Description**: FDD project SHALL have defined directory structure with specific purposes for each directory. Root files SHALL include AGENTS.md, README.md, QUICKSTART.md, Makefile. Subdirectories SHALL include requirements/, workflows/, architecture/, skills/, tests/, examples/.

**References**:
- None (foundational requirement)

**Implements**:
- None (specification only)

**Phases**:
- [x] `ph-1`: Define directory structure

**Tests Covered**:
- `fdd-fdd-feature-init-structure-test-directories-exist`

**Acceptance Criteria**:
- All required directories exist
- Each directory has defined purpose
- No extraneous top-level directories

<!-- fdd-id-content -->

---

### Base File Structure

- [x] **ID**: `fdd-fdd-feature-init-structure-req-base-file-structure`

<!-- fdd-id-content -->

**Status**: IMPLEMENTED

**Description**: All FDD specification files SHALL have YAML frontmatter with `fdd: true` marker and required fields (type, name, version, purpose). Files SHALL have `# FDD:` title prefix, Prerequisite Checklist, Overview, Validation Criteria, and Validation Checklist sections.

**References**:
- None (foundational requirement)

**Implements**:
- None (specification only)

**Phases**:
- [x] `ph-1`: Define base file template

**Tests Covered**:
- `fdd-fdd-feature-init-structure-test-base-structure`

**Acceptance Criteria**:
- All spec files have YAML frontmatter with `fdd: true`
- All spec files have required fields: type, name, version, purpose
- All spec files have `# FDD:` title prefix
- All spec files have Prerequisite Checklist section
- All spec files have Overview section
- All spec files have Validation Criteria and Validation Checklist sections

<!-- fdd-id-content -->

---

### Requirements File Structure

- [x] **ID**: `fdd-fdd-feature-init-structure-req-requirements-structure`

<!-- fdd-id-content -->

**Status**: IMPLEMENTED

**Description**: Requirements files in requirements/ directory SHALL follow base structure plus: Scope field, MUST/MUST NOT sections, Examples section. Files SHALL be named `*-structure.md` for artifact structure specifications.

**References**:
- None (foundational requirement)

**Implements**:
- None (specification only)

**Phases**:
- [x] `ph-1`: Define requirements file structure

**Tests Covered**:
- `fdd-fdd-feature-init-structure-test-requirements-structure`

**Acceptance Criteria**:
- All requirements files have `type: requirement` in frontmatter
- All requirements files follow `*-structure.md` naming
- All requirements files have MUST/MUST NOT sections
- All requirements files have Examples section

<!-- fdd-id-content -->

---

### Workflow File Structure

- [x] **ID**: `fdd-fdd-feature-init-structure-req-workflow-structure`

<!-- fdd-id-content -->

**Status**: IMPLEMENTED

**Description**: Workflow files in workflows/ directory SHALL follow base structure plus: YAML frontmatter with description, Prerequisites section with checkboxes, Steps section with numbered actions, Next Steps section. Operation workflows have no suffix, validation workflows have -validate suffix.

**References**:
- None (foundational requirement)

**Implements**:
- None (specification only)

**Phases**:
- [x] `ph-1`: Define workflow file structure

**Tests Covered**:
- `fdd-fdd-feature-init-structure-test-workflow-structure`

**Acceptance Criteria**:
- All workflow files have `type: workflow` in frontmatter
- All workflow files have Prerequisites section with checkboxes
- All workflow files have Steps section with numbered actions
- All workflow files have Next Steps section
- Operation workflows: no suffix; Validation workflows: `-validate` suffix

<!-- fdd-id-content -->

---

### AGENTS.md File Structure

- [x] **ID**: `fdd-fdd-feature-init-structure-req-agents-structure`

<!-- fdd-id-content -->

**Status**: IMPLEMENTED

**Description**: AGENTS.md files SHALL contain ONLY navigation instructions using ALWAYS/WHEN pattern. Root AGENTS.md MAY include instruction semantics. Adapter AGENTS.md MUST use Extends field and workflow-specific WHEN clauses.

**References**:
- None (foundational requirement)

**Implements**:
- None (specification only)

**Phases**:
- [x] `ph-1`: Define AGENTS.md structure

**Tests Covered**:
- `fdd-fdd-feature-init-structure-test-agents-structure`

**Acceptance Criteria**:
- All AGENTS.md have `type: agents` in frontmatter
- AGENTS.md contains ONLY ALWAYS/WHEN navigation instructions
- All WHEN clauses reference existing files

<!-- fdd-id-content -->

---

### Makefile Structure

- [x] **ID**: `fdd-fdd-feature-init-structure-req-makefile-structure`

<!-- fdd-id-content -->

**Status**: IMPLEMENTED

**Description**: Makefile SHALL provide standard targets: test (run pytest), validate (run fdd validate), lint (check formatting), clean (remove artifacts). All targets SHALL be documented with comments.

**References**:
- None (foundational requirement)

**Implements**:
- None (specification only)

**Phases**:
- [x] `ph-1`: Define Makefile structure

**Tests Covered**:
- `fdd-fdd-feature-init-structure-test-makefile-targets`

**Acceptance Criteria**:
- Makefile has test target
- Makefile has validate target
- All targets documented

<!-- fdd-id-content -->

---

## G. Testing Scenarios

### All required directories exist

- [x] **ID**: `fdd-fdd-feature-init-structure-test-directories-exist`

<!-- fdd-id-content -->

**Validates**: `fdd-fdd-feature-init-structure-req-directory-structure`

1. [x] - `ph-1` - Check requirements/ directory exists - `inst-check-requirements-dir`
2. [x] - `ph-1` - Check workflows/ directory exists - `inst-check-workflows-dir`
3. [x] - `ph-1` - Check skills/ directory exists - `inst-check-skills-dir`
4. [x] - `ph-1` - Check tests/ directory exists - `inst-check-tests-dir`
5. [x] - `ph-1` - Check examples/ directory exists - `inst-check-examples-dir`
6. [x] - `ph-1` - Assert all directories present - `inst-assert-dirs`

<!-- fdd-id-content -->

---

### All spec files have base structure

- [x] **ID**: `fdd-fdd-feature-init-structure-test-base-structure`

<!-- fdd-id-content -->

**Validates**: `fdd-fdd-feature-init-structure-req-base-file-structure`

1. [x] - `ph-1` - Scan all .md files in requirements/ and workflows/ - `inst-scan-spec-files`
2. [x] - `ph-1` - Verify YAML frontmatter exists with `fdd: true` - `inst-verify-fdd-marker`
3. [x] - `ph-1` - Verify required fields: type, name, version, purpose - `inst-verify-required-fields`
4. [x] - `ph-1` - Verify field types: version is MAJOR.MINOR format - `inst-verify-field-types`
5. [x] - `ph-1` - Verify title format `# FDD: {Title}` - `inst-verify-title-format`
6. [x] - `ph-1` - Verify Prerequisite Checklist section exists - `inst-verify-prereq-checklist`
7. [x] - `ph-1` - Verify Overview section exists - `inst-verify-overview`
8. [x] - `ph-1` - Verify Validation Criteria section exists - `inst-verify-validation-criteria`
9. [x] - `ph-1` - Verify Validation Checklist section exists - `inst-verify-validation-checklist`
10. [x] - `ph-1` - Assert all files pass base structure check - `inst-assert-base`

<!-- fdd-id-content -->

---

### Requirements files have required sections

- [x] **ID**: `fdd-fdd-feature-init-structure-test-requirements-structure`

<!-- fdd-id-content -->

**Validates**: `fdd-fdd-feature-init-structure-req-requirements-structure`

1. [x] - `ph-1` - Scan requirements/*.md files - `inst-scan-req-files`
2. [x] - `ph-1` - Verify frontmatter has `type: requirement` - `inst-verify-type-requirement`
3. [x] - `ph-1` - Verify naming convention `*-structure.md` - `inst-verify-naming`
4. [x] - `ph-1` - Verify MUST/MUST NOT sections exist - `inst-verify-must-sections`
5. [x] - `ph-1` - Verify Examples section exists - `inst-verify-examples`
6. [x] - `ph-1` - Assert all requirements files valid - `inst-assert-req-valid`

<!-- fdd-id-content -->

---

### Workflow files have required structure

- [x] **ID**: `fdd-fdd-feature-init-structure-test-workflow-structure`

<!-- fdd-id-content -->

**Validates**: `fdd-fdd-feature-init-structure-req-workflow-structure`

1. [x] - `ph-1` - Scan workflows/*.md files - `inst-scan-workflow-files`
2. [x] - `ph-1` - Verify frontmatter has `type: workflow` - `inst-verify-type-workflow`
3. [x] - `ph-1` - Verify Prerequisites section with checkboxes - `inst-verify-prereq-checkboxes`
4. [x] - `ph-1` - Verify Steps section with numbered actions - `inst-verify-steps-numbered`
5. [x] - `ph-1` - Verify Next Steps section exists - `inst-verify-next-steps`
6. [x] - `ph-1` - Verify naming: no suffix = operation, `-validate` = validation - `inst-verify-workflow-naming`
7. [x] - `ph-1` - Assert all workflow files valid - `inst-assert-workflow-valid`

<!-- fdd-id-content -->

---

### AGENTS.md files have valid format

- [x] **ID**: `fdd-fdd-feature-init-structure-test-agents-structure`

<!-- fdd-id-content -->

**Validates**: `fdd-fdd-feature-init-structure-req-agents-structure`

1. [x] - `ph-1` - Load root AGENTS.md - `inst-load-root-agents`
2. [x] - `ph-1` - Verify frontmatter has `type: agents` - `inst-verify-type-agents`
3. [x] - `ph-1` - Verify contains ONLY ALWAYS/WHEN navigation instructions - `inst-verify-only-navigation`
4. [x] - `ph-1` - Extract all WHEN clauses - `inst-extract-clauses`
5. [x] - `ph-1` - Verify each WHEN clause references existing file - `inst-verify-refs-exist`
6. [x] - `ph-1` - Assert all AGENTS.md files valid - `inst-assert-agents-valid`

<!-- fdd-id-content -->

---

### Makefile has required targets

- [x] **ID**: `fdd-fdd-feature-init-structure-test-makefile-targets`

<!-- fdd-id-content -->

**Validates**: `fdd-fdd-feature-init-structure-req-makefile-structure`

1. [x] - `ph-1` - Load Makefile - `inst-load-makefile`
2. [x] - `ph-1` - Verify `test` target exists - `inst-verify-test-target`
3. [x] - `ph-1` - Verify `validate` target exists - `inst-verify-validate-target`
4. [x] - `ph-1` - Verify all targets have documentation comments - `inst-verify-target-docs`
5. [x] - `ph-1` - Assert Makefile valid - `inst-assert-makefile-valid`

<!-- fdd-id-content -->

---

## H. Additional Context

### Implementation Approach

This feature produces:
1. **Specification files** (core*.md) - Define structure rules
2. **Pytest tests** - Validate file existence and structure
3. **Base templates** - Skeleton files with common elements

### Relationship to Other Features

- **feature-adapter-system**: Uses core specs as base for adapter configuration
- **feature-validation-engine**: Implements validators based on these specs
- **feature-workflow-engine**: Uses workflow structure specs

### Migration Path

After implementation:
1. Run `fdd adapter` to transfer core specs to adapter
2. Adapter specs customize core rules for project
3. Specific file type features extend base templates
