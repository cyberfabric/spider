# @fdd-test:fdd-fdd-feature-core-methodology-test-helpers:ph-1
"""
Test helper functions for parsing artifacts.

Tests find_present_section_ids, parse_business_model, and parse_adr_index.
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))

from fdd.utils.helpers import (
    find_present_section_ids,
    parse_business_model,
    parse_adr_index,
)


class TestFindPresentSectionIds(unittest.TestCase):
    """Test find_present_section_ids function."""

    def test_find_section_ids_single_section(self):
        """Test finding single section ID."""
        text = """# Document

## A. First Section

Some content here.
"""
        result = find_present_section_ids(text)
        self.assertEqual(result, ["A"])

    def test_find_section_ids_multiple_sections(self):
        """Test finding multiple section IDs."""
        text = """# Document

## A. First Section

Content A

## B. Second Section

Content B

## C. Third Section

Content C
"""
        result = find_present_section_ids(text)
        self.assertEqual(result, ["A", "B", "C"])

    def test_find_section_ids_with_subsections(self):
        """Test that subsections (###) are not captured as section IDs."""
        text = """# Document

## A. First Section

### A.1 Subsection

Content

## B. Second Section

### B.1 Subsection
"""
        result = find_present_section_ids(text)
        self.assertEqual(result, ["A", "B"])

    def test_find_section_ids_empty_text(self):
        """Test with empty text."""
        result = find_present_section_ids("")
        self.assertEqual(result, [])

    def test_find_section_ids_no_sections(self):
        """Test with text that has no sections."""
        text = """# Document

Some content without sections.

More content.
"""
        result = find_present_section_ids(text)
        self.assertEqual(result, [])

    def test_find_section_ids_preserves_order(self):
        """Test that section order is preserved."""
        text = """## C. Third
## A. First
## B. Second
"""
        result = find_present_section_ids(text)
        self.assertEqual(result, ["C", "A", "B"])


class TestParseBusinessModel(unittest.TestCase):
    """Test parse_business_model function."""

    def test_parse_business_model_basic(self):
        """Test basic parsing of actors, capabilities, and use cases."""
        text = """# Business Context

## B. Actors

- **ID**: `fdd-app-actor-admin`
- **ID**: `fdd-app-actor-user`

## C. Capabilities

### CAP-001: Manage Users

**ID**: `fdd-app-capability-manage-users`

**Actors**: `fdd-app-actor-admin`

### CAP-002: View Dashboard

**ID**: `fdd-app-capability-view-dashboard`

**Actors**: `fdd-app-actor-user`, `fdd-app-actor-admin`

## D. Use Cases

- **ID**: `fdd-app-usecase-login`
- **ID**: `fdd-app-usecase-logout`
"""
        actors, capabilities, usecases = parse_business_model(text)
        
        # Verify actors
        self.assertIn("fdd-app-actor-admin", actors)
        self.assertIn("fdd-app-actor-user", actors)
        self.assertEqual(len(actors), 2)
        
        # Verify capabilities
        self.assertIn("fdd-app-capability-manage-users", capabilities)
        self.assertIn("fdd-app-capability-view-dashboard", capabilities)
        
        # Verify capability-actor mappings
        self.assertIn("fdd-app-actor-admin", capabilities["fdd-app-capability-manage-users"])
        self.assertIn("fdd-app-actor-user", capabilities["fdd-app-capability-view-dashboard"])
        self.assertIn("fdd-app-actor-admin", capabilities["fdd-app-capability-view-dashboard"])
        
        # Verify use cases
        self.assertIn("fdd-app-usecase-login", usecases)
        self.assertIn("fdd-app-usecase-logout", usecases)
        self.assertEqual(len(usecases), 2)

    def test_parse_business_model_empty(self):
        """Test parsing empty text."""
        actors, capabilities, usecases = parse_business_model("")
        
        self.assertEqual(len(actors), 0)
        self.assertEqual(len(capabilities), 0)
        self.assertEqual(len(usecases), 0)

    def test_parse_business_model_section_c_variations(self):
        """Test that both 'Section C' and 'C. Capabilities' are recognized."""
        text1 = """## C. Capabilities

**ID**: `fdd-app-capability-test`

**Actors**: `fdd-app-actor-test`
"""
        
        text2 = """## Section C: Capabilities

**ID**: `fdd-app-capability-test`

**Actors**: `fdd-app-actor-test`
"""
        
        _, caps1, _ = parse_business_model(text1)
        _, caps2, _ = parse_business_model(text2)
        
        self.assertIn("fdd-app-capability-test", caps1)
        self.assertIn("fdd-app-capability-test", caps2)

    def test_parse_business_model_capability_without_actors(self):
        """Test capability that doesn't reference any actors."""
        text = """## C. Capabilities

### CAP-001: Generic Capability

**ID**: `fdd-app-capability-generic`

No actors referenced.
"""
        _, capabilities, _ = parse_business_model(text)
        
        self.assertIn("fdd-app-capability-generic", capabilities)
        self.assertEqual(len(capabilities["fdd-app-capability-generic"]), 0)

    def test_parse_business_model_multiple_actors_per_capability(self):
        """Test capability with multiple actor references."""
        text = """## C. Capabilities

### CAP-001: Multi-Actor Capability

**ID**: `fdd-app-capability-multi`

**Actors**: `fdd-app-actor-one`, `fdd-app-actor-two`, `fdd-app-actor-three`

Additional line: `fdd-app-actor-four`
"""
        _, capabilities, _ = parse_business_model(text)
        
        cap_actors = capabilities["fdd-app-capability-multi"]
        self.assertEqual(len(cap_actors), 4)
        self.assertIn("fdd-app-actor-one", cap_actors)
        self.assertIn("fdd-app-actor-two", cap_actors)
        self.assertIn("fdd-app-actor-three", cap_actors)
        self.assertIn("fdd-app-actor-four", cap_actors)

    def test_parse_business_model_stops_at_next_section(self):
        """Test that capability parsing stops at next section."""
        text = """## C. Capabilities

**ID**: `fdd-app-capability-test`

**Actors**: `fdd-app-actor-test`

## D. Use Cases

**ID**: `fdd-app-capability-not-in-c`

**Actors**: `fdd-app-actor-not-in-c`
"""
        _, capabilities, _ = parse_business_model(text)
        
        self.assertIn("fdd-app-capability-test", capabilities)
        self.assertNotIn("fdd-app-capability-not-in-c", capabilities)


class TestParseAdrIndex(unittest.TestCase):
    """Test parse_adr_index function."""

    def test_parse_adr_index_basic(self):
        """Test basic ADR index parsing."""
        text = """# ADR Index

## ADR-0001: Use Python for Implementation

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

Decision content here.

## ADR-0002: Choose PostgreSQL

**Date**: 2024-01-20

**Status**: Proposed

**ID**: `fdd-app-adr-0002`

Decision content.
"""
        adrs, issues = parse_adr_index(text)
        
        self.assertEqual(len(adrs), 2)
        self.assertEqual(len(issues), 0)
        
        # Check first ADR
        self.assertEqual(adrs[0]["ref"], "ADR-0001")
        self.assertEqual(adrs[0]["num"], 1)
        self.assertEqual(adrs[0]["title"], "Use Python for Implementation")
        self.assertEqual(adrs[0]["date"], "2024-01-15")
        self.assertEqual(adrs[0]["status"], "Accepted")
        self.assertEqual(adrs[0]["id"], "fdd-app-adr-0001")
        
        # Check second ADR
        self.assertEqual(adrs[1]["ref"], "ADR-0002")
        self.assertEqual(adrs[1]["num"], 2)
        self.assertEqual(adrs[1]["title"], "Choose PostgreSQL")
        self.assertEqual(adrs[1]["date"], "2024-01-20")
        self.assertEqual(adrs[1]["status"], "Proposed")
        self.assertEqual(adrs[1]["id"], "fdd-app-adr-0002")

    def test_parse_adr_index_empty(self):
        """Test parsing empty text."""
        adrs, issues = parse_adr_index("")
        
        self.assertEqual(len(adrs), 0)
        self.assertEqual(len(issues), 0)

    def test_parse_adr_index_missing_metadata(self):
        """Test ADR with missing date, status, or ID."""
        text = """## ADR-0001: Minimal ADR

Some content without metadata.
"""
        adrs, issues = parse_adr_index(text)
        
        self.assertEqual(len(adrs), 1)
        self.assertEqual(adrs[0]["ref"], "ADR-0001")
        self.assertEqual(adrs[0]["title"], "Minimal ADR")
        self.assertIsNone(adrs[0]["date"])
        self.assertIsNone(adrs[0]["status"])
        self.assertIsNone(adrs[0]["id"])

    def test_parse_adr_index_metadata_in_various_positions(self):
        """Test that metadata is found within 10 lines after heading."""
        text = """## ADR-0001: Test

Line 1
Line 2
**Date**: 2024-01-15
Line 4
Line 5
**Status**: Accepted
Line 7
**ID**: `fdd-app-adr-0001`
"""
        adrs, issues = parse_adr_index(text)
        
        self.assertEqual(len(adrs), 1)
        self.assertEqual(adrs[0]["date"], "2024-01-15")
        self.assertEqual(adrs[0]["status"], "Accepted")
        self.assertEqual(adrs[0]["id"], "fdd-app-adr-0001")

    def test_parse_adr_index_stops_at_next_heading(self):
        """Test that metadata search stops at next heading."""
        text = """## ADR-0001: First

Content

## ADR-0002: Second

**Date**: 2024-01-20

This date should not be for ADR-0001.
"""
        adrs, issues = parse_adr_index(text)
        
        self.assertEqual(len(adrs), 2)
        self.assertIsNone(adrs[0]["date"])
        self.assertEqual(adrs[1]["date"], "2024-01-20")

    def test_parse_adr_index_padded_numbers(self):
        """Test ADR numbers with leading zeros."""
        text = """## ADR-0042: High Number ADR

**Date**: 2024-01-15
"""
        adrs, issues = parse_adr_index(text)
        
        self.assertEqual(len(adrs), 1)
        self.assertEqual(adrs[0]["ref"], "ADR-0042")
        self.assertEqual(adrs[0]["num"], 42)

    def test_parse_adr_index_multiple_status_values(self):
        """Test different status values."""
        text = """## ADR-0001: Accepted One

**Status**: Accepted

## ADR-0002: Proposed One

**Status**: Proposed

## ADR-0003: Deprecated One

**Status**: Deprecated

## ADR-0004: Superseded One

**Status**: Superseded
"""
        adrs, issues = parse_adr_index(text)
        
        self.assertEqual(len(adrs), 4)
        self.assertEqual(adrs[0]["status"], "Accepted")
        self.assertEqual(adrs[1]["status"], "Proposed")
        self.assertEqual(adrs[2]["status"], "Deprecated")
        self.assertEqual(adrs[3]["status"], "Superseded")


if __name__ == "__main__":
    unittest.main()
