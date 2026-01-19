# @fdd-test:fdd-fdd-feature-core-methodology-test-helpers:ph-1
"""
Test helper functions for parsing artifacts.

Tests find_present_section_ids, parse_business_model, and parse_adr_index.
"""

import unittest
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))

from fdd.utils.helpers import (
    find_present_section_ids,
    parse_business_model,
    parse_adr_index,
)

from fdd.utils.markdown import (
    business_block_bounds,
    design_item_block_bounds,
    extract_heading_block,
    find_anchor_idx_for_id,
    list_items,
    list_section_entries,
    read_change_block,
    read_letter_section,
    resolve_under_heading,
)

from fdd.utils.search import (
    compile_trace_regex,
    definition_hits_in_file,
    iter_candidate_definition_files,
    scan_ids,
    where_defined_internal,
    where_used,
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


class TestMarkdownUtils(unittest.TestCase):
    def test_extract_heading_block_from_body_line(self) -> None:
        lines = [
            "# Top\n",
            "intro\n",
            "## Section B\n",
            "b1\n",
            "### Inner\n",
            "inner text\n",
            "## Section C\n",
            "c1\n",
        ]

        start, end = extract_heading_block(lines, 5)
        self.assertEqual(start, 4)
        self.assertEqual(end, 6)

    def test_resolve_under_heading_returns_bounds_and_level(self) -> None:
        lines = [
            "# Top\n",
            "intro\n",
            "## Section B\n",
            "b1\n",
            "### Inner\n",
            "inner text\n",
            "## Section C\n",
            "c1\n",
        ]

        resolved = resolve_under_heading(lines, "Section B")
        self.assertIsNotNone(resolved)
        assert resolved is not None
        start, end, level = resolved
        self.assertEqual((start, end, level), (2, 6, 2))

    def test_find_anchor_idx_for_id_prefers_id_line(self) -> None:
        fid = "fdd-example-feature-x-req-do-thing"
        lines = [
            "# Doc\n",
            f"- **ID**: `{fid}`\n",
            f"## {fid}\n",
        ]

        idx = find_anchor_idx_for_id(lines, fid)
        self.assertEqual(idx, 1)

    def test_business_block_bounds_returns_enclosing_heading_block(self) -> None:
        lines = [
            "## B. Actors\n",
            "\n",
            "#### Admin\n",
            "**ID**: `fdd-app-actor-admin`\n",
            "extra\n",
            "#### User\n",
            "**ID**: `fdd-app-actor-user`\n",
        ]

        bounds = business_block_bounds(lines, section_start=0, section_end=len(lines), id_idx=3)
        self.assertEqual(bounds, (2, 5))

    def test_design_item_block_bounds_respects_boundaries(self) -> None:
        lines = [
            "## A. Section\n",
            "\n",
            "#### Item One\n",
            "some text\n",
            "- **ID**: `fdd-example-item-one`\n",
            "more text\n",
            "**Outputs**:\n",
            "- ok\n",
            "#### Item Two\n",
        ]

        start, end = design_item_block_bounds(lines, start=0, end=len(lines), id_idx=4)
        self.assertEqual((start, end), (2, 6))

    def test_read_change_block_bounds(self) -> None:
        lines = [
            "# Implementation Plan\n",
            "\n",
            "## Change 1: First\n",
            "x\n",
            "## Change 2: Second\n",
            "y\n",
        ]

        b = read_change_block(lines, 1)
        self.assertEqual(b, (2, 4))
        self.assertIsNone(read_change_block(lines, 3))

    def test_read_letter_section_is_case_insensitive(self) -> None:
        lines = [
            "# Doc\n",
            "## A. First\n",
            "a\n",
            "## B. Second\n",
            "b\n",
        ]

        sec = read_letter_section(lines, "b")
        self.assertEqual(sec, (3, 5))

    def test_list_section_entries_features_manifest(self) -> None:
        lines = [
            "# Features\n",
            "\n",
            "### 1. [Feature One](feature-one/) ✅ HIGH\n",
            "### 2. [Feature Two](feature-two/) ⏳ MEDIUM\n",
        ]

        entries = list_section_entries(lines, kind="features-manifest")
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["line"], 3)
        self.assertEqual(entries[0]["feature_id"], "Feature One")
        self.assertEqual(entries[0]["dir"], "feature-one/")
        self.assertEqual(entries[0]["emoji"], "✅")
        self.assertEqual(entries[0]["priority"], "HIGH")

    def test_list_items_feature_changes_summary(self) -> None:
        cid = "fdd-app-feature-x-change-first"
        lines = [
            "# Implementation Plan: X\n",
            "\n",
            "## Change 1: Do thing\n",
            f"**ID**: `{cid}`\n",
            "**Status**: IN_PROGRESS\n",
            "\n",
            "## Change 2: Another\n",
            "**Status**: NOT_STARTED\n",
        ]

        items = list_items(
            kind="feature-changes",
            artifact_name="CHANGES.md",
            lines=lines,
            active_lines=lines,
            base_offset=0,
            lod="summary",
            pattern=None,
            regex=False,
            type_filter=None,
        )

        self.assertEqual(len(items), 2)
        by_change = {int(it["change"]): it for it in items}
        self.assertEqual(set(by_change.keys()), {1, 2})

        self.assertEqual(by_change[1]["type"], "change")
        self.assertEqual(by_change[1]["id"], cid)
        self.assertEqual(by_change[1]["title"], "Do thing")
        self.assertEqual(by_change[1]["status"], "IN_PROGRESS")

        self.assertEqual(by_change[2]["type"], "change")
        self.assertEqual(by_change[2]["id"], "change-2")

    def test_list_items_generic_adr_summary(self) -> None:
        lines = [
            "# ADR Index\n",
            "\n",
            "## ADR-0001: Use Python\n",
            "**Date**: 2024-01-15\n",
            "**Status**: Accepted\n",
            "\n",
            "## ADR-0002: Use Rust\n",
        ]

        items = list_items(
            kind="generic",
            artifact_name="ADR.md",
            lines=lines,
            active_lines=lines,
            base_offset=0,
            lod="summary",
            pattern=None,
            regex=False,
            type_filter=None,
        )

        self.assertEqual([it["id"] for it in items], ["ADR-0001", "ADR-0002"])
        self.assertEqual(items[0]["type"], "adr")
        self.assertEqual(items[0]["title"], "Use Python")
        self.assertEqual(items[0]["date"], "2024-01-15")
        self.assertEqual(items[0]["status"], "Accepted")

    def test_list_items_generic_business_summary(self) -> None:
        a1 = "fdd-app-actor-admin"
        c1 = "fdd-app-capability-manage"
        u1 = "fdd-app-usecase-login"
        lines = [
            "# Business Context\n",
            "\n",
            "## B. Actors\n",
            "\n",
            "#### Admin\n",
            f"**ID**: `{a1}`\n",
            "\n",
            "## C. Capabilities\n",
            "\n",
            "#### Manage\n",
            f"**ID**: `{c1}`\n",
            "\n",
            "## D. Use Cases\n",
            "\n",
            "#### Login\n",
            f"**ID**: `{u1}`\n",
        ]

        items = list_items(
            kind="generic",
            artifact_name="BUSINESS.md",
            lines=lines,
            active_lines=lines,
            base_offset=0,
            lod="summary",
            pattern=None,
            regex=False,
            type_filter=None,
        )

        self.assertEqual([it["type"] for it in items], ["actor", "capability", "usecase"])
        self.assertEqual([it["id"] for it in items], [a1, c1, u1])
        self.assertEqual(items[0]["title"], "Admin")
        self.assertEqual(items[0]["section"], "B")

    def test_list_items_overall_design_checked_and_title(self) -> None:
        rid = "fdd-app-req-login"
        lines = [
            "# Overall Design\n",
            "\n",
            "## A. Requirements\n",
            "- [x] **ID**: `fdd-app-req-login`\n",
        ]

        items = list_items(
            kind="overall-design",
            artifact_name="DESIGN.md",
            lines=lines,
            active_lines=lines,
            base_offset=0,
            lod="summary",
            pattern=None,
            regex=False,
            type_filter=None,
        )

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["id"], rid)
        self.assertEqual(items[0]["type"], "requirement")
        self.assertEqual(items[0]["checked"], True)
        self.assertEqual(items[0]["title"], "A. Requirements")

    def test_list_items_feature_design_checked_and_title(self) -> None:
        fid = "fdd-app-feature-x-algo-do-thing"
        lines = [
            "# Feature: X\n",
            "\n",
            "## C. Algorithms (FDL)\n",
            "### Algo\n",
            "- [ ] **ID**: `fdd-app-feature-x-algo-do-thing`\n",
        ]

        items = list_items(
            kind="feature-design",
            artifact_name="DESIGN.md",
            lines=lines,
            active_lines=lines,
            base_offset=0,
            lod="summary",
            pattern=None,
            regex=False,
            type_filter=None,
        )

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["id"], fid)
        self.assertEqual(items[0]["type"], "algo")
        self.assertEqual(items[0]["checked"], False)
        self.assertEqual(items[0]["title"], "Algo")


class TestSearchUtils(unittest.TestCase):
    def test_compile_trace_regex_matches_variants(self) -> None:
        base = "fdd-app-feature-x-algo-do-thing"
        rx = compile_trace_regex(base, "ph-1", "inst-ok")

        self.assertIsNotNone(rx.search(f"// {base}:ph-1:inst-ok"))
        self.assertIsNotNone(rx.search(f"// {base} `ph-1` `inst-ok`"))
        self.assertIsNotNone(rx.search(f"// {base} :ph-1 :inst-ok"))

    def test_iter_candidate_definition_files_prefers_expected_files(self) -> None:
        with TemporaryDirectory() as tds:
            td = Path(tds)
            (td / "architecture" / "features" / "feature-x").mkdir(parents=True)
            (td / "architecture" / "features").mkdir(parents=True, exist_ok=True)

            (td / "architecture" / "BUSINESS.md").write_text("# Biz\n", encoding="utf-8")
            (td / "architecture" / "DESIGN.md").write_text("# Design\n", encoding="utf-8")
            (td / "architecture" / "ADR.md").write_text("# ADR\n", encoding="utf-8")
            (td / "architecture" / "features" / "FEATURES.md").write_text("# Features\n", encoding="utf-8")
            (td / "architecture" / "features" / "feature-x" / "DESIGN.md").write_text("# Feature\n", encoding="utf-8")
            (td / "architecture" / "features" / "feature-x" / "CHANGES.md").write_text("# Implementation Plan: X\n", encoding="utf-8")

            actor = "fdd-app-actor-admin"
            req = "fdd-app-req-login"
            adr = "ADR-0001"
            f_adr = "fdd-app-adr-0001"
            algo = "fdd-app-feature-x-algo-do-thing"
            change = "fdd-app-feature-x-change-first"

            actor_files = iter_candidate_definition_files(td, needle=actor)
            self.assertTrue(any(str(p).endswith("architecture/BUSINESS.md") for p in actor_files))

            req_files = iter_candidate_definition_files(td, needle=req)
            self.assertTrue(any(str(p).endswith("architecture/DESIGN.md") for p in req_files))

            adr_files = iter_candidate_definition_files(td, needle=adr)
            self.assertTrue(any(str(p).endswith("architecture/ADR.md") for p in adr_files))

            fadr_files = iter_candidate_definition_files(td, needle=f_adr)
            self.assertTrue(any(str(p).endswith("architecture/ADR.md") for p in fadr_files))

            algo_files = iter_candidate_definition_files(td, needle=algo)
            self.assertTrue(any("architecture/features/" in str(p) and str(p).endswith("/DESIGN.md") for p in algo_files))

            change_files = iter_candidate_definition_files(td, needle=change)
            self.assertTrue(any("/CHANGES.md" in str(p) for p in change_files))

    def test_definition_hits_in_file_business_filters_by_section(self) -> None:
        with TemporaryDirectory() as tds:
            td = Path(tds)
            (td / "architecture").mkdir(parents=True)
            p = td / "architecture" / "BUSINESS.md"
            fid = "fdd-app-actor-admin"
            p.write_text(
                "\n".join(
                    [
                        "# Biz",
                        "",
                        "## B. Actors",
                        "",
                        "#### Admin",
                        f"**ID**: `{fid}`",
                        "",
                        "## C. Capabilities",
                        "",
                        f"**ID**: `{fid}`",
                        "",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            hits = definition_hits_in_file(path=p, root=td, needle=fid, include_tags=False)
            self.assertEqual(len(hits), 1)
            self.assertEqual(hits[0]["match"], "id_line")
            self.assertEqual(hits[0]["path"], "architecture/BUSINESS.md")

    def test_definition_hits_in_file_design_filters_by_subsection(self) -> None:
        with TemporaryDirectory() as tds:
            td = Path(tds)
            (td / "architecture").mkdir(parents=True)
            p = td / "architecture" / "DESIGN.md"
            rid = "fdd-app-req-login"
            p.write_text(
                "\n".join(
                    [
                        "# Design",
                        "",
                        "## A. Overview",
                        "",
                        "## B. Requirements",
                        "",
                        "### 1. Functional Requirements",
                        f"- [ ] **ID**: `{rid}`",
                        "",
                        "### 2. NFR",
                        f"- [ ] **ID**: `fdd-app-nfr-fast`",
                        "",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            hits = definition_hits_in_file(path=p, root=td, needle=rid, include_tags=False)
            self.assertEqual(len(hits), 1)
            self.assertEqual(hits[0]["match"], "id_line")
            self.assertEqual(hits[0]["path"], "architecture/DESIGN.md")

    def test_where_defined_internal_returns_segment_defs_for_phase_inst(self) -> None:
        with TemporaryDirectory() as tds:
            td = Path(tds)
            (td / "architecture" / "features" / "feature-x").mkdir(parents=True)

            base = "fdd-app-feature-x-algo-do-thing"
            inst = "inst-return-ok"
            (td / "architecture" / "features" / "feature-x" / "DESIGN.md").write_text(
                "\n".join(
                    [
                        "# Feature: X",
                        "",
                        "## C. Algorithms (FDL)",
                        "### Algo",
                        "",
                        f"- [ ] **ID**: `{base}`",
                        "",
                        f"1. [ ] - `ph-1` - RETURN ok - `{inst}`",
                        "",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            raw = f"{base}:ph-1:{inst}"
            _, defs, ctx_defs = where_defined_internal(
                root=td,
                raw_id=raw,
                include_tags=False,
                includes=None,
                excludes=None,
                max_bytes=1_000_000,
            )

            self.assertTrue(len(ctx_defs) >= 1)
            self.assertTrue(any(d.get("segment") == "inst" for d in defs))

    def test_where_used_excludes_definition_lines(self) -> None:
        with TemporaryDirectory() as tds:
            td = Path(tds)
            (td / "architecture" / "features" / "feature-x").mkdir(parents=True)
            (td / "src").mkdir(parents=True)

            base = "fdd-app-feature-x-algo-do-thing"
            inst = "inst-return-ok"
            (td / "architecture" / "features" / "feature-x" / "DESIGN.md").write_text(
                "\n".join(
                    [
                        "# Feature: X",
                        "",
                        "## C. Algorithms (FDL)",
                        "### Algo",
                        "",
                        f"- [ ] **ID**: `{base}`",
                        "",
                        f"1. [ ] - `ph-1` - RETURN ok - `{inst}`",
                        "",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (td / "src" / "lib.rs").write_text(
                f"// usage {base}:ph-1:{inst}\n",
                encoding="utf-8",
            )

            raw = f"{base}:ph-1:{inst}"
            _base, _ph, _inst, hits = where_used(root=td, raw_id=raw, include=None, exclude=None, max_bytes=1_000_000)
            paths = [h["path"] for h in hits]
            self.assertIn("src/lib.rs", paths)
            self.assertNotIn("architecture/features/feature-x/DESIGN.md", paths)

    def test_scan_ids_deduplicates_by_default(self) -> None:
        with TemporaryDirectory() as tds:
            td = Path(tds)
            p = td / "doc.md"
            p.write_text(
                "\n".join(
                    [
                        "**ID**: `fdd-app-actor-admin`",
                        "**ID**: `fdd-app-actor-admin`",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            hits = scan_ids(
                root=p,
                pattern=None,
                regex=False,
                kind="fdd",
                include=None,
                exclude=None,
                max_bytes=1_000_000,
                all_ids=False,
            )
            self.assertEqual(len(hits), 1)


if __name__ == "__main__":
    unittest.main()
