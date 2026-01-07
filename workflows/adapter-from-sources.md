---
description: Create or update FDD adapter by analyzing existing codebase
---

# Create or Update FDD Adapter from Sources

**Type**: Operation  
**Role**: Project Manager, Architect  
**Artifact**: `{adapter-directory}/FDD-Adapter/AGENTS.md` and spec files

---

## Requirements

**MUST read**: `../requirements/adapter-structure.md`

Extract:
- Required file structure
- Required AGENTS.md format
- Required spec files
- Validation criteria

---

## Prerequisites

**MUST validate**:
- [ ] Project repository exists - validate: Check .git directory exists
- [ ] Codebase exists - validate: Check src/ or similar directories exist
- [ ] Write permissions - validate: Can create directories and files

**No other prerequisites** - Alternative to `adapter` workflow

---

## Steps

### 1. Detect Mode

Search for existing adapter in common locations:
- `spec/FDD-Adapter/AGENTS.md`
- `guidelines/FDD-Adapter/AGENTS.md`
- `docs/FDD-Adapter/AGENTS.md`

**If adapter found**:
- UPDATE mode - Re-analyze codebase, propose updates to adapter
- Store found location as `ADAPTER_DIR`

**If NOT found**:
- CREATE mode - Analyze codebase, generate new adapter
- Will determine location in Step 3

### 2. Analyze Codebase

**Scan project structure**:
- Detect package manager (package.json, Cargo.toml, requirements.txt, go.mod)
- Detect language and framework
- Find domain model files (types, schemas, proto)
- Find API specs (openapi, graphql, proto)
- Find test directories and configs
- Find build configs (Makefile, package.json scripts)

**Store detected information** for proposals

### 2. Determine Adapter Location

Ask user:
**Context**: Choose adapter directory location

**Options**:
1. `spec/FDD-Adapter/` (recommended for technical projects)
2. `guidelines/FDD-Adapter/` (recommended for documentation-heavy projects)
3. `docs/FDD-Adapter/` (alternative)
4. Custom path

**Propose**: `spec/FDD-Adapter/` (most common)

Store as: `ADAPTER_DIR`

### 3. Interactive Input with Proposals

**Q1: Project Name**
- Context: Name for this project
- **Propose**: Detected from package.json, Cargo.toml, or repository name
- Show detection: "Detected: {name} from {source}"
- Allow modification

**Q2: Domain Model Technology**
- Context: Technology for domain model definitions
- **Propose**: Detected from file extensions and structure
  - If `.gts` files found → "GTS"
  - If `.proto` files found → "Protobuf"
  - If `schemas/*.json` → "JSON Schema"
  - If TypeScript types → "TypeScript"
- Show detection: "Detected: {tech} from {files}"
- Allow modification

**Q3: Domain Model Location**
- Context: Where domain model files are stored
- **Propose**: Detected directory (gts/, schemas/, proto/, src/types/)
- Show detection: "Detected: `{path}` ({count} files found)"
- Allow modification

**Q4: API Contract Technology**
- Context: Technology for API definitions
- **Propose**: Detected from files
  - If openapi.yaml → "OpenAPI"
  - If .proto with services → "gRPC"
  - If graphql schema → "GraphQL"
  - If REST routes without spec → "REST (no spec)"
- Show detection: "Detected: {tech} from {files}"
- Allow modification

**Q5: API Contract Location**
- Context: Where API specs are stored
- **Propose**: Detected directory (docs/api/, api/, openapi/, proto/)
- Show detection: "Detected: `{path}` ({count} files found)"
- Allow modification

**Q6: Testing Framework**
- Context: Testing tools used
- **Propose**: Detected from package.json devDependencies, Cargo.toml dev-dependencies
  - Unit tests: jest, pytest, cargo test
  - Integration: same as unit or detected
  - E2E: playwright, cypress, pytest
- Show detection: "Detected: {frameworks}"
- Allow modification

**Q7: Test Commands**
- Context: Commands to run tests
- **Propose**: Detected from package.json scripts, Makefile, Cargo.toml
  - Test: `npm test`, `cargo test`, `make test`, `pytest`
  - Coverage: `npm run coverage`, `cargo tarpaulin`, `make coverage`
- Show detection: "Detected: test=`{cmd}`, coverage=`{cmd}`"
- Allow modification

**Q8: Build Commands**
- Context: Commands for build, clean, lint
- **Propose**: Detected from package.json, Makefile, Cargo.toml
  - Build: `npm run build`, `cargo build --release`, `make build`
  - Clean: `npm run clean`, `cargo clean`, `make clean`
  - Lint: `npm run lint`, `cargo clippy`, `make lint`
- Show detection: "Detected: build=`{cmd}`, clean=`{cmd}`, lint=`{cmd}`"
- Allow modification

**Q9: Behavior Description Language**
- Context: Use FDL or custom
- **Propose**: FDL (default, no custom detected)
- Allow specification of custom if needed

### 4. Show Analysis Summary

Display detected project structure:
```
Project Analysis Summary:

**Detected**:
- Language: {language}
- Framework: {framework}
- Package Manager: {package manager}
- Domain Model: {tech} at {location} ({count} files)
- API Contracts: {tech} at {location} ({count} files)
- Tests: {frameworks}
- Build: {build system}

**Will create**:
- Adapter at: {ADAPTER_DIR}
- AGENTS.md with navigation
- 6 specification files

Proceed with detected configuration? [yes/no/modify]
```

### 5. Create Directory Structure

Create directories:
- `{ADAPTER_DIR}/`
- `{ADAPTER_DIR}/specs/`

### 6. Generate AGENTS.md

Create `{ADAPTER_DIR}/AGENTS.md` following `adapter-structure.md` format

### 7. Generate Specification Files

Create 6 spec files in `{ADAPTER_DIR}/specs/` using detected/confirmed information

Include detected examples from codebase

### 8. Summary and Confirmation

Show:
- Adapter location
- All files created
- Detected vs user-modified values
- Examples extracted from codebase

Ask: Create files? [yes/no]

### 9. Create Files

After confirmation:
- Create all directories
- Create AGENTS.md
- Create all spec files with detected information
- Verify creation successful

---

## Detection Logic

### Package Manager Detection
```
Check files in order:
1. package.json → npm/yarn/pnpm
2. Cargo.toml → Cargo
3. go.mod → Go modules
4. requirements.txt → pip
5. pom.xml → Maven
```

### Domain Model Detection
```
Search for:
1. *.gts files → GTS
2. *.proto files → Protobuf
3. schemas/*.json → JSON Schema
4. src/types/*.ts → TypeScript
5. *.graphql → GraphQL Schema
```

### API Contract Detection
```
Search for:
1. openapi.yaml, swagger.yaml → OpenAPI
2. *.proto with service definitions → gRPC
3. schema.graphql → GraphQL
4. REST route files without spec → REST (no spec)
```

---

## Validation

Run: `adapter-validate`

Expected:
- Score: ≥90/100
- Status: PASS
- All detected information validated

---

## Next Steps

**Recommended**:
- `adapter-agents` - Configure AI agent integration (optional)
- `business-context` - Start defining business requirements

**Advantage over `adapter`**:
- Faster (proposes instead of asks)
- More accurate (based on actual codebase)
- Better examples (extracted from code)
