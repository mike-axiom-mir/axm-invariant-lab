# Formal-tool comparison boundary — INV-01 / Z3 v0.1

## Status

This is a bounded **formal-tool comparison experiment**, not a repository-wide proof system and not a new authority surface.

The original seed explicitly deferred mature formal-tool comparison until the local semantics were understood. After the dependency-free explorer, independent path enumerator, counterexample packets, tractability boundary, donor refinements, and cross-repository consumers were already grounded, INV-01 is now small enough to compare honestly with a mature SMT solver without turning the lab into a solver framework.

## Compared claim

Only candidate invariant **INV-01 — no silent authority escalation** is compared here.

The primary model represents one non-baseline capability, `write`:

- a write candidate may be proposed;
- write authority may be added after an explicit grant;
- the synthetic fault transition may add write authority from a candidate without the explicit grant;
- the invariant requires effective write authority to imply an explicit write grant.

The repository's primary breadth-first explorer operates on the authored Python transition functions in `models/no_silent_authority.py`.

The formal comparison in `formal/z3_inv01.py` does **not** call those transition guards or apply functions. It independently restates the bounded model as a three-boolean symbolic transition relation and asks pinned Z3 to search exact depths from 0 through 3 for `write_authority AND NOT granted`.

## Falsifier

The comparison is useful only if it can disagree.

It fails when the primary and Z3 results differ in status, shortest witness depth, or witness action sequence for either retained case. The synthetic fault case is expected to produce the unique two-step minimal witness:

1. `propose-write-candidate`
2. `FAULT-inherit-candidate-authority`

A depth-1 Z3 search intentionally finds no violation. That is a bounded result, not evidence that the fault is globally safe.

## Dependency boundary

The core Invariant Lab remains dependency-free. Z3 is isolated as a formal comparison dependency and pinned in `requirements-formal.txt`:

`z3-solver==5.1.0.0`

Normal repository unit/refinement tests run before that dependency is installed. Hosted CI then installs the exact formal dependency, runs the dedicated formal tests, and checks the retained receipt at `evidence/z3_inv01_comparison.json`.

## What this supports

On this exact model and bound, agreement between the primary breadth-first explorer and a mature SMT solver is stronger than agreement between two local traversal algorithms that share the same authored transition functions.

It independently challenges the transition relation at the symbolic level and preserves the same shortest counterexample for the injected fault.

## Evidence ceiling

This is **not** a proof that the Python donor/model is faithful to any real AXM permission system. The Z3 encoding is independently authored inside this repository, so transcription error or shared conceptual error remains possible. It proves neither unbounded behavior nor arbitrary authority semantics, and it says nothing about donor runtimes, real users, networks, hardware, or CANON.

The seed's general exploration/model-fidelity ceiling therefore remains **rung 5 / CROSS-IMPLEMENTATION**. This run strengthens the *kind* of independent verification inside that rung; it does not silently grant rung 6 or 7.

## Root gate

- **Truth:** exact model, exact depth, exact package pin, and exact unsupported claims are explicit.
- **Agency / non-domination:** the formal result grants no execution, installation, merge, promotion, or CANON authority.
- **Continuity:** the dependency-free core remains intact; the mature solver is isolated behind a dedicated optional evidence lane.
- **Wisdom before speed:** one tiny invariant is compared first. The lab does not acquire a generic SMT abstraction layer or attempt to formalize every donor system.
