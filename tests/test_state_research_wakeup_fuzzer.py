import copy
import json
from pathlib import Path
import unittest

from adapters.state_research_wakeup_fuzzer import inspect

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "state-research-wakeup-fuzzer-v1.projection.json"


class StateResearchWakeupFuzzerTests(unittest.TestCase):
    def load_fixture(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_runtime_observation_triangulates_omitted_wake_without_necessary_field(self):
        result = inspect(self.load_fixture())
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.failures, [])
        self.assertEqual(result.unknowns, [])
        self.assertEqual(result.derived["counterexample.instrumented_required_ids"], ["check_00000"])
        self.assertEqual(result.derived["inv_14_counterexample_status"], "FAIL")
        self.assertEqual(result.derived["inv_14_repaired_status"], "PASS")
        self.assertEqual(result.derived["repaired_equivalent_trace_count"], 4)

    def test_sparse_claim_cannot_hide_instrumented_wake(self):
        fixture = self.load_fixture()
        fixture["counterexample"]["declared_sparse"]["awakened"].append("check_00000")
        result = inspect(fixture)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("runtime signals" in failure for failure in result.failures))

    def test_observed_change_signal_is_required(self):
        fixture = self.load_fixture()
        fixture["counterexample"]["observed"]["changed"].remove("check_00000")
        result = inspect(fixture)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("runtime signals" in failure for failure in result.failures))

    def test_missing_runtime_observation_holds(self):
        fixture = self.load_fixture()
        del fixture["counterexample"]["observed"]["awakened"]
        result = inspect(fixture)
        self.assertEqual(result.status, "HOLD")
        self.assertIn("counterexample.observed.awakened", result.unknowns)

    def test_repaired_trace_divergence_fails(self):
        fixture = self.load_fixture()
        fixture["repaired_traces"][2]["declared_sparse"]["changed_hash"] = "0" * 64
        result = inspect(fixture)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("repaired transition 2 diverges" in failure for failure in result.failures))

    def test_source_identity_drift_fails(self):
        fixture = self.load_fixture()
        fixture["source"]["trace_git_blob_sha"] = "0" * 40
        result = inspect(fixture)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("source.trace_git_blob_sha" in failure for failure in result.failures))

    def test_adapter_is_read_only(self):
        fixture = self.load_fixture()
        before = copy.deepcopy(fixture)
        inspect(fixture)
        self.assertEqual(fixture, before)


if __name__ == "__main__":
    unittest.main()
