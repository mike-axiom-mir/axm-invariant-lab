# AXM Invariant Lab

**Status:** research implementation / not CANON / no merge authority.

AXM Invariant Lab is a small dependency-free research lane for asking a different
question than ordinary example tests:

> Across the bounded state space we explicitly modeled, can any reachable legal
> transition sequence violate a declared invariant?

The repository is deliberately narrow. It does not replace unit, integration,
fuzz, replay, checkpoint, or real-environment testing. It does not prove
unmodeled code or the real world.

## v0.1 experiment

The first implementation contains:

- a dependency-free breadth-first bounded state explorer;
- tri-state invariant results: PASS / FAIL / HOLD (unknown is never treated as safe);
- four tiny AXM-shaped models;
- shortest counterexample traces for state invariants;
- a reusable counterexample packet schema;
- a bounded TruthGrid evidence refinement adapter;
- synthetic fault-injection fixtures that prove the explorer can catch transition-order failures;
- deterministic tests and evidence generation.

## Run

Python 3.10+; no third-party packages.

```bash
python -m unittest discover -s tests -v
python tools/run_evidence.py
python tools/run_evidence.py --check
```

## Important truth boundary

A PASS means only: **no counterexample was found within the exact model,
transition set, invariant predicates, and exploration bound that were run.**

A FAIL is a counterexample to the modeled claim. It is not automatically proof
of a bug in a donor repository.

A HOLD means at least one relevant state could not be decided from the modeled
or observed evidence. HOLD never silently becomes PASS.

Read `INVARIANT_CONTRACT.md`, `REFINEMENT_BOUNDARY.md`, and
`DONOR_SCAN_2026-09-12.md` before extending the lab.
