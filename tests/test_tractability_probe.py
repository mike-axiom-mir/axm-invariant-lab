import unittest

from src.tractability_probe import PATH_NODE_BUDGET, build_tractability_receipt, run_probe


class TractabilityProbeTests(unittest.TestCase):
    def test_reference_is_complete_at_depth_15(self):
        case = run_probe(15)
        self.assertEqual(case["primaryStatus"], "PASS")
        self.assertEqual(case["primaryUniqueStates"], 16)
        self.assertTrue(case["referenceComplete"])
        self.assertEqual(case["referenceStatus"], "PASS")
        self.assertEqual(case["referencePathNodes"], 65_535)
        self.assertEqual(case["referenceUniqueStates"], 16)

    def test_reference_holds_when_depth_16_exceeds_budget(self):
        case = run_probe(16)
        self.assertEqual(case["primaryStatus"], "PASS")
        self.assertEqual(case["primaryUniqueStates"], 17)
        self.assertFalse(case["referenceComplete"])
        self.assertEqual(case["referenceStatus"], "HOLD")
        self.assertEqual(case["referencePathNodes"], PATH_NODE_BUDGET)
        self.assertEqual(case["referenceUniqueStates"], 17)

    def test_receipt_records_observed_boundary_without_timing_claim(self):
        receipt = build_tractability_receipt()
        self.assertEqual(receipt["largestCompleteReferenceDepth"], 15)
        self.assertEqual(receipt["firstIncompleteReferenceDepth"], 16)
        self.assertIn("no wall-clock", receipt["measurement"])
        self.assertIn("does not predict arbitrary AXM model size", receipt["truthBoundary"])


if __name__ == "__main__":
    unittest.main()
