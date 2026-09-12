"""Refine pinned AXM State Research cross-version opaque recovery evidence.

This adapter checks a narrow continuity/truth boundary for opaque evaluator versions.
A checkpoint or resolved output must not cross an evaluator-source identity change as
if semantics were unchanged. If current evaluator source is unavailable, affected
opaque outputs stay explicitly unresolved/escalated rather than being reconstructed
from state or an older checkpoint.

The adapter does not execute State Research, derive the donor scoring oracle, infer
opaque dependencies, or claim the candidate policy is generally sufficient.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any

SUPPORTED_PROJECTION_SCHEMA = "axm.invariant-lab.cross-version-opaque-recovery-projection/v0.1"
PINNED_REPOSITORY = "mike-axiom-mir/axm-state-research"
PINNED_COMMIT = "cf891d3614d472b1426fbdc4304e4e9fe290fb24"
BENCHMARK_PATH = "experiments/07-cross-version-opaque-recovery-challenge/results/raw/benchmark_results.json"
BENCHMARK_BLOB = "748f8d4c232cbe1952800c904ba69f9b3158acb9"
PROVENANCE_PATH = "experiments/07-cross-version-opaque-recovery-challenge/results/raw/provenance_receipts.jsonl"
PROVENANCE_BLOB = "b5a771bbc6682e4042608442e9b13653e499face"
REPORT_PATH = "experiments/07-cross-version-opaque-recovery-challenge/FINAL_REPORT.md"
REPORT_BLOB = "d263438ed7e021fb2cd228b462486bf561e78bbb"
ARCHITECTURE_PATH = "experiments/07-cross-version-opaque-recovery-challenge/ARCHITECTURE.md"
ARCHITECTURE_BLOB = "2768bd92f74e6285fed68bd14e9ba4bd06c26b9a"
HELD_OUT_MANIFEST_HASH = "976e4bd3153ff2cc9201417f19e5d33e8f2eeff00f778f203e7b34e49e25d188"
EXPECTED_V3_UNRESOLVED = ["opaque-guard", "safety-summary"]

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
            "provenance_receipts_path": PROVENANCE_PATH, "provenance_receipts_git_blob_sha": PROVENANCE_BLOB,
            "final_report_path": REPORT_PATH, "final_report_git_blob_sha": REPORT_BLOB,
            "architecture_path": ARCHITECTURE_PATH, "architecture_git_blob_sha": ARCHITECTURE_BLOB,
        }
        for key, expected_value in expected.items():
            if key not in source: unknowns.append(f"source.{key}")
            else: _equal(checks, failures, f"source-{key}", source[key], expected_value)

    meta = _record(projection, "projection", "projection", unknowns, failures)
    if meta is not None:
        excluded = _list(meta, "excluded_donor_fields", "projection.excluded_donor_fields", unknowns, failures)
        if excluded is not None:
            required_exclusions = {"scoring_oracle answers", "opaque evaluator source/code", "inferred hidden dependency path"}
            ok = required_exclusions.issubset(set(excluded))
            checks.append({"check":"projection-excludes-oracle-and-opaque-semantics","ok":ok})
            if not ok: failures.append("projection must exclude oracle answers, opaque evaluator code, and inferred hidden dependency path")
        paths = _list(meta, "source_paths", "projection.source_paths", unknowns, failures)
        if paths is not None and len(paths) < 6: failures.append("projection.source_paths is unexpectedly incomplete")

    challenge = _record(projection, "challenge", "challenge", unknowns, failures)
    if challenge is not None:
        for key, expected_value in {
            "held_out_manifest_hash": HELD_OUT_MANIFEST_HASH,
            "held_out_project_count": 2,
            "held_out_transition_count": 12,
            "registered_nodes_per_project": 12,
            "minimum_resolved_coverage_percentage": 85.0,
        }.items():
            if key not in challenge: unknowns.append(f"challenge.{key}")
            else: _equal(checks, failures, f"challenge-{key}", challenge[key], expected_value)

    controls = _record(projection, "failure_controls", "failure_controls", unknowns, failures)
    if controls is not None:
        expected_controls = {
            "BROKEN_SPARSE": {"wrong_resolved_outputs":6, "untrusted_checkpoint_replays":1},
            "OBSERVED_ONLY": {"wrong_resolved_outputs":4, "untrusted_checkpoint_replays":0},
            "STRUCTURAL_ONLY": {"wrong_resolved_outputs":4, "untrusted_checkpoint_replays":0},
            "ABSTAIN_ALL": {"wrong_resolved_outputs":0, "false_abstentions":154, "resolved_coverage_percentage":0.0},
        }
        for name, expected_fields in expected_controls.items():
            row = _record(controls, name, f"failure_controls.{name}", unknowns, failures)
            if row is None: continue
            for key, expected_value in expected_fields.items():
                if key not in row: unknowns.append(f"failure_controls.{name}.{key}")
                else: _equal(checks, failures, f"control-{name}-{key}", row[key], expected_value)

    candidate = _record(projection, "candidate", "candidate", unknowns, failures)
    if candidate is not None:
        for key, expected_value in {
            "policy":"VERSION_AWARE_BOUNDED", "gate_passed":True,
            "wrong_resolved_outputs":0, "false_abstentions":0,
            "untrusted_checkpoint_replays":0, "resolved_coverage_percentage":91.6667,
            "unresolved_decisions":14, "total_policy_work":41, "full_oracle_reference_work":168,
            "checkpoint_validations":2, "checkpoint_quarantines":2,
            "changed_source_guard_executions":5, "escalation_events":7,
            "repeat_replay_equal":True, "registration_order_invariant":True,
        }.items():
            if key not in candidate: unknowns.append(f"candidate.{key}")
            else: _equal(checks, failures, f"candidate-{key}", candidate[key], expected_value)
        if all(k in candidate for k in ("total_policy_work", "full_oracle_reference_work")):
            ok = candidate["total_policy_work"] < candidate["full_oracle_reference_work"]
            checks.append({"check":"candidate-work-below-full-oracle","ok":ok})
            if not ok: failures.append("candidate work is not below full oracle reference")

        projects = _record(candidate, "projects", "candidate.projects", unknowns, failures)
        if projects is not None:
            v2 = _record(projects, "opaque-workcell-v2", "candidate.projects.opaque-workcell-v2", unknowns, failures)
            if v2 is not None:
                for key, expected_value in {
                    "source_available":True, "source_changed_since_training":True,
                    "checkpoint_case":"training_checkpoint_bound_to_v1", "resolved_coverage_percentage":100.0,
                    "wrong_resolved_outputs":0, "final_unresolved_ids":[], "total_policy_work":25,
                }.items():
                    if key not in v2: unknowns.append(f"candidate.projects.opaque-workcell-v2.{key}")
                    else: _equal(checks, failures, f"v2-{key}", v2[key], expected_value)
            v3 = _record(projects, "opaque-workcell-v3-unavailable", "candidate.projects.opaque-workcell-v3-unavailable", unknowns, failures)
            if v3 is not None:
                for key, expected_value in {
                    "source_available":False, "source_changed_since_training":True,
                    "checkpoint_case":"absent_source_unavailable", "resolved_coverage_percentage":83.3333,
                    "wrong_resolved_outputs":0, "final_unresolved_ids":EXPECTED_V3_UNRESOLVED, "total_policy_work":16,
                }.items():
                    if key not in v3: unknowns.append(f"candidate.projects.opaque-workcell-v3-unavailable.{key}")
                    else: _equal(checks, failures, f"v3-{key}", v3[key], expected_value)

    provenance = _record(projection, "provenance", "provenance", unknowns, failures)
    if provenance is not None:
        v2 = _record(provenance, "v2_checkpoint", "provenance.v2_checkpoint", unknowns, failures)
        if v2 is not None:
            for key, expected_value in {
                "status":"QUARANTINED_UNTRUSTED", "reasons":["evaluator_source_hash_mismatch"],
                "untrusted_replay_permitted":False,
            }.items():
                if key not in v2: unknowns.append(f"provenance.v2_checkpoint.{key}")
                else: _equal(checks, failures, f"v2-checkpoint-{key}", v2[key], expected_value)
        v3 = _record(provenance, "v3_checkpoint", "provenance.v3_checkpoint", unknowns, failures)
        if v3 is not None:
            for key, expected_value in {
                "status":"QUARANTINED_UNTRUSTED", "reasons":["checkpoint_absent"],
                "untrusted_replay_permitted":False,
            }.items():
                if key not in v3: unknowns.append(f"provenance.v3_checkpoint.{key}")
                else: _equal(checks, failures, f"v3-checkpoint-{key}", v3[key], expected_value)
        esc = _record(provenance, "v3_escalation", "provenance.v3_escalation", unknowns, failures)
        if esc is not None:
            for key, expected_value in {
                "action":"retain_unresolved_and_escalate", "receipt_count":7,
                "unresolved_node_ids":EXPECTED_V3_UNRESOLVED, "untrusted_replay":False,
            }.items():
                if key not in esc: unknowns.append(f"provenance.v3_escalation.{key}")
                else: _equal(checks, failures, f"v3-escalation-{key}", esc[key], expected_value)
            events = _list(esc, "triggering_events", "provenance.v3_escalation.triggering_events", unknowns, failures)
            if events is not None:
                expected_events=["initial","v3-width","v3-hidden-off","v3-name","v3-load","v3-hidden-on","v3-budget"]
                _equal(checks, failures, "v3-escalation-events", events, expected_events)

    if not failures and not unknowns:
        derived.update({
            "inv_17_stale_checkpoint_or_semantic_reuse_status":"FAIL",
            "v2_changed_source_bounded_resolution_status":"PASS",
            "v3_unavailable_source_fail_closed_status":"PASS",
            "candidate_wrong_resolved_outputs":0,
            "candidate_explicit_unresolved_decisions":14,
            "claim_ceiling":"on the pinned synthetic two-version challenge, evaluator-source identity invalidates stale semantic reuse; changed available source is bounded by execution, while unavailable source remains explicitly unresolved/escalated",
        })
    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(status, checks, sorted(set(unknowns)), failures, derived)
