import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / 'adapters' / 'state_research_reference_state_closure.py'
spec = importlib.util.spec_from_file_location('state_research_reference_state_closure', MODULE_PATH)
adapter = importlib.util.module_from_spec(spec)
assert spec.loader
sys.modules[spec.name] = adapter
spec.loader.exec_module(adapter)
FIXTURE = ROOT / 'fixtures' / 'state-research-reference-state-closure-v1.projection.json'

class ReferenceStateClosureTests(unittest.TestCase):
    def load(self):
        return json.loads(FIXTURE.read_text(encoding='utf-8'))

    def test_valid_projection_promotes_inv18_on_pinned_boundary(self):
        result = adapter.inspect(self.load())
        self.assertEqual(result.status, 'PASS')
        self.assertEqual(result.derived['inv_18_reference_state_closure_status'], 'PASS')
        self.assertEqual(result.derived['same_wake_set_negative_control_status'], 'PASS')
        self.assertEqual(result.derived['body_executions_avoided'], 86)

    def test_missing_required_field_holds(self):
        fixture = self.load()
        del fixture['baseline']['sleeping_reference_event_wakes']
        result = adapter.inspect(fixture)
        self.assertEqual(result.status, 'HOLD')
        self.assertIn('baseline.sleeping_reference_event_wakes', result.unknowns)

    def test_source_and_fixture_blob_drift_fail(self):
        fixture = self.load()
        fixture['source']['experiment_git_blob_sha'] = '0' * 40
        self.assertEqual(adapter.inspect(fixture).status, 'FAIL')
        fixture = self.load()
        fixture['source']['fixture_git_blob_sha'] = 'f' * 40
        self.assertEqual(adapter.inspect(fixture).status, 'FAIL')

    def test_dense_sparse_equivalence_must_hold(self):
        fixture = self.load()
        fixture['baseline']['canonical_output_equality_A_B'] = False
        self.assertEqual(adapter.inspect(fixture).status, 'FAIL')
        fixture = self.load()
        fixture['baseline']['replay_digest_B'] = '0' * 64
        self.assertEqual(adapter.inspect(fixture).status, 'FAIL')

    def test_same_wake_set_control_must_diverge(self):
        fixture = self.load()
        fixture['baseline']['aggressive_control_divergences_A_C'] = 0
        self.assertEqual(adapter.inspect(fixture).status, 'FAIL')
        fixture = self.load()
        fixture['semantics']['control_uses_same_wake_set_as_sparse'] = False
        self.assertEqual(adapter.inspect(fixture).status, 'FAIL')

    def test_reference_only_change_must_not_require_body_wake(self):
        fixture = self.load()
        fixture['baseline']['sleeping_reference_event_wakes'] = ['archive']
        self.assertEqual(adapter.inspect(fixture).status, 'FAIL')
        fixture = self.load()
        fixture['semantics']['reference_only_change_wakes_no_body'] = False
        self.assertEqual(adapter.inspect(fixture).status, 'FAIL')

    def test_dropped_summary_fault_must_break_equivalence(self):
        fixture = self.load()
        fixture['dropped_summary_fault']['status'] = 'PASS'
        self.assertEqual(adapter.inspect(fixture).status, 'FAIL')
        fixture = self.load()
        fixture['dropped_summary_fault']['canonical_output_equality_A_B'] = True
        self.assertEqual(adapter.inspect(fixture).status, 'FAIL')

    def test_work_reduction_is_evidence_not_authority(self):
        fixture = self.load()
        fixture['baseline']['sparse_body_executions_B'] = 104
        self.assertEqual(adapter.inspect(fixture).status, 'FAIL')
        fixture = self.load()
        fixture['semantics']['packaging_grants_no_automatic_authority'] = False
        self.assertEqual(adapter.inspect(fixture).status, 'FAIL')

    def test_reference_state_closure_is_machine_discoverable(self):
        module = json.loads((ROOT / 'AXM_MODULE.json').read_text(encoding='utf-8'))
        capability_ids = {item['id'] for item in module['capabilities']}
        self.assertIn('invariant.refinement.state-research-reference-state-closure', capability_ids)
        paths = {item['path'] for item in module['entrypoints']}
        self.assertIn('adapters/state_research_reference_state_closure.py', paths)
        self.assertIn('tools/run_state_research_reference_state_closure_refinement.py', paths)

if __name__ == '__main__':
    unittest.main()
