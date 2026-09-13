"""Read-only invariant checks for AXM Connected Monolith result receipts.

This adapter treats topology, wiring and package presence as evidence classes,
not as automatic callability or verification. It consumes only explicit fields
from ``axm.monolith.connected-zip-result/v0.2`` receipts and never inspects or
executes the referenced archive.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

SUPPORTED_SCHEMA = "axm.monolith.connected-zip-result/v0.2"
KNOWN_STATUS_KEYS = (
    "blocked_missing_callable_binding",
    "blocked_missing_native_contract",
    "callable_through_named_workflow",
    "executable_inspection",
    "executable_test_evidence",
    "launchable_local_surface",
)
REQUIRED_WIRING_COUNTS = (
    "addressable_endpoint_count",
    "aggregate_endpoint_count",
    "callable_workflow_stage_count",
    "composition_count",
    "declared_leaf_endpoint_count",
    "edge_count",
    "endpoint_count",
    "source_callable_endpoint_count",
    "wired_composition_count",
    "wired_edge_count",
)


@dataclass
class ConnectedReceiptResult:
    status: str
    checks: list[dict[str, Any]]
    unknowns: list[str]
    failures: list[str]
    metrics: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _is_nonnegative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def inspect(
    receipt: dict[str, Any],
    *,
    consumer_claim: dict[str, Any] | None = None,
) -> ConnectedReceiptResult:
    """Evaluate one Connected Monolith receipt without semantic promotion.

    PASS means the supported receipt is internally coherent and, when a
    ``consumer_claim`` is supplied, that claim does not upgrade addressable,
    wired or blocked state into callability/verification.

    Missing or future/unknown evidence is HOLD. Explicit contradictions or
    semantic promotion are FAIL.
    """

    checks: list[dict[str, Any]] = []
    unknowns: list[str] = []
    failures: list[str] = []
    metrics: dict[str, Any] = {}

    if not isinstance(receipt, dict):
        return ConnectedReceiptResult(
            status="FAIL",
            checks=[],
            unknowns=[],
            failures=["receipt is not an object"],
            metrics={},
        )

    schema = receipt.get("schema")
    if schema is None:
        unknowns.append("schema")
    elif schema != SUPPORTED_SCHEMA:
        unknowns.append(f"unsupported schema: {schema}")
    else:
        checks.append({"check": "supported-schema", "ok": True})

    for field in ("archive_file_count", "module_count", "zip_bytes"):
        value = receipt.get(field)
        if value is None:
            unknowns.append(field)
        elif not _is_nonnegative_int(value):
            failures.append(f"{field} is not a non-negative integer")

    snapshot_receipt = receipt.get("snapshot_receipt")
    if snapshot_receipt is None:
        unknowns.append("snapshot_receipt")
    elif not isinstance(snapshot_receipt, str) or not snapshot_receipt.strip():
        failures.append("snapshot_receipt is not a non-empty string")

    truth_boundary = receipt.get("truth_boundary")
    if truth_boundary is None:
        unknowns.append("truth_boundary")
    elif not isinstance(truth_boundary, str) or not truth_boundary.strip():
        failures.append("truth_boundary is not a non-empty string")

    zip_sha256 = receipt.get("zip_sha256")
    if zip_sha256 is None:
        unknowns.append("zip_sha256")
    elif not (
        isinstance(zip_sha256, str)
        and zip_sha256.startswith("sha256:")
        and len(zip_sha256) == 71
        and all(ch in "0123456789abcdef" for ch in zip_sha256[7:].lower())
    ):
        failures.append("zip_sha256 is not a sha256:<64-hex> value")

    wiring = receipt.get("wiring")
    if wiring is None:
        unknowns.append("wiring")
        wiring = {}
    elif not isinstance(wiring, dict):
        failures.append("wiring is not an object")
        wiring = {}

    counts: dict[str, int] = {}
    for field in REQUIRED_WIRING_COUNTS:
        value = wiring.get(field)
        if value is None:
            unknowns.append(f"wiring.{field}")
        elif not _is_nonnegative_int(value):
            failures.append(f"wiring.{field} is not a non-negative integer")
        else:
            counts[field] = value

    statuses = wiring.get("adapter_status_counts")
    status_counts: dict[str, int] = {}
    if statuses is None:
        unknowns.append("wiring.adapter_status_counts")
    elif not isinstance(statuses, dict):
        failures.append("wiring.adapter_status_counts is not an object")
    else:
        unknown_statuses = sorted(set(statuses) - set(KNOWN_STATUS_KEYS))
        for key in unknown_statuses:
            unknowns.append(f"wiring.adapter_status_counts.{key}")
        for key in KNOWN_STATUS_KEYS:
            value = statuses.get(key)
            if value is None:
                unknowns.append(f"wiring.adapter_status_counts.{key}")
            elif not _is_nonnegative_int(value):
                failures.append(
                    f"wiring.adapter_status_counts.{key} is not a non-negative integer"
                )
            else:
                status_counts[key] = value

    endpoint_count = counts.get("endpoint_count")
    addressable_count = counts.get("addressable_endpoint_count")
    source_callable = counts.get("source_callable_endpoint_count")
    workflow_stage_count = counts.get("callable_workflow_stage_count")
    status_callable = status_counts.get("callable_through_named_workflow")

    if endpoint_count is not None and addressable_count is not None:
        ok = endpoint_count == addressable_count
        checks.append({"check": "endpoint-addressable-coherence", "ok": ok})
        if not ok:
            failures.append(
                "endpoint_count and addressable_endpoint_count contradict each other"
            )

    if endpoint_count is not None and len(status_counts) == len(KNOWN_STATUS_KEYS):
        status_total = sum(status_counts.values())
        metrics["classified_endpoint_count"] = status_total
        ok = status_total == endpoint_count
        checks.append({"check": "adapter-status-partition", "ok": ok})
        if not ok:
            failures.append(
                f"adapter status counts sum to {status_total}, expected endpoint_count {endpoint_count}"
            )

    callable_values = [
        value
        for value in (source_callable, workflow_stage_count, status_callable)
        if value is not None
    ]
    if len(callable_values) == 3:
        ok = len(set(callable_values)) == 1
        checks.append({"check": "explicit-callable-coherence", "ok": ok})
        if not ok:
            failures.append(
                "explicit callable counts disagree across source/workflow/status evidence"
            )
        else:
            metrics["explicit_callable_endpoint_count"] = source_callable

    for wired_field, total_field, name in (
        ("wired_edge_count", "edge_count", "wired-edge-upper-bound"),
        ("wired_composition_count", "composition_count", "wired-composition-upper-bound"),
    ):
        wired = counts.get(wired_field)
        total = counts.get(total_field)
        if wired is not None and total is not None:
            ok = wired <= total
            checks.append({"check": name, "ok": ok})
            if not ok:
                failures.append(f"{wired_field} exceeds {total_field}")

    if endpoint_count is not None:
        metrics["endpoint_count"] = endpoint_count
    if addressable_count is not None:
        metrics["addressable_endpoint_count"] = addressable_count
    for key in ("blocked_missing_callable_binding", "blocked_missing_native_contract"):
        if key in status_counts:
            metrics[key] = status_counts[key]

    if consumer_claim is not None:
        if not isinstance(consumer_claim, dict):
            failures.append("consumer_claim is not an object")
        else:
            claimed_callable = consumer_claim.get("callable_endpoint_count")
            if claimed_callable is not None:
                if not _is_nonnegative_int(claimed_callable):
                    failures.append("consumer_claim.callable_endpoint_count is not a non-negative integer")
                elif source_callable is None:
                    unknowns.append("consumer claim cannot be checked without source callable evidence")
                elif claimed_callable > source_callable:
                    failures.append(
                        f"consumer claims {claimed_callable} callable endpoints but receipt explicitly grounds {source_callable}"
                    )

            if consumer_claim.get("blocked_endpoints_are_callable") is True:
                failures.append("consumer promotes explicitly blocked endpoints to callable")

            if consumer_claim.get("all_wired_compositions_verified") is True:
                failures.append("consumer promotes wired compositions to verified compositions")

            if consumer_claim.get("addressable_implies_callable") is True:
                failures.append("consumer promotes addressability to callability")

    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return ConnectedReceiptResult(
        status=status,
        checks=checks,
        unknowns=sorted(set(unknowns)),
        failures=failures,
        metrics=metrics,
    )
