#!/usr/bin/env python3
"""Generate/check deterministic evidence for the State Research unlabeled multi-project closure refinement."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from adapters.state_research_unlabeled_multiproject_closure import inspect
FIXTURE=ROOT/'fixtures'/'state-research-unlabeled-multiproject-closure-v1.projection.json'
EVIDENCE=ROOT/'evidence'/'STATE_RESEARCH_UNLABELED_MULTIPROJECT_CLOSURE_REFINEMENT.json'

def build_evidence()->dict:
    fixture=json.loads(FIXTURE.read_text(encoding='utf-8')); result=inspect(fixture)
    return {
      'schema':'axm.invariant-lab.state-research-unlabeled-multiproject-closure-refinement/v0.1',
      'source':fixture['source'],
      'projection':fixture['projection'],
      'invariant':{
        'id':'INV-16',
        'statement':'A cross-project closure claim is not supported by final equality alone: every held-out project/version must retain zero silent-stale outputs through the trace, and absent/corrupt checkpoints must be quarantined and reconstructed only from verified source with provenance.'
      },
      'result':{
        'status':result.status,
        'check_count':len(result.checks),
        'failed_checks':[x['check'] for x in result.checks if not x.get('ok')],
        'unknowns':result.unknowns,
        'failures':result.failures,
        'derived':result.derived,
      },
      'observed_boundary':{
        'held_out_manifest_hash':fixture['held_out']['manifest_hash'],
        'held_out_project_count':len(fixture['held_out']['project_ids']),
        'held_out_mutation_count':fixture['held_out']['mutation_count'],
        'held_out_contains_declared_risk_labels':fixture['held_out']['contains_declared_risk_labels'],
        'observed_reads_final_oracle_equality':fixture['observed_reads']['final_oracle_equality'],
        'observed_reads_silent_stale_outputs':fixture['observed_reads']['silent_stale_outputs'],
        'combined_candidate_silent_stale_outputs':fixture['combined_candidate']['silent_stale_outputs'],
        'combined_candidate_total_policy_check_work':fixture['combined_candidate']['total_policy_check_work'],
        'full_oracle_reference_work':fixture['combined_candidate']['full_oracle_reference_work'],
        'checkpoint_cases':{x['project_id']:x['checkpoint_case'] for x in fixture['checkpoint_recovery']},
        'donor_necessary_or_missed_fields_used':False,
      },
      'truth_boundary':'PASS means the exact pinned donor records support a narrow cross-project boundary: OBSERVED_READS ends oracle-equal yet retains eight silent-stale outputs across both held-out projects, so final equality alone is insufficient; the separately selected combined structural+observed candidate has zero silent stale outputs on both projects, less counted check work than the full-oracle reference, and fail-closed checkpoint quarantine/reconstruction provenance for one corrupt and one absent checkpoint. The donor offline oracle still scores hidden staleness/equality; Invariant Lab does not execute either donor project, prove the combined policy generally sufficient, or promote general model fidelity beyond seed rung 5.'
    }

def render(x): return json.dumps(x,indent=2,sort_keys=True)+'\n'
def main():
    p=argparse.ArgumentParser(); p.add_argument('--check',action='store_true'); a=p.parse_args(); payload=build_evidence(); text=render(payload)
    if a.check:
        if not EVIDENCE.exists(): print(f'missing retained evidence: {EVIDENCE}',file=sys.stderr); return 2
        try: retained=json.loads(EVIDENCE.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e: print(f'invalid retained unlabeled multi-project evidence: {e}',file=sys.stderr); return 1
        if retained!=payload: print('retained unlabeled multi-project closure refinement evidence drifted',file=sys.stderr); return 1
        print('State Research unlabeled multi-project closure refinement evidence: PASS'); return 0
    EVIDENCE.parent.mkdir(parents=True,exist_ok=True); EVIDENCE.write_text(text,encoding='utf-8'); print(text,end=''); return 0
if __name__=='__main__': raise SystemExit(main())
