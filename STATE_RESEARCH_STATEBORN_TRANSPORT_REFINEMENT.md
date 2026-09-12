# State Research Stateborn Hostile-Transport Refinement

## Scope

This refinement promotes existing **INV-08** on one narrow, pinned Stateborn v0.7 boundary:

> Deterministic duplicate execution should agree on the declared state identity.

For this donor, the useful executable form is stricter: a packet digest may become a duplicate/replay barrier only after the state-language engine accepted the packet. A later duplicate of that accepted digest must be suppressed before a second state effect. Merely seeing a packet is not enough.

## Pinned donor evidence

Repository: `mike-axiom-mir/axm-state-research`  
Integration commit: `cf891d3614d472b1426fbdc4304e4e9fe290fb24`

Pinned Git blobs:

- `dist/state-transport.js`: `a97bde28404e9904bed2eaf76f528b0245dba29c`
- `tests/state-transport.test.mjs`: `0036fe3764207c498f9dd832591c614bdab8868c`
- `results/raw/state_transport_probe.json`: `f8ef63db0109e7c64637916f39174cbaf684719e`
- retained transport failure: `90516df35d599767d9815036a09ae4d554b5de20`
- hostile transport report: `10151fc6bbb81be91b391b2201ade2be0caac35b`

The source and raw gate agree on frozen fixture digest
`937ea582ce4576bdff15db1afebbece7c9f11e2b138860d66cfcbc381f948079`.

The prose report prints `937ea582ce4576bdff15fb1afebbece7c9f11e2b138860d66cfcbc381f948079`
instead — a one-character `d`/`f` discrepancy. This refinement preserves that discrepancy explicitly and does **not** treat the prose digest as identity authority.

## Falsifiable relation

The pinned source checks `deliveredDigests` before applying a packet. When the digest is already present, it records `DUPLICATE_SUPPRESSED` with identical engine digests before/after and returns before `applyPacket`.

Critically, the source inserts a digest into that set only when `applyPacket` returns `APPLIED`.

Three held-out relations are retained:

1. `held-duplicate`: one duplicate is suppressed, six packets are accepted, no second effect occurs, and nested engine plus transport replay pass.
2. `held-consent-refusal`: duplicate transport does not turn refusal into a commit; the donor test retains joint state `[0, 0, 0]`.
3. `held-corrupt-retry`: a corrupt packet is refused, does not install the barrier, and the clean retry succeeds.

The third case matters because the donor retained the pre-repair failure: the old transport marked a rejected digest as delivered, which poisoned deduplication and suppressed the clean retry. The fixture universe stayed frozen while the repair moved barrier insertion behind `APPLIED`.

## Truth boundary

This is deterministic simulator evidence over the exact pinned Stateborn source/test/raw receipt. It supports a narrow replay/idempotence relation; it does not establish:

- real-network exactly-once delivery;
- authenticated peer or producer identity;
- Byzantine or hostile-peer safety;
- concurrent-writer conflict correctness;
- durable crash/power-loss persistence;
- production-scale multiplayer behavior;
- merge, promotion, release, or CANON authority.

General model fidelity remains at **seed rung 5 / CROSS-IMPLEMENTATION**. Counterexample-packet consumption remains separately at rung 6.
