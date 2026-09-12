# AXM Invariant Lab — Action Report v1.1

## Bounded question

Can Invariant Lab strengthen execution-evidence fidelity without recreating donor code by checking a cross-version opaque-evaluator boundary already frozen in AXM State Research Experiment 07?

## Starting state

- base: `main` at `6597d878c922a6393f787a814d04c583a0d73b91`;
- open PR scan: none;
- branch scan: only completed historical growth lanes plus `main`;
- exact-base `invariant-lab-tests` run: SUCCESS;
- preserved `RESEARCH_SEED_v0.1.md` remains provenance, not a research-only restriction;
- existing strongest adjacent capability: INV-16 unlabeled two-project trace closure over State Research Experiment 06.

No semantic overlap was found with an active lane. Experiment 07 attacks a distinct unresolved assumption: evaluator semantics can change while public shape stays stable, and a later evaluator may be unavailable entirely.

## Change

Added **INV-17** and a read-only refinement capability over the pinned State Research Cross-Version Opaque Recovery challenge:

- `adapters/state_research_opaque_recovery.py`;
- `fixtures/state-research-cross-version-opaque-recovery-v1.projection.json`;
- `tests/test_state_research_opaque_recovery.py`;
- `tools/run_state_research_opaque_recovery_refinement.py`;
- retained deterministic evidence;
- `STATE_RESEARCH_CROSS_VERSION_OPAQUE_RECOVERY_REFINEMENT.md`;
- CI drift check and machine-readable capability discovery.

## Falsifiable result

The donor retains three distinct failure controls relevant to the boundary:

- stale sparse reuse: 6 wrong resolved outputs plus one untrusted checkpoint replay;
- observed-only: 4 wrong resolved outputs;
- structural-only: 4 wrong resolved outputs.

The selected version-aware candidate has 0 wrong resolved outputs and 0 untrusted replays at 91.6667% resolved coverage with 41 counted operations versus 168 full-oracle executions. Its v2 source-hash mismatch invalidates the v1-bound checkpoint. Its source-unavailable v3 path keeps exactly `opaque-guard` and `safety-summary` unresolved and emits seven explicit escalation receipts instead of reconstructing missing semantics.

The adapter fails closed on contradictory evidence and HOLDs on missing required evidence.

## Evidence and limitations

Focused local adapter tests before publication: **9/9 PASS**. Deterministic retained evidence generation/check: **PASS**.

The donor oracle still supplies correctness scoring. The fixture is synthetic, contains 12 nodes per project and 12 held-out transitions, and does not establish source-hash semantic completeness, performance scaling, production behavior, security isolation, or arbitrary cross-version compatibility. General model fidelity therefore remains capped at seed rung 5.

## Four-root review

- **Truth:** exact donor commit/path/blob provenance retained; oracle and synthetic-fixture boundaries stated; missing evidence HOLDs.
- **Agency / non-domination:** no authority is derived; read-only inspection only.
- **Continuity:** evaluator-source change, stale-checkpoint invalidation, unavailable-source state, and escalation provenance remain explicit.
- **Wisdom before speed:** this reuses one frozen donor challenge rather than adding a solver, generic version framework, or copied evaluator.

## Next bounded frontier

Do not add more Experiment 07 traces merely to increase sample count. A meaningful next step requires a different failure axis: e.g. the donor's budgeted opaque-version swarm, signed/runtime-generated dependency receipts, or another real implementation where evaluator identity and fallback budget can be checked without importing its semantics. If no such grounded evidence exists, HOLD is preferable to framework growth.
