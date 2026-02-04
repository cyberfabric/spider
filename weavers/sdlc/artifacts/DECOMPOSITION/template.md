---
spider-template:
  version:
    major: 2
    minor: 0
  kind: DECOMPOSITION
  unknown_sections: warn
---

# Decomposition: {PROJECT_NAME}

<!-- spd:#:decomposition -->
# Decomposition

<!-- spd:##:overview -->
## 1. Overview

{ Description of how the DESIGN was decomposed into specs, the decomposition strategy, and any relevant decomposition rationale. }


<!-- spd:##:overview -->

<!-- spd:##:entries -->
## 2. Entries

**Overall implementation status:**
<!-- spd:id:status has="priority,task" -->
- [ ] `p1` - **ID**: `spd-{system}-status-overall`

<!-- spd:###:spec-title repeat="many" -->
### 1. [{Spec Title}](spec-{slug}/) ⏳ MEDIUM

<!-- spd:id:spec has="priority,task" -->
- [ ] `p1` - **ID**: `spd-{system}-spec-{slug}`

<!-- spd:paragraph:spec-purpose required="true" -->
- **Purpose**: {Few sentences}
<!-- spd:paragraph:spec-purpose -->

<!-- spd:paragraph:spec-depends -->
- **Depends On**: {None or `spd-{system}-spec-{slug}`}
<!-- spd:paragraph:spec-depends -->

<!-- spd:list:spec-scope -->
- **Scope**:
  - {in-scope item}
  - {in-scope item}
<!-- spd:list:spec-scope -->

<!-- spd:list:spec-out-scope -->
- **Out of scope**:
  - {Out-of-scope item}
  - {Out-of-scope item}
<!-- spd:list:spec-out-scope -->

- **Requirements Covered**:
<!-- spd:id-ref:fr has="priority,task" -->
  - [ ] `p1` - `spd-{system}-fr-{slug}`
  - [ ] `p1` - `spd-{system}-nfr-{slug}`
<!-- spd:id-ref:fr -->

- **Design Principles Covered**:
<!-- spd:id-ref:principle has="priority,task" -->
  - [ ] `p1` - `spd-{system}-principle-{slug}`
<!-- spd:id-ref:principle -->

- **Design Constraints Covered**:
<!-- spd:id-ref:constraint has="priority,task" -->
  - [ ] `p1` - `spd-{system}-constraint-{slug}`
<!-- spd:id-ref:constraint -->

<!-- spd:list:spec-domain-entities -->
- **Domain Model Entities**:
  - {entity/type/object}
<!-- spd:list:spec-domain-entities -->

- **Design Components**:
<!-- spd:id-ref:component has="priority,task" -->
  - [ ] `p1` - `spd-{system}-component-{slug}`
<!-- spd:id-ref:component -->

<!-- spd:list:spec-api -->
- **API**:
  - /{resource-name}
  - {CLI command}
<!-- spd:list:spec-api -->

- **Sequences**:
<!-- spd:id-ref:seq has="priority,task" -->
  - [ ] `p1` - `spd-{system}-seq-{slug}`
<!-- spd:id-ref:seq -->

- **Data**:
<!-- spd:id-ref:dbtable has="priority,task" -->
  - [ ] `p1` - `spd-{system}-dbtable-{slug}`
<!-- spd:id-ref:dbtable -->

<!-- spd:id:spec -->

<!-- spd:###:spec-title repeat="many" -->
<!-- spd:id:status -->
<!-- spd:##:entries -->
<!-- spd:#:decomposition -->
