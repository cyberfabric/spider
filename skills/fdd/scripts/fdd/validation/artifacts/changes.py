"""
FDD Validator - Feature CHANGES.md Validation

Validates implementation plans: structure, change entries, dependencies, FDL coverage.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ...constants import (
    CHANGES_HEADER_TITLE_RE,
    CHANGE_HEADING_RE,
    CHANGE_ID_RE,
    CHANGE_STATUS_RE,
    CHANGE_PRIORITY_RE,
    PHASE_TOKEN_RE,
    CHANGE_TASK_LINE_RE,
    FEATURE_REQ_ID_RE,
    LINK_RE,
)

from ...utils import find_placeholders, load_text

# Import FDL validation
from ..fdl import (
    extract_fdl_instructions,
    validate_fdl_coverage,
    extract_scope_references_from_changes,
)


__all__ = ["validate_feature_changes"]
def validate_feature_changes(
    artifact_text: str,
    *,
    artifact_path: Optional[Path] = None,
    skip_fs_checks: bool = False,
) -> Dict[str, object]:
    errors: List[Dict[str, object]] = []
    placeholders = find_placeholders(artifact_text)

    feature_slug: Optional[str] = None
    feature_root: Optional[Path] = None
    if artifact_path is not None:
        if artifact_path.parent.name == "archive" and artifact_path.parent.parent.name.startswith("feature-"):
            feature_root = artifact_path.parent.parent
        elif artifact_path.parent.name.startswith("feature-"):
            feature_root = artifact_path.parent
        else:
            feature_root = artifact_path.parent

        if feature_root.name.startswith("feature-"):
            feature_slug = feature_root.name[len("feature-") :]

    lines = artifact_text.splitlines()
    if not lines or not CHANGES_HEADER_TITLE_RE.match(lines[0].strip()):
        errors.append({"type": "header", "message": "Missing or invalid title '# Implementation Plan: {Feature Name}'", "line": 1})

    header_text = "\n".join(lines[:160])

    m_feature = re.search(r"\*\*Feature\*\*:\s*`([^`]+)`", header_text)
    if not m_feature:
        errors.append({"type": "header", "message": "Missing **Feature**: `{feature-slug}`"})
    else:
        header_slug = m_feature.group(1).strip()
        if feature_slug is not None and header_slug != feature_slug:
            errors.append({"type": "header", "message": "Header **Feature** slug must match directory slug", "expected": feature_slug, "found": header_slug})

    if not re.search(r"\*\*Version\*\*:\s*\S+", header_text):
        errors.append({"type": "header", "message": "Missing **Version**"})

    if not re.search(r"\*\*Last Updated\*\*:\s*\d{4}-\d{2}-\d{2}", header_text):
        errors.append({"type": "header", "message": "Missing or invalid **Last Updated** date", "expected": "YYYY-MM-DD"})

    m_status = re.search(r"\*\*Status\*\*:\s*(.+)$", header_text, re.MULTILINE)
    if not m_status:
        errors.append({"type": "header", "message": "Missing **Status**"})
    else:
        s = m_status.group(1).strip()
        if not CHANGE_STATUS_RE.match(s):
            errors.append({"type": "header", "message": "Invalid overall **Status**", "status": s})

    if not re.search(r"\*\*Feature DESIGN\*\*:\s*\[[^\]]+\]\((?:\.\./)?DESIGN\.md\)", header_text):
        errors.append({"type": "header", "message": "Missing or invalid **Feature DESIGN** link (must point to DESIGN.md)"})

    summary_counts: Optional[Dict[str, int]] = None
    if "## Summary" not in artifact_text:
        errors.append({"type": "structure", "message": "Missing ## Summary section"})
    else:
        m_total = re.search(r"\*\*Total Changes\*\*:\s*(\d+)", artifact_text)
        m_completed = re.search(r"\*\*Completed\*\*:\s*(\d+)", artifact_text)
        m_in_progress = re.search(r"\*\*In Progress\*\*:\s*(\d+)", artifact_text)
        m_not_started = re.search(r"\*\*Not Started\*\*:\s*(\d+)", artifact_text)
        m_effort = re.search(r"\*\*Estimated Effort\*\*:\s*.+", artifact_text)
        if not (m_total and m_completed and m_in_progress and m_not_started):
            errors.append({"type": "structure", "message": "Summary must include Total/Completed/In Progress/Not Started counts"})
        if not m_effort:
            errors.append({"type": "structure", "message": "Summary must include **Estimated Effort**"})
        else:
            total = int(m_total.group(1))
            completed = int(m_completed.group(1))
            in_progress = int(m_in_progress.group(1))
            not_started = int(m_not_started.group(1))
            if total != (completed + in_progress + not_started):
                errors.append({"type": "structure", "message": "Summary counts do not add up", "total": total, "sum": completed + in_progress + not_started})
            summary_counts = {"total": total, "completed": completed, "in_progress": in_progress, "not_started": not_started}

    change_starts: List[int] = []
    change_nums: List[int] = []
    for i, line in enumerate(lines):
        m = CHANGE_HEADING_RE.match(line.strip())
        if not m:
            continue
        change_starts.append(i)
        change_nums.append(int(m.group(1)))

    if not change_starts:
        errors.append({"type": "structure", "message": "No change entries found (expected '## Change 1: ...')"})
        change_blocks: List[Tuple[int, int, int, List[str]]] = []
    else:
        expected = list(range(1, len(change_nums) + 1))
        if change_nums != expected:
            errors.append({"type": "structure", "message": "Change entries must be numbered sequentially", "expected": expected, "found": change_nums})

        change_blocks = []
        for idx, start in enumerate(change_starts):
            end = change_starts[idx + 1] if idx + 1 < len(change_starts) else len(lines)
            change_blocks.append((change_nums[idx], start, end, lines[start:end]))

    def _get_field_value(block_lines: List[str], field: str) -> Optional[str]:
        pat = re.compile(rf"^\*\*{re.escape(field)}\*\*:\s*(.+?)\s*$")
        for l in block_lines:
            m = pat.match(l.strip())
            if m:
                return m.group(1).strip()
        return None

    def _subsection_bounds(block_lines: List[str], title: str) -> Optional[Tuple[int, int]]:
        start = None
        for i, l in enumerate(block_lines):
            if l.strip() == title:
                start = i
                break
        if start is None:
            return None
        end = len(block_lines)
        for j in range(start + 1, len(block_lines)):
            if block_lines[j].strip().startswith("### "):
                end = j
                break
        return start, end

    def _count_list_items(lines: List[str]) -> int:
        return sum(1 for l in lines if re.match(r"^\s*[-*]\s+\S+", l))

    def _task_has_affected_path(desc: str) -> bool:
        # Accept any backticked filename/path/pattern (excluding fdd-* IDs), e.g.:
        # - `src/lib.rs`
        # - `Makefile`
        # - `requirements/`
        # - `*-structure.md`
        # Reject: `fdd-...` IDs
        toks = [t.strip() for t in re.findall(r"`([^`]+)`", desc) if t.strip()]
        for tok in toks:
            if tok.startswith("fdd-"):
                continue
            if "/" in tok:
                return True
            if tok.endswith("/"):
                return True
            if "." in tok:
                return True
            if "*" in tok and "." in tok:
                return True
            if tok in {"Makefile", "Dockerfile", "LICENSE"}:
                return True
        return False

    def _task_is_allowed_pathless(desc: str) -> bool:
        s = desc.strip().lower()
        if "validate:" not in s:
            return False
        if "fdd" in s and "tag" in s:
            return True
        if s.startswith("verify "):
            return True
        if s.startswith("run "):
            return True
        return False

    change_ids: List[str] = []
    implements_by_change: Dict[int, List[str]] = {}
    phases_by_change: Dict[int, List[int]] = {}
    deps: Dict[int, List[int]] = {}

    for n, start, _, block in change_blocks:
        block_text = "\n".join(block)

        cid_val = _get_field_value(block, "ID")
        cid: Optional[str] = None
        if cid_val is None:
            errors.append({"type": "id", "message": "Change missing **ID**", "change": n, "line": start + 1})
        else:
            m = re.search(r"`([^`]+)`", cid_val)
            if not m:
                errors.append({"type": "id", "message": "Change **ID** must be wrapped in backticks", "change": n, "line": start + 1})
            else:
                cid = m.group(1).strip()
                change_ids.append(cid)
                m2 = CHANGE_ID_RE.fullmatch(cid)
                if not m2:
                    errors.append({"type": "id", "message": "Invalid change ID format", "change": n, "id": cid})
                elif feature_slug is not None and m2.group(1) != feature_slug:
                    errors.append({"type": "id", "message": "Feature slug in change ID does not match directory slug", "change": n, "expected": feature_slug, "found": m2.group(1)})

        status_val = _get_field_value(block, "Status")
        if status_val is None:
            errors.append({"type": "content", "message": "Change missing **Status**", "change": n})
        elif not CHANGE_STATUS_RE.match(status_val):
            errors.append({"type": "content", "message": "Invalid change **Status**", "change": n, "status": status_val})

        prio_val = _get_field_value(block, "Priority")
        if prio_val is None:
            errors.append({"type": "content", "message": "Change missing **Priority**", "change": n})
        elif not CHANGE_PRIORITY_RE.match(prio_val):
            errors.append({"type": "content", "message": "Invalid change **Priority**", "change": n, "priority": prio_val})

        if _get_field_value(block, "Effort") is None:
            errors.append({"type": "content", "message": "Change missing **Effort**", "change": n})

        impl_val = _get_field_value(block, "Implements")
        impl_ids: List[str] = []
        if impl_val is None:
            errors.append({"type": "content", "message": "Change missing **Implements**", "change": n})
        else:
            impl_ids = [x.strip() for x in re.findall(r"`([^`]+)`", impl_val) if x.strip().startswith("fdd-")]
            if not impl_ids:
                errors.append({"type": "content", "message": "Change **Implements** must include at least one requirement ID", "change": n})
            if len(impl_ids) > 5:
                errors.append({"type": "content", "message": "Change must implement 1-5 requirements", "change": n, "count": len(impl_ids)})
            for rid in impl_ids:
                m_req = FEATURE_REQ_ID_RE.fullmatch(rid)
                if not m_req:
                    errors.append({"type": "id", "message": "Invalid requirement ID in **Implements**", "change": n, "id": rid})
                elif feature_slug is not None and m_req.group(1) != feature_slug:
                    errors.append({"type": "id", "message": "Feature slug in requirement ID does not match directory slug", "change": n, "expected": feature_slug, "found": m_req.group(1), "id": rid})

        phases_val = _get_field_value(block, "Phases")
        phase_nums: List[int] = []
        if phases_val is None:
            errors.append({"type": "content", "message": "Change missing **Phases**", "change": n})
        else:
            phase_nums = [int(x) for x in PHASE_TOKEN_RE.findall(phases_val)]
            if 1 not in phase_nums:
                errors.append({"type": "content", "message": "Change phases must include ph-1", "change": n})
        phases_by_change[n] = sorted(set(phase_nums))
        implements_by_change[n] = impl_ids

        for sub in ("### Objective", "### Requirements Coverage", "### Tasks", "### Specification", "### Dependencies", "### Testing"):
            if sub not in block_text:
                errors.append({"type": "structure", "message": "Missing required subsection in change", "change": n, "subsection": sub})

        tasks: List[Tuple[List[int], str]] = []
        for l in block:
            m_task = CHANGE_TASK_LINE_RE.match(l)
            if not m_task:
                continue
            nums = [int(x) for x in m_task.group(1).split(".")]
            tasks.append((nums, m_task.group(2).strip()))
        if not tasks:
            errors.append({"type": "content", "message": "Change must contain checkbox tasks with hierarchical numbering", "change": n})
        else:
            has_any_path = False
            for _nums, desc in tasks:
                if "validate:" not in desc.lower():
                    errors.append({"type": "content", "message": "Task must include validation criteria (use 'validate: ...')", "change": n, "task": desc})
                if _task_has_affected_path(desc):
                    has_any_path = True
                elif not _task_is_allowed_pathless(desc):
                    errors.append({"type": "content", "message": "Task must specify affected file paths using backticks", "change": n, "task": desc})

            if not has_any_path:
                errors.append({"type": "content", "message": "At least one task must specify an affected file path using backticks", "change": n})

            if len(tasks) > 10:
                errors.append({"type": "content", "message": "No change too large (>10 tasks)", "change": n, "count": len(tasks)})

        # Requirements Coverage section content checks
        rng_rc = _subsection_bounds(block, "### Requirements Coverage")
        if rng_rc is not None:
            rc_lines = block[rng_rc[0] : rng_rc[1]]
            rc_text = "\n".join(rc_lines)
            if "**Implements**:" not in rc_text:
                errors.append({"type": "content", "message": "Requirements Coverage must include **Implements** list", "change": n})
            else:
                covered = set(re.findall(r"`(fdd-[^`]+)`", rc_text))
                missing_cov = sorted([rid for rid in implements_by_change.get(n, []) if rid not in covered])
                if missing_cov:
                    errors.append({"type": "cross", "message": "Requirements Coverage must include entries for all IDs from **Implements**", "change": n, "missing": missing_cov})

            if "**References**:" not in rc_text:
                errors.append({"type": "content", "message": "Requirements Coverage must include **References** list", "change": n})
            else:
                if not re.search(r"\bfdd-[a-z0-9-]+-feature-[a-z0-9-]+-(?:flow|algo|state|td)-[a-z0-9-]+\b", rc_text):
                    errors.append({"type": "content", "message": "References must include at least one flow/algo/state/technical-detail ID", "change": n})

        # Specification section content checks
        rng_spec = _subsection_bounds(block, "### Specification")
        if rng_spec is not None:
            spec_lines = block[rng_spec[0] : rng_spec[1]]
            spec_text = "\n".join(spec_lines)

            required_spec_headers = [
                "**Domain Model Changes**:",
                "**API Changes**:",
                "**Database Changes**:",
                "**Code Changes**:",
            ]
            for h in required_spec_headers:
                if h not in spec_text:
                    errors.append({"type": "content", "message": "Specification must include required section", "change": n, "section": h})

            # Require at least one list item under each spec header when present.
            for i, l in enumerate(spec_lines):
                if l.strip() not in required_spec_headers:
                    continue
                j = i + 1
                bucket: List[str] = []
                while j < len(spec_lines) and not spec_lines[j].strip().startswith("**"):
                    bucket.append(spec_lines[j])
                    j += 1
                if _count_list_items(bucket) == 0:
                    errors.append({"type": "content", "message": "Specification section must include at least one list item", "change": n, "section": l.strip()})

            if "@fdd-change:" not in spec_text:
                errors.append({"type": "content", "message": "Specification must mention code tagging via @fdd-change", "change": n})
            if ":ph-" not in spec_text:
                errors.append({"type": "content", "message": "Specification must mention phase postfix ':ph-' for code tags", "change": n})

        # Dependencies section structure checks
        rng_deps = _subsection_bounds(block, "### Dependencies")
        if rng_deps is not None:
            deps_text = "\n".join(block[rng_deps[0] : rng_deps[1]])
            if "**Depends on**" not in deps_text:
                errors.append({"type": "content", "message": "Dependencies section must include **Depends on**", "change": n})
            if "**Blocks**" not in deps_text:
                errors.append({"type": "content", "message": "Dependencies section must include **Blocks**", "change": n})

        # Testing section structure checks
        rng_test = _subsection_bounds(block, "### Testing")
        if rng_test is not None:
            t_text = "\n".join(block[rng_test[0] : rng_test[1]])
            if "**Unit Tests**" not in t_text and "**Integration Tests**" not in t_text and "**E2E Tests**" not in t_text:
                errors.append({"type": "content", "message": "Testing section must specify Unit/Integration/E2E tests (or explicitly None)", "change": n})

        deps.setdefault(n, [])
        in_deps = False
        in_depends = False
        in_blocks = False
        for l in block:
            if l.strip() == "### Dependencies":
                in_deps = True
                in_depends = False
                in_blocks = False
                continue
            if in_deps and l.strip().startswith("### ") and l.strip() != "### Dependencies":
                break
            if not in_deps:
                continue
            if l.strip().startswith("**Depends on**"):
                in_depends = True
                in_blocks = False
                continue
            if l.strip().startswith("**Blocks**"):
                in_blocks = True
                in_depends = False
                continue
            m_cn = re.match(r"^\s*-\s+Change\s+(\d+):", l.strip())
            if m_cn and in_depends:
                deps[n].append(int(m_cn.group(1)))
            if m_cn and in_blocks:
                deps.setdefault(int(m_cn.group(1)), [])
                deps[int(m_cn.group(1))].append(n)

    dup_change_ids = sorted({x for x in change_ids if change_ids.count(x) > 1})
    if dup_change_ids:
        errors.append({"type": "id", "message": "Duplicate change IDs", "ids": dup_change_ids})

    if summary_counts is not None and change_nums:
        if summary_counts["total"] != len(change_nums):
            errors.append({"type": "structure", "message": "Total Changes must equal number of change entries", "total": summary_counts["total"], "entries": len(change_nums)})
        st_map = {"✅ COMPLETED": "completed", "🔄 IN_PROGRESS": "in_progress", "⏳ NOT_STARTED": "not_started"}
        counts = {"completed": 0, "in_progress": 0, "not_started": 0}
        for _, _, _, block in change_blocks:
            v = _get_field_value(block, "Status")
            if v in st_map:
                counts[st_map[v]] += 1
        if any(counts[k] != summary_counts[k] for k in counts.keys()):
            errors.append({"type": "structure", "message": "Summary status counts must match statuses of change entries", "summary": summary_counts, "found": counts})

    def _has_cycle(graph: Dict[int, List[int]]) -> bool:
        visiting: set = set()
        visited: set = set()

        def dfs(v: int) -> bool:
            if v in visited:
                return False
            if v in visiting:
                return True
            visiting.add(v)
            for nxt in graph.get(v, []):
                if dfs(nxt):
                    return True
            visiting.remove(v)
            visited.add(v)
            return False

        for v in graph.keys():
            if dfs(v):
                return True
        return False

    if deps and _has_cycle(deps):
        errors.append({"type": "content", "message": "Dependency graph contains a cycle"})

    if not skip_fs_checks and feature_root is not None:
        dp = feature_root / "DESIGN.md"
        dt, derr = load_text(dp)
        if derr:
            errors.append({"type": "cross", "message": derr})
        else:
            design_req_ids = sorted(set(FEATURE_REQ_ID_RE.findall(dt or "")))
            design_req_full = sorted(set(re.findall(r"\bfdd-[a-z0-9-]+-feature-[a-z0-9-]+-req-[a-z0-9-]+\b", dt or "")))
            if feature_slug is not None:
                design_req_full = [x for x in design_req_full if f"-feature-{feature_slug}-" in x]
            implemented = sorted(set([rid for ids in implements_by_change.values() for rid in ids]))
            unknown = sorted([x for x in implemented if x not in set(design_req_full)])
            if unknown:
                errors.append({"type": "cross", "message": "CHANGES implements unknown requirement IDs (not found in feature DESIGN.md)", "ids": unknown})
            missing = sorted([x for x in design_req_full if x not in set(implemented)])
            if design_req_full and missing:
                errors.append({"type": "cross", "message": "Not all feature requirements are covered by changes", "missing": missing})

    # FDL Coverage Validation: Check if CHANGES.md references all FDL scopes (flows/algos/states/tests) from DESIGN.md
    if feature_root is not None and not skip_fs_checks:
        design_path = feature_root / "DESIGN.md"
        if design_path.exists():
            try:
                design_text = design_path.read_text(encoding="utf-8")
                design_fdl = extract_fdl_instructions(design_text)
                
                # Validate FDL scope coverage in CHANGES.md
                fdl_coverage_errors = validate_fdl_coverage(artifact_text, design_fdl)
                errors.extend(fdl_coverage_errors)
            except Exception:
                pass

    # ----------------------------
    # Scoring
    # ----------------------------
    buckets = {
        "file_structure": [],
        "change_structure": [],
        "task_breakdown": [],
        "specification": [],
        "code_tagging": [],
        "testing": [],
        "consistency": [],
        "completeness": [],
    }

    def _bucket_for_error(e: Dict[str, object]) -> str:
        t = str(e.get("type", ""))
        msg = str(e.get("message", ""))
        if t in {"header"}:
            return "file_structure"
        if t == "structure":
            # Summary/ordering are file structure; missing subsections are change structure.
            if "Summary" in msg or "number" in msg or "Total Changes" in msg:
                return "file_structure"
            return "change_structure"
        if t == "id":
            return "change_structure"
        if t == "content":
            if msg.startswith("Task") or "task" in msg.lower() or "checkbox" in msg.lower():
                return "task_breakdown"
            if "Specification" in msg or "spec" in msg.lower():
                return "specification"
            if "Testing" in msg or "tests" in msg.lower():
                return "testing"
            if "Dependencies" in msg or "dependency" in msg.lower():
                return "consistency"
            return "change_structure"
        if t == "cross":
            if "requirements" in msg.lower() or "covered" in msg.lower():
                return "completeness"
            return "consistency"
        if t.startswith("fdl"):
            return "consistency"
        return "consistency"

    for e in errors:
        buckets[_bucket_for_error(e)].append(e)
    if placeholders:
        buckets["completeness"].append({"type": "placeholder", "message": "Placeholders found"})

    max_points = {
        "file_structure": 10,
        "change_structure": 20,
        "task_breakdown": 15,
        "specification": 15,
        "code_tagging": 5,
        "testing": 15,
        "consistency": 10,
        "completeness": 10,
    }

    def _penalty(cat: str, issue: Dict[str, object]) -> int:
        t = str(issue.get("type", ""))
        msg = str(issue.get("message", ""))
        if cat == "file_structure" and "Missing" in msg:
            return 5
        if t == "cross" and "Not all feature requirements" in msg:
            return 10
        if "Dependency graph contains a cycle" in msg:
            return 10
        return 5

    score_breakdown: Dict[str, int] = {}
    for cat, maxv in max_points.items():
        pen = sum(_penalty(cat, it) for it in buckets[cat])
        score_breakdown[cat] = max(0, int(maxv - pen))

    score = sum(score_breakdown.values())

    # Critical failures override scoring.
    critical = any(
        (e.get("type") == "header")
        or (e.get("type") == "structure" and str(e.get("message", "")).startswith("No change entries"))
        for e in errors
    )

    passed = (not critical) and (score >= 90)
    return {
        "required_section_count": 0,
        "missing_sections": [],
        "placeholder_hits": placeholders,
        "status": "PASS" if passed else "FAIL",
        "score": score,
        "score_breakdown": score_breakdown,
        "errors": errors,
    }


def _normalize_feature_relpath(path: str) -> str:
    p = path.strip()
    if not p.endswith("/"):
        p = p + "/"
    return p


def _extract_feature_links(text: str) -> List[str]:
    links: List[str] = []
    for _, target in LINK_RE.findall(text):
        t = target.strip()
        if not t.startswith("feature-"):
            continue
        links.append(_normalize_feature_relpath(t))
    return links


def _extract_id_list(field_block: Dict[str, object]) -> List[str]:
    raw: List[str] = []
    inline = str(field_block["value"]).strip()
    if inline:
        raw.extend([p.strip() for p in inline.split(",") if p.strip()])
    for line in list(field_block["tail"]):
        m = re.match(r"^\s*[-*]\s+(.+?)\s*$", line)
        if not m:
            continue
        raw.append(m.group(1).strip())

    ids: List[str] = []
    for item in raw:
        cleaned = item.strip().strip("`")
        if cleaned:
            ids.append(cleaned)
    return ids


