# FDD Validation Workflow Execution

**Version**: 1.0  
**Purpose**: Define execution specifics for validation workflows  
**Scope**: All validation workflows (validate structure/completeness)

---

## Overview

**Validation workflows** - Fully automated procedures to validate artifacts

**This file defines**: Specific execution instructions for validation workflows

**Read after**: `workflow-execution.md` (general instructions)

**Applies when**: Workflow has `**Type**: Validation`

---

## Execution Sequence

### 1. File Existence Check

**Execute**:
1. Check target file exists at path specified in workflow
2. Check file is not empty
3. Check file is readable

**If fails**:
- STOP validation
- Report file not found or unreadable
- Suggest operation workflow to create file
- Do NOT proceed with validation

### 2. Requirements File Reading

**Read**:
1. Requirements file specified in workflow
2. Extract validation criteria sections
3. Extract scoring breakdown
4. Extract pass threshold

**MUST**:
- Use requirements file as source of truth
- Never invent validation criteria
- Follow scoring exactly as specified
- Use terminology from requirements

**MUST NOT**:
- Make up additional criteria
- Skip criteria from requirements
- Change scoring weights
- Use different terminology

### 3. Parent Artifacts Reading

**If workflow specifies parent artifacts**:
1. Read each parent artifact
2. Extract relevant IDs, concepts, types
3. Store for consistency checking
4. Store for coverage validation

**Use for**:
- Non-contradiction validation
- Coverage validation
- Cross-reference validation

### 4. Structure Validation

**Check against requirements**:
1. All required sections present
2. Section numbering correct
3. Section order correct
4. Required subsections present
5. Headers formatted correctly

**Score**: Points specified in requirements (typically 20-25)

**Report**:
- Each missing section
- Each incorrect numbering
- Each wrong order
- Each missing subsection

### 5. Completeness Validation

**Check**:
1. No placeholder markers (TODO, TBD, [Description], ...)
2. No empty sections
3. All IDs follow format from requirements
4. All IDs are unique
5. All required content present per section

**Score**: Points specified in requirements (typically 25-30)

**Report**:
- Each placeholder found
- Each empty section
- Each invalid ID format
- Each duplicate ID
- Each missing content item

### 6. Non-Contradiction Validation

**Check against parent artifacts**:
1. No contradictions with parent requirements
2. All parent concepts referenced correctly
3. No redefinition of parent types/entities
4. References use valid IDs from parent
5. No conflicting statements

**Score**: Points specified in requirements (typically 20-30)

**Report**:
- Each contradiction found
- Each incorrect reference
- Each redefined type
- Each invalid ID reference

### 7. Coverage Validation

**Check**:
1. All parent requirements addressed
2. All referenced IDs exist in parent artifacts
3. All actors/capabilities/requirements from parent covered
4. No orphaned references

**Score**: Points specified in requirements (typically 20-25)

**Report**:
- Each missing requirement coverage
- Each non-existent ID reference
- Each uncovered parent concept

### 8. Scoring and Status

**Calculate**:
1. Sum all category scores
2. Total out of 100
3. Compare to threshold from requirements
4. Determine PASS/FAIL

**Status**:
- PASS: Score ≥ threshold
- FAIL: Score < threshold

### 9. Output to Chat

**Format** (directly in chat, NO files):
```markdown
## Validation: {Artifact Name}

**Score**: {X}/100  
**Status**: PASS | FAIL  
**Threshold**: ≥{threshold}/100

---

### Findings

**Structure** ({X}/{points}):
✅ {passed item}
❌ {failed item}
❌ {failed item}

**Completeness** ({X}/{points}):
✅ {passed item}
❌ {failed item}

**Non-Contradiction** ({X}/{points}):
✅ {passed item}
❌ {failed item}

**Coverage** ({X}/{points}):
✅ {passed item}
❌ {failed item}

---

### Recommendations

**High Priority** (critical issues):
1. {Fix description}
2. {Fix description}

**Medium Priority** (important issues):
1. {Fix description}

**Low Priority** (nice-to-have):
1. {Fix description}

---

### Next Steps

{If PASS}:
✅ Validation passed! Proceed to `{next-workflow}`

{If FAIL}:
❌ Validation failed. Fix issues above, then re-run validation.
```

**MUST**:
- Output to chat only (no files)
- Show complete scoring breakdown
- List all issues by category
- Prioritize recommendations
- Suggest next workflow (PASS) or fixes (FAIL)

**MUST NOT**:
- Create validation report files
- Skip showing issues
- Proceed to next workflow if FAIL
- Output incomplete information

---

## Validation Implementation

### Using Requirements File

**Pattern**:
```
1. Open requirements/{artifact}-structure.md
2. Find "## Validation Criteria" section
3. Extract each category and points
4. Extract checklist items per category
5. Execute each check exactly as specified
6. Award points per requirements (full/partial/zero)
7. Sum total score
8. Compare to threshold from requirements
```

**Example** (from business-context-structure.md):
```markdown
## Validation Criteria

### Structure (25 points)
- All required sections present
- Section numbering correct

### Completeness (30 points)
- No placeholders
- All IDs valid
```

**Implementation**:
```
Structure validation:
- Check Section A: Vision present → 12.5 pts
- Check Section B: Actors present → 12.5 pts
- Check numbering A, B, C → full credit

Completeness validation:
- Check for [TODO] markers → 10 pts
- Check all actor IDs valid → 10 pts
- Check all capability IDs valid → 10 pts
```

### Scoring Guidelines

**Full credit**: Criterion fully satisfied
**Partial credit**: Criterion partially satisfied (if requirements allow)
**Zero credit**: Criterion not satisfied

**Example**:
- "All required sections present" → Binary (all or nothing)
- "All IDs follow format" → Could be partial (90% valid = 90% credit)

**Follow requirements**: Some criteria are binary, some allow partial credit

### Cross-Validation

**When checking parent artifacts**:
1. Read parent artifact completely
2. Build index of IDs, concepts, types
3. For each reference in current artifact:
   - Check ID exists in index
   - Check reference is correct
   - Check no contradiction
4. Report each issue found

**Example**:
```
BUSINESS.md has actor: `fdd-actor-admin`
DESIGN.md references: `fdd-actor-administrator` ❌

Issue: Actor ID mismatch
Should be: `fdd-actor-admin`
```

---

## Validation Criteria

### Requirements Following (30 points)

**Check**:
- [ ] Validation criteria from requirements file used
- [ ] Scoring breakdown from requirements followed
- [ ] No invented criteria added
- [ ] Terminology matches requirements

### Automation (25 points)

**Check**:
- [ ] No user interaction
- [ ] Fully executable by agent
- [ ] Deterministic output
- [ ] Clear pass/fail logic

### Output Quality (25 points)

**Check**:
- [ ] Output to chat only (no files)
- [ ] Complete scoring shown
- [ ] All issues listed by category
- [ ] Recommendations prioritized
- [ ] Next steps clear

### Accuracy (20 points)

**Check**:
- [ ] Correct score calculation
- [ ] All issues detected
- [ ] No false positives
- [ ] Correct pass/fail status

**Total**: 100/100

**Pass threshold**: ≥95/100

---

## Examples

**Valid execution** (PASS scenario):
```
1. Read validation workflow file
2. Target: architecture/BUSINESS.md
3. Check file exists ✓
4. Read requirements/business-context-structure.md
5. Extract validation criteria

6. Structure validation:
   - Section A: Vision ✓ (12.5 pts)
   - Section B: Actors ✓ (12.5 pts)
   - Total: 25/25 pts

7. Completeness validation:
   - No placeholders ✓ (10 pts)
   - All actor IDs valid ✓ (10 pts)
   - All capability IDs valid ✓ (10 pts)
   - Total: 30/30 pts

8. Non-Contradiction validation:
   - No parent (first artifact) ✓
   - Total: 30/30 pts

9. Coverage validation:
   - All actors in capabilities ✓ (10 pts)
   - All capabilities reference actors ✓ (10 pts)
   - Total: 20/20 pts

10. Calculate: 25+30+30+20 = 105... wait, recalc: 25+30+20+20 = 95/100
11. Threshold: ≥90/100
12. Status: PASS ✓

13. Output to chat:
## Validation: BUSINESS.md
**Score**: 95/100
**Status**: PASS
...
**Next Steps**: Proceed to `design` workflow

14. Workflow complete
```

**Valid execution** (FAIL scenario):
```
1. Read validation workflow file
2. Target: architecture/DESIGN.md
3. Check file exists ✓
4. Read requirements/overall-design-structure.md
5. Read parent: BUSINESS.md

6. Structure validation:
   - Section A missing ❌ (0 pts)
   - Section B present ✓ (10 pts)
   - Total: 10/20 pts

7. Completeness validation:
   - Found [TODO] in Section B ❌ (0 pts)
   - Found placeholder text ❌ (0 pts)
   - Requirements incomplete ❌ (0 pts)
   - Total: 0/30 pts

8. Non-Contradiction validation:
   - References actor `fdd-actor-xyz` not in BUSINESS.md ❌
   - Total: 15/25 pts

9. Coverage validation:
   - Missing capability CAP-001 ❌
   - Total: 15/25 pts

10. Calculate: 10+0+15+15 = 40/100
11. Threshold: ≥90/100
12. Status: FAIL ❌

13. Output to chat:
## Validation: DESIGN.md
**Score**: 40/100
**Status**: FAIL

### Findings
**Structure** (10/20):
❌ Section A: Architecture Overview missing
✓ Section B: Requirements present

**Completeness** (0/30):
❌ Found [TODO] marker in Section B
❌ Found placeholder text "[Description]"
❌ Requirements section incomplete

**Non-Contradiction** (15/25):
❌ References non-existent actor `fdd-actor-xyz`

**Coverage** (15/25):
❌ Missing coverage for capability CAP-001

### Recommendations
**High Priority**:
1. Add Section A: Architecture Overview
2. Remove all [TODO] markers
3. Fix actor reference to existing ID

**Medium Priority**:
1. Complete requirements section
2. Add coverage for CAP-001

### Next Steps
❌ Fix issues above, then re-run `design-validate`

14. Workflow complete
```

**Invalid execution**:
```
1. Skip file existence check ❌
2. Invent validation criteria not in requirements ❌
3. Create VALIDATION_REPORT.md file ❌
4. Suggest next workflow despite FAIL ❌
5. Skip showing detailed issues ❌
```

---

## References

**This file is referenced by**:
- MUST read WHEN executing validation workflows

**References**:
- `workflow-execution.md` - General execution instructions
- `core-workflow-validation.md` - Validation workflow structure requirements
- `core-requirements.md` - Requirements file validation format
