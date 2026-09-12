# Formal-tool comparison boundary — INV-03 / Z3 v0.2

## Status

This is a bounded formal comparison and a repair of one model-boundary defect. It is not a generic solver layer, not a durable-storage proof, and not an authority surface.

## Defect found before expansion

The original rollback model stored a successful rollback receipt in the current state and never cleared that receipt on later normal forward mutation. At the repository's retained depth 4, the model stopped immediately after rollback and therefore passed. At depth 5, one more legal `mutate-S1-to-S2` step made the old receipt compare against the new current state and produced a false failure in the nominally safe relation.

That is a model-lifecycle defect, not evidence of a donor-repository rollback bug.

The repair gives the field a precise bounded meaning: `rollback` is the **current rollback assertion**. A later normal forward mutation clears that current assertion. Durable historical receipts are outside this tiny model.

The pre-repair behavior remains executable as `FAULT-forward-mutation-keeps-stale-rollback-receipt`, so the defect is retained as a falsifier rather than erased from history.

## Compared claim

Candidate invariant **INV-03 — rollback known-good lineage** is compared through depth 6.

The primary Python relation models:

- mutation from S0 to S1;
- marking S1 known-good;
- forward mutation from S1 to S2;
- rollback from S2 to known-good S1;
- a wrong-target fault that reports S1 while restoring S9; and
- a stale-current-receipt fault that moves forward after rollback without clearing the current rollback assertion.

The independent Z3 relation in `formal/z3_inv03.py` does not call those Python transition guards or apply functions. It separately encodes current state, S1 known-good membership, S1 lineage observation, current receipt activity, and receipt target identity.

## Retained falsifiers

Three cases are retained:

1. **safe post-rollback forward progress** — PASS through depth 6;
2. **wrong-target rollback** — shortest FAIL at depth 4:
   `mutate-S0-to-S1 -> checkpoint-S1 -> mutate-S1-to-S2 -> FAULT-rollback-reports-S1-but-restores-S9`;
3. **stale receipt lifecycle** — shortest FAIL at depth 5:
   `mutate-S0-to-S1 -> checkpoint-S1 -> mutate-S1-to-S2 -> rollback-to-S1 -> FAULT-forward-mutation-keeps-stale-rollback-receipt`.

The depth-4 stale-receipt solver check remains PASS because the violating fifth transition has not occurred yet. That boundary is retained so a too-small bound cannot be described as global safety.

## Evidence ceiling

This is the second materially different invariant semantics checked with pinned Z3 after INV-01. It demonstrates that the comparison method can handle a temporal rollback/receipt lifecycle shape rather than only a three-boolean authority relation.

It still does **not** establish unbounded proof, durable disk safety, crash or power-loss recovery, concurrent-writer correctness, cryptographic snapshot identity, donor-runtime fidelity, or real-world rollback behavior. The symbolic model is authored inside this repository, so shared conceptual mistakes remain possible.

General model fidelity therefore stays at seed rung 5 / CROSS-IMPLEMENTATION. The separately earned counterexample-packet rung-6 claim is unchanged.

## Root gate

- **Truth:** the depth-5 defect is named as a model defect and preserved as a regression/falsifier; it is not rewritten into a donor claim.
- **Agency / non-domination:** solver receipts grant no execution, merge, promotion, installation, or CANON authority.
- **Continuity:** the original seed remains provenance, the existing default depth-4 evidence contract is preserved, and the pre-repair lifecycle behavior remains testable.
- **Wisdom before speed:** one existing rollback model is repaired and independently challenged rather than creating a generic formal DSL or expanding to the whole AXM stack.
