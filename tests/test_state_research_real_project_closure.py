import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "adapters" / "state_research_real_project_closure.py"
spec = importlib.util.spec_from_file_location("state_research_real_project_closure", MODULE_PATH)
adapter = importlib.util.module_from_spec(spec)
assert spec.loader
sys.modules[spec.name] = adapter
spec.loader.exec_module(adapter)
FIXTURE = ROOT / "fixtures" / "state-research-real-project-closure-v1.projection.json"


class StateResearchRealProjectClosureTests(unittest.TestCase):
    def load(self):
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_valid_projection_falsifies_observed_only_completeness(self):
        result = adapter.inspect(self.load())
        self.assertEqual(result.status, "PASS")
        self.assertEqual(result.derived["inv_15_observed_only_completeness_status"], "FAIL")
        self.assertEqual(result.derived["declared_risk_independent_detection_control"], "PASS")
        self.assertEqual(result.derived["minimized_counterexample_length"], 1)

    def test_unknown_projection_field_holds(self):
        fixture = self.load()
        del fixture["minimized_counterexample"]["observed_mutation_id"]
        result = adapter.inspect(fixture)
        self.assertEqual(result.status, "HOLD")
        self.assertIn("minimized_counterexample.observed_mutation_id", result.unknowns)

    def test_schema_drift_fails(self):
        fixture = self.load()
        fixture["schema"] = "future"
        self.assertEqual(adapter.inspect(fixture).status, "FAIL")

    def test_source_blob_drift_fails(self):
        fixture = self.load()
        fixture["source"]["benchmark_git_blob_sha"] = "0" * 40
        self.assertEqual(adapter.inspect(fixture).status, "FAIL")

    def test_training_exposed_conditional_fault_fails_boundary(self):
        fixture = self.load()
        fixture["conditional_fault"]["training_exposed"] = True
        self.assertEqual(adapter.inspect(fixture).status, "FAIL")

    def test_counterexample_must_remain_one_mutation(self):
        fixture = self.load()
        fixture["minimized_counterexample"]["minimized_length"] = 2
        self.assertEqual(adapter.inspect(fixture).status, "FAIL")

    def test_observed_only_must_retain_silent_stale_failure(self):
        fixture = self.load()
        fixture["observed_reads"]["held_out"]["silent_stale_outputs"] = 0
        self.assertEqual(adapter.inspect(fixture).status, "FAIL")

    def test_declared_risk_control_must_reach_equality(self):
        fixture = self.load()
        fixture["declared_risk"]["gate"]["final_oracle_equality"] = False
        self.assertEqual(adapter.inspect(fixture).status, "FAIL")


if __name__ == "__main__":
    unittest.main()
