# Validate OpenSpec Structure

**Phase**: 3 - Feature Development  
**Purpose**: Validate OpenSpec directory structure and specifications consistency

---

## Prerequisites

- OpenSpec initialized for feature
- Feature directory exists: `architecture/features/feature-{slug}/`

## Input Parameters

- **slug**: Feature identifier (lowercase, kebab-case)

---

## Requirements

### 1: Validate Directory Structure

**Requirement**: Check OpenSpec directories exist and are correctly structured

**Validation Approach**:
```bash
cd architecture/features/feature-{slug}/

# Check main directories
if [ ! -d openspec ]; then
  echo "ERROR: openspec/ directory not found"
  echo "Run: 09-openspec-init.md {slug}"
  exit 1
fi

if [ ! -d openspec/specs ]; then
  echo "ERROR: openspec/specs/ missing"
  exit 1
fi

if [ ! -d openspec/changes ]; then
  echo "ERROR: openspec/changes/ missing"
  exit 1
fi

echo "✓ Directory structure valid"
```

**Expected Outcome**: All required directories exist

---

### 2: Validate Active Changes

**Requirement**: Check each active change has required files

**Validation Approach**:
```bash
cd openspec/changes/

# Find all change directories
CHANGES=$(find . -type d -mindepth 1 -maxdepth 1)

if [ -z "$CHANGES" ]; then
  echo "No active changes found"
  exit 0
fi

for change_dir in $CHANGES; do
  echo "Validating: $change_dir"
  
  # Check required files
  if [ ! -f "$change_dir/proposal.md" ]; then
    echo "ERROR: $change_dir missing proposal.md"
    exit 1
  fi
  
  if [ ! -f "$change_dir/tasks.md" ]; then
    echo "ERROR: $change_dir missing tasks.md"
    exit 1
  fi
  
  if [ ! -d "$change_dir/specs" ]; then
    echo "ERROR: $change_dir missing specs/ directory"
    exit 1
  fi
  
  # Check specs directory not empty
  SPEC_COUNT=$(find "$change_dir/specs" -name "*.md" | wc -l)
  if [ $SPEC_COUNT -eq 0 ]; then
    echo "WARNING: $change_dir has no spec files"
  fi
  
  echo "  ✓ Structure valid"
done

echo "✓ All changes validated"
```

**Expected Outcome**: All changes have required structure

---

### 3: Validate Change Numbering

**Requirement**: Check changes are numbered sequentially

**Validation Approach**:
```bash
# Get change numbers
CHANGE_NUMS=$(find . -type d -mindepth 1 -maxdepth 1 | sed 's|./||' | cut -d- -f1 | sort -n)

EXPECTED=1
for num in $CHANGE_NUMS; do
  # Remove leading zeros
  NUM_INT=$(echo $num | sed 's/^0*//')
  
  if [ $NUM_INT -ne $EXPECTED ]; then
    echo "ERROR: Change numbering gap - expected $EXPECTED, found $NUM_INT"
    exit 1
  fi
  
  EXPECTED=$((EXPECTED + 1))
done

echo "✓ Change numbering valid"
```

**Expected Outcome**: Sequential numbering (001, 002, 003)

---

### 4: Validate Change Status

**Requirement**: Check status consistency in proposal.md and tasks.md

**Validation Approach**:
```bash
for change_dir in $(find . -type d -mindepth 1 -maxdepth 1); do
  echo "Checking status: $change_dir"
  
  # Extract status from proposal
  PROPOSAL_STATUS=$(grep "^\*\*Status\*\*:" "$change_dir/proposal.md" | head -1 | sed 's/.*Status\*\*: //' | cut -d' ' -f1)
  
  # Extract status from tasks
  TASKS_STATUS=$(grep "^\*\*Status\*\*:" "$change_dir/tasks.md" | head -1 | sed 's/.*Status\*\*: //' | cut -d' ' -f1)
  
  if [ "$PROPOSAL_STATUS" != "$TASKS_STATUS" ]; then
    echo "ERROR: Status mismatch in $change_dir"
    echo "  proposal.md: $PROPOSAL_STATUS"
    echo "  tasks.md: $TASKS_STATUS"
    exit 1
  fi
  
  echo "  ✓ Status: $PROPOSAL_STATUS"
done

echo "✓ Status consistency validated"
```

**Expected Outcome**: Statuses match across files

---

### 5: Validate Spec Files

**Requirement**: Check spec files are valid markdown

**Validation Approach**:
```bash
for change_dir in $(find . -type d -mindepth 1 -maxdepth 1); do
  for spec in $change_dir/specs/*.md; do
    if [ -f "$spec" ]; then
      # Check file not empty
      if [ ! -s "$spec" ]; then
        echo "ERROR: Empty spec file: $spec"
        exit 1
      fi
      
      # Check has heading
      if ! grep -q "^#" "$spec"; then
        echo "WARNING: $spec has no heading"
      fi
      
      echo "  ✓ $(basename $spec)"
    fi
  done
done

echo "✓ Spec files validated"
```

**Expected Outcome**: All specs valid

---

### 6: Validate Source of Truth

**Requirement**: Check specs/ directory state

**Validation Approach**:
```bash
cd ../specs/

# Count archived specs
SPEC_COUNT=$(find . -name "*.md" -not -name "README.md" | wc -l)

echo "Source of truth: $SPEC_COUNT spec files"

# Validate each spec
for spec in *.md; do
  if [ "$spec" != "README.md" ] && [ -f "$spec" ]; then
    # Check not empty
    if [ ! -s "$spec" ]; then
      echo "ERROR: Empty spec in source of truth: $spec"
      exit 1
    fi
    
    echo "  ✓ $spec"
  fi
done

echo "✓ Source of truth validated"
```

**Expected Outcome**: Specs archived properly

---

### 7: Check for Orphaned Files

**Requirement**: Find unexpected files in openspec/

**Validation Approach**:
```bash
cd ..

# Find files not in standard locations
ORPHANS=$(find . -type f \
  ! -path "./specs/*.md" \
  ! -path "./changes/*/proposal.md" \
  ! -path "./changes/*/tasks.md" \
  ! -path "./changes/*/specs/*.md" \
  ! -path "./changes/*/COMPLETED.md" \
  ! -path "./completed/*/proposal.md" \
  ! -path "./completed/*/tasks.md" \
  ! -path "./completed/*/specs/*.md" \
  ! -path "./completed/*/COMPLETED.md")

if [ -n "$ORPHANS" ]; then
  echo "WARNING: Orphaned files found:"
  echo "$ORPHANS"
fi

echo "✓ No critical orphaned files"
```

**Expected Outcome**: No unexpected files

---

### 8: Generate Validation Report

**Requirement**: Create summary report

**Validation Approach**:
```bash
cat > VALIDATION_REPORT.md << EOF
# OpenSpec Validation Report

**Feature**: feature-{slug}  
**Date**: $(date +%Y-%m-%d)

## Structure

- ✅ Directory structure valid
- ✅ Changes directory exists
- ✅ Specs directory exists

## Active Changes

$(find changes -type d -mindepth 1 -maxdepth 1 | wc -l) active change(s)

$(for change in changes/*; do
  if [ -d "$change" ]; then
    STATUS=$(grep "^\*\*Status\*\*:" "$change/proposal.md" | head -1 | sed 's/.*Status\*\*: //')
    echo "- $(basename $change): $STATUS"
  fi
done)

## Source of Truth

$(find specs -name "*.md" -not -name "README.md" | wc -l) spec file(s) archived

## Validation

- ✅ All changes have required files
- ✅ Change numbering sequential
- ✅ Status consistency across files
- ✅ Spec files valid
- ✅ Source of truth valid

---
EOF

cat VALIDATION_REPORT.md
echo "✓ Validation report generated"
```

**Expected Outcome**: Complete validation report

---

## Completion Criteria

Validation complete when:

- [ ] Directory structure valid
- [ ] All changes have proposal.md, tasks.md, specs/
- [ ] Change numbering sequential
- [ ] Status consistent across files
- [ ] Spec files valid markdown
- [ ] Source of truth specs valid
- [ ] No critical orphaned files
- [ ] Validation report generated

---

## Common Challenges

### Issue: Missing Required Files

**Resolution**: Create missing files following templates in `09-openspec-init.md`

### Issue: Status Mismatch

**Resolution**: Synchronize status across proposal.md and tasks.md

### Issue: Empty Spec Files

**Resolution**: Fill in specs or remove empty files

---

## When to Run

**Regular Validation**:
- Before completing a change
- Before completing a feature
- During code review

**Troubleshooting**:
- When OpenSpec structure seems corrupted
- After manual changes to openspec/
- When merging branches

---

## Next Activities

After validation:

1. **Fix Issues**: Address any errors or warnings

2. **Continue Work**: If validation passes
   - Continue implementation
   - Complete changes

3. **Report**: Share validation report with team if needed

---

## References

- **Core FDD**: `../AGENTS.md` - OpenSpec integration
- **OpenSpec**: https://openspec.dev - Framework docs
- **Init Workflow**: `09-openspec-init.md` - Structure templates
