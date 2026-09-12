# AXM Invariant Lab — Action Report v1.8

## Decision

**GROW / repair one bounded model defect and challenge a second invariant with Z3; no evidence-rung promotion.**

The previous run established the first mature formal-tool comparison on INV-01. This run first challenged whether a materially different existing model remained truthful when the bound was extended by one legal post-rollback step.

## Defect discovered

`models/rollback_continuity.py` previously left a successful rollback receipt active forever. The retained default bound ended at depth 4, exactly when rollback completed, so the nominally safe relation passed. At depth 5 a normal legal forward mutation changed `current` to S2 while the old receipt still asserted restored S1, causing the invariant to fail.

That was a bounded-model lifecycle defect, not a donor-system defect.

## Repair

The rollback field is now explicitly the **current rollback assertion**. Normal forward mutation clears it. The default retained depth remains 4 so existing baseline evidence semantics are not silently widened.

The pre-repair behavior is preserved as a dedicated synthetic transition:

`FAULT-forward-mutation-keeps-stale-rollback-receipt`

This produces a shortest five-step counterexample after a valid rollback, so the repaired semantic boundary remains falsifiable.

Two dependency-free regressions were added: the safe rollback relation must remain PASS through depth 6, and the stale-receipt fault must FAIL at depth 5 with the exact minimized trace.

## Second formal-tool comparison

INV-03 is materially different from INV-01: it includes checkpoint/known-good state, lineage observation, rollback target consistency, a current receipt lifecycle, and post-rollback forward progress.

A separately authored Z3 relation now checks three cases through depth 6 without calling the Python model's transition guards/apply functions:

- safe post-rollback forward progress: PASS;
- wrong-target rollback: shortest FAIL at depth 4;
- stale-current-receipt lifecycle: shortest FAIL at depth 5.

The dedicated formal lane remains isolated behind the already pinned `z3-solver==5.1.0.0` dependency.

## Root gate

- **Truth:** the hidden depth-5 model defect is recorded as such, repaired, and retained as a falsifier instead of being erased or misreported as a donor bug.
- **Agency / non-domination:** the model, solver, and receipts grant no execution, merge, promotion, installation, or CANON authority.
- **Continuity:** the seed remains provenance; existing default evidence depth is preserved; the old faulty lifecycle remains executable as a regression fixture.
- **Wisdom before speed:** the second formal comparison was earned by a different semantic shape and a real model-boundary finding, not by duplicating INV-01 in another file.

## Evidence ceiling

General model fidelity remains **seed rung 5 / CROSS-IMPLEMENTATION**. The solver relation is independently authored but still lives in this repository and does not prove donor-runtime fidelity, unbounded behavior, durable crash/power-loss safety, concurrent writers, or real-world rollback semantics.

The counterexample packet retains its separate rung-6 external-consumption claim.

## Next useful frontier

Do not add a third Z3 model merely to increase count. The next formal growth should require either an independently generated relation from a donor implementation, a new semantic class that exposes another concrete model defect, or a materially different verification mechanism. Otherwise HOLD formal expansion and grow a different evidence axis.
