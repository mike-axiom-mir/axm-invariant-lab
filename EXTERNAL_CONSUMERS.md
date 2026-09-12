# AXM Invariant Lab — External Consumer Boundary

## Current status

Invariant Lab now has **two real, materially different external AXM consumers** of the same counterexample packet contract:

1. **AXM Monolith** — assembly/analysis consumer
   - repo: `mike-axiom-mir/axm-monolith`
   - consumer merge: `1c0ab8dc787086add3d8c60feeb494db7a33b935`
   - capability: `evidence.invariant-lab-consumer`
   - use: preserves FAIL/HOLD as evidence-only summary without mutating pipeline status.

2. **AXM Profession Mesh** — transport/admission consumer
   - repo: `mike-axiom-mir/axm-profession-mesh`
   - consumer merge: `8a9a471fd2fda1d2b548c738de96b5249ae17429`
   - capability: `mesh.invariant-evidence-admission`
   - use: preserves FAIL/HOLD verbatim, then applies a separate local receiving policy: FAIL -> `quarantine`, HOLD -> `hold`; invariant evidence can never return candidate acceptance.

Both pin the same producer packet/schema bytes:

- source schema: `axm.invariant-lab.counterexample/v0.1`
- packet Git blob: `02eeddfd12351ff6b7647bc412db3695ee45e5b3`
- schema Git blob: `cc9f1fde4855a56557ad6338c7595a99fc71cb21`

This satisfies the seed's **rung 6 / CROSS-REPO requirement for the counterexample-packet external-consumption claim**: at least two real AXM systems use the result without replacing its FAIL/HOLD meaning.

It does **not** promote the bounded exploration/model-fidelity claim beyond rung 5. Both consumers use an emitted result; neither independently proves that the authored model represents a donor runtime or reality.

## What Monolith consumes

Monolith's consumer accepts the exact counterexample v0.1 field set. It:

- preserves the donor-defined `FAIL` and `HOLD` statuses;
- rejects `PASS` because this packet schema does not define PASS;
- rejects unexpected fields rather than guessing future semantics;
- requires merge/CANON/execution/promotion authority fields to remain explicitly false;
- hashes the exact input bytes;
- emits a deterministic evidence-only summary;
- does not change Monolith pipeline status or grant action authority.

The consumer was merged after its exact PR candidate passed Monolith's full 56-test repository suite. An earlier CI attempt failed only because the first manifest edit accidentally removed an existing Machine Voice truth-boundary phrase; that wording was restored rather than weakening the old test.

## What Profession Mesh consumes

Profession Mesh is a materially different consumer because its job is transport/discovery/admission rather than stack assembly/analysis. Its consumer:

- requires the exact content SHA-256 advertised in its consumer manifest before parsing;
- preserves the producer `FAIL` / `HOLD` status verbatim;
- rejects `PASS`, unknown top-level fields, authority escalation, and content-digest mismatch;
- maps FAIL to local `quarantine` and HOLD to local `hold` as an additional receiving policy;
- sets `mayAcceptCandidate: false` for invariant evidence;
- explicitly keeps transport authority separate from profession authority.

Profession Mesh PR #3 exact source head `293272e08cf6af0a18f4b011447e10a36957faf9` passed workflow run `34692275335` on Node 22. The hosted `npm test` ran both the existing foundation authority-boundary test and the new invariant evidence consumer test successfully before the PR was squash-merged as `8a9a471fd2fda1d2b548c738de96b5249ae17429`.

## Producer-side continuity guard

`EXTERNAL_CONSUMERS.json` is the machine-readable registry of consumers that have pinned an Invariant Lab producer contract.

`tools/check_external_consumers.py` computes Git blob identity for the local packet and schema files and compares them with the exact blobs every registered consumer pinned. The registry now also rejects duplicate consumer repository entries so one system cannot be counted twice by accident.

This means a later edit to the packet or schema cannot silently pretend that either integration is still compatible. The check fails until the affected consumer relationship is deliberately reviewed and repinned.

Run:

```bash
python tools/check_external_consumers.py --check
```

## Truth boundary

The producer-side check verifies only that local bytes still match what registered consumers pinned. It does not remotely execute either consumer, attest deployed runtime behavior, prove the modeled counterexample applies to those systems, or grant any authority.

Seed rung 6 is promoted only for **external use of the counterexample packet/result contract**. Bounded exploration semantics remain rung 5 / CROSS-IMPLEMENTATION; real-environment validation remains unearned.
