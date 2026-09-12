"""Refine pinned AXM State Research held-out closure evidence.

This adapter checks a narrow falsification boundary: a runtime-observed dependency set
cannot be treated as closure-complete when a frozen held-out mutation produces a
minimized silent-stale counterexample under the observed-only policy.

The comparison uses the same held-out manifest for an observed-only policy and a
separately selected declared-risk audit policy. It does not execute State Research,
derive the donor oracle, or claim the risk policy is universally sufficient.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any

SUPPORTED_PROJECTION_SCHEMA = "axm.invariant-lab.real-project-closure-projection/v0.1"
PINNED_REPOSITORY = "mike-axiom-mir/axm-state-research"
PINNED_COMMIT = "cf891d3614d472b1426fbdc4304e4e9fe290fb24"
BENCHMARK_PATH = "experiments/05-real-project-closure-trial/results/raw/benchmark_results.json"
BENCHMARK_BLOB = "f7107a348a6e3a328d16d3d149c0438faeb14a21"
COUNTEREXAMPLES_PATH = "experiments/05-real-project-closure-trial/results/raw/counterexamples.json"
COUNTEREXAMPLES_BLOB = "ee0b01e07319721a2bd9e7afe7a1f30ebcba7317"
BENCHMARK_SCHEMA = "axm.real-project-closure.benchmark/v1"
COUNTEREXAMPLE_SCHEMA = "axm.real-project-closure.counterexample/v1"
CONDITIONAL_FAULT_ID = "fault-conditional-read"
CONDITIONAL_CHECK_ID = "json-timings--results__benchmark_results__json"
HELD_OUT_MUTATION_ID = "held-conditional-negative-timing"
HELD_OUT_MANIFEST_HASH = "72315d3330709384129c6a3589b47455beae5e166115f979869127f08afb362e"

@dataclass
class RefinementResult:
    status: str
    checks: list[dict[str, Any]]
    unknowns: list[str]
    failures: list[str]
    derived: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def _record(container: dict[str, Any], key: str, path: str, unknowns: list[str], failures: list[str]) -> dict[str, Any] | None:
    value = container.get(key)
    if value is None:
        unknowns.append(path)
        return None
    if not isinstance(value, dict):
        failures.append(f"{path} is not an object")
        return None
    return value

def _value(container: dict[str, Any], key: str, path: str, unknowns: list[str]) -> Any:
    if key not in container:
        unknowns.append(path)
        return None
    return container[key]

def _check_equal(checks: list[dict[str, Any]], failures: list[str], name: str, value: Any, expected: Any) -> None:
    ok = value == expected
    checks.append({"check": name, "ok": ok})
    if not ok:
        failures.append(f"{name} expected {expected!r}, got {value!r}")

def inspect(projection: dict[str, Any]) -> RefinementResult:
    checks: list[dict[str, Any]] = []
    unknowns: list[str] = []
    failures: list[str] = []
    derived: dict[str, Any] = {}

    schema = projection.get("schema")
    if schema is None:
        unknowns.append("schema")
    else:
        _check_equal(checks, failures, "projection-schema", schema, SUPPORTED_PROJECTION_SCHEMA)

    source = _record(projection, "source", "source", unknowns, failures)
    if source is not None:
        expected = {
            "repository": PINNED_REPOSITORY,
            "commit": PINNED_COMMIT,
            "benchmark_path": BENCHMARK_PATH,
            "benchmark_git_blob_sha": BENCHMARK_BLOB,
            "counterexamples_path": COUNTEREXAMPLES_PATH,
            "counterexamples_git_blob_sha": COUNTEREXAMPLES_BLOB,
            "benchmark_schema": BENCHMARK_SCHEMA,
            "counterexample_schema": COUNTEREXAMPLE_SCHEMA,
        }
        for key, expected_value in expected.items():
            if key not in source:
                unknowns.append(f"source.{key}")
            else:
                _check_equal(checks, failures, f"source-{key}", source[key], expected_value)

    meta = _record(projection, "projection", "projection", unknowns, failures)
    if meta is not None:
        method = _value(meta, "method", "projection.method", unknowns)
        if method is not None and (not isinstance(method, str) or not method.strip()):
            failures.append("projection.method is empty")
        excluded = _value(meta, "excluded_donor_fields", "projection.excluded_donor_fields", unknowns)
        if excluded is not None:
            if not isinstance(excluded, list) or any(not isinstance(item, str) for item in excluded):
                failures.append("projection.excluded_donor_fields is not a list of strings")
            elif not {"necessary_wakes", "missed_wakes"}.issubset(set(excluded)):
                failures.append("projection must explicitly exclude donor necessary_wakes/missed_wakes from the refinement relation")

    fault = _record(projection, "conditional_fault", "conditional_fault", unknowns, failures)
    if fault is not None:
        for key, expected in {
            "id": CONDITIONAL_FAULT_ID,
            "kind": "conditional_read",
            "check_id": CONDITIONAL_CHECK_ID,
            "training_exposed": False,
        }.items():
            if key not in fault:
                unknowns.append(f"conditional_fault.{key}")
            else:
                _check_equal(checks, failures, f"conditional-fault-{key}", fault[key], expected)

    manifest_hash = projection.get("held_out_manifest_hash")
    if manifest_hash is None:
        unknowns.append("held_out_manifest_hash")
    else:
        _check_equal(checks, failures, "held-out-manifest-hash", manifest_hash, HELD_OUT_MANIFEST_HASH)
    mutation_id = projection.get("held_out_mutation_id")
    if mutation_id is None:
        unknowns.append("held_out_mutation_id")
    else:
        _check_equal(checks, failures, "held-out-mutation-id", mutation_id, HELD_OUT_MUTATION_ID)

    observed = _record(projection, "observed_reads", "observed_reads", unknowns, failures)
    counterexample = _record(projection, "minimized_counterexample", "minimized_counterexample", unknowns, failures)
    risk = _record(projection, "declared_risk", "declared_risk", unknowns, failures)

    if observed is not None:
        if "policy" not in observed:
            unknowns.append("observed_reads.policy")
        else:
            _check_equal(checks, failures, "observed-policy", observed["policy"], "OBSERVED_READS")
        if "held_out_manifest_hash" not in observed:
            unknowns.append("observed_reads.held_out_manifest_hash")
        else:
            _check_equal(checks, failures, "observed-held-out-manifest", observed["held_out_manifest_hash"], HELD_OUT_MANIFEST_HASH)
        gate = _record(observed, "gate", "observed_reads.gate", unknowns, failures)
        held = _record(observed, "held_out", "observed_reads.held_out", unknowns, failures)
        mismatches = _value(observed, "final_mismatch_ids", "observed_reads.final_mismatch_ids", unknowns)
        if gate is not None:
            for key, expected in {"final_oracle_equality": False, "silent_stale_outputs_zero": False}.items():
                if key not in gate:
                    unknowns.append(f"observed_reads.gate.{key}")
                else:
                    _check_equal(checks, failures, f"observed-gate-{key}", gate[key], expected)
        if held is not None:
            for key in ("silent_stale_outputs", "silent_stale_transitions", "maximum_silent_stale_window"):
                value = _value(held, key, f"observed_reads.held_out.{key}", unknowns)
                if value is not None:
                    ok = isinstance(value, int) and not isinstance(value, bool) and value > 0
                    checks.append({"check": f"observed-{key}-positive", "ok": ok})
                    if not ok:
                        failures.append(f"observed_reads.held_out.{key} must be a positive integer")
            detected = _value(held, "detected_stale_outputs", "observed_reads.held_out.detected_stale_outputs", unknowns)
            if detected is not None:
                _check_equal(checks, failures, "observed-detected-stale-outputs", detected, 0)
            learned = _value(held, "learned_edges", "observed_reads.held_out.learned_edges", unknowns)
            if learned is not None:
                _check_equal(checks, failures, "observed-held-out-learned-edges", learned, 0)
        if mismatches is not None:
            ok = isinstance(mismatches, list) and CONDITIONAL_CHECK_ID in mismatches
            checks.append({"check": "observed-final-mismatch-contains-conditional-check", "ok": ok})
            if not ok:
                failures.append("observed-only final mismatch does not contain the held-out conditional-read check")

    if counterexample is not None:
        expected = {
            "schema": COUNTEREXAMPLE_SCHEMA,
            "policy": "OBSERVED_READS",
            "check_id": CONDITIONAL_CHECK_ID,
            "minimized_length": 1,
            "minimized_mutation_ids": [HELD_OUT_MUTATION_ID],
            "observed_mutation_id": HELD_OUT_MUTATION_ID,
        }
        for key, expected_value in expected.items():
            if key not in counterexample:
                unknowns.append(f"minimized_counterexample.{key}")
            else:
                _check_equal(checks, failures, f"counterexample-{key}", counterexample[key], expected_value)
        derived["minimized_counterexample_length"] = counterexample.get("minimized_length")
        derived["minimized_counterexample_mutation_ids"] = counterexample.get("minimized_mutation_ids")

    if risk is not None:
        if "policy" not in risk:
            unknowns.append("declared_risk.policy")
        else:
            _check_equal(checks, failures, "risk-policy", risk["policy"], "DECLARED_RISK")
        if "held_out_manifest_hash" not in risk:
            unknowns.append("declared_risk.held_out_manifest_hash")
        else:
            _check_equal(checks, failures, "risk-held-out-manifest", risk["held_out_manifest_hash"], HELD_OUT_MANIFEST_HASH)
        gate = _record(risk, "gate", "declared_risk.gate", unknowns, failures)
        held = _record(risk, "held_out", "declared_risk.held_out", unknowns, failures)
        mismatches = _value(risk, "final_mismatch_ids", "declared_risk.final_mismatch_ids", unknowns)
        if gate is not None:
            for key, expected in {
                "final_oracle_equality": True,
                "silent_stale_outputs_zero": True,
                "all_repairs_retain_provenance": True,
            }.items():
                if key not in gate:
                    unknowns.append(f"declared_risk.gate.{key}")
                else:
                    _check_equal(checks, failures, f"risk-gate-{key}", gate[key], expected)
        if held is not None:
            for key, expected in {
                "silent_stale_outputs": 0,
                "silent_stale_transitions": 0,
                "maximum_silent_stale_window": 0,
            }.items():
                value = _value(held, key, f"declared_risk.held_out.{key}", unknowns)
                if value is not None:
                    _check_equal(checks, failures, f"risk-{key}", value, expected)
            for key in ("detected_stale_outputs", "learned_edges", "repairs", "repairs_with_provenance"):
                value = _value(held, key, f"declared_risk.held_out.{key}", unknowns)
                if value is not None:
                    ok = isinstance(value, int) and not isinstance(value, bool) and value > 0
                    checks.append({"check": f"risk-{key}-positive", "ok": ok})
                    if not ok:
                        failures.append(f"declared_risk.held_out.{key} must be a positive integer")
            if all(key in held for key in ("repairs", "repairs_with_provenance")):
                ok = held["repairs"] == held["repairs_with_provenance"]
                checks.append({"check": "risk-all-repairs-retain-provenance", "ok": ok})
                if not ok:
                    failures.append("declared-risk repair count differs from repairs-with-provenance count")
        if mismatches is not None:
            ok = mismatches == []
            checks.append({"check": "risk-final-mismatch-empty", "ok": ok})
            if not ok:
                failures.append("declared-risk final mismatch list is not empty")

    if observed is not None and risk is not None:
        same_manifest = observed.get("held_out_manifest_hash") == risk.get("held_out_manifest_hash") == manifest_hash == HELD_OUT_MANIFEST_HASH
        checks.append({"check": "policy-comparison-same-held-out-manifest", "ok": same_manifest})
        if not same_manifest:
            failures.append("observed-only and declared-risk records do not share the exact pinned held-out manifest")

    if not failures and not unknowns:
        derived["inv_15_observed_only_completeness_status"] = "FAIL"
        derived["declared_risk_independent_detection_control"] = "PASS"
        derived["claim_ceiling"] = "runtime-observed dependency evidence is not closure-complete on this pinned held-out trial"
    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(status, checks, sorted(set(unknowns)), failures, derived)
