from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class ReferenceRule:
    coverage: str  # required|optional|prohibited
    task: Optional[str] = None  # required|allowed|prohibited
    priority: Optional[str] = None  # required|allowed|prohibited
    headings: Optional[List[str]] = None


@dataclass(frozen=True)
class IdConstraint:
    kind: str
    required: bool = True
    name: Optional[str] = None
    description: Optional[str] = None
    examples: Optional[List[object]] = None
    task: Optional[str] = None  # required|allowed|prohibited
    priority: Optional[str] = None  # required|allowed|prohibited
    to_code: Optional[bool] = None
    headings: Optional[List[str]] = None
    references: Optional[Dict[str, ReferenceRule]] = None


def _parse_tri_state(v: object, field: str) -> Tuple[Optional[str], Optional[str]]:
    if v is None:
        return None, None
    if isinstance(v, bool):
        return ("required" if v else "prohibited"), None
    if isinstance(v, str):
        vv = v.strip().lower()
        if vv in {"required", "allowed", "prohibited"}:
            return vv, None
        return None, f"Constraint field '{field}' must be one of: required, allowed, prohibited"
    return None, f"Constraint field '{field}' must be string (required|allowed|prohibited)"


@dataclass(frozen=True)
class ArtifactKindConstraints:
    name: Optional[str]
    description: Optional[str]
    defined_id: List[IdConstraint]


@dataclass(frozen=True)
class KitConstraints:
    by_kind: Dict[str, ArtifactKindConstraints]


def _parse_examples(v: object) -> Tuple[Optional[List[object]], Optional[str]]:
    if v is None:
        return None, None
    if not isinstance(v, list):
        return None, "Constraint field 'examples' must be a list"
    return list(v), None


def _parse_reference_rule(obj: object) -> Tuple[Optional[ReferenceRule], Optional[str]]:
    if not isinstance(obj, dict):
        return None, "Reference rule must be an object"
    coverage = obj.get("coverage")
    if not isinstance(coverage, str) or coverage.strip() not in {"required", "optional", "prohibited"}:
        return None, "Reference rule field 'coverage' must be one of: required, optional, prohibited"

    task, task_err = _parse_tri_state(obj.get("task"), "references.task")
    if task_err:
        return None, task_err

    priority, pr_err = _parse_tri_state(obj.get("priority"), "references.priority")
    if pr_err:
        return None, pr_err

    headings_raw = obj.get("headings")
    headings: Optional[List[str]] = None
    if headings_raw is not None:
        if not isinstance(headings_raw, list) or any(not isinstance(h, str) for h in headings_raw):
            return None, "Reference rule field 'headings' must be list[str]"
        headings = [h for h in (x.strip() for x in headings_raw) if h]

    return ReferenceRule(
        coverage=coverage.strip(),
        task=task,
        priority=priority,
        headings=headings,
    ), None


def _parse_references(v: object) -> Tuple[Optional[Dict[str, ReferenceRule]], Optional[str]]:
    if v is None:
        return None, None
    if not isinstance(v, dict):
        return None, "Constraint field 'references' must be an object mapping artifact kinds to rules"
    out: Dict[str, ReferenceRule] = {}
    for k, raw in v.items():
        if not isinstance(k, str) or not k.strip():
            return None, "Constraint field 'references' has non-string artifact kind key"
        rule, err = _parse_reference_rule(raw)
        if err:
            return None, f"references[{k}]: {err}"
        if rule is not None:
            out[k.strip().upper()] = rule
    return out, None


def _parse_id_constraint(obj: object) -> Tuple[Optional[IdConstraint], Optional[str]]:
    if not isinstance(obj, dict):
        return None, "Constraint entry must be an object"
    kind = obj.get("kind")
    if not isinstance(kind, str) or not kind.strip():
        return None, "Constraint entry missing required 'kind'"

    required = obj.get("required")
    if required is None:
        required_bool = True
    elif isinstance(required, bool):
        required_bool = required
    else:
        return None, "Constraint field 'required' must be boolean"

    name = obj.get("name")
    if name is not None and not isinstance(name, str):
        return None, "Constraint field 'name' must be string"

    description = obj.get("description")
    if description is not None and not isinstance(description, str):
        return None, "Constraint field 'description' must be string"

    examples, ex_err = _parse_examples(obj.get("examples"))
    if ex_err:
        return None, ex_err

    task, task_err = _parse_tri_state(obj.get("task"), "task")
    if task_err:
        return None, task_err

    priority, pr_err = _parse_tri_state(obj.get("priority"), "priority")
    if pr_err:
        return None, pr_err

    to_code = obj.get("to_code")
    if to_code is not None and not isinstance(to_code, bool):
        return None, "Constraint field 'to_code' must be boolean"

    headings_raw = obj.get("headings")
    headings: Optional[List[str]] = None
    if headings_raw is not None:
        if not isinstance(headings_raw, list) or any(not isinstance(h, str) for h in headings_raw):
            return None, "Constraint field 'headings' must be list[str]"
        headings = [h for h in (x.strip() for x in headings_raw) if h]

    # New schema: embedded references map.
    references, ref_err = _parse_references(obj.get("references"))
    if ref_err:
        return None, ref_err

    return (
        IdConstraint(
            kind=kind.strip(),
            required=required_bool,
            name=name,
            description=description,
            examples=examples,
            task=task,
            priority=priority,
            to_code=to_code,
            headings=headings,
            references=references,
        ),
        None,
    )


def parse_kit_constraints(data: object) -> Tuple[Optional[KitConstraints], List[str]]:
    if data is None:
        return None, []
    if not isinstance(data, dict):
        return None, ["constraints.json root must be an object mapping artifact kinds to constraints"]

    out: Dict[str, ArtifactKindConstraints] = {}
    errors: List[str] = []

    for kind, raw in data.items():
        # Allow optional JSON Schema metadata keys.
        # Example: {"$schema": "../../schemas/kit-constraints.schema.json", "PRD": {...}}
        if isinstance(kind, str) and kind.strip().startswith("$"):
            continue
        if not isinstance(kind, str) or not kind.strip():
            errors.append("constraints.json has non-string kind key")
            continue
        if not isinstance(raw, dict):
            errors.append(f"constraints for {kind} must be an object")
            continue

        has_identifiers = "identifiers" in raw
        if not has_identifiers:
            errors.append(f"constraints for {kind} must include 'identifiers'")
            continue

        name = raw.get("name")
        if name is not None and not isinstance(name, str):
            errors.append(f"constraints for {kind} field 'name' must be string")
            continue

        description = raw.get("description")
        if description is not None and not isinstance(description, str):
            errors.append(f"constraints for {kind} field 'description' must be string")
            continue

        defined_id: List[IdConstraint] = []
        seen_defined: set[str] = set()

        identifiers_raw = raw.get("identifiers")
        if not isinstance(identifiers_raw, dict):
            errors.append(f"constraints for {kind} field 'identifiers' must be an object")
            continue
        for kkind, entry in identifiers_raw.items():
            if not isinstance(kkind, str) or not kkind.strip():
                errors.append(f"constraints for {kind} field 'identifiers' has non-string kind key")
                continue
            if not isinstance(entry, dict):
                errors.append(f"constraints for {kind} identifiers[{kkind}]: Constraint entry must be an object")
                continue

            # Infer kind from map key when omitted.
            inferred_kind = kkind.strip()
            if "kind" in entry:
                vv = entry.get("kind")
                if not isinstance(vv, str) or not vv.strip():
                    errors.append(f"constraints for {kind} identifiers[{kkind}]: Constraint entry missing required 'kind'")
                    continue
                if vv.strip().lower() != inferred_kind.lower():
                    errors.append(f"constraints for {kind} identifiers[{kkind}]: Constraint entry kind does not match identifiers key")
                    continue
                normalized = dict(entry)
            else:
                normalized = dict(entry)
                normalized["kind"] = inferred_kind

            c, e = _parse_id_constraint(normalized)
            if e:
                errors.append(f"constraints for {kind} identifiers[{kkind}]: {e}")
                continue
            if c is not None:
                kk = c.kind.strip().lower()
                if kk in seen_defined:
                    errors.append(f"constraints for {kind} identifiers has duplicate kind '{c.kind.strip()}'")
                    continue
                seen_defined.add(kk)
                defined_id.append(c)

        out[kind.strip().upper()] = ArtifactKindConstraints(
            name=name,
            description=description,
            defined_id=defined_id,
        )

    if errors:
        return None, errors
    return KitConstraints(by_kind=out), []


def load_constraints_json(kit_root: Path) -> Tuple[Optional[KitConstraints], List[str]]:
    path = (kit_root / "constraints.json").resolve()
    if not path.is_file():
        return None, []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return None, [f"Failed to parse constraints.json: {e}"]

    constraints, errs = parse_kit_constraints(data)
    if errs:
        return None, errs
    return constraints, []


__all__ = [
    "ReferenceRule",
    "IdConstraint",
    "ArtifactKindConstraints",
    "KitConstraints",
    "load_constraints_json",
    "parse_kit_constraints",
]
