"""
FDD Validator - ADR.md Validation

Validates architectural decision records.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ...constants import (
    ADR_HEADING_RE,
    ADR_DATE_RE,
    ADR_STATUS_RE,
    ADR_ID_RE,
    ADR_NUM_RE,
    ACTOR_ID_RE,
    CAPABILITY_ID_RE,
    REQ_ID_RE,
    PRINCIPLE_ID_RE,
)

from ...utils import (
    find_placeholders,
    parse_adr_index,
    load_text,
    field_block,
    has_list_item,
)


__all__ = ["validate_adr"]
def validate_adr(
    artifact_text: str,
    *,
    artifact_path: Optional[Path] = None,
    business_path: Optional[Path] = None,
    design_path: Optional[Path] = None,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    errors: List[Dict[str, object]] = []
    placeholders = find_placeholders(artifact_text)

    adr_entries, issues = parse_adr_index(artifact_text)
    errors.extend(issues)

    business_actors: set = set()
    business_caps: set = set()
    design_req: set = set()
    design_principle: set = set()

    if not skip_fs_checks and artifact_path is not None:
        bp = business_path or (artifact_path.parent / "BUSINESS.md")
        dp = design_path or (artifact_path.parent / "DESIGN.md")

        bt, berr = load_text(bp)
        if berr:
            errors.append({"type": "cross", "message": berr})
        else:
            business_actors = set(ACTOR_ID_RE.findall(bt or ""))
            business_caps = set(CAPABILITY_ID_RE.findall(bt or ""))

        dt, derr = load_text(dp)
        if derr:
            errors.append({"type": "cross", "message": derr})
        else:
            design_req = set(REQ_ID_RE.findall(dt or ""))
            design_principle = set(PRINCIPLE_ID_RE.findall(dt or ""))

    lines = artifact_text.splitlines()
    current_adr: Optional[str] = None
    current_block: List[str] = []
    per_adr_issues: List[Dict[str, object]] = []

    def flush():
        nonlocal current_adr, current_block
        if current_adr is None:
            return
        block_text = "\n".join(current_block)

        if ADR_DATE_RE.search(block_text) is None:
            per_adr_issues.append({"adr": current_adr, "message": "Missing **Date**: YYYY-MM-DD"})
        if ADR_STATUS_RE.search(block_text) is None:
            per_adr_issues.append({"adr": current_adr, "message": "Missing or invalid **Status**"})

        required_sections = [
            "### Context and Problem Statement",
            "### Decision Drivers",
            "### Considered Options",
            "### Decision Outcome",
            "### Related Design Elements",
        ]
        for sec in required_sections:
            if sec not in block_text:
                per_adr_issues.append({"adr": current_adr, "message": f"Missing section: {sec}"})

        if "### Related Design Elements" in block_text:
            related_text = block_text.split("### Related Design Elements", 1)[1]
            referenced = set(ACTOR_ID_RE.findall(related_text)) | set(CAPABILITY_ID_RE.findall(related_text)) | set(REQ_ID_RE.findall(related_text)) | set(PRINCIPLE_ID_RE.findall(related_text))
            if not referenced:
                per_adr_issues.append({"adr": current_adr, "message": "Related Design Elements must contain at least one ID"})
            if business_actors:
                bad = sorted([x for x in ACTOR_ID_RE.findall(related_text) if x not in business_actors])
                if bad:
                    per_adr_issues.append({"adr": current_adr, "message": "Unknown actor IDs in Related Design Elements", "ids": bad})
            if business_caps:
                bad = sorted([x for x in CAPABILITY_ID_RE.findall(related_text) if x not in business_caps])
                if bad:
                    per_adr_issues.append({"adr": current_adr, "message": "Unknown capability IDs in Related Design Elements", "ids": bad})
            if design_req:
                bad = sorted([x for x in REQ_ID_RE.findall(related_text) if x not in design_req])
                if bad:
                    per_adr_issues.append({"adr": current_adr, "message": "Unknown requirement IDs in Related Design Elements", "ids": bad})
            if design_principle:
                bad = sorted([x for x in PRINCIPLE_ID_RE.findall(related_text) if x not in design_principle])
                if bad:
                    per_adr_issues.append({"adr": current_adr, "message": "Unknown principle IDs in Related Design Elements", "ids": bad})

        current_adr = None
        current_block = []

    for line in lines:
        m = ADR_HEADING_RE.match(line.strip())
        if m:
            flush()
            current_adr = m.group(1)
            current_block = []
            continue
        if current_adr is not None:
            current_block.append(line)
    flush()

    passed = (len(errors) == 0) and (len(per_adr_issues) == 0) and (len(placeholders) == 0)
    return {
        "required_section_count": 5,
        "missing_sections": [],
        "placeholder_hits": placeholders,
        "status": "PASS" if passed else "FAIL",
        "errors": errors,
        "adr_issues": per_adr_issues,
        "adr_count": len(adr_entries),
    }


FIELD_HEADER_RE = re.compile(r"^\s*[-*]?\s*\*\*([^*]+)\*\*:\s*(.*)$")

KNOWN_FIELD_NAMES = {
    "Purpose",
    "Target Users",
    "Key Problems Solved",
    "Success Criteria",
    "Actor",
    "Actors",
    "Role",
    "Preconditions",
    "Flow",
    "Postconditions",
    "Status",
    "Depends On",
    "Blocks",
    "Scope",
    "Requirements Covered",
    "Principles Covered",
    "Constraints Affected",
    "Phases",
    "References",
    "Implements",
    "ADRs",
    "Capabilities",
    "Technology",
    "Location",
    "Input",
    "Output",
    "Testing Scenarios",
    "Testing Scenarios (FDL)",
    "Acceptance Criteria",
}
