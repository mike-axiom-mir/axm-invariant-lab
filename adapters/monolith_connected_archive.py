"""Bounded archive-backed INV-20 checks for one Connected Monolith package.

The archive reader verifies the internal snapshot receipt, then keeps only a
small cross-artifact projection. Packaged source code is never executed.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import hashlib, json, zipfile
from pathlib import Path
from typing import Any

PROJECTION_SCHEMA = "axm.invariant-lab.monolith-connected-archive-projection/v0.1"
SOURCE_SCHEMAS = {
    "snapshot_integrity": "axm.monolith.connected-snapshot-package/v0.2",
    "execution_fabric": "axm.monolith.execution-fabric/v0.1",
    "gaps": "axm.monolith.execution-gaps/v0.1",
    "leaf_registry": "axm.monolith.leaf-capability-registry/v0.1",
    "workflow": "axm.monolith.workflow-registry/v0.1",
    "compositions": "axm.monolith.executable-compositions/v0.1",
    "full_power_test": "axm.monolith.full-power-test/v0.1",
}
SELECTED = (
    "EXECUTION_FABRIC.json", "EXECUTION_GAPS.json", "LEAF_CAPABILITY_REGISTRY.json",
    "WORKFLOW_REGISTRY.json", "EXECUTABLE_COMPOSITIONS.json",
    "evidence/execution-fabric/FULL_POWER_TEST.json",
)
CALLABLE = "callable_through_named_workflow"


@dataclass
class ArchiveResult:
    status: str
    checks: list[dict[str, Any]]
    unknowns: list[str]
    failures: list[str]
    metrics: dict[str, Any]
    def to_dict(self) -> dict[str, Any]: return asdict(self)


def _sha(data: bytes) -> str: return "sha256:" + hashlib.sha256(data).hexdigest()
def _file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""): h.update(chunk)
    return "sha256:" + h.hexdigest()

def _json(zf: zipfile.ZipFile, path: str) -> dict[str, Any]:
    value = json.loads(zf.read(path))
    if not isinstance(value, dict): raise ValueError(f"{path} is not an object")
    return value


def project_archive(zip_path: str | Path) -> dict[str, Any]:
    """Verify one actual archive and return a deterministic bounded projection."""
    path = Path(zip_path)
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        hits = [n for n in names if n.endswith("/SNAPSHOT_FILE_RECEIPT.json")]
        if len(hits) != 1: raise ValueError(f"expected one snapshot receipt, found {len(hits)}")
        root = hits[0][:-len("SNAPSHOT_FILE_RECEIPT.json")]
        snapshot = _json(zf, hits[0])
        records = snapshot.get("files")
        if not isinstance(records, list): raise ValueError("snapshot files is not a list")
        recs: dict[str, dict[str, Any]] = {}
        missing = mismatch = 0
        for rec in records:
            if not isinstance(rec, dict) or not isinstance(rec.get("path"), str):
                raise ValueError("malformed snapshot file record")
            rel = rec["path"]; recs[rel] = rec; member = root + rel
            if member not in names: missing += 1; continue
            data = zf.read(member)
            if len(data) != rec.get("bytes") or _sha(data) != rec.get("sha256"): mismatch += 1
        nonreceipt = {n[len(root):] for n in names if n.startswith(root) and not n.endswith("/") and n != hits[0]}
        extra = len(nonreceipt - set(recs))
        if any(rel not in recs for rel in SELECTED): raise ValueError("snapshot omits required evidence file")

        execution = _json(zf, root + "EXECUTION_FABRIC.json")
        gaps = _json(zf, root + "EXECUTION_GAPS.json")
        leaf = _json(zf, root + "LEAF_CAPABILITY_REGISTRY.json")
        workflows = _json(zf, root + "WORKFLOW_REGISTRY.json")
        compositions = _json(zf, root + "EXECUTABLE_COMPOSITIONS.json")
        full = _json(zf, root + "evidence/execution-fabric/FULL_POWER_TEST.json")

        endpoints = execution.get("endpoints")
        if not isinstance(endpoints, list): raise ValueError("execution endpoints is not a list")
        status_by_address = {}
        for ep in endpoints:
            try: status_by_address[ep["address"]] = ep["adapter"]["status"]
            except (KeyError, TypeError): raise ValueError("malformed execution endpoint")

        rows = compositions.get("compositions")
        if not isinstance(rows, list): raise ValueError("compositions is not a list")
        step_counts: Counter[str] = Counter(); triples: Counter[tuple[str,str,str]] = Counter()
        with_callable, scope_violations, all_callable = [], [], []
        for row in rows:
            steps = row.get("steps") if isinstance(row, dict) else None
            if not isinstance(steps, list): raise ValueError("malformed composition")
            try: statuses = [status_by_address[a] for a in steps]
            except KeyError as exc: raise ValueError(f"unknown composition step {exc.args[0]}")
            step_counts.update(statuses); cid = str(row.get("id"))
            triples[(str(row.get("wiring_status")), str(row.get("source_status")), str(row.get("execution_status")))] += 1
            if CALLABLE in statuses:
                with_callable.append(cid)
                if row.get("source_status") != "candidate_unverified" or row.get("execution_status") != "not_executed":
                    scope_violations.append(cid)
            if statuses and all(s == CALLABLE for s in statuses): all_callable.append(cid)

        workflow_rows = workflows.get("workflows")
        if not isinstance(workflow_rows, list) or len(workflow_rows) != 1: raise ValueError("expected one named workflow")
        wf = workflow_rows[0]; stages = wf.get("stages")
        if not isinstance(stages, list): raise ValueError("workflow stages is not a list")
        addresses = [s.get("capability") for s in stages]
        try: stage_statuses = [status_by_address[a] for a in addresses]
        except KeyError as exc: raise ValueError(f"unknown workflow stage {exc.args[0]}")

        return {
            "schema": PROJECTION_SCHEMA,
            "source_archive": {"folder_name": root.rstrip("/"), "file_name": root.rstrip("/") + ".zip", "bytes": path.stat().st_size, "sha256": _file_sha(path), "archive_file_count": len(names)},
            "snapshot_integrity": {"receipt_path": "SNAPSHOT_FILE_RECEIPT.json", "receipt_schema": snapshot.get("schema"), "record_count": len(records), "verified_count": len(records)-missing-mismatch, "missing_count": missing, "mismatch_count": mismatch, "extra_nonreceipt_count": extra, "selected_file_sha256": {r: recs[r].get("sha256") for r in SELECTED}},
            "execution_fabric": {"schema": execution.get("schema"), "authority": execution.get("authority"), "summary": execution.get("summary"), "truth_boundary": execution.get("truth_boundary")},
            "gaps": {"schema": gaps.get("schema"), "blocked_endpoint_count": gaps.get("blocked_endpoint_count"), "missing_edge_endpoint_count": gaps.get("missing_edge_endpoint_count"), "truth_boundary": gaps.get("truth_boundary")},
            "leaf_registry": {"schema": leaf.get("schema"), "canonical_capability_count": leaf.get("canonical_capability_count"), "declaration_occurrence_count": leaf.get("declaration_occurrence_count"), "declared_callable_count": leaf.get("declared_callable_count"), "truth_boundary": leaf.get("truth_boundary")},
            "workflow": {"schema": workflows.get("schema"), "workflow_count": workflows.get("workflow_count"), "id": wf.get("id"), "status": wf.get("status"), "stages": addresses, "stage_adapter_statuses": stage_statuses, "required_workflow_receipt": snapshot.get("required_workflow"), "truth_boundary": wf.get("truth_boundary") or workflows.get("truth_boundary")},
            "compositions": {"schema": compositions.get("schema"), "composition_count": compositions.get("composition_count"), "wired_composition_count": compositions.get("wired_composition_count"), "status_triples": [{"wiring_status": k[0], "source_status": k[1], "execution_status": k[2], "count": v} for k,v in sorted(triples.items())], "step_occurrence_count": sum(step_counts.values()), "step_status_counts": dict(sorted(step_counts.items())), "contains_named_workflow_callable_count": len(with_callable), "contains_named_workflow_callable_ids": sorted(with_callable), "all_steps_named_workflow_callable_count": len(all_callable), "callable_scope_violation_ids": sorted(scope_violations), "truth_boundary": compositions.get("truth_boundary")},
            "full_power_test": {"schema": full.get("schema"), "status": full.get("status"), "probe": full.get("probe"), "tests": full.get("tests"), "truth_boundary": full.get("truth_boundary")},
            "truth_boundary": "Projection is derived from one exact user-supplied archive. Hash/integrity checks prove byte identity for recorded package files; cross-artifact checks do not prove source authorship, arbitrary runtime correctness, deployment, or constitutional authority.",
        }


def inspect_projection(p: dict[str, Any], *, consumer_claim: dict[str, Any] | None = None) -> ArchiveResult:
    checks, unknowns, failures, metrics = [], [], [], {}
    if not isinstance(p, dict): return ArchiveResult("FAIL", [], [], ["projection is not an object"], {})
    if p.get("schema") != PROJECTION_SCHEMA:
        return ArchiveResult("HOLD", [], [f"unsupported schema: {p.get('schema')}"], [], {})

    for section, expected in SOURCE_SCHEMAS.items():
        obj = p.get(section)
        key = "receipt_schema" if section == "snapshot_integrity" else "schema"
        if not isinstance(obj, dict) or obj.get(key) != expected:
            unknowns.append(f"unsupported {section}.{key}: {obj.get(key) if isinstance(obj, dict) else None}")
    if unknowns: return ArchiveResult("HOLD", [], sorted(unknowns), [], {})
    checks.append({"check":"supported-projection-and-source-schemas","ok":True})

    snap=p["snapshot_integrity"]; ex=p["execution_fabric"]; gaps=p["gaps"]; leaf=p["leaf_registry"]
    wf=p["workflow"]; comps=p["compositions"]; full=p["full_power_test"]
    summary=ex.get("summary",{}); statuses=summary.get("adapter_status_counts",{})

    ok = snap.get("missing_count")==snap.get("mismatch_count")==snap.get("extra_nonreceipt_count")==0 and snap.get("verified_count")==snap.get("record_count")
    checks.append({"check":"snapshot-byte-integrity","ok":ok})
    if not ok: failures.append("snapshot receipt does not exactly match archive files")
    metrics["snapshot_verified_file_count"] = snap.get("verified_count")

    blocked = statuses.get("blocked_missing_callable_binding",0)+statuses.get("blocked_missing_native_contract",0)
    ok = blocked == gaps.get("blocked_endpoint_count")
    checks.append({"check":"blocked-statuses-match-gap-registry","ok":ok})
    if not ok: failures.append("blocked execution statuses disagree with gap registry")
    metrics["blocked_endpoint_count"] = blocked; metrics["endpoint_count"] = summary.get("endpoint_count")

    ok = summary.get("declared_leaf_endpoint_count") == leaf.get("canonical_capability_count")
    checks.append({"check":"leaf-count-cross-artifact-coherence","ok":ok})
    if not ok: failures.append("declared leaf count disagrees with leaf registry")
    if leaf.get("declared_callable_count") != 0: failures.append("leaf registry silently promotes declarations into callable evidence")
    else: checks.append({"check":"declarations-not-callable","ok":True})

    callables=(summary.get("source_callable_endpoint_count"), summary.get("callable_workflow_stage_count"), statuses.get(CALLABLE))
    ok = wf.get("workflow_count")==1 and wf.get("status")=="callable" and len(wf.get("stages",[]))==len(wf.get("stage_adapter_statuses",[]))==3 and callables==(3,3,3) and all(s==CALLABLE for s in wf.get("stage_adapter_statuses",[]))
    checks.append({"check":"named-workflow-callability-is-explicit-and-bounded","ok":ok})
    if not ok: failures.append("named workflow callability evidence is inconsistent")
    metrics["explicit_callable_endpoint_count"] = callables[0]
    req=wf.get("required_workflow_receipt",{})
    ok = req.get("id")==wf.get("id") and req.get("status")=="EXECUTED_END_TO_END_AND_STRUCTURALLY_ACCEPTED" and req.get("source_capability_executed") is True
    checks.append({"check":"required-workflow-receipt-bound-to-named-workflow","ok":ok})
    if not ok: failures.append("required workflow receipt is not bound to named workflow")

    count=comps.get("composition_count"); expected=[{"wiring_status":"wired_candidate","source_status":"candidate_unverified","execution_status":"not_executed","count":count}]
    ok = comps.get("wired_composition_count")==count and comps.get("status_triples")==expected
    checks.append({"check":"wired-compositions-remain-candidates","ok":ok})
    if not ok: failures.append("wired compositions were promoted beyond candidate/not-executed state")
    metrics["composition_count"] = count
    ok = comps.get("callable_scope_violation_ids")==[] and comps.get("all_steps_named_workflow_callable_count")==0
    checks.append({"check":"named-workflow-scope-does-not-leak-to-compositions","ok":ok})
    if not ok: failures.append("named-workflow callability leaked into candidate composition status")
    metrics["compositions_containing_callable_stage"] = comps.get("contains_named_workflow_callable_count")
    step_counts=comps.get("step_status_counts",{}); step_total=comps.get("step_occurrence_count")
    ok = isinstance(step_counts,dict) and sum(step_counts.values())==step_total
    checks.append({"check":"composition-step-status-partition","ok":ok})
    if not ok: failures.append("composition step statuses do not partition occurrences")
    metrics["composition_step_occurrence_count"] = step_total

    probe_counts=full.get("probe",{}).get("counts",{}); tests=full.get("tests",{})
    ready=probe_counts.get("test_adapter_ready"); ok=ready==statuses.get("executable_test_evidence")
    checks.append({"check":"test-adapter-readiness-cross-artifact-coherence","ok":ok})
    if not ok: failures.append("test adapter readiness disagrees with execution fabric")
    metrics["test_adapter_ready_endpoint_count"] = ready
    command_count=tests.get("command_count"); command_status=tests.get("command_status_counts",{})
    ok=isinstance(command_status,dict) and sum(command_status.values())==command_count
    checks.append({"check":"test-command-status-partition","ok":ok})
    if not ok: failures.append("test command statuses do not partition command count")
    metrics.update(test_command_count=command_count, test_command_failed_count=command_status.get("failed"), test_command_timed_out_count=command_status.get("timed_out"))
    classification=tests.get("command_classification_counts",{}); modules=tests.get("module_status_counts",{})
    if sum(classification.values()) != command_count: failures.append("test command classifications do not partition command count")
    else: checks.append({"check":"test-command-classification-partition","ok":True})
    if sum(modules.values()) != tests.get("module_count"): failures.append("test module statuses do not partition module count")
    else: checks.append({"check":"test-module-status-partition","ok":True})

    authority=ex.get("authority",{}); keys=("automatic_canon","automatic_install","automatic_merge","automatic_network","automatic_source_mutation")
    ok=all(authority.get(k) is False for k in keys)
    checks.append({"check":"no-automatic-authority","ok":ok})
    if not ok: failures.append("execution fabric claims automatic authority")

    if consumer_claim is not None:
        if not isinstance(consumer_claim,dict): failures.append("consumer_claim is not an object")
        else:
            promotions={
                "candidate_compositions_executable":"consumer promotes candidate compositions to executable",
                "named_workflow_callability_transfers_to_compositions":"consumer leaks named-workflow callability into candidate compositions",
                "test_adapter_ready_means_tests_passed":"consumer equates test-adapter readiness with passing tests",
                "declarations_are_callable":"consumer equates leaf declarations with callability",
                "package_integrity_proves_semantics":"consumer equates package byte integrity with semantic correctness",
                "blocked_gaps_may_be_filled_by_guessing":"consumer treats visible adapter gaps as permission to invent semantics",
            }
            failures += [msg for key,msg in promotions.items() if consumer_claim.get(key) is True]

    return ArchiveResult("FAIL" if failures else "PASS", checks, [], failures, metrics)
