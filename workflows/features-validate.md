---
description: Validate features manifest
---

# Validate Features Manifest

**Type**: Validation  
**Role**: Architect  
**Artifact**: Validation report (output to chat)

---

## Requirements

**MUST read**: `../requirements/features-manifest-structure.md`

Extract:
- Required structure
- Validation criteria (100 points breakdown)
- Pass threshold (≥95/100)

---

## Prerequisites

**MUST validate**:
- [ ] FEATURES.md exists - validate: Check file at `architecture/features/FEATURES.md`
- [ ] DESIGN.md exists - validate: Check file at `architecture/DESIGN.md`
- [ ] DESIGN.md validated - validate: Score ≥90/100

**If missing**: Run prerequisite workflows

---

## Steps

### 1. Read Dependencies

Open `architecture/DESIGN.md`

Extract:
- All requirement IDs (Section B)

### 2. Execute Validation

Follow validation criteria from `features-manifest-structure.md`:
- Structure (20 pts): Required sections present
- Feature Definitions (30 pts): All features have ID, name, purpose, scope
- Coverage (30 pts): All DESIGN.md requirements covered by features
- Dependencies (20 pts): Valid, no circular dependencies

Calculate total score

### 3. Output Results to Chat

**Format**:
```markdown
## Validation: FEATURES.md

**Score**: {X}/100  
**Status**: PASS | FAIL  
**Threshold**: ≥95/100

---

### Findings

**Structure** ({X}/20):
✅ | ❌ {item}

**Feature Definitions** ({X}/30):
✅ | ❌ {item}

**Coverage** ({X}/30):
✅ | ❌ {item}

**Dependencies** ({X}/20):
✅ | ❌ {item}

---

### Coverage Analysis

**Requirements covered**: {X}/{total} ({percentage}%)
**Orphaned requirements**: {list if any}

---

### Recommendations

**High Priority**:
1. {Fix}

```

---

## Validation

Self-validating workflow

---

## Next Steps

**If PASS**: `feature` workflow (design first feature from FEATURES.md)

**If FAIL**: Fix FEATURES.md issues, re-run `features-validate`
