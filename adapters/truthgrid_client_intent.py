"""Read-only refinement for the pinned TruthGrid client-intent/consequence boundary."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

SCHEMA = "axm.invariant-lab.truthgrid-client-intent-projection/v1"
RESULT_SCHEMA = "axm.invariant-lab.truthgrid-client-intent-refinement/v1"
DONOR_REPO = "mike-axiom-mir/axm-TruthGrid"
DONOR_COMMIT = "e3875e02db14eb9aef040dc2727dc0ccd58d8ff0"
PINNED_BLOBS = {
    "src/transport/referee.js": "074bbf01a75d9422b4b4b0093f9a2540e3ce513b",
    "src/core/engine.js": "451968447f420b6c13cd24814c61752605fddcbe",
    "tests/determinism.test.js": "47a60a10a49d8de1ed2bea97efc18fc34ee8af77",
}
WIRE_FIELDS = {
    "roomId",
    "actorId",
    "action",
    "direction",
    "clientSequence",
    "proposedTick",
    "schema",
    "revisionOrder",
}
MANIFESTED_FIELDS = {"damage", "resultingState", "hit"}


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
                failures.append("one or more pinned donor source/test blobs drifted")
        elif blobs is not None:
            failures.append("donor.blobs is not an object")

    transport = projection.get("transportBoundary")
    if not isinstance(transport, dict):
        unknowns.append("transportBoundary")
    else:
        input_fields = require("transportBoundary.inputFields", transport.get("inputFields"))
        transported_fields = require("transportBoundary.transportedFields", transport.get("transportedFields"))
        stripped_fields = require("transportBoundary.strippedFields", transport.get("strippedFields"))
        if isinstance(input_fields, list) and isinstance(transported_fields, list) and isinstance(stripped_fields, list):
            input_set = set(input_fields)
            transported_set = set(transported_fields)
            stripped_set = set(stripped_fields)
            manifested_seen = MANIFESTED_FIELDS.issubset(input_set)
            manifested_stripped = MANIFESTED_FIELDS.issubset(stripped_set) and MANIFESTED_FIELDS.isdisjoint(transported_set)
            wire_only = transported_set.issubset(WIRE_FIELDS)
            checks.extend([
                {"check": "manifested-fields-present-in-hostile-input", "ok": manifested_seen},
                {"check": "manifested-fields-stripped-before-wire-event", "ok": manifested_stripped},
                {"check": "transported-event-is-wire-intent-only", "ok": wire_only},
            ])
            if not manifested_seen:
                failures.append("projection does not retain the donor hostile manifested-field input")
            if not manifested_stripped:
                failures.append("manifested outcome fields survive the bounded wire-intent boundary")
            if not wire_only:
                failures.append("transported event contains a non-wire field")
        elif None not in (input_fields, transported_fields, stripped_fields):
            failures.append("transport boundary field sets must be lists")

    conflict = projection.get("conflictAdjudication")
    if not isinstance(conflict, dict):
        unknowns.append("conflictAdjudication")
    else:
        start = require("conflictAdjudication.startCells", conflict.get("startCells"))
        final = require("conflictAdjudication.finalCells", conflict.get("finalCells"))
        requested = require("conflictAdjudication.requestedDestination", conflict.get("requestedDestination"))
        conflict_count = require("conflictAdjudication.conflictCount", conflict.get("conflictCount"))
        if isinstance(start, dict) and isinstance(final, dict) and requested is not None and conflict_count is not None:
            actors = sorted(set(start) & set(final))
            moved = [actor for actor in actors if start[actor] != final[actor]]
            stayed = [actor for actor in actors if start[actor] == final[actor]]
            exactly_one_winner = len(actors) == 2 and len(moved) == 1 and len(stayed) == 1 and final[moved[0]] == requested
            loser_not_manifested = len(stayed) == 1 and final[stayed[0]] != requested
            one_conflict = conflict_count == 1
            checks.extend([
                {"check": "same-destination-intents-have-one-engine-selected-winner", "ok": exactly_one_winner},
                {"check": "losing-client-direction-does-not-manifest", "ok": loser_not_manifested},
                {"check": "engine-records-conflict", "ok": one_conflict},
            ])
            if not exactly_one_winner:
                failures.append("same-destination conflict does not show exactly one engine-selected movement")
            if not loser_not_manifested:
                failures.append("losing client direction manifested as consequence")
            if not one_conflict:
                failures.append("donor conflict receipt count is not one")
        elif None not in (start, final, requested, conflict_count):
            failures.append("conflict adjudication shape is invalid")

    chronology = projection.get("chronologyRejection")
    if not isinstance(chronology, dict):
        unknowns.append("chronologyRejection")
    else:
        reason = require("chronologyRejection.reason", chronology.get("reason"))
        before = require("chronologyRejection.lastClientSequenceBefore", chronology.get("lastClientSequenceBefore"))
        after = require("chronologyRejection.lastClientSequenceAfter", chronology.get("lastClientSequenceAfter"))
        if None not in (reason, before, after):
            future_rejected = reason == "future_action"
            chronology_unchanged = before == after == 0
            checks.extend([
                {"check": "future-intent-rejected", "ok": future_rejected},
                {"check": "rejected-intent-does-not-advance-accepted-chronology", "ok": chronology_unchanged},
            ])
            if not future_rejected:
                failures.append("future intent was not retained as a rejection")
            if not chronology_unchanged:
                failures.append("rejected future intent changed accepted chronology")

    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(status, checks, sorted(set(unknowns)), failures)


def build_receipt(projection: dict[str, Any]) -> dict[str, Any]:
    result = inspect(projection)
    return {
        "schema": RESULT_SCHEMA,
        "status": result.status,
        "invariant": "INV-06",
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
            "PASS means only that the pinned TruthGrid source/test projection shows client traffic constrained "
            "to causal intent fields, an engine-adjudicated same-destination conflict, and a future intent rejected "
            "without advancing accepted chronology. 'Consequence' here is simulation state/receipt outcome, not "
            "constitutional or CANON authority."
        ),
    }
