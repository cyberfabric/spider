# FDL - FDD Description Language

**Version**: 1.0  
**Purpose**: Define syntax and grammar for behavior description language  
**Scope**: Actor Flows, Algorithms, State Machines

---

## Overview

**FDL** - Plain English behavior description using markdown lists and bold keywords

**Format**: Numbered markdown lists (1, 2, 3...) + Bold keywords + Plain English

**No code syntax**: FDL is language-agnostic, implementation-independent

---

## Core Rules

1. ✅ Use markdown numbered lists only
2. ✅ Bold keywords for control flow
3. ✅ Plain English descriptions
4. ✅ Indent nested steps
5. ❌ No code syntax ever

---

## Basic Format

**Algorithm: [Name]**

Input: [parameters]  
Output: [result]

1. [Step description]
2. [Step description]
3. **RETURN** [result]

**That's it!** No complex syntax needed.

---

## Control Flow Keywords

### IF/ELSE IF/ELSE

1. [Step]
2. **IF** [condition]:
   1. [Nested step]
3. **ELSE IF** [condition]:
   1. [Nested step]
4. **ELSE**:
   1. [Nested step]

### FOR EACH

1. [Step]
2. **FOR EACH** item in collection:
   1. [Process item]
3. [Next step]

### WHILE

1. [Step]
2. **WHILE** [condition]:
   1. [Process]
3. [Next step]

### TRY/CATCH

1. **TRY**:
   1. [Operation that may fail]
2. **CATCH** [ErrorType]:
   1. [Handle error]
3. [Continue]

### PARALLEL

1. [Prepare]
2. **PARALLEL**:
   - [Task 1]
   - [Task 2]
   - [Task 3]
3. Wait for completion
4. [Combine results]

### MATCH (Pattern Matching)

1. [Get value]
2. **MATCH** [value]:
   - **CASE** [pattern]: [Action]
   - **CASE** [pattern]: [Action]
   - **DEFAULT**: [Action]
3. [Continue]

### GO TO / SKIP TO

1. [Step]
2. **IF** [condition]:
   1. **GO TO** step N
3. [Step]
4. **SKIP TO** step N

### RETURN (Early Exit)

1. [Step]
2. **IF** [condition]:
   1. **RETURN** [value] (exit early)
3. [Continue only if not returned]

---

## Example: Algorithm

**Algorithm: Enable Entity with Dependencies**

Input: entity_id, tenants, security_context  
Output: List of enabled entity IDs

1. Initialize empty list: enabled_entities
2. Load entity from registry
3. **IF** entity not found:
   1. **RETURN** 404 error
4. Update entity.enabled_for = tenants
5. Add entity_id to enabled_entities
6. **FOR EACH** ref_id in references:
   1. Load ref_entity
   2. **IF** ref_entity not enabled:
      1. Enable ref_entity (recursive)
      2. Add to enabled_entities
7. **TRY**:
   1. Commit transaction
   2. Log audit trail
8. **CATCH** any errors:
   1. Rollback transaction
   2. **RETURN** 500 error
9. **RETURN** enabled_entities

---

## Example: Actor Flow

**Flow: Admin Creates Dashboard**

Actor: Admin  
Goal: Create new dashboard

1. User opens Dashboard page
2. User clicks "Create New"
3. UI shows dashboard editor
4. User enters name and description
5. User clicks "Save"
6. **API**: `POST /api/analytics/v1/gts`
   - Body: `{type: "layout.dashboard", name: "..."}`
7. UI redirects to dashboard editor
8. User adds widgets

---

## Validation Rules

### ✅ Required

- Markdown numbered lists (1, 2, 3...)
- Bold keywords: **IF**, **FOR EACH**, **WHILE**, **TRY/CATCH**, **RETURN**, **MATCH**
- Plain English descriptions
- Indentation for nested steps

### ❌ Prohibited

- Code examples (any language)
- Function syntax (`fn`, `function`, `async`)
- Type annotations (`: string`, `<T>`)
- Language operators (`&&`, `||`, `=>`)
- Pseudo-code syntax

### ✅ Allowed

- Variable names (no types): `entity`, `items`, `result`
- Simple notation: `entity.field`, `array[0]`
- API endpoints: `POST /api/v1/resource`
- Inline clarifications: `(condition explanation)`

---

## State Machines (Section D)

### Basic Format

**State Machine: [Entity Name]**

**States**: [ALL_STATES, COMMA_SEPARATED]

**Transitions**:
1. **FROM** [state] **TO** [state] **WHEN** [trigger]
2. **FROM** [state] **TO** [state] **WHEN** [trigger]

### With Actions

**Transition: [STATE_A] → [STATE_B]**  
**When**: [trigger]  
**Actions**:
1. [Action step]
2. [Action step]
3. **IF** [condition]:
   1. [Conditional action]

### Example

**State Machine: Order**

**States**: DRAFT, PENDING_PAYMENT, PAID, SHIPPED, DELIVERED, CANCELLED

**Transitions**:
1. **FROM** DRAFT **TO** PENDING_PAYMENT **WHEN** user submits order
2. **FROM** PENDING_PAYMENT **TO** PAID **WHEN** payment confirmed
3. **FROM** PAID **TO** SHIPPED **WHEN** order dispatched
4. **FROM** SHIPPED **TO** DELIVERED **WHEN** delivery confirmed
5. **FROM** DRAFT **TO** CANCELLED **WHEN** user cancels

---

## Validation Criteria

### Structure (25 points)

**Check**:
- [ ] Uses numbered markdown lists (1, 2, 3...)
- [ ] Proper nesting with indentation
- [ ] No code blocks or function syntax
- [ ] No type annotations

### Keyword Usage (30 points)

**Check**:
- [ ] Keywords are bold (**IF**, **FOR EACH**, **WHILE**, etc.)
- [ ] Keywords used correctly (IF for conditions, FOR EACH for iterations)
- [ ] FROM/TO/WHEN used for state transitions
- [ ] TRY/CATCH used for error handling
- [ ] RETURN used for algorithm outputs

### Clarity (25 points)

**Check**:
- [ ] Plain English descriptions
- [ ] No programming language syntax (no =>, &&, ||, etc.)
- [ ] No function definitions (fn, function, async)
- [ ] Language-agnostic (implementation-independent)
- [ ] Clear and unambiguous steps

### Completeness (20 points)

**Check**:
- [ ] All flows have numbered steps
- [ ] All algorithms have Input/Output defined
- [ ] All state machines have States and Transitions defined
- [ ] No placeholders or TODOs
- [ ] All conditions and actions specified

**Total**: 100/100

**Pass threshold**: ≥90/100

---

## References

**This file is referenced by**:
- `overall-design-structure.md` - Requires FDL for behavioral sections
- `feature-design-structure.md` - Requires FDL for behavioral sections

**Note**: Project adapters CAN override FDL by specifying custom behavior description language in adapter AGENTS.md
