"""Read-only refinement checks for AXM Monolith Pipeline Fabric exports.

This adapter checks only explicit donor fields from the pinned v0.1 contract.
It does not execute candidate pipelines, infer permission from prose, or grant
authority to either repository.
"""

from dataclasses import dataclass, asdict
from typing import Any

SUPPORTED_DESCRIPTOR_SCHEMA = "axm.monolith.pipeline-fabric/v0.1"
SUPPORTED_CANDIDATE_SCHEMA = "axm.monolith.pipeline-candidates/v0.1"
CANDIDATE_ONLY_STATUSES = {
    "declared_contract_path_not_tested",
    "structurally_possible_path_not_tested",
    "inferred_candidate_path_not_tested",
}
REQUIRED_AUTHORITY_FLAGS = (
    "automatic_execution",
    "automatic_install",
    "automatic_merge",
    "automatic_canon",
)
REQUIRED_OUTPUTS = ("graph", "candidates", "gaps")


@dataclass
class RefinementResult:
    status: str
    checks: list[dict[str, Any]]
    unknowns: list[str]
    failures: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def inspect(
    descriptor: dict[str, Any],
    candidates: dict[str, Any] | None,
) -> RefinementResult:
    """Check explicit candidate/authority semantics without mutating donor input.

    PASS requires a supported Pipeline Fabric descriptor, all four explicit
    automatic-authority flags set to false, all three declared output names,
    and a supported candidates payload whose pipeline statuses remain inside
    the donor's candidate-only v0.1 vocabulary.

    Missing evidence is HOLD. A contradictory explicit value is FAIL.
    """

    checks: list[dict[str, Any]] = []
    unknowns: list[str] = []
    failures: list[str] = []

    def require(path: str, value: Any) -> Any:
        if value is None:
            unknowns.append(path)
            return None
        return value

    schema = require("descriptor.schema", descriptor.get("schema"))
    if schema is not None:
        ok = schema == SUPPORTED_DESCRIPTOR_SCHEMA
        checks.append({"check": "descriptor-schema", "ok": ok})
        if not ok:
            failures.append(f"unsupported descriptor schema: {schema}")

    source = require("descriptor.source", descriptor.get("source"))
    if source is not None:
        ok = source == "STACK_ANALYSIS.json"
        checks.append({"check": "descriptor-source", "ok": ok})
        if not ok:
            failures.append("descriptor source is not STACK_ANALYSIS.json")

    outputs = descriptor.get("outputs")
    if outputs is None:
        unknowns.append("descriptor.outputs")
    elif not isinstance(outputs, dict):
        failures.append("descriptor.outputs is not an object")
    else:
        for key in REQUIRED_OUTPUTS:
            value = require(f"descriptor.outputs.{key}", outputs.get(key))
            if value is not None:
                ok = isinstance(value, str) and bool(value.strip())
                checks.append({"check": f"output-{key}", "ok": ok})
                if not ok:
                    failures.append(f"descriptor output {key} is not a non-empty string")

    authority = descriptor.get("authority")
    if authority is None:
        unknowns.append("descriptor.authority")
    elif not isinstance(authority, dict):
        failures.append("descriptor.authority is not an object")
    else:
        for flag in REQUIRED_AUTHORITY_FLAGS:
            value = require(f"descriptor.authority.{flag}", authority.get(flag))
            if value is not None:
                ok = value is False
                checks.append({"check": f"authority-{flag}-false", "ok": ok})
                if not ok:
                    failures.append(f"{flag} is not explicitly false")

    boundary = require("descriptor.truth_boundary", descriptor.get("truth_boundary"))
    if boundary is not None:
        ok = isinstance(boundary, str) and bool(boundary.strip())
        checks.append({"check": "descriptor-truth-boundary-present", "ok": ok})
        if not ok:
            failures.append("descriptor truth_boundary is empty")

    if candidates is None:
        unknowns.append("candidates")
    elif not isinstance(candidates, dict):
        failures.append("candidates payload is not an object")
    else:
        candidate_schema = require("candidates.schema", candidates.get("schema"))
        if candidate_schema is not None:
            ok = candidate_schema == SUPPORTED_CANDIDATE_SCHEMA
            checks.append({"check": "candidates-schema", "ok": ok})
            if not ok:
                failures.append(f"unsupported candidates schema: {candidate_schema}")

        pipelines = candidates.get("pipelines")
        if pipelines is None:
            unknowns.append("candidates.pipelines")
        elif not isinstance(pipelines, list):
            failures.append("candidates.pipelines is not a list")
        else:
            for index, pipeline in enumerate(pipelines):
                if not isinstance(pipeline, dict):
                    failures.append(f"candidates.pipelines[{index}] is not an object")
                    continue
                status = require(
                    f"candidates.pipelines[{index}].status",
                    pipeline.get("status"),
                )
                if status is None:
                    continue
                ok = status in CANDIDATE_ONLY_STATUSES
                checks.append({
                    "check": f"pipeline-{index}-candidate-status",
                    "ok": ok,
                })
                if not ok:
                    failures.append(
                        f"pipeline {index} status escapes candidate-only v0.1 vocabulary: {status}"
                    )

        candidate_boundary = require(
            "candidates.truth_boundary",
            candidates.get("truth_boundary"),
        )
        if candidate_boundary is not None:
            ok = isinstance(candidate_boundary, str) and bool(candidate_boundary.strip())
            checks.append({"check": "candidates-truth-boundary-present", "ok": ok})
            if not ok:
                failures.append("candidates truth_boundary is empty")

    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(
        status=status,
        checks=checks,
        unknowns=sorted(set(unknowns)),
        failures=failures,
    )
