import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
MODULE_PATH=ROOT/'adapters'/'state_research_stateborn_transport.py'
spec=importlib.util.spec_from_file_location('state_research_stateborn_transport',MODULE_PATH)
adapter=importlib.util.module_from_spec(spec); assert spec.loader; sys.modules[spec.name]=adapter; spec.loader.exec_module(adapter)
FIXTURE=ROOT/'fixtures'/'state-research-stateborn-hostile-transport-v1.projection.json'

class StatebornHostileTransportTests(unittest.TestCase):
    def load(self): return json.loads(FIXTURE.read_text(encoding='utf-8'))
    def test_valid_projection_promotes_inv08_on_pinned_boundary(self):
        r=adapter.inspect(self.load()); self.assertEqual(r.status,'PASS')
        self.assertEqual(r.derived['inv_08_state_identity_on_duplicate_status'],'PASS')
        self.assertEqual(r.derived['accepted_only_replay_barrier_status'],'PASS')
        self.assertEqual(r.derived['report_digest_discrepancy_status'],'EXPLICIT_NON_AUTHORITY')
    def test_missing_required_field_holds(self):
        f=self.load(); del f['held_duplicate']['duplicate_no_effect']; r=adapter.inspect(f)
        self.assertEqual(r.status,'HOLD'); self.assertIn('held_duplicate.duplicate_no_effect',r.unknowns)
    def test_source_or_raw_blob_drift_fails(self):
        f=self.load(); f['source']['source_git_blob_sha']='0'*40; self.assertEqual(adapter.inspect(f).status,'FAIL')
        f=self.load(); f['source']['raw_git_blob_sha']='f'*40; self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_duplicate_must_not_create_second_effect(self):
        f=self.load(); f['held_duplicate']['duplicate_no_effect']=False; self.assertEqual(adapter.inspect(f).status,'FAIL')
        f=self.load(); f['held_duplicate']['accepted_packets']=7; self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_duplicate_barrier_is_accepted_only(self):
        f=self.load(); f['source_semantics']['digest_added_only_when_apply_status_applied']=False
        self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_corrupt_refusal_must_not_poison_clean_retry(self):
        f=self.load(); f['held_corrupt_retry']['outcome_matches_expected']=False; self.assertEqual(adapter.inspect(f).status,'FAIL')
        f=self.load(); f['held_corrupt_retry']['duplicates_suppressed']=1; self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_consent_refusal_survives_duplicate_without_commit(self):
        f=self.load(); f['held_consent_refusal']['joint_state_after']=[1,0,0]; self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_report_digest_typo_is_preserved_not_silently_normalized(self):
        f=self.load(); f['fixture_identity']['report_printed_digest']=f['fixture_identity']['source_frozen_digest']
        self.assertEqual(adapter.inspect(f).status,'FAIL')
        f=self.load(); f['fixture_identity']['report_digest_matches_source']=True
        self.assertEqual(adapter.inspect(f).status,'FAIL')
    def test_aggregate_replay_and_duplicate_gate_must_hold(self):
        f=self.load(); f['aggregate']['all_replay']=False; self.assertEqual(adapter.inspect(f).status,'FAIL')
        f=self.load(); f['aggregate']['all_duplicates_no_effect']=False; self.assertEqual(adapter.inspect(f).status,'FAIL')

if __name__=='__main__': unittest.main()
