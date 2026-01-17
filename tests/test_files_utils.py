"""
Test files utility functions.

Tests load_text, find_adapter_directory and related file operations.
"""

import unittest
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))

from fdd.utils.files import load_text, find_adapter_directory


class TestLoadText(unittest.TestCase):
    """Test load_text function."""

    def test_load_text_existing_file(self):
        """Test loading text from existing file."""
        with TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("Test content\nLine 2")
            
            content, error = load_text(test_file)
            
            self.assertIsNone(error)
            self.assertEqual(content, "Test content\nLine 2")

    def test_load_text_nonexistent_file(self):
        """Test loading text from nonexistent file returns error."""
        with TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "nonexistent.md"
            
            content, error = load_text(test_file)
            
            # Function returns empty string on error, not None
            self.assertEqual(content, "")
            self.assertIsNotNone(error)
            self.assertIn("not found", error.lower())

    def test_load_text_empty_file(self):
        """Test loading text from empty file."""
        with TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "empty.md"
            test_file.write_text("")
            
            content, error = load_text(test_file)
            
            self.assertIsNone(error)
            self.assertEqual(content, "")


class TestFindAdapterDirectory(unittest.TestCase):
    """Test find_adapter_directory function."""

    def test_find_adapter_with_agents_md(self):
        """Test finding adapter directory with AGENTS.md."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            
            # Create .git to mark as project root
            (root / ".git").mkdir()
            
            adapter_dir = root / ".adapter"
            adapter_dir.mkdir()
            
            # Create AGENTS.md with adapter markers
            (adapter_dir / "AGENTS.md").write_text("# FDD Adapter: Test\n\nThis is an FDD adapter for testing.")
            
            # Create specs directory (required for validation)
            specs_dir = adapter_dir / "specs"
            specs_dir.mkdir()
            (specs_dir / "test.md").write_text("# Spec")
            
            result = find_adapter_directory(root)
            
            self.assertIsNotNone(result)
            self.assertEqual(result.resolve(), adapter_dir.resolve())

    def test_find_adapter_no_adapter(self):
        """Test when no adapter directory exists."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            
            # Create .git to mark as project root
            (root / ".git").mkdir()
            
            result = find_adapter_directory(root)
            
            self.assertIsNone(result)

    def test_find_adapter_with_specs_only(self):
        """Test finding adapter with specs/ directory only."""
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            
            # Create .git to mark as project root
            (root / ".git").mkdir()
            
            adapter_dir = root / ".fdd-adapter"
            adapter_dir.mkdir()
            
            # Create AGENTS.md (required)
            (adapter_dir / "AGENTS.md").write_text("# Navigation\n\nAdapter navigation.")
            
            # Create specs directory (validates as adapter)
            specs_dir = adapter_dir / "specs"
            specs_dir.mkdir()
            (specs_dir / "api.md").write_text("# API")
            
            result = find_adapter_directory(root)
            
            self.assertIsNotNone(result)
            self.assertEqual(result.resolve(), adapter_dir.resolve())


if __name__ == "__main__":
    unittest.main()
