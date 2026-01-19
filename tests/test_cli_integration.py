# @fdd-test:fdd-fdd-feature-core-methodology-test-cli-integration:ph-1
"""
Integration tests for CLI commands.

Tests CLI entry point with various command combinations to improve coverage.
"""

import unittest
import sys
import os
import json
import io
from pathlib import Path
from tempfile import TemporaryDirectory
from contextlib import redirect_stdout, redirect_stderr

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))

from fdd.cli import main


class TestCLIValidateCommand(unittest.TestCase):
    """Test validate command variations."""

    def test_validate_missing_artifact_argument(self):
        """Test validate command without --artifact argument."""
        stdout = io.StringIO()
        stderr = io.StringIO()
        
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(["validate"])
                self.assertNotEqual(exit_code, 0)
            except SystemExit as e:
                # argparse calls sys.exit on error
                self.assertNotEqual(e.code, 0)

    def test_validate_nonexistent_artifact(self):
        """Test validate command with non-existent artifact."""
        with TemporaryDirectory() as tmpdir:
            # Use valid artifact name
            fake_path = Path(tmpdir) / "DESIGN.md"
            
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                try:
                    exit_code = main(["validate", "--artifact", str(fake_path)])
                    # Should fail with file not found
                    self.assertNotEqual(exit_code, 0)
                    output = stdout.getvalue()
                    self.assertIn("ERROR", output.upper())
                except FileNotFoundError:
                    # Also acceptable - file doesn't exist
                    pass

    def test_validate_dir_with_design_and_features_flag_fails(self):
        """When --artifact is a feature dir containing DESIGN.md, --features must error."""
        with TemporaryDirectory() as tmpdir:
            feat = Path(tmpdir)
            (feat / "DESIGN.md").write_text("# Feature: X\n", encoding="utf-8")

            with self.assertRaises(SystemExit):
                main(["validate", "--artifact", str(feat), "--features", "feature-x"]) 

    def test_validate_dir_without_design_uses_code_root_traceability(self):
        """Cover validate branch when --artifact is a directory without DESIGN.md."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / ".git").mkdir()

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["validate", "--artifact", str(root)])

            self.assertIn(exit_code, (0, 1, 2))
            out = json.loads(stdout.getvalue())
            self.assertIn("status", out)

    def test_validate_code_root_with_features_parsing(self):
        """Cover --features parsing when validating a code root directory."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / ".git").mkdir()
            (root / "architecture" / "features" / "feature-a").mkdir(parents=True)
            (root / "architecture" / "features" / "feature-b").mkdir(parents=True)

            # Minimal artifacts for feature-a/feature-b so traceability runs.
            (root / "architecture" / "features" / "feature-a" / "DESIGN.md").write_text("# Feature: A\n", encoding="utf-8")
            (root / "architecture" / "features" / "feature-a" / "CHANGES.md").write_text("# Implementation Plan: A\n", encoding="utf-8")
            (root / "architecture" / "features" / "feature-b" / "DESIGN.md").write_text("# Feature: B\n", encoding="utf-8")
            (root / "architecture" / "features" / "feature-b" / "CHANGES.md").write_text("# Implementation Plan: B\n", encoding="utf-8")

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["validate", "--artifact", str(root), "--features", "feature-a, b, ,feature-b", "--skip-fs-checks"])

            self.assertIn(exit_code, (0, 2))
            out = json.loads(stdout.getvalue())
            self.assertIn("status", out)

    def test_validate_requires_requirements_file_exists(self):
        """Cover SystemExit when requirements file path does not exist."""
        with TemporaryDirectory() as tmpdir:
            art = Path(tmpdir) / "DESIGN.md"
            art.write_text("# Technical Design\n\n## A. X\n", encoding="utf-8")
            missing_req = Path(tmpdir) / "missing-req.md"

            with self.assertRaises(SystemExit):
                main(["validate", "--artifact", str(art), "--requirements", str(missing_req)])

    def test_validate_writes_output_file(self):
        """Cover --output branch (writes JSON report to file)."""
        with TemporaryDirectory() as tmpdir:
            td = Path(tmpdir)
            art = td / "DESIGN.md"
            art.write_text("# Technical Design\n\n## A. X\n", encoding="utf-8")
            req = td / "req.md"
            req.write_text("### Section A: a\n", encoding="utf-8")

            out_path = td / "out.json"
            exit_code = main(["validate", "--artifact", str(art), "--requirements", str(req), "--output", str(out_path)])
            self.assertIn(exit_code, (0, 2))
            self.assertTrue(out_path.exists())

    def test_validate_dir_mode_writes_output_file(self):
        """Cover --output branch when --artifact is a directory."""
        with TemporaryDirectory() as tmpdir:
            td = Path(tmpdir)
            (td / ".git").mkdir()
            (td / "architecture" / "features" / "feature-a").mkdir(parents=True)
            (td / "architecture" / "features" / "feature-a" / "DESIGN.md").write_text("# Feature: A\n", encoding="utf-8")
            (td / "architecture" / "features" / "feature-a" / "CHANGES.md").write_text("# Implementation Plan: A\n", encoding="utf-8")

            out_path = td / "out.json"
            exit_code = main(["validate", "--artifact", str(td), "--output", str(out_path), "--skip-fs-checks"])
            self.assertIn(exit_code, (0, 2))
            self.assertTrue(out_path.exists())

    def test_validate_feature_dir_with_design_md_runs_codebase_traceability(self):
        """Cover validate branch when --artifact is a feature directory containing DESIGN.md."""
        with TemporaryDirectory() as tmpdir:
            feat = Path(tmpdir) / "architecture" / "features" / "feature-x"
            feat.mkdir(parents=True)
            (feat / "DESIGN.md").write_text("# Feature: X\n", encoding="utf-8")

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["validate", "--artifact", str(feat), "--skip-fs-checks"])
            self.assertIn(exit_code, (0, 2))
            out = json.loads(stdout.getvalue())
            self.assertIn("artifact_kind", out)


class TestCLISearchCommands(unittest.TestCase):
    """Test search command variations."""

    def test_list_sections_basic(self):
        """Test list-sections command."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("""# Document

## A. First Section

Content

## B. Second Section

More content
""")
            
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["list-sections", "--artifact", str(doc)])
            
            self.assertEqual(exit_code, 0)
            output = json.loads(stdout.getvalue())
            self.assertIn("entries", output)
            self.assertGreater(len(output["entries"]), 0)

    def test_list_ids_basic(self):
        """Test list-ids command."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("""# Document

**ID**: `fdd-test-actor-user`

**ID**: `fdd-test-capability-login`
""")
            
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["list-ids", "--artifact", str(doc)])
            
            self.assertEqual(exit_code, 0)
            output = json.loads(stdout.getvalue())
            self.assertIn("ids", output)
            self.assertEqual(len(output["ids"]), 2)

    def test_list_ids_missing_file_errors(self):
        """Cover list-ids load_text error branch."""
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = main(["list-ids", "--artifact", "/tmp/does-not-exist.md"])
        self.assertEqual(exit_code, 1)

    def test_list_ids_with_pattern(self):
        """Test list-ids with pattern filter."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("""# Document

**ID**: `fdd-test-actor-user`
**ID**: `fdd-test-actor-admin`
**ID**: `fdd-test-capability-login`
""")
            
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                # Use = form for pattern starting with dash
                exit_code = main(["list-ids", "--artifact", str(doc), "--pattern=-actor-"])
            
            self.assertEqual(exit_code, 0)
            output = json.loads(stdout.getvalue())
            self.assertEqual(len(output["ids"]), 2)

    def test_search_literal(self):
        """Test search command with literal query."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("""# Document

This is a test document.

Test appears twice in this test.
""")
            
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["search", "--artifact", str(doc), "--query", "test"])
            
            self.assertEqual(exit_code, 0)
            output = json.loads(stdout.getvalue())
            self.assertIn("hits", output)
            self.assertGreater(len(output["hits"]), 0)

    def test_search_regex(self):
        """Test search command with regex query."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("""# Document

test123
test456
other
""")
            
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["search", "--artifact", str(doc), "--query", r"test\d+", "--regex"])
            
            self.assertEqual(exit_code, 0)
            output = json.loads(stdout.getvalue())
            self.assertEqual(len(output["hits"]), 2)

    def test_where_used_with_regex_query_components(self):
        """Cover where-used parsing for trace query with phase/inst."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            doc = tmppath / "doc.md"
            doc.write_text("x fdd-test-req-auth:ph-1:inst-step\n", encoding="utf-8")

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["where-used", "--root", str(tmppath), "--id", "fdd-test-req-auth:ph-1:inst-step"])

            self.assertEqual(exit_code, 0)
            output = json.loads(stdout.getvalue())
            self.assertEqual(output.get("phase"), "ph-1")
            self.assertEqual(output.get("inst"), "inst-step")

    def test_list_sections_missing_file_errors(self):
        """Cover error path when artifact file can't be loaded."""
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = main(["list-sections", "--artifact", "/tmp/does-not-exist.md"])
        self.assertEqual(exit_code, 1)

    def test_list_ids_under_heading_not_found(self):
        """Cover NOT_FOUND branch for --under-heading."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("# Doc\n\n## A\n\n**ID**: `fdd-test-actor-user`\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["list-ids", "--artifact", str(doc), "--under-heading", "Missing"])
            self.assertEqual(exit_code, 1)

    def test_list_ids_under_heading_found(self):
        """Cover FOUND branch for --under-heading with base_offset adjustment."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text(
                "\n".join(
                    [
                        "# Doc",
                        "",
                        "## A",
                        "",
                        "**ID**: `fdd-test-actor-user`",
                        "",
                        "## B",
                        "",
                        "**ID**: `fdd-test-actor-admin`",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["list-ids", "--artifact", str(doc), "--under-heading", "A"])
            self.assertEqual(exit_code, 0)
            out = json.loads(stdout.getvalue())
            self.assertEqual(out.get("count"), 1)
            self.assertEqual(out.get("ids")[0].get("id"), "fdd-test-actor-user")

    def test_read_section_change_wrong_kind(self):
        """Cover --change only valid for CHANGES.md."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("# Doc\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["read-section", "--artifact", str(doc), "--change", "1"])
            self.assertEqual(exit_code, 1)

    def test_read_section_section_not_found(self):
        """Cover NOT_FOUND for --section."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("# Doc\n\n## A. A\n\nX\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["read-section", "--artifact", str(doc), "--section", "B"])
            self.assertEqual(exit_code, 1)
            out = json.loads(stdout.getvalue())
            self.assertEqual(out.get("status"), "NOT_FOUND")

    def test_get_item_delegates_to_read_section(self):
        """Cover get-item delegating to read-section."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("# Doc\n\n## A. A\n\nX\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["get-item", "--artifact", str(doc), "--section", "A"])
            self.assertEqual(exit_code, 0)
            out = json.loads(stdout.getvalue())
            self.assertEqual(out.get("status"), "FOUND")

    def test_list_items_under_heading_not_found(self):
        """Cover NOT_FOUND branch for list-items --under-heading."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("# Doc\n\n## A\n\n**ID**: `fdd-test-actor-user`\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["list-items", "--artifact", str(doc), "--under-heading", "Missing"])
            self.assertEqual(exit_code, 1)
            out = json.loads(stdout.getvalue())
            self.assertEqual(out["status"], "NOT_FOUND")

    def test_list_items_under_heading_found(self):
        """Cover list-items --under-heading FOUND path."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "BUSINESS.md"
            doc.write_text(
                "\n".join(
                    [
                        "# Business Context",
                        "",
                        "## B. Actors",
                        "",
                        "#### Admin",
                        "**ID**: `fdd-test-actor-admin`",
                        "**Role**: Admin",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["list-items", "--artifact", str(doc), "--under-heading", "B. Actors", "--lod", "id"])
            self.assertEqual(exit_code, 0)
            out = json.loads(stdout.getvalue())
            self.assertEqual(out.get("count"), 1)
            self.assertEqual(out.get("items")[0].get("id"), "fdd-test-actor-admin")


class TestCLITraceabilityCommands(unittest.TestCase):
    """Test traceability command variations."""

    def test_scan_ids_basic(self):
        """Test scan-ids command."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create test file with IDs
            doc = tmppath / "doc.md"
            doc.write_text("**ID**: `fdd-test-actor-user`\n")
            
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["scan-ids", "--root", str(tmppath)])
            
            self.assertEqual(exit_code, 0)
            output = json.loads(stdout.getvalue())
            self.assertIn("ids", output)
            self.assertGreater(len(output["ids"]), 0)

    def test_scan_ids_with_kind_filter(self):
        """Test scan-ids with kind filter."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            doc = tmppath / "doc.md"
            doc.write_text("""
**ID**: `fdd-test-actor-user`
**ID**: `ADR-0001`
""")
            
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["scan-ids", "--root", str(tmppath), "--kind", "fdd"])
            
            self.assertEqual(exit_code, 0)
            output = json.loads(stdout.getvalue())
            # Should only find FDD IDs, not ADR
            fdd_ids = [id_obj["id"] for id_obj in output["ids"]]
            self.assertIn("fdd-test-actor-user", fdd_ids)
            self.assertNotIn("ADR-0001", fdd_ids)

    def test_where_used_basic(self):
        """Test where-used command."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            
            # Create file with ID usage
            doc = tmppath / "doc.md"
            doc.write_text("""
Reference to fdd-test-req-auth in doc.

Another reference to fdd-test-req-auth here.
""")
            
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["where-used", "--root", str(tmppath), "--id", "fdd-test-req-auth"])
            
            self.assertEqual(exit_code, 0)
            output = json.loads(stdout.getvalue())
            self.assertIn("hits", output)
            self.assertEqual(len(output["hits"]), 2)

    def test_where_defined_and_where_used_with_definition_filtering(self):
        """Cover where-defined FOUND and where-used filtering out definition lines."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "architecture").mkdir(parents=True)

            # Definition file
            design = root / "architecture" / "DESIGN.md"
            design.write_text(
                "\n".join(
                    [
                        "# Design",
                        "## A. x",
                        "## B. Requirements",
                        "- [ ] **ID**: `fdd-test-req-auth`",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            # Usage file
            use = root / "notes.md"
            use.write_text("ref fdd-test-req-auth\n", encoding="utf-8")

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["where-defined", "--root", str(root), "--id", "fdd-test-req-auth"])
            self.assertIn(exit_code, (0, 2))
            out = json.loads(stdout.getvalue())
            self.assertIn(out["status"], ("FOUND", "AMBIGUOUS"))

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["where-used", "--root", str(root), "--id", "fdd-test-req-auth"])
            self.assertEqual(exit_code, 0)
            out = json.loads(stdout.getvalue())
            # Should not count the definition line in DESIGN.md as usage
            self.assertGreaterEqual(len(out.get("hits", [])), 1)

    def test_where_defined_not_found(self):
        """Cover where-defined NOT_FOUND branch."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "architecture").mkdir(parents=True)
            (root / "architecture" / "DESIGN.md").write_text("# Design\n", encoding="utf-8")

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["where-defined", "--root", str(root), "--id", "fdd-missing-id"])

            self.assertIn(exit_code, (1, 2))
            out = json.loads(stdout.getvalue())
            self.assertEqual(out.get("status"), "NOT_FOUND")


class TestCLIErrorHandling(unittest.TestCase):
    """Test CLI error handling."""

    def test_unknown_command(self):
        """Test CLI with unknown command."""
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = main(["unknown-command"])
        
        self.assertNotEqual(exit_code, 0)
        output = json.loads(stdout.getvalue())
        self.assertEqual(output["status"], "ERROR")
        self.assertIn("Unknown command", output["message"])

    def test_missing_required_option(self):
        """Test CLI command with missing required option."""
        stdout = io.StringIO()
        stderr = io.StringIO()
        
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exit_code = main(["search", "--artifact", "/tmp/test.md"])
                # Missing --query
                self.assertNotEqual(exit_code, 0)
            except SystemExit as e:
                # argparse calls sys.exit on missing required arg
                self.assertNotEqual(e.code, 0)

    def test_empty_command(self):
        """Test CLI with no command."""
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = main([])
        
        self.assertNotEqual(exit_code, 0)
        output = json.loads(stdout.getvalue())
        self.assertEqual(output["status"], "ERROR")
        self.assertIn("Missing subcommand", output["message"])

    def test_read_section_feature_id_wrong_kind(self):
        """Cover --feature-id only valid for FEATURES.md."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("# Doc\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["read-section", "--artifact", str(doc), "--feature-id", "fdd-x-feature-y"])
            self.assertEqual(exit_code, 1)

    def test_read_section_heading_not_found(self):
        """Cover NOT_FOUND for --heading."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("# Doc\n\n## A. A\n\nX\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["read-section", "--artifact", str(doc), "--heading", "Missing"])
            self.assertEqual(exit_code, 1)

    def test_find_id_not_found(self):
        """Cover NOT_FOUND for find-id."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("# Doc\n\n**ID**: `fdd-test-actor-user`\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["find-id", "--artifact", str(doc), "--id", "fdd-missing"])
            self.assertEqual(exit_code, 1)

    def test_find_id_found(self):
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("# Doc\n\n**ID**: `fdd-test-actor-user`\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["find-id", "--artifact", str(doc), "--id", "fdd-test-actor-user"])
            self.assertEqual(exit_code, 0)
            out = json.loads(stdout.getvalue())
            self.assertEqual(out.get("status"), "FOUND")
            self.assertIn("payload", out)
            self.assertIsNone(out.get("payload"))

    def test_find_id_found_with_payload(self):
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text(
                "\n".join(
                    [
                        "# Doc",
                        "",
                        "**ID**: `fdd-test-actor-user`",
                        "",
                        "---",
                        "payload-line",
                        "---",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["find-id", "--artifact", str(doc), "--id", "fdd-test-actor-user"])
            self.assertEqual(exit_code, 0)
            out = json.loads(stdout.getvalue())
            self.assertEqual(out.get("status"), "FOUND")
            payload = out.get("payload")
            self.assertIsInstance(payload, dict)
            self.assertEqual(payload.get("open_line"), 5)
            self.assertEqual(payload.get("close_line"), 7)
            self.assertEqual(payload.get("text"), "payload-line")

    def test_read_section_id_delegates_to_find_id(self):
        """Cover read-section --id delegation."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("# Doc\n\n**ID**: `fdd-test-actor-user`\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["read-section", "--artifact", str(doc), "--id", "fdd-test-actor-user"])
            self.assertEqual(exit_code, 0)
            out = json.loads(stdout.getvalue())
            self.assertEqual(out.get("status"), "FOUND")

    def test_get_item_id_delegates_to_find_id(self):
        """Cover get-item --id delegation."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "doc.md"
            doc.write_text("# Doc\n\n**ID**: `fdd-test-actor-user`\n", encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["get-item", "--artifact", str(doc), "--id", "fdd-test-actor-user"])
            self.assertEqual(exit_code, 0)
            out = json.loads(stdout.getvalue())
            self.assertEqual(out.get("status"), "FOUND")


class TestCLIBackwardCompatibility(unittest.TestCase):
    """Test CLI backward compatibility features."""

    def test_validate_without_subcommand(self):
        """Test that --artifact without subcommand defaults to validate."""
        with TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "DESIGN.md"
            doc.write_text("""# Technical Design

## A. Architecture Overview

Content

## B. Requirements

Content

## C. Domain Model

Content
""")
            
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                # Old style: no subcommand, just --artifact
                exit_code = main(["--artifact", str(doc)])
            
            # Should work (backward compat)
            output = json.loads(stdout.getvalue())
            self.assertIn("status", output)


class TestCLIAdapterInfo(unittest.TestCase):
    def test_adapter_info_basic(self):
        """Cover adapter-info command."""
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = main(["adapter-info"])
        self.assertEqual(exit_code, 0)
        out = json.loads(stdout.getvalue())
        self.assertIn("status", out)

    def test_adapter_info_config_error_when_path_invalid(self):
        """Cover adapter-info CONFIG_ERROR when .fdd-config.json points to missing adapter directory."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / ".git").mkdir()
            (root / ".fdd-config.json").write_text('{"fddAdapterPath": "missing-adapter"}', encoding="utf-8")

            cwd = os.getcwd()
            try:
                os.chdir(str(root))
                stdout = io.StringIO()
                with redirect_stdout(stdout):
                    exit_code = main(["adapter-info"])
                self.assertEqual(exit_code, 1)
                out = json.loads(stdout.getvalue())
                self.assertEqual(out.get("status"), "CONFIG_ERROR")
            finally:
                os.chdir(cwd)

    def test_adapter_info_relative_path_outside_project_root(self):
        """Cover adapter-info relative_to() ValueError branch when adapter is outside project root."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "project"
            root.mkdir(parents=True)
            (root / ".git").mkdir()

            outside = Path(tmpdir) / "outside-adapter"
            outside.mkdir(parents=True)
            (outside / "AGENTS.md").write_text("# FDD Adapter: Outside\n\n**Extends**: `../AGENTS.md`\n", encoding="utf-8")

            # Point config path outside the project.
            (root / ".fdd-config.json").write_text('{"fddAdapterPath": "../outside-adapter"}', encoding="utf-8")

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["adapter-info", "--root", str(root)])

            self.assertEqual(exit_code, 0)
            out = json.loads(stdout.getvalue())
            self.assertEqual(out.get("status"), "FOUND")
            self.assertEqual(out.get("relative_path"), str(outside.resolve().as_posix()))


if __name__ == "__main__":
    unittest.main()
