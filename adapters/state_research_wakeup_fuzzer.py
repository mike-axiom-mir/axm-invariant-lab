"""Read-only refinement over pinned AXM State Research Wakeup Fuzzer evidence.

This adapter deliberately does not consume the donor's `necessary` or `missed` oracle
fields. For one minimized broken trace it derives a required wake by triangulating three
runtime observations: observed-read activation absent from declared sparse routing, an
output change visible only when that observed activation executes, and the sparse
scheduler's mismatched output id. It then checks several repaired transitions against
full-scan, declared-sparse, and observed-read execution records.

PASS is evidence only for the exact pinned records. It does not prove observed-read
instrumentation is complete for branches, dynamic/external reads, concurrency, unseen
mutations, or State Research as a whole.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

SUPPORTED_PROJECTION_SCHEMA = "axm.invariant-lab.wakeup-fuzzer-projection/v0.1"
PINNED_REPOSITORY = "mike-axiom-mir/axm-state-research"
PINNED_COMMIT = "cf891d3614d472b1426fbdc4304e4e9fe290fb24"
COUNTEREXAMPLE_PATH = "experiments/03-wakeup-fuzzer/results/raw/counterexample.json"
COUNTEREXAMPLE_BLOB = "2598facfdf681a60aa5a25f083818b143b5cee8b"
TRACE_PATH = "experiments/03-wakeup-fuzzer/results/raw/fuzz_transitions_100.jsonl"
TRACE_BLOB = "79cd00c865e9d21a211fd132dff4679182378795"
COUNTEREXAMPLE_SCHEMA = "axm.wakeup-fuzzer.counterexample/v1"


@dataclass
class RefinementResult:
    status: str
    checks: list[dict[str, Any]]
    unknowns: list[str]
    failures: list[str]
    derived: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _string_set(value: Any, path: str, unknowns: list[str], failures: list[str]) -> set[str] | None:
    if value is None:
        unknowns.append(path)
        return None
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        failures.append(f"{path} is not a list of strings")
        return None
    if len(value) != len(set(value)):
        failures.append(f"{path} contains duplicate ids")
    return set(value)


def _require_record(container: dict[str, Any], key: str, path: str, unknowns: list[str], failures: list[str]) -> dict[str, Any] | None:
    value = container.get(key)
    if value is None:
        unknowns.append(path)
        return None
    if not isinstance(value, dict):
        failures.append(f"{path} is not an object")
        return None
    return value


def inspect(projection: dict[str, Any]) -> RefinementResult:
    checks: list[dict[str, Any]] = []
    unknowns: list[str] = []
    failures: list[str] = []
    derived: dict[str, Any] = {}

    schema = projection.get("schema")
    if schema is None:
        unknowns.append("schema")
    else:
        ok = schema == SUPPORTED_PROJECTION_SCHEMA
        checks.append({"check": "projection-schema", "ok": ok})
        if not ok:
            failures.append(f"unsupported projection schema: {schema}")

    source = _require_record(projection, "source", "source", unknowns, failures)
    if source is not None:
        expected = {
            "repository": PINNED_REPOSITORY,
            "commit": PINNED_COMMIT,
            "counterexample_path": COUNTEREXAMPLE_PATH,
            "counterexample_git_blob_sha": COUNTEREXAMPLE_BLOB,
            "trace_path": TRACE_PATH,
            "trace_git_blob_sha": TRACE_BLOB,
            "counterexample_schema": COUNTEREXAMPLE_SCHEMA,
        }
        for key, expected_value in expected.items():
            value = source.get(key)
            if value is None:
                unknowns.append(f"source.{key}")
                continue
            ok = value == expected_value
            checks.append({"check": f"source-{key}", "ok": ok})
            if not ok:
                failures.append(f"source.{key} does not match pinned donor identity")

    meta = _require_record(projection, "projection", "projection", unknowns, failures)
    if meta is not None:
        method = meta.get("method")
        excluded = meta.get("excluded_donor_fields")
        if method is None:
            unknowns.append("projection.method")
        elif not isinstance(method, str) or not method.strip():
            failures.append("projection.method is empty")
        if excluded is None:
            unknowns.append("projection.excluded_donor_fields")
        elif not isinstance(excluded, list) or not {"necessary", "missed"}.issubset(set(excluded)):
            failures.append("projection must explicitly exclude donor necessary/missed fields")

    counterexample = _require_record(projection, "counterexample", "counterexample", unknowns, failures)
    if counterexample is not None:
        sparse = _require_record(counterexample, "declared_sparse", "counterexample.declared_sparse", unknowns, failures)
        observed = _require_record(counterexample, "observed", "counterexample.observed", unknowns, failures)
        if sparse is not None and observed is not None:
            sparse_awake = _string_set(sparse.get("awakened"), "counterexample.declared_sparse.awakened", unknowns, failures)
            observed_awake = _string_set(observed.get("awakened"), "counterexample.observed.awakened", unknowns, failures)
            sparse_changed = _string_set(sparse.get("changed"), "counterexample.declared_sparse.changed", unknowns, failures)
            observed_changed = _string_set(observed.get("changed"), "counterexample.observed.changed", unknowns, failures)
            sparse_mismatch = _string_set(sparse.get("mismatched_outputs"), "counterexample.declared_sparse.mismatched_outputs", unknowns, failures)
            observed_mismatch = _string_set(observed.get("mismatched_outputs"), "counterexample.observed.mismatched_outputs", unknowns, failures)

            if None not in (sparse_awake, observed_awake, sparse_changed, observed_changed, sparse_mismatch):
                extra_awake = observed_awake - sparse_awake
                extra_changed = observed_changed - sparse_changed
                triangulated = extra_awake & extra_changed & sparse_mismatch
                derived["counterexample.observed_only_awakened_ids"] = sorted(extra_awake)
                derived["counterexample.observed_only_changed_ids"] = sorted(extra_changed)
                derived["counterexample.sparse_mismatch_ids"] = sorted(sparse_mismatch)
                derived["counterexample.instrumented_required_ids"] = sorted(triangulated)
                same_signal = extra_awake == extra_changed == sparse_mismatch and bool(triangulated)
                checks.append({"check": "counterexample-three-signal-triangulation", "ok": same_signal})
                if not same_signal:
                    failures.append("counterexample runtime signals do not identify the same non-empty omitted wake")

            sparse_equiv = sparse.get("output_equivalence")
            observed_equiv = observed.get("output_equivalence")
            if sparse_equiv is None:
                unknowns.append("counterexample.declared_sparse.output_equivalence")
            if observed_equiv is None:
                unknowns.append("counterexample.observed.output_equivalence")
            if sparse_equiv is not None and observed_equiv is not None:
                ok = sparse_equiv is False and observed_equiv is True
                checks.append({"check": "counterexample-equivalence-split", "ok": ok})
                if not ok:
                    failures.append("counterexample does not show sparse failure and observed-read convergence")

            if observed_mismatch is not None:
                ok = not observed_mismatch
                checks.append({"check": "counterexample-observed-no-mismatch", "ok": ok})
                if not ok:
                    failures.append("observed-read counterexample execution still reports mismatched outputs")

            sparse_mutation = sparse.get("mutation")
            observed_mutation = observed.get("mutation")
            if sparse_mutation is None or observed_mutation is None:
                unknowns.append("counterexample.mutation")
            else:
                ok = sparse_mutation == observed_mutation
                checks.append({"check": "counterexample-same-mutation", "ok": ok})
                if not ok:
                    failures.append("counterexample scheduler records do not share the same mutation")

    traces = projection.get("repaired_traces")
    if traces is None:
        unknowns.append("repaired_traces")
    elif not isinstance(traces, list):
        failures.append("repaired_traces is not a list")
    else:
        if len(traces) < 4:
            failures.append("repaired_traces must contain at least four bounded transitions")
        seen: set[int] = set()
        repaired_ok = 0
        for index, trace in enumerate(traces):
            path = f"repaired_traces[{index}]"
            if not isinstance(trace, dict):
                failures.append(f"{path} is not an object")
                continue
            transition = trace.get("transition")
            if not isinstance(transition, int):
                failures.append(f"{path}.transition is not an integer")
                continue
            if transition in seen:
                failures.append(f"duplicate repaired transition: {transition}")
            seen.add(transition)
            modes = {}
            for mode in ("full_scan", "declared_sparse", "observed"):
                record = _require_record(trace, mode, f"{path}.{mode}", unknowns, failures)
                if record is not None:
                    modes[mode] = record
            if len(modes) != 3:
                continue
            same_transition = all(record.get("transition") == transition for record in modes.values())
            same_mutation = len({repr(record.get("mutation")) for record in modes.values()}) == 1
            changed_match = len({(record.get("changed_count"), record.get("changed_hash")) for record in modes.values()}) == 1
            output_match = len({record.get("output_hash") for record in modes.values()}) == 1
            mismatch_clear = all(record.get("mismatched_outputs") == [] for record in modes.values())
            complete = all(
                record.get("changed_count") is not None
                and record.get("changed_hash") is not None
                and record.get("output_hash") is not None
                and record.get("mutation") is not None
                and record.get("mismatched_outputs") is not None
                for record in modes.values()
            )
            if not complete:
                unknowns.append(f"{path}.required_execution_fields")
                continue
            ok = same_transition and same_mutation and changed_match and output_match and mismatch_clear
            checks.append({"check": f"repaired-transition-{transition}-three-mode-equivalence", "ok": ok})
            if not ok:
                failures.append(f"repaired transition {transition} diverges across full_scan/declared_sparse/observed")
            else:
                repaired_ok += 1
        derived["repaired_trace_count"] = len(traces)
        derived["repaired_equivalent_trace_count"] = repaired_ok

    if derived.get("counterexample.instrumented_required_ids"):
        derived["inv_14_counterexample_status"] = "FAIL"
    elif counterexample is not None and not unknowns:
        derived["inv_14_counterexample_status"] = "PASS"
    if isinstance(traces, list) and traces and derived.get("repaired_equivalent_trace_count") == len(traces):
        derived["inv_14_repaired_status"] = "PASS"

    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(status, checks, sorted(set(unknowns)), failures, derived)
