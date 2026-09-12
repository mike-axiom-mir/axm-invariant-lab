import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'adapters'/'state_research_stateborn_checkpoint.py'
spec=importlib.util.spec_from_file_location('state_research_stateborn_checkpoint',MODULE_PATH)
adapter=importlib.util.module_from_spec(spec); assert spec.loader; sys.modules[spec.name]=adapter; spec.loader.exec_module(adapter)
FIXTURE=ROOT/'fixtures'/'state-research-stateborn-checkpoint-continuity-v1.projection.json'

class StatebornCheckpointContinuityTests(unittest.TestCase):
    def load(self): return json.loads(FIXTURE.read_text(encoding='utf-8'))
    def test_valid_projection_promotes_inv09_on_pinned_boundary(self):
        r=adapter.inspect(self.load()); self.assertEqual(r.status,'PASS')
        self.assertEqual(r.derived['inv_09_fresh_process_checkpoint_binding_status'],'PASS')
        self.assertEqual(r.derived['outer_digest_only_integrity_status'],'FAIL')
        self.assertEqual(r.derived['resealed_inner_tamper_status'],'HOLD')
    def test_missing_required_field_holds(self):
        f=self.load(); del f['positive']['engine_state_digest_equal']; r=adapter.inspect(f)
        self.assertEqual(r.status,'HOLD'); self.assertIn('positive.engine_state_digest_equal',r.unknowns)
    def test_source_blob_drift_fails(self):
        f=self.load(); f['source']['test_git_blob_sha']='0'*40; self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_hosted_run_must_match_exact_donor_head(self):
        f=self.load(); f['source']['hosted_run_head']='f'*40; self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_fresh_process_must_equal_local_receipt(self):
        f=self.load(); f['positive']['fresh_receipt_equal_local']=False; self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_resealed_inner_tamper_must_hold_on_replay(self):
        f=self.load(); f['tamper_control']['fresh_status']='PASS'; self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_verification_never_grants_resume_or_canon(self):
        f=self.load(); f['positive']['authority']['automaticResume']=True; self.assertEqual(adapter.inspect(f).status,'FAIL')
        f=self.load(); f['tamper_control']['authority']['canon']=True; self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_process_adapter_keeps_bounded_admission(self):
        f=self.load(); f['admission']['max_input_bytes']=0; self.assertEqual(adapter.inspect(f).status,'FAIL')

if __name__=='__main__': unittest.main()
