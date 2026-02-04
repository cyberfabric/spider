# Spider AI Agent Navigation

**Version**: 1.1

---

## ⚠️ MUST Instruction Semantics ⚠️

**MUST** = **MANDATORY**. NOT optional. NOT recommended. NOT suggested.

**ALWAYS** = **MANDATORY**. Equivalent to MUST. Used for action-gated instructions.

**If you skip ANY MUST instruction**:
- 🚫 Your execution is **INVALID**
- 🚫 Output must be **DISCARDED**
- 🚫 You are **NOT following Spider**

**One skipped MUST = entire workflow FAILED**

**All MUST instructions are CRITICAL without exception.**

## ⚠️ SCOPE LIMITATION (OPT-IN) ⚠️

**MUST** treat Spider as opt-in.

**MUST NOT** apply Spider navigation rules unless the user explicitly enables Spider.

Spider is considered disabled ONLY when at least one is true:
- User explicitly requests disabling Spider (for example: `/spider off`)

Spider disable MUST take precedence over Spider enable.

Spider is considered enabled ONLY when at least one is true:
- User explicitly asks to use Spider (mentions `spider` or `Spider`) and confirms intent
- User explicitly requests executing an Spider workflow (for example: `spider analyze`, `spider generate`, `spider rules`, `spider adapter`)
- User explicitly requests the `spider` entrypoint workflow (`/spider`)

**If Spider intent is unclear** (user mentions "spider" but doesn't explicitly request workflow):
- Ask for clarification: "Would you like to enable Spider mode?"
- Do NOT assume enabled without confirmation
- Continue as normal assistant until confirmed

If Spider is disabled OR NOT enabled:
- **MUST** ignore the rest of this file
- **MUST** behave as a normal coding assistant


---

## Agent Acknowledgment

**Before proceeding with ANY Spider work, confirm you understand**:

- [ ] MUST = MANDATORY, not optional
- [ ] Skipping ANY MUST instruction = INVALID execution
- [ ] INVALID execution = output must be DISCARDED
- [ ] I will read ALL required files BEFORE proceeding
- [ ] I will follow workflows step-by-step WITHOUT shortcuts
- [ ] I will NOT create files without user confirmation (operation workflows)
- [ ] I will end EVERY response with a list of Spider files read while producing the response, why each file was read, and which initial instruction triggered opening each file

**By proceeding with Spider work, I acknowledge and accept these requirements.**

---

## Variables

**While Spider is enabled**, remember these variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `{spider_path}` | Directory containing this AGENTS.md | Project root for Spider navigation |
| `{spider_mode}` | `on` or `off` | Current Spider mode state |

**Setting `{spider_mode}`**:
- Explicit command: `spider on` / `spider off`
- Spider prompts that activate/deactivate Spider workflows

Use `{spider_path}` as the base path for all relative Spider file references.

---

## Navigation Rules

ALWAYS open and follow `requirements/extension.md` WHEN you see **Extends**: {file}

ALWAYS open and follow `{adapter-directory}/AGENTS.md` WHEN starting any Spider work

ALWAYS open and follow `skills/spider/SKILL.md` WHEN you see `spider` in the prompt

## Skill registration

<available_skills>
  <skill>
    <name>spider</name>
    <description>Framework for Documentation and Development - AI agent toolkit. Use when user works with PRD, DESIGN, DECOMPOSITION, ADR, spec specs, architecture documentation, requirements, or mentions Spider/workflow/artifact/adapter/traceability. Provides structured artifact templates, validation, design-to-code traceability, and guided code implementation with traceability markers. Opt-in - suggest enabling when design/architecture activities detected.</description>
    <location>skills/spider/SKILL.md</location>
  </skill>
</available_skills>

### Dependency Error Handling

**If referenced file not found**:
- Log warning to user: "Spider dependency not found: {path}"
- Continue with available files — do NOT fail silently
- If critical dependency missing (SKILL.md, workflow), inform user and suggest `/spider` to reinitialize

---

## Execution Logging

ALWAYS provide execution visibility WHEN Spider is enabled.

ALWAYS notify the user WHEN entering a major section (H2 heading `##`) of any Spider prompt (workflow, rules, requirements).

ALWAYS notify the user WHEN completing a checklist task (a Markdown task line starting with `- [ ]`).

ALWAYS use this notification format WHEN emitting execution logs:

```
🕷️ [CONTEXT]: MESSAGE
```

ALWAYS set **CONTEXT** to the file or section being executed WHEN emitting execution logs (e.g., `workflows/generate.md`, `DESIGN rules`, `execution-protocol`).

ALWAYS set **MESSAGE** to what Spider is doing and why WHEN emitting execution logs.

ALWAYS ensure execution logging supports these goals WHEN Spider is enabled:
- Help the user understand which Spider prompts are being followed
- Help the user track decision points and branching logic
- Help the user debug unexpected behavior
- Help the user learn the Spider workflow

ALWAYS consider these examples as valid execution logs WHEN Spider is enabled:

```
🕷️ [execution-protocol]: Entering "Load Rules" — target is CODE, loading codebase/rules.md
🕷️ [DESIGN rules]: Completing "Validate structure" — all required sections present
🕷️ [workflows/generate.md]: Entering "Determine Target" — user requested code implementation
```