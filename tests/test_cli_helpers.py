"""
Unit tests for CLI helper functions.

Tests utility functions from fdd.utils.search, fdd.utils.markdown, and fdd.utils.document that perform parsing, filtering, and formatting.
"""

import unittest
import sys
import re
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))

from fdd.utils.document import detect_artifact_kind, iter_text_files, read_text_safe, to_relative_posix
from fdd.utils.markdown import find_nearest_heading, get_heading_level
from fdd.utils.search import (
    extract_ids,
    filter_hits,
    find_all_positions,
    infer_fdd_type,
    parse_trace_query,
    unique_hits,
)


class TestParseTraceQuery(unittest.TestCase):
    """Test parse_trace_query function."""

    def test_parse_simple_base(self):
        """Test parsing simple base ID."""
        base, phase, inst = parse_trace_query("@fdd-test-flow-login")
        
        # Function strips @fdd- prefix when present
        self.assertIsNotNone(base)
        self.assertIsNone(phase)
        self.assertIsNone(inst)

    def test_parse_with_phase(self):
        """Test parsing with phase."""
        base, phase, inst = parse_trace_query("fdd-test-flow-login:ph-1")
        
        # Extracts phase correctly
        self.assertEqual(base, "fdd-test-flow-login")
        self.assertEqual(phase, "ph-1")
        self.assertIsNone(inst)

    def test_parse_with_phase_and_instruction(self):
        """Test parsing with phase and instruction."""
        base, phase, inst = parse_trace_query("fdd-test-flow-login:ph-1:inst-step-1")
        
        # Extracts both phase and instruction
        self.assertEqual(base, "fdd-test-flow-login")
        self.assertEqual(phase, "ph-1")
        self.assertEqual(inst, "inst-step-1")

    def test_parse_without_at_symbol(self):
        """Test parsing without @ symbol."""
        base, phase, inst = parse_trace_query("fdd-test-flow-login:ph-1")
        
        # Without @ it treats whole thing as base
        self.assertIsNotNone(base)
        self.assertIsNone(inst)


class TestExtractIds(unittest.TestCase):
    """Test extract_ids function."""

    def test_extract_single_id(self):
        """Test extracting single ID."""
        lines = ["Some text with `fdd-test-actor-user` in it"]
        
        ids = extract_ids(lines)
        
        self.assertGreater(len(ids), 0)
        self.assertEqual(ids[0]["id"], "fdd-test-actor-user")

    def test_extract_multiple_ids(self):
        """Test extracting multiple IDs."""
        lines = [
            "Actor: `fdd-test-actor-user`",
            "Capability: `fdd-test-capability-login`",
        ]
        
        ids = extract_ids(lines)
        
        self.assertGreaterEqual(len(ids), 2)

    def test_extract_with_columns(self):
        """Test extracting IDs with column numbers."""
        lines = ["Text `fdd-test-actor-user` more text"]
        
        ids = extract_ids(lines, with_cols=True)
        
        self.assertGreater(len(ids), 0)
        self.assertIn("col", ids[0])


class TestFilterIdHits(unittest.TestCase):
    """Test filter_hits function."""

    def test_filter_with_substring(self):
        """Test filtering with substring pattern."""
        hits = [
            {"id": "fdd-test-actor-user"},
            {"id": "fdd-test-actor-admin"},
            {"id": "fdd-test-capability-login"},
        ]
        
        filtered = filter_hits(hits, pattern="actor", regex=False)
        
        self.assertEqual(len(filtered), 2)

    def test_filter_with_regex(self):
        """Test filtering with regex pattern."""
        hits = [
            {"id": "fdd-test-actor-user"},
            {"id": "fdd-test-actor-admin"},
            {"id": "fdd-test-capability-login"},
        ]
        
        filtered = filter_hits(hits, pattern="actor-.*", regex=True)
        
        self.assertEqual(len(filtered), 2)

    def test_filter_no_pattern(self):
        """Test filtering with no pattern returns all."""
        hits = [
            {"id": "fdd-test-actor-user"},
            {"id": "fdd-test-capability-login"},
        ]
        
        filtered = filter_hits(hits, pattern=None, regex=False)
        
        self.assertEqual(len(filtered), 2)


class TestUniqueIdHits(unittest.TestCase):
    """Test unique_hits function."""

    def test_remove_duplicates(self):
        """Test removing duplicate IDs."""
        hits = [
            {"id": "fdd-test-actor-user", "line": 10},
            {"id": "fdd-test-actor-user", "line": 20},
            {"id": "fdd-test-capability-login", "line": 30},
        ]
        
        unique = unique_hits(hits)
        
        self.assertEqual(len(unique), 2)

    def test_preserve_order(self):
        """Test preserving first occurrence order."""
        hits = [
            {"id": "fdd-test-actor-admin", "line": 10},
            {"id": "fdd-test-actor-user", "line": 20},
            {"id": "fdd-test-actor-admin", "line": 30},
        ]
        
        unique = unique_hits(hits)
        
        self.assertEqual(len(unique), 2)
        self.assertEqual(unique[0]["id"], "fdd-test-actor-admin")
        self.assertEqual(unique[1]["id"], "fdd-test-actor-user")


class TestNearestHeadingTitle(unittest.TestCase):
    """Test find_nearest_heading function."""

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
        
        title = find_nearest_heading(lines, from_idx=5)
        
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
        
        title = find_nearest_heading(lines, from_idx=5)
        
        self.assertEqual(title, "Subsection")

    def test_no_heading_found(self):
        """Test when no heading is found."""
        lines = [
            "Just some text",
            "No headings here",
        ]
        
        title = find_nearest_heading(lines, from_idx=1)
        
        self.assertIsNone(title)


class TestInferFddTypeFromId(unittest.TestCase):
    """Test infer_fdd_type function."""

    def test_infer_actor(self):
        """Test inferring actor type."""
        fdd_type = infer_fdd_type("fdd-test-actor-user")
        self.assertEqual(fdd_type, "actor")

    def test_infer_capability(self):
        """Test inferring capability type."""
        fdd_type = infer_fdd_type("fdd-test-capability-login")
        self.assertEqual(fdd_type, "capability")

    def test_infer_requirement(self):
        """Test inferring requirement type."""
        fdd_type = infer_fdd_type("fdd-test-req-001")
        self.assertEqual(fdd_type, "requirement")

    def test_infer_usecase(self):
        """Test inferring usecase type."""
        fdd_type = infer_fdd_type("fdd-test-usecase-login")
        self.assertEqual(fdd_type, "usecase")

    def test_infer_adr(self):
        """Test inferring ADR type."""
        fdd_type = infer_fdd_type("fdd-test-adr-0001")
        self.assertEqual(fdd_type, "adr")

    def test_infer_generic(self):
        """Test inferring generic ID type."""
        fdd_type = infer_fdd_type("fdd-test-something-else")
        self.assertEqual(fdd_type, "id")


class TestDetectKind(unittest.TestCase):
    """Test detect_artifact_kind function."""

    def test_detect_features_manifest(self):
        """Test detecting FEATURES.md."""
        path = Path("/test/FEATURES.md")
        kind = detect_artifact_kind(path)
        self.assertEqual(kind, "features-manifest")

    def test_detect_feature_changes(self):
        """Test detecting feature CHANGES.md."""
        path = Path("/test/feature-test-CHANGES.md")
        kind = detect_artifact_kind(path)
        self.assertEqual(kind, "feature-changes")

    def test_detect_design(self):
        """Test detecting DESIGN.md."""
        path = Path("/test/DESIGN.md")
        kind = detect_artifact_kind(path)
        self.assertEqual(kind, "overall-design")

    def test_detect_feature_design(self):
        """Test detecting feature DESIGN.md."""
        path = Path("/test/architecture/features/feature-x/DESIGN.md")
        kind = detect_artifact_kind(path)
        self.assertEqual(kind, "feature-design")

    def test_detect_changes(self):
        """Test detecting CHANGES.md."""
        path = Path("/test/CHANGES.md")
        kind = detect_artifact_kind(path)
        self.assertEqual(kind, "feature-changes")

    def test_detect_generic(self):
        """Test detecting generic file."""
        path = Path("/test/README.md")
        kind = detect_artifact_kind(path)
        self.assertEqual(kind, "generic")


class TestFindAllInLine(unittest.TestCase):
    """Test find_all_positions function."""

    def test_find_single_occurrence(self):
        """Test finding single occurrence."""
        positions = find_all_positions("Hello world", "world")
        
        self.assertEqual(len(positions), 1)
        self.assertEqual(positions[0], 6)

    def test_find_multiple_occurrences(self):
        """Test finding multiple occurrences."""
        positions = find_all_positions("test test test", "test")
        
        self.assertEqual(len(positions), 3)
        self.assertEqual(positions, [0, 5, 10])

    def test_find_no_occurrences(self):
        """Test finding no occurrences."""
        positions = find_all_positions("Hello world", "xyz")
        
        self.assertEqual(len(positions), 0)


class TestRelativePosix(unittest.TestCase):
    """Test to_relative_posix function."""

    def test_relative_path_within_root(self):
        """Test relative path within root."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            subpath = root / "subdir" / "file.txt"
            
            rel = to_relative_posix(subpath, root)
            
            self.assertEqual(rel, "subdir/file.txt")

    def test_absolute_path_outside_root(self):
        """Test absolute path when outside root."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "root"
            outside = Path(tmpdir) / "outside" / "file.txt"
            
            rel = to_relative_posix(outside, root)
            
            # Should return absolute path when outside root
            self.assertIn("outside", rel)


class TestIterTextFiles(unittest.TestCase):
    def test_iter_text_files_include_exclude_and_max_bytes(self):
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "a").mkdir()
            (root / "a" / "small.md").write_text("x\n", encoding="utf-8")
            (root / "a" / "big.md").write_text("x" * 200, encoding="utf-8")
            (root / "a" / "skip.md").write_text("x\n", encoding="utf-8")

            hits = iter_text_files(
                root,
                includes=["**/*.md"],
                excludes=["**/skip.md"],
                max_bytes=100,
            )
            rels = sorted([p.resolve().relative_to(root.resolve()).as_posix() for p in hits])
            self.assertEqual(rels, ["a/small.md"])

    def test_iter_text_files_relative_to_value_error_is_ignored(self):
        import os
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)

            orig_walk = os.walk

            def fake_walk(_root):
                yield ("/", [], ["outside.md"])

            os.walk = fake_walk
            try:
                hits = iter_text_files(root)
                self.assertEqual(hits, [])
            finally:
                os.walk = orig_walk


class TestReadTextSafe(unittest.TestCase):
    def test_read_text_safe_nonexistent_returns_none(self):
        with TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "missing.txt"
            self.assertIsNone(read_text_safe(p))

    def test_read_text_safe_null_bytes_returns_none(self):
        with TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "bin.txt"
            p.write_bytes(b"a\x00b")
            self.assertIsNone(read_text_safe(p))

    def test_read_text_safe_invalid_utf8_ignores(self):
        with TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "bad.txt"
            p.write_bytes(b"hi\xff\xfe")
            lines = read_text_safe(p)
            self.assertIsNotNone(lines)
            self.assertTrue(any("hi" in x for x in lines or []))

    def test_read_text_safe_normalizes_crlf_when_linesep_differs(self):
        import os

        with TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "crlf.txt"
            p.write_bytes(b"a\r\nb\r\n")

            orig = os.linesep
            try:
                os.linesep = "\r\n"
                lines = read_text_safe(p)
                self.assertEqual(lines, ["a", "b"])
            finally:
                os.linesep = orig


class TestHeadingLevel(unittest.TestCase):
    """Test get_heading_level function."""

    def test_level_1(self):
        """Test detecting level 1 heading."""
        level = get_heading_level("# Title")
        self.assertEqual(level, 1)

    def test_level_2(self):
        """Test detecting level 2 heading."""
        level = get_heading_level("## Section")
        self.assertEqual(level, 2)

    def test_level_3(self):
        """Test detecting level 3 heading."""
        level = get_heading_level("### Subsection")
        self.assertEqual(level, 3)

    def test_not_heading(self):
        """Test detecting non-heading line."""
        level = get_heading_level("Regular text")
        self.assertIsNone(level)

    def test_heading_with_spaces(self):
        """Test heading with extra spaces."""
        level = get_heading_level("####    Title with spaces")
        self.assertEqual(level, 4)


if __name__ == "__main__":
    unittest.main()
