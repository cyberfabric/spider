# Business Context

## A. Vision

**Purpose**: Provide a lightweight framework for creating and validating structured architecture artifacts.

This system defines a small set of artifacts and rules.

**Target Users**:
- Architects
- Developers

**Key Problems Solved**:
- Missing structure in architecture docs
- Inconsistent cross-references between artifacts

**Success Criteria**:
- Validation reports are deterministic
- Cross-references resolve without manual hunting

## B. Actors

### Human Actors

#### Architect

**ID**: `fdd-demo-actor-architect`

<!-- fdd-id-content -->
**Role**: Creates and updates architecture artifacts.
<!-- fdd-id-content -->

### System Actors

#### Validator

**ID**: `fdd-demo-actor-validator`

<!-- fdd-id-content -->
**Role**: Validates artifacts and reports issues.
<!-- fdd-id-content -->

## C. Capabilities

#### Artifact Validation

**ID**: `fdd-demo-capability-artifact-validation`

<!-- fdd-id-content -->
- Validate artifact structure
- Validate ID formatting

**Actors**: `fdd-demo-actor-architect`, `fdd-demo-actor-validator`
<!-- fdd-id-content -->

## D. Use Cases

#### UC-001: Validate an Artifact

**ID**: `fdd-demo-usecase-validate-artifact`

<!-- fdd-id-content -->
**Actor**: `fdd-demo-actor-architect`

**Preconditions**: Artifact file exists

**Flow**:
1. Architect runs validation
2. System reports issues

**Postconditions**: Issues are visible and actionable
<!-- fdd-id-content -->
