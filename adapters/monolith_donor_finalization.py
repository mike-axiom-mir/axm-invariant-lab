"""INV-20 verifier for a pinned donor-owned AXM Monolith finalization probe."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

OBSERVATION_SCHEMA = "axm.invariant-lab.monolith-donor-finalization-observation/v0.1"
RESULT_SCHEMA = "axm.invariant-lab.monolith-donor-finalization-refinement/v0.1"
DONOR_REPO = "mike-axiom-mir/axm-monolith"
DONOR_COMMIT = "9586e1d11af4ef5a475105f4568627c7a5fdb312"
PINNED_BLOBS = {
    "tools/finalize_connected_snapshot.py": "bfa1088166fc1cd59806efe79c2867e412e50e13",
    "tools/monolith_plumbing.py": "39ada899576ab931ae23443de909cae8f05a663e",
    "tools/callable_execution_ledger.py": "924b9e90464d5361d50228bd84367748621397e8",
    "tools/invoke_declared_callable.py": "360f474384558628c7fbf0ddea0b6f67b9103a35",
    "tests/test_connected_finalization.py": "de8bfe355927d81b66724c301fb184f8972e116b",
}
EXPECTED_DONOR_TESTS = 6
EXECUTED_ADDRESS = "demo-module::demo.double"
UNREQUESTED_ADDRESS = "demo-module::demo.triple"


@dataclass(frozen=True)
class RefinementResult:
    status: str
    checks: list[dict[str, Any]]
    unknowns: list[str]
    failures: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def inspect(observation: dict[str, Any]) -> RefinementResult:
    checks: list[dict[str, Any]] = []
    unknowns: list[str] = []
    failures: list[str] = []

    def require(path: str, value: Any) -> Any:
        if value is None:
            unknowns.append(path)
        return value

    schema = require("schema", observation.get("schema"))
    if schema is not None:
        ok = schema == OBSERVATION_SCHEMA
        checks.append({"check": "observation-schema", "ok": ok})
        if not ok:
            failures.append("unsupported donor-finalization observation schema")

    tests = observation.get("donorTests")
    if not isinstance(tests, dict):
        unknowns.append("donorTests")
    else:
        run = require("donorTests.testsRun", tests.get("testsRun"))
        failures_count = require("donorTests.failures", tests.get("failures"))
        errors_count = require("donorTests.errors", tests.get("errors"))
        ok_flag = require("donorTests.ok", tests.get("ok"))
        if run is not None:
            ok = run == EXPECTED_DONOR_TESTS
            checks.append({"check": "pinned-donor-finalization-test-count", "ok": ok})
            if not ok:
                failures.append("pinned donor finalization test count drifted")
        if failures_count is not None and errors_count is not None and ok_flag is not None:
            ok = failures_count == 0 and errors_count == 0 and ok_flag is True
            checks.append({"check": "pinned-donor-finalization-tests-pass", "ok": ok})
            if not ok:
                failures.append("pinned donor finalization tests did not pass")

    before = observation.get("preExecution")
    if not isinstance(before, dict):
        unknowns.append("preExecution")
    else:
        declarations = require("preExecution.declaredCallableCount", before.get("declaredCallableCount"))
        executed = require("preExecution.sourceCallableExecuted", before.get("sourceCallableExecuted"))
        plumbing_status = require("preExecution.plumbingStatus", before.get("plumbingStatus"))
        if declarations is not None:
            ok = declarations == 2
            checks.append({"check": "two-callables-declared", "ok": ok})
            if not ok:
                failures.append("probe did not expose exactly two declared callables")
        if executed is not None:
            ok = executed == 0
            checks.append({"check": "declaration-does-not-imply-execution", "ok": ok})
            if not ok:
                failures.append("plumbing silently promoted a declaration to executed evidence")
        if plumbing_status is not None:
            ok = plumbing_status == "PLUMBING_INSTALLED_WITH_EXPLICIT_EXECUTION_BOUNDARY"
            checks.append({"check": "explicit-execution-boundary", "ok": ok})
            if not ok:
                failures.append("donor plumbing lost its explicit execution boundary")

    blocked = observation.get("unprovenRequiredAddress")
    if not isinstance(blocked, dict):
        unknowns.append("unprovenRequiredAddress")
    else:
        address = require("unprovenRequiredAddress.address", blocked.get("address"))
        was_blocked = require("unprovenRequiredAddress.blocked", blocked.get("blocked"))
        if address is not None:
            ok = address == EXECUTED_ADDRESS
            checks.append({"check": "unproven-required-address-identity", "ok": ok})
            if not ok:
                failures.append("unproven-address control targeted the wrong callable")
        if was_blocked is not None:
            ok = was_blocked is True
            checks.append({"check": "unproven-required-address-blocked", "ok": ok})
            if not ok:
                failures.append("package gate accepted a required address without execution evidence")

    explicit = observation.get("explicitExecution")
    if not isinstance(explicit, dict):
        unknowns.append("explicitExecution")
    else:
        requested = require("explicitExecution.requestedAddresses", explicit.get("requestedAddresses"))
        executed_addresses = require("explicitExecution.executedAddresses", explicit.get("executedAddresses"))
        accepted = require("explicitExecution.acceptedExercisedReceipts", explicit.get("acceptedExercisedReceipts"))
        registry_count = require("explicitExecution.registryDeclaredCallableCount", explicit.get("registryDeclaredCallableCount"))
        package_status = require("explicitExecution.packageStatus", explicit.get("packageStatus"))
        if requested is not None:
            ok = requested == [EXECUTED_ADDRESS]
            checks.append({"check": "explicit-request-scope", "ok": ok})
            if not ok:
                failures.append("probe execution request was not scoped to the exact named callable")
        if executed_addresses is not None:
            ok = executed_addresses == [EXECUTED_ADDRESS]
            checks.append({"check": "execution-evidence-does-not-leak", "ok": ok})
            if not ok:
                failures.append("execution evidence leaked beyond the explicitly invoked callable")
            if isinstance(executed_addresses, list):
                not_leaked = UNREQUESTED_ADDRESS not in executed_addresses
                checks.append({"check": "unrequested-declared-callable-remains-unexecuted", "ok": not_leaked})
                if not not_leaked:
                    failures.append("an unrequested declared callable was silently marked executed")
        if accepted is not None:
            ok = accepted == 1
            checks.append({"check": "one-accepted-exercised-receipt", "ok": ok})
            if not ok:
                failures.append("exact invocation did not yield exactly one accepted execution receipt")
        if registry_count is not None:
            ok = registry_count == 2
            checks.append({"check": "ledger-retains-declared-callable-count", "ok": ok})
            if not ok:
                failures.append("execution ledger lost the second declared callable boundary")
        if package_status is not None:
            ok = package_status == "PACKAGED_AFTER_REQUIRED_EVIDENCE_PASS"
            checks.append({"check": "package-requires-evidence-pass", "ok": ok})
            if not ok:
                failures.append("donor finalizer did not report evidence-gated packaging")

    package = observation.get("package")
    if not isinstance(package, dict):
        unknowns.append("package")
    else:
        required = require("package.requiredCallableAddresses", package.get("requiredCallableAddresses"))
        boundary = require("package.truthBoundary", package.get("truthBoundary"))
        if required is not None:
            ok = required == [EXECUTED_ADDRESS]
            checks.append({"check": "package-receipt-binds-exact-required-address", "ok": ok})
            if not ok:
                failures.append("package receipt widened the required callable set")
        if boundary is not None:
            text = str(boundary)
            ok = (
                "only the explicitly required routes" in text
                and "Unbound leaf declarations and candidate compositions remain unexecuted" in text
            )
            checks.append({"check": "package-truth-boundary-preserves-unrelated-gaps", "ok": ok})
            if not ok:
                failures.append("package truth boundary no longer preserves unrelated execution gaps")

    authority = observation.get("authority")
    if not isinstance(authority, dict):
        unknowns.append("authority")
    else:
        for key in ("execution", "merge", "promotion", "canon"):
            value = require(f"authority.{key}", authority.get(key))
            if value is not None:
                ok = value is False
                checks.append({"check": f"authority-{key}-false", "ok": ok})
                if not ok:
                    failures.append(f"refinement attempted authority escalation through {key}")

    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(status, checks, sorted(set(unknowns)), failures)


def build_receipt(
    observation: dict[str, Any],
    *,
    provenance_checks: list[dict[str, Any]] | None = None,
    provenance_failures: list[str] | None = None,
) -> dict[str, Any]:
    result = inspect(observation)
    checks = list(provenance_checks or []) + result.checks
    failures = list(provenance_failures or []) + result.failures
    status = "FAIL" if failures else ("HOLD" if result.unknowns else "PASS")
    return {
        "schema": RESULT_SCHEMA,
        "status": status,
        "invariant": "INV-20",
        "donor": {
            "repo": DONOR_REPO,
            "commit": DONOR_COMMIT,
            "blobs": dict(sorted(PINNED_BLOBS.items())),
        },
        "checks": checks,
        "unknowns": result.unknowns,
        "failures": failures,
        "authority": {
            "execution": False,
            "merge": False,
            "promotion": False,
            "canon": False,
        },
        "truthBoundary": (
            "PASS means the exact pinned AXM Monolith donor commit passed its own connected-finalization tests and an external bounded probe observed declaration-before-execution, fail-closed required-address packaging, exact opt-in execution, and non-leakage to a second unrequested declared callable. It does not prove arbitrary Monolith packages, arbitrary callables, deployment, safety, quality, future donor versions, or merge/CANON/constitutional authority."
        ),
    }
