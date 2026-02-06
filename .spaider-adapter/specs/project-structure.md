# Project Structure

## Root Directory

```
FDD/
├── .spaider-adapter/          # Project adapter (this directory)
├── .spaider-config.json       # Spaider configuration
├── AGENTS.md                 # Root navigation rules
├── README.md                 # Project documentation
├── Makefile                  # Build automation
├── LICENSE                   # License file
│
├── architecture/             # Design artifacts
│   ├── PRD.md               # Product Requirements Document
│   ├── DESIGN.md            # Technical Design
│   ├── specs/
│   │   └── DECOMPOSITION.md      # Specs Manifest
│   └── ADR/
│       └── general/         # Architecture Decision Records
│
├── weavers/                  # Weaver packages
│   └── sdlc/                # SDLC weaver
│       ├── artifacts/       # Artifact templates
│       ├── codebase/        # Code rules
│       └── guides/          # Usage guides
│
├── workflows/                # Spaider workflows
│   ├── generate.md          # Generation workflow
│   ├── analyze.md          # Analysis/validation workflow
│   └── adapter.md           # Adapter workflow
│
├── requirements/             # Spaider requirements specs
│   ├── execution-protocol.md
│   ├── adapter-structure.md
│   ├── artifacts-registry.md
│   ├── traceability.md
│   └── ...
│
├── schemas/                  # JSON schemas
│   ├── artifacts.schema.json
│   └── spaider-template-frontmatter.schema.json
│
├── skills/                   # Spaider skills
│   └── spaider/
│       ├── SKILL.md         # Skill definition
│       └── scripts/
│           └── spaider/      # CLI package
│
├── tests/                    # Test suite
│   ├── test_*.py            # Test modules
│   └── __init__.py
│
├── scripts/                  # Utility scripts
│   ├── check_coverage.py
│   └── score_comparison_matrix.py
│
└── guides/                   # User guides
    ├── ADAPTER.md
    └── TAXONOMY.md
```

---

## CLI Package Structure

```
skills/spaider/scripts/spaider/
├── __init__.py              # Package init (version info)
├── __main__.py              # Entry point for `python -m spaider`
├── cli.py                   # Main CLI (2398 lines)
│                            # - All subcommands
│                            # - Agent config generation
│                            # - Validation logic
├── constants.py             # Shared constants
│                            # - ARTIFACTS_REGISTRY_FILENAME
│                            # - CONFIG_FILENAME
│                            # - ADAPTER_AGENTS_FILENAME
│
└── utils/                   # Utility modules
    ├── __init__.py          # Re-exports all utilities
    ├── artifacts_meta.py    # artifacts.json parsing
    │                        # - Weaver, Artifact, SystemNode
    │                        # - ArtifactsMeta class
    ├── codebase.py          # Code file parsing
    │                        # - CodeFile, ScopeMarker
    │                        # - Spaider marker detection
    ├── context.py           # Global context
    │                        # - SpaiderContext
    │                        # - LoadedWeaver
    ├── document.py          # Document utilities
    ├── files.py             # File operations
    │                        # - find_project_root
    │                        # - find_adapter_directory
    │                        # - load_artifacts_registry
    ├── language_config.py   # Language-specific configs
    │                        # - Comment syntax detection
    ├── parsing.py           # Markdown parsing
    │                        # - Section splitting
    │                        # - ID extraction
    └── template.py          # Template parsing (1211 lines)
                             # - Template class
                             # - TemplateBlock
                             # - Artifact validation
```

---

## Weaver Package Structure

```
weavers/sdlc/
├── README.md                 # Weaver documentation
├── artifacts/
│   ├── README.md            # Artifacts overview
│   ├── PRD/
│   │   ├── template.md      # PRD template with markers
│   │   ├── rules.md         # Generation/validation rules
│   │   ├── checklist.md     # Review checklist
│   │   └── examples/
│   │       └── example.md   # Canonical example
│   ├── DESIGN/              # Same structure
│   ├── DECOMPOSITION/            # Same structure
│   ├── SPEC/             # Same structure
│   └── ADR/                 # Same structure
├── codebase/
│   ├── rules.md             # Code implementation rules
│   └── checklist.md         # Code review checklist
└── guides/
    ├── QUICKSTART.md
    ├── GREENFIELD.md
    ├── BROWNFIELD.md
    └── MONOLITH.md
```

---

## Agent Integration Directories

```
.cursor/
├── commands/                 # Cursor slash commands
│   ├── spaider.md
│   ├── spaider-adapter.md
│   ├── spaider-generate.md
│   └── spaider-analyze.md
└── rules/                    # Cursor rules

.claude/
├── commands/                 # Claude slash commands
└── settings.local.json       # Claude settings

.windsurf/
├── workflows/                # Windsurf workflows
└── skills/
    └── spaider/
        └── SKILL.md

.github/
├── copilot-instructions.md   # GitHub Copilot instructions
└── prompts/                  # Copilot prompts
```

---

## Key Files

| File | Purpose |
|------|---------|
| `.spaider-config.json` | Spaider config (adapter path) |
| `.spaider-adapter/artifacts.json` | Artifact registry |
| `.spaider-adapter/AGENTS.md` | Navigation rules |
| `AGENTS.md` | Root navigation (extends) |
| `Makefile` | Build/test commands |

---

**Source**: Project directory analysis
**Last Updated**: 2026-02-03
