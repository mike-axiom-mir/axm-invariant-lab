# Connected Monolith donor-finalization refinement — INV-20 v2.4

## Status

Grounded reusable bounded capability. Not CANON. Not a general Monolith verifier.

This extends **INV-20** beyond the detached receipt and frozen v0.3.2 archive into a separately published, donor-owned Monolith implementation boundary:

> Connected topology, wiring, packaging, or aggregate composition does not by itself establish callability or verification; callable coverage must come from explicit callable evidence and blocked states remain blocked.

The original `RESEARCH_SEED_v0.1.md` remains provenance. Fresh implementation evidence controls this refinement.

## Exact donor boundary

Pinned donor repository:

- repository: `mike-axiom-mir/axm-monolith`
- commit: `9586e1d11af4ef5a475105f4568627c7a5fdb312`
- donor CI on that commit: `Assembly unit tests` — SUCCESS

Pinned semantic/test blobs:

- `tools/finalize_connected_snapshot.py` — `bfa1088166fc1cd59806efe79c2867e412e50e13`
- `tools/monolith_plumbing.py` — `39ada899576ab931ae23443de909cae8f05a663e`
- `tools/callable_execution_ledger.py` — `924b9e90464d5361d50228bd84367748621397e8`
- `tools/invoke_declared_callable.py` — `360f474384558628c7fbf0ddea0b6f67b9103a35`
- `tests/test_connected_finalization.py` — `de8bfe355927d81b66724c301fb184f8972e116b`

The commit pin fixes the whole donor tree; the blob pins make the bounded semantics relied on by this refinement explicit.

## Why this is new evidence

v2.2 checked a Connected Monolith result receipt. v2.3 checked the bytes and internal evidence surfaces of one frozen package. v2.4 does neither again.

Instead, CI checks out the exact published Monolith implementation and executes:

1. the donor's own six connected-finalization tests; and
2. an Invariant Lab probe that uses the donor's real plumbing, finalizer, Python callable runtime, and execution ledger.

That tests the **transition from declaration to explicit execution evidence** rather than only a packaged state.

## External probe

The bounded probe creates one synthetic module with two source-declared Python callables:

- `demo-module::demo.double`
- `demo-module::demo.triple`

It then asks the pinned donor implementation to perform four observations:

1. install plumbing and report two callable declarations while `source_callable_executed` remains `0`;
2. attempt to package with `demo.double` required but with no execution ledger, which must fail closed;
3. explicitly opt in to execute only `demo.double`, producing one accepted source-bound receipt;
4. package only after that exact evidence passes, while the ledger must still omit unrequested `demo.triple`.

The package receipt must bind only `demo.double` and retain the donor truth boundary that hashes prove integrity while callable/workflow receipts prove only explicitly required routes; unrelated leaf declarations and candidate compositions remain unexecuted.

## PASS / FAIL / HOLD

**PASS** requires the pinned donor tests to pass and every external observation above to remain exact.

**FAIL** includes:

- plumbing marking declarations executed before an invocation;
- packaging an unproven required callable;
- execution evidence appearing for the unrequested second callable;
- widening the package's required-address set;
- losing the package truth boundary that preserves unrelated gaps;
- donor commit/blob drift; or
- authority escalation in the refinement receipt.

**HOLD** is used when required observations are absent rather than assuming a safe default.

## Reproduction

With the pinned donor checkout available:

```bash
python tools/run_monolith_donor_finalization.py \
  --donor-root /path/to/axm-monolith \
  --check
```

Repository CI performs that exact checkout and command on Python 3.11 and 3.13.

## Evidence ceiling

This verifies one exact published Monolith implementation and one bounded two-callable probe. It does not prove arbitrary modules, arbitrary runtimes, every pipeline, every package, deployment behavior, future donor commits, safety/quality, or constitutional/CANON authority. It also does not make Invariant Lab the owner of Monolith semantics; the donor remains authoritative for its own implementation evidence.
