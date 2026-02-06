# Spaider Tool

Unified Spaider tool for artifact validation, search, and traceability.

## Commands

| Command | Description |
|---------|-------------|
| `validate` | Validate Spaider artifacts against templates |
| `validate-weavers` | Validate weaver configuration and templates |
| `validate-code` | Validate Spaider traceability markers in code |
| `list-ids` | List all Spaider IDs from artifacts |
| `list-id-kinds` | List ID kinds that exist in artifacts |
| `get-content` | Get content block for a specific Spaider ID |
| `where-defined` | Find where an Spaider ID is defined |
| `where-used` | Find all references to an Spaider ID |
| `adapter-info` | Discover Spaider adapter configuration |
| `init` | Initialize Spaider config and adapter |
| `agents` | Generate agent-specific workflow proxies and skill outputs |
| `self-check` | Validate examples against templates |

## Usage

```bash
# Validate all registered artifacts
python3 scripts/spaider.py validate

# Validate specific artifact
python3 scripts/spaider.py validate --artifact architecture/PRD.md

# Validate code traceability
python3 scripts/spaider.py validate-code

# List all IDs
python3 scripts/spaider.py list-ids

# Find where ID is defined
python3 scripts/spaider.py where-defined --id spd-myapp-req-auth

# Initialize project
python3 scripts/spaider.py init --yes
```

## Testing

```bash
make test
```

## Documentation

See `SKILL.md` for complete command reference and `spaider.clispec` for CLI specification.
