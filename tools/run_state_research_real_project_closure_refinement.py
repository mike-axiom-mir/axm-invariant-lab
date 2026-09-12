#!/usr/bin/env python3
"""Generate/check deterministic evidence for the State Research held-out closure refinement."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from adapters.state_research_real_project_closure import inspect
FIXTURE=ROOT/'fixtures'/'state-research-real-project-closure-v1.projection.json'
EVIDENCE=ROOT/'evidence'/'STATE_RESEARCH_REAL_PROJECT_CLOSURE_REFINEMENT.json'

def build_evidence()->dict:
    fixture=json.loads(FIXTURE.read_text(encoding='utf-8'))
    result=inspect(fixture)
    return {
      'schema':'axm.invariant-lab.state-research-real-project-closure-refinement/v0.1',
      'source':fixture['source'],
      'projection':fixture['projection'],
      'invariant':{
        'id':'INV-15',
        'statement':'Runtime-observed dependency evidence must not be treated as closure-complete when a frozen held-out mutation yields a minimized silent-stale counterexample under observed-only routing; absent independent closure evidence, the completeness claim fails.'
      },
      'result':result.to_dict(),
      'observed_boundary':{
        'held_out_manifest_hash':fixture['held_out_manifest_hash'],
        'held_out_mutation_id':fixture['held_out_mutation_id'],
        'observed_only_counterexample_length':result.derived.get('minimized_counterexample_length'),
        'observed_only_completeness_status':result.derived.get('inv_15_observed_only_completeness_status'),
        'declared_risk_independent_detection_control':result.derived.get('declared_risk_independent_detection_control'),
        'donor_necessary_or_missed_fields_used':False
      },
      'truth_boundary':'PASS means the exact pinned donor records support a narrow falsification: observed-only runtime-read closure misses one training-unexposed conditional dependency on the frozen held-out set, with a one-mutation minimized counterexample, while a separately selected declared-risk audit control detects/repairs held-out staleness and ends equal on the same manifest. The donor offline oracle still scores staleness/equality; Invariant Lab does not execute Sentinel, prove the risk policy generally sufficient, or promote model fidelity beyond seed rung 5.'
    }

def render(x): return json.dumps(x,indent=2,sort_keys=True)+'\n'
def main():
    p=argparse.ArgumentParser(); p.add_argument('--check',action='store_true'); a=p.parse_args(); payload=build_evidence(); text=render(payload)
    if a.check:
        if not EVIDENCE.exists(): print(f'missing retained evidence: {EVIDENCE}',file=sys.stderr); return 2
        try: retained=json.loads(EVIDENCE.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e: print(f'invalid retained real-project closure evidence: {e}',file=sys.stderr); return 1
        if retained!=payload: print('retained real-project closure refinement evidence drifted',file=sys.stderr); return 1
        print('State Research real-project closure refinement evidence: PASS'); return 0
    EVIDENCE.parent.mkdir(parents=True,exist_ok=True); EVIDENCE.write_text(text,encoding='utf-8'); print(text,end=''); return 0
if __name__=='__main__': raise SystemExit(main())
