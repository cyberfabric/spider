"""Tests for cascading validation module."""

import tempfile
import unittest
from pathlib import Path

from skills.fdd.scripts.fdd.validation.cascade import (
    ARTIFACT_DEPENDENCIES,
    find_artifact_path,
    resolve_dependencies,
    validate_with_dependencies,
)


class TestArtifactDependencies(unittest.TestCase):
    """Test artifact dependency graph."""

    def test_dependency_graph_structure(self):
        """Verify dependency graph has expected structure."""
        self.assertEqual(ARTIFACT_DEPENDENCIES["feature-changes"], ["feature-design"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["feature-design"], ["features-manifest", "overall-design"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["features-manifest"], ["overall-design"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["overall-design"], ["business-context", "adr"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["adr"], ["business-context"])
        self.assertEqual(ARTIFACT_DEPENDENCIES["business-context"], [])

    def test_unknown_artifact_has_no_dependencies(self):
        """Unknown artifact kind returns empty list."""
        self.assertEqual(ARTIFACT_DEPENDENCIES.get("unknown", []), [])


class TestFindArtifactPath(unittest.TestCase):
    """Test artifact path discovery."""

    def test_find_feature_design_exists(self):
        """Find DESIGN.md in same directory as CHANGES.md."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            changes = tmp_path / "CHANGES.md"
            design = tmp_path / "DESIGN.md"
            changes.write_text("# Changes")
            design.write_text("# Design")
            
            result = find_artifact_path("feature-design", changes)
            self.assertEqual(result, design)

    def test_find_feature_design_not_exists(self):
        """Return None if DESIGN.md not found."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            changes = tmp_path / "CHANGES.md"
            changes.write_text("# Changes")
            
            result = find_artifact_path("feature-design", changes)
            self.assertIsNone(result)

    def test_find_features_manifest_exists(self):
        """Find FEATURES.md in architecture/features/."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch_features = tmp_path / "architecture" / "features"
            arch_features.mkdir(parents=True)
            features = arch_features / "FEATURES.md"
            features.write_text("# Features")
            artifact = tmp_path / "some" / "path" / "artifact.md"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("features-manifest", artifact)
            self.assertEqual(result, features)

    def test_find_features_manifest_not_exists(self):
        """Return None if FEATURES.md not found."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact = tmp_path / "artifact.md"
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("features-manifest", artifact)
            self.assertIsNone(result)

    def test_find_overall_design_exists(self):
        """Find DESIGN.md in architecture/."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            design = arch / "DESIGN.md"
            design.write_text("# Design")
            artifact = tmp_path / "some" / "path" / "artifact.md"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("overall-design", artifact)
            self.assertEqual(result, design)

    def test_find_overall_design_not_exists(self):
        """Return None if overall DESIGN.md not found."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact = tmp_path / "artifact.md"
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("overall-design", artifact)
            self.assertIsNone(result)

    def test_find_business_context_exists(self):
        """Find BUSINESS.md in architecture/."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            business = arch / "BUSINESS.md"
            business.write_text("# Business")
            artifact = tmp_path / "some" / "path" / "artifact.md"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("business-context", artifact)
            self.assertEqual(result, business)

    def test_find_business_context_not_exists(self):
        """Return None if BUSINESS.md not found."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact = tmp_path / "artifact.md"
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("business-context", artifact)
            self.assertIsNone(result)

    def test_find_adr_exists(self):
        """Find ADR.md in architecture/."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            adr = arch / "ADR.md"
            adr.write_text("# ADR")
            artifact = tmp_path / "some" / "path" / "artifact.md"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("adr", artifact)
            self.assertEqual(result, adr)

    def test_find_adr_not_exists(self):
        """Return None if ADR.md not found."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact = tmp_path / "artifact.md"
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("adr", artifact)
            self.assertIsNone(result)

    def test_find_unknown_artifact_kind(self):
        """Return None for unknown artifact kind."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact = tmp_path / "artifact.md"
            artifact.write_text("# Artifact")
            
            result = find_artifact_path("unknown-kind", artifact)
            self.assertIsNone(result)


class TestResolveDependencies(unittest.TestCase):
    """Test dependency resolution."""

    def test_resolve_no_dependencies(self):
        """business-context has no dependencies."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            business = tmp_path / "BUSINESS.md"
            business.write_text("# Business")
            
            result = resolve_dependencies("business-context", business)
            self.assertEqual(result, {})

    def test_resolve_adr_depends_on_business(self):
        """ADR depends on business-context."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            adr = arch / "ADR.md"
            business = arch / "BUSINESS.md"
            adr.write_text("# ADR")
            business.write_text("# Business")
            
            result = resolve_dependencies("adr", adr)
            self.assertIn("business-context", result)
            self.assertEqual(result["business-context"], business)

    def test_resolve_overall_design_full_chain(self):
        """overall-design depends on business-context and adr."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            design = arch / "DESIGN.md"
            business = arch / "BUSINESS.md"
            adr = arch / "ADR.md"
            design.write_text("# Design")
            business.write_text("# Business")
            adr.write_text("# ADR")
            
            result = resolve_dependencies("overall-design", design)
            self.assertIn("business-context", result)
            self.assertIn("adr", result)

    def test_resolve_already_resolved_skipped(self):
        """Dependencies already resolved are skipped."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            design = arch / "DESIGN.md"
            business = arch / "BUSINESS.md"
            design.write_text("# Design")
            business.write_text("# Business")
            
            # Pre-populate resolved
            existing = {"business-context": business}
            result = resolve_dependencies("overall-design", design, resolved=existing)
            # Should still have business-context from pre-populated
            self.assertIn("business-context", result)


class TestValidateWithDependencies(unittest.TestCase):
    """Test cascading validation."""

    def test_validate_business_context_no_deps(self):
        """Validate business-context with no dependencies."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            business = tmp_path / "BUSINESS.md"
            business.write_text("""---
fdd: true
type: business-context
name: Test Business
version: "1.0"
purpose: Test
---

# FDD: Test Business Context

## Overview

Test overview.

## Actors

### Actor: Test Actor

**ID**: `fdd-test-actor-user`

**Description**: Test user actor.

## Capabilities

### Capability: Test Capability

**ID**: `fdd-test-capability-main`

Provided by `fdd-test-actor-user`.

## Use Cases

None yet.
""")
            
            report = validate_with_dependencies(business, skip_fs_checks=True)
            self.assertEqual(report["artifact_kind"], "business-context")
            self.assertNotIn("dependency_validation", report)

    def test_validate_with_failing_dependency(self):
        """Validation fails if dependency fails."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            arch = tmp_path / "architecture"
            arch.mkdir()
            
            # Create invalid BUSINESS.md (missing required content)
            business = arch / "BUSINESS.md"
            business.write_text("# Empty Business")
            
            # Create ADR that depends on business
            adr = arch / "ADR.md"
            adr.write_text("""---
fdd: true
type: adr
name: Test ADR
version: "1.0"
purpose: Test
---

# FDD: Test ADR

## Overview

Test overview.

## ADR Index

None.

## Superseded ADRs

None.
""")
            
            report = validate_with_dependencies(adr, skip_fs_checks=True)
            # ADR validation should fail due to failing business dependency
            self.assertIn("dependency_validation", report)
            self.assertIn("business-context", report["dependency_validation"])


if __name__ == "__main__":
    unittest.main()
