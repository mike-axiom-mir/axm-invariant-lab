# Monolith native-route evolution refinement — INV-20 v2.5

## Question

Does INV-20 survive the Monolith's later evolution from one explicitly named callable workflow into a broader native-command routing layer without allowing declaration, addressability, or old execution evidence to become current execution automatically?

## Pinned donor

- repository: `mike-axiom-mir/axm-monolith`
- commit: `8ce73a54d488805b126fe7fa64eac1ec2b28e900`
- `tools/totality_native_smokes.py` blob: `4286dbd2ef550841889644c56b620abda5cdf504`
- `tests/test_totality_native_smokes.py` blob: `d41f5e0aa727f0718df2e4f783431de98f185b96`

The donor exposes 15 retained native-smoke recipes across multiple AXM repositories. Each recipe carries an exact endpoint address, exact producer repository commit, and fixed arguments.

## Bounded invariant projection

INV-20 is extended with one narrow evolution rule:

> A retained native route may become `READY` for a separate explicit execution attempt only when the endpoint exists at the exact pinned producer ref and retains verified native-command execution evidence. `READY` in plan mode is not execution. A changed ref, missing endpoint, or loss of verified native-command evidence must return HOLD rather than inherit callability from the wider Monolith.

The refinement executes the donor's own planning gate over a synthetic `EXECUTION_FABRIC.json` containing exactly the 15 pinned routes. It does not execute the capabilities themselves.

### Positive observation

All 15 exact recipes produce:

- donor plan status: `PASS`
- per-route status: `READY`
- per-route `executed: false`

### Falsifiers

For the first retained recipe, Invariant Lab independently changes one condition at a time and requires the donor gate to fail closed:

- changed producer commit -> `HOLD_RECIPE_REF_MISMATCH`
- retained endpoint without verified native-command evidence -> `HOLD_NO_VERIFIED_NATIVE_EVIDENCE`
- missing endpoint -> `HOLD_ENDPOINT_MISSING`

Every falsifier must remain `executed: false`.

## Why this is distinct from v2.4

v2.4 tested declaration -> explicit execution -> connected package evidence in the Monolith finalizer with a two-callable probe.

v2.5 tests survival of the same non-promotion principle after the donor expanded into a multi-repository learned native-route layer. It is therefore implementation-evolution evidence, not another frozen-package projection and not another hand-authored endpoint count.

## Four-root boundary

**Truth** — exact repository commits and donor blobs are pinned. `READY`, `PASS`, and executed source behavior remain distinct. Changed or missing evidence HOLDs.

**Agency / non-domination** — this refinement never sets the donor `--run` path and grants no execution, merge, promotion, or CANON authority.

**Continuity** — the earlier receipt, archive, and finalization evidence remains intact. This run extends INV-20 rather than silently replacing its meaning.

**Wisdom before speed** — only 15 retained routes and three fail-closed mutations are inspected. The lab does not model the entire evolved Monolith.

## Evidence ceiling

This proves only the exact pinned donor planning/gating behavior for the retained native-smoke recipes. It does not prove the underlying source commands succeed, deployed products work, future producer refs remain compatible, every native command in the Monolith is safe, or any constitutional/CANON authority.
