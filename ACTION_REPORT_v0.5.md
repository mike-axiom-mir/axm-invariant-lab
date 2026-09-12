# AXM Invariant Lab — Action Report v0.5

## Question tested

Can one real external AXM repository consume Invariant Lab's existing counterexample packet without semantic rewriting or authority escalation, and can Invariant Lab detect later producer-byte drift that would invalidate that consumer pin?

## Pre-run scan

- `main` started at `f3aab96f448c67fa79c1277b00f374707c4577f7`.
- No open Invariant Lab PRs were present.
- Remaining non-main Invariant Lab branches were historical merged v0.1-v0.4 lanes.
- The exact v0.4 PR head had a successful `invariant-lab-tests` workflow.
- `RESEARCH_SEED_v0.1.md` remains unchanged provenance.
- Monolith had no open PR and no existing invariant/counterexample consumer lane before this work.

## External consumer delta

A bounded consumer was added to `mike-axiom-mir/axm-monolith`:

- strict `axm.invariant-lab.counterexample/v0.1` import;
- exact pinned packet/schema provenance;
- FAIL/HOLD preserved;
- PASS and unknown future fields rejected rather than reinterpreted;
- explicit no-authority fields required;
- deterministic source-byte hashing;
- no Monolith pipeline status mutation.

Monolith PR #4 exact final head `d35e075cdf754e3a6d180e6651f13d018ea63a20` passed its full **56-test** repository suite in workflow run `34689515032` and was squash-merged as `1c0ab8dc787086add3d8c60feeb494db7a33b935`.

An earlier hosted run failed one pre-existing Machine Voice boundary test because the first manifest edit had dropped the exact phrase `not cross-repository runtime verification`. The old boundary was restored unchanged; the test was not weakened.

## Invariant Lab delta

Added:

- `EXTERNAL_CONSUMERS.json` — machine-readable registered consumer pins;
- `tools/check_external_consumers.py` — Git-blob compatibility check for producer packet/schema bytes;
- `evidence/external-consumers-latest.json` — deterministic local compatibility receipt;
- `tests/test_external_consumers.py` — intact/drift/unknown-status regressions;
- `EXTERNAL_CONSUMERS.md` — evidence and truth boundary.

## Falsifier

This result would fail if:

- Monolith rewrote FAIL/HOLD into stronger pipeline truth;
- the consumer granted authority from the packet;
- Monolith's full suite failed on the final candidate;
- Invariant Lab could change packet/schema bytes without the producer-side compatibility check noticing;
- the work claimed seed rung 6 from only one external consumer.

## Evidence result

- standalone Monolith consumer tests: **6/6 PASS** before publication;
- Monolith hosted full repository suite on the final exact PR candidate: **56/56 PASS**;
- Invariant Lab external-consumer focused tests: **3/3 PASS** before publication;
- retained producer compatibility receipt: packet blob and schema blob both exactly match the Monolith pins.

## Evidence ceiling

This is the **first real external consumer**, not seed rung 6.

The bounded exploration engine remains at seed rung 5 / CROSS-IMPLEMENTATION. The counterexample packet now has one demonstrated cross-repo consumer, but the seed requires at least two real AXM systems to use the result without semantic rewriting before CROSS-REPO can be promoted.

## Root check

**Truth:** consumer semantics stay exact; failed first CI is retained as evidence; producer drift is detectable; no rung-6 overclaim.

**Agency / non-domination:** packet import is evidence-only and grants no execution, merge, CANON, promotion, installation, device, or network authority.

**Continuity:** source packet/schema identity is pinned and Invariant Lab now fails closed if those producer bytes drift relative to a registered consumer.

**Wisdom before speed:** one small real consumer was built before attempting automatic pipeline integration or a broad consumer framework.

## Next meaningful frontier

A second materially different external AXM consumer of the same result/packet contract. Until then, more internal consumer fixtures would mostly duplicate evidence rather than advance the seed ladder.
