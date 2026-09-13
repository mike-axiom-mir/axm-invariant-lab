import copy
import json
from pathlib import Path
import unittest

from adapters.monolith_connected_zip import inspect

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "monolith-connected-zip-v0.3.2.receipt.json"


class MonolithConnectedZipRefinementTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_reference_receipt_passes_without_promotion(self):
        result = inspect(self.load_fixture())
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failures, [])
        self.assertEqual(result.unknowns, [])
        self.assertEqual(result.metrics["endpoint_count"], 23472)
        self.assertEqual(result.metrics["explicit_callable_endpoint_count"], 3)
        self.assertEqual(result.metrics["classified_endpoint_count"], 23472)

    def test_addressable_endpoints_cannot_be_claimed_callable(self):
        receipt = self.load_fixture()
        result = inspect(
            receipt,
            consumer_claim={"callable_endpoint_count": receipt["wiring"]["addressable_endpoint_count"]},
        )
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("callable endpoints" in failure for failure in result.failures))

    def test_addressable_implies_callable_flag_fails(self):
        result = inspect(self.load_fixture(), consumer_claim={"addressable_implies_callable": True})
        self.assertEqual(result.status, "FAIL")
        self.assertIn("consumer promotes addressability to callability", result.failures)

    def test_blocked_endpoint_promotion_fails(self):
        result = inspect(self.load_fixture(), consumer_claim={"blocked_endpoints_are_callable": True})
        self.assertEqual(result.status, "FAIL")
        self.assertIn("consumer promotes explicitly blocked endpoints to callable", result.failures)

    def test_wired_composition_verification_promotion_fails(self):
        result = inspect(self.load_fixture(), consumer_claim={"all_wired_compositions_verified": True})
        self.assertEqual(result.status, "FAIL")
        self.assertIn("consumer promotes wired compositions to verified compositions", result.failures)

    def test_callable_count_disagreement_fails(self):
        receipt = self.load_fixture()
        receipt["wiring"]["source_callable_endpoint_count"] = 4
        result = inspect(receipt)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("callable counts disagree" in failure for failure in result.failures))

    def test_status_partition_mismatch_fails(self):
        receipt = self.load_fixture()
        receipt["wiring"]["adapter_status_counts"]["blocked_missing_callable_binding"] -= 1
        result = inspect(receipt)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("status counts sum" in failure for failure in result.failures))

    def test_missing_callable_evidence_holds(self):
        receipt = self.load_fixture()
        del receipt["wiring"]["source_callable_endpoint_count"]
        result = inspect(receipt)
        self.assertEqual(result.status, "HOLD")
        self.assertIn("wiring.source_callable_endpoint_count", result.unknowns)

    def test_future_status_holds(self):
        receipt = self.load_fixture()
        receipt["wiring"]["adapter_status_counts"]["future_unknown_status"] = 0
        result = inspect(receipt)
        self.assertEqual(result.status, "HOLD")
        self.assertIn("wiring.adapter_status_counts.future_unknown_status", result.unknowns)

    def test_future_schema_holds(self):
        receipt = self.load_fixture()
        receipt["schema"] = "axm.monolith.connected-zip-result/v9"
        result = inspect(receipt)
        self.assertEqual(result.status, "HOLD")
        self.assertTrue(any(item.startswith("unsupported schema:") for item in result.unknowns))

    def test_adapter_is_read_only(self):
        receipt = self.load_fixture()
        before = copy.deepcopy(receipt)
        inspect(receipt, consumer_claim={"callable_endpoint_count": 3})
        self.assertEqual(receipt, before)


if __name__ == "__main__":
    unittest.main()
