# Complete OpenSpec Change

**Phase**: 3 - Feature Development  
**Purpose**: Mark OpenSpec change as complete and archive specifications

---

## Prerequisites

- Change implemented (run `10-openspec-change-implement.md` first)
- Code validated against spec (run `10-1-openspec-code-validate.md` - runs automatically)
- All tasks in tasks.md completed
- All tests passing
- Implementation verified against specs

## Input Parameters

- **slug**: Feature identifier (lowercase, kebab-case)
- **change-id**: Change number (e.g., "001", "002")

---

## Requirements

### 1: Verify All Tasks Complete

**Requirement**: All tasks in tasks.md must be completed (100%)

**Location**: `openspec/changes/{change-name}/tasks.md` (project root)

**Validation Criteria**:
- All checklist items marked with [x]
- No items remaining with [ ]
- Task count: X/X (100%)

**Expected Outcome**: 100% tasks completed

**Resolution if Failed**: Return to workflow 10, complete remaining tasks

---

### 2: Run Final Tests

**Requirement**: Execute full test suite for final verification

**Test Coverage**:
- All unit tests for this change
- Integration tests if applicable
- Regression tests to ensure no breaking changes

**Expected Outcome**: 100% tests passing, zero failures

**Framework Examples** (reference only):
- Rust: `cargo test`
- Node.js: `npm test`
- Python: `pytest`
- Java: `mvn test`
- Go: `go test`

**Resolution if Failed**: Fix test failures before completing change

---

### 3: Verify Specs Implemented

**Requirement**: Confirm implementation matches all specifications

**Location**: `specs/` directory in change folder

**Verification Process** (for each spec file):
- Review spec requirements
- Verify all requirements implemented in code
- Check implementation behavior matches spec description
- Confirm edge cases and error handling complete

**Verification Checklist** (per spec):
- [ ] All spec requirements implemented
- [ ] Implementation tested and verified
- [ ] No deviations from specification
- [ ] Edge cases handled correctly

**Expected Outcome**: All specifications fully implemented and verified

**Resolution if Failed**: Complete missing implementation before marking change done

---

### 4: Update Change Status

**Requirement**: Mark change as COMPLETED in proposal.md

**Status Update**:
- Change status from 🔄 IN_PROGRESS to ✅ COMPLETED

**Add Completion Section** to proposal.md:
```markdown
---

## Completion

**Date**: YYYY-MM-DD  
**Status**: ✅ COMPLETED

**Verification**:
- All tasks completed (100%)
- All tests passing
- All specs implemented

---
```

**Expected Outcome**: proposal.md reflects completion

**Validation Criteria**:
- Status updated to COMPLETED
- Completion date recorded
- Verification checklist included

---

### 5: Archive Change with OpenSpec (MANDATORY)

**Requirement**: MUST use OpenSpec CLI to archive change

**⚠️ CRITICAL**: Agent MUST execute this command, not skip it

**Command**:
```bash
# Run from project root
cd {project-root}
openspec archive {change-name} -y
```

**Agent Instructions**:

⚠️ **MANDATORY**: Agent MUST call `run_command` tool with these parameters:
- `CommandLine`: `"openspec archive {change-name} -y"`
- `Cwd`: `"{project-root}"`
- `Blocking`: `True`
- `SafeToAutoRun`: `True`

**What this command does**:
- Merges delta specs to openspec/specs/
- Applies ADDED/MODIFIED/REMOVED/RENAMED operations
- Moves change to changes/archive/
- Preserves full change history

**What This Does**:
- Merges delta specs to `openspec/specs/{feature-slug}/spec.md`
- Applies ADDED/MODIFIED/REMOVED/RENAMED operations automatically
- Moves change to `changes/archive/YYYY-MM-DD-{change-name}/`
- Preserves full change history

**Expected Outcome**: Change archived, specs merged

**Verification**: 
```bash
# Change no longer in active list
openspec list

# Change in archived list  
openspec list --archived

# Specs updated
openspec list --specs
```

---

### 6: Run OpenSpec Validation (MANDATORY)

**Requirement**: MUST validate OpenSpec structure after archive

**⚠️ CRITICAL**: Agent MUST execute this command after archiving

**Command**:
```bash
cd {project-root}
openspec validate --all --no-interactive
```

**Agent Instructions**:

⚠️ **MANDATORY**: Agent MUST call `run_command` tool with these parameters:
- `CommandLine`: `"openspec validate --all --no-interactive"`
- `Cwd`: `"{project-root}"`
- `Blocking`: `True`
- `SafeToAutoRun`: `True`

**Expected**: Exit code 0 (all specs valid)

**If exit code != 0**:
1. Read error output
2. Fix reported issues (missing files, format errors, etc.)
3. Re-run validation
4. BLOCK completion until passes

**Expected Outcome**: Exit code 0, all checks pass

**Resolution if Failed**: 
1. Parse OpenSpec error output
2. Fix reported issues (missing files, format errors, etc.)
3. Re-run `openspec validate --all --no-interactive`
4. Repeat until validation passes
5. **BLOCK** workflow progression until validation succeeds

---

### 7: Update Feature DESIGN.md Section G Status

**Requirement**: Mark change as COMPLETED in Feature DESIGN.md Section G

**Location**: `architecture/features/feature-{slug}/DESIGN.md` Section G

**Update Section G**:
```markdown
## G. Implementation Plan

### Change {NUMBER}: {change-name}
**Status**: ✅ COMPLETED
**Description**: {description}
**Implements Requirements**: {requirement IDs}
**Dependencies**: {dependencies}
**Completed**: {YYYY-MM-DD}

{Keep remaining changes with their current status}
```

**Expected Outcome**: Feature DESIGN.md Section G reflects change as COMPLETED

---

### 8: Update Section F Requirements Status

**Requirement**: Mark requirements as COMPLETED in Section F for this change

**Location**: `architecture/features/feature-{slug}/DESIGN.md` Section F

**For each requirement implemented in this change**:
```markdown
## F. Requirements

### Requirement: {Requirement Title}

**Status**: ✅ COMPLETED

{Requirement description with SHALL statements}

**Testing Scenarios (FDL)**:
{FDL numbered list scenarios}

**Acceptance Criteria**:
{Criteria list}
```

**What to Update**:
- Find requirements listed in Section G under "Implements Requirements" for this change
- Update each requirement's status from 🔄 IN_PROGRESS to ✅ COMPLETED
- Requirements not in this change keep their existing status

**Expected Outcome**: Requirements in Section F show COMPLETED for those in this change

---

### 9: Clean Up (Handled by OpenSpec)

**Requirement**: Archive handles cleanup automatically

**What OpenSpec Does**:
- Moves change from `changes/` to `changes/archive/YYYY-MM-DD-{change-id}/`
- Keeps clean separation of active vs completed
- Maintains full history in archive
- Preserves all files for audit trail

**Archive Location Standard**:
- Path: `openspec/changes/archive/YYYY-MM-DD-{change-id}/`
- Format: Date prefix for chronological ordering
- Example: `changes/archive/2026-01-03-implement-core/`

**Expected Outcome**: Clean structure maintained automatically

**Note**: This is handled by `openspec archive` command, no manual action needed

---

### 10: Check Feature Status with OpenSpec

**Requirement**: Assess if feature implementation is complete

**Command**:
```bash
openspec list
```

**Status Assessment**:
- **If more changes needed**: Feature implementation continues
  - Next: Run `09-openspec-change-next.md` to create next change
  - Run `openspec list --archived` to see all completed work

- **If changes remaining**: Continue implementation
  - List shows remaining active changes
  - Prioritize next change
  - Use workflow `10-openspec-change-implement.md`

**Expected Outcome**: Clear feature completion status

**Next Steps**:
- No active changes → Complete feature (workflow 07)
- Active changes remain → Implement next change (workflow 10)

---

## Completion Criteria

Change completion verified when:

- [ ] All tasks verified complete (100%)
- [ ] Final tests passing
- [ ] All specs implemented and verified
- [ ] Change status updated to COMPLETED
- [ ] Specs archived to `openspec/specs/`
- [ ] Change archived with `openspec archive`
- [ ] Feature DESIGN.md Section G updated (change marked COMPLETED)
- [ ] Feature DESIGN.md Section F updated (requirements marked COMPLETED)
- [ ] Feature status checked

---

## Common Challenges

### Issue: Tests Failing on Final Run

**Resolution**: Fix issues before completing. Return to `10-openspec-change-implement.md`.

### Issue: Spec Not Fully Implemented

**Resolution**: Complete missing implementation. Update tasks.md and verify.

---

## After Completion

### If More Changes Needed

1. **Initialize Next Change**: Create change 002, 003, etc.
   - `mkdir openspec/changes/002-{name}`
   - Follow same structure as 001

2. **Implement Next Change**: Run `10-openspec-change-implement.md`

### If Feature Complete

1. **Complete Feature**: Run `07-complete-feature.md {slug}`
   - Marks feature as IMPLEMENTED
   - Updates FEATURES.md
   - Identifies unblocked features

---

## OpenSpec Archive Structure

After completion, structure should be:

```
openspec/
├── specs/                    # Source of truth
│   ├── api-spec.md          # Merged from changes
│   ├── database-spec.md
│   └── ...
├── completed/                # Archived changes (optional)
│   └── 001-{name}/
│       ├── proposal.md      # With completion metadata
│       ├── tasks.md         # With completion status
│       └── specs/           # Original specs
└── changes/                  # Active changes only
    └── (empty or next change)
```

---

## Next Activities

1. **If more changes**: Start next change
   - Initialize change 002+
   - Implement and complete

2. **If feature done**: Complete feature
   - Run: `07-complete-feature.md {slug}`

3. **If feature done + dependencies met**: Start dependent features
   - Check FEATURES.md for unblocked features

---

## References

- **Core FDD**: `../AGENTS.md` - Completion criteria
- **OpenSpec**: https://openspec.dev - Change management
- **Next Workflow**: `07-complete-feature.md` or next change
