---
description: Validate business context document
---

# Validate Business Context

**Type**: Validation  
**Role**: Product Manager  
**Artifact**: Validation report (output to chat)

---

## Requirements

**MUST read**: `../requirements/business-context-structure.md`

Extract:
- Required sections structure
- ID format requirements
- Validation criteria (100 points breakdown)
- Pass threshold (≥90/100)

---

## Prerequisites

**MUST validate**:
- [ ] BUSINESS.md exists - validate: Check file at `architecture/BUSINESS.md`

**If missing**: Suggest `business-context` workflow

---

## Steps

### 1. Execute Validation

Follow validation criteria from `business-context-structure.md`:
- Structure (25 pts): Sections A-D present, correct numbering
- Completeness (30 pts): No placeholders, all IDs valid, content complete
- ID Formats (25 pts): Actor IDs, capability IDs follow format
- Consistency (20 pts): Capabilities reference valid actors

Calculate total score

### 2. Output Results to Chat

**Format**:
```markdown
## Validation: BUSINESS.md

**Score**: {X}/100  
**Status**: PASS | FAIL  
**Threshold**: ≥90/100

---

### Findings

**Structure** ({X}/25):
✅ | ❌ {item}

**Completeness** ({X}/30):
✅ | ❌ {item}

**ID Formats** ({X}/25):
✅ | ❌ {item}

**Consistency** ({X}/20):
✅ | ❌ {item}

---

### Recommendations

**High Priority**:
1. {Fix}

---

### Next Steps

{If PASS}: ✅ Proceed to `design` workflow

{If FAIL}: ❌ Fix issues, re-run validation
```

---

## Validation

Self-validating workflow

---

## Next Steps

**If PASS**: `design` workflow

**If FAIL**: Fix BUSINESS.md, re-validate
