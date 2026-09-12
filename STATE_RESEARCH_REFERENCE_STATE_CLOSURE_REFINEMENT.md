# State Research reference-state closure refinement

**Status:** working bounded refinement / INV-18 / seed evidence ceiling rung 5 / not CANON.

This capability pins `mike-axiom-mir/axm-state-research` at commit `cf891d3614d472b1426fbdc4304e4e9fe290fb24` and refines the exact `experiments/reference-state-closure-v1` workload without importing donor authority.

## Question

Can sparse execution preserve dense-oracle output when a component stays asleep but still contributes to shared normalization/reference state?

The donor experiment is unusually useful for this question because its negative control uses **the same body wake set** as the working sparse engine. The difference is reference closure: the working engine keeps a derived total containing still-live sleeping contributions; the negative control drops one sleeping contribution.

## Pinned result

On the exact 8-node / 12-transition fixture:

- dense oracle A executes 104 bodies;
- sparse closure engine B executes 18, avoiding 86 body executions;
- A and B produce the same replay digest: `31882bcce06d84826ce3112a6538913c3cdcfc9b35f4c149e672a86c85fdf9a0`;
- the reference-only `sleeping-reference-change` event wakes **zero bodies**;
- same-wake-set control C diverges from A on 11 transitions and records 11 missed sleeping reference contributions;
- the retained injected `drop-reference-summary-update` fault makes A/B equality false and returns donor status HOLD;
- the maximum explicit reference encoding is 119 bytes while the derived reference-total encoding is 23 bytes on this fixture.

The important result is semantic, not a speed claim: wake-set correctness alone is insufficient when sleeping components still participate in shared/reference state.

## INV-18

> A sparse execution may claim dense-oracle equivalence only if still-live contributions from sleeping components remain in shared reference closure; an identical wake set is insufficient when a sleeping reference contribution is dropped.

This is distinct from INV-13/INV-14. Those refinements ask whether required bodies/checks were awakened. INV-18 covers the case where the wake set is intentionally unchanged and correctness instead depends on preserving shared state contributed by sleeping components.

## Evidence and provenance

The adapter pins the donor README, experiment source, fixture, experiment tests, portable runner, and portable tests by exact Git blob identity. The projected deterministic outputs were independently reproduced from the pinned experiment semantics before retention in this repository. Missing required evidence HOLDs; known contradictory values or source identity drift FAIL.

The donor's portable runner is also kept inside the boundary: internal archive consistency is not producer authentication, and packaging grants no automatic execution, installation, merge, selection, or CANON authority.

## Truth boundary

A PASS establishes only this inspectable deterministic software workload. It does **not** prove arbitrary sparse routing, neural or hardware behavior, wall-clock performance, all donor runtimes, producer identity/authentication, real-environment behavior, or any constitutional/technical authority.

General model fidelity therefore remains at seed rung 5 / CROSS-IMPLEMENTATION. This capability does not borrow the counterexample packet's separate rung-6 external-consumption status.
