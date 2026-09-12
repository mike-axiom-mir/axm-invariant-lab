"""Refine pinned State Research Stateborn hostile-transport idempotence evidence.

This adapter promotes existing INV-08 on one narrow donor boundary:
an already accepted packet digest may be suppressed on duplicate delivery without a
second state effect, while rejected/corrupt attempts must not become replay barriers.

The projection is read-only and pins exact donor source/test/raw-evidence/report
blobs. It does not execute Stateborn, prove real-network exactly-once delivery,
authenticate peers, or grant execution/merge/CANON authority.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any

SUPPORTED_SCHEMA = "axm.invariant-lab.stateborn-hostile-transport-projection/v0.1"
PINNED_REPOSITORY = "mike-axiom-mir/axm-state-research"
PINNED_COMMIT = "cf891d3614d472b1426fbdc4304e4e9fe290fb24"
SOURCE_PATH = "experiments/07-stateborn-rpg-lab/dist/state-transport.js"
SOURCE_BLOB = "a97bde28404e9904bed2eaf76f528b0245dba29c"
TEST_PATH = "experiments/07-stateborn-rpg-lab/tests/state-transport.test.mjs"
TEST_BLOB = "0036fe3764207c498f9dd832591c614bdab8868c"
RAW_PATH = "experiments/07-stateborn-rpg-lab/results/raw/state_transport_probe.json"
RAW_BLOB = "f8ef63db0109e7c64637916f39174cbaf684719e"
FAILURE_PATH = "experiments/07-stateborn-rpg-lab/docs/RETAINED_TRANSPORT_FAILURE_v0.7.0.md"
FAILURE_BLOB = "90516df35d599767d9815036a09ae4d554b5de20"
REPORT_PATH = "experiments/07-stateborn-rpg-lab/docs/HOSTILE_TRANSPORT_REPORT_v0.7.0.md"
REPORT_BLOB = "10151fc6bbb81be91b391b2201ade2be0caac35b"
FROZEN_FIXTURE_DIGEST = "937ea582ce4576bdff15db1afebbece7c9f11e2b138860d66cfcbc381f948079"
REPORT_PRINTED_DIGEST = "937ea582ce4576bdff15fb1afebbece7c9f11e2b138860d66cfcbc381f948079"

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
            "source_path": SOURCE_PATH,
            "source_git_blob_sha": SOURCE_BLOB,
            "test_path": TEST_PATH,
            "test_git_blob_sha": TEST_BLOB,
            "raw_path": RAW_PATH,
            "raw_git_blob_sha": RAW_BLOB,
            "retained_failure_path": FAILURE_PATH,
            "retained_failure_git_blob_sha": FAILURE_BLOB,
            "report_path": REPORT_PATH,
            "report_git_blob_sha": REPORT_BLOB,
        }
        for key, want in expected.items():
            if key not in source:
                unknowns.append(f"source.{key}")
            else:
                _eq(checks, failures, f"source-{key}", source[key], want)

    identity = _record(projection, "fixture_identity", "fixture_identity", unknowns, failures)
    if identity is not None:
        for key, want in {
            "source_frozen_digest": FROZEN_FIXTURE_DIGEST,
            "raw_fixture_digest": FROZEN_FIXTURE_DIGEST,
            "raw_frozen_fixture_digest": FROZEN_FIXTURE_DIGEST,
            "freeze_valid": True,
            "report_printed_digest": REPORT_PRINTED_DIGEST,
            "report_digest_matches_source": False,
            "report_digest_is_identity_authority": False,
        }.items():
            if key not in identity:
                unknowns.append(f"fixture_identity.{key}")
            else:
                _eq(checks, failures, f"fixture-{key}", identity[key], want)

    semantics = _record(projection, "source_semantics", "source_semantics", unknowns, failures)
    if semantics is not None:
        for key, want in {
            "duplicate_guard_uses_accepted_digest_set": True,
            "duplicate_suppression_returns_before_apply": True,
            "duplicate_event_before_after_digest_equal": True,
            "digest_added_only_when_apply_status_applied": True,
            "rejected_attempts_do_not_install_barrier": True,
        }.items():
            if key not in semantics:
                unknowns.append(f"source_semantics.{key}")
            else:
                _eq(checks, failures, f"semantics-{key}", semantics[key], want)

    duplicate = _record(projection, "held_duplicate", "held_duplicate", unknowns, failures)
    if duplicate is not None:
        for key, want in {
            "fixture_id": "held-duplicate",
            "outcome_code": 1,
            "expected_outcome_code": 1,
            "outcome_matches_expected": True,
            "accepted_packets": 6,
            "duplicates_suppressed": 1,
            "duplicate_no_effect": True,
            "engine_replay": "PASS",
            "transport_replay": "PASS",
        }.items():
            if key not in duplicate:
                unknowns.append(f"held_duplicate.{key}")
            else:
                _eq(checks, failures, f"duplicate-{key}", duplicate[key], want)

    refusal = _record(projection, "held_consent_refusal", "held_consent_refusal", unknowns, failures)
    if refusal is not None:
        for key, want in {
            "fixture_id": "held-consent-refusal",
            "outcome_code": 2,
            "expected_outcome_code": 2,
            "outcome_matches_expected": True,
            "duplicates_suppressed": 1,
            "duplicate_no_effect": True,
            "joint_state_after": [0, 0, 0],
            "engine_replay": "PASS",
            "transport_replay": "PASS",
        }.items():
            if key not in refusal:
                unknowns.append(f"held_consent_refusal.{key}")
            else:
                _eq(checks, failures, f"refusal-{key}", refusal[key], want)

    corrupt = _record(projection, "held_corrupt_retry", "held_corrupt_retry", unknowns, failures)
    if corrupt is not None:
        for key, want in {
            "fixture_id": "held-corrupt-retry",
            "outcome_code": 1,
            "expected_outcome_code": 1,
            "outcome_matches_expected": True,
            "accepted_packets": 6,
            "tamper_refusals": 1,
            "duplicates_suppressed": 0,
            "engine_replay": "PASS",
            "transport_replay": "PASS",
            "retained_failure_before_repair": "rejected digest poisoned deduplication and clean retry was suppressed",
            "repair": "insert digest into duplicate tracking only after APPLIED",
        }.items():
            if key not in corrupt:
                unknowns.append(f"held_corrupt_retry.{key}")
            else:
                _eq(checks, failures, f"corrupt-{key}", corrupt[key], want)

    aggregate = _record(projection, "aggregate", "aggregate", unknowns, failures)
    if aggregate is not None:
        for key, want in {
            "held_out_runs": 10,
            "all_expected_outcomes": True,
            "all_replay": True,
            "all_duplicates_no_effect": True,
            "total_duplicates_suppressed": 2,
            "gate_pass": True,
        }.items():
            if key not in aggregate:
                unknowns.append(f"aggregate.{key}")
            else:
                _eq(checks, failures, f"aggregate-{key}", aggregate[key], want)

    if not failures and not unknowns:
        derived = {
            "inv_08_state_identity_on_duplicate_status": "PASS",
            "accepted_only_replay_barrier_status": "PASS",
            "consent_refusal_survives_duplicate_without_commit": "PASS",
            "report_digest_discrepancy_status": "EXPLICIT_NON_AUTHORITY",
            "claim_ceiling": (
                "on the exact pinned deterministic Stateborn v0.7 hostile-transport boundary, "
                "accepted packet digests suppress later duplicates without a second engine effect, "
                "while refused/corrupt attempts do not become replay barriers; this is simulator evidence, "
                "not real-network exactly-once delivery or peer-authentication proof"
            ),
        }

    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(status, checks, sorted(set(unknowns)), failures, derived)
