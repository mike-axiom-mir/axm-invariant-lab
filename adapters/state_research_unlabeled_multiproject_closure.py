"""Refine pinned AXM State Research unlabeled multi-project closure evidence.

This adapter checks a narrow cross-project trace-closure boundary. Final equality is
not sufficient evidence of closure when silent stale outputs occurred during a held-out
trace. A portable closure claim over the pinned challenge additionally requires zero
silent stale outputs for every held-out project and fail-closed checkpoint recovery.

The adapter does not execute State Research, derive the donor scoring oracle, or claim
the combined policy is universally sufficient.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any

SUPPORTED_PROJECTION_SCHEMA = "axm.invariant-lab.unlabeled-multiproject-closure-projection/v0.1"
PINNED_REPOSITORY = "mike-axiom-mir/axm-state-research"
PINNED_COMMIT = "cf891d3614d472b1426fbdc4304e4e9fe290fb24"
BENCHMARK_PATH = "experiments/06-unlabeled-multiproject-closure-challenge/results/raw/benchmark_results.json"
BENCHMARK_BLOB = "f6be4ae9b42e9c2edbb114d2d85ce1c5689660e7"
CHECKPOINT_PATH = "experiments/06-unlabeled-multiproject-closure-challenge/results/raw/checkpoint_receipts.json"
CHECKPOINT_BLOB = "541cfe64e15fb580ae575cb38e243ac49ffa9350"
REPORT_PATH = "experiments/06-unlabeled-multiproject-closure-challenge/FINAL_REPORT.md"
REPORT_BLOB = "316aea1d795acc1c6a503fdac6800bbd60c35782"
HELD_OUT_MANIFEST_HASH = "2d3b07b3f5eaf5bac06c739d7ff3e3ac9a45f71daff757b7c18d37eb601da251"
EXPECTED_PROJECTS = {
    "adaptive-closure-v0.1.0-at-7ba2b1d": "corrupt_payload",
    "workfloor-sentinel-v0.1.0-at-7ba2b1d": "absent",
}

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
    if key not in container:
        unknowns.append(path); return None
    value = container[key]
    if not isinstance(value, dict):
        failures.append(f"{path} is not an object"); return None
    return value

def _list(container: dict[str, Any], key: str, path: str, unknowns: list[str], failures: list[str]) -> list[Any] | None:
    if key not in container:
        unknowns.append(path); return None
    value = container[key]
    if not isinstance(value, list):
        failures.append(f"{path} is not an array"); return None
    return value

def _equal(checks: list[dict[str, Any]], failures: list[str], name: str, value: Any, expected: Any) -> None:
    ok = value == expected
    checks.append({"check": name, "ok": ok})
    if not ok: failures.append(f"{name} expected {expected!r}, got {value!r}")

def _positive_int(checks: list[dict[str, Any]], failures: list[str], name: str, value: Any) -> None:
    ok = isinstance(value, int) and not isinstance(value, bool) and value > 0
    checks.append({"check": name, "ok": ok})
    if not ok: failures.append(f"{name} must be a positive integer")

def inspect(projection: dict[str, Any]) -> RefinementResult:
    checks: list[dict[str, Any]] = []; unknowns: list[str] = []; failures: list[str] = []; derived: dict[str, Any] = {}
    if "schema" not in projection: unknowns.append("schema")
    else: _equal(checks, failures, "projection-schema", projection["schema"], SUPPORTED_PROJECTION_SCHEMA)

    source = _record(projection, "source", "source", unknowns, failures)
    if source is not None:
        expected = {
            "repository": PINNED_REPOSITORY, "commit": PINNED_COMMIT,
            "benchmark_path": BENCHMARK_PATH, "benchmark_git_blob_sha": BENCHMARK_BLOB,
            "checkpoint_receipts_path": CHECKPOINT_PATH, "checkpoint_receipts_git_blob_sha": CHECKPOINT_BLOB,
            "final_report_path": REPORT_PATH, "final_report_git_blob_sha": REPORT_BLOB,
        }
        for key, value in expected.items():
            if key not in source: unknowns.append(f"source.{key}")
            else: _equal(checks, failures, f"source-{key}", source[key], value)

    meta = _record(projection, "projection", "projection", unknowns, failures)
    if meta is not None:
        excluded = _list(meta, "excluded_donor_fields", "projection.excluded_donor_fields", unknowns, failures)
        if excluded is not None and not {"necessary_wakes", "missed_wakes"}.issubset(set(excluded)):
            failures.append("projection must exclude donor necessary_wakes/missed_wakes")
        paths = _list(meta, "source_paths", "projection.source_paths", unknowns, failures)
        if paths is not None and len(paths) < 6: failures.append("projection.source_paths is unexpectedly incomplete")

    held = _record(projection, "held_out", "held_out", unknowns, failures)
    if held is not None:
        for key, expected in {
            "contains_declared_risk_labels": False,
            "manifest_hash": HELD_OUT_MANIFEST_HASH,
            "mutation_count": 10,
        }.items():
            if key not in held: unknowns.append(f"held_out.{key}")
            else: _equal(checks, failures, f"held-out-{key}", held[key], expected)
        project_ids = _list(held, "project_ids", "held_out.project_ids", unknowns, failures)
        if project_ids is not None:
            unique = set(project_ids)
            ok = len(project_ids) == len(unique) == 2 and unique == set(EXPECTED_PROJECTS)
            checks.append({"check": "held-out-two-distinct-projects", "ok": ok})
            if not ok: failures.append("held_out.project_ids must be exactly the two pinned distinct projects")

    observed = _record(projection, "observed_reads", "observed_reads", unknowns, failures)
    if observed is not None:
        for key, expected in {"policy":"OBSERVED_READS", "final_oracle_equality":True, "silent_stale_outputs":8, "counterexample_count":8}.items():
            if key not in observed: unknowns.append(f"observed_reads.{key}")
            else: _equal(checks, failures, f"observed-{key}", observed[key], expected)
        projects = _list(observed, "projects", "observed_reads.projects", unknowns, failures)
        if projects is not None:
            seen: set[str] = set()
            for idx, item in enumerate(projects):
                if not isinstance(item, dict): failures.append(f"observed_reads.projects[{idx}] is not an object"); continue
                pid = item.get("project_id")
                if not isinstance(pid, str): unknowns.append(f"observed_reads.projects[{idx}].project_id"); continue
                if pid in seen: failures.append(f"duplicate observed project {pid}")
                seen.add(pid)
                if pid not in EXPECTED_PROJECTS: failures.append(f"unexpected observed project {pid}"); continue
                _equal(checks, failures, f"observed-{pid}-checkpoint-case", item.get("checkpoint_case"), EXPECTED_PROJECTS[pid])
                _equal(checks, failures, f"observed-{pid}-final-equality", item.get("final_oracle_equality"), True)
                _equal(checks, failures, f"observed-{pid}-silent-stale", item.get("silent_stale_outputs"), 4)
                _equal(checks, failures, f"observed-{pid}-max-window", item.get("maximum_silent_stale_window"), 4)
            if seen != set(EXPECTED_PROJECTS): failures.append("observed project coverage is incomplete")

    candidate = _record(projection, "combined_candidate", "combined_candidate", unknowns, failures)
    if candidate is not None:
        if "policy" not in candidate: unknowns.append("combined_candidate.policy")
        else: _equal(checks, failures, "candidate-policy", candidate["policy"], "COMBINED_STRUCTURAL_OBSERVED")
        gate = _record(candidate, "gate", "combined_candidate.gate", unknowns, failures)
        if gate is not None:
            for key in ("final_oracle_equality", "silent_stale_outputs_zero", "all_repair_quarantine_provenance_valid", "total_policy_work_less_than_full_oracle"):
                if key not in gate: unknowns.append(f"combined_candidate.gate.{key}")
                else: _equal(checks, failures, f"candidate-gate-{key}", gate[key], True)
        for key, expected in {"final_oracle_equality":True, "silent_stale_outputs":0, "total_policy_check_work":597, "full_oracle_reference_work":1955}.items():
            if key not in candidate: unknowns.append(f"combined_candidate.{key}")
            else: _equal(checks, failures, f"candidate-{key}", candidate[key], expected)
        if all(k in candidate for k in ("total_policy_check_work", "full_oracle_reference_work")):
            ok = candidate["total_policy_check_work"] < candidate["full_oracle_reference_work"]
            checks.append({"check":"candidate-work-below-full-oracle","ok":ok})
            if not ok: failures.append("candidate work is not below full oracle work")
        projects = _list(candidate, "projects", "combined_candidate.projects", unknowns, failures)
        if projects is not None:
            seen: set[str] = set()
            work_sum = 0
            for idx, item in enumerate(projects):
                if not isinstance(item, dict): failures.append(f"combined_candidate.projects[{idx}] is not an object"); continue
                pid=item.get("project_id")
                if not isinstance(pid,str): unknowns.append(f"combined_candidate.projects[{idx}].project_id"); continue
                if pid in seen: failures.append(f"duplicate candidate project {pid}")
                seen.add(pid)
                if pid not in EXPECTED_PROJECTS: failures.append(f"unexpected candidate project {pid}"); continue
                _equal(checks, failures, f"candidate-{pid}-checkpoint-case", item.get("checkpoint_case"), EXPECTED_PROJECTS[pid])
                _equal(checks, failures, f"candidate-{pid}-final-equality", item.get("final_oracle_equality"), True)
                _equal(checks, failures, f"candidate-{pid}-silent-stale", item.get("silent_stale_outputs"), 0)
                _equal(checks, failures, f"candidate-{pid}-quarantines", item.get("quarantines"), 1)
                _equal(checks, failures, f"candidate-{pid}-unresolved-recoveries", item.get("unresolved_recoveries"), 0)
                work=item.get("total_policy_check_work")
                _positive_int(checks, failures, f"candidate-{pid}-work-positive", work)
                if isinstance(work,int) and not isinstance(work,bool): work_sum += work
            if seen != set(EXPECTED_PROJECTS): failures.append("candidate project coverage is incomplete")
            if "total_policy_check_work" in candidate: _equal(checks, failures, "candidate-project-work-sum", work_sum, candidate["total_policy_check_work"])

    recoveries = _list(projection, "checkpoint_recovery", "checkpoint_recovery", unknowns, failures)
    if recoveries is not None:
        seen: set[str] = set()
        for idx, item in enumerate(recoveries):
            if not isinstance(item, dict): failures.append(f"checkpoint_recovery[{idx}] is not an object"); continue
            pid=item.get("project_id")
            if not isinstance(pid,str): unknowns.append(f"checkpoint_recovery[{idx}].project_id"); continue
            if pid in seen: failures.append(f"duplicate checkpoint recovery {pid}")
            seen.add(pid)
            if pid not in EXPECTED_PROJECTS: failures.append(f"unexpected checkpoint recovery project {pid}"); continue
            _equal(checks, failures, f"checkpoint-{pid}-case", item.get("checkpoint_case"), EXPECTED_PROJECTS[pid])
            _equal(checks, failures, f"checkpoint-{pid}-validation", item.get("validation_status"), "quarantined_untrusted")
            _equal(checks, failures, f"checkpoint-{pid}-action", item.get("recovery_action"), "quarantine_then_reconstruct_from_verified_source")
            _positive_int(checks, failures, f"checkpoint-{pid}-reconstruction-positive", item.get("reconstruction_check_executions"))
            for key in ("source_snapshot_hash", "replacement_checkpoint_hash"):
                value=item.get(key)
                ok=isinstance(value,str) and len(value)==64
                checks.append({"check":f"checkpoint-{pid}-{key}-sha256","ok":ok})
                if not ok: failures.append(f"checkpoint {pid} {key} is not a 64-hex-character identity")
            reasons=item.get("validation_reasons")
            if not isinstance(reasons,list) or not reasons: failures.append(f"checkpoint {pid} validation reasons missing")
        if seen != set(EXPECTED_PROJECTS): failures.append("checkpoint recovery coverage is incomplete")

    if not failures and not unknowns:
        derived.update({
            "inv_16_final_equality_only_status":"FAIL",
            "combined_candidate_trace_closure_status":"PASS",
            "checkpoint_trust_status":"PASS",
            "cross_project_project_count":2,
            "observed_only_hidden_transient_failures":8,
            "claim_ceiling":"on the pinned unlabeled two-project challenge, final equality alone is insufficient; per-project zero silent-stale trace closure plus fail-closed checkpoint provenance is required",
        })
    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(status, checks, sorted(set(unknowns)), failures, derived)
