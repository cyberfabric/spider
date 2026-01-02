# Implement OpenSpec Change

**Phase**: 3 - Feature Development  
**Purpose**: Implement OpenSpec change according to specifications

---

## Prerequisites

- OpenSpec initialized for feature (run `09-openspec-init.md` first)
- Change directory exists: `architecture/features/feature-{slug}/openspec/changes/{id}-{name}/`
- Proposal and specs reviewed

## Input Parameters

- **slug**: Feature identifier (lowercase, kebab-case)
- **change-id**: Change number (e.g., "001", "002")

---

## Requirements

### 1: Navigate to Change Directory

**Requirement**: Enter change directory

**Required Actions**:
```bash
cd architecture/features/feature-{slug}/openspec/changes/{change-id}-*/

echo "Current change: $(basename $(pwd))"
ls -la
```

**Expected Outcome**: In change directory, see proposal.md, tasks.md, specs/

---

### 2: Review Proposal and Specs

**Requirement**: Read all specification documents

**Required Actions**:
```bash
# Review proposal
echo "=== PROPOSAL ==="
cat proposal.md

# Review specs
echo ""
echo "=== SPECS ==="
ls specs/
for spec in specs/*.md; do
  echo ""
  echo "--- $spec ---"
  cat "$spec"
done
```

**Expected Outcome**: Clear understanding of what to implement

**Manual Step**: Ensure you understand:
- Implementation scope
- Technical requirements
- Testing criteria

---

### 3: Update Status to IN_PROGRESS

**Requirement**: Mark change as started

**Required Actions**:
```bash
# Update proposal status
sed -i.bak 's/⏳ NOT_STARTED/🔄 IN_PROGRESS/' proposal.md

# Update tasks
sed -i.bak 's/⏳ NOT_STARTED/🔄 IN_PROGRESS/' tasks.md

echo "✓ Status updated to IN_PROGRESS"
```

**Expected Outcome**: Status changed in both files

---

### 4: Implement According to Specs

**Requirement**: Write code following specifications

**Manual Step**: Implement the change

**Guidelines**:
- Follow specs exactly
- Implement incrementally (task by task)
- Update tasks.md checklist as you complete items
- Write tests alongside code
- Commit frequently with clear messages

---

### 5: Update Tasks Checklist

**Requirement**: Mark completed tasks

**Required Actions**:
```bash
# Example: Mark task as done
# Replace "- [ ] Task 1" with "- [x] Task 1"

# Check progress
TOTAL=$(grep -c "^- \[" tasks.md)
DONE=$(grep -c "^- \[x\]" tasks.md)
PROGRESS=$((DONE * 100 / TOTAL))

echo "Progress: $DONE/$TOTAL tasks ($PROGRESS%)"
```

**Expected Outcome**: Checklist tracks progress

**Validation**: Update after each significant task completion

---

### 6: Run Tests Continuously

**Requirement**: Verify implementation as you go

**Examples** (framework-specific):

**Rust**:
```bash
# Run tests
cargo test --package {module}

# Run specific test
cargo test --package {module} test_name
```

**TypeScript**:
```bash
npm test -- {feature}
```

**Python**:
```bash
pytest tests/features/{slug}/
```

**Expected Outcome**: Tests pass

---

### 7: Verify Against Specs

**Requirement**: Check implementation matches specifications

**Required Actions**:
```bash
# Review each spec file and verify implementation
for spec in specs/*.md; do
  echo "Verifying: $spec"
  echo "Manual check required:"
  cat "$spec"
  echo ""
  read -p "Does implementation match this spec? (y/n) " answer
  if [ "$answer" != "y" ]; then
    echo "ERROR: Implementation doesn't match spec"
    exit 1
  fi
done

echo "✓ All specs verified"
```

**Expected Outcome**: Implementation matches all specs

---

### 8: Complete Final Checks

**Requirement**: Run all verification criteria

**Required Actions**:
```bash
# Check all tasks complete
INCOMPLETE=$(grep -c "^- \[ \]" tasks.md)

if [ $INCOMPLETE -gt 0 ]; then
  echo "WARNING: $INCOMPLETE tasks still incomplete"
  grep "^- \[ \]" tasks.md
fi

# Verify tests passing
echo "Running full test suite..."
# Run appropriate test command for your framework

echo "✓ Final checks complete"
```

**Expected Outcome**: All tasks done, tests pass

---

### 9: Document Implementation Notes

**Requirement**: Add notes about implementation decisions

**Required Actions**:
```bash
# Add notes section to tasks.md
cat >> tasks.md << EOF

---

## Implementation Notes

**Date Completed**: $(date +%Y-%m-%d)

**Key Decisions**:
- Decision 1: {Rationale}
- Decision 2: {Rationale}

**Challenges Encountered**:
- Challenge 1: {How resolved}

**Performance Considerations**:
- {Any performance notes}

**Technical Debt** (if any):
- {Items to address later}

---
EOF

echo "✓ Implementation notes added"
```

**Expected Outcome**: Complete implementation record

---

## Completion Criteria

Implementation complete when:

- [ ] Proposal and specs reviewed
- [ ] Status updated to IN_PROGRESS
- [ ] All tasks in tasks.md completed (100%)
- [ ] Code implements all specifications
- [ ] All tests passing
- [ ] Implementation verified against specs
- [ ] Implementation notes documented
- [ ] Ready to complete change

---

## Common Challenges

### Issue: Specs Unclear

**Resolution**: Return to DESIGN.md, clarify requirements. May need to run `08-fix-design.md`.

### Issue: Tests Failing

**Resolution**: Debug and fix. Don't mark change complete until tests pass.

### Issue: Implementation Deviates from Spec

**Resolution**: Either fix code to match spec, or update spec if requirements changed (requires design update).

---

## Implementation Best Practices

### 1. Incremental Development

- Implement one task at a time
- Run tests after each task
- Commit frequently

### 2. Test-Driven

- Write test first when possible
- Ensure tests fail before implementation
- Verify tests pass after implementation

### 3. Spec Compliance

- Refer to specs constantly
- Don't add scope beyond specs
- If specs are wrong, update design first

### 4. Code Quality

- Follow project conventions
- Add comments for complex logic
- Keep functions focused
- Handle errors properly

---

## Next Activities

After implementation complete:

1. **Complete Change**: Run `11-openspec-change-complete.md {slug} {change-id}`
   - Archive specs
   - Mark change done
   - Merge to source of truth

2. **Next Change** (if any):
   - Check if more changes needed
   - Initialize next change
   - Repeat cycle

3. **Complete Feature** (if last change):
   - Run `07-complete-feature.md {slug}`

---

## References

- **Core FDD**: `../AGENTS.md` - Implementation guidelines
- **OpenSpec**: https://openspec.dev - Change management
- **Next Workflow**: `11-openspec-change-complete.md`
