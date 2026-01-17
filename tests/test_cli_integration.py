# @fdd-test:fdd-fdd-feature-core-methodology-test-cli-integration:ph-1
"""
Integration tests for CLI commands.

Tests CLI entry point with various command combinations to improve coverage.
"""

import unittest
import sys
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


if __name__ == "__main__":
    unittest.main()
