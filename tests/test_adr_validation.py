# @fdd-test:fdd-fdd-feature-core-methodology-test-adr-validation:ph-1
"""
Test ADR.md validation.

Critical validator for architectural decision records.
Ensures proper structure, metadata, required sections, and cross-references.
"""

import unittest
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "fdd" / "scripts"))

from fdd.validation.artifacts.adr import validate_adr


class TestADRStructure(unittest.TestCase):
    """Test ADR.md structure validation."""

    def test_minimal_valid_adr_passes(self):
        """Test minimal valid ADR passes validation."""
        text = """# ADR Index

## ADR-0001: Use Python for Implementation

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

We need to choose a programming language.

### Decision Drivers

- Team expertise
- Ecosystem

### Considered Options

- Python
- Java

### Decision Outcome

Chosen: Python

### Related Design Elements

- Implements: `fdd-app-req-language-selection`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(len(report["errors"]), 0)
        self.assertEqual(len(report["adr_issues"]), 0)

    def test_missing_date_fails(self):
        """Test that missing Date fails validation."""
        text = """# ADR Index

## ADR-0001: Test Decision

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        date_issues = [i for i in report["adr_issues"] if "Date" in i.get("message", "")]
        self.assertGreater(len(date_issues), 0)

    def test_missing_status_fails(self):
        """Test that missing Status fails validation."""
        text = """# ADR Index

## ADR-0001: Test Decision

**Date**: 2024-01-15

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        status_issues = [i for i in report["adr_issues"] if "Status" in i.get("message", "")]
        self.assertGreater(len(status_issues), 0)

    def test_invalid_status_value_fails(self):
        """Test that invalid status value fails."""
        text = """# ADR Index

## ADR-0001: Test Decision

**Date**: 2024-01-15

**Status**: Invalid

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        # Invalid status should be caught
        status_issues = [i for i in report["adr_issues"] if "Status" in i.get("message", "")]
        self.assertGreater(len(status_issues), 0)


class TestADRRequiredSections(unittest.TestCase):
    """Test ADR required sections validation."""

    def test_missing_context_section_fails(self):
        """Test that missing Context section fails."""
        text = """# ADR Index

## ADR-0001: Test Decision

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        section_issues = [i for i in report["adr_issues"] 
                         if "Context and Problem Statement" in i.get("message", "")]
        self.assertGreater(len(section_issues), 0)

    def test_missing_drivers_section_fails(self):
        """Test that missing Decision Drivers section fails."""
        text = """# ADR Index

## ADR-0001: Test Decision

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        section_issues = [i for i in report["adr_issues"]
                         if "Decision Drivers" in i.get("message", "")]
        self.assertGreater(len(section_issues), 0)

    def test_missing_options_section_fails(self):
        """Test that missing Considered Options section fails."""
        text = """# ADR Index

## ADR-0001: Test Decision

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        section_issues = [i for i in report["adr_issues"]
                         if "Considered Options" in i.get("message", "")]
        self.assertGreater(len(section_issues), 0)

    def test_missing_outcome_section_fails(self):
        """Test that missing Decision Outcome section fails."""
        text = """# ADR Index

## ADR-0001: Test Decision

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        section_issues = [i for i in report["adr_issues"]
                         if "Decision Outcome" in i.get("message", "")]
        self.assertGreater(len(section_issues), 0)

    def test_missing_related_elements_section_fails(self):
        """Test that missing Related Design Elements section fails."""
        text = """# ADR Index

## ADR-0001: Test Decision

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        section_issues = [i for i in report["adr_issues"]
                         if "Related Design Elements" in i.get("message", "")]
        self.assertGreater(len(section_issues), 0)

    def test_all_sections_present_passes(self):
        """Test that ADR with all sections passes."""
        text = """# ADR Index

## ADR-0001: Complete ADR

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

We need to decide something important.

### Decision Drivers

- Performance
- Maintainability
- Team skills

### Considered Options

1. Option A
2. Option B
3. Option C

### Decision Outcome

Chosen: Option B

Rationale: Best balance of performance and maintainability.

### Related Design Elements

- Implements: `fdd-app-req-performance`
- Supports: `fdd-app-principle-maintainability`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "PASS")


class TestADRRelatedElements(unittest.TestCase):
    """Test ADR Related Design Elements validation."""

    def test_empty_related_elements_fails(self):
        """Test that empty Related Design Elements fails."""
        text = """# ADR Index

## ADR-0001: Test Decision

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

No IDs here.
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        related_issues = [i for i in report["adr_issues"]
                         if "at least one ID" in i.get("message", "")]
        self.assertGreater(len(related_issues), 0)

    def test_related_elements_with_valid_ids_passes(self):
        """Test that Related Elements with valid IDs passes."""
        text = """# ADR Index

## ADR-0001: Test Decision

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- Implements: `fdd-app-req-authentication`
- Supports: `fdd-app-capability-secure-login`
- Impacts: `fdd-app-actor-admin`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "PASS")


class TestADRCrossReferences(unittest.TestCase):
    """Test ADR cross-reference validation."""

    def test_cross_reference_with_business_and_design(self):
        """Test ADR validates against BUSINESS.md and DESIGN.md."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            arch = tmppath / "architecture"
            arch.mkdir()
            
            # Create BUSINESS.md
            business = arch / "BUSINESS.md"
            business.write_text("""# Business Context

## B. Actors

- **ID**: `fdd-app-actor-user`

## C. Capabilities

### CAP-001: Login

**ID**: `fdd-app-capability-login`

**Actors**: `fdd-app-actor-user`
""")
            
            # Create DESIGN.md
            design = arch / "DESIGN.md"
            design.write_text("""# Technical Design

## B. Requirements

### FR-001: Authentication

**ID**: `fdd-app-req-auth`

**Capabilities**: `fdd-app-capability-login`

**Actors**: `fdd-app-actor-user`
""")
            
            # Create ADR.md
            adr = arch / "ADR.md"
            adr_text = """# ADR Index

## ADR-0001: Use JWT

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Choose auth mechanism.

### Decision Drivers

- Security

### Considered Options

- JWT
- Sessions

### Decision Outcome

Chosen: JWT

### Related Design Elements

- Implements: `fdd-app-req-auth`
- Impacts: `fdd-app-actor-user`
- Supports: `fdd-app-capability-login`
"""
            adr.write_text(adr_text)
            
            report = validate_adr(
                adr_text,
                artifact_path=adr,
                business_path=business,
                design_path=design,
                skip_fs_checks=False
            )
            
            # Should pass with valid cross-references
            self.assertEqual(report["status"], "PASS")

    def test_unknown_actor_reference_fails(self):
        """Test that unknown actor in Related Elements fails."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            arch = tmppath / "architecture"
            arch.mkdir()
            
            business = arch / "BUSINESS.md"
            business.write_text("""# Business Context

## B. Actors

- **ID**: `fdd-app-actor-user`
""")
            
            design = arch / "DESIGN.md"
            design.write_text("""# Technical Design

## B. Requirements

### FR-001: Test

**ID**: `fdd-app-req-test`
""")
            
            adr = arch / "ADR.md"
            adr_text = """# ADR Index

## ADR-0001: Test

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- Impacts: `fdd-app-actor-unknown`
"""
            adr.write_text(adr_text)
            
            report = validate_adr(
                adr_text,
                artifact_path=adr,
                business_path=business,
                design_path=design,
                skip_fs_checks=False
            )
            
            self.assertEqual(report["status"], "FAIL")
            unknown_actor = [i for i in report["adr_issues"]
                           if "Unknown actor" in i.get("message", "")]
            self.assertGreater(len(unknown_actor), 0)


class TestADRMultipleEntries(unittest.TestCase):
    """Test ADR.md with multiple ADR entries."""

    def test_multiple_adrs_all_valid_passes(self):
        """Test multiple ADRs that are all valid."""
        text = """# ADR Index

## ADR-0001: First Decision

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

First context.

### Decision Drivers

- Driver 1

### Considered Options

- Option A

### Decision Outcome

Chosen A.

### Related Design Elements

- `fdd-app-req-first`

## ADR-0002: Second Decision

**Date**: 2024-01-20

**Status**: Proposed

**ID**: `fdd-app-adr-0002`

### Context and Problem Statement

Second context.

### Decision Drivers

- Driver 2

### Considered Options

- Option B

### Decision Outcome

Chosen B.

### Related Design Elements

- `fdd-app-req-second`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "PASS")

    def test_multiple_adrs_some_invalid_fails(self):
        """Test that if some ADRs are invalid, validation fails."""
        text = """# ADR Index

## ADR-0001: Valid ADR

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`

## ADR-0002: Invalid ADR - Missing Date

**Status**: Accepted

**ID**: `fdd-app-adr-0002`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        # ADR-0002 should have issues
        adr_0002_issues = [i for i in report["adr_issues"]
                          if i.get("adr") == "ADR-0002"]
        self.assertGreater(len(adr_0002_issues), 0)


class TestADRPlaceholders(unittest.TestCase):
    """Test placeholder detection in ADR.md."""

    def test_placeholders_detected(self):
        """Test that placeholders cause validation failure."""
        text = """# ADR Index

## ADR-0001: Test Decision

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

TODO: Add context

### Decision Drivers

TBD: List drivers

### Considered Options

FIXME: Add options

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        self.assertGreater(len(report["placeholder_hits"]), 0)


class TestADRFileSystemChecks(unittest.TestCase):
    """Test ADR validation with file system checks."""

    def test_missing_business_file_adds_error(self):
        """Test that missing BUSINESS.md file adds cross-reference error."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            arch = tmppath / "architecture"
            arch.mkdir()
            
            # Create ADR.md but no BUSINESS.md
            adr = arch / "ADR.md"
            adr_text = """# ADR Index

## ADR-0001: Test

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`
"""
            adr.write_text(adr_text)
            
            report = validate_adr(
                adr_text,
                artifact_path=adr,
                skip_fs_checks=False
            )
            
            # Should have cross-reference error for missing BUSINESS.md
            cross_errors = [e for e in report["errors"] if e.get("type") == "cross"]
            self.assertGreater(len(cross_errors), 0)

    def test_missing_design_file_adds_error(self):
        """Test that missing DESIGN.md file adds cross-reference error."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            arch = tmppath / "architecture"
            arch.mkdir()
            
            # Create ADR.md and BUSINESS.md but no DESIGN.md
            business = arch / "BUSINESS.md"
            business.write_text("# Business Context\n\n## B. Actors\n\n- **ID**: `fdd-app-actor-user`")
            
            adr = arch / "ADR.md"
            adr_text = """# ADR Index

## ADR-0001: Test

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-actor-user`
"""
            adr.write_text(adr_text)
            
            report = validate_adr(
                adr_text,
                artifact_path=adr,
                skip_fs_checks=False
            )
            
            # Should have cross-reference error for missing DESIGN.md
            cross_errors = [e for e in report["errors"] if e.get("type") == "cross"]
            self.assertGreater(len(cross_errors), 0)

    def test_unknown_capability_reference_fails(self):
        """Test that unknown capability in Related Elements fails."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            arch = tmppath / "architecture"
            arch.mkdir()
            
            business = arch / "BUSINESS.md"
            business.write_text("""# Business Context

## B. Actors

- **ID**: `fdd-app-actor-user`

## C. Capabilities

### CAP-001: Real Capability

**ID**: `fdd-app-capability-real`

**Actors**: `fdd-app-actor-user`
""")
            
            design = arch / "DESIGN.md"
            design.write_text("""# Technical Design

## B. Requirements

### FR-001: Test

**ID**: `fdd-app-req-test`
""")
            
            adr = arch / "ADR.md"
            adr_text = """# ADR Index

## ADR-0001: Test

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- Supports: `fdd-app-capability-unknown`
"""
            adr.write_text(adr_text)
            
            report = validate_adr(
                adr_text,
                artifact_path=adr,
                business_path=business,
                design_path=design,
                skip_fs_checks=False
            )
            
            self.assertEqual(report["status"], "FAIL")
            unknown_cap = [i for i in report["adr_issues"]
                          if "Unknown capability" in i.get("message", "")]
            self.assertGreater(len(unknown_cap), 0)

    def test_unknown_requirement_reference_fails(self):
        """Test that unknown requirement in Related Elements fails."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            arch = tmppath / "architecture"
            arch.mkdir()
            
            business = arch / "BUSINESS.md"
            business.write_text("# Business Context\n\n## B. Actors\n\n- **ID**: `fdd-app-actor-user`")
            
            design = arch / "DESIGN.md"
            design.write_text("""# Technical Design

## B. Requirements

### FR-001: Real Requirement

**ID**: `fdd-app-req-real`
""")
            
            adr = arch / "ADR.md"
            adr_text = """# ADR Index

## ADR-0001: Test

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- Implements: `fdd-app-req-unknown`
"""
            adr.write_text(adr_text)
            
            report = validate_adr(
                adr_text,
                artifact_path=adr,
                business_path=business,
                design_path=design,
                skip_fs_checks=False
            )
            
            self.assertEqual(report["status"], "FAIL")
            unknown_req = [i for i in report["adr_issues"]
                          if "Unknown requirement" in i.get("message", "")]
            self.assertGreater(len(unknown_req), 0)

    def test_unknown_principle_reference_fails(self):
        """Test that unknown principle in Related Elements fails."""
        with TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            arch = tmppath / "architecture"
            arch.mkdir()
            
            business = arch / "BUSINESS.md"
            business.write_text("# Business Context\n\n## B. Actors\n\n- **ID**: `fdd-app-actor-user`")
            
            design = arch / "DESIGN.md"
            design.write_text("""# Technical Design

## B. Requirements

**ID**: `fdd-app-principle-real`

Real principle.
""")
            
            adr = arch / "ADR.md"
            adr_text = """# ADR Index

## ADR-0001: Test

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- Supports: `fdd-app-principle-unknown`
"""
            adr.write_text(adr_text)
            
            report = validate_adr(
                adr_text,
                artifact_path=adr,
                business_path=business,
                design_path=design,
                skip_fs_checks=False
            )
            
            self.assertEqual(report["status"], "FAIL")
            unknown_principle = [i for i in report["adr_issues"]
                                if "Unknown principle" in i.get("message", "")]
            self.assertGreater(len(unknown_principle), 0)


class TestADRDateValidation(unittest.TestCase):
    """Test ADR date validation."""

    def test_adr_with_valid_date_passes(self):
        """Test ADR with properly formatted date."""
        text = """# ADR Index

## ADR-0001: Test Decision

**Date**: 2024-01-15

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context here.

### Decision Drivers

Drivers here.

### Considered Options

Options here.

### Decision Outcome

Outcome here.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        date_issues = [i for i in report["adr_issues"] if "Date" in i.get("message", "")]
        self.assertEqual(len(date_issues), 0)

    def test_adr_missing_date_fails(self):
        """Test ADR without Date field fails."""
        text = """# ADR Index

## ADR-0001: Test Decision

**Status**: Accepted

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        self.assertEqual(report["status"], "FAIL")
        date_issues = [i for i in report["adr_issues"] if "Date" in i.get("message", "")]
        self.assertGreater(len(date_issues), 0)


class TestADRStatusValidation(unittest.TestCase):
    """Test ADR status validation."""

    def test_adr_with_proposed_status(self):
        """Test ADR with Proposed status."""
        text = """# ADR Index

## ADR-0001: Test

**Date**: 2024-01-15

**Status**: Proposed

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        status_issues = [i for i in report["adr_issues"] if "Status" in i.get("message", "")]
        self.assertEqual(len(status_issues), 0)

    def test_adr_with_deprecated_status(self):
        """Test ADR with Deprecated status."""
        text = """# ADR Index

## ADR-0001: Test

**Date**: 2024-01-15

**Status**: Deprecated

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        status_issues = [i for i in report["adr_issues"] if "Status" in i.get("message", "")]
        self.assertEqual(len(status_issues), 0)

    def test_adr_with_superseded_status(self):
        """Test ADR with Superseded status."""
        text = """# ADR Index

## ADR-0001: Test

**Date**: 2024-01-15

**Status**: Superseded

**ID**: `fdd-app-adr-0001`

### Context and Problem Statement

Context.

### Decision Drivers

Drivers.

### Considered Options

Options.

### Decision Outcome

Outcome.

### Related Design Elements

- `fdd-app-req-test`
"""
        report = validate_adr(text, skip_fs_checks=True)
        
        status_issues = [i for i in report["adr_issues"] if "Status" in i.get("message", "")]
        self.assertEqual(len(status_issues), 0)


if __name__ == "__main__":
    unittest.main()
