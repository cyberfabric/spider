# Create Next OpenSpec Change

**Phase**: 3 - Feature Implementation  
**Purpose**: Create next change from Feature DESIGN.md implementation plan

---

## Prerequisites

- OpenSpec initialized for feature
- Previous change completed and archived
- Feature DESIGN.md Section F has multiple changes planned
- At least one change remaining to implement

## Input Parameters

- **slug**: Feature identifier (lowercase, kebab-case)
- **next-change-name**: Name for next change from DESIGN.md Section F

---

## Requirements

### 1: Identify Next Change from Feature Design

**Requirement**: Review Feature DESIGN.md Section F for next planned change

**Location**: `architecture/features/feature-{slug}/DESIGN.md`

**Review Section F**:
```markdown
## F. Validation & Implementation

### OpenSpec Changes

**Total Changes**: {Number}

#### Change 001: {Completed}
**Status**: ✅ COMPLETED

#### Change 002: {Next to implement}
**Status**: ⏳ NOT_STARTED
...
```

**Manual Step**: Identify next NOT_STARTED change from plan

**Expected Outcome**: Clear understanding of what next change implements

---

### 2: Create Change Directory Structure

**Requirement**: Manually create change directory

**Commands**:
```bash
cd architecture/features/feature-{slug}/openspec/
mkdir -p changes/{next-change-name}/specs
```

**What This Does**:
- Creates `changes/{next-change-name}/` directory
- Creates `specs/` subdirectory for delta specifications

**Expected Outcome**: Change directory structure created

**Note**: OpenSpec does not have a `create` command. Changes are created manually.

---

### 3: Create Proposal Document

**Requirement**: Write proposal.md following OpenSpec format

**Location**: `openspec/changes/{next-change-name}/proposal.md`

**Required Structure** (OpenSpec standard):
```markdown
# Change: {Brief description of change}

## Why
{1-2 sentences on problem/opportunity}

## What Changes
- {Bullet list of changes}
- {Mark breaking changes with **BREAKING**}

## Impact
- Affected specs: {list capabilities}
- Affected code: {key files/systems}
```

**Content Source**: Extract from `../../DESIGN.md` Section F for this specific change

**Expected Outcome**: Proposal created with proper OpenSpec format

**Note**: Use OpenSpec standard format, not custom templates

---

### 4: Create Tasks Checklist

**Requirement**: Write tasks.md with implementation steps

**Location**: `openspec/changes/{next-change-name}/tasks.md`

**Required Structure** (OpenSpec standard):
```markdown
## 1. Implementation
- [ ] 1.1 {Task from DESIGN.md}
- [ ] 1.2 {Task from DESIGN.md}
- [ ] 1.3 {Task from DESIGN.md}
- [ ] 1.4 Write tests
```

**Guidelines**:
- Number tasks sequentially
- Break down into specific, actionable items
- Include testing and documentation tasks
- Extract tasks from DESIGN.md Section F for this change

**Expected Outcome**: Clear implementation checklist

---

### 5: Create Delta Specifications

**Requirement**: Write delta specs using OpenSpec format

**Location**: `openspec/changes/{next-change-name}/specs/{capability}/spec.md`

**Delta Operations** (use these headers):
- `## ADDED Requirements` - New capabilities
- `## MODIFIED Requirements` - Changed behavior
- `## REMOVED Requirements` - Deprecated features
- `## RENAMED Requirements` - Name changes

**Required Format**:
```markdown
## ADDED Requirements
### Requirement: New Feature
The system SHALL provide...

#### Scenario: Success case
- **WHEN** user performs action
- **THEN** expected result
```

**Critical Rules**:
- Every requirement MUST have at least one `#### Scenario:`
- Use `**WHEN**` and `**THEN**` in scenarios
- Use SHALL/MUST for normative requirements
- For MODIFIED: copy full requirement from `openspec/specs/`, then edit

**Content Source**: Extract from Feature DESIGN.md Section E (Technical Details) and Section F

**Expected Outcome**: Delta specs created per affected capability

---

### 6: Create design.md (Optional)

**Requirement**: Create design.md only if needed

**Location**: `openspec/changes/{next-change-name}/design.md`

**Create design.md if ANY apply**:
- Cross-cutting change (multiple services/modules)
- New external dependency
- Significant data model changes
- Security, performance, or migration complexity
- Technical decisions needed before coding

**Otherwise**: Skip this file

**Minimal Structure**:
```markdown
## Context
{Background, constraints}

## Goals / Non-Goals
- Goals: {...}
- Non-Goals: {...}

## Decisions
- Decision: {What and why}
- Alternatives: {Options + rationale}

## Risks / Trade-offs
- {Risk} → Mitigation

## Migration Plan
{Steps, rollback}
```

**Note**: Feature DESIGN.md is at `../../DESIGN.md` - reference it, don't duplicate

**Expected Outcome**: design.md created only if complexity requires it

---

### 7: Validate with OpenSpec

**Requirement**: Validate change structure and specs

**Command**:
```bash
openspec validate {next-change-name} --strict
```

**What This Checks**:
- Change has at least one delta
- All requirements have scenarios
- Scenario format correct (`#### Scenario:`)
- Files not empty
- Delta operations properly formatted

**Expected Outcome**: Validation passes with zero errors

**Resolution if Failed**: Fix reported issues, then re-validate

---

### 8: Update Feature DESIGN.md Status

**Requirement**: Mark change as ready for implementation in Feature DESIGN.md

**Location**: `../../DESIGN.md`

**Update Section F**:
```markdown
## F. Validation & Implementation

### OpenSpec Changes

See `openspec/changes/` for implementation details:
- `{previous-change}` - ✅ COMPLETED
- `{next-change-name}` - ⏳ NOT_STARTED (ready)
- `{future-change}` - ⏳ NOT_STARTED
```

**Expected Outcome**: Feature DESIGN.md reflects current implementation status

---

## Completion Criteria

Next change creation complete when:

- [ ] Next change identified from DESIGN.md Section F
- [ ] `openspec/changes/{next-change-name}/` created manually
- [ ] `proposal.md` follows OpenSpec format (Why, What Changes, Impact)
- [ ] `tasks.md` has numbered implementation checklist
- [ ] Delta specs created in `specs/{capability}/spec.md` with ADDED/MODIFIED/etc
- [ ] Each requirement has at least one `#### Scenario:`
- [ ] `design.md` created if complexity requires it (optional)
- [ ] `openspec validate {next-change-name} --strict` passes
- [ ] Feature DESIGN.md Section F updated with change status
- [ ] Ready to start implementation (workflow 10)

---

## Common Challenges

### Issue: Unclear Which Change to Create Next

**Resolution**: Review DESIGN.md Section F implementation plan. Changes should be ordered by dependencies. If order unclear, implement foundational changes first (data model, core logic, then UI/API).

### Issue: Change Plan Changed Since Design

**Resolution**: If implementation reveals changes need to be different:
1. Use workflow 08 (fix-design) to update DESIGN.md Section F
2. Re-validate Feature Design
3. Then create change with updated plan

### Issue: Multiple Changes Could Be Next

**Resolution**: Choose based on:
- Dependency order (prerequisites first)
- Risk level (higher risk earlier for feedback)
- Team capacity (parallel work if independent)

---

## Next Activities

After creating next change:

1. **Implement Change**: Run `10-openspec-change-implement.md`
   - Follow implementation workflow
   - Complete all tasks in tasks.md

2. **Complete When Done**: Run `11-openspec-change-complete.md`
   - Archive change
   - Merge specs

3. **Repeat if Needed**: If more changes remain
   - Run this workflow again for next change
   - Or run `13-openspec-validate.md` to check overall structure

4. **Complete Feature**: When all changes done
   - Run `07-complete-feature.md`
   - Mark feature as IMPLEMENTED

---

## Best Practices

**Change Extraction**:
- Copy implementation details directly from DESIGN.md Section F
- Don't make up new requirements - follow design
- If design is insufficient, fix design first (workflow 08)

**Change Scope**:
- Each change should be completable in 4-8 hours
- If too large, break into multiple changes
- If too small, consider combining with next

**Dependencies**:
- Check if change depends on previous changes being deployed
- Document dependencies in proposal.md Impact section
- Order changes by dependency graph

---

## References

- **Core FDD**: `../AGENTS.md` - OpenSpec integration
- **Feature Design**: `../../DESIGN.md` - Section F implementation plan
- **Previous Workflow**: `11-openspec-change-complete.md` - Complete previous change
- **Next Workflow**: `10-openspec-change-implement.md` - Implement this change
- **OpenSpec Docs**: `../openspec/AGENTS.md` - Full OpenSpec specification
