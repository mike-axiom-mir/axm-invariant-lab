#!/usr/bin/env python3
"""Generate/check deterministic evidence for Stateborn hostile-transport INV-08 refinement."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from adapters.state_research_stateborn_transport import inspect
FIXTURE=ROOT/'fixtures'/'state-research-stateborn-hostile-transport-v1.projection.json'
EVIDENCE=ROOT/'evidence'/'STATE_RESEARCH_STATEBORN_TRANSPORT_REFINEMENT.json'

def build_evidence()->dict:
    fixture=json.loads(FIXTURE.read_text(encoding='utf-8')); result=inspect(fixture)
    return {
      'schema':'axm.invariant-lab.state-research-stateborn-transport-refinement/v0.1',
      'source':fixture['source'],
      'projection':fixture['projection'],
      'invariant':{
        'id':'INV-08',
        'statement':'Deterministic duplicate execution should agree on the declared state identity; on this donor boundary, only accepted state effects may install the duplicate/replay barrier.'
      },
      'result':{
        'status':result.status,'check_count':len(result.checks),
        'failed_checks':[x['check'] for x in result.checks if not x.get('ok')],
        'unknowns':result.unknowns,'failures':result.failures,'derived':result.derived,
      },
      'observed_boundary':{
        'frozen_fixture_digest':fixture['fixture_identity']['source_frozen_digest'],
        'report_printed_digest':fixture['fixture_identity']['report_printed_digest'],
        'report_digest_matches_source':fixture['fixture_identity']['report_digest_matches_source'],
        'held_duplicate_suppressed':fixture['held_duplicate']['duplicates_suppressed'],
        'held_duplicate_no_effect':fixture['held_duplicate']['duplicate_no_effect'],
        'consent_refusal_joint_state_after':fixture['held_consent_refusal']['joint_state_after'],
        'corrupt_retry_tamper_refusals':fixture['held_corrupt_retry']['tamper_refusals'],
        'corrupt_retry_outcome_matches_expected':fixture['held_corrupt_retry']['outcome_matches_expected'],
        'aggregate_duplicates_suppressed':fixture['aggregate']['total_duplicates_suppressed'],
      },
      'truth_boundary':'PASS means the exact pinned deterministic Stateborn v0.7 hostile-transport source/test/raw-evidence relation supports INV-08 narrowly: an already accepted packet digest is suppressed before a second state effect, while rejected/corrupt attempts do not install the replay barrier. The donor prose report contains a one-character frozen-fixture digest mismatch; source and raw gate identity agree and remain authoritative for this projection. This is not real-network exactly-once delivery, peer-authentication, concurrent-writer, durable-crash, or CANON proof, and it does not promote general model fidelity beyond seed rung 5.'
    }

def render(x): return json.dumps(x,indent=2,sort_keys=True)+'\n'
def main():
    p=argparse.ArgumentParser(); p.add_argument('--check',action='store_true'); a=p.parse_args(); payload=build_evidence(); text=render(payload)
    if a.check:
        if not EVIDENCE.exists(): print(f'missing retained evidence: {EVIDENCE}',file=sys.stderr); return 2
        try: retained=json.loads(EVIDENCE.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e: print(f'invalid retained Stateborn transport evidence: {e}',file=sys.stderr); return 1
        if retained!=payload: print('retained Stateborn transport refinement evidence drifted',file=sys.stderr); return 1
        print('State Research Stateborn hostile-transport refinement evidence: PASS'); return 0
    EVIDENCE.parent.mkdir(parents=True,exist_ok=True); EVIDENCE.write_text(text,encoding='utf-8'); print(text,end=''); return 0
if __name__=='__main__': raise SystemExit(main())
