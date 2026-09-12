#!/usr/bin/env python3
"""Generate/check deterministic evidence for Wakeup Fuzzer runtime-observation refinement."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from adapters.state_research_wakeup_fuzzer import inspect
FIXTURE=ROOT/'fixtures'/'state-research-wakeup-fuzzer-v1.projection.json'
EVIDENCE=ROOT/'evidence'/'STATE_RESEARCH_WAKEUP_FUZZER_REFINEMENT.json'

def build_evidence()->dict:
    fixture=json.loads(FIXTURE.read_text(encoding='utf-8'))
    result=inspect(fixture)
    return {
      'schema':'axm.invariant-lab.state-research-wakeup-fuzzer-refinement/v0.1',
      'source':fixture['source'],
      'projection':fixture['projection'],
      'invariant':{
        'id':'INV-14',
        'statement':'When runtime-observed activation identifies a check omitted by declared sparse routing, and that check produces an output change that appears in the sparse mismatch set, sparse oracle-equivalence must be rejected for that transition.'
      },
      'result':result.to_dict(),
      'observed_boundary':{
        'counterexample_trace_count':1,
        'repaired_trace_count':result.derived.get('repaired_trace_count'),
        'repaired_equivalent_trace_count':result.derived.get('repaired_equivalent_trace_count'),
        'oracle_fields_used_for_derivation':False,
        'claim':'one minimized broken donor trace plus four pinned repaired donor transitions'
      },
      'truth_boundary':'PASS means the exact pinned Wakeup Fuzzer records support INV-14 without using donor necessary/missed oracle fields: one omitted wake is triangulated from runtime-observed activation, actual change, and sparse mismatch, while four repaired transitions agree across full-scan, declared-sparse, and observed-read records. It does not prove observed-read instrumentation complete for unseen branches/dynamic reads/concurrency or promote general model fidelity beyond rung 5.'
    }

def render(x): return json.dumps(x,indent=2,sort_keys=True)+'\n'
def main():
    p=argparse.ArgumentParser(); p.add_argument('--check',action='store_true'); a=p.parse_args(); payload=build_evidence(); text=render(payload)
    if a.check:
        if not EVIDENCE.exists(): print(f'missing retained evidence: {EVIDENCE}',file=sys.stderr); return 2
        try: retained=json.loads(EVIDENCE.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e: print(f'invalid retained Wakeup Fuzzer evidence: {e}',file=sys.stderr); return 1
        if retained!=payload: print('retained Wakeup Fuzzer refinement evidence drifted',file=sys.stderr); return 1
        print('State Research Wakeup Fuzzer refinement evidence: PASS'); return 0
    EVIDENCE.parent.mkdir(parents=True,exist_ok=True); EVIDENCE.write_text(text,encoding='utf-8'); print(text,end=''); return 0
if __name__=='__main__': raise SystemExit(main())
