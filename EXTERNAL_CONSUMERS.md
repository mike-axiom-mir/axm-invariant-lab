# AXM Invariant Lab — External Consumer Boundary

## Current status

Invariant Lab now has **one real external AXM consumer** of its existing counterexample packet contract:

- consumer: `mike-axiom-mir/axm-monolith`
- consumer merge: `1c0ab8dc787086add3d8c60feeb494db7a33b935`
- consumer capability: `evidence.invariant-lab-consumer`
- source packet schema: `axm.invariant-lab.counterexample/v0.1`

This is real cross-repository use, but it does **not** yet satisfy the seed's rung 6 / CROSS-REPO requirement. The seed requires at least two real AXM systems to use the result without semantic rewriting.

## What Monolith actually consumes

Monolith's consumer accepts the exact counterexample v0.1 field set. It:

- preserves the donor-defined `FAIL` and `HOLD` statuses;
- rejects `PASS` because this packet schema does not define PASS;
- rejects unexpected fields rather than guessing future semantics;
- requires merge/CANON/execution/promotion authority fields to remain explicitly false;
- hashes the exact input bytes;
- emits a deterministic evidence-only summary;
- does not change Monolith pipeline status or grant action authority.

The consumer was merged after its exact PR candidate passed Monolith's full 56-test repository suite. An earlier CI attempt failed only because the first manifest edit accidentally removed an existing Machine Voice truth-boundary phrase; that wording was restored rather than weakening the old test.

## Producer-side continuity guard

`EXTERNAL_CONSUMERS.json` is the machine-readable registry of consumers that have pinned an Invariant Lab producer contract.

`tools/check_external_consumers.py` computes Git blob identity for the local packet and schema files and compares them with the exact blobs the registered consumer pinned.

This means a later edit to the packet or schema cannot silently pretend that the existing Monolith integration is still compatible. The check will fail until the consumer relationship is deliberately reviewed and repinned.

Run:

```bash
python tools/check_external_consumers.py --check
```

## Truth boundary

The producer-side check verifies only that the local bytes still match what a registered consumer pinned. It does not remotely execute Monolith, attest that a deployed consumer is running, prove the modeled counterexample applies to Monolith, or grant any authority.

A second materially different external AXM consumer remains the next evidence frontier before rung 6 can be promoted.
