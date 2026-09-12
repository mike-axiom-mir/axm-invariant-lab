# AXM Invariant Lab — Action Report v0.9

## Scope

One bounded growth run. The preserved `RESEARCH_SEED_v0.1.md` remains provenance, not a permanent research-only restriction. No generic framework expansion and no evidence-rung promotion were attempted.

## Starting truth

- Starting `main`: `8d249ed352369444acf61c0e87898b559db976aa` (`v0.8`).
- Open PRs at claim time: none.
- Existing non-main branches were prior merged growth lanes; no semantic competitor for held-out observed-read closure was open.
- Exact `main` push workflow at the starting head was green on Python 3.11 and 3.13.
- v0.8 explicitly left observed-read completeness for unseen branches open.

## Chosen advance

State Research experiment 05 supplies the smallest useful falsification of that open question. It imports the real 242-check Workfloor Sentinel contract, freezes a six-mutation held-out set, and retains a minimized one-mutation counterexample for an unseen conditional dependency under the donor's `OBSERVED_READS` policy.

New candidate invariant **INV-15**:

> Runtime-observed dependency evidence must not be treated as closure-complete when a frozen held-out mutation yields a minimized silent-stale counterexample under observed-only routing; absent independent closure evidence, the completeness claim fails.

The adapter pins donor commit and raw Git blobs, excludes donor `necessary_wakes` / `missed_wakes` from the refinement relation, and compares two policies on the exact same frozen held-out manifest:

- `OBSERVED_READS`: one-mutation minimized `held-conditional-negative-timing` counterexample, three silent stale outputs across three transitions, maximum silent window 3, final inequality, conditional check retained in final mismatch set.
- `DECLARED_RISK`: one detected held-out stale output, one learned edge, one provenance-bearing repair, zero silent stale outputs, final equality.

The declared-risk result is retained only as a materially different detection control for this fixture. It is not promoted as a universal solution.

## Changes

- `adapters/state_research_real_project_closure.py`
- `fixtures/state-research-real-project-closure-v1.projection.json`
- `tests/test_state_research_real_project_closure.py`
- `tools/run_state_research_real_project_closure_refinement.py`
- `evidence/STATE_RESEARCH_REAL_PROJECT_CLOSURE_REFINEMENT.json`
- `STATE_RESEARCH_REAL_PROJECT_CLOSURE_REFINEMENT.md`
- `CANDIDATE_INVARIANTS.md` — adds INV-15
- `AXM_MODULE.json` — exposes the bounded held-out-closure falsifier
- CI evidence-drift gate for the new retained receipt

## Local focused evidence

Focused adversarial fixture gate: **8/8 PASS**.

Covered valid projection, missing evidence -> HOLD, schema/source drift -> FAIL, training-exposed substitution -> FAIL, loss of one-mutation minimization -> FAIL, disappearance of observed-only silent staleness -> FAIL, and loss of declared-risk final equality -> FAIL.

## Evidence ceiling

This run intentionally does **not** promote general model fidelity beyond seed rung 5. The donor offline full oracle still scores hidden staleness and final equality. Invariant Lab does not execute Sentinel or reconstruct that oracle. What changed is the truth boundary: v0.8's runtime-observation evidence is now explicitly known **not** to be closure-complete on this pinned held-out real-project trial.

## Four-root check

- **Truth:** records an actual held-out counterexample instead of extrapolating from favorable v0.8 traces.
- **Agency / non-domination:** grants no execution, merge, CANON, installation, device, or network authority.
- **Continuity:** preserves the seed, prior adapters, evidence rungs, donor identities, and v0.8 claim; it narrows that claim rather than rewriting it.
- **Wisdom before speed:** adds one falsifiable ceiling instead of another large verifier or generic solver layer.

Hosted exact-head repository CI is required before merge. If it fails, this lane stays HOLD until the exact failure is resolved without weakening existing boundaries.
