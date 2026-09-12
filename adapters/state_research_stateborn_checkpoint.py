"""Refine pinned State Research Stateborn fresh-process checkpoint evidence.

This adapter promotes existing candidate INV-09 to an executable donor refinement:
a detached checkpoint reconstruction must bind to the checkpoint/source identity it
claims to reconstruct. An outer digest alone is insufficient when an inner receipt
has changed; deterministic replay must still agree, and verification grants no
resume/transport/merge/CANON authority.

The adapter checks a mechanical projection of pinned donor test/verifier evidence.
It does not run Stateborn, authenticate the producer, prove complete session resume,
or claim checkpoint persistence/crash safety.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any

SUPPORTED_SCHEMA = "axm.invariant-lab.stateborn-checkpoint-continuity-projection/v0.1"
PINNED_REPOSITORY = "mike-axiom-mir/axm-state-research"
PINNED_INTEGRATION_COMMIT = "cf891d3614d472b1426fbdc4304e4e9fe290fb24"
PINNED_DONOR_HEAD = "0cef53c3900c48a4d7cece62bcbfd6fa34f40fab"
TEST_PATH = "experiments/07-stateborn-rpg-lab/tests/state-transport-process-restart.test.mjs"
TEST_BLOB = "7383822c140522cc71684371bdade3d187271d67"
VERIFIER_PATH = "experiments/07-stateborn-rpg-lab/dist/state-transport-checkpoint.js"
VERIFIER_BLOB = "79ebc5422ea80ca122677f0e2df69eca8a3908d2"
PROCESS_PATH = "experiments/07-stateborn-rpg-lab/tools/verify-state-transport-checkpoint.mjs"
PROCESS_BLOB = "c30f6a46abcd21478642e023c37fff187a634352"
LANE_PATH = "lanes/2026-09-11-stateborn-checkpoint-process-verifier.md"
LANE_BLOB = "9bc0feaa335b9822662252349b55b81a859a31ce"
HOSTED_RUN_ID = 34586268082
NO_AUTHORITY = {
    "automaticResume": False,
    "transportMutation": False,
    "canonicalStateMutation": False,
    "merge": False,
    "canon": False,
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
    value=container[key]
    if not isinstance(value,dict):
        failures.append(f"{path} is not an object"); return None
    return value

def _list(container: dict[str, Any], key: str, path: str, unknowns: list[str], failures: list[str]) -> list[Any] | None:
    if key not in container:
        unknowns.append(path); return None
    value=container[key]
    if not isinstance(value,list):
        failures.append(f"{path} is not an array"); return None
    return value

def _eq(checks: list[dict[str, Any]], failures: list[str], name: str, value: Any, expected: Any) -> None:
    ok=value==expected; checks.append({"check":name,"ok":ok})
    if not ok: failures.append(f"{name} expected {expected!r}, got {value!r}")

def inspect(projection: dict[str, Any]) -> RefinementResult:
    checks=[]; unknowns=[]; failures=[]; derived={}
    if "schema" not in projection: unknowns.append("schema")
    else: _eq(checks,failures,"projection-schema",projection["schema"],SUPPORTED_SCHEMA)

    source=_record(projection,"source","source",unknowns,failures)
    if source is not None:
        expected={
            "repository":PINNED_REPOSITORY,
            "integration_commit":PINNED_INTEGRATION_COMMIT,
            "donor_head":PINNED_DONOR_HEAD,
            "test_path":TEST_PATH,"test_git_blob_sha":TEST_BLOB,
            "verifier_path":VERIFIER_PATH,"verifier_git_blob_sha":VERIFIER_BLOB,
            "process_adapter_path":PROCESS_PATH,"process_adapter_git_blob_sha":PROCESS_BLOB,
            "lane_path":LANE_PATH,"lane_git_blob_sha":LANE_BLOB,
            "hosted_run_id":HOSTED_RUN_ID,"hosted_run_head":PINNED_DONOR_HEAD,
            "hosted_run_conclusion":"success","hosted_node_versions":[20,22],
        }
        for key,want in expected.items():
            if key not in source: unknowns.append(f"source.{key}")
            else: _eq(checks,failures,f"source-{key}",source[key],want)

    meta=_record(projection,"projection","projection",unknowns,failures)
    if meta is not None:
        excluded=_list(meta,"excluded_donor_fields","projection.excluded_donor_fields",unknowns,failures)
        if excluded is not None:
            required={"live Stateborn engine object","complete transport session state","producer authentication or authorship","CANON authority"}
            ok=required.issubset(set(excluded)); checks.append({"check":"projection-preserves-truth-boundary","ok":ok})
            if not ok: failures.append("projection must exclude live runtime/session semantics, producer-authentication claims, and CANON authority")
        paths=_list(meta,"source_paths","projection.source_paths",unknowns,failures)
        if paths is not None and len(paths)<6: failures.append("projection.source_paths is unexpectedly incomplete")

    positive=_record(projection,"positive","positive",unknowns,failures)
    if positive is not None:
        for key,want in {
            "fixture_id":"held-disconnect-recover","local_status":"PASS","fresh_process_exit":0,"fresh_status":"PASS",
            "fresh_receipt_equal_local":True,"checkpoint_digest_equal":True,"engine_receipt_ids_equal":True,"engine_state_digest_equal":True,
        }.items():
            if key not in positive: unknowns.append(f"positive.{key}")
            else: _eq(checks,failures,f"positive-{key}",positive[key],want)
        authority=_record(positive,"authority","positive.authority",unknowns,failures)
        if authority is not None: _eq(checks,failures,"positive-no-authority",authority,NO_AUTHORITY)

    tamper=_record(projection,"tamper_control","tamper_control",unknowns,failures)
    if tamper is not None:
        for key,want in {
            "outer_checkpoint_resealed":True,"fresh_process_exit":2,"fresh_status":"HOLD","reason_code":"CHECKPOINT_REPLAY",
        }.items():
            if key not in tamper: unknowns.append(f"tamper_control.{key}")
            else: _eq(checks,failures,f"tamper-{key}",tamper[key],want)
        if "mutation" not in tamper: unknowns.append("tamper_control.mutation")
        else:
            ok=isinstance(tamper["mutation"],str) and "inner engine receipt" in tamper["mutation"] and "outer checkpoint digest" in tamper["mutation"]
            checks.append({"check":"tamper-reseals-outer-after-inner-change","ok":ok})
            if not ok: failures.append("tamper control must explicitly change an inner receipt and reseal only the outer checkpoint")
        authority=_record(tamper,"authority","tamper_control.authority",unknowns,failures)
        if authority is not None: _eq(checks,failures,"tamper-no-authority",authority,NO_AUTHORITY)

    admission=_record(projection,"admission","admission",unknowns,failures)
    if admission is not None:
        for key,want in {"max_input_bytes":1048576,"fatal_utf8_decode":True,"non_pass_exit_code":2,"input_error_exit_code":1}.items():
            if key not in admission: unknowns.append(f"admission.{key}")
            else: _eq(checks,failures,f"admission-{key}",admission[key],want)

    if not failures and not unknowns:
        derived={
            "inv_09_fresh_process_checkpoint_binding_status":"PASS",
            "outer_digest_only_integrity_status":"FAIL",
            "resealed_inner_tamper_status":"HOLD",
            "verification_authority_status":"NO_AUTHORITY",
            "hosted_node_versions":[20,22],
            "claim_ceiling":"on the exact pinned Stateborn checkpoint-v2 verifier and fresh-process regression, serialized checkpoint-owned state-language evidence reconstructs identically in a detached process, while an inner receipt change remains rejected even after recomputing the outer checkpoint digest",
        }
    status="FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(status,checks,sorted(set(unknowns)),failures,derived)
