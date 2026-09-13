from __future__ import annotations

import copy
import unittest

from adapters.universal_creation_donor_execution import build_receipt, inspect


def valid_receipt() -> dict:
    return {
        "schema": "axm.universal-creation.material-donor-invariant-receipt/v1",
        "producer": {
            "repository": "mike-axiom-mir/axm-universal-creation",
            "tool": "tools/material_donor_invariant_receipt.py",
            "fixture": "fixtures/material-donor-invariant-probe-v1.json",
            "fixtureSha256": "a" * 64,
            "adapterFormat": "axm-material-donor-pack",
            "adapterVersion": "0.2.0",
        },
        "observations": {
            "complete": {
                "truthStatus": "READY_EXACT_MATERIAL_DONOR_ADAPTER",
                "source": {
                    "format": "axm-material-donor-pack",
                    "version": "0.2.0",
                    "pack_id": "invariant-probe-pack",
                    "exported_at": "2026-09-13T00:00:00Z",
                    "source_library_id": "invariant-probe-library",
                },
                "acceptedEntries": [
                    {
                        "entryId": "probe-base",
                        "channel": "base-color",
                        "source": {"method": "self-made-invariant-probe"},
                    },
                    {
                        "entryId": "probe-roughness",
                        "channel": "roughness",
                        "source": {"method": "self-made-invariant-probe"},
                    },
                ],
                "heldEntryCount": 0,
                "heldFamilyCount": 0,
                "renderingVerified": False,
            },
            "unassigned": {
                "truthStatus": "PARTIAL_EXACT_MATERIAL_DONOR_ADAPTER_WITH_HOLDS",
                "acceptedEntries": [
                    {
                        "entryId": "probe-base",
                        "channel": "base-color",
                        "source": {"method": "self-made-invariant-probe"},
                    },
                    {
                        "entryId": "probe-roughness",
                        "channel": "roughness",
                        "source": {"method": "self-made-invariant-probe"},
                    },
                ],
                "heldEntries": [
                    {
                        "entry_id": "probe-unassigned",
                        "reason": "entry has no supported explicit channel hint",
                        "observed_hint": "unassigned",
                    }
                ],
                "strictRejected": True,
            },
            "familyConflict": {
                "truthStatus": "PARTIAL_EXACT_MATERIAL_DONOR_ADAPTER_WITH_HOLDS",
                "acceptedEntries": [
                    {
                        "entryId": "probe-base",
                        "channel": "base-color",
                        "source": {"method": "self-made-invariant-probe"},
                    },
                    {
                        "entryId": "probe-roughness",
                        "channel": "roughness",
                        "source": {"method": "self-made-invariant-probe"},
                    },
                    {
                        "entryId": "probe-base-duplicate",
                        "channel": "base-color",
                        "source": {"method": "self-made-invariant-probe"},
                    },
                ],
                "acceptedFamilyCount": 0,
                "heldFamilies": [
                    {
                        "family_id": "probe-family",
                        "reason": "family cannot be mapped exactly to one texture per supported channel",
                        "missing_or_held_members": [],
                        "duplicate_channels": ["base-color"],
                    }
                ],
            },
            "unsupportedVersion": {
                "rejected": True,
                "message": "unsupported material donor version",
            },
        },
        "authority": {
            "mayExecute": False,
            "mayMerge": False,
            "mayPromote": False,
            "mayDeclareCanon": False,
        },
        "truthBoundary": {
            "claim": "Executable donor-owned observations for the exact material-donor adapter and bounded probe fixture.",
            "notProven": ["rendering", "constitutional authority"],
        },
    }


class UniversalCreationDonorExecutionTests(unittest.TestCase):
    def test_valid_donor_owned_receipt_passes(self) -> None:
        result = inspect(valid_receipt())
        self.assertEqual(result.status, "PASS")
        self.assertFalse(result.failures)
        self.assertFalse(result.unknowns)

    def test_missing_observation_holds_instead_of_passing(self) -> None:
        receipt = valid_receipt()
        del receipt["observations"]["unassigned"]
        result = inspect(receipt)
        self.assertEqual(result.status, "HOLD")
        self.assertIn("observations.unassigned", result.unknowns)

    def test_authority_escalation_fails(self) -> None:
        receipt = valid_receipt()
        receipt["authority"]["mayPromote"] = True
        result = inspect(receipt)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("authority escalation" in item for item in result.failures))

    def test_source_identity_drift_fails(self) -> None:
        receipt = valid_receipt()
        receipt["observations"]["complete"]["source"]["source_library_id"] = "other-library"
        self.assertEqual(inspect(receipt).status, "FAIL")

    def test_unassigned_silent_promotion_fails(self) -> None:
        receipt = valid_receipt()
        receipt["observations"]["unassigned"]["truthStatus"] = "READY_EXACT_MATERIAL_DONOR_ADAPTER"
        self.assertEqual(inspect(receipt).status, "FAIL")

    def test_family_conflict_silent_acceptance_fails(self) -> None:
        receipt = valid_receipt()
        receipt["observations"]["familyConflict"]["acceptedFamilyCount"] = 1
        self.assertEqual(inspect(receipt).status, "FAIL")

    def test_unsupported_version_fail_open_is_rejected(self) -> None:
        receipt = valid_receipt()
        receipt["observations"]["unsupportedVersion"]["rejected"] = False
        self.assertEqual(inspect(receipt).status, "FAIL")

    def test_provenance_failure_overrides_semantic_pass(self) -> None:
        result = build_receipt(
            copy.deepcopy(valid_receipt()),
            provenance_checks=[{"check": "pinned-donor-commit", "ok": False}],
            provenance_failures=["donor checkout drifted"],
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("donor checkout drifted", result["failures"])
        self.assertTrue(all(value is False for value in result["authority"].values()))


if __name__ == "__main__":
    unittest.main()
