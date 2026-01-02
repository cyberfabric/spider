# Validate Features Manifest

**Phase**: 2 - Feature Planning  
**Purpose**: Validate FEATURES.md manifest completeness and consistency

---

## Prerequisites

- `architecture/features/FEATURES.md` exists
- At least one feature defined (init-module)

## Input Parameters

None (validates entire FEATURES.md)

---

## Requirements

### 1. Verify Manifest Existence

**Requirement**: Features manifest must exist

**Required File**: `architecture/features/FEATURES.md`

**Expected Outcome**: Manifest file present

**Validation Criteria**: File exists at specified path

---

### 2. Verify Init Priority

**Requirement**: Init must be first feature in implementation order

**Rationale**: Init has no dependencies and creates foundation

**Expected Outcome**: Feature #1 is init

**Validation Criteria**: First numbered feature is `feature-init`

---

### 3. Validate Feature Completeness

**Requirement**: Each feature must have complete metadata

**Required Fields per Feature**:
- Feature slug (unique identifier)
- Status (NOT_STARTED, IN_PROGRESS, IMPLEMENTED)
- Priority (CRITICAL, HIGH, MEDIUM, LOW)
- Depends On (list or "None")
- Purpose (one-line description)
- Scope (bulleted list of deliverables)

**Expected Outcome**: All features fully documented

**Validation Criteria**: Every feature has all 6 required fields

---

### 4. Validate Status Values

**Requirement**: All features must use valid status values

**Valid Status Values**:
- `NOT_STARTED` - Not yet begun
- `IN_PROGRESS` - Currently being implemented
- `IMPLEMENTED` - Complete and verified

**Expected Outcome**: No invalid statuses

**Validation Criteria**: Each feature has one of three valid statuses

---

### 5. Validate Dependency References

**Requirement**: All dependencies must reference existing features

**Dependency Rules**:
- Each dependency must be valid feature slug from manifest
- "None" indicates no dependencies (valid for init only)
- Multiple dependencies comma-separated

**Expected Outcome**: No broken dependency references

**Validation Criteria**: Every listed dependency exists in features list

---

### 6. Check Dependency Graph Acyclicity

**Requirement**: Dependency graph must be acyclic (DAG)

**Circular Dependency Example** (prohibited):
```
feature-A depends on feature-B
feature-B depends on feature-A
```

**Expected Outcome**: Valid dependency graph without cycles

**Validation Criteria**: No feature depends on itself directly or transitively

---

### 7. Validate Feature Slug Format

**Requirement**: Feature slugs must follow naming convention

**Slug Format**:
- Pattern: `feature-{descriptive-name}`
- Lowercase letters only
- Hyphens for word separation
- No underscores, spaces, or special characters

**Uniqueness**: Each slug must be unique in manifest

**Expected Outcome**: All slugs valid and unique

**Validation Criteria**: Slugs match pattern and no duplicates

---

### 8. Validate Implementation Order

**Requirement**: Features ordered respecting dependency graph (topological sort)

**Ordering Rule**: Dependencies must appear before features that depend on them

**Example Valid Order**:
```
1. feature-init (no deps)
2. feature-user-crud (depends on init)
3. feature-user-auth (depends on user-crud)
```

**Expected Outcome**: Implementation order is executable

**Validation Criteria**: For each feature, all dependencies have lower numbers

---

## Completion Criteria

Manifest validation complete when:

- [ ] FEATURES.md exists
- [ ] init is first feature
- [ ] All features have: status, priority, dependencies, purpose, scope
- [ ] All statuses valid (NOT_STARTED, IN_PROGRESS, IMPLEMENTED)
- [ ] All dependencies reference existing features
- [ ] No circular dependencies
- [ ] Feature slugs valid and unique
- [ ] Implementation order topologically valid

---

## Common Challenges

### Issue: Circular Dependencies

**Resolution**: Refactor features to break cycle. One feature should be split or dependencies reordered.

### Issue: Wrong Implementation Order

**Resolution**: Reorder features in FEATURES.md to match dependency graph.

---

## Next Activities

After validation passes:

1. **Start Implementation**: Begin with feature #1 (init)
   - Run: `05-init-feature.md init`
   - Fill in DESIGN.md
   - Validate and implement

2. **Update Manifest**: As features complete
   - Update status to IN_PROGRESS → IMPLEMENTED
   - Track progress

---

## References

- **Core FDD**: `../AGENTS.md` - Feature planning
- **Next Workflow**: `05-init-feature.md`
