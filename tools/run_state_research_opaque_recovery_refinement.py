#!/usr/bin/env python3
"""Generate/check deterministic evidence for cross-version opaque recovery refinement."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from adapters.state_research_opaque_recovery import inspect
FIXTURE=ROOT/'fixtures'/'state-research-cross-version-opaque-recovery-v1.projection.json'
EVIDENCE=ROOT/'evidence'/'STATE_RESEARCH_CROSS_VERSION_OPAQUE_RECOVERY_REFINEMENT.json'

def build_evidence()->dict:
    fixture=json.loads(FIXTURE.read_text(encoding='utf-8')); result=inspect(fixture)
    return {
      'schema':'axm.invariant-lab.state-research-cross-version-opaque-recovery-refinement/v0.1',
      'source':fixture['source'],
      'projection':fixture['projection'],
      'invariant':{
        'id':'INV-17',
        'statement':'Opaque evaluator results/checkpoints must not cross evaluator-source identity changes as if semantics were unchanged; changed available source needs grounded re-execution/compatibility evidence, while unavailable source keeps affected outputs explicitly unresolved and escalated rather than reconstructing unknown semantics.'
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
        'held_out_manifest_hash':fixture['challenge']['held_out_manifest_hash'],
        'broken_sparse_wrong_resolved_outputs':fixture['failure_controls']['BROKEN_SPARSE']['wrong_resolved_outputs'],
        'broken_sparse_untrusted_checkpoint_replays':fixture['failure_controls']['BROKEN_SPARSE']['untrusted_checkpoint_replays'],
        'observed_only_wrong_resolved_outputs':fixture['failure_controls']['OBSERVED_ONLY']['wrong_resolved_outputs'],
        'structural_only_wrong_resolved_outputs':fixture['failure_controls']['STRUCTURAL_ONLY']['wrong_resolved_outputs'],
        'candidate_wrong_resolved_outputs':fixture['candidate']['wrong_resolved_outputs'],
        'candidate_resolved_coverage_percentage':fixture['candidate']['resolved_coverage_percentage'],
        'candidate_policy_work':fixture['candidate']['total_policy_work'],
        'full_oracle_reference_work':fixture['candidate']['full_oracle_reference_work'],
        'v3_final_unresolved_ids':fixture['candidate']['projects']['opaque-workcell-v3-unavailable']['final_unresolved_ids'],
        'v3_escalation_receipt_count':fixture['provenance']['v3_escalation']['receipt_count'],
        'donor_oracle_answers_or_opaque_code_used':False,
      },
      'truth_boundary':'PASS means the exact pinned synthetic State Research challenge supports one narrow version/provenance boundary: a v1-bound checkpoint is invalidated when evaluator source identity changes; the changed available v2 evaluator is handled by bounded guard execution without wrong resolved outputs; when v3 source is unavailable, opaque-guard and safety-summary remain explicitly unresolved with escalation receipts instead of reconstructed semantics. The donor offline oracle still scores correctness, and Invariant Lab does not execute donor evaluators, infer the hidden dependency, prove the version-aware policy generally sufficient, or promote general model fidelity beyond seed rung 5.'
    }

def render(x): return json.dumps(x,indent=2,sort_keys=True)+'\n'
def main():
    p=argparse.ArgumentParser(); p.add_argument('--check',action='store_true'); a=p.parse_args(); payload=build_evidence(); text=render(payload)
    if a.check:
        if not EVIDENCE.exists(): print(f'missing retained evidence: {EVIDENCE}',file=sys.stderr); return 2
        try: retained=json.loads(EVIDENCE.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e: print(f'invalid retained cross-version opaque recovery evidence: {e}',file=sys.stderr); return 1
        if retained!=payload: print('retained cross-version opaque recovery refinement evidence drifted',file=sys.stderr); return 1
        print('State Research cross-version opaque recovery refinement evidence: PASS'); return 0
    EVIDENCE.parent.mkdir(parents=True,exist_ok=True); EVIDENCE.write_text(text,encoding='utf-8'); print(text,end=''); return 0
if __name__=='__main__': raise SystemExit(main())
