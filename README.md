# AXM Invariant Lab

**Status:** working experimental capability / cross-implementation evidence / two donor refinement fixtures / measured tractability boundary / first real external consumer / not CANON / no merge or execution authority.

The original `RESEARCH_SEED_v0.1.md` is preserved as provenance. It was the kickstart document, not a permanent requirement that this repository remain research-only. Fresh evidence decides the repo's current status.

AXM Invariant Lab is a small dependency-free capability for asking a different question than ordinary example tests:

> Across the bounded state space we explicitly modeled, can any reachable legal transition sequence violate a declared invariant?

The repository is deliberately narrow. It does not replace unit, integration, fuzz, replay, checkpoint, or real-environment testing. It does not prove unmodeled code or the real world.

## Grounded capability

The current implementation contains:

- a dependency-free breadth-first bounded state explorer;
- tri-state invariant results: PASS / FAIL / HOLD (unknown is never treated as safe);
- four tiny AXM-shaped models;
- shortest counterexample traces for state invariants;
- a reusable counterexample packet schema;
- a bounded TruthGrid evidence refinement adapter;
- synthetic fault-injection fixtures that demonstrate transition-order failure detection;
- a second dependency-free path-enumeration verifier that does not call the primary explorer or prune revisited states;
- cross-implementation agreement receipts with an explicit path-node tractability budget;
- a deterministic tractability probe showing where all-path enumeration reaches that budget while visited-state exploration remains small;
- a read-only AXM Monolith Pipeline Fabric v0.1 refinement adapter pinned to an exact donor contract, preserving candidate-only status and explicit no-automatic-authority fields;
- a first real external consumer: AXM Monolith imports the exact counterexample v0.1 packet as evidence-only without changing pipeline status;
- an external-consumer registry and producer-side blob-identity guard so later packet/schema drift cannot silently claim compatibility with a pinned consumer;
- deterministic tests and evidence generation.

The primary callable surface is `src.bounded_explorer.explore(...)`. The independent bounded cross-check is `src.reference_verifier.verify_paths(...)`, composed through `src.cross_verifier.cross_verify(...)`. The tractability probe is `src.tractability_probe.run_probe(...)`. Donor refinement surfaces live under `adapters/`. Consumer continuity is checked by `tools/check_external_consumers.py`. Machine discovery is declared in `AXM_MODULE.json`.

## Evidence level

The bounded **exploration semantics** remain at the seed's **rung 5 / CROSS-IMPLEMENTATION** boundary:

- the retained four safe models and four fault-injected variants produce **8/8 cross-implementation agreements**;
- both implementations agree on PASS/FAIL status, reachable unique-state count, failing invariant names, and unknown invariant names for those retained cases;
- the reference verifier fully enumerates those cases inside its explicit path-node budget;
- budget exhaustion forbids an unearned PASS and produces HOLD unless a concrete modeled failure has already been observed;
- the earlier adversarial evidence remains: safe models PASS, injected faults FAIL, missing donor evidence HOLDs, and the TruthGrid refinement fixture detects an adversarial `rollbackRef` mutation.

A second real donor boundary is mapped through the Monolith Pipeline Fabric v0.1 refinement fixture. The adapter checks explicit `automatic_execution/install/merge/canon = false` fields and candidate-only pipeline statuses; contradictory values FAIL and missing evidence HOLDs.

The retained tractability probe adds a separate operational boundary without promoting the evidence rung. On an authored reconverging two-branch model with a 100,000 path-node budget, the reference verifier completes depth 15 at **65,535 path nodes**, then reaches the budget and returns **HOLD at depth 16**, while the visited-state explorer still completes with only **17 unique states**. These are deterministic work counts, not wall-clock performance claims. See `TRACTABILITY_BOUNDARY.md`.

### First external consumer

AXM Monolith is now a real consumer of `axm.invariant-lab.counterexample/v0.1`.

Its merged consumer preserves FAIL/HOLD, rejects unsupported PASS/future fields, requires all authority fields to remain false, hashes the exact packet bytes, and emits an evidence-only summary. It does not mutate Monolith pipeline status. The exact final Monolith PR candidate passed the full **56-test** suite before merge.

Invariant Lab now keeps `EXTERNAL_CONSUMERS.json` and checks that the local packet/schema Git blob identities still match the consumer's exact pins. Producer-byte drift fails closed until compatibility is deliberately reviewed.

This is meaningful cross-repository use, but it is **not seed rung 6 yet**. The seed requires at least **two materially different real AXM systems** to use the result without semantic rewriting. One consumer does not silently grant the next rung.

The rung-5 exploration claim also remains intentionally narrow. Both exploration verifiers consume the **same authored transition and invariant functions**. Agreement cross-checks the search/exploration implementation; it does not independently prove that the model faithfully represents donor code.

There is still no second external consumer, solver-backed proof, or real-environment validation.

## Run

Python 3.10+; no third-party packages.

```bash
python -m unittest discover -s tests -v
python tools/run_evidence.py --check
python tools/run_cross_verification.py --check
python tools/run_monolith_refinement.py --check
python tools/run_tractability.py --check
python tools/check_external_consumers.py --check
```

Regenerate retained receipts only when deliberately reviewing a semantic change:

```bash
python tools/run_cross_verification.py
python tools/run_monolith_refinement.py
python tools/run_tractability.py
python tools/check_external_consumers.py
```

## Important truth boundary

A primary PASS means only: **no counterexample was found within the exact model, transition set, invariant predicates, and exploration bound that were run.**

A cross-verification `AGREE` means the independent path enumerator matched the primary bounded result on the compared observables. It does not mean the model itself is correct.

A donor-refinement PASS means only that the exact explicit donor fields represented by the pinned fixture satisfy the adapter contract. It does not prove a full donor runtime or an unobserved field.

A tractability HOLD means the declared comparison budget was exhausted. It is evidence that the independent comparison is incomplete, not evidence against the primary result and not a reason to force a larger budget.

An external-consumer compatibility PASS means only that local producer packet/schema bytes still equal the blobs the registered consumer pinned. It does not remotely execute or attest that consumer.

A FAIL is a counterexample to the modeled/declared claim. It is not automatically proof of a bug in a donor repository.

A HOLD means required evidence or bounded enumeration is incomplete. HOLD never silently becomes PASS.

Synthetic fault traces and tractability fixtures validate the explorers against authored conditions; they do not assert those conditions exist in donor systems.

## Authority boundary

This repository may describe, explore, falsify, cross-check, measure bounded tractability, emit evidence, and track consumer compatibility. It does not grant execution, device, network, merge, promotion, installation, or CANON authority. The four AXM roots — Truth, Agency/non-domination, Continuity, and Wisdom before speed — remain the merge gate.

Read `INVARIANT_CONTRACT.md`, `REFINEMENT_BOUNDARY.md`, `MONOLITH_PIPELINE_REFINEMENT.md`, `TRACTABILITY_BOUNDARY.md`, `EXTERNAL_CONSUMERS.md`, `DONOR_SCAN_2026-09-12.md`, and the latest `ACTION_REPORT_v0.*.md` before extending the lab.
