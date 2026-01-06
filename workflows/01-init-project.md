# Initialize FDD Project

**Phase**: 1 - Architecture Design  
**Purpose**: Create FDD project structure with Overall Design template through guided questions

**Structure Requirements**: See `../requirements/overall-design-structure.md` for complete Overall Design structure specification

---

## Prerequisites

- FDD adapter exists and is valid (run workflow `adapter-config` first if needed)
- Project repository exists
- Write permissions in project directory

---

## ⚠️ CRITICAL CHECKLIST - MUST COMPLETE ALL

This workflow has **6 mandatory requirements**. You MUST complete ALL before finishing:

- [ ] **Requirement 1**: Create directory structure (architecture/, features/, diagrams/)
- [ ] **Requirement 2**: Create domain model files (from adapter specification)
- [ ] **Requirement 3**: Create API contract files (from adapter specification)
- [ ] **Requirement 4**: Create openspec structure (specs/, changes/, changes/archive/)
- [ ] **Requirement 5**: Create openspec/project.md with project conventions
- [ ] **Requirement 6**: Generate architecture/DESIGN.md with all sections A-D

**STOP after each requirement and verify completion before proceeding to next.**

**If you skip ANY requirement, validation will FAIL in Phase 3 (workflow 02).**

---

## Overview

This workflow creates FDD project structure and Overall Design document through interactive questions. The workflow gathers project context first, then generates structured documentation with actual content instead of empty placeholders.

**Key Principle**: Ask questions, generate meaningful content, avoid empty templates.

---

## Interactive Questions

Ask the user these questions **one by one** to gather requirements:

### Q1: Module/System Name
```
What is the name of this module or system?
Example: "User Management Service", "Payment API", "Analytics Dashboard"
```
**Store as**: `MODULE_NAME`

### Q2: System Vision
```
What does this system do and why does it exist?
Describe in 2-4 sentences the core purpose and value.

Example: "This system manages user authentication and authorization 
for the platform. It provides secure login, role-based access control, 
and user profile management. The goal is to centralize identity 
management across all services."
```
**Store as**: `SYSTEM_VISION`

### Q3: Core Capabilities
```
What are the main capabilities this system provides?
List 3-7 key capabilities (one per line):

Example:
- User registration and login
- Password reset and recovery
- Role and permission management
- User profile management
- Session management
```
**Store as**: `CAPABILITIES[]`

### Q4: Actors
```
Who are the actors (users/systems) that interact with this system?
For each actor, provide:
- Actor name
- Role and responsibilities

Example:
- End User: Regular user who logs in and manages their profile
- Administrator: Manages users, roles, and permissions
- External Service: Other services that validate tokens and check permissions
```
**Store as**: `ACTORS[]` (each with name and description)

### Q5: Key Business Rules
```
What are the key business rules or principles for this system?
List 2-5 important rules that guide the design.

Example:
- Passwords must meet complexity requirements (8+ chars, mixed case, numbers)
- Sessions expire after 24 hours of inactivity
- Users can only have one active session at a time
- All authentication attempts are logged for security audit
```
**Store as**: `BUSINESS_RULES[]`

### Q6: Architecture Style
```
What is the architectural style of this system?
Options:
  1. Monolithic application
  2. Microservice
  3. CLI tool
  4. Library/SDK
  5. Serverless functions
  6. Other (specify)
```
**Store as**: `ARCHITECTURE_STYLE`

**If user selects "Other"**, ask:
```
Please describe the architectural style: ___
```

### Q7: Additional Context (Optional)
```
Is there any additional context about this system?

Examples:
- Integration requirements
- Performance constraints
- Compliance requirements
- Migration from existing system

Additional context (optional, free form): ___
```
**Store as**: `ADDITIONAL_CONTEXT`

### Q8: Naming Conventions
```
What naming conventions should be used for changes and specs?

Examples:
- Change IDs: "add-", "update-", "fix-", "refactor-" prefix
- Spec names: kebab-case, descriptive (e.g., "user-authentication")
- File naming: lowercase-with-dashes

Describe conventions (or press Enter for defaults): ___
```
**Store as**: `NAMING_CONVENTIONS`
**Default**: "Use verb-led kebab-case for changes (add-, update-, fix-), descriptive kebab-case for spec names"

### Q9: Code Standards
```
What code standards and patterns should be followed?

Examples:
- Language style guides (e.g., PEP 8, ESLint config)
- Architecture patterns (e.g., MVC, Clean Architecture)
- Anti-patterns to avoid

Describe standards (or press Enter for defaults): ___
```
**Store as**: `CODE_STANDARDS`
**Default**: "Follow language-specific best practices and consistent code style"

### Q10: Testing Requirements
```
What are the testing requirements?

Examples:
- Unit test coverage: 80%
- Integration tests for all API endpoints
- Contract tests for external services
- Performance benchmarks

Describe requirements (or press Enter for defaults): ___
```
**Store as**: `TESTING_REQUIREMENTS`
**Default**: "Unit tests for business logic, integration tests for API endpoints"

### Q11: Deployment Context
```
What is the deployment context?

Examples:
- CI/CD: GitHub Actions, Jenkins
- Environments: dev, staging, production
- Deployment strategy: blue-green, rolling updates

Describe context (or press Enter for defaults): ___
```
**Store as**: `DEPLOYMENT_CONTEXT`
**Default**: "Standard CI/CD pipeline with dev, staging, and production environments"

---

## Requirements

### 1. Create Directory Structure

**Requirement**: Establish core FDD directory hierarchy

**Required Directories**:
- `architecture/` - Overall Design and feature designs
  - `architecture/features/` - Feature-specific designs
  - `architecture/diagrams/` - Architecture diagrams
- DML specification directory (location per adapter)
- API contract specification directory (location per adapter)

**Expected Outcome**: All required directories exist and are accessible

**Validation Criteria**:
- Directory `architecture/features/` exists
- Directory `architecture/diagrams/` exists
- DML specification directory exists (per adapter)
- API contract specification directory exists (per adapter)

**Note**: Specific directory structure (e.g., `gts/`, `openapi/`) defined by adapter

---

### 2. Generate Overall Design Document

**Requirement**: Create `architecture/DESIGN.md` with actual content based on collected answers

**Required Content**:
Generate `architecture/DESIGN.md` according to structure defined in `../requirements/overall-design-structure.md`:

**Structure** (see requirements file for complete specification):
- Section A: Business Context (vision, capabilities, actors)
- Section B: Requirements & Principles (use cases, business rules, design principles)
- Section C: Technical Architecture (5 subsections: C.1-C.5)
- Section D: Project-Specific Details (optional)

**Content Mapping** (answers → sections):
- **Section A**:
  - System Vision ← Q2 (SYSTEM_VISION)
  - Core Capabilities ← Q3 (CAPABILITIES list with descriptions)
  - Actors ← Q4 (ACTORS list with roles)
  
- **Section B**:
  - Use Cases ← Generate from actors + capabilities (2-3 per actor)
  - Business Rules ← Q5 (BUSINESS_RULES list)
  - Design Principles ← Auto-generate FDD principles
  
- **Section C**:
  - C.1 (Architecture Overview) ← Q6 (ARCHITECTURE_STYLE + key components)
  - C.2 (Domain Model) ← Adapter (DML_TECH, DML_LOCATION, syntax reference)
  - C.3 (API Contracts) ← Adapter (API_TECH, API_LOCATION, spec reference)
  - C.4 (Security Model) ← Adapter (SECURITY_MODEL)
  - C.5 (Non-Functional Requirements) ← Adapter (NFR_LIST) + architecture style NFRs
  
- **Section D** (optional):
  - Project-Specific Details ← Q7 (ADDITIONAL_CONTEXT, if provided)

**Generation Instructions**:
1. Read `../requirements/overall-design-structure.md` for complete structure specification
2. Use answers from interactive questions to populate sections
3. Follow section format exactly as specified in requirements
4. Include "Document Status" and "Next Steps" at the end
5. Ensure ≥200 lines with substantive content (no placeholders)

**Expected Outcome**: DESIGN.md with meaningful initial content

**Verification** (MANDATORY):
```bash
# Verify DESIGN.md created and has content
test -f architecture/DESIGN.md && echo "✅ DESIGN.md exists" || echo "❌ MISSING DESIGN.md"
wc -l architecture/DESIGN.md | awk '{print ($1 >= 200) ? "✅ DESIGN.md has "$1" lines" : "❌ DESIGN.md too short: "$1" lines"}'
grep -q "## Section A: Business Context" architecture/DESIGN.md && echo "✅ Section A present" || echo "❌ Section A missing"
grep -q "## Section D: Architecture Decision Records" architecture/DESIGN.md && echo "✅ Section D present" || echo "❌ Section D missing"
```

**STOP if verification fails** - Do not proceed until DESIGN.md is complete.

---

### 4. Create Features Manifest Placeholder

**Requirement**: Initialize features tracking document

**Required Content**:
```markdown
# Features Manifest: {MODULE_NAME}

**Status**: PLANNING

## Features

Features will be generated after Overall Design validation.

**Next Steps**:
1. Complete Overall Design (add domain model types and API endpoints)
2. Validate architecture (workflow 02-validate-architecture)
3. Generate features (workflow 03-init-features)
```

**Expected Outcome**: Features manifest placeholder created

**Validation Criteria**:
- File `architecture/features/FEATURES.md` exists
- Contains module name from Q1
- References next workflows

---

### 5. Create OpenSpec Project Conventions

**Requirement**: Initialize `openspec/project.md` with project-specific conventions for OpenSpec changes and specs

**Required Actions**:
- Create directory: `openspec/`
- Create subdirectories: `openspec/specs/`, `openspec/changes/`, `openspec/changes/archive/`

**Required Content**:
Generate `openspec/project.md` with the following structure and content from Q8-Q11:

```markdown
# OpenSpec Project Conventions: {MODULE_NAME}

This document defines project-specific conventions for creating OpenSpec changes and specifications.

**Read this before creating any changes or specs.**

---

## Project Overview

**System**: {MODULE_NAME from Q1}

**Architecture**: {ARCHITECTURE_STYLE from Q6}

**Technology Stack**:
- Domain Model: {DML_TECH from adapter}
- API Contracts: {API_TECH from adapter}

---

## Naming Conventions

{NAMING_CONVENTIONS from Q8}

### Change ID Format

Use verb-led kebab-case for change IDs:
- `add-*` - New features or capabilities
- `update-*` - Modifications to existing features
- `fix-*` - Bug fixes (use only for bugs, not enhancements)
- `refactor-*` - Code restructuring without behavior changes
- `remove-*` - Deprecation or removal

**Examples**:
- `add-user-authentication`
- `update-payment-validation`
- `fix-session-timeout`

### Spec Naming

Use descriptive kebab-case for spec names:
- Format: `fdd-{project-slug}-feature-{feature-slug}`
- Keep names concise but clear
- Match feature names from `architecture/features/`

---

## Code Standards

{CODE_STANDARDS from Q9}

### Required Practices

- Follow language-specific style guides
- Use consistent formatting (automated formatters preferred)
- Document public APIs and complex logic
- Avoid anti-patterns specific to this project

---

## Testing Requirements

{TESTING_REQUIREMENTS from Q10}

### Coverage Expectations

- Unit tests: Test business logic and algorithms
- Integration tests: Test API endpoints and external integrations
- Contract tests: Verify external service contracts
- Performance tests: Benchmark critical paths (if applicable)

### Test Documentation

- Include test scenarios in Feature DESIGN.md Section F
- Reference test scenarios in OpenSpec change specs
- Keep tests maintainable and readable

---

## Deployment Context

{DEPLOYMENT_CONTEXT from Q11}

### Environments

- Development: Local and CI
- Staging: Pre-production validation
- Production: Live environment

### CI/CD Pipeline

- All changes must pass automated tests
- Changes require review before merge
- Deployments follow project deployment strategy

---

## OpenSpec Change Guidelines

**For complete OpenSpec change structure and requirements**, see:
- `../requirements/openspec-change-structure.md` - Full specification of change directory structure, required files, and validation criteria

**Key points**:
- All changes follow structure defined in requirements file
- Changes are atomic and implement 1-5 requirements from Feature DESIGN.md
- Integration with Feature Design Section F (Requirements) and Section G (Implementation Plan)

---

**Document Status**: Project conventions defined

**Last Updated**: {Current date}
```

**Expected Outcome**: File `openspec/project.md` exists with project conventions

**Validation Criteria**:
- Directory `openspec/` exists with subdirectories
- File `openspec/project.md` exists
- Contains module name from Q1
- Contains naming conventions from Q8 (or defaults)
- Contains code standards from Q9 (or defaults)
- Contains testing requirements from Q10 (or defaults)
- Contains deployment context from Q11 (or defaults)
- Contains architecture style from Q6
- References adapter settings (DML_TECH, API_TECH)
- No empty placeholders

---

### 6. Initialize API Contract Directory

**Requirement**: Create API specification directory structure per adapter settings

**Required Actions**:
- Create directory: {API_LOCATION from adapter}
- Note: Specific API contract files will be created as part of Overall Design development

**Expected Outcome**: API specification directory exists and is ready for use

**Validation Criteria**:
- Directory {API_LOCATION} exists
- Directory is writable
───────────────────────────────────
Module: {MODULE_NAME}
Architecture: {ARCHITECTURE_STYLE}

Will create:
✓ architecture/
  ✓ DESIGN.md (with content from your answers)
  ✓ features/
    ✓ FEATURES.md (placeholder)
  ✓ diagrams/
✓ {DML_LOCATION from adapter}/
✓ {API_LOCATION from adapter}/
✓ openspec/ (project-level change management)
  ✓ specs/ (feature specifications)
  ✓ changes/ (implementation changes)
  ✓ project.md (OpenSpec conventions)

DESIGN.md will include:
- System vision: {first 60 chars of SYSTEM_VISION}...
- {count} capabilities
- {count} actors
- {count} business rules
- Technical architecture (from adapter)
{If ADDITIONAL_CONTEXT: "- Additional project context"}

Proceed with initialization? (y/n)
```

**Expected Outcome**: User confirms or cancels

**Validation Criteria**:
- Summary shows all files to be created
- User can review before proceeding
- Easy to abort if needed

---

### 7. Version Control Integration (Optional)

**Requirement**: Add FDD structure to version control system

**Ask user**:
```
Commit changes to version control? (y/n)
```

**If yes**:
- Stage all created FDD directories and files
- Commit with message: "Initialize FDD project: {MODULE_NAME}"
- Verify commit successful

**Expected Outcome**: FDD structure under version control (if requested)

**Validation Criteria**:
- All FDD directories tracked in VCS
- Initial commit exists with FDD structure

---

## Final Verification Checklist

**Before completing this workflow, verify ALL items:**

```bash
echo "=== Workflow 01 Final Verification ==="
echo ""

# Requirement 1: Directory structure
test -d architecture && echo "✅ architecture/" || echo "❌ CRITICAL: Missing architecture/"
test -d architecture/features && echo "✅ architecture/features/" || echo "❌ CRITICAL: Missing architecture/features/"
test -d architecture/diagrams && echo "✅ architecture/diagrams/" || echo "❌ CRITICAL: Missing architecture/diagrams/"

echo ""

# Requirement 2-3: Domain model & API contracts (check adapter for location)
echo "Note: Check adapter for exact domain model and API contract locations"
test -d schemas && echo "✅ Domain model directory found (schemas/)" || echo "⚠️  Domain model directory - verify with adapter"
test -d spec && echo "✅ API contract directory found (spec/)" || echo "⚠️  API contract directory - verify with adapter"

echo ""

# Requirement 4-5: OpenSpec structure (CRITICAL - most commonly missed)
test -d openspec && echo "✅ openspec/" || echo "❌ CRITICAL: Missing openspec/ - GO BACK TO REQUIREMENT 4"
test -d openspec/specs && echo "✅ openspec/specs/" || echo "❌ CRITICAL: Missing openspec/specs/"
test -d openspec/changes && echo "✅ openspec/changes/" || echo "❌ CRITICAL: Missing openspec/changes/"
test -d openspec/changes/archive && echo "✅ openspec/changes/archive/" || echo "❌ CRITICAL: Missing openspec/changes/archive/"
test -f openspec/project.md && echo "✅ openspec/project.md" || echo "❌ CRITICAL: Missing openspec/project.md - GO BACK TO REQUIREMENT 5"

echo ""

# Requirement 6: Overall Design
test -f architecture/DESIGN.md && echo "✅ architecture/DESIGN.md" || echo "❌ CRITICAL: Missing DESIGN.md"
if [ -f architecture/DESIGN.md ]; then
  LINES=$(wc -l < architecture/DESIGN.md)
  [ $LINES -ge 200 ] && echo "✅ DESIGN.md has $LINES lines (≥200)" || echo "❌ DESIGN.md too short: $LINES lines (need ≥200)"
  grep -q "## Section A: Business Context" architecture/DESIGN.md && echo "✅ Section A present" || echo "❌ Section A missing"
  grep -q "## Section B: Requirements" architecture/DESIGN.md && echo "✅ Section B present" || echo "❌ Section B missing"
  grep -q "## Section C: Technical Architecture" architecture/DESIGN.md && echo "✅ Section C present" || echo "❌ Section C missing"
  grep -q "## Section D: Architecture Decision Records" architecture/DESIGN.md && echo "✅ Section D present" || echo "❌ Section D missing"
fi

echo ""
echo "=== End Verification ==="
echo ""
echo "✅ All checks must pass before proceeding to workflow 02."
echo "❌ If ANY ❌ appears, go back and complete that requirement."
echo ""
```

**All checks must show ✅ before workflow is complete.**

**If ANY check shows ❌**:
1. Identify which requirement number failed (1-6)
2. Scroll up to that requirement section in this workflow
3. Complete the missing steps
4. Re-run this verification script
5. Repeat until all checks pass

**Most common failure**: Missing openspec structure (Requirements 4-5)
- If you see ❌ for openspec/, go back to Requirement 4 and create the directories
- If you see ❌ for openspec/project.md, go back to Requirement 5 and create the file

---

**Interactive Mode**: See `../AGENTS.md` for interactive workflow rules (DO/DO NOT)

---

## Common Challenges

### Challenge: User Unsure About System Vision

**Resolution**: Guide user with examples. Ask clarifying questions:
- What problem does this solve?
- Who will use it?
- What's the primary value?

### Challenge: Too Many or Too Few Capabilities

**Resolution**: Aim for 3-7 core capabilities. If more, suggest grouping related ones. If fewer, explore if capabilities can be broken down.

### Challenge: Unclear Actor Roles

**Resolution**: Focus on "who does what". Each actor should have clear responsibilities. Examples help clarify.

### Challenge: Existing Project Structure

**Resolution**: FDD structure integrates alongside existing directories. It's documentation layer, not replacement.

---

## Next Activities

After project initialization:

1. **Complete Domain Model Types**: Edit `architecture/DESIGN.md` Section C
   - Add type definitions per DML specification
   - Define entities, value objects, DTOs
   - Document relationships

2. **Define API Endpoints**: Edit `architecture/DESIGN.md` Section C
   - Specify endpoints per API specification
   - Document request/response formats
   - Define error responses

3. **Validate Architecture**: Run workflow `02-validate-architecture.md`
   - Ensures completeness
   - Validates structure
   - Checks consistency

4. **Generate Features**: After validation, run workflow `03-init-features.md`
   - Extracts features from capabilities
   - Creates feature structure
   - Establishes dependencies

---

## References

- **Methodology**: `../AGENTS.md` - Overall Design guidelines
- **Next Workflow**: `02-validate-architecture.md`
