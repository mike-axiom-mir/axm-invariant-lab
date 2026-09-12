import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'adapters'/'state_research_unlabeled_multiproject_closure.py'
spec=importlib.util.spec_from_file_location('state_research_unlabeled_multiproject_closure',MODULE_PATH)
adapter=importlib.util.module_from_spec(spec); assert spec.loader; sys.modules[spec.name]=adapter; spec.loader.exec_module(adapter)
FIXTURE=ROOT/'fixtures'/'state-research-unlabeled-multiproject-closure-v1.projection.json'

class UnlabeledMultiProjectClosureTests(unittest.TestCase):
    def load(self): return json.loads(FIXTURE.read_text(encoding='utf-8'))
    def test_valid_projection_separates_final_equality_from_trace_closure(self):
        result=adapter.inspect(self.load())
        self.assertEqual(result.status,'PASS')
        self.assertEqual(result.derived['inv_16_final_equality_only_status'],'FAIL')
        self.assertEqual(result.derived['combined_candidate_trace_closure_status'],'PASS')
        self.assertEqual(result.derived['cross_project_project_count'],2)
        self.assertEqual(result.derived['observed_only_hidden_transient_failures'],8)
    def test_missing_required_field_holds(self):
        f=self.load(); del f['held_out']['manifest_hash']; r=adapter.inspect(f)
        self.assertEqual(r.status,'HOLD'); self.assertIn('held_out.manifest_hash',r.unknowns)
    def test_source_blob_drift_fails(self):
        f=self.load(); f['source']['benchmark_git_blob_sha']='0'*40
        self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_observed_final_equality_without_hidden_stale_does_not_support_falsifier(self):
        f=self.load(); f['observed_reads']['silent_stale_outputs']=0
        self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_candidate_silent_stale_breaks_trace_closure(self):
        f=self.load(); f['combined_candidate']['projects'][0]['silent_stale_outputs']=1
        self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_duplicate_project_cannot_fake_cross_project_coverage(self):
        f=self.load(); f['held_out']['project_ids'][1]=f['held_out']['project_ids'][0]
        self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_untrusted_checkpoint_must_be_quarantined_before_reconstruction(self):
        f=self.load(); f['checkpoint_recovery'][0]['recovery_action']='replay_untrusted'
        self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_candidate_work_must_remain_below_full_oracle_reference(self):
        f=self.load(); f['combined_candidate']['total_policy_check_work']=1955
        self.assertEqual(adapter.inspect(f).status,'FAIL')

if __name__=='__main__': unittest.main()
