# FDD Adapter Creation Guide

**Purpose**: Step-by-step guide for creating a project-specific FDD adapter

**Audience**: Technical leads, architects setting up FDD for their project

---

## What is an Adapter?

An **adapter** connects FDD's universal methodology to your project's specific:
- Technology stack (language, framework)
- Specification formats (domain model, API contracts)
- Development patterns (database, authentication, testing)

**Core FDD is universal** - adapters make it practical for your tech stack.

---

## Prerequisites

Before creating an adapter, ensure you have:

1. **Chosen specification technologies**:
   - Domain model format (JSON Schema, TypeScript, Protobuf, etc.)
   - API contract format (OpenAPI, GraphQL Schema, gRPC, etc.)

2. **Identified project patterns**:
   - Database access patterns (ORM, query builders, raw SQL)
   - Authentication/authorization approach
   - Testing strategy (unit, integration, e2e)

3. **Set up FDD core**:
   ```bash
   your-project/
   └── guidelines/
       └── FDD/  # Core FDD methodology
   ```

---

## Step 1: Create Adapter Directory

Create your adapter next to FDD core:

```bash
mkdir -p guidelines/your-project-fdd-adapter
cd guidelines/your-project-fdd-adapter
```

**Naming convention**: `{project-name}-fdd-adapter`

Examples:
- `hyperspot-fdd-adapter`
- `ecommerce-fdd-adapter`
- `analytics-fdd-adapter`

---

## Step 2: Create Adapter Structure

Create these files in your adapter directory:

```bash
guidelines/your-project-fdd-adapter/
├── README.md                    # Integration overview
├── AGENTS.md                    # AI agent instructions (project-specific)
├── PATTERNS.md                  # Technology-specific patterns
├── VALIDATION.md                # Validation requirements
└── COMMON_PITFALLS.md          # Common mistakes and solutions
```

---

## Step 3: Write README.md (Integration Overview)

**Purpose**: Explain how FDD integrates with your project

**Template**:

```markdown
# {Project Name} FDD Adapter

**Purpose**: Integrate FDD with {Project Name}'s {tech stack}

## Technology Choices

### Domain Model
- **Format**: {JSON Schema / TypeScript / Protobuf / etc.}
- **Location**: `{path to domain model specs}`
- **Validation**: {how to validate}
- **Code Generation**: {if applicable}

### API Contracts
- **Format**: {OpenAPI / GraphQL Schema / gRPC / etc.}
- **Location**: `{path to API specs}`
- **Validation**: {how to validate}
- **Code Generation**: {if applicable}

## Feature Structure

```
architecture/features/feature-{slug}/
├── DESIGN.md                    # Feature design (FDD format)
├── {domain-model-files}         # Domain model specs
├── {api-spec-files}             # API specs
└── openspec/                    # OpenSpec changes
```

## Quick Start

1. Initialize FDD structure:
   ```bash
   # Follow FDD workflow
   cat ../FDD/workflows/01-init-project.md
   ```

2. Create your first feature:
   ```bash
   # Follow FDD workflow
   cat ../FDD/workflows/05-init-feature.md
   ```

3. Review project-specific patterns:
   ```bash
   cat PATTERNS.md
   ```

## References

- **Core FDD**: `../FDD/README.md`
- **Patterns**: `PATTERNS.md`
- **Common Pitfalls**: `COMMON_PITFALLS.md`

---

## Step 4: Write AGENTS.md (AI Instructions)

**Purpose**: Provide AI agents with project-specific instructions

**Template**:

```markdown
# AI Agent Instructions for {Project Name}

**READ THIS FIRST**: Project-specific FDD instructions. Read `../FDD/AGENTS.md` first for core methodology.

---

## Project-Specific Rules

### Domain Model

**Format**: {JSON Schema / TypeScript / Protobuf / etc.}
**Location**: `{path}`

**Rules**:
- {Rule 1 - e.g., "Use PascalCase for type names"}
- {Rule 2 - e.g., "All types must have descriptions"}
- {Rule 3 - e.g., "Use strict validation"}

**Example**:
```{format}
{example domain model type}
```

### API Contracts

**Format**: {OpenAPI / GraphQL Schema / etc.}
**Location**: `{path}`

**Rules**:
- {Rule 1 - e.g., "Use /api/v1 prefix"}
- {Rule 2 - e.g., "All endpoints must have 401/403 responses"}
- {Rule 3 - e.g., "Use JSON for request/response"}

### Database Access

**Pattern**: {ORM / Query Builder / Raw SQL}

**Rules**:
- {Rule 1}
- {Rule 2}

### Authentication

**Pattern**: {JWT / Session / OAuth}

**Rules**:
- {Rule 1}
- {Rule 2}

### Testing

**Patterns**:
- Unit tests: {where and how}
- Integration tests: {where and how}
- E2E tests: {where and how}

---

## Validation Commands

```bash
# Validate domain model
{command to validate domain model}

# Validate API specs
{command to validate API specs}

# Run tests
{command to run tests}
```

---

## Common Patterns

### Pattern 1: {Name}

**When to use**: {description}

**Implementation**:
```{language}
{code example}
```

### Pattern 2: {Name}

{...}

---

## References

- **Core FDD**: `../FDD/AGENTS.md`
- **Patterns**: `PATTERNS.md`
- **Pitfalls**: `COMMON_PITFALLS.md`

---

## Step 5: Write PATTERNS.md (Technology Patterns)

**Purpose**: Document technology-specific implementation patterns

**Template**:

```markdown
# {Project Name} Implementation Patterns

Technology-specific patterns for implementing FDD features.

---

## Database Patterns

### Pattern: Create Entity

**Implementation**:
```{language}
{code example}
```

### Pattern: Query with Relations

**Implementation**:
```{language}
{code example}
```

---

## API Patterns

### Pattern: REST Endpoint

**Implementation**:
```{language}
{code example}
```

### Pattern: Error Response

**Implementation**:
```{language}
{code example}
```

---

## Authentication Patterns

### Pattern: Protected Route

**Implementation**:
```{language}
{code example}
```

---

## Testing Patterns

### Pattern: Unit Test

**Implementation**:
```{language}
{code example}
```

### Pattern: Integration Test

**Implementation**:
```{language}
{code example}
```

---

## Validation Patterns

### Pattern: Input Validation

**Implementation**:
```{language}
{code example}
```

---

## Step 6: Write VALIDATION.md (Validation Requirements)

**Purpose**: Define project-specific validation rules

**Template**:

```markdown
# {Project Name} Validation Requirements

Project-specific validation rules and checks.

---

## Domain Model Validation

**Command**:
```bash
{command to validate domain model}
```

**Requirements**:
- [ ] All types have descriptions
- [ ] All fields have types
- [ ] {project-specific rule}
- [ ] {project-specific rule}

---

## API Contract Validation

**Command**:
```bash
{command to validate API specs}
```

**Requirements**:
- [ ] All endpoints documented
- [ ] All responses defined (200, 400, 401, 403, 500)
- [ ] {project-specific rule}
- [ ] {project-specific rule}

---

## Code Validation

**Pre-commit checks**:
```bash
# Type checking
{command}

# Linting
{command}

# Tests
{command}
```

**CI/CD checks**:
```bash
# Build
{command}

# Test suite
{command}

# Integration tests
{command}
```

---

## Feature Validation Checklist

Before marking feature complete:

- [ ] Domain model specs valid
- [ ] API specs valid
- [ ] All tests pass
- [ ] Code compiles/type-checks
- [ ] Linting passes
- [ ] {project-specific check}
- [ ] {project-specific check}

---

## Step 7: Write COMMON_PITFALLS.md

**Purpose**: Document common mistakes and solutions

**Template**:

```markdown
# {Project Name} Common Pitfalls

Common mistakes when implementing FDD features in {Project Name}.

---

## Pitfall 1: {Name}

**Symptom**: {what developers see}

**Cause**: {why it happens}

**Solution**:
```{language}
// Bad
{bad example}

// Good
{good example}
```

---

## Pitfall 2: {Name}

{...}

---

## Debugging Guide

### Issue: {Common issue}

**Symptoms**:
- {symptom 1}
- {symptom 2}

**Diagnosis**:
```bash
{commands to diagnose}
```

**Fix**:
{step-by-step fix}

---

## Performance Considerations

### Consideration 1: {Name}

**Issue**: {what can go wrong}

**Solution**: {how to avoid}

---

## Security Considerations

### Consideration 1: {Name}

**Issue**: {security risk}

**Solution**: {how to secure}

---

## Step 8: Test Your Adapter

1. **Create test feature**:
   ```bash
   # Follow FDD workflows
   cat ../FDD/workflows/05-init-feature.md
   ```

2. **Implement using adapter patterns**:
   - Use domain model format from adapter
   - Use API contract format from adapter
   - Follow implementation patterns from PATTERNS.md

3. **Validate**:
   ```bash
   # Run validation commands from VALIDATION.md
   ```

4. **Iterate**:
   - Update adapter based on learnings
   - Document new patterns
   - Add common pitfalls

---

## Step 9: Team Onboarding

Create onboarding checklist for new team members:

```markdown
# {Project Name} FDD Onboarding

## Reading (30 min)
- [ ] Read `../FDD/README.md` - Core FDD methodology
- [ ] Read `README.md` - Project integration
- [ ] Read `PATTERNS.md` - Implementation patterns

## Setup (15 min)
- [ ] Install FDD tools (if any)
- [ ] Configure IDE (see main project README)
- [ ] Run validation commands

## Practice (2 hours)
- [ ] Review existing feature: `architecture/features/feature-{example}/`
- [ ] Create small feature following workflows
- [ ] Get feedback from team lead
```

---

## Maintenance

### When to Update Adapter

- **Technology changes**: New framework version, new patterns
- **New patterns discovered**: Team finds better approach
- **Common pitfalls identified**: Same mistake happens multiple times
- **Validation rules change**: New checks needed

### How to Update

1. Update relevant file (PATTERNS.md, PITFALLS.md, etc.)
2. Notify team of changes
3. Update existing features if needed (create migration plan)

---

## Example Adapters

### My FDD Adapter

**Stack**:
- Domain Model: JSON Schema (GTS)
- API Contracts: OpenAPI
- Database: Prisma ORM
- API: Express + TypeScript

**Reference** for creating your own adapter.

---

## Getting Help

- **Core FDD questions**: See `../FDD/README.md`

---

## Checklist: Is Your Adapter Complete?

- [ ] README.md explains integration
- [ ] AGENTS.md provides AI-specific instructions
- [ ] PATTERNS.md documents implementation patterns
- [ ] VALIDATION.md defines validation rules
- [ ] COMMON_PITFALLS.md helps avoid mistakes
- [ ] Example feature demonstrates all patterns
- [ ] Team onboarding process documented
- [ ] Validation commands work and pass
