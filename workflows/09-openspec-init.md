# Initialize OpenSpec for Feature

**Phase**: 3 - Feature Development  
**Purpose**: Create OpenSpec structure and first change for feature implementation

---

## Prerequisites

- Feature DESIGN.md validated (100/100 + 100%)
- Feature status IN_PROGRESS
- Feature directory exists: `architecture/features/feature-{slug}/`

## Input Parameters

- **slug**: Feature identifier (lowercase, kebab-case)
- **change-name**: Name for first change (e.g., "implement-core")

---

## Requirements

### 1: Create OpenSpec Directory Structure

**Requirement**: Initialize openspec directories

**Required Structure**:
```bash
cd architecture/features/feature-{slug}/

# Create directory structure
mkdir -p openspec/specs
mkdir -p openspec/changes

echo "✓ OpenSpec structure created"
```

**Expected Outcome**: Directory structure exists

---

### 2: Initialize Specs Directory

**Requirement**: Create placeholder for source of truth specs

**Required Structure**:
```bash
cat > openspec/specs/README.md << 'EOF'
# OpenSpec Specs - Source of Truth

This directory contains the **source of truth** specifications after changes are merged.

## Structure

Each spec file represents a completed change's specifications:
- `{spec-name}.md` - Specification document

## Workflow

1. Changes start in `changes/{id}-{name}/specs/`
2. After implementation and validation, specs are merged here
3. This becomes the authoritative source

## Status

Empty initially - specs will be added as changes complete.
EOF

echo "✓ Specs directory initialized"
```

**Expected Outcome**: README created

---

### 3: Create First Change

**Requirement**: Initialize change 001

**Required Structure**:
```bash
# Create change directory
mkdir -p openspec/changes/001-{change-name}
cd openspec/changes/001-{change-name}

# Create subdirectories
mkdir -p specs

echo "✓ Change 001 structure created"
```

**Expected Outcome**: Change directory exists

---

### 4: Create Proposal Document

**Requirement**: Generate proposal.md for the change

**Required Structure**:
```bash
cat > proposal.md << 'EOF'
# Change 001: {Change Name}

**Status**: ⏳ NOT_STARTED  
**Feature**: feature-{slug}  
**Created**: $(date +%Y-%m-%d)

---

## Overview

{Brief description of what this change implements}

## Scope

**In Scope**:
- Item 1
- Item 2

**Out of Scope**:
- Item 1
- Item 2

## Dependencies

{List dependencies or "None"}

## Effort Estimate

**Estimated Time**: {Hours}

---

## Implementation Plan

### Phase 1: {Phase Name}

Steps:
1. Step 1
2. Step 2

### Phase 2: {Phase Name}

Steps:
1. Step 1
2. Step 2

---

## Testing Strategy

**Unit Tests**:
- Test 1
- Test 2

**Integration Tests**:
- Test 1
- Test 2

---

## Verification Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] All tests pass
- [ ] Documentation updated

---
EOF

echo "✓ Proposal document created"
```

**Expected Outcome**: proposal.md exists

---

### 5: Create Tasks Document

**Requirement**: Generate tasks.md with implementation checklist

**Required Structure**:
```bash
cat > tasks.md << 'EOF'
# Implementation Tasks - Change 001

**Status**: ⏳ NOT_STARTED

---

## Task Checklist

### Setup
- [ ] Review proposal.md
- [ ] Review specs
- [ ] Prepare environment

### Implementation
- [ ] Task 1: {Description}
- [ ] Task 2: {Description}
- [ ] Task 3: {Description}

### Testing
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] All tests passing

### Documentation
- [ ] Code comments
- [ ] Update README if needed
- [ ] Document any gotchas

### Verification
- [ ] Manual testing
- [ ] Code review (if applicable)
- [ ] Performance check

---

## Notes

{Any implementation notes or decisions}

---
EOF

echo "✓ Tasks document created"
```

**Expected Outcome**: tasks.md exists

---

### 6: Create Initial Spec Files

**Requirement**: Create spec placeholders based on DESIGN.md Section F

**Manual Step**: Extract specs from DESIGN.md Section F

**Required Structure**:
```bash
# Example: Create spec files for different aspects
cat > specs/api-spec.md << 'EOF'
# API Specification

{Describe API changes/additions}

## Endpoints

### Endpoint 1

**Method**: GET/POST/etc  
**Path**: `/api/v1/{path}`

**Request**:
\`\`\`json
{request example}
\`\`\`

**Response**:
\`\`\`json
{response example}
\`\`\`

---
EOF

# Add more specs as needed:
# - database-spec.md (schema changes)
# - integration-spec.md (external integrations)
# - security-spec.md (auth/authz)

echo "✓ Initial spec files created"
```

**Expected Outcome**: Spec files exist in `specs/`

---

### 7: Update Feature DESIGN.md

**Requirement**: Reference OpenSpec in Section F

**Required Structure**:
```bash
cd ../../../

# Verify Section F references OpenSpec
if ! grep -q "openspec" DESIGN.md; then
  echo "WARNING: DESIGN.md Section F should reference openspec/"
  echo "Add: See openspec/changes/001-{change-name}/ for implementation details"
fi

echo "✓ DESIGN.md check complete"
```

**Expected Outcome**: Section F links to OpenSpec

---

## Completion Criteria

OpenSpec initialization complete when:

- [ ] `openspec/specs/` directory exists
- [ ] `openspec/changes/001-{change-name}/` created
- [ ] `proposal.md` created with implementation plan
- [ ] `tasks.md` created with checklist
- [ ] Spec files created in `changes/001-{change-name}/specs/`
- [ ] DESIGN.md Section F references OpenSpec
- [ ] Ready to start implementation

---

## Common Challenges

### Issue: Too Many Tasks

**Resolution**: Break change into smaller changes (001, 002, etc.). Each change should be completable in 4-8 hours.

### Issue: Unclear Specs

**Resolution**: Return to DESIGN.md, clarify Section E (Technical Details). Specs should be unambiguous.

---

## Next Activities

After OpenSpec initialization:

1. **Review Proposal**: Ensure implementation plan is clear
   - Verify scope
   - Check dependencies
   - Validate effort estimate

2. **Start Implementation**: Run `10-openspec-change-implement.md`
   - Follow tasks.md checklist
   - Implement according to specs
   - Test as you go

3. **Track Progress**: Update tasks.md as work progresses

---

## OpenSpec Best Practices

**Changes Should Be**:
- **Atomic**: Self-contained unit of work
- **Traceable**: Clear what changed and why
- **Testable**: Verification criteria defined
- **Reversible**: Can be undone if needed

**Specs Should Be**:
- **Precise**: No ambiguity
- **Complete**: All details specified
- **Consistent**: Align with DESIGN.md
- **Reviewable**: Easy to validate

---

## References

- **Core FDD**: `../AGENTS.md` - OpenSpec integration
- **OpenSpec Docs**: https://openspec.dev - Full OpenSpec framework
- **Next Workflow**: `10-openspec-change-implement.md`
