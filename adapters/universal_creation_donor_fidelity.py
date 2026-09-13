"""Read-only INV-10 refinement for Universal Creation's pinned material donor adapter."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

SCHEMA = "axm.invariant-lab.universal-creation-donor-fidelity-projection/v1"
RESULT_SCHEMA = "axm.invariant-lab.universal-creation-donor-fidelity-refinement/v1"
DONOR_REPO = "mike-axiom-mir/axm-universal-creation"
DONOR_COMMIT = "8c8a313fa076a49f947df594e6997b7def267ac9"
PINNED_BLOBS = {
    "MATERIAL_DONOR_ADAPTER.md": "7cc4129924df0a4934b609fa29913643ce5e6c1a",
    "src/axm_uc/material_donor.py": "8e2504714825b38c07754eb90c23158c3794df51",
    "tests/test_material_donor.py": "8288592d647ae8687f4daf670b6bcb84c695d97b",
}
EXPECTED_FORMAT = "axm-material-donor-pack"
EXPECTED_VERSION = "0.2.0"


@dataclass(frozen=True)
class RefinementResult:
    status: str
    checks: list[dict[str, Any]]
    unknowns: list[str]
    failures: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def inspect(projection: dict[str, Any]) -> RefinementResult:
    checks: list[dict[str, Any]] = []
    unknowns: list[str] = []
    failures: list[str] = []

    def require(path: str, value: Any) -> Any:
        if value is None:
            unknowns.append(path)
        return value

    schema = require("schema", projection.get("schema"))
    if schema is not None:
        ok = schema == SCHEMA
        checks.append({"check": "schema", "ok": ok})
        if not ok:
            failures.append("unsupported projection schema")

    donor = projection.get("donor")
    if not isinstance(donor, dict):
        unknowns.append("donor")
    else:
        repo = require("donor.repo", donor.get("repo"))
        commit = require("donor.commit", donor.get("commit"))
        blobs = require("donor.blobs", donor.get("blobs"))
        if repo is not None:
            ok = repo == DONOR_REPO
            checks.append({"check": "donor-repo", "ok": ok})
            if not ok:
                failures.append("donor repository identity drifted")
        if commit is not None:
            ok = commit == DONOR_COMMIT
            checks.append({"check": "donor-commit", "ok": ok})
            if not ok:
                failures.append("donor commit identity drifted")
        if isinstance(blobs, dict):
            ok = all(blobs.get(path) == sha for path, sha in PINNED_BLOBS.items())
            checks.append({"check": "pinned-donor-blobs", "ok": ok})
            if not ok:
                failures.append("one or more pinned donor source/test/doc blobs drifted")
        elif blobs is not None:
            failures.append("donor.blobs is not an object")

    complete = projection.get("completeAdaptation")
    if not isinstance(complete, dict):
        unknowns.append("completeAdaptation")
    else:
        truth_status = require("completeAdaptation.truthStatus", complete.get("truthStatus"))
        source = require("completeAdaptation.source", complete.get("source"))
        accepted = require("completeAdaptation.acceptedEntries", complete.get("acceptedEntries"))
        rendering_verified = require("completeAdaptation.renderingVerified", complete.get("renderingVerified"))
        if truth_status is not None:
            ok = truth_status == "READY_EXACT_MATERIAL_DONOR_ADAPTER"
            checks.append({"check": "complete-adaptation-explicit-ready-status", "ok": ok})
            if not ok:
                failures.append("complete adaptation is not retained as the donor READY status")
        if isinstance(source, dict):
            identity_ok = (
                source.get("format") == EXPECTED_FORMAT
                and source.get("version") == EXPECTED_VERSION
                and source.get("pack_id") == "donor-test-pack"
                and source.get("source_library_id") == "library-test"
            )
            checks.append({"check": "source-identity-survives-adaptation", "ok": identity_ok})
            if not identity_ok:
                failures.append("adapted result does not retain the declared donor pack/library identity")
        elif source is not None:
            failures.append("completeAdaptation.source is not an object")
        if isinstance(accepted, list):
            exact_entries = {item.get("entry_id"): item for item in accepted if isinstance(item, dict)}
            identities_ok = set(exact_entries) == {"material-base", "material-roughness"}
            sources_ok = identities_ok and all(
                isinstance(exact_entries[entry_id].get("source"), dict)
                and exact_entries[entry_id]["source"].get("method") == "self-made-test"
                for entry_id in exact_entries
            )
            channels_ok = identities_ok and {
                exact_entries["material-base"].get("channel"),
                exact_entries["material-roughness"].get("channel"),
            } == {"base-color", "roughness"}
            checks.extend([
                {"check": "accepted-entry-identities-retained", "ok": identities_ok},
                {"check": "accepted-entry-source-metadata-retained", "ok": sources_ok},
                {"check": "accepted-channels-come-from-explicit-donor-routing", "ok": channels_ok},
            ])
            if not identities_ok:
                failures.append("accepted donor entry identities changed or disappeared")
            if not sources_ok:
                failures.append("accepted donor entry source metadata was not retained")
            if not channels_ok:
                failures.append("accepted donor channel mapping does not match the explicit donor hints")
        elif accepted is not None:
            failures.append("completeAdaptation.acceptedEntries is not a list")
        if rendering_verified is not None:
            ok = rendering_verified is False
            checks.append({"check": "descriptor-adaptation-does-not-claim-rendering", "ok": ok})
            if not ok:
                failures.append("detached donor adaptation silently claims rendering verification")

    ambiguous = projection.get("ambiguousEntry")
    if not isinstance(ambiguous, dict):
        unknowns.append("ambiguousEntry")
    else:
        truth_status = require("ambiguousEntry.truthStatus", ambiguous.get("truthStatus"))
        held = require("ambiguousEntry.heldEntries", ambiguous.get("heldEntries"))
        strict_rejects = require("ambiguousEntry.strictRejects", ambiguous.get("strictRejects"))
        if truth_status is not None:
            ok = truth_status == "PARTIAL_EXACT_MATERIAL_DONOR_ADAPTER_WITH_HOLDS"
            checks.append({"check": "ambiguous-entry-remains-partial-hold", "ok": ok})
            if not ok:
                failures.append("ambiguous donor entry was silently promoted out of HOLD")
        if isinstance(held, list):
            target = next((item for item in held if isinstance(item, dict) and item.get("entry_id") == "material-unknown"), None)
            hold_ok = (
                target is not None
                and target.get("observed_hint") == "unassigned"
                and "no supported explicit channel hint" in str(target.get("reason", ""))
            )
            checks.append({"check": "unassigned-channel-remains-visible-hold", "ok": hold_ok})
            if not hold_ok:
                failures.append("unassigned donor channel was guessed, dropped, or lost from held evidence")
        elif held is not None:
            failures.append("ambiguousEntry.heldEntries is not a list")
        if strict_rejects is not None:
            ok = strict_rejects is True
            checks.append({"check": "strict-mode-refuses-held-state", "ok": ok})
            if not ok:
                failures.append("strict adaptation does not reject held donor state")

    conflict = projection.get("familyConflict")
    if not isinstance(conflict, dict):
        unknowns.append("familyConflict")
    else:
        accepted_count = require("familyConflict.acceptedEntryCount", conflict.get("acceptedEntryCount"))
        accepted_family_count = require("familyConflict.acceptedFamilyCount", conflict.get("acceptedFamilyCount"))
        held_families = require("familyConflict.heldFamilies", conflict.get("heldFamilies"))
        if None not in (accepted_count, accepted_family_count):
            textures_survive = accepted_count == 3 and accepted_family_count == 0
            checks.append({"check": "family-conflict-does-not-discard-accepted-textures", "ok": textures_survive})
            if not textures_survive:
                failures.append("family conflict changed the donor's partial-reuse boundary")
        if isinstance(held_families, list):
            target = next((item for item in held_families if isinstance(item, dict) and item.get("family_id") == "family-painted-metal"), None)
            conflict_visible = target is not None and target.get("duplicate_channels") == ["base-color"]
            checks.append({"check": "duplicate-family-channel-remains-explicit-hold", "ok": conflict_visible})
            if not conflict_visible:
                failures.append("duplicate family channel conflict is not retained explicitly")
        elif held_families is not None:
            failures.append("familyConflict.heldFamilies is not a list")

    wrong_version_fails = require("wrongVersionFailsClosed", projection.get("wrongVersionFailsClosed"))
    if wrong_version_fails is not None:
        ok = wrong_version_fails is True
        checks.append({"check": "unsupported-version-fails-closed", "ok": ok})
        if not ok:
            failures.append("unsupported donor version was not retained as fail-closed")

    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(status, checks, sorted(set(unknowns)), failures)


def build_receipt(projection: dict[str, Any]) -> dict[str, Any]:
    result = inspect(projection)
    return {
        "schema": RESULT_SCHEMA,
        "status": result.status,
        "invariant": "INV-10",
        "donor": {
            "repo": DONOR_REPO,
            "commit": DONOR_COMMIT,
            "blobs": dict(sorted(PINNED_BLOBS.items())),
        },
        "checks": result.checks,
        "unknowns": result.unknowns,
        "failures": result.failures,
        "authority": {
            "execution": False,
            "merge": False,
            "promotion": False,
            "canon": False,
        },
        "truthBoundary": (
            "PASS means only that the pinned Universal Creation material-donor source/test projection retains donor "
            "pack/library and accepted-entry source identity, keeps unassigned or conflicting donor state explicit as "
            "HOLD, rejects unsupported versions, and does not claim rendering. It does not prove pixel semantics, "
            "rendering, material correctness, deployment, authorship, or constitutional/CANON authority."
        ),
    }
