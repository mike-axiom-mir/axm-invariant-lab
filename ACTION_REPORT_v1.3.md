# AXM Invariant Lab — Action Report v1.3

## Decision

**GROW / PROMOTE EXISTING INV-08 NARROWLY + REPAIR MACHINE DISCOVERY DRIFT.**

The v1.2 frontier asked for a materially different grounded axis. State Research already contains one: the frozen Stateborn v0.7 hostile-transport trial, including duplicate suppression, consent refusal under duplication, corrupt-retry recovery, and a retained pre-repair deduplication failure.

This run does not add another synthetic invariant. It promotes existing **INV-08** on that exact donor boundary.

During pre-work inspection, a continuity discrepancy was also found in Invariant Lab itself: v1.2 added the Stateborn checkpoint adapter, CI gate, fixture, tests, and docs, but `AXM_MODULE.json` did not expose that new capability/entrypoint even though the prior run described machine discovery as present. v1.3 repairs that machine-readable omission while adding the transport capability.

## Source truth

Pinned State Research integration commit: `cf891d3614d472b1426fbdc4304e4e9fe290fb24`.

Pinned donor blobs:

- hostile transport implementation: `a97bde28404e9904bed2eaf76f528b0245dba29c`
- transport regression suite: `0036fe3764207c498f9dd832591c614bdab8868c`
- raw hostile-transport gate: `f8ef63db0109e7c64637916f39174cbaf684719e`
- retained pre-repair failure: `90516df35d599767d9815036a09ae4d554b5de20`
- evidence report: `10151fc6bbb81be91b391b2201ade2be0caac35b`

The executable source and raw gate agree on frozen fixture digest
`937ea582ce4576bdff15db1afebbece7c9f11e2b138860d66cfcbc381f948079`.
The prose report prints `...ff15fb1a...` instead of `...ff15db1a...`. That one-character discrepancy is retained explicitly; it is not silently normalized.

## Useful delta

- Promotes existing **INV-08** from generic `ADAPTER NOW` to a pinned Stateborn hostile-transport idempotence adapter.
- Makes the accepted-only replay barrier explicit: a packet digest enters duplicate tracking only after `APPLIED`.
- Retains a positive duplicate test, a refusal-under-duplicate test, and a corruption/retry falsifier with the donor's pre-repair failure history.
- Adds exact source/test/raw/report/failure blob provenance.
- Adds nine focused adversarial tests and a deterministic evidence-drift gate.
- Repairs `AXM_MODULE.json` discovery for both the already-merged v1.2 Stateborn checkpoint capability and the new v1.3 transport capability.

## Local focused evidence before publish

The new focused suite ran **9/9 PASS** locally, and its generated evidence reproduced deterministically with `--check`.

## Evidence ceiling

The donor simulator establishes explicit behavior for its authored deterministic transport faults. It does **not** prove real-network exactly-once semantics, peer authentication, concurrent writers, durable crash/power-loss safety, arbitrary adversaries, or deployment behavior.

The report-digest typo is itself a source-integrity lesson: prose is useful evidence context but cannot override the pinned executable/raw identity.

General model fidelity remains at **seed rung 5 / CROSS-IMPLEMENTATION**. Counterexample-packet consumption remains separately at rung 6. No execution, merge, or CANON authority is created by the adapter.

## Next bounded frontier

Do not add more duplicate routes merely to increase sample count. A stronger next step needs new evidence class: authenticated runtime provenance, actual concurrent-writer conflict evidence, durable crash/power-loss persistence, or a grounded budgeted opaque-version swarm. If none exists, HOLD is preferable to framework growth.
