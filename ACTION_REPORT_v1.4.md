# AXM Invariant Lab — Action Report v1.4

Date: 2026-09-12

## Question tested

Can a sparse execution legitimately match a dense oracle when a sleeping component still contributes to shared reference/normalization state, without incorrectly requiring every such contribution change to wake the component body?

## Pre-work overlap scan

- `main` base: `64c9c62185f4313759f83b749c246441bd3dbb9b`.
- No open pull requests existed at claim time.
- Existing target refinements covered dependency wake completeness, runtime observation, held-out closure, cross-version opaque recovery, Stateborn checkpoint continuity, and hostile transport idempotence.
- No target code or capability named/reference-mapped `reference-state-closure` existed.
- The donor capability is `mike-axiom-mir/axm-state-research/experiments/reference-state-closure-v1` at pinned commit `cf891d3614d472b1426fbdc4304e4e9fe290fb24`.

## Exact delta

Added a read-only INV-18 refinement with:

- exact donor source/fixture/test/README/portable blob pins;
- deterministic baseline projection;
- the same-wake-set negative control;
- a dropped-reference-summary fault boundary;
- PASS / FAIL / HOLD adapter semantics;
- adversarial tests;
- retained evidence and CI drift checking;
- explicit documentation and invariant-map promotion.

## Result retained

On the pinned 8-node, 12-transition donor workload:

- dense A and sparse-closure B replay digests agree;
- A executes 104 bodies and B executes 18, avoiding 86 executions;
- a reference-only change wakes zero bodies yet B remains equivalent because the derived reference total is updated;
- control C uses B's wake set but drops a sleeping reference contribution and diverges on 11 transitions;
- deliberately dropping reference-summary updates makes A/B equivalence false and donor status HOLD;
- maximum reference encoding on the retained fixture is 119 bytes dense vs 23 bytes derived.

## Root gate

**Truth:** the capability pins exact donor bytes, retains the negative control and HOLD fault, and limits its claim to the modeled workload.

**Agency / non-domination:** no evidence packet, packaging step, test, or adapter result grants execution, installation, merge, selection, or CANON authority.

**Continuity:** donor semantics are not rewritten; the source repo/commit/blob identities are explicit, and INV-18 is additive rather than replacing existing wake-completeness refinements.

**Wisdom before speed:** the run chose a small existing executable donor experiment rather than creating a new universal model or solver layer.

## Evidence ceiling

General model fidelity remains seed rung 5 / CROSS-IMPLEMENTATION. This run does not establish arbitrary sparse scheduler correctness, neural/hardware behavior, producer authentication, real-environment behavior, or rung-6 cross-repo use for INV-18.

## Next frontier

If this boundary remains useful, the next stronger evidence would be a materially different real AXM implementation where sleeping components contribute to a shared derived/reference state and an independent refinement can compare sparse output to a dense/reference oracle. More synthetic variants of the same fixture should not be counted as an evidence-class advance.
