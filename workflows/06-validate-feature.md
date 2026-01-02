# Validate Feature Design

**Phase**: 3 - Feature Development  
**Purpose**: Validate Feature DESIGN.md completeness and compliance with FDD requirements

---

## Prerequisites

- Feature directory exists: `architecture/features/feature-{slug}/`
- Feature DESIGN.md exists and contains content

## Input Parameters

- **slug**: Feature identifier (lowercase, kebab-case)
  - Example: `dashboard-mgmt`, `user-auth`

---

## Requirements

### 1: Validate File Exists and Size

**Requirement**: Check that DESIGN.md exists and has reasonable size

**Validation Approach**:
```bash
cd architecture/features/feature-{slug}/

# Check file exists
if [ ! -f DESIGN.md ]; then
  echo "ERROR: DESIGN.md not found"
  exit 1
fi

# Check file size
LINE_COUNT=$(wc -l < DESIGN.md)
echo "DESIGN.md size: $LINE_COUNT lines"

# Recommended: ≤3000 lines
# Hard limit: ≤4000 lines
if [ $LINE_COUNT -gt 4000 ]; then
  echo "WARNING: File too large ($LINE_COUNT > 4000 lines)"
fi
```

**Expected Outcome**: File exists with reasonable size

**Validation Criteria**: File size displayed, no errors

---

### 2: Validate Section Structure

**Requirement**: Check that all required sections A-F are present

**Validation Approach**:
```bash
# Check for all sections
grep -E "^## (A|B|C|D|E|F)\." DESIGN.md

# Should output 6 lines (one for each section)
SECTION_COUNT=$(grep -E "^## (A|B|C|D|E|F)\." DESIGN.md | wc -l)

if [ $SECTION_COUNT -ne 6 ]; then
  echo "ERROR: Expected 6 sections (A-F), found $SECTION_COUNT"
  exit 1
fi

echo "✓ All sections A-F present"
```

**Expected Outcome**: 6 sections found

**Validation Criteria**: Message "All sections A-F present"

---

### 3: Validate Section A (Feature Context)

**Requirement**: Check Section A size and content

**Validation Approach**:
```bash
# Extract Section A (from ## A. to ## B.)
SECTION_A=$(sed -n '/^## A\./,/^## B\./p' DESIGN.md | head -n -1)
SECTION_A_LINES=$(echo "$SECTION_A" | wc -l)

echo "Section A size: $SECTION_A_LINES lines"

# Recommended: ≤500 lines
if [ $SECTION_A_LINES -gt 500 ]; then
  echo "WARNING: Section A too large ($SECTION_A_LINES > 500 lines)"
fi

# Check for required subsections
echo "$SECTION_A" | grep -q "### Overview" || echo "WARNING: Missing Overview subsection"
echo "$SECTION_A" | grep -q "### Purpose" || echo "WARNING: Missing Purpose subsection"
echo "$SECTION_A" | grep -q "### Actors" || echo "WARNING: Missing Actors subsection"

echo "✓ Section A validated"
```

**Expected Outcome**: Section A has reasonable size and required subsections

**Validation Criteria**: Warnings for missing content

---

### 4: Validate Section B (Actor Flows)

**Requirement**: Check that actor flows are documented

**Validation Approach**:
```bash
# Extract Section B
SECTION_B=$(sed -n '/^## B\./,/^## C\./p' DESIGN.md | head -n -1)
SECTION_B_LINES=$(echo "$SECTION_B" | wc -l)

echo "Section B size: $SECTION_B_LINES lines"

# Exception for init-module
if [ "{slug}" = "init-module" ]; then
  echo "Note: init-module has intentionally minimal Section B"
  if [ $SECTION_B_LINES -lt 5 ]; then
    echo "✓ Section B minimal (as expected for init-module)"
  fi
else
  # Standard features: ≥50 lines
  if [ $SECTION_B_LINES -lt 50 ]; then
    echo "ERROR: Section B too short ($SECTION_B_LINES < 50 lines)"
    exit 1
  fi
  echo "✓ Section B has adequate content"
fi
```

**Expected Outcome**: Section B has actor flows documented

**Validation Criteria**: Size check passes

**Note**: Some frameworks may have init-module exceptions - see project adapter documentation

---

### 5: Validate Section C (Algorithms)

**Requirement**: Check algorithms are in ADL (not code)

**Validation Approach**:
```bash
# Extract Section C
SECTION_C=$(sed -n '/^## C\./,/^## D\./p' DESIGN.md | head -n -1)
SECTION_C_LINES=$(echo "$SECTION_C" | wc -l)

echo "Section C size: $SECTION_C_LINES lines"

# Exception for init-module
if [ "{slug}" = "init-module" ]; then
  echo "Note: init-module has intentionally minimal Section C"
else
  # Standard features: ≥100 lines
  if [ $SECTION_C_LINES -lt 100 ]; then
    echo "ERROR: Section C too short ($SECTION_C_LINES < 100 lines)"
    exit 1
  fi
  
  # Check for prohibited code blocks
  if echo "$SECTION_C" | grep -E "^\`\`\`(rust|typescript|javascript|python|java)" > /dev/null; then
    echo "ERROR: Code blocks found in Section C - use ADL instead"
    exit 1
  fi
  
  # Check for programming syntax
  if echo "$SECTION_C" | grep -E "(fn |function |def |class |interface )" > /dev/null; then
    echo "WARNING: Programming syntax found - should use ADL"
  fi
  
  echo "✓ Section C uses ADL"
fi
```

**Expected Outcome**: Algorithms in ADL, no code blocks

**Validation Criteria**: No programming language syntax

**Reference**: See `../FDL.md` for FDL syntax

---

### 6: Validate Section E (Technical Details)

**Requirement**: Check technical details are documented

**Validation Approach**:
```bash
# Extract Section E
SECTION_E=$(sed -n '/^## E\./,/^## F\./p' DESIGN.md | head -n -1)
SECTION_E_LINES=$(echo "$SECTION_E" | wc -l)

echo "Section E size: $SECTION_E_LINES lines"

# Recommended: ≥200 lines
if [ $SECTION_E_LINES -lt 200 ]; then
  echo "WARNING: Section E may lack detail ($SECTION_E_LINES < 200 lines)"
fi

echo "✓ Section E validated"
```

**Expected Outcome**: Technical details documented

---

### 7: Check for Type Redefinitions

**Requirement**: Ensure feature references domain model types, not redefines them

**Validation Approach**:
```bash
# Search for type definitions (should reference, not define)
if grep -i "type definition" DESIGN.md > /dev/null; then
  echo "WARNING: Found 'type definition' - should reference domain model types instead"
fi

# Look for schema definitions
if grep -E "^\`\`\`(json|yaml)" DESIGN.md | grep -i "schema" > /dev/null; then
  echo "WARNING: Found schema definitions - should reference domain model types"
fi

echo "✓ No obvious type redefinitions"
```

**Expected Outcome**: Feature references existing types

**Validation Criteria**: No new type definitions

---

### 8: Check for TODO/TBD Markers

**Requirement**: Ensure design is complete, no placeholder content

**Validation Approach**:
```bash
# Check for incomplete markers
TODO_COUNT=$(grep -i "TODO\|TBD\|FIXME\|XXX" DESIGN.md | wc -l)

if [ $TODO_COUNT -gt 0 ]; then
  echo "ERROR: Found $TODO_COUNT TODO/TBD markers:"
  grep -n -i "TODO\|TBD\|FIXME\|XXX" DESIGN.md
  exit 1
fi

echo "✓ No TODO/TBD markers"
```

**Expected Outcome**: No incomplete markers

**Validation Criteria**: Clean design document

---

### Step 9: Validate OpenSpec Changes Listed

**Requirement**: Check that Section F lists OpenSpec changes

**Validation Approach**:
```bash
# Extract Section F
SECTION_F=$(sed -n '/^## F\./,$ p' DESIGN.md)

# Check for OpenSpec mention
if ! echo "$SECTION_F" | grep -i "openspec" > /dev/null; then
  echo "WARNING: Section F should list OpenSpec changes"
fi

echo "✓ Section F validated"
```

**Expected Outcome**: OpenSpec changes documented

---

## Completion Criteria

Validation complete when:

- [ ] File size ≤4000 lines (recommended ≤3000)
- [ ] All sections A-F present
- [ ] Section A ≤500 lines
- [ ] Section B ≥50 lines (or minimal for init-module)
- [ ] Section C ≥100 lines, uses ADL (or minimal for init-module)
- [ ] Section E ≥200 lines
- [ ] No type redefinitions
- [ ] No TODO/TBD markers
- [ ] OpenSpec changes listed

---

## Common Challenges

### Issue: Section Too Short

**Resolution**: Add more detail. Review FDD requirements in `../AGENTS.md`

### Issue: Code Blocks in Section C

**Resolution**: Convert to FDL. See `../FDL.md`

### Issue: Type Definitions Found

**Resolution**: Remove definitions, reference domain model types from Overall Design instead

---

## Next Activities

After validation passes:

1. **Initialize OpenSpec**: Run `09-openspec-init.md`
   - Creates openspec structure
   - Generates first change

2. **Start Implementation**: Follow OpenSpec workflow
   - Implement changes
   - Complete feature

---

## Scoring

**Validation Score**: 100/100 if all checks pass

**Completeness**: 100% if all sections have required content

**Target**: 100/100 + 100% completeness before starting implementation

---

## References

- **Core FDD**: `../AGENTS.md` - Validation requirements
- **FDL Spec**: `../FDL.md` - FDL syntax (flows, algorithms, states)
- **Next Workflow**: `09-openspec-init.md`
