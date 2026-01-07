---
description: Validate FDD adapter structure
---

# Validate FDD Adapter

**Type**: Validation  
**Role**: Project Manager, Architect  
**Artifact**: Validation report (output to chat)

---

## Requirements

**MUST read**: `../requirements/adapter-structure.md`

Extract:
- File structure requirements
- AGENTS.md format requirements
- Spec files requirements
- Validation criteria (100 points breakdown)
- Pass threshold (≥90/100)

---

## Prerequisites

**MUST validate**:
- [ ] Adapter exists - validate: Check `{adapter-directory}/FDD-Adapter/AGENTS.md` exists

**If adapter missing**: Suggest `adapter` or `adapter-from-sources` workflow

---

## Steps

### 1. Locate Adapter

Search common locations:
- `spec/FDD-Adapter/AGENTS.md`
- `guidelines/FDD-Adapter/AGENTS.md`
- `docs/FDD-Adapter/AGENTS.md`

If not found: STOP, report missing

Store location as: `ADAPTER_DIR`

### 2. Execute Validation

Follow validation criteria from `adapter-structure.md`:
- File Structure (10 pts)
- AGENTS.md Structure (15 pts)
- Specification Files (60 pts)
- Completeness (10 pts)
- OS Agnosticism (5 pts)

Calculate total score

### 3. Output Results to Chat

**Format**:
```markdown
## Validation: FDD Adapter

**Location**: `{ADAPTER_DIR}`  
**Score**: {X}/100  
**Status**: PASS | FAIL  
**Threshold**: ≥90/100

---

### Findings

**File Structure** ({X}/10):
✅ | ❌ {item}

**AGENTS.md Structure** ({X}/15):
✅ | ❌ {item}

**Specification Files** ({X}/60):
✅ | ❌ {item}

**Completeness** ({X}/10):
✅ | ❌ {item}

**OS Agnosticism** ({X}/5):
✅ | ❌ {item}

---

### Recommendations

**High Priority**:
1. {Fix}

**Medium Priority**:
1. {Fix}

```

---

## Validation

Self-validating workflow

---

## Next Steps

**If PASS**: `business-context` workflow (start defining business requirements)

**If FAIL**: Fix adapter issues, re-run `adapter-validate`
