# AXM Invariant Lab

**Status:** working experimental capability / adversarial-fixture evidence / not CANON / no merge or execution authority.

The original `RESEARCH_SEED_v0.1.md` is preserved as provenance. It was the kickstart document, not a permanent requirement that this repository remain research-only. Fresh evidence decides the repo's current status.

AXM Invariant Lab is a small dependency-free capability for asking a different question than ordinary example tests:

> Across the bounded state space we explicitly modeled, can any reachable legal transition sequence violate a declared invariant?

The repository is deliberately narrow. It does not replace unit, integration, fuzz, replay, checkpoint, or real-environment testing. It does not prove unmodeled code or the real world.

## v0.1 capability

The first grounded implementation contains:

- a dependency-free breadth-first bounded state explorer;
- tri-state invariant results: PASS / FAIL / HOLD (unknown is never treated as safe);
- four tiny AXM-shaped models;
- shortest counterexample traces for state invariants;
- a reusable counterexample packet schema;
- a bounded TruthGrid evidence refinement adapter;
- synthetic fault-injection fixtures that demonstrate transition-order failure detection;
- deterministic tests and evidence generation.

The callable Python surface is `src.bounded_explorer.explore(...)` with `Transition` and `Invariant` contracts. Machine discovery is declared in `AXM_MODULE.json`. Counterexample interchange is bounded by `COUNTEREXAMPLE_PACKET.schema.json`.

## Evidence level

v0.1 has reached the seed's **rung 4 / ADVERSARIAL** boundary:

- 11/11 repository tests pass on the retained v0.1 evidence set;
- all four safe authored models PASS;
- all four fault-injected variants FAIL;
- unknown/missing required donor evidence HOLDs rather than silently PASSing;
- the TruthGrid refinement fixture detects an adversarial `rollbackRef` mutation;
- GitHub Actions passed on the exact proposed v0.1 head on Python 3.11 and 3.13.

This is enough to treat the bounded explorer and packet contract as a **working experimental capability**. It is not enough to claim cross-implementation, cross-repo adoption, real-environment validation, or formal proof of AXM as a whole.

## Run

Python 3.10+; no third-party packages.

```bash
python -m unittest discover -s tests -v
python tools/run_evidence.py
python tools/run_evidence.py --check
```

## Important truth boundary

A PASS means only: **no counterexample was found within the exact model, transition set, invariant predicates, and exploration bound that were run.**

A FAIL is a counterexample to the modeled claim. It is not automatically proof of a bug in a donor repository.

A HOLD means at least one relevant state could not be decided from the modeled or observed evidence. HOLD never silently becomes PASS.

Synthetic fault traces validate the explorer against authored faults; they do not assert those faults exist in donor systems.

## Authority boundary

This repository may describe, explore, falsify, and emit evidence. It does not grant execution, device, network, merge, promotion, or CANON authority. The four AXM roots — Truth, Agency/non-domination, Continuity, and Wisdom before speed — remain the merge gate.

Read `INVARIANT_CONTRACT.md`, `REFINEMENT_BOUNDARY.md`, `DONOR_SCAN_2026-09-12.md`, and `ACTION_REPORT_v0.1.md` before extending the lab.
