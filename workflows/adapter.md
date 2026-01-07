---
description: Create or update FDD adapter
---

# Create or Update FDD Adapter

**Type**: Operation  
**Role**: Project Manager, Architect  
**Artifact**: `{adapter-directory}/FDD-Adapter/AGENTS.md` and spec files

---

## Requirements

**MUST read**: `../requirements/adapter-structure.md`

Extract:
- Required file structure (AGENTS.md + specs/)
- Required AGENTS.md format (MUST WHEN instructions)
- Required spec files (domain-model, api-contracts, testing, build-deploy, project-structure, conventions)
- Validation criteria

---

## Prerequisites

**MUST validate**:
- [ ] Project repository exists - validate: Check .git directory exists
- [ ] Write permissions - validate: Can create directories and files

**No other prerequisites** - This is typically first workflow

---

## Steps

### 1. Detect Mode

Search for existing adapter in common locations:
- `spec/FDD-Adapter/AGENTS.md`
- `guidelines/FDD-Adapter/AGENTS.md`
- `docs/FDD-Adapter/AGENTS.md`

**If adapter found**:
- UPDATE mode - Read existing adapter, propose changes
- Store found location as `ADAPTER_DIR`

**If NOT found**:
- CREATE mode - Generate adapter from scratch
- Ask user for adapter location (Step 2)

### 2. Determine Adapter Location (CREATE mode only)

**Skip if UPDATE mode** (location already known)

Ask user:
**Context**: Choose adapter directory location

**Options**:
1. `spec/FDD-Adapter/` (recommended for technical projects)
2. `guidelines/FDD-Adapter/` (recommended for documentation-heavy projects)
3. `docs/FDD-Adapter/` (alternative)
4. Custom path

**Propose**: `spec/FDD-Adapter/` (most common)

Store as: `ADAPTER_DIR`

### 3. Mode-Specific Actions

**CREATE Mode**:
- Proceed to Step 4 for interactive input collection

**UPDATE Mode**:
- Read existing AGENTS.md and all spec files
- Extract current configuration:
  - Project name
  - Domain model technology and location
  - API contract technology and location
  - Testing frameworks and commands
  - Build commands
  - Project structure
  - Conventions
- Ask user: What to update?
  - Update domain model specs
  - Update API contract specs
  - Update testing specs
  - Update build/deploy specs
  - Update project structure
  - Update conventions
  - Add missing spec files
- Proceed to Step 4 with targeted questions

### 4. Interactive Input Collection

**Mode-specific behavior**:

**Q1: Project Name**
- Context: Name for this project
- **CREATE**: Propose based on repository name or package.json name
- **UPDATE**: Show current name, ask to change or keep
- Store as: `PROJECT_NAME`

**Q2: Domain Model Technology**
- Context: Technology for domain model definitions
- Examples: GTS, TypeScript, JSON Schema, Protobuf, OpenAPI schemas
- **CREATE**: Detect from project (look for .gts, .proto, schemas/)
- **UPDATE**: Show current technology, ask to change or keep
- Store as: `DML_TECH`

**Q3: Domain Model Location**
- Context: Where domain model files are stored (relative to project root)
- Examples: `gts/`, `schemas/`, `proto/`, `src/types/`
- **CREATE**: Detect from project structure
- **UPDATE**: Show current location, ask to update or keep
- Store as: `DML_LOCATION`

**Q4: API Contract Technology**
- Context: Technology for API definitions
- Examples: OpenAPI, gRPC, GraphQL, REST (no spec), tRPC
- **CREATE**: Detect from project files
- **UPDATE**: Show current technology, ask to change or keep
- Store as: `API_TECH`

**Q5: API Contract Location**
- Context: Where API specs are stored (relative to project root)
- Examples: `docs/api/`, `api/`, `openapi/`, `proto/`
- **CREATE**: Detect from project structure
- **UPDATE**: Show current location, ask to update or keep
- Store as: `API_LOCATION`

**Q6: Testing Framework**
- Context: Testing tools used
- Ask for: Unit test framework, Integration test framework, E2E framework
- **CREATE**: Detect from package.json, Cargo.toml, etc.
- **UPDATE**: Show current frameworks, ask to update or keep
- Store as: `TEST_FRAMEWORKS`

**Q7: Test Commands**
- Context: Commands to run tests
- Ask for: Test command, Coverage command
- **CREATE**: Detect from package.json scripts, Makefile
- **UPDATE**: Show current commands, ask to update or keep
- Store as: `TEST_COMMANDS`

**Q8: Build Commands**
- Context: Commands for build, clean, lint
- **CREATE**: Detect from package.json, Makefile, Cargo.toml
- **UPDATE**: Show current commands, ask to update or keep
- Store as: `BUILD_COMMANDS`

**Q9: Behavior Description Language**
- Context: Use FDL or custom
- Options: FDL (default) | Custom
- **CREATE**: Default to FDL
- **UPDATE**: Show current choice, ask to change or keep
- If custom, ask for spec file path
- Store as: `BDL_CHOICE`

### 5. Create Directory Structure (CREATE mode only)

**CREATE Mode**:
- Create directories: `{ADAPTER_DIR}/` and `{ADAPTER_DIR}/specs/`

**UPDATE Mode**:
- Skip (directories already exist)

### 6. Generate/Update Content

**CREATE mode**: Generate complete adapter from scratch

**UPDATE mode**: Update specific spec files based on changes

Generate/update content following `adapter-structure.md`:
- AGENTS.md - Header with Extends, MUST WHEN instructions
- `domain-model.md` - Technology, location, format, examples
- `api-contracts.md` - Technology, location, format, examples
- `testing.md` - Frameworks, commands, location
- `build-deploy.md` - Build, clean, lint commands
- `project-structure.md` - Architecture + source structure
- `conventions.md` - Coding standards, patterns

### 7. Summary and Confirmation

Show:
- **CREATE**: Adapter location: `{ADAPTER_DIR}` (new adapter)
- **UPDATE**: Adapter location: `{ADAPTER_DIR}` (updating existing)
- Files to be created/updated: AGENTS.md + spec files
- Technology stack summary
- All collected information
- Changes summary (for UPDATE mode)

Ask: Proceed? [yes/no/modify]

### 8. Create or Update Files

**CREATE Mode**:
- Create all directories
- Create AGENTS.md
- Create all 6 spec files

**UPDATE Mode**:
- Update AGENTS.md if needed
- Update modified spec files only
- Create missing spec files if any

After operation:
- Verify all files exist
- Verify content correct

---

## Validation

Run: `adapter-validate`

Expected:
- Score: ≥90/100
- Status: PASS
- All spec files validated

---

## Next Steps

**Recommended**:
- `adapter-agents` - Configure AI agent integration (optional)
- `business-context` - Start defining business requirements

**Can proceed without adapter** for:
- Product Manager workflows (business-context, business-validate)
- Early Architect workflows (design with defaults)
