# AXM Invariant Lab — Action Report v1.2

## Decision

**GROW / PROMOTE EXISTING INV-09 NARROWLY.**

The previous v1.1 frontier asked for a materially different continuity/provenance axis rather than more opaque-version samples. AXM State Research now contains a grounded Stateborn fresh-process checkpoint verifier with a resealed-inner-tamper control and exact hosted evidence. This is non-duplicative with INV-17: it tests whether serialized checkpoint-owned evidence reconstructs identically without access to the live engine object, and whether replay identity still rejects changed inner history after the outer seal is recomputed.

## Source truth

Pinned State Research integration commit: `cf891d3614d472b1426fbdc4304e4e9fe290fb24`.

Pinned donor verifier head: `0cef53c3900c48a4d7cece62bcbfd6fa34f40fab`.

Pinned donor Git blobs:

- fresh-process regression: `7383822c140522cc71684371bdade3d187271d67`
- detached checkpoint verifier: `79ebc5422ea80ca122677f0e2df69eca8a3908d2`
- bounded process adapter: `c30f6a46abcd21478642e023c37fff187a634352`
- lane/evidence receipt: `9bc0feaa335b9822662252349b55b81a859a31ce`

Independently queried hosted donor run `34586268082` is `success` on exact head `0cef53c...`; Node 20 and Node 22 jobs both passed their focused fresh-process checkpoint regression step and complete Stateborn suite.

## Useful delta

- Promotes existing **INV-09** from `ADAPTER LATER` to `FRESH-PROCESS CHECKPOINT ADAPTER NOW` on a precise donor boundary.
- Adds a read-only Stateborn checkpoint continuity adapter and pinned projection.
- Retains the positive detached-reconstruction relation: fresh receipt equals local receipt and checkpoint/state/receipt identities agree.
- Retains the falsifier: change an inner receipt, recompute only the outer checkpoint digest, and verification still fails closed as `HOLD / CHECKPOINT_REPLAY`.
- Preserves explicit no-authority fields for resume, transport mutation, canonical-state mutation, merge, and CANON.
- Adds eight focused adversarial tests and a deterministic evidence-drift gate.

## Local focused evidence before publish

The new focused suite ran **8/8 PASS** locally. The generated retained evidence rechecked deterministically as PASS before publication.

## Evidence ceiling

The donor fresh-process regression proves detached verification of checkpoint-owned state-language evidence on tested Node paths. It does not prove full transport-session restart/resume, durable persistence, filesystem crash atomicity, authenticated producer identity, concurrent writers, hostile-peer security, real networking, or external truth. SHA-256/replay establish content/reconstruction relationships, not authorship.

General model fidelity therefore remains at **seed rung 5 / CROSS-IMPLEMENTATION**. Counterexample-packet consumption remains separately at rung 6. No constitutional or CANON authority is created.

## Next bounded frontier

Do not add more checkpoint fixtures merely to increase sample count. A meaningful next step requires a different grounded axis: authenticated/signed runtime provenance, durable crash/power-loss checkpoint behavior, multiple-writer conflict evidence, or the previously identified budgeted opaque-version swarm. If none exists in real donor evidence, HOLD is preferable to framework growth.
