"""Refine pinned State Research reference-state closure evidence.

This adapter checks one narrow bounded claim: sparse body execution may match a
dense oracle while sleeping components still contribute through a derived shared
reference summary. A control with the same wake set that drops a sleeping
reference contribution must diverge, and deliberately dropping summary updates
must fail closed.

The projection is read-only and pins exact donor source/fixture/test/README
blobs. It does not execute State Research, prove arbitrary sparse scheduling,
claim neural/hardware performance, authenticate producers, or grant execution,
merge, or CANON authority.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any

SUPPORTED_SCHEMA = "axm.invariant-lab.reference-state-closure-projection/v0.1"
PINNED_REPOSITORY = "mike-axiom-mir/axm-state-research"
PINNED_COMMIT = "cf891d3614d472b1426fbdc4304e4e9fe290fb24"
README_PATH = "experiments/reference-state-closure-v1/README.md"
README_BLOB = "9e54750a23808ae291d08c4047df91698d41d882"
EXPERIMENT_PATH = "experiments/reference-state-closure-v1/experiment.py"
EXPERIMENT_BLOB = "537a695258927b6f9f7acf924c44900dc306632b"
FIXTURE_PATH = "experiments/reference-state-closure-v1/fixture.json"
FIXTURE_BLOB = "adee7a66f724d4a83b063ec9cb1da4698455480d"
TEST_PATH = "experiments/reference-state-closure-v1/test_experiment.py"
TEST_BLOB = "8e6acbd97d7a772b842a8f180f02b2b9dc8c26bf"
PORTABLE_PATH = "experiments/reference-state-closure-v1/portable.py"
PORTABLE_BLOB = "382c60a8aefea603d3329033e0ce5f3b59c1575e"
PORTABLE_TEST_PATH = "experiments/reference-state-closure-v1/test_portable.py"
PORTABLE_TEST_BLOB = "e8f4cd20e41f3d4e4c7ce2ceb1cce537ed54c2d2"
FIXTURE_SHA256 = "7f65abe33661b1deef2bac40052efff68088cb2d461e14d6a738f1556fb5d6a5"
REPLAY_DIGEST = "31882bcce06d84826ce3112a6538913c3cdcfc9b35f4c149e672a86c85fdf9a0"
FAULT_REPLAY_DIGEST_B = "7cdefd2a393b2123549e339526b60f75465972f1a4813a540f327a6dee94c157"

@dataclass
class RefinementResult:
    status: str
    checks: list[dict[str, Any]]
    unknowns: list[str]
    failures: list[str]
    derived: dict[str, Any]
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def _record(container: dict[str, Any], key: str, path: str,
            unknowns: list[str], failures: list[str]) -> dict[str, Any] | None:
    if key not in container:
        unknowns.append(path); return None
    value = container[key]
    if not isinstance(value, dict):
        failures.append(f"{path} is not an object"); return None
    return value

def _eq(checks: list[dict[str, Any]], failures: list[str],
        name: str, value: Any, expected: Any) -> None:
    ok = value == expected
    checks.append({"check": name, "ok": ok})
    if not ok:
        failures.append(f"{name} expected {expected!r}, got {value!r}")

def inspect(projection: dict[str, Any]) -> RefinementResult:
    checks: list[dict[str, Any]] = []
    unknowns: list[str] = []
    failures: list[str] = []
    derived: dict[str, Any] = {}

    if "schema" not in projection:
        unknowns.append("schema")
    else:
        _eq(checks, failures, "projection-schema", projection["schema"], SUPPORTED_SCHEMA)

    source = _record(projection, "source", "source", unknowns, failures)
    if source is not None:
        expected = {
            "repository": PINNED_REPOSITORY,
            "commit": PINNED_COMMIT,
            "readme_path": README_PATH,
            "readme_git_blob_sha": README_BLOB,
            "experiment_path": EXPERIMENT_PATH,
            "experiment_git_blob_sha": EXPERIMENT_BLOB,
            "fixture_path": FIXTURE_PATH,
            "fixture_git_blob_sha": FIXTURE_BLOB,
            "test_path": TEST_PATH,
            "test_git_blob_sha": TEST_BLOB,
            "portable_path": PORTABLE_PATH,
            "portable_git_blob_sha": PORTABLE_BLOB,
            "portable_test_path": PORTABLE_TEST_PATH,
            "portable_test_git_blob_sha": PORTABLE_TEST_BLOB,
        }
        for key, want in expected.items():
            if key not in source:
                unknowns.append(f"source.{key}")
            else:
                _eq(checks, failures, f"source-{key}", source[key], want)

    baseline = _record(projection, "baseline", "baseline", unknowns, failures)
    if baseline is not None:
        expected = {
            "status": "PASS",
            "fixture_sha256": FIXTURE_SHA256,
            "canonical_output_equality_A_B": True,
            "normalization_equality_A_B": True,
            "replay_digest_A": REPLAY_DIGEST,
            "replay_digest_B": REPLAY_DIGEST,
            "aggressive_control_divergences_A_C": 11,
            "missed_reference_contributions_C": 11,
            "nodes": 8,
            "transitions": 12,
            "dense_body_executions_A": 104,
            "sparse_body_executions_B": 18,
            "executions_avoided_B": 86,
            "sleeping_reference_event_wakes": [],
            "max_dense_reference_bytes_A": 119,
            "max_derived_reference_bytes_B": 23,
            "max_dense_default_bytes_A": 293,
            "max_sparse_default_bytes_B": 35,
            "implicit_default_bytes_avoided_B": 258,
        }
        for key, want in expected.items():
            if key not in baseline:
                unknowns.append(f"baseline.{key}")
            else:
                _eq(checks, failures, f"baseline-{key}", baseline[key], want)

    fault = _record(projection, "dropped_summary_fault", "dropped_summary_fault", unknowns, failures)
    if fault is not None:
        expected = {
            "status": "HOLD",
            "canonical_output_equality_A_B": False,
            "normalization_equality_A_B": False,
            "replay_digest_A": REPLAY_DIGEST,
            "replay_digest_B": FAULT_REPLAY_DIGEST_B,
            "dense_body_executions_A": 104,
            "sparse_body_executions_B": 18,
            "executions_avoided_B": 86,
        }
        for key, want in expected.items():
            if key not in fault:
                unknowns.append(f"dropped_summary_fault.{key}")
            else:
                _eq(checks, failures, f"fault-{key}", fault[key], want)

    semantics = _record(projection, "semantics", "semantics", unknowns, failures)
    if semantics is not None:
        expected = {
            "control_uses_same_wake_set_as_sparse": True,
            "reference_only_change_wakes_no_body": True,
            "derived_reference_update_preserves_dense_equivalence": True,
            "dropping_sleeping_reference_contribution_diverges": True,
            "dropping_reference_summary_update_breaks_equivalence": True,
            "derived_reference_summary_is_rebuildable": True,
            "standalone_portable_verify_is_not_producer_authentication": True,
            "packaging_grants_no_automatic_authority": True,
        }
        for key, want in expected.items():
            if key not in semantics:
                unknowns.append(f"semantics.{key}")
            else:
                _eq(checks, failures, f"semantics-{key}", semantics[key], want)

    if not failures and not unknowns:
        derived = {
            "inv_18_reference_state_closure_status": "PASS",
            "same_wake_set_negative_control_status": "PASS",
            "sleeping_reference_event_body_wakes": 0,
            "body_executions_avoided": 86,
            "reference_encoding_bytes_avoided": 96,
            "claim_ceiling": (
                "on the exact pinned deterministic reference-state-closure workload, sparse body "
                "execution matches the dense oracle only when still-live sleeping reference "
                "contributions remain in derived closure; the same wake set is insufficient when "
                "that shared contribution is dropped. This does not prove arbitrary sparse "
                "schedulers, donor-runtime universality, neural/hardware behavior, or authority."
            ),
        }

    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(status, checks, sorted(set(unknowns)), failures, derived)
