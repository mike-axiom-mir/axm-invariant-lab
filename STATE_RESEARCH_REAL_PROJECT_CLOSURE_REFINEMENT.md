# State Research real-project closure refinement v0.1

This refinement records a **ceiling**, not a promotion.

## INV-15

> Runtime-observed dependency evidence must not be treated as closure-complete when a frozen held-out mutation yields a minimized silent-stale counterexample under observed-only routing; absent independent closure evidence, the completeness claim fails.

## Pinned donor evidence

Repository: `mike-axiom-mir/axm-state-research`

Commit: `cf891d3614d472b1426fbdc4304e4e9fe290fb24`

Raw sources:

- `experiments/05-real-project-closure-trial/results/raw/benchmark_results.json` — Git blob `f7107a348a6e3a328d16d3d149c0438faeb14a21`
- `experiments/05-real-project-closure-trial/results/raw/counterexamples.json` — Git blob `ee0b01e07319721a2bd9e7afe7a1f30ebcba7317`

The projection explicitly excludes donor `necessary_wakes` and `missed_wakes` from this refinement relation.

## What the held-out trial says

The planted conditional-read fault was marked `training_exposed: false`. On the frozen held-out manifest, `OBSERVED_READS` ended with three silent stale outputs across three transitions, a maximum silent window of three, final oracle inequality, and the conditional check still in the final mismatch set. The donor minimizer reduces that policy/check failure to the single mutation `held-conditional-negative-timing`.

On that same held-out manifest, the separately selected `DECLARED_RISK` policy detected one stale output, learned one edge, performed one provenance-bearing repair, retained zero silent stale outputs, and ended at final oracle equality.

Invariant Lab therefore treats **observed-only closure completeness as FAIL for this exact pinned trial**. The declared-risk result is an independent detection control for this fixture; it is not promoted into a universal policy.

## Truth boundary

The donor's offline full oracle still determines hidden staleness and final equality. Invariant Lab does not execute Workfloor Sentinel, reconstruct its oracle, prove that risk tags are sufficient generally, or prove read instrumentation complete. This result falsifies a stronger completeness interpretation of observed-read evidence; it does not raise general model fidelity beyond seed rung 5.

The practical consequence for AXM is narrow: runtime-observed reads are useful evidence, but **unseen branches remain a reason to require independent closure evidence or HOLD** rather than silently upgrading observation into proof.
