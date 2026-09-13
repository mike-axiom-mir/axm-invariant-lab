import json
from pathlib import Path
import unittest

from adapters.truthgrid_client_intent import build_receipt, inspect

ROOT = Path(__file__).resolve().parents[1]


class TruthGridClientIntentRefinementTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads((ROOT / "fixtures" / "truthgrid-client-intent-v1.projection.json").read_text(encoding="utf-8"))

    def test_pinned_projection_passes(self):
        result = inspect(self.load_fixture())
        self.assertEqual("PASS", result.status)
        self.assertEqual([], result.failures)
        self.assertEqual([], result.unknowns)

    def test_manifested_outcome_field_on_wire_fails(self):
        fixture = self.load_fixture()
        fixture["transportBoundary"]["transportedFields"].append("damage")
        result = inspect(fixture)
        self.assertEqual("FAIL", result.status)
        self.assertTrue(any("manifested" in failure or "non-wire" in failure for failure in result.failures))

    def test_same_destination_both_manifest_fails(self):
        fixture = self.load_fixture()
        fixture["conflictAdjudication"]["finalCells"]["B"] = "5,4"
        result = inspect(fixture)
        self.assertEqual("FAIL", result.status)

    def test_loser_direction_manifest_fails(self):
        fixture = self.load_fixture()
        fixture["conflictAdjudication"]["finalCells"] = {"A": "4,4", "B": "5,4"}
        fixture["conflictAdjudication"]["conflictCount"] = 0
        result = inspect(fixture)
        self.assertEqual("FAIL", result.status)

    def test_future_intent_advancing_chronology_fails(self):
        fixture = self.load_fixture()
        fixture["chronologyRejection"]["lastClientSequenceAfter"] = 1
        result = inspect(fixture)
        self.assertEqual("FAIL", result.status)

    def test_missing_conflict_evidence_holds(self):
        fixture = self.load_fixture()
        del fixture["conflictAdjudication"]
        result = inspect(fixture)
        self.assertEqual("HOLD", result.status)
        self.assertIn("conflictAdjudication", result.unknowns)

    def test_donor_blob_drift_fails(self):
        fixture = self.load_fixture()
        fixture["donor"]["blobs"]["src/core/engine.js"] = "different"
        result = inspect(fixture)
        self.assertEqual("FAIL", result.status)
        self.assertTrue(any("blob" in failure for failure in result.failures))

    def test_receipt_never_grants_authority(self):
        receipt = build_receipt(self.load_fixture())
        self.assertEqual("PASS", receipt["status"])
        self.assertEqual({"execution": False, "merge": False, "promotion": False, "canon": False}, receipt["authority"])

    def test_retained_evidence_matches_exact_projection(self):
        expected = json.loads((ROOT / "evidence" / "TRUTHGRID_CLIENT_INTENT_REFINEMENT.json").read_text(encoding="utf-8"))
        self.assertEqual(expected, build_receipt(self.load_fixture()))


if __name__ == "__main__":
    unittest.main()
