#!/usr/bin/env python3
"""Generate/check deterministic evidence for State Research reference-state closure."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from adapters.state_research_reference_state_closure import inspect
FIXTURE = ROOT / 'fixtures' / 'state-research-reference-state-closure-v1.projection.json'
EVIDENCE = ROOT / 'evidence' / 'STATE_RESEARCH_REFERENCE_STATE_CLOSURE_REFINEMENT.json'

def build_evidence() -> dict:
    fixture = json.loads(FIXTURE.read_text(encoding='utf-8'))
    result = inspect(fixture)
    return {
        'schema': 'axm.invariant-lab.state-research-reference-state-closure-refinement/v0.1',
        'source': fixture['source'],
        'projection': fixture['projection'],
        'invariant': {
            'id': 'INV-18',
            'statement': 'A sparse execution may claim dense-oracle equivalence only if still-live contributions from sleeping components remain in shared reference closure; an identical wake set is insufficient when a sleeping reference contribution is dropped.'
        },
        'result': {
            'status': result.status,
            'check_count': len(result.checks),
            'failed_checks': [x['check'] for x in result.checks if not x.get('ok')],
            'unknowns': result.unknowns,
            'failures': result.failures,
            'derived': result.derived,
        },
        'observed_boundary': {
            'fixture_sha256': fixture['baseline']['fixture_sha256'],
            'dense_sparse_replay_digest': fixture['baseline']['replay_digest_A'],
            'same_wake_set_control_divergences': fixture['baseline']['aggressive_control_divergences_A_C'],
            'sleeping_reference_event_wakes': fixture['baseline']['sleeping_reference_event_wakes'],
            'dense_body_executions': fixture['baseline']['dense_body_executions_A'],
            'sparse_body_executions': fixture['baseline']['sparse_body_executions_B'],
            'executions_avoided': fixture['baseline']['executions_avoided_B'],
            'dense_reference_bytes': fixture['baseline']['max_dense_reference_bytes_A'],
            'derived_reference_bytes': fixture['baseline']['max_derived_reference_bytes_B'],
            'fault_status': fixture['dropped_summary_fault']['status'],
            'fault_replay_digest_B': fixture['dropped_summary_fault']['replay_digest_B'],
        },
        'truth_boundary': 'PASS means the exact pinned deterministic State Research reference-state-closure workload supports INV-18 narrowly: sparse body execution matches the dense oracle while sleeping reference contributions remain represented in derived closure; a same-wake-set control that drops a sleeping contribution diverges, and deliberately dropping summary updates HOLDs. This is one inspectable software workload, not arbitrary sparse-scheduler, neural/hardware, producer-authentication, real-environment, or authority proof, and it does not promote general model fidelity beyond seed rung 5.'
    }

def render(value: dict) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + '\n'

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    payload = build_evidence()
    text = render(payload)
    if args.check:
        if not EVIDENCE.exists():
            print(f'missing retained evidence: {EVIDENCE}', file=sys.stderr)
            return 2
        try:
            retained = json.loads(EVIDENCE.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            print(f'invalid retained reference-state closure evidence: {exc}', file=sys.stderr)
            return 1
        if retained != payload:
            print('retained reference-state closure refinement evidence drifted', file=sys.stderr)
            return 1
        print('State Research reference-state closure refinement evidence: PASS')
        return 0
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(text, encoding='utf-8')
    print(text, end='')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
