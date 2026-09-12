#!/usr/bin/env python3
"""Generate/check deterministic evidence for Stateborn checkpoint continuity refinement."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from adapters.state_research_stateborn_checkpoint import inspect
FIXTURE=ROOT/'fixtures'/'state-research-stateborn-checkpoint-continuity-v1.projection.json'
EVIDENCE=ROOT/'evidence'/'STATE_RESEARCH_STATEBORN_CHECKPOINT_REFINEMENT.json'

def build_evidence()->dict:
    fixture=json.loads(FIXTURE.read_text(encoding='utf-8')); result=inspect(fixture)
    return {
      'schema':'axm.invariant-lab.state-research-stateborn-checkpoint-refinement/v0.1',
      'source':fixture['source'],
      'projection':fixture['projection'],
      'invariant':{
        'id':'INV-09',
        'statement':'Detached checkpoint reconstruction must bind to the checkpoint/source identity it claims to reconstruct; an outer seal alone cannot make altered inner receipt history trusted.'
      },
      'result':{
        'status':result.status,'check_count':len(result.checks),
        'failed_checks':[x['check'] for x in result.checks if not x.get('ok')],
        'unknowns':result.unknowns,'failures':result.failures,'derived':result.derived,
      },
      'observed_boundary':{
        'fixture_id':fixture['positive']['fixture_id'],
        'fresh_receipt_equal_local':fixture['positive']['fresh_receipt_equal_local'],
        'positive_checkpoint_digest_equal':fixture['positive']['checkpoint_digest_equal'],
        'positive_engine_receipt_ids_equal':fixture['positive']['engine_receipt_ids_equal'],
        'positive_engine_state_digest_equal':fixture['positive']['engine_state_digest_equal'],
        'tamper_outer_checkpoint_resealed':fixture['tamper_control']['outer_checkpoint_resealed'],
        'tamper_result':fixture['tamper_control']['fresh_status'],
        'tamper_reason_code':fixture['tamper_control']['reason_code'],
        'hosted_node_versions':fixture['source']['hosted_node_versions'],
        'automatic_resume_authority':fixture['positive']['authority']['automaticResume'],
        'canon_authority':fixture['positive']['authority']['canon'],
      },
      'truth_boundary':'PASS means the exact pinned Stateborn checkpoint-v2 regression supports INV-09 on one narrow boundary: serialized checkpoint-owned state-language evidence verifies identically in a fresh Node process, and changing an inner receipt remains HOLD/CHECKPOINT_REPLAY even after recomputing the outer checkpoint digest. The evidence does not prove complete transport-session resume, durable persistence/crash atomicity, producer authentication/authorship, hostile-peer security, or CANON authority, and it does not promote general model fidelity beyond seed rung 5.'
    }

def render(x): return json.dumps(x,indent=2,sort_keys=True)+'\n'
def main():
    p=argparse.ArgumentParser(); p.add_argument('--check',action='store_true'); a=p.parse_args(); payload=build_evidence(); text=render(payload)
    if a.check:
        if not EVIDENCE.exists(): print(f'missing retained evidence: {EVIDENCE}',file=sys.stderr); return 2
        try: retained=json.loads(EVIDENCE.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e: print(f'invalid retained Stateborn checkpoint evidence: {e}',file=sys.stderr); return 1
        if retained!=payload: print('retained Stateborn checkpoint refinement evidence drifted',file=sys.stderr); return 1
        print('State Research Stateborn checkpoint refinement evidence: PASS'); return 0
    EVIDENCE.parent.mkdir(parents=True,exist_ok=True); EVIDENCE.write_text(text,encoding='utf-8'); print(text,end=''); return 0
if __name__=='__main__': raise SystemExit(main())
