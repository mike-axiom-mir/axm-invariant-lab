"""INV-10 verifier for Universal Creation's donor-owned executable material receipt."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any

RECEIPT_SCHEMA = "axm.universal-creation.material-donor-invariant-receipt/v1"
RESULT_SCHEMA = "axm.invariant-lab.universal-creation-donor-execution-refinement/v1"
DONOR_REPO = "mike-axiom-mir/axm-universal-creation"
DONOR_COMMIT = "b6e77afca5dce48f42c41e73af3ec2f7709d6a6d"
DONOR_TOOL = "tools/material_donor_invariant_receipt.py"
DONOR_FIXTURE = "fixtures/material-donor-invariant-probe-v1.json"
PINNED_BLOBS = {
    "src/axm_uc/material_donor.py": "8e2504714825b38c07754eb90c23158c3794df51",
    DONOR_TOOL: "0b46d9c8e07da2ac149541b55fcac9cda26d4ad0",
    DONOR_FIXTURE: "749045f49eb9768e865782c0e582eca883e3d55a",
}
EXPECTED_FORMAT = "axm-material-donor-pack"
EXPECTED_VERSION = "0.2.0"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class RefinementResult:
    status: str
    checks: list[dict[str, Any]]
    unknowns: list[str]
    failures: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def inspect(receipt: dict[str, Any]) -> RefinementResult:
    checks: list[dict[str, Any]] = []
    unknowns: list[str] = []
    failures: list[str] = []

    def require(path: str, value: Any) -> Any:
        if value is None:
            unknowns.append(path)
        return value

    schema = require("schema", receipt.get("schema"))
    if schema is not None:
        ok = schema == RECEIPT_SCHEMA
        checks.append({"check": "donor-receipt-schema", "ok": ok})
        if not ok:
            failures.append("unsupported donor-owned receipt schema")

    producer = receipt.get("producer")
    if not isinstance(producer, dict):
        unknowns.append("producer")
    else:
        expected = {
            "repository": DONOR_REPO,
            "tool": DONOR_TOOL,
            "fixture": DONOR_FIXTURE,
            "adapterFormat": EXPECTED_FORMAT,
            "adapterVersion": EXPECTED_VERSION,
        }
        for key, expected_value in expected.items():
            value = require(f"producer.{key}", producer.get(key))
            if value is not None:
                ok = value == expected_value
                checks.append({"check": f"producer-{key}", "ok": ok})
                if not ok:
                    failures.append(f"donor producer {key} drifted")
        fixture_sha = require("producer.fixtureSha256", producer.get("fixtureSha256"))
        if fixture_sha is not None:
            ok = isinstance(fixture_sha, str) and HEX64.fullmatch(fixture_sha) is not None
            checks.append({"check": "fixture-content-sha256-present", "ok": ok})
            if not ok:
                failures.append("donor receipt does not carry a valid fixture SHA-256")

    observations = receipt.get("observations")
    if not isinstance(observations, dict):
        unknowns.append("observations")
    else:
        complete = observations.get("complete")
        if not isinstance(complete, dict):
            unknowns.append("observations.complete")
        else:
            truth_status = require("observations.complete.truthStatus", complete.get("truthStatus"))
            if truth_status is not None:
                ok = truth_status == "READY_EXACT_MATERIAL_DONOR_ADAPTER"
                checks.append({"check": "complete-ready-status", "ok": ok})
                if not ok:
                    failures.append("donor-owned complete probe is not READY_EXACT_MATERIAL_DONOR_ADAPTER")
            source = require("observations.complete.source", complete.get("source"))
            if isinstance(source, dict):
                ok = (
                    source.get("format") == EXPECTED_FORMAT
                    and source.get("version") == EXPECTED_VERSION
                    and source.get("pack_id") == "invariant-probe-pack"
                    and source.get("source_library_id") == "invariant-probe-library"
                )
                checks.append({"check": "complete-source-identity", "ok": ok})
                if not ok:
                    failures.append("donor-owned complete probe lost declared source identity")
            elif source is not None:
                failures.append("observations.complete.source is not an object")
            accepted = require("observations.complete.acceptedEntries", complete.get("acceptedEntries"))
            if isinstance(accepted, list):
                by_id = {item.get("entryId"): item for item in accepted if isinstance(item, dict)}
                ids_ok = set(by_id) == {"probe-base", "probe-roughness"}
                channels_ok = ids_ok and by_id["probe-base"].get("channel") == "base-color" and by_id["probe-roughness"].get("channel") == "roughness"
                sources_ok = ids_ok and all(
                    isinstance(by_id[item_id].get("source"), dict)
                    and by_id[item_id]["source"].get("method") == "self-made-invariant-probe"
                    for item_id in by_id
                )
                checks.extend(
                    [
                        {"check": "complete-entry-identities", "ok": ids_ok},
                        {"check": "complete-explicit-channel-routing", "ok": channels_ok},
                        {"check": "complete-source-metadata-retained", "ok": sources_ok},
                    ]
                )
                if not ids_ok:
                    failures.append("donor-owned complete probe changed accepted entry identities")
                if not channels_ok:
                    failures.append("donor-owned complete probe changed explicit channel routing")
                if not sources_ok:
                    failures.append("donor-owned complete probe lost entry source metadata")
            elif accepted is not None:
                failures.append("observations.complete.acceptedEntries is not a list")
            for field in ("heldEntryCount", "heldFamilyCount"):
                value = require(f"observations.complete.{field}", complete.get(field))
                if value is not None:
                    ok = value == 0
                    checks.append({"check": f"complete-{field}-zero", "ok": ok})
                    if not ok:
                        failures.append("donor-owned complete probe unexpectedly contains held state")
            rendering = require("observations.complete.renderingVerified", complete.get("renderingVerified"))
            if rendering is not None:
                ok = rendering is False
                checks.append({"check": "complete-does-not-claim-rendering", "ok": ok})
                if not ok:
                    failures.append("donor-owned receipt silently claims rendering verification")

        unassigned = observations.get("unassigned")
        if not isinstance(unassigned, dict):
            unknowns.append("observations.unassigned")
        else:
            status = require("observations.unassigned.truthStatus", unassigned.get("truthStatus"))
            strict = require("observations.unassigned.strictRejected", unassigned.get("strictRejected"))
            held = require("observations.unassigned.heldEntries", unassigned.get("heldEntries"))
            if status is not None:
                ok = status == "PARTIAL_EXACT_MATERIAL_DONOR_ADAPTER_WITH_HOLDS"
                checks.append({"check": "unassigned-remains-hold", "ok": ok})
                if not ok:
                    failures.append("unassigned donor state was promoted out of HOLD")
            if strict is not None:
                ok = strict is True
                checks.append({"check": "strict-rejects-unassigned-hold", "ok": ok})
                if not ok:
                    failures.append("strict donor execution did not reject held state")
            if isinstance(held, list):
                target = next((item for item in held if isinstance(item, dict) and item.get("entry_id") == "probe-unassigned"), None)
                ok = target is not None and target.get("observed_hint") == "unassigned" and "no supported explicit channel hint" in str(target.get("reason", ""))
                checks.append({"check": "unassigned-hold-visible", "ok": ok})
                if not ok:
                    failures.append("unassigned donor state is not retained explicitly")
            elif held is not None:
                failures.append("observations.unassigned.heldEntries is not a list")

        family = observations.get("familyConflict")
        if not isinstance(family, dict):
            unknowns.append("observations.familyConflict")
        else:
            status = require("observations.familyConflict.truthStatus", family.get("truthStatus"))
            count = require("observations.familyConflict.acceptedFamilyCount", family.get("acceptedFamilyCount"))
            accepted = require("observations.familyConflict.acceptedEntries", family.get("acceptedEntries"))
            held = require("observations.familyConflict.heldFamilies", family.get("heldFamilies"))
            if status is not None:
                ok = status == "PARTIAL_EXACT_MATERIAL_DONOR_ADAPTER_WITH_HOLDS"
                checks.append({"check": "family-conflict-remains-hold", "ok": ok})
                if not ok:
                    failures.append("duplicate-channel family conflict was promoted out of HOLD")
            if count is not None:
                ok = count == 0
                checks.append({"check": "family-conflict-no-material-family", "ok": ok})
                if not ok:
                    failures.append("conflicting family was silently accepted")
            if isinstance(accepted, list):
                ids = {item.get("entryId") for item in accepted if isinstance(item, dict)}
                ok = ids == {"probe-base", "probe-roughness", "probe-base-duplicate"}
                checks.append({"check": "family-conflict-keeps-accepted-textures", "ok": ok})
                if not ok:
                    failures.append("family conflict changed the donor partial-reuse boundary")
            elif accepted is not None:
                failures.append("observations.familyConflict.acceptedEntries is not a list")
            if isinstance(held, list):
                target = next((item for item in held if isinstance(item, dict) and item.get("family_id") == "probe-family"), None)
                ok = target is not None and target.get("duplicate_channels") == ["base-color"]
                checks.append({"check": "family-conflict-visible", "ok": ok})
                if not ok:
                    failures.append("duplicate family channel is not retained explicitly")
            elif held is not None:
                failures.append("observations.familyConflict.heldFamilies is not a list")

        unsupported = observations.get("unsupportedVersion")
        if not isinstance(unsupported, dict):
            unknowns.append("observations.unsupportedVersion")
        else:
            rejected = require("observations.unsupportedVersion.rejected", unsupported.get("rejected"))
            message = require("observations.unsupportedVersion.message", unsupported.get("message"))
            if rejected is not None:
                ok = rejected is True
                checks.append({"check": "unsupported-version-rejected", "ok": ok})
                if not ok:
                    failures.append("unsupported donor version did not fail closed")
            if message is not None:
                ok = "unsupported material donor version" in str(message)
                checks.append({"check": "unsupported-version-reason-visible", "ok": ok})
                if not ok:
                    failures.append("unsupported-version rejection lost its donor reason")

    authority = receipt.get("authority")
    if not isinstance(authority, dict):
        unknowns.append("authority")
    else:
        expected_false = ("mayExecute", "mayMerge", "mayPromote", "mayDeclareCanon")
        for key in expected_false:
            value = require(f"authority.{key}", authority.get(key))
            if value is not None:
                ok = value is False
                checks.append({"check": f"authority-{key}-false", "ok": ok})
                if not ok:
                    failures.append(f"donor receipt attempted authority escalation through {key}")

    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(status, checks, sorted(set(unknowns)), failures)


def build_receipt(donor_receipt: dict[str, Any], provenance_checks: list[dict[str, Any]] | None = None, provenance_failures: list[str] | None = None) -> dict[str, Any]:
    result = inspect(donor_receipt)
    provenance_checks = list(provenance_checks or [])
    provenance_failures = list(provenance_failures or [])
    failures = provenance_failures + result.failures
    status = "FAIL" if failures else ("HOLD" if result.unknowns else "PASS")
    return {
        "schema": RESULT_SCHEMA,
        "status": status,
        "invariant": "INV-10",
        "donor": {
            "repo": DONOR_REPO,
            "commit": DONOR_COMMIT,
            "blobs": dict(sorted(PINNED_BLOBS.items())),
        },
        "checks": provenance_checks + result.checks,
        "unknowns": result.unknowns,
        "failures": failures,
        "authority": {
            "execution": False,
            "merge": False,
            "promotion": False,
            "canon": False,
        },
        "truthBoundary": (
            "PASS means the exact pinned Universal Creation commit/blob set executed its own material-donor invariant probe and the emitted receipt preserved the bounded INV-10 source-identity/HOLD semantics checked here. It does not prove arbitrary donor packs, image semantics, PBR correctness, rendering, authorship, deployment, or constitutional/CANON authority."
        ),
    }
