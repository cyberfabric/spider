# Complete Feature

**Phase**: 3 - Feature Development  
**Purpose**: Mark feature as complete after all implementation is done

---

## Prerequisites

- Feature is IN_PROGRESS
- All OpenSpec changes implemented and archived
- All tests passing
- Feature fully functional

## Input Parameters

- **slug**: Feature identifier (lowercase, kebab-case)

---

## Requirements

### 1: Verify All Changes Complete

**Requirement**: Check no pending OpenSpec changes

**Required Actions**:
```bash
cd architecture/features/feature-{slug}/

# Check if openspec directory exists
if [ -d openspec/changes ]; then
  # Check for remaining changes
  PENDING=$(find openspec/changes -type d -mindepth 1 -maxdepth 1 | wc -l)
  
  if [ $PENDING -gt 0 ]; then
    echo "ERROR: $PENDING OpenSpec changes not complete"
    echo "Run: cd openspec/ && openspec list"
    exit 1
  fi
fi

echo "✓ All OpenSpec changes complete"
```

**Expected Outcome**: No pending changes

---

### 2: Run Final Design Validation

**Requirement**: Re-validate design one last time

**Manual Step**: Run validation workflow

**Required Actions**:
```bash
# Reference validation workflow
echo "Run: 06-validate-feature.md {slug}"
```

**Expected Outcome**: Validation passes 100/100 + 100%

---

### 3: Verify Tests

**Requirement**: Check all tests pass

**Required Actions** (framework-specific examples):
```bash
# Run feature tests
echo "Run feature tests and verify they pass"

# Example for various frameworks:
# Rust: cargo test --package {module} --lib
# Node: npm test -- {feature}
# Python: pytest tests/features/{slug}/
```

**Expected Outcome**: All tests pass

---

### 4: Verify Compilation/Build

**Requirement**: Ensure code compiles without errors

**Required Actions** (framework examples):
```bash
# Run appropriate build/check command for your framework
# Examples:
# Rust: cargo check --package {module}
# TypeScript: tsc --noEmit
# Python: mypy src/
# Java: mvn compile
# Go: go build
```

**Expected Outcome**: No compilation errors

**Critical**: This step prevents marking incomplete work as done

---

### 5: Update FEATURES.md Status

**Requirement**: Mark feature as IMPLEMENTED

**Required Actions**:
```bash
cd ../../

# Update status from IN_PROGRESS to IMPLEMENTED
sed -i.bak "/^### .*feature-{slug}/,/^###/s/🔄 IN_PROGRESS/✅ IMPLEMENTED/" FEATURES.md

# Verify change
if grep -A 1 "feature-{slug}" FEATURES.md | grep -q "IMPLEMENTED"; then
  echo "✓ Feature marked as IMPLEMENTED"
else
  echo "ERROR: Status update failed"
  exit 1
fi
```

**Expected Outcome**: Status updated to IMPLEMENTED

---

### 6: Identify Unblocked Features

**Requirement**: Check which features can now start

**Required Actions**:
```bash
# Find features that depend on this one
echo "Features that can now start:"
grep -B 5 "Depends On:.*{slug}" FEATURES.md | grep "^###" | sed 's/### //'

# Check if their other dependencies are also met
echo ""
echo "Verify all dependencies for each feature before starting"
```

**Expected Outcome**: List of potentially unblocked features

---

### 7: Verify OpenSpec Structure

**Requirement**: Confirm changes archived properly

**Required Actions**:
```bash
cd features/feature-{slug}/

if [ -d openspec ]; then
  echo "OpenSpec structure:"
  ls -la openspec/
  
  # Verify specs/ exists (source of truth)
  if [ ! -d openspec/specs ]; then
    echo "WARNING: openspec/specs/ missing"
  fi
  
  # Verify changes/ is empty
  if [ -d openspec/changes ] && [ "$(ls -A openspec/changes)" ]; then
    echo "WARNING: openspec/changes/ not empty"
  fi
  
  echo "✓ OpenSpec structure valid"
fi
```

**Expected Outcome**: Specs archived, changes empty

---

### 8: Add Completion Note

**Requirement**: Document completion in DESIGN.md

**Required Actions**:
```bash
# Get current date
COMPLETION_DATE=$(date +%Y-%m-%d)

# Count changes
if [ -d openspec/specs ]; then
  CHANGE_COUNT=$(find openspec/specs -name "*.md" | wc -l)
else
  CHANGE_COUNT=0
fi

# Add completion note
cat >> DESIGN.md << EOF

---

## Implementation Complete

**Date**: $COMPLETION_DATE  
**All Changes**: $CHANGE_COUNT changes implemented and archived  
**Status**: ✅ IMPLEMENTED
EOF

echo "✓ Completion note added to DESIGN.md"
```

**Expected Outcome**: Completion note added

---

## Completion Criteria

Feature completion verified when:

- [ ] All OpenSpec changes completed
- [ ] Design validation passes (100/100 + 100%)
- [ ] Tests passing
- [ ] Code compiles without errors
- [ ] FEATURES.md status = IMPLEMENTED
- [ ] Dependent features identified
- [ ] OpenSpec structure valid (changes archived)
- [ ] Completion note in DESIGN.md

---

## Common Challenges

### Issue: Tests Failing

**Resolution**: Fix tests before marking complete. Feature is not done if tests fail.

### Issue: OpenSpec Changes Not Archived

**Resolution**: Complete and archive remaining changes:
```bash
cd openspec/
openspec complete {change-id}
```

---

## Next Activities

After completing feature:

1. **Review FEATURES.md**: Check for next feature to implement
   - Look at implementation order
   - Verify dependencies met

2. **Start Next Feature**: Run `05-init-feature.md {next-slug}`
   - Or start dependent feature that's now unblocked

3. **Update Documentation**: If needed
   - Update Overall Design
   - Update architecture diagrams

---

## References

- **Core FDD**: `../AGENTS.md` - Completion criteria
- **Next Workflow**: `05-init-feature.md` for next feature
