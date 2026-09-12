"""Read-only refinement over a pinned AXM State Research Workfloor Sentinel trace.

The adapter does not reproduce Sentinel's checks or router. It performs only set and
identity relations over explicit donor-emitted fields: necessary checks, awakened checks,
reported misses, mismatch ids, equivalence flags, and final result hashes.

PASS means the pinned bug/repaired projection is internally consistent with the narrow
INV-13 refinement relation. It does not prove the donor dependency map is complete for
unobserved mutations and does not promote Invariant Lab's general model fidelity.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

SUPPORTED_PROJECTION_SCHEMA = "axm.invariant-lab.donor-projection/v0.1"
SUPPORTED_DONOR_SCHEMA = "axm.workfloor-sentinel-results/v1"
PINNED_REPOSITORY = "mike-axiom-mir/axm-state-research"
PINNED_COMMIT = "cf891d3614d472b1426fbdc4304e4e9fe290fb24"
PINNED_PATH = "experiments/02-workfloor-sentinel/results/sentinel_results.json"
PINNED_BLOB = "c5cb479a4955940b170c735bd5ee9d58bcb9c888"


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


def inspect(projection: dict[str, Any]) -> RefinementResult:
    """Check the narrow necessary-wakeup refinement against explicit donor fields.

    Missing required evidence is HOLD. Contradictory explicit evidence is FAIL.
    The adapter is read-only and never executes donor code.
    """

    checks: list[dict[str, Any]] = []
    unknowns: list[str] = []
    failures: list[str] = []
    derived: dict[str, Any] = {}

    def require(path: str, value: Any) -> Any:
        if value is None:
            unknowns.append(path)
        return value

    schema = require("schema", projection.get("schema"))
    if schema is not None:
        ok = schema == SUPPORTED_PROJECTION_SCHEMA
        checks.append({"check": "projection-schema", "ok": ok})
        if not ok:
            failures.append(f"unsupported projection schema: {schema}")

    source = projection.get("source")
    if source is None:
        unknowns.append("source")
    elif not isinstance(source, dict):
        failures.append("source is not an object")
    else:
        expected = {
            "repository": PINNED_REPOSITORY,
            "commit": PINNED_COMMIT,
            "path": PINNED_PATH,
            "git_blob_sha": PINNED_BLOB,
            "donor_schema": SUPPORTED_DONOR_SCHEMA,
        }
        for key, expected_value in expected.items():
            value = require(f"source.{key}", source.get(key))
            if value is None:
                continue
            ok = value == expected_value
            checks.append({"check": f"source-{key}", "ok": ok})
            if not ok:
                failures.append(f"source.{key} does not match the pinned donor identity")

    projection_meta = projection.get("projection")
    if projection_meta is None:
        unknowns.append("projection")
    elif not isinstance(projection_meta, dict):
        failures.append("projection is not an object")
    else:
        method = require("projection.method", projection_meta.get("method"))
        fields = require("projection.field_paths", projection_meta.get("field_paths"))
        if method is not None:
            ok = isinstance(method, str) and bool(method.strip())
            checks.append({"check": "projection-method-present", "ok": ok})
            if not ok:
                failures.append("projection.method is empty")
        if fields is not None:
            ok = isinstance(fields, list) and len(fields) >= 20 and all(isinstance(item, str) for item in fields)
            checks.append({"check": "projection-field-paths-explicit", "ok": ok})
            if not ok:
                failures.append("projection.field_paths is incomplete or invalid")

    runs: dict[str, dict[str, Any]] = {}
    for run_name in ("dependency_bug_run", "repaired_run"):
        run = projection.get(run_name)
        if run is None:
            unknowns.append(run_name)
            continue
        if not isinstance(run, dict):
            failures.append(f"{run_name} is not an object")
            continue
        runs[run_name] = run
        step = run.get("step")
        totals = run.get("totals")
        if step is None:
            unknowns.append(f"{run_name}.step")
            continue
        if not isinstance(step, dict):
            failures.append(f"{run_name}.step is not an object")
            continue
        if totals is None:
            unknowns.append(f"{run_name}.totals")
        elif not isinstance(totals, dict):
            failures.append(f"{run_name}.totals is not an object")
            totals = None

        necessary = _string_set(step.get("necessary_check_ids"), f"{run_name}.step.necessary_check_ids", unknowns, failures)
        awakened = _string_set(step.get("awakened_check_ids"), f"{run_name}.step.awakened_check_ids", unknowns, failures)
        reported_missed = _string_set(step.get("missed_check_ids"), f"{run_name}.step.missed_check_ids", unknowns, failures)
        mismatch = _string_set(step.get("sparse_output_mismatch_ids"), f"{run_name}.step.sparse_output_mismatch_ids", unknowns, failures)
        equivalent = require(f"{run_name}.step.sparse_output_equivalent_to_oracle", step.get("sparse_output_equivalent_to_oracle"))

        if necessary is not None and awakened is not None and reported_missed is not None:
            derived_missed = necessary - awakened
            ok = derived_missed == reported_missed
            checks.append({"check": f"{run_name}-reported-miss-set", "ok": ok})
            if not ok:
                failures.append(f"{run_name} reported misses do not equal necessary minus awakened")
            derived[f"{run_name}.derived_missed_check_ids"] = sorted(derived_missed)
            derived[f"{run_name}.invariant_status"] = "PASS" if not derived_missed else "FAIL"

        if mismatch is not None and equivalent is not None:
            if not isinstance(equivalent, bool):
                failures.append(f"{run_name}.step.sparse_output_equivalent_to_oracle is not boolean")
            else:
                ok = equivalent == (len(mismatch) == 0)
                checks.append({"check": f"{run_name}-equivalence-mismatch-consistency", "ok": ok})
                if not ok:
                    failures.append(f"{run_name} equivalence flag contradicts mismatch ids")

        if reported_missed is not None and mismatch is not None:
            ok = reported_missed <= mismatch
            checks.append({"check": f"{run_name}-misses-visible-in-mismatch", "ok": ok})
            if not ok:
                failures.append(f"{run_name} missed necessary checks are absent from mismatch ids")

        if totals is not None and reported_missed is not None:
            missed_total = require(f"{run_name}.totals.missed_wakeups", totals.get("missed_wakeups"))
            if missed_total is not None:
                ok = isinstance(missed_total, int) and missed_total >= len(reported_missed)
                checks.append({"check": f"{run_name}-total-misses-cover-step", "ok": ok})
                if not ok:
                    failures.append(f"{run_name} total missed_wakeups is smaller than projected step misses")

    bug = runs.get("dependency_bug_run")
    repaired = runs.get("repaired_run")
    if bug is not None and repaired is not None:
        bug_flag = require("dependency_bug_run.repaired_dependencies", bug.get("repaired_dependencies"))
        repaired_flag = require("repaired_run.repaired_dependencies", repaired.get("repaired_dependencies"))
        if bug_flag is not None and repaired_flag is not None:
            ok = bug_flag is False and repaired_flag is True
            checks.append({"check": "repair-flag-transition", "ok": ok})
            if not ok:
                failures.append("donor repair flags do not identify bug then repaired runs")

        bug_step = bug.get("step") if isinstance(bug.get("step"), dict) else None
        repaired_step = repaired.get("step") if isinstance(repaired.get("step"), dict) else None
        if bug_step is not None and repaired_step is not None:
            for key in ("sequence", "change_id", "necessary_check_ids"):
                left = require(f"dependency_bug_run.step.{key}", bug_step.get(key))
                right = require(f"repaired_run.step.{key}", repaired_step.get(key))
                if left is not None and right is not None:
                    ok = left == right
                    checks.append({"check": f"same-trace-{key}", "ok": ok})
                    if not ok:
                        failures.append(f"bug/repaired projection changed trace field {key}")

        bug_oracle = require("dependency_bug_run.final_oracle_check_results_hash", bug.get("final_oracle_check_results_hash"))
        repaired_oracle = require("repaired_run.final_oracle_check_results_hash", repaired.get("final_oracle_check_results_hash"))
        bug_sparse = require("dependency_bug_run.final_sparse_check_results_hash", bug.get("final_sparse_check_results_hash"))
        repaired_sparse = require("repaired_run.final_sparse_check_results_hash", repaired.get("final_sparse_check_results_hash"))
        if None not in (bug_oracle, repaired_oracle, bug_sparse, repaired_sparse):
            same_oracle = bug_oracle == repaired_oracle
            bug_diverges = bug_sparse != bug_oracle
            repaired_converges = repaired_sparse == repaired_oracle
            checks.extend([
                {"check": "same-final-oracle-target", "ok": same_oracle},
                {"check": "bug-final-sparse-diverges", "ok": bug_diverges},
                {"check": "repaired-final-sparse-converges", "ok": repaired_converges},
            ])
            if not same_oracle:
                failures.append("bug/repaired runs do not share the same final oracle target")
            if not bug_diverges:
                failures.append("dependency-bug sparse result does not diverge from oracle")
            if not repaired_converges:
                failures.append("repaired sparse result does not converge to oracle")

        bug_status = derived.get("dependency_bug_run.invariant_status")
        repaired_status = derived.get("repaired_run.invariant_status")
        if bug_status is not None and repaired_status is not None:
            ok = bug_status == "FAIL" and repaired_status == "PASS"
            checks.append({"check": "inv-13-falsified-then-repaired", "ok": ok})
            if not ok:
                failures.append("INV-13 does not falsify the bug run and pass the repaired run")

    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(
        status=status,
        checks=checks,
        unknowns=sorted(set(unknowns)),
        failures=failures,
        derived=derived,
    )
