import json
from pathlib import Path
import unittest

from adapters.universal_creation_donor_fidelity import build_receipt, inspect

ROOT = Path(__file__).resolve().parents[1]


class UniversalCreationDonorFidelityTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads((ROOT / "fixtures" / "universal-creation-material-donor-v1.projection.json").read_text(encoding="utf-8"))

    def test_pinned_projection_passes(self):
        result = inspect(self.load_fixture())
        self.assertEqual("PASS", result.status)
        self.assertEqual([], result.failures)
        self.assertEqual([], result.unknowns)

    def test_pack_identity_drift_fails(self):
        fixture = self.load_fixture()
        fixture["completeAdaptation"]["source"]["pack_id"] = "other-pack"
        result = inspect(fixture)
        self.assertEqual("FAIL", result.status)
        self.assertTrue(any("pack/library identity" in failure for failure in result.failures))

    def test_entry_source_metadata_loss_fails(self):
        fixture = self.load_fixture()
        fixture["completeAdaptation"]["acceptedEntries"][0]["source"] = {}
        result = inspect(fixture)
        self.assertEqual("FAIL", result.status)
        self.assertTrue(any("source metadata" in failure for failure in result.failures))

    def test_unassigned_channel_silent_guess_fails(self):
        fixture = self.load_fixture()
        fixture["ambiguousEntry"]["heldEntries"] = []
        result = inspect(fixture)
        self.assertEqual("FAIL", result.status)
        self.assertTrue(any("unassigned" in failure for failure in result.failures))

    def test_missing_ambiguous_evidence_holds(self):
        fixture = self.load_fixture()
        del fixture["ambiguousEntry"]
        result = inspect(fixture)
        self.assertEqual("HOLD", result.status)
        self.assertIn("ambiguousEntry", result.unknowns)

    def test_family_conflict_silent_promotion_fails(self):
        fixture = self.load_fixture()
        fixture["familyConflict"]["acceptedFamilyCount"] = 1
        result = inspect(fixture)
        self.assertEqual("FAIL", result.status)

    def test_rendering_claim_fails(self):
        fixture = self.load_fixture()
        fixture["completeAdaptation"]["renderingVerified"] = True
        result = inspect(fixture)
        self.assertEqual("FAIL", result.status)
        self.assertTrue(any("rendering" in failure for failure in result.failures))

    def test_donor_blob_drift_fails(self):
        fixture = self.load_fixture()
        fixture["donor"]["blobs"]["src/axm_uc/material_donor.py"] = "different"
        result = inspect(fixture)
        self.assertEqual("FAIL", result.status)
        self.assertTrue(any("blob" in failure for failure in result.failures))

    def test_unsupported_version_must_fail_closed(self):
        fixture = self.load_fixture()
        fixture["wrongVersionFailsClosed"] = False
        result = inspect(fixture)
        self.assertEqual("FAIL", result.status)

    def test_receipt_never_grants_authority(self):
        receipt = build_receipt(self.load_fixture())
        self.assertEqual("PASS", receipt["status"])
        self.assertEqual({"execution": False, "merge": False, "promotion": False, "canon": False}, receipt["authority"])

    def test_retained_evidence_matches_exact_projection(self):
        expected = json.loads((ROOT / "evidence" / "UNIVERSAL_CREATION_DONOR_FIDELITY_INV10.json").read_text(encoding="utf-8"))
        self.assertEqual(expected, build_receipt(self.load_fixture()))


if __name__ == "__main__":
    unittest.main()
