"""
FDD Validator - CLI Entry Point

Command-line interface for the FDD validation tool.
"""

import sys
import os
import json
import re
import fnmatch
import argparse
from pathlib import Path
from typing import List, Optional, Dict, Set, Tuple

from .validation.artifacts import validate
from .validation.traceability import (
    validate_codebase_traceability,
    validate_code_root_traceability,
)
from .validation.fdl import validate_fdl_completion
from .utils import (
    detect_requirements,
    load_text,
    parse_required_sections,
    split_by_section_letter,
)
from .utils.files import (
    find_project_root,
    load_project_config,
    find_adapter_directory,
    load_adapter_config,
)
from .utils.document import detect_artifact_kind
from .utils.markdown import (
    extract_block,
    extract_id_block,
    extract_id_payload_block,
    find_anchor_idx_for_id,
    find_id_line,
    list_items,
    list_section_entries,
    read_change_block,
    read_feature_entry,
    read_heading_block_by_title,
    read_letter_section,
    resolve_under_heading,
)
from .utils.search import (
    list_ids,
    parse_trace_query,
    scan_ids,
    search_lines,
    where_defined_internal,
    where_used,
)
from . import constants


# =============================================================================
def _cmd_validate(argv: List[str]) -> int:
    """
    Validation command handler - wraps validate() function.
    """
    p = argparse.ArgumentParser(prog="validate")
    p.add_argument("--artifact", default=".", help="Path to artifact to validate (default: current directory = validate all)")
    p.add_argument("--requirements", default=None, help="Path to requirements file (optional, auto-detected)")
    p.add_argument("--design", default=None, help="Path to DESIGN.md for cross-references")
    p.add_argument("--business", default=None, help="Path to BUSINESS.md for cross-references")
    p.add_argument("--adr", default=None, help="Path to ADR.md for cross-references")
    p.add_argument("--skip-fs-checks", action="store_true", help="Skip filesystem checks")
    p.add_argument("--skip-code-traceability", action="store_true", help="Skip code traceability validation (only validate artifacts)")
    p.add_argument("--output", default=None, help="Write report to file instead of stdout")
    p.add_argument("--features", default=None, help="Comma-separated feature slugs for code-root traceability")
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()
    
    # Check .fdd-config.json for skip-code-traceability setting
    skip_code_traceability = args.skip_code_traceability
    config_path = artifact_path / ".fdd-config.json" if artifact_path.is_dir() else artifact_path.parent / ".fdd-config.json"
    if not skip_code_traceability and config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding="utf-8"))
            skip_code_traceability = config.get("skipCodeTraceability", False)
        except (json.JSONDecodeError, OSError):
            pass

    if artifact_path.is_dir():
        from .validation.cascade import validate_all_artifacts
        
        # Backwards-compatible: feature directory mode (artifact contains DESIGN.md).
        if (artifact_path / "DESIGN.md").exists():
            if args.features:
                raise SystemExit("--features is only supported when --artifact is a code root directory")
            if skip_code_traceability:
                # Only validate the artifact, skip code traceability
                from .validation.cascade import validate_with_dependencies
                report = validate_with_dependencies(
                    artifact_path / "DESIGN.md",
                    skip_fs_checks=bool(args.skip_fs_checks),
                )
            else:
                report = validate_codebase_traceability(
                    artifact_path,
                    feature_design_path=Path(args.design).resolve() if args.design else None,
                    feature_changes_path=None,
                    skip_fs_checks=bool(args.skip_fs_checks),
                )
            report["artifact_kind"] = "codebase-trace"
        else:
            # First validate all FDD artifacts
            artifacts_report = validate_all_artifacts(
                artifact_path,
                skip_fs_checks=bool(args.skip_fs_checks),
            )
            
            if skip_code_traceability:
                # Only artifact validation, no code traceability
                report = {
                    "status": artifacts_report.get("status", "PASS"),
                    "artifact_kind": "codebase-trace",
                    "artifact_validation": artifacts_report.get("artifact_validation", {}),
                    "code_traceability_skipped": True,
                }
            else:
                # Then validate codebase traceability
                slugs: Optional[List[str]] = None
                if args.features:
                    slugs = [x.strip() for x in str(args.features).split(",") if x.strip()]
                trace_report = validate_code_root_traceability(
                    artifact_path,
                    feature_slugs=slugs,
                    skip_fs_checks=bool(args.skip_fs_checks),
                )
                
                # Combine reports
                report = trace_report
                report["artifact_kind"] = "codebase-trace"
                report["artifact_validation"] = artifacts_report.get("artifact_validation", {})
                
                # Overall status fails if either fails
                if artifacts_report.get("status") != "PASS":
                    report["status"] = "FAIL"

        out = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            Path(args.output).write_text(out, encoding="utf-8")
        else:
            print(out, end="")

        return 0 if report["status"] == "PASS" else 2

    # If custom requirements provided, use direct validation (no cascading)
    if args.requirements:
        requirements_path = Path(args.requirements).resolve()
        if not requirements_path.exists() or not requirements_path.is_file():
            raise SystemExit(f"Requirements file not found: {requirements_path}")
        
        artifact_kind, _ = detect_requirements(artifact_path) if artifact_path.name in (
            "BUSINESS.md", "ADR.md", "FEATURES.md", "CHANGES.md", "DESIGN.md"
        ) else ("custom", None)
        
        report = validate(
            artifact_path,
            requirements_path,
            artifact_kind,
            skip_fs_checks=bool(args.skip_fs_checks),
        )
        report["artifact_kind"] = artifact_kind
    else:
        # Use core cascading validation - automatically discovers and validates all dependencies
        from .validation.cascade import validate_with_dependencies
        
        report = validate_with_dependencies(
            artifact_path,
            skip_fs_checks=bool(args.skip_fs_checks),
        )

    out = json.dumps(report, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
    else:
        print(out, end="")

    return 0 if report["status"] == "PASS" else 2


# =============================================================================
# SEARCH COMMANDS
# =============================================================================

def _cmd_list_sections(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="list-sections")
    p.add_argument("--artifact", required=True)
    p.add_argument("--under-heading", default=None)
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()
    text, err = load_text(artifact_path)
    if err:
        print(json.dumps({"status": "ERROR", "message": err}, indent=None, ensure_ascii=False))
        return 1
    lines = text.splitlines()
    kind = detect_artifact_kind(artifact_path)
    entries = list_section_entries(lines, kind=kind)
    print(json.dumps({"kind": kind, "count": len(entries), "entries": entries}, indent=None, ensure_ascii=False))
    return 0


def _cmd_list_ids(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="list-ids")
    p.add_argument("--artifact", required=True)
    p.add_argument("--under-heading", default=None)
    p.add_argument("--pattern", default=None)
    p.add_argument("--regex", action="store_true")
    p.add_argument("--all", action="store_true")
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()
    text, err = load_text(artifact_path)
    if err:
        print(json.dumps({"status": "ERROR", "message": err}, indent=None, ensure_ascii=False))
        return 1
    lines = text.splitlines()

    base_offset = 0
    if args.under_heading:
        resolved = resolve_under_heading(lines, args.under_heading)
        if resolved is None:
            print(json.dumps({"status": "NOT_FOUND", "heading": args.under_heading}, indent=None, ensure_ascii=False))
            return 1
        start, end, _ = resolved
        base_offset = start
        lines = lines[start:end]

    hits = list_ids(lines=lines, base_offset=base_offset, pattern=args.pattern, regex=bool(args.regex), all_ids=bool(args.all))
    print(json.dumps({"kind": detect_artifact_kind(artifact_path), "count": len(hits), "ids": hits}, indent=None, ensure_ascii=False))
    return 0


def _cmd_list_items(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="list-items", description="List structured items in an artifact")
    p.add_argument("--artifact", required=True)
    p.add_argument("--type", default=None, help="Filter by item type (e.g., actor, capability, requirement, flow)")
    p.add_argument("--lod", default="summary", choices=["id", "summary"], help="Level of detail")
    p.add_argument("--under-heading", default=None, help="Only search/list items inside the specified heading block")
    p.add_argument("--pattern", default=None, help="Substring filter (applied to id)")
    p.add_argument("--regex", action="store_true", help="Treat --pattern as regex")
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()
    text, err = load_text(artifact_path)
    if err:
        print(json.dumps({"status": "ERROR", "message": err}, indent=None, ensure_ascii=False))
        return 1
    lines = text.splitlines()
    kind = detect_artifact_kind(artifact_path)

    active_lines = lines
    base_offset = 0
    if args.under_heading:
        resolved = resolve_under_heading(lines, args.under_heading)
        if resolved is None:
            print(json.dumps({"status": "NOT_FOUND", "kind": kind, "heading": args.under_heading}, indent=None, ensure_ascii=False))
            return 1
        start, end, _ = resolved
        base_offset = start
        active_lines = lines[start:end]

    items = list_items(
        kind=kind,
        artifact_name=artifact_path.name,
        lines=lines,
        active_lines=active_lines,
        base_offset=base_offset,
        lod=str(args.lod),
        pattern=args.pattern,
        regex=bool(args.regex),
        type_filter=args.type,
    )
    print(json.dumps({"kind": kind, "count": len(items), "items": items}, indent=None, ensure_ascii=False))
    return 0


def _cmd_read_section(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="read-section", description="Read a section of an artifact")
    p.add_argument("--artifact", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--section", help="Top-level letter section (e.g. A, B, C)")
    g.add_argument("--heading", help="Exact heading title to match")
    g.add_argument("--feature-id", help="Feature ID for FEATURES.md entry")
    g.add_argument("--change", type=int, help="Change number for CHANGES.md")
    g.add_argument("--id", help="Any ID to locate, then return its block")
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()
    text, err = load_text(artifact_path)
    if err:
        print(json.dumps({"status": "ERROR", "message": err}, indent=None, ensure_ascii=False))
        return 1
    lines = text.splitlines()
    kind = detect_artifact_kind(artifact_path)

    if args.id is not None:
        return _cmd_find_id(["--artifact", str(artifact_path), "--id", args.id])

    if args.feature_id is not None:
        if kind != "features-manifest":
            print(json.dumps({"status": "ERROR", "message": "--feature-id is only supported for FEATURES.md"}, indent=None, ensure_ascii=False))
            return 1
        rng = read_feature_entry(lines, args.feature_id)
        if rng is None:
            print(json.dumps({"status": "NOT_FOUND", "feature_id": args.feature_id}, indent=None, ensure_ascii=False))
            return 1
        start, end = rng
        print(json.dumps({"status": "FOUND", "feature_id": args.feature_id, "text": "\n".join(lines[start:end])}, indent=None, ensure_ascii=False))
        return 0

    if args.change is not None:
        if kind != "feature-changes":
            print(json.dumps({"status": "ERROR", "message": "--change is only supported for CHANGES.md"}, indent=None, ensure_ascii=False))
            return 1
        rng = read_change_block(lines, int(args.change))
        if rng is None:
            print(json.dumps({"status": "NOT_FOUND", "change": args.change}, indent=None, ensure_ascii=False))
            return 1
        start_idx, end = rng
        print(json.dumps({"status": "FOUND", "change": args.change, "text": "\n".join(lines[start_idx:end])}, indent=None, ensure_ascii=False))
        return 0

    if args.section is not None:
        letter = args.section.strip().upper()
        rng = read_letter_section(lines, letter)
        if rng is None:
            print(json.dumps({"status": "NOT_FOUND", "section": letter}, indent=None, ensure_ascii=False))
            return 1
        start_idx, end = rng
        print(json.dumps({"status": "FOUND", "section": letter, "text": "\n".join(lines[start_idx:end])}, indent=None, ensure_ascii=False))
        return 0

    if args.heading is not None:
        title = args.heading.strip()
        rng = read_heading_block_by_title(lines, title)
        if rng is None:
            print(json.dumps({"status": "NOT_FOUND", "heading": title}, indent=None, ensure_ascii=False))
            return 1
        start, end = rng
        print(json.dumps({"status": "FOUND", "heading": title, "text": "\n".join(lines[start:end])}, indent=None, ensure_ascii=False))
        return 0

    print(json.dumps({"status": "ERROR", "message": "No selector provided"}, indent=None, ensure_ascii=False))
    return 1


def _cmd_get_item(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="get-item", description="Get a structured block by id/heading/section/feature/change")
    p.add_argument("--artifact", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--section")
    g.add_argument("--heading")
    g.add_argument("--feature-id")
    g.add_argument("--change", type=int)
    g.add_argument("--id")
    args = p.parse_args(argv)

    if args.id is not None:
        return _cmd_find_id(["--artifact", args.artifact, "--id", args.id])

    sub: List[str] = ["--artifact", args.artifact]
    if args.section is not None:
        sub.extend(["--section", args.section])
    elif args.heading is not None:
        sub.extend(["--heading", args.heading])
    elif args.feature_id is not None:
        sub.extend(["--feature-id", args.feature_id])
    elif args.change is not None:
        sub.extend(["--change", str(args.change)])

    return _cmd_read_section(sub)


def _cmd_find_id(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="find-id")
    p.add_argument("--artifact", required=True)
    p.add_argument("--id", required=True)
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()
    text, err = load_text(artifact_path)
    if err:
        print(json.dumps({"status": "ERROR", "message": err}, indent=None, ensure_ascii=False))
        return 1
    lines = text.splitlines()

    kind = detect_artifact_kind(artifact_path)

    idx = find_id_line(lines, args.id)
    if idx is None:
        print(json.dumps({"status": "NOT_FOUND", "id": args.id}, indent=None, ensure_ascii=False))
        return 1

    anchor = find_anchor_idx_for_id(lines, args.id) or idx
    start, end = extract_id_block(lines, anchor_idx=anchor, id_value=args.id, kind=kind)
    payload = extract_id_payload_block(lines, id_idx=idx)
    payload_out: Optional[Dict[str, object]] = None
    if payload is not None:
        payload_out = {
            "open_line": int(payload["open_idx"]) + 1,
            "close_line": int(payload["close_idx"]) + 1,
            "text": str(payload["text"]),
        }
    print(json.dumps({
        "status": "FOUND",
        "id": args.id,
        "line": idx + 1,
        "payload": payload_out,
        "block_start_line": start + 1,
        "block_end_line": end,
        "text": "\n".join(lines[start:end]),
    }, indent=None, ensure_ascii=False))
    return 0


def _cmd_search(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="search")
    p.add_argument("--artifact", required=True)
    p.add_argument("--query", required=True)
    p.add_argument("--regex", action="store_true")
    args = p.parse_args(argv)

    artifact_path = Path(args.artifact).resolve()
    text, err = load_text(artifact_path)
    if err:
        print(json.dumps({"status": "ERROR", "message": err}, indent=None, ensure_ascii=False))
        return 1
    lines = text.splitlines()

    hits = search_lines(lines=lines, query=str(args.query), regex=bool(args.regex))
    print(json.dumps({"count": len(hits), "hits": hits}, indent=None, ensure_ascii=False))
    return 0


def _cmd_scan_ids(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="scan-ids")
    p.add_argument("--root", required=True)
    p.add_argument("--pattern", default=None)
    p.add_argument("--regex", action="store_true")
    p.add_argument("--kind", default="all", choices=["all", "fdd", "adr"])
    p.add_argument("--all", action="store_true")
    p.add_argument("--include", action="append", default=None)
    p.add_argument("--exclude", action="append", default=None)
    p.add_argument("--max-bytes", type=int, default=1_000_000)
    args = p.parse_args(argv)

    root = Path(args.root).resolve()
    hits = scan_ids(
        root=root,
        pattern=args.pattern,
        regex=bool(args.regex),
        kind=str(args.kind),
        include=args.include,
        exclude=args.exclude,
        max_bytes=int(args.max_bytes),
        all_ids=bool(args.all),
    )
    print(json.dumps({"root": root.as_posix(), "count": len(hits), "ids": hits}, indent=None, ensure_ascii=False))
    return 0


def _cmd_where_defined(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="where-defined", description="Find where an ID is defined")
    p.add_argument("--id", required=True)
    p.add_argument("--root", default=".", help="Root directory to search (default: current working directory)")
    p.add_argument("--include-tags", action="store_true", help="Also treat @fdd-* code tags as definitions")
    p.add_argument("--include", action="append", default=None, help="Glob include filter over relative paths (repeatable)")
    p.add_argument("--exclude", action="append", default=None, help="Glob exclude filter over relative paths (repeatable)")
    p.add_argument("--max-bytes", type=int, default=1_000_000, help="Skip files larger than this size")
    args = p.parse_args(argv)

    raw_id = str(args.id).strip()
    base, phase, inst = parse_trace_query(raw_id)
    root = Path(args.root).resolve()

    _base2, defs, ctx_defs = where_defined_internal(
        root=root,
        raw_id=raw_id,
        include_tags=bool(args.include_tags),
        includes=args.include,
        excludes=args.exclude,
        max_bytes=int(args.max_bytes),
    )

    _ = _base2

    if not defs:
        print(json.dumps(
            {
                "status": "NOT_FOUND",
                "id": raw_id,
                "base_id": base,
                "phase": phase,
                "inst": inst,
                "root": root.as_posix(),
                "count": 0,
                "definitions": [],
                "context_definitions": ctx_defs,
            },
            indent=None,
            ensure_ascii=False,
        ))
        return 1
    status = "FOUND" if len(defs) == 1 else "AMBIGUOUS"
    print(json.dumps(
        {
            "status": status,
            "id": raw_id,
            "base_id": base,
            "phase": phase,
            "inst": inst,
            "root": root.as_posix(),
            "count": len(defs),
            "definitions": defs,
            "context_definitions": ctx_defs,
        },
        indent=None,
        ensure_ascii=False,
    ))
    return 0 if status == "FOUND" else 2


def _cmd_where_used(argv: List[str]) -> int:
    p = argparse.ArgumentParser(prog="where-used", description="Find where an ID is referenced across a repository")
    p.add_argument("--id", required=True)
    p.add_argument("--root", default=".", help="Root directory to search (default: current working directory)")
    p.add_argument("--include", action="append", default=None, help="Glob include filter over relative paths (repeatable)")
    p.add_argument("--exclude", action="append", default=None, help="Glob exclude filter over relative paths (repeatable)")
    p.add_argument("--max-bytes", type=int, default=1_000_000, help="Skip files larger than this size")
    args = p.parse_args(argv)

    raw_id = str(args.id).strip()
    root = Path(args.root).resolve()

    base, phase, inst, hits = where_used(
        root=root,
        raw_id=raw_id,
        include=args.include,
        exclude=args.exclude,
        max_bytes=int(args.max_bytes),
    )
    print(json.dumps({"id": raw_id, "base_id": base, "phase": phase, "inst": inst, "root": root.as_posix(), "count": len(hits), "hits": hits}, indent=None, ensure_ascii=False))
    return 0


# =============================================================================
# ADAPTER COMMAND
# =============================================================================

def _cmd_adapter_info(argv: List[str]) -> int:
    """
    Discover and display FDD adapter information.
    Shows adapter location, project name, and available specs.
    """
    p = argparse.ArgumentParser(prog="adapter-info", description="Discover FDD adapter configuration")
    p.add_argument("--root", default=".", help="Project root to search from (default: current directory)")
    p.add_argument("--fdd-root", default=None, help="FDD core location (if agent knows it)")
    args = p.parse_args(argv)
    
    start_path = Path(args.root).resolve()
    fdd_root_path = Path(args.fdd_root).resolve() if args.fdd_root else None
    
    # Find project root
    project_root = find_project_root(start_path)
    if project_root is None:
        print(json.dumps(
            {
                "status": "NOT_FOUND",
                "message": "No project root found (no .git or .fdd-config.json)",
                "searched_from": start_path.as_posix(),
                "hint": "Create .fdd-config.json in project root to configure FDD",
            },
            indent=2,
            ensure_ascii=False,
        ))
        return 1
    
    # Find adapter
    adapter_dir = find_adapter_directory(start_path, fdd_root=fdd_root_path)
    if adapter_dir is None:
        # Check if config exists to provide better error message
        cfg = load_project_config(project_root)
        if cfg is not None:
            adapter_rel = cfg.get("fddAdapterPath")
            if adapter_rel is not None and isinstance(adapter_rel, str):
                # Config exists but path is invalid
                print(json.dumps(
                    {
                        "status": "CONFIG_ERROR",
                        "message": f"Config specifies adapter path but directory not found or invalid",
                        "project_root": project_root.as_posix(),
                        "config_path": adapter_rel,
                        "expected_location": (project_root / adapter_rel).as_posix(),
                        "hint": "Check .fdd-config.json fddAdapterPath points to valid directory with AGENTS.md",
                    },
                    indent=2,
                    ensure_ascii=False,
                ))
                return 1
        
        # No config, no adapter found via recursive search
        print(json.dumps(
            {
                "status": "NOT_FOUND",
                "message": "No FDD-Adapter found in project (searched recursively up to 5 levels deep)",
                "project_root": project_root.as_posix(),
                "hint": "Create .fdd-config.json with fddAdapterPath or run adapter-bootstrap workflow",
            },
            indent=2,
            ensure_ascii=False,
        ))
        return 1
    
    # Load adapter config
    config = load_adapter_config(adapter_dir)
    config["status"] = "FOUND"
    config["project_root"] = project_root.as_posix()
    
    # Calculate relative path
    try:
        relative_path = adapter_dir.relative_to(project_root).as_posix()
    except ValueError:
        relative_path = adapter_dir.as_posix()
    config["relative_path"] = relative_path
    
    # Check if .fdd-config.json exists
    config_file = project_root / ".fdd-config.json"
    config["has_config"] = config_file.exists()
    if not config_file.exists():
        config["config_hint"] = f"Create .fdd-config.json with: {{\"fddAdapterPath\": \"{relative_path}\"}}"
    
    print(json.dumps(config, indent=2, ensure_ascii=False))
    return 0


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main(argv: Optional[List[str]] = None) -> int:
    argv_list = list(argv) if argv is not None else sys.argv[1:]
    
    # Define all available commands
    validation_commands = ["validate"]
    search_commands = [
        "list-sections", "list-ids", "list-items",
        "read-section", "get-item", "find-id",
        "search", "scan-ids",
        "where-defined", "where-used",
        "adapter-info",
    ]
    all_commands = validation_commands + search_commands

    if not argv_list:
        print(json.dumps({
            "status": "ERROR",
            "message": "Missing subcommand",
            "validation_commands": validation_commands,
            "search_commands": search_commands,
        }, indent=None, ensure_ascii=False))
        return 1

    # Backward compatibility: if first arg starts with --, assume validate command
    if argv_list[0].startswith("-"):
        cmd = "validate"
        rest = argv_list
    else:
        cmd = argv_list[0]
        rest = argv_list[1:]

    # Dispatch to appropriate command handler
    if cmd == "validate":
        return _cmd_validate(rest)
    elif cmd == "list-sections":
        return _cmd_list_sections(rest)
    elif cmd == "list-ids":
        return _cmd_list_ids(rest)
    elif cmd == "list-items":
        return _cmd_list_items(rest)
    elif cmd == "read-section":
        return _cmd_read_section(rest)
    elif cmd == "get-item":
        return _cmd_get_item(rest)
    elif cmd == "find-id":
        return _cmd_find_id(rest)
    elif cmd == "search":
        return _cmd_search(rest)
    elif cmd == "scan-ids":
        return _cmd_scan_ids(rest)
    elif cmd == "where-defined":
        return _cmd_where_defined(rest)
    elif cmd == "where-used":
        return _cmd_where_used(rest)
    elif cmd == "adapter-info":
        return _cmd_adapter_info(rest)
    else:
        print(json.dumps({
            "status": "ERROR",
            "message": f"Unknown command: {cmd}",
            "available": all_commands,
        }, indent=None, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["main"]
