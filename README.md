# AXM Invariant Lab

**Status:** working experimental capability / cross-implementation evidence / second-donor refinement fixture / not CANON / no merge or execution authority.

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
- a read-only AXM Monolith Pipeline Fabric v0.1 refinement adapter pinned to an exact donor contract, preserving candidate-only status and explicit no-automatic-authority fields;
- deterministic tests and evidence generation.

The primary callable surface is `src.bounded_explorer.explore(...)`. The independent bounded cross-check is `src.reference_verifier.verify_paths(...)`, composed through `src.cross_verifier.cross_verify(...)`. Donor refinement surfaces live under `adapters/`. Machine discovery is declared in `AXM_MODULE.json`.

## Evidence level

The bounded **exploration semantics** have reached the seed's **rung 5 / CROSS-IMPLEMENTATION** boundary:

- the retained four safe models and four fault-injected variants produce **8/8 cross-implementation agreements**;
- both implementations agree on PASS/FAIL status, reachable unique-state count, failing invariant names, and unknown invariant names for those retained cases;
- the reference verifier fully enumerates those cases inside its explicit path-node budget;
- budget exhaustion forbids an unearned PASS and produces HOLD unless a concrete modeled failure has already been observed;
- the earlier adversarial evidence remains: safe models PASS, injected faults FAIL, missing donor evidence HOLDs, and the TruthGrid refinement fixture detects an adversarial `rollbackRef` mutation.

A second real donor boundary is now mapped through the Monolith Pipeline Fabric v0.1 refinement fixture. The adapter checks explicit `automatic_execution/install/merge/canon = false` fields and candidate-only pipeline statuses; contradictory values FAIL and missing evidence HOLDs. This reduces the shared-model risk identified in v0.2, but it **does not earn seed rung 6** because two external AXM systems are not yet consuming Invariant Lab output.

The rung-5 claim remains intentionally narrow. Both exploration verifiers consume the **same authored transition and invariant functions**. Agreement cross-checks the search/exploration implementation; it does not independently prove that the model faithfully represents donor code.

The counterexample packet and cross-repo adoption claims have **not** silently inherited rung 5/6. There is still no two-repo consumer evidence, solver-backed proof, or real-environment validation.

## Run

Python 3.10+; no third-party packages.

```bash
python -m unittest discover -s tests -v
python tools/run_evidence.py --check
python tools/run_cross_verification.py --check
python tools/run_monolith_refinement.py --check
```

Regenerate retained receipts only when deliberately reviewing a semantic change:

```bash
python tools/run_cross_verification.py
python tools/run_monolith_refinement.py
```

## Important truth boundary

A primary PASS means only: **no counterexample was found within the exact model, transition set, invariant predicates, and exploration bound that were run.**

A cross-verification `AGREE` means the independent path enumerator matched the primary bounded result on the compared observables. It does not mean the model itself is correct.

A donor-refinement PASS means only that the exact explicit donor fields represented by the pinned fixture satisfy the adapter contract. It does not prove a full donor runtime, an unobserved field, or cross-repo adoption.

A FAIL is a counterexample to the modeled/declared claim. It is not automatically proof of a bug in a donor repository.

A HOLD means required evidence or bounded enumeration is incomplete. HOLD never silently becomes PASS.

Synthetic fault traces validate the explorers against authored faults; they do not assert those faults exist in donor systems.

## Authority boundary

This repository may describe, explore, falsify, cross-check, and emit evidence. It does not grant execution, device, network, merge, promotion, installation, or CANON authority. The four AXM roots — Truth, Agency/non-domination, Continuity, and Wisdom before speed — remain the merge gate.

Read `INVARIANT_CONTRACT.md`, `REFINEMENT_BOUNDARY.md`, `MONOLITH_PIPELINE_REFINEMENT.md`, `DONOR_SCAN_2026-09-12.md`, `ACTION_REPORT_v0.1.md`, `ACTION_REPORT_v0.2.md`, and `ACTION_REPORT_v0.3.md` before extending the lab.
