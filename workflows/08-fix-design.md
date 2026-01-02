# Fix Design Issue

**Phase**: 3 - Feature Development  
**Purpose**: Fix design issues discovered during implementation

---

## Prerequisites

- Feature is IN_PROGRESS or IMPLEMENTED
- Design issue identified (missing detail, incorrect logic, etc.)
- Feature directory exists: `architecture/features/feature-{slug}/`

## Input Parameters

- **slug**: Feature identifier (lowercase, kebab-case)
- **issue**: Description of design issue to fix

---

## Requirements

### 1: Document Issue

**Requirement**: Create issue description before making changes

**Required Actions**:
```bash
cd architecture/features/feature-{slug}/

# Create or append to DESIGN_ISSUES.md
cat >> DESIGN_ISSUES.md << EOF

---

## Issue: {Brief Description}

**Date**: $(date +%Y-%m-%d)  
**Discovered During**: {Implementation phase}

### Problem

{Detailed description of what's wrong or missing}

### Impact

{What this affects - implementation, testing, etc.}

### Proposed Solution

{How to fix it}

---
EOF

echo "✓ Issue documented"
```

**Expected Outcome**: Issue recorded

---

### 2: Update DESIGN.md

**Requirement**: Make necessary changes to design document

**Manual Step**: Edit DESIGN.md to fix the issue

**Guidelines**:
- Update relevant sections (A-F)
- Maintain section structure
- Keep ADL syntax in Section C
- Update OpenSpec changes if needed

**Example Changes**:
- Add missing actor flow (Section B)
- Clarify algorithm steps (Section C)
- Add missing technical details (Section E)
- Define new error cases

---

### 3: Validate Updated Design

**Requirement**: Re-run design validation

**Required Actions**:
```bash
# Reference validation workflow
echo "Run validation: 06-validate-feature.md {slug}"

# Manual execution
cd ../../
# Follow validation steps
```

**Expected Outcome**: Validation passes 100/100

---

### 4: Update OpenSpec if Needed

**Requirement**: Create new change if implementation must change

**Required Actions**:
```bash
cd architecture/features/feature-{slug}/

# Check if implementation changes needed
if [ -d openspec ]; then
  echo "Consider if new OpenSpec change needed for implementation updates"
  echo "If yes, run: 09-openspec-init.md {slug}"
fi
```

**Expected Outcome**: OpenSpec updated if implementation affected

**Note**: Design clarifications may not require code changes

---

### 5: Document Resolution

**Requirement**: Record how issue was resolved

**Required Actions**:
```bash
# Update issue with resolution
cat >> DESIGN_ISSUES.md << EOF

### Resolution

**Date**: $(date +%Y-%m-%d)

{Describe what was changed in DESIGN.md}

**Changes Made**:
- Section B: {changes}
- Section C: {changes}
- Section E: {changes}

**Validation**: ✅ Passed (100/100)

**Implementation Impact**: {None/Minor/Major}

---
EOF

echo "✓ Resolution documented"
```

**Expected Outcome**: Complete issue record

---

### 6: Notify Team (Optional)

**Requirement**: If working in team, notify about design changes

**Manual Step**: 
- Update team via communication channel
- Review changes with stakeholders if significant
- Update documentation references if needed

---

## Completion Criteria

Design fix complete when:

- [ ] Issue documented in DESIGN_ISSUES.md
- [ ] DESIGN.md updated to fix issue
- [ ] Design validation passes (100/100)
- [ ] OpenSpec updated if implementation affected
- [ ] Resolution documented
- [ ] Team notified (if applicable)

---

## Common Challenges

### Issue: Validation Fails After Changes

**Resolution**: Review validation errors, fix issues iteratively. May need multiple update cycles.

### Issue: Breaking Changes to Implementation

**Resolution**: Create new OpenSpec change to handle implementation updates. May need to revert some code.

### Issue: Unclear What to Fix

**Resolution**: Consult with team, review Overall Design, check similar features for patterns.

---

## Design Issue Categories

### 1. Missing Detail

**Example**: Actor flow too vague  
**Fix**: Add detailed steps, error scenarios

### 2. Incorrect Logic

**Example**: Algorithm has logical flaw  
**Fix**: Rewrite algorithm in Section C

### 3. Incomplete Technical Details

**Example**: Security requirements missing  
**Fix**: Add to Section E

### 4. Scope Creep

**Example**: Feature trying to do too much  
**Fix**: Split into multiple features, update FEATURES.md

### 5. Missing Error Cases

**Example**: No handling for edge case  
**Fix**: Add error scenarios to Section B, update Section E

---

## When to Fix vs Start Over

**Fix Design (this workflow)**:
- Minor clarifications
- Adding missing details
- Fixing logical errors
- Improving existing content

**Start New Feature**:
- Major scope change
- Complete redesign
- Different approach entirely
- Would invalidate most of current design

---

## Next Activities

After fixing design:

1. **Continue Implementation**: If in progress
   - Apply design changes to code
   - Update tests if needed
   - Complete remaining work

2. **Re-implement**: If major changes
   - May need to refactor code
   - Update OpenSpec changes
   - Re-run tests

3. **Complete Feature**: After fixes applied
   - Run: `07-complete-feature.md {slug}`

---

## References

- **Core FDD**: `../AGENTS.md` - Design iteration
- **Validation**: `06-validate-feature.md` - Re-validate after changes
- **OpenSpec**: `09-openspec-init.md` - If implementation needs updates
