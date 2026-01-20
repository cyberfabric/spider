"""
FDD Validator - Cascading Validation

Handles artifact dependency resolution and cascading validation.
Artifact dependency graph:
  - feature-changes -> feature-design -> features-manifest -> overall-design -> (business-context, adr)
  - feature-design -> features-manifest -> overall-design -> (business-context, adr)
  - features-manifest -> overall-design -> (business-context, adr)
  - overall-design -> (business-context, adr)
  - adr -> business-context
  - business-context -> (none)
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ..utils import detect_requirements, load_text


# Artifact dependency graph: artifact_kind -> list of dependency kinds
ARTIFACT_DEPENDENCIES: Dict[str, List[str]] = {
    "feature-changes": ["feature-design"],
    "feature-design": ["features-manifest", "overall-design"],
    "features-manifest": ["overall-design"],
    "overall-design": ["business-context", "adr"],
    "adr": ["business-context"],
    "business-context": [],
}


def find_artifact_path(artifact_kind: str, from_path: Path) -> Optional[Path]:
    """
    Find artifact path by kind, searching from the given path upward.
    
    Returns None if not found.
    """
    if artifact_kind == "feature-design":
        # Look in same directory as CHANGES.md
        candidate = from_path.parent / "DESIGN.md"
        if candidate.exists() and candidate.is_file():
            return candidate
        return None
    
    if artifact_kind == "features-manifest":
        # Look for architecture/features/FEATURES.md
        for parent in from_path.parents:
            candidate = parent / "architecture" / "features" / "FEATURES.md"
            if candidate.exists() and candidate.is_file():
                return candidate
        return None
    
    if artifact_kind == "overall-design":
        # Look for architecture/DESIGN.md
        for parent in from_path.parents:
            candidate = parent / "architecture" / "DESIGN.md"
            if candidate.exists() and candidate.is_file():
                return candidate
        return None
    
    if artifact_kind == "business-context":
        # Look for architecture/BUSINESS.md
        for parent in from_path.parents:
            candidate = parent / "architecture" / "BUSINESS.md"
            if candidate.exists() and candidate.is_file():
                return candidate
        return None
    
    if artifact_kind == "adr":
        # Look for architecture/ADR.md
        for parent in from_path.parents:
            candidate = parent / "architecture" / "ADR.md"
            if candidate.exists() and candidate.is_file():
                return candidate
        return None
    
    return None


def resolve_dependencies(
    artifact_kind: str,
    artifact_path: Path,
    *,
    resolved: Optional[Dict[str, Path]] = None,
) -> Dict[str, Path]:
    """
    Resolve all dependencies for an artifact recursively.
    
    Returns dict mapping artifact_kind -> path for all dependencies.
    """
    if resolved is None:
        resolved = {}
    
    deps = ARTIFACT_DEPENDENCIES.get(artifact_kind, [])
    
    for dep_kind in deps:
        if dep_kind in resolved:
            continue
        
        dep_path = find_artifact_path(dep_kind, artifact_path)
        if dep_path:
            resolved[dep_kind] = dep_path
            # Recursively resolve dependencies of this dependency
            resolve_dependencies(dep_kind, dep_path, resolved=resolved)
    
    return resolved


def validate_with_dependencies(
    artifact_path: Path,
    *,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    """
    Validate an artifact along with all its dependencies.
    
    Automatically discovers and validates all dependent artifacts.
    Returns a comprehensive report with main validation and dependency validations.
    """
    from . import validate
    
    # Detect artifact kind and requirements
    artifact_kind, requirements_path = detect_requirements(artifact_path)
    
    # Resolve all dependencies
    dependencies = resolve_dependencies(artifact_kind, artifact_path)
    
    # Validate dependencies first (bottom-up: business/adr -> overall -> features -> feature)
    dependency_reports: Dict[str, Dict[str, object]] = {}
    overall_status = "PASS"
    
    # Define validation order (dependencies first)
    validation_order = ["business-context", "adr", "overall-design", "features-manifest", "feature-design"]
    
    for dep_kind in validation_order:
        if dep_kind not in dependencies:
            continue
        
        dep_path = dependencies[dep_kind]
        dep_artifact_kind, dep_requirements = detect_requirements(dep_path)
        
        # Get paths for cross-reference validation
        design_path = dependencies.get("overall-design")
        business_path = dependencies.get("business-context")
        adr_path = dependencies.get("adr")
        
        dep_report = validate(
            dep_path,
            dep_requirements,
            dep_artifact_kind,
            design_path=design_path,
            business_path=business_path,
            adr_path=adr_path,
            skip_fs_checks=skip_fs_checks,
        )
        dep_report["artifact_kind"] = dep_artifact_kind
        dep_report["path"] = str(dep_path)
        dependency_reports[dep_kind] = dep_report
        
        if dep_report.get("status") != "PASS":
            overall_status = "FAIL"
    
    # Validate the main artifact
    design_path = dependencies.get("overall-design")
    business_path = dependencies.get("business-context")
    adr_path = dependencies.get("adr")
    
    report = validate(
        artifact_path,
        requirements_path,
        artifact_kind,
        design_path=design_path,
        business_path=business_path,
        adr_path=adr_path,
        skip_fs_checks=skip_fs_checks,
    )
    report["artifact_kind"] = artifact_kind
    
    # Include dependency validation results
    if dependency_reports:
        report["dependency_validation"] = dependency_reports
        if overall_status == "FAIL" and report.get("status") == "PASS":
            report["status"] = "FAIL"
            if "errors" not in report:
                report["errors"] = []
            report["errors"].append({
                "type": "dependency",
                "message": "One or more dependencies failed validation",
            })
    
    return report


def validate_all_artifacts(
    code_root: Path,
    *,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    """
    Validate all FDD artifacts in a codebase.
    
    Discovers and validates:
    - architecture/BUSINESS.md
    - architecture/ADR.md
    - architecture/DESIGN.md
    - architecture/features/FEATURES.md
    - All feature DESIGN.md and CHANGES.md
    
    Returns a comprehensive report with all artifact validations.
    """
    from . import validate
    
    artifact_reports: Dict[str, Dict[str, object]] = {}
    overall_status = "PASS"
    
    arch_dir = code_root / "architecture"
    
    # Validate core artifacts in order (dependencies first)
    core_artifacts = [
        ("business-context", arch_dir / "BUSINESS.md"),
        ("adr", arch_dir / "ADR.md"),
        ("overall-design", arch_dir / "DESIGN.md"),
        ("features-manifest", arch_dir / "features" / "FEATURES.md"),
    ]
    
    for artifact_kind, artifact_path in core_artifacts:
        if not artifact_path.exists():
            continue
        
        # Get dependency paths for cross-reference validation
        business_path = arch_dir / "BUSINESS.md" if (arch_dir / "BUSINESS.md").exists() else None
        adr_path = arch_dir / "ADR.md" if (arch_dir / "ADR.md").exists() else None
        design_path = arch_dir / "DESIGN.md" if (arch_dir / "DESIGN.md").exists() else None
        
        ak, ar = detect_requirements(artifact_path)
        report = validate(
            artifact_path,
            ar,
            ak,
            design_path=design_path if artifact_kind != "overall-design" else None,
            business_path=business_path if artifact_kind not in ("business-context",) else None,
            adr_path=adr_path if artifact_kind not in ("adr", "business-context") else None,
            skip_fs_checks=skip_fs_checks,
        )
        report["artifact_kind"] = ak
        report["path"] = str(artifact_path)
        artifact_reports[artifact_kind] = report
        
        if report.get("status") != "PASS":
            overall_status = "FAIL"
    
    # Validate all feature artifacts
    features_dir = arch_dir / "features"
    if features_dir.exists():
        for feature_dir in sorted(features_dir.iterdir()):
            if not feature_dir.is_dir() or feature_dir.name.startswith("."):
                continue
            
            feature_slug = feature_dir.name
            
            # Validate feature DESIGN.md
            feature_design = feature_dir / "DESIGN.md"
            if feature_design.exists():
                fk, fr = detect_requirements(feature_design)
                report = validate(
                    feature_design,
                    fr,
                    fk,
                    design_path=arch_dir / "DESIGN.md" if (arch_dir / "DESIGN.md").exists() else None,
                    business_path=arch_dir / "BUSINESS.md" if (arch_dir / "BUSINESS.md").exists() else None,
                    adr_path=arch_dir / "ADR.md" if (arch_dir / "ADR.md").exists() else None,
                    skip_fs_checks=skip_fs_checks,
                )
                report["artifact_kind"] = fk
                report["path"] = str(feature_design)
                artifact_reports[f"feature-design:{feature_slug}"] = report
                
                if report.get("status") != "PASS":
                    overall_status = "FAIL"
            
            # Validate feature CHANGES.md
            feature_changes = feature_dir / "CHANGES.md"
            if feature_changes.exists():
                ck, cr = detect_requirements(feature_changes)
                report = validate(
                    feature_changes,
                    cr,
                    ck,
                    design_path=feature_design if feature_design.exists() else None,
                    skip_fs_checks=skip_fs_checks,
                )
                report["artifact_kind"] = ck
                report["path"] = str(feature_changes)
                artifact_reports[f"feature-changes:{feature_slug}"] = report
                
                if report.get("status") != "PASS":
                    overall_status = "FAIL"
    
    return {
        "status": overall_status,
        "artifact_validation": artifact_reports,
    }


__all__ = [
    "ARTIFACT_DEPENDENCIES",
    "find_artifact_path",
    "resolve_dependencies",
    "validate_with_dependencies",
    "validate_all_artifacts",
]
