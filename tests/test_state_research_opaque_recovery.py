import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'adapters'/'state_research_opaque_recovery.py'
spec=importlib.util.spec_from_file_location('state_research_opaque_recovery',MODULE_PATH)
adapter=importlib.util.module_from_spec(spec); assert spec.loader; sys.modules[spec.name]=adapter; spec.loader.exec_module(adapter)
FIXTURE=ROOT/'fixtures'/'state-research-cross-version-opaque-recovery-v1.projection.json'

class CrossVersionOpaqueRecoveryTests(unittest.TestCase):
    def load(self): return json.loads(FIXTURE.read_text(encoding='utf-8'))
    def test_valid_projection_preserves_version_and_unavailable_source_boundaries(self):
        result=adapter.inspect(self.load())
        self.assertEqual(result.status,'PASS')
        self.assertEqual(result.derived['inv_17_stale_checkpoint_or_semantic_reuse_status'],'FAIL')
        self.assertEqual(result.derived['v2_changed_source_bounded_resolution_status'],'PASS')
        self.assertEqual(result.derived['v3_unavailable_source_fail_closed_status'],'PASS')
        self.assertEqual(result.derived['candidate_explicit_unresolved_decisions'],14)
    def test_missing_required_field_holds(self):
        f=self.load(); del f['challenge']['held_out_manifest_hash']; r=adapter.inspect(f)
        self.assertEqual(r.status,'HOLD'); self.assertIn('challenge.held_out_manifest_hash',r.unknowns)
    def test_source_blob_drift_fails(self):
        f=self.load(); f['source']['provenance_receipts_git_blob_sha']='0'*40
        self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_control_must_retain_stale_replay_counterexample(self):
        f=self.load(); f['failure_controls']['BROKEN_SPARSE']['untrusted_checkpoint_replays']=0
        self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_candidate_wrong_resolved_output_fails(self):
        f=self.load(); f['candidate']['wrong_resolved_outputs']=1
        self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_changed_source_identity_cannot_disappear(self):
        f=self.load(); f['candidate']['projects']['opaque-workcell-v2']['source_changed_since_training']=False
        self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_unavailable_source_must_keep_opaque_dependents_unresolved(self):
        f=self.load(); f['candidate']['projects']['opaque-workcell-v3-unavailable']['final_unresolved_ids']=[]
        self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_unavailable_source_requires_explicit_escalation_receipts(self):
        f=self.load(); f['provenance']['v3_escalation']['receipt_count']=0
        self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_candidate_work_must_remain_below_full_oracle(self):
        f=self.load(); f['candidate']['total_policy_work']=168
        self.assertEqual(adapter.inspect(f).status,'FAIL')

if __name__=='__main__': unittest.main()
