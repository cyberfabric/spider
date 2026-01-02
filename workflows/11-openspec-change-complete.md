# Complete OpenSpec Change

**Phase**: 3 - Feature Development  
**Purpose**: Mark OpenSpec change as complete and archive specifications

---

## Prerequisites

- Change implemented (run `10-openspec-change-implement.md` first)
- All tasks in tasks.md completed
- All tests passing
- Implementation verified against specs

## Input Parameters

- **slug**: Feature identifier (lowercase, kebab-case)
- **change-id**: Change number (e.g., "001", "002")

---

## Requirements

### 1: Verify All Tasks Complete

**Requirement**: Check tasks.md is 100% done

**Required Actions**:
```bash
cd architecture/features/feature-{slug}/openspec/changes/{change-id}-*/

# Count tasks
TOTAL=$(grep -c "^- \[" tasks.md)
DONE=$(grep -c "^- \[x\]" tasks.md)

if [ $DONE -ne $TOTAL ]; then
  echo "ERROR: Only $DONE/$TOTAL tasks complete"
  echo "Incomplete tasks:"
  grep "^- \[ \]" tasks.md
  exit 1
fi

echo "✓ All tasks complete ($DONE/$TOTAL)"
```

**Expected Outcome**: 100% tasks done

---

### 2: Run Final Tests

**Requirement**: Execute full test suite one last time

**Examples** (framework-specific):
```bash
echo "Run your framework's test command"
echo "Example: cargo test, npm test, pytest"
```

**Expected Outcome**: All tests pass

---

### 3: Verify Specs Implemented

**Requirement**: Manual verification against each spec

**Required Actions**:
```bash
# List all specs
echo "Verifying specs:"
ls specs/

for spec in specs/*.md; do
  echo ""
  echo "=== $(basename $spec) ==="
  cat "$spec"
  echo ""
  read -p "Spec fully implemented? (y/n) " answer
  if [ "$answer" != "y" ]; then
    echo "ERROR: Spec not fully implemented"
    exit 1
  fi
done

echo "✓ All specs verified"
```

**Expected Outcome**: All specifications implemented

---

### 4: Update Change Status

**Requirement**: Mark change as COMPLETED

**Required Actions**:
```bash
# Update proposal
sed -i.bak 's/🔄 IN_PROGRESS/✅ COMPLETED/' proposal.md

# Add completion date
cat >> proposal.md << EOF

---

## Completion

**Date**: $(date +%Y-%m-%d)  
**Status**: ✅ COMPLETED

**Verification**:
- All tasks completed (100%)
- All tests passing
- All specs implemented

---
EOF

echo "✓ Change marked as COMPLETED"
```

**Expected Outcome**: proposal.md updated

---

### 5: Archive Specs to Source of Truth

**Requirement**: Merge specs to `openspec/specs/`

**Required Actions**:
```bash
cd ../../..  # Back to feature directory

# Copy specs to source of truth
CHANGE_NAME=$(basename openspec/changes/{change-id}-*)

for spec in openspec/changes/{change-id}-*/specs/*.md; do
  SPEC_NAME=$(basename "$spec")
  
  # If spec exists, append change info
  if [ -f "openspec/specs/$SPEC_NAME" ]; then
    echo "" >> "openspec/specs/$SPEC_NAME"
    echo "---" >> "openspec/specs/$SPEC_NAME"
    echo "Updated by: $CHANGE_NAME" >> "openspec/specs/$SPEC_NAME"
    cat "$spec" >> "openspec/specs/$SPEC_NAME"
  else
    # New spec
    cat > "openspec/specs/$SPEC_NAME" << EOF
# $(basename "$SPEC_NAME" .md)

**Source**: $CHANGE_NAME  
**Date**: $(date +%Y-%m-%d)

---

EOF
    cat "$spec" >> "openspec/specs/$SPEC_NAME"
  fi
  
  echo "Archived: $SPEC_NAME"
done

echo "✓ Specs archived to source of truth"
```

**Expected Outcome**: Specs in `openspec/specs/`

---

### 6: Create Completed Metadata

**Requirement**: Add completion record

**Required Actions**:
```bash
cd openspec/changes/{change-id}-*/

cat > COMPLETED.md << EOF
# Change Completed

**Change**: {change-id}-{name}  
**Feature**: feature-{slug}  
**Completed**: $(date +%Y-%m-%d)

## Summary

{Brief summary of what was implemented}

## Specs Archived

$(ls specs/*.md | sed 's/specs\//- /')

## Verification

- ✅ All tasks completed
- ✅ All tests passing
- ✅ All specs implemented
- ✅ Specs archived to source of truth

---
EOF

echo "✓ Completion record created"
```

**Expected Outcome**: COMPLETED.md exists

---

### 7: Move to Completed (Optional)

**Requirement**: Organize completed changes

**Required Actions**:
```bash
cd ../..  # Back to openspec/

# Create completed directory if needed
mkdir -p completed

# Move change to completed
mv changes/{change-id}-* completed/

echo "✓ Change moved to completed/"
```

**Expected Outcome**: Change in `openspec/completed/`

**Note**: This step is optional - some prefer keeping changes in place

---

### 8: Update Feature Status

**Requirement**: Check if feature is complete

**Required Actions**:
```bash
cd ../../..  # Back to features/

# Check if more changes needed
REMAINING=$(find feature-{slug}/openspec/changes -type d -mindepth 1 -maxdepth 1 2>/dev/null | wc -l)

if [ $REMAINING -eq 0 ]; then
  echo "✅ All changes complete - feature ready to complete"
  echo "Run: 07-complete-feature.md {slug}"
else
  echo "⏳ $REMAINING changes remaining"
  find feature-{slug}/openspec/changes -type d -mindepth 1 -maxdepth 1
fi
```

**Expected Outcome**: Status update

---

## Completion Criteria

Change completion verified when:

- [ ] All tasks verified complete (100%)
- [ ] Final tests passing
- [ ] All specs implemented and verified
- [ ] Change status updated to COMPLETED
- [ ] Specs archived to `openspec/specs/`
- [ ] Completion record created (COMPLETED.md)
- [ ] Change moved to completed/ (optional)
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
│       ├── proposal.md
│       ├── tasks.md
│       ├── COMPLETED.md
│       └── specs/
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
