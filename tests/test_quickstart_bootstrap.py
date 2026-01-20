"""
Tests for QUICKSTART bootstrap workflow.

Validates that QUICKSTART.md is readable and has proper structure.
"""

import sys
import unittest
from pathlib import Path

# Add skills/fdd/scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))


class TestQuickstartBootstrap(unittest.TestCase):
    """Test QUICKSTART.md file structure and content."""

    def test_quickstart_exists_and_readable(self):
        """Verify QUICKSTART.md exists and is readable."""
        quickstart = Path(__file__).parent.parent / "QUICKSTART.md"
        self.assertTrue(quickstart.exists(), "QUICKSTART.md must exist")
        
        content = quickstart.read_text(encoding='utf-8')
        self.assertGreater(len(content), 100, "QUICKSTART.md should have substantial content")
        
        # Check for key sections
        self.assertIn("Quick Start", content, "Should have Quick Start heading")
        self.assertIn("fdd", content.lower(), "Should mention fdd")


if __name__ == "__main__":
    unittest.main(verbosity=2)
