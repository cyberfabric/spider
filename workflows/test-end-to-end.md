---
extends: ../AGENTS.md
---

# Workflow 14: End-to-End FDD Testing

**Purpose**: Test complete FDD methodology by simulating user-agent conversation

**Approach**: Act as USER, give prompts to AI agent, validate agent follows FDD workflows correctly

**Test Project**: `touch` CLI tool in `test-projects/touch-cli-test/` (relative to FDD root)

---

## 🔄 GLOBAL CONTEXT RESET - READ BEFORE STARTING

**⚠️ CRITICAL: Agent instructions for ENTIRE test workflow**

**BEFORE starting Phase 0, you MUST**:
- **FORGET** all previous work, conversations, and decisions
- **CLEAR** all assumptions about FDD, workflows, or project structure
- **TREAT** this as first time seeing FDD methodology
- **DO NOT use** any cached knowledge about:
  - Previous test runs or iterations
  - Files that "should exist" 
  - Decisions made in other sessions
  - Patterns from other projects

**START FRESH**:
- Read ONLY files explicitly mentioned in each phase
- Follow ONLY the workflow instructions for that phase
- Validate ONLY what the phase asks to validate
- Create ONLY what the phase asks to create

**EXCEPTION - Project Context (DO NOT FORGET)**:
- `FDD-Adapter/AGENTS.md` - Contains project-specific tech stack
- This is the ONLY file you may reference across all phases
- Read it when phases mention "adapter" or technology choices

**This test simulates a NEW agent with NO prior FDD knowledge.**

**Each phase has its own CONTEXT RESET** - follow those too.

---

## Iteration Tracking

**IMPORTANT**: USER manually tracks iterations to achieve working state

**Current Iteration**: `[UPDATE THIS: 1, 2, 3, ...]`

**Iteration Log**:
- **Iteration 1**: Started [Date] - [Status: IN_PROGRESS / FAILED / SUCCESS]
  - Failed at: Phase X
  - Issue: [description]
  - Fix applied: [description]
- **Iteration 2**: ...

**How to restart**:
1. If phase fails → Document failure in log above
2. Fix issue (update workflow, fix FDD specs, etc.)
3. Increment iteration number
4. Resume from failed phase OR restart from Phase 0
5. Continue until all 16 phases complete successfully

**Resume commands**:
- **From Phase 0**: Delete `test-projects/touch-cli-test/`, start fresh
- **From Phase X**: Continue from that phase's USER prompt
- **After fix**: Re-run failed phase's validation

---

## Phase 0: Setup

**USER**: "Clean and create a new test project in test-projects/touch-cli-test to test all FDD workflows. This will be a simple touch CLI utility on Node.js."

**Agent should**: 
- Delete existing test-projects/touch-cli-test directory completely
- Create fresh empty directory
- Initialize git repository

**Validate**: 
- ✅ Directory test-projects/touch-cli-test/ exists
- ✅ Directory contains ONLY .git/ (no other files or folders)
- ✅ Git repository initialized (`test -d test-projects/touch-cli-test/.git`)
- ✅ No leftover files from previous tests

**Validation commands**:
```bash
cd test-projects/touch-cli-test
ls -A | grep -v '^\.git$' | wc -l  # Should output: 0
test -d .git && echo "Git initialized" || echo "Git NOT initialized"
```

---

## Phase 1: Create FDD Adapter

**USER**: "Follow workflows/adapter-config.md with answers: {\"domain_model_tech\": \"JSON Schema\", \"domain_model_location\": \"schemas/\", \"api_contract_tech\": \"CLI Specification\", \"api_contract_location\": \"spec/CLI/\", \"implementation_tech\": \"Node.js/TypeScript\", \"testing_framework\": \"Jest\", \"build_tool\": \"tsc\"}"

**Agent workflow execution**:
- Execute workflow `adapter-config.md` with provided answers
- Create `FDD-Adapter/AGENTS.md` in test project root

**Agent manual validation**:
1. Read `FDD-Adapter/AGENTS.md` (in test project root)
2. Read `../../AGENTS.md` (base file at FDD root)
3. Verify extends relationship
4. Check technology specifications against answers
5. Verify Status field

**Validation criteria** (from FDD spec):
- ✅ File exists: `FDD-Adapter/AGENTS.md`
- ✅ Contains `**Extends**: ../../AGENTS.md`
- ✅ Domain Model: JSON Schema, location `schemas/`
- ✅ API Contracts: CLI Specification, location `spec/CLI/`
- ✅ Status: COMPLETE (no missing specs)

**Compare**: Agent's manual check vs workflow output - must match

---

## Phase 2: Create Valid Overall Design

**🔄 CONTEXT RESET - READ THIS FIRST**

**Agent instructions for this phase ONLY**:
- **FORGET** all outputs and decisions from Phase 0-1
- **DO NOT assume** anything from previous phases exists
- **READ ONLY** these files for this phase:
  1. `workflows/01-init-project.md` (workflow to execute)
  2. `../../requirements/overall-design-structure.md` (validation spec)
  3. `FDD-Adapter/AGENTS.md` (project adapter - created in Phase 1)
- **VERIFY** adapter exists before starting (created in Phase 1)
- **TREAT** this as a fresh start - re-read specifications
- **OUTPUT** validation results in chat (no report files)

---

**USER**: "Follow workflows/01-init-project.md with answers: {\"project_name\": \"Touch CLI Tool\", \"project_vision\": \"Simple Unix touch utility - creates empty files or updates file timestamps\", \"actors\": [\"End User\", \"File System\"], \"capabilities\": [\"Touch Command - create files and update timestamps\"], \"platform\": \"Node.js\", \"constraints\": [\"POSIX compatible\", \"Handle permission errors\", \"Node.js 16+\"]}"

**Agent workflow execution**:
- Execute workflow `01-init-project.md` with provided answers
- Workflow creates `architecture/DESIGN.md`

**Agent manual validation**:
1. Read `architecture/DESIGN.md`
2. Read `../../requirements/overall-design-structure.md` (FDD validation spec)
3. Count lines
4. Check each section exists
5. Verify domain model format (must reference JSON Schema files)
6. Verify API contracts format (must reference CLI spec files)
7. Check for placeholders (TODO/TBD/[Description])
8. **NEW**: Verify openspec structure created

**Validation criteria** (from `overall-design-structure.md`):
- ✅ Section A: Business Context
  - A.1 Project Vision (2-3 paragraphs)
  - A.2 Stakeholders (actors listed)
  - A.3 Success Criteria
- ✅ Section B: Requirements & Principles
  - B.1 Functional Requirements
  - B.2 Non-Functional Requirements
  - B.3 Design Principles
  - B.4 Constraints
- ✅ Section C: Technical Architecture
  - C.1 Architecture Overview + component diagram (Mermaid/ASCII)
  - C.2 Domain Model (JSON Schema, verifiable file references)
  - C.3 API Contracts (CLI spec, verifiable file references)
  - C.4 Security Model
  - C.5 Non-Functional Requirements
- ✅ Section D: Architecture Decision Records
  - Minimum ADR-0001 in MADR format
- ✅ File length ≥200 lines
- ✅ No TODO/TBD/[placeholder] text
- ✅ **OpenSpec structure created** (CRITICAL from workflow 01):
  - Directory `openspec/` exists
  - Directory `openspec/specs/` exists
  - Directory `openspec/changes/` exists
  - Directory `openspec/changes/archive/` exists
  - File `openspec/project.md` exists

**Compare**: Agent's manual check vs workflow 02 validation - scores must align

**ON VALIDATION FAILURE** (OpenSpec structure missing):
1. STOP immediately - this is CRITICAL error in workflow 01
2. Report: "Workflow 01 failed to create openspec structure (Requirements 5-6)"
3. Agent must re-run workflow 01 correctly
4. Do NOT proceed to Phase 3 until openspec structure exists

---

## Phase 3: Validate Overall Design (Pass)

**USER**: "Follow workflows/02-validate-architecture.md for architecture/DESIGN.md"

**Agent workflow execution**:
- Execute workflow `02-validate-architecture.md`
- Workflow reads `../../requirements/overall-design-structure.md`
- Workflow outputs validation results to chat

**Agent manual validation** (independent check):
1. Read `architecture/DESIGN.md`
2. Read `../../requirements/overall-design-structure.md`
3. Score each criterion:
   - Structure (30 points): Section presence, hierarchy
   - Domain Model (25 points): JSON Schema files exist, machine-readable
   - API Contracts (25 points): CLI spec files exist, machine-readable  
   - Content Quality (20 points): No placeholders, sufficient detail
4. Calculate total score
5. Check completeness percentage

**Expected**:
- Manual score: ≥90/100
- Workflow score: ≥90/100
- Completeness: 100%

**Compare**:
- Agent's manual score: [X]/100
- Workflow 02 score: [Y]/100
- Difference acceptable if <5 points
- If difference >5: FAIL - validation logic mismatch

---

## Phase 4: Generate FEATURES.md

**🔄 CONTEXT RESET - READ THIS FIRST**

**Agent instructions for this phase ONLY**:
- **FORGET** all previous phases except Phase 2-3 outputs
- **READ ONLY** these files:
  1. `workflows/03-init-features.md` (workflow to execute)
  2. `architecture/DESIGN.md` (created in Phase 2)
  3. `../../requirements/features-manifest-structure.md` (validation spec)
- **DO NOT assume** feature list - extract from DESIGN.md
- **VERIFY** Overall Design validated before starting

---

**USER**: "Follow workflows/03-init-features.md"

**Agent should**:
- Use workflow 03 (init-features)
- Extract capabilities from `architecture/DESIGN.md`
- Create `architecture/features/FEATURES.md`

**Validate**:
- ✅ Lists exactly ONE feature: feature-touch-command
- ✅ Feature includes all touch functionality (create files, update timestamps, error handling)
- ✅ Status, priority, directory present
- ✅ No unnecessary feature splitting for this small tool

---

## Phase 5: Validate FEATURES.md

**USER**: "Follow workflows/04-validate-features.md"

**Agent should**:
- Use workflow 04 (validate-features)

**Validate**:
- ✅ Score 100/100
- ✅ Single feature matches single capability from Overall Design
- ✅ Feature directory created: architecture/features/feature-touch-command/

---

## Phase 6: Create Valid Feature Design

**🔄 CONTEXT RESET - READ THIS FIRST**

**Agent instructions for this phase ONLY**:
- **FORGET** all previous design decisions
- **READ ONLY** these files:
  1. `workflows/05-init-feature.md` (workflow to execute)
  2. `../../FDL.md` (behavior specification)
  3. `../../requirements/feature-design-structure.md` (structure spec)
  4. `architecture/DESIGN.md` (for type references)
  5. `architecture/features/FEATURES.md` (feature list)
  6. `FDD-Adapter/AGENTS.md` (project tech stack)
- **MUST use FDL** for all flows/algorithms/states
- **NEVER redefine types** from Overall Design

---

**USER**: "Create touch-command feature. Implements complete touch utility: create empty files if don't exist, update timestamps if exist, handle multiple files, handle errors (EACCES, ENOENT, EISDIR). All functionality in one feature."

**Agent should**:
- Use workflow 05 (init-feature)
- Read `../../requirements/feature-design-structure.md`
- Read `../../FDL.md` for syntax
- Create `architecture/features/feature-touch-command/DESIGN.md`

**Validate `architecture/features/feature-touch-command/DESIGN.md`**:
- ✅ Section A: Overview (purpose, actors match Overall Design, references)
- ✅ Section B: Actor Flows in FDL
  - Numbered lists with proper indentation
  - **IF**, **FOR EACH**, **RETURN** keywords
  - NO prohibited keywords (**WHEN** in flows, **THEN**, **SET**, etc.)
- ✅ Section C: Algorithms in FDL
  - Input, Output, Steps
  - NO code blocks
- ✅ Section D: States in FDL
  - **FROM/TO/WHEN** format for transitions
- ✅ Section E: Technical Details
- ✅ Section F: Requirements
  - Format: `fdd-touch-cli-feature-file-creation-req-{name}`
  - References to sections B-E
- ✅ Section G: Implementation Plan
  - Format: `fdd-touch-cli-feature-file-creation-change-{name}` [⏳ NOT_STARTED]
  - Lists requirements implemented
  - Lists dependencies

---

## Phase 7: Validate Feature Design (Pass)

**USER**: "Follow workflows/06-validate-feature.md for architecture/features/feature-file-creation/DESIGN.md"

**Agent should**:
- Use workflow 06 (validate-feature)
- Read `../../requirements/feature-design-structure.md`
- Read `../../FDL.md`
- Check FDL syntax strictly

**Validate**:
- ✅ Score 100/100
- ✅ Completeness 100%
- ✅ FDL syntax correct
- ✅ No type redefinitions
- ✅ Requirement IDs correct format
- ✅ Change names correct format

---

## Phase 8: Initialize First Change

**🔄 CONTEXT RESET - READ THIS FIRST**

**Agent instructions for this phase ONLY**:
- **FORGET** all previous phases
- **READ ONLY** these files:
  1. `workflows/09-openspec-change-next.md` (workflow to execute)
  2. `../../requirements/openspec-change-structure.md` (structure spec)
  3. `architecture/features/feature-touch-command/DESIGN.md` (Section F & G)
- **VERIFY** Feature Design validated (Phase 7)
- **CREATE** change from Section G implementation plan

---

**USER**: "Follow workflows/09-openspec-change-next.md with change_name: implement-touch-command, requirements: [fdd-touch-cli-feature-touch-command-req-create-file, req-update-timestamp, req-batch-ops, req-error-handling]"

**Agent should**:
- Use workflow 09 (openspec-init)
- Create `openspec/changes/implement-core-file-ops/`
- Create proposal.md, tasks.md, design.md
- Create specs delta files

**Validate**:
- ✅ Directory exists: `openspec/changes/implement-core-file-ops/`
- ✅ File exists: `openspec/changes/implement-core-file-ops/proposal.md`
- ✅ File exists: `openspec/changes/implement-core-file-ops/tasks.md`
- ✅ File exists: `openspec/changes/implement-core-file-ops/design.md`
- ✅ File exists: `openspec/changes/implement-core-file-ops/specs/feature-file-creation/spec.md`
- ✅ proposal.md contains requirement IDs from Feature Design Section F
- ✅ tasks.md has at least 3 implementation tasks
- ✅ tasks.md includes task: "Create tests for Testing Scenarios"
- ✅ design.md contains reference to Feature Design path: `../../architecture/features/feature-file-creation/DESIGN.md`
- ✅ design.md references Section F requirements
- ✅ specs delta file uses `## ADDED Requirements` header (OpenSpec format)
- ✅ specs delta file has requirements with `### Requirement:` headers
- ✅ specs delta file has scenarios with `#### Scenario:` headers (4 hashtags)
- ✅ scenarios use `**WHEN**` and `**THEN**` format (not FDL numbered lists)
- ✅ Run `openspec validate implement-core-file-ops --strict` from project root
- ✅ OpenSpec validation passes with zero errors

**ON VALIDATION FAILURE**:
1. Stop current phase
2. Report specific failures (list missing files, validation errors)
3. Agent must re-run workflow 09 with corrections
4. Retry validation
5. If retry succeeds: continue to Phase 10
6. If retry fails after 2 attempts: escalate to user

---

## Phase 8a: Validate Change Structure (Pre-Implementation)

**USER**: "Follow workflows/12-openspec-validate.md for change implement-core-file-ops"

**Agent should**:
- Use workflow 12 (openspec-validate)
- Validate change structure BEFORE implementation starts
- Run `openspec validate implement-core-file-ops --strict`
- Verify all change files (proposal.md, tasks.md, design.md, spec.md) are valid

**Validate**:
- ✅ Change directory structure is correct
- ✅ proposal.md format is valid
- ✅ tasks.md has implementation checklist
- ✅ design.md exists (full or minimal reference)
- ✅ spec.md uses OpenSpec Delta format (not FDL)
- ✅ spec.md has `## ADDED Requirements` headers
- ✅ spec.md has `### Requirement:` and `#### Scenario:` structure
- ✅ `openspec validate implement-core-file-ops --strict` passes

**ON VALIDATION FAILURE**:
1. Stop current phase
2. Report specific failures (format errors, missing files)
3. Agent must fix change structure (return to Phase 9)
4. Retry validation
5. If retry succeeds: continue to Phase 10
6. If retry fails after 2 attempts: escalate to user

---

## Phase 9: Implement Node.js Code

**🔄 CONTEXT RESET - READ THIS FIRST**

**Agent instructions for this phase ONLY**:
- **FORGET** all previous implementation decisions
- **READ ONLY** these files:
  1. `workflows/10-openspec-change-implement.md` (workflow to execute)
  2. `openspec/changes/implement-touch-command/proposal.md`
  3. `openspec/changes/implement-touch-command/tasks.md`
  4. `openspec/changes/implement-touch-command/specs/fdd-touch-cli-touch-command-feature/spec.md`
  5. `FDD-Adapter/AGENTS.md` (project tech stack - Node.js/TypeScript/Jest)
- **IMPLEMENT** exactly per spec - no deviations
- **CHECK** tasks.md checklist after implementation

---

**USER**: "Follow workflows/10-openspec-change-implement.md for change implement-touch-command"

**Agent should**:
- Use workflow 10 (implement)
- Read design.md for Feature Design reference
- Create Node.js project structure
- Implement TypeScript code matching Feature Design
- Create test files for Testing Scenarios

**Validate**:
- ✅ `package.json` exists with correct structure
- ✅ `package.json` includes Jest in devDependencies
- ✅ `package.json` has "test" script defined
- ✅ `tsconfig.json` exists
- ✅ `jest.config.js` or Jest config in package.json exists
- ✅ `schemas/file-path.json` exists (JSON Schema)
- ✅ `schemas/file-operation.json` exists
- ✅ `src/fileOps.ts` implements validatePath, createFile, updateTimestamp
- ✅ `src/index.ts` has CLI logic
- ✅ Test files exist matching pattern `**/*.test.ts` or `**/*.spec.ts`
- ✅ At least 4 test suites (one per requirement from Feature Design Section F)
- ✅ Test files cover Testing Scenarios from Feature Design Section F
- ✅ `npm test` command runs without errors
- ✅ No compilation errors

**ON VALIDATION FAILURE**:
1. Stop current phase
2. Report specific failures (list missing tests, test failures)
3. Agent must re-run workflow 10 with corrections (add missing tests)
4. Retry validation
5. If retry succeeds: continue to Phase 11
6. If retry fails after 2 attempts: escalate to user

---

## Phase 9a: Code Validation (AUTOMATIC)

**USER**: "Follow workflows/10-1-openspec-code-validate.md for change implement-core-file-ops"

**Agent should**:
- Use workflow 10-1 (openspec-code-validate) - runs automatically after workflow 10
- Validate code matches spec requirements
- Validate all requirements from specs/feature-file-creation/spec.md implemented
- Validate tests cover all scenarios

**Validate**:
- ✅ All requirements from change delta spec.md are implemented in code
- ✅ Each requirement has corresponding test coverage
- ✅ Test scenarios match Feature Design Section F Testing Scenarios
- ✅ No spec requirements left unimplemented
- ✅ Code structure matches technical specifications

**ON VALIDATION FAILURE**:
1. Stop current phase
2. Report specific failures (missing implementations, missing tests)
3. Agent must return to Phase 10 and add missing code/tests
4. Retry validation
5. If retry succeeds: continue to Phase 11
6. If retry fails after 2 attempts: escalate to user

---

## Phase 10: Build Project

**USER**: "Install dependencies and build the project"

**Agent should**:
- Propose `npm install` command
- Propose `npm run build` command
- USER runs commands

**Validate**:
- ✅ `node_modules/` created
- ✅ `dist/` created with compiled JS
- ✅ No TypeScript errors

---

## Phase 11: Test CLI Tool

**USER**: "Test touch CLI - create file /tmp/test-touch.txt, then update its timestamp, check error handling"

**Agent should**:
- Propose test commands
- USER runs manually

**Validate**:
- ✅ `node dist/index.js /tmp/test-touch.txt` creates file
- ✅ File has 0 bytes
- ✅ Running again updates timestamp
- ✅ Permission error handled correctly
- ✅ Tool works as designed

---

## Phase 12: Complete Change

**USER**: "Follow workflows/11-openspec-change-complete.md for change implement-core-file-ops"

**Agent should**:
- Use workflow 11 (openspec-change-complete)
- Merge specs to `openspec/specs/`
- Archive change to `openspec/changes/archive/implement-core-file-ops/`
- Update change status

**Validate**:
- ✅ Directory exists: `openspec/changes/archive/implement-core-file-ops/`
- ✅ Archive contains: proposal.md, tasks.md, design.md, specs/
- ✅ File exists: `openspec/specs/feature-file-creation/spec.md`
- ✅ Merged spec contains requirements from change delta
- ✅ Active changes directory is empty (except archive/)

**ON VALIDATION FAILURE**:
1. Stop current phase
2. Report specific failures (missing archive files, unmerged specs)
3. Agent must re-run workflow 11 with corrections
4. Retry validation
5. If retry succeeds: continue to Phase 14
6. If retry fails after 2 attempts: escalate to user

---

## Phase 12a: OpenSpec Structure Validation

**USER**: "Follow workflows/12-openspec-validate.md"

**Agent should**:
- Use workflow 12 (openspec-validate)
- Validate OpenSpec structure consistency
- Validate all specs in openspec/specs/ are valid
- Validate no active changes remain in openspec/changes/ (except archive/)

**Validate**:
- ✅ All specs in openspec/specs/ pass validation
- ✅ No active changes in openspec/changes/ (only archive/ directory exists)
- ✅ All specs have proper format (Requirements with Scenarios)
- ✅ No orphaned or incomplete specs
- ✅ OpenSpec structure is consistent

**ON VALIDATION FAILURE**:
1. Stop current phase
2. Report specific failures (invalid specs, active changes remaining)
3. Agent must fix issues or re-run workflow 11 if changes not archived properly
4. Retry validation
5. If retry succeeds: continue to Phase 14
6. If retry fails after 2 attempts: escalate to user

---

## Phase 13: Complete Feature

**USER**: "Follow workflows/07-complete-feature.md for feature-file-creation"

**Agent should**:
- Use workflow 07 (complete-feature)
- Update FEATURES.md status

**Validate**:
- ✅ FEATURES.md shows ✅ IMPLEMENTED
- ✅ Status changed from IN_PROGRESS

---

## Success Criteria

**Complete test passes if**:
- ✅ All 13 phases complete (0-13, with 8a, 9a, 12a subphases)
- ✅ Valid documents pass validation (≥90/100 for Overall Design, 100/100 for Feature Design)
- ✅ Node.js project compiles
- ✅ CLI tool actually works
- ✅ All files follow FDD structure
- ✅ OpenSpec changes created with all required files (proposal.md, tasks.md, design.md, specs/)
- ✅ OpenSpec archive exists with completed change
- ✅ Automated tests exist covering Testing Scenarios
- ✅ `npm test` passes
- ✅ design.md references Feature Design
- ✅ Agent uses workflows, not bash scripts
- ✅ Agent outputs validation to chat, not files
- ✅ Manual validation matches workflow validation scores

---

## Final Report

**When all phases complete successfully**, USER documents:

### Test Completion Report

**Date**: [completion date]

**Total Iterations**: [X iterations]

**Iteration Summary**:
| Iteration | Failed At | Issue | Fix Applied | Duration |
|-----------|-----------|-------|-------------|----------|
| 1 | Phase X | [issue] | [fix] | [time] |
| 2 | Phase Y | [issue] | [fix] | [time] |
| ... | ... | ... | ... | ... |
| N | - | SUCCESS | - | [time] |

**Total Time**: [X hours/days]

**Lessons Learned**:
1. [what didn't work initially]
2. [what fixes were needed]
3. [FDD workflow improvements needed]

**Workflow Quality Score**:
- **Iteration 1 success rate**: 0% (if failed) or 100% (if passed)
- **Final success achieved**: Iteration N
- **Average fixes per phase**: X

**Recommendations**:
- [improvements to FDD workflows]
- [improvements to test workflow]
- [documentation gaps found]

---

## Final Project Structure

```
test-projects/touch-cli-test/
├── FDD-Adapter/AGENTS.md                ✅
├── architecture/
│   ├── DESIGN.md                        ✅
│   └── features/
│       ├── FEATURES.md                  ✅
│       └── feature-file-creation/
│           └── DESIGN.md                ✅
├── schemas/                             ✅ JSON Schema
│   ├── file-path.json
│   └── file-operation.json
├── openspec/
│   ├── project.md                       ✅
│   ├── specs/
│   │   └── feature-file-creation/
│   │       └── spec.md                  ✅ (merged)
│   └── changes/archive/
│       └── implement-core-file-ops/     ✅ (completed)
│           ├── proposal.md              ✅
│           ├── tasks.md                 ✅
│           ├── design.md                ✅ (refs Feature Design)
│           └── specs/
│               └── feature-file-creation/
│                   └── spec.md          ✅
├── src/                                 ✅ TypeScript
│   ├── fileOps.ts
│   ├── fileOps.test.ts                  ✅ (Testing Scenarios)
│   └── index.ts
├── dist/                                ✅ Compiled JS
├── jest.config.js                       ✅
├── package.json                         ✅
└── tsconfig.json                        ✅
```

---

**Document Status**: Ready for execution
**Last Updated**: 2026-01-06
