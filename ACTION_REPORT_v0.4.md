# AXM Invariant Lab — Action Report v0.4

## Question tested

Can the lab establish a deterministic stop/hold boundary for its independent path verifier instead of assuming that a second exhaustive implementation remains tractable as model depth grows?

## Pre-run overlap scan

- `main` started at `993473ce5a6033b3ff1716d94c8f35439b2a7029`.
- No open pull requests were present.
- Remaining non-main branches were historical merged lanes for v0.1, v0.2, and v0.3.
- The latest exact v0.3 PR head had a successful `invariant-lab-tests` workflow.
- `RESEARCH_SEED_v0.1.md` remains preserved unchanged as kickstart/provenance.

## Exact delta

Added a narrow deterministic tractability probe for the two existing exploration strategies. The synthetic fixture has two legal transition names that reconverge onto one next state, separating unique-state growth from path-count growth.

Added:

- `src/tractability_probe.py`
- `tools/run_tractability.py`
- `tests/test_tractability_probe.py`
- `evidence/tractability-latest.json`
- `TRACTABILITY_BOUNDARY.md`

The repository CI now checks retained tractability evidence for drift.

## Falsifier

With a 100,000 path-node budget:

- if the reference verifier remained complete at depth 16, the expected boundary was falsified;
- if budget exhaustion became PASS, the verifier's truth boundary was broken;
- if the primary visited-state explorer also became incomplete/failing on this tiny reconverging model, the probe would not isolate path multiplicity as intended.

## Result

Deterministic retained work counts:

- depth 12: primary 13 unique states / PASS; reference 8,191 path nodes / complete / PASS;
- depth 15: primary 16 unique states / PASS; reference 65,535 path nodes / complete / PASS;
- depth 16: primary 17 unique states / PASS; reference 100,000 path nodes / incomplete / HOLD.

This demonstrates a real tractability boundary in the current independent verifier and validates that its budget-exhaustion HOLD is necessary.

## What this does not prove

- depth 16 is not a general AXM limit;
- the primary explorer is not proven tractable on arbitrary unique-state spaces;
- no wall-clock performance claim is made;
- no solver/model-checker comparison was performed;
- no donor runtime or real-world system was measured;
- seed rung 6 / CROSS-REPO remains unearned.

## Root check

**Truth:** uses deterministic work counts and preserves incomplete reference enumeration as HOLD.

**Agency / non-domination:** measurement grants no execution or adoption authority and does not force a verification method on donor repos.

**Continuity:** no donor semantics were changed; the seed and existing explorer/verifier interfaces remain intact.

**Wisdom before speed:** establishes an evidence-backed point to stop exhaustive path checking rather than raising budgets or adding complexity by instinct.

## Status

This is a bounded capability-strengthening result, not a new evidence-rung promotion. The useful next method change should occur only when a grounded model is actually blocked by this boundary; otherwise more tractability machinery would be churn.
