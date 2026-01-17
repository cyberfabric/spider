"""
Unit tests for CLI helper functions.

Tests utility functions from cli.py that perform parsing, filtering, and formatting.
"""

import unittest
import sys
import re
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))

from fdd.cli import (
    _parse_trace_query,
    _extract_ids,
    _filter_id_hits,
    _unique_id_hits,
    _nearest_heading_title,
    _infer_fdd_type_from_id,
    _detect_kind,
    _find_all_in_line,
    _relative_posix,
    _heading_level,
)


class TestParseTraceQuery(unittest.TestCase):
    """Test _parse_trace_query function."""

    def test_parse_simple_base(self):
        """Test parsing simple base ID."""
        base, phase, inst = _parse_trace_query("@fdd-test-flow-login")
        
        # Function strips @fdd- prefix when present
        self.assertIsNotNone(base)
        self.assertIsNone(phase)
        self.assertIsNone(inst)

    def test_parse_with_phase(self):
        """Test parsing with phase."""
        base, phase, inst = _parse_trace_query("fdd-test-flow-login:ph-1")
        
        # Extracts phase correctly
        self.assertEqual(base, "fdd-test-flow-login")
        self.assertEqual(phase, "ph-1")
        self.assertIsNone(inst)

    def test_parse_with_phase_and_instruction(self):
        """Test parsing with phase and instruction."""
        base, phase, inst = _parse_trace_query("fdd-test-flow-login:ph-1:inst-step-1")
        
        # Extracts both phase and instruction
        self.assertEqual(base, "fdd-test-flow-login")
        self.assertEqual(phase, "ph-1")
        self.assertEqual(inst, "inst-step-1")

    def test_parse_without_at_symbol(self):
        """Test parsing without @ symbol."""
        base, phase, inst = _parse_trace_query("fdd-test-flow-login:ph-1")
        
        # Without @ it treats whole thing as base
        self.assertIsNotNone(base)
        self.assertIsNone(inst)


class TestExtractIds(unittest.TestCase):
    """Test _extract_ids function."""

    def test_extract_single_id(self):
        """Test extracting single ID."""
        lines = ["Some text with `fdd-test-actor-user` in it"]
        
        ids = _extract_ids(lines)
        
        self.assertGreater(len(ids), 0)
        self.assertEqual(ids[0]["id"], "fdd-test-actor-user")

    def test_extract_multiple_ids(self):
        """Test extracting multiple IDs."""
        lines = [
            "Actor: `fdd-test-actor-user`",
            "Capability: `fdd-test-capability-login`",
        ]
        
        ids = _extract_ids(lines)
        
        self.assertGreaterEqual(len(ids), 2)

    def test_extract_with_columns(self):
        """Test extracting IDs with column numbers."""
        lines = ["Text `fdd-test-actor-user` more text"]
        
        ids = _extract_ids(lines, with_cols=True)
        
        self.assertGreater(len(ids), 0)
        self.assertIn("col", ids[0])


class TestFilterIdHits(unittest.TestCase):
    """Test _filter_id_hits function."""

    def test_filter_with_substring(self):
        """Test filtering with substring pattern."""
        hits = [
            {"id": "fdd-test-actor-user"},
            {"id": "fdd-test-actor-admin"},
            {"id": "fdd-test-capability-login"},
        ]
        
        filtered = _filter_id_hits(hits, pattern="actor", regex=False)
        
        self.assertEqual(len(filtered), 2)

    def test_filter_with_regex(self):
        """Test filtering with regex pattern."""
        hits = [
            {"id": "fdd-test-actor-user"},
            {"id": "fdd-test-actor-admin"},
            {"id": "fdd-test-capability-login"},
        ]
        
        filtered = _filter_id_hits(hits, pattern="actor-.*", regex=True)
        
        self.assertEqual(len(filtered), 2)

    def test_filter_no_pattern(self):
        """Test filtering with no pattern returns all."""
        hits = [
            {"id": "fdd-test-actor-user"},
            {"id": "fdd-test-capability-login"},
        ]
        
        filtered = _filter_id_hits(hits, pattern=None, regex=False)
        
        self.assertEqual(len(filtered), 2)


class TestUniqueIdHits(unittest.TestCase):
    """Test _unique_id_hits function."""

    def test_remove_duplicates(self):
        """Test removing duplicate IDs."""
        hits = [
            {"id": "fdd-test-actor-user", "line": 10},
            {"id": "fdd-test-actor-user", "line": 20},
            {"id": "fdd-test-capability-login", "line": 30},
        ]
        
        unique = _unique_id_hits(hits)
        
        self.assertEqual(len(unique), 2)

    def test_preserve_order(self):
        """Test preserving first occurrence order."""
        hits = [
            {"id": "fdd-test-actor-admin", "line": 10},
            {"id": "fdd-test-actor-user", "line": 20},
            {"id": "fdd-test-actor-admin", "line": 30},
        ]
        
        unique = _unique_id_hits(hits)
        
        self.assertEqual(len(unique), 2)
        self.assertEqual(unique[0]["id"], "fdd-test-actor-admin")
        self.assertEqual(unique[1]["id"], "fdd-test-actor-user")


class TestNearestHeadingTitle(unittest.TestCase):
    """Test _nearest_heading_title function."""

    def test_find_nearest_heading(self):
        """Test finding nearest heading."""
        lines = [
            "# Main Title",
            "",
            "## Section A",
            "",
            "Some content",
            "More content",
        ]
        
        title = _nearest_heading_title(lines, from_idx=5)
        
        self.assertEqual(title, "Section A")

    def test_find_parent_heading(self):
        """Test finding parent heading."""
        lines = [
            "# Main Title",
            "",
            "## Section A",
            "",
            "### Subsection",
            "Content",
        ]
        
        title = _nearest_heading_title(lines, from_idx=5)
        
        self.assertEqual(title, "Subsection")

    def test_no_heading_found(self):
        """Test when no heading is found."""
        lines = [
            "Just some text",
            "No headings here",
        ]
        
        title = _nearest_heading_title(lines, from_idx=1)
        
        self.assertIsNone(title)


class TestInferFddTypeFromId(unittest.TestCase):
    """Test _infer_fdd_type_from_id function."""

    def test_infer_actor(self):
        """Test inferring actor type."""
        fdd_type = _infer_fdd_type_from_id("fdd-test-actor-user")
        self.assertEqual(fdd_type, "actor")

    def test_infer_capability(self):
        """Test inferring capability type."""
        fdd_type = _infer_fdd_type_from_id("fdd-test-capability-login")
        self.assertEqual(fdd_type, "capability")

    def test_infer_requirement(self):
        """Test inferring requirement type."""
        fdd_type = _infer_fdd_type_from_id("fdd-test-req-001")
        self.assertEqual(fdd_type, "requirement")

    def test_infer_usecase(self):
        """Test inferring usecase type."""
        fdd_type = _infer_fdd_type_from_id("fdd-test-usecase-login")
        self.assertEqual(fdd_type, "usecase")

    def test_infer_adr(self):
        """Test inferring ADR type."""
        fdd_type = _infer_fdd_type_from_id("fdd-test-adr-0001")
        self.assertEqual(fdd_type, "adr")

    def test_infer_generic(self):
        """Test inferring generic ID type."""
        fdd_type = _infer_fdd_type_from_id("fdd-test-something-else")
        self.assertEqual(fdd_type, "id")


class TestDetectKind(unittest.TestCase):
    """Test _detect_kind function."""

    def test_detect_features_manifest(self):
        """Test detecting FEATURES.md."""
        path = Path("/test/FEATURES.md")
        kind = _detect_kind(path)
        self.assertEqual(kind, "features-manifest")

    def test_detect_feature_changes(self):
        """Test detecting feature CHANGES.md."""
        path = Path("/test/feature-test-CHANGES.md")
        kind = _detect_kind(path)
        self.assertEqual(kind, "feature-changes")

    def test_detect_design(self):
        """Test detecting DESIGN.md."""
        path = Path("/test/DESIGN.md")
        kind = _detect_kind(path)
        self.assertEqual(kind, "overall-design")

    def test_detect_changes(self):
        """Test detecting CHANGES.md."""
        path = Path("/test/CHANGES.md")
        kind = _detect_kind(path)
        self.assertEqual(kind, "feature-changes")

    def test_detect_generic(self):
        """Test detecting generic file."""
        path = Path("/test/README.md")
        kind = _detect_kind(path)
        self.assertEqual(kind, "generic")


class TestFindAllInLine(unittest.TestCase):
    """Test _find_all_in_line function."""

    def test_find_single_occurrence(self):
        """Test finding single occurrence."""
        positions = _find_all_in_line("Hello world", "world")
        
        self.assertEqual(len(positions), 1)
        self.assertEqual(positions[0], 6)

    def test_find_multiple_occurrences(self):
        """Test finding multiple occurrences."""
        positions = _find_all_in_line("test test test", "test")
        
        self.assertEqual(len(positions), 3)
        self.assertEqual(positions, [0, 5, 10])

    def test_find_no_occurrences(self):
        """Test finding no occurrences."""
        positions = _find_all_in_line("Hello world", "xyz")
        
        self.assertEqual(len(positions), 0)


class TestRelativePosix(unittest.TestCase):
    """Test _relative_posix function."""

    def test_relative_path_within_root(self):
        """Test relative path within root."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            subpath = root / "subdir" / "file.txt"
            
            rel = _relative_posix(subpath, root)
            
            self.assertEqual(rel, "subdir/file.txt")

    def test_absolute_path_outside_root(self):
        """Test absolute path when outside root."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "root"
            outside = Path(tmpdir) / "outside" / "file.txt"
            
            rel = _relative_posix(outside, root)
            
            # Should return absolute path when outside root
            self.assertIn("outside", rel)


class TestHeadingLevel(unittest.TestCase):
    """Test _heading_level function."""

    def test_level_1(self):
        """Test detecting level 1 heading."""
        level = _heading_level("# Title")
        self.assertEqual(level, 1)

    def test_level_2(self):
        """Test detecting level 2 heading."""
        level = _heading_level("## Section")
        self.assertEqual(level, 2)

    def test_level_3(self):
        """Test detecting level 3 heading."""
        level = _heading_level("### Subsection")
        self.assertEqual(level, 3)

    def test_not_heading(self):
        """Test detecting non-heading line."""
        level = _heading_level("Regular text")
        self.assertIsNone(level)

    def test_heading_with_spaces(self):
        """Test heading with extra spaces."""
        level = _heading_level("####    Title with spaces")
        self.assertEqual(level, 4)


if __name__ == "__main__":
    unittest.main()
