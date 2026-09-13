# Connected Monolith callability refinement boundary — INV-20

## Question

Can a large connected AXM package remain honest about the difference between **addressable/wired** structure and **explicitly callable** evidence?

INV-20 is:

> Connected topology, wiring, packaging, or aggregate composition does not by itself establish callability or verification. A consumer may claim callable coverage only from explicit callable evidence, and explicitly blocked states remain blocked.

This is intentionally narrower than a generic Monolith verifier.

## Why this is not duplicate work

Existing Invariant Lab work already checks two adjacent boundaries:

- INV-19: local/public discovery declarations cannot silently promote unsupported machine-discovery claims;
- the earlier Monolith Pipeline Fabric refinement: candidate pipeline states cannot silently become VERIFIED and automatic authority flags must remain false.

The supplied Connected Monolith receipt exposes a materially different scale/evidence problem: a package can have tens of thousands of addressable endpoints and every reported edge/composition wired while explicit source-callable evidence remains tiny. INV-20 protects that evidence-class distinction.

## Exact source evidence

The retained fixture is an exact copy of the user-supplied file `AXM_Connected_Monolith_v0.3.2.zip.receipt.json`.

- fixture SHA-256: `06588a18e592a5b553562ad9a4c5b6f911c943fc4bbcee6ebf86ee56afddcc93`
- receipt schema: `axm.monolith.connected-zip-result/v0.2`
- reported archive files: `15,956`
- reported modules: `38`
- reported endpoints/addressable endpoints: `23,472`
- reported adapter status partition: `23,472`
- reported `blocked_missing_callable_binding`: `23,248`
- reported `blocked_missing_native_contract`: `68`
- reported `callable_through_named_workflow`: `3`
- reported source-callable endpoints: `3`
- reported callable workflow stages: `3`
- reported edges/wired edges: `3,618 / 3,618`
- reported compositions/wired compositions: `80 / 80`
- reported archive SHA-256 claim: `sha256:f0a0d1d30007d71bb4ded6a9cc03259e5a12ceb7967cd532b12d366ae0cdf55e`

The receipt's own truth boundary says package hashes prove package integrity while the required workflow receipt proves only the exact Blackline Relay route; unrelated unbound leaf capabilities and candidate compositions remain blocked.

## Executable refinement

`adapters/monolith_connected_zip.py` checks only explicit receipt fields. It never opens the referenced ZIP and never executes a Monolith endpoint.

For the supported v0.2 result schema it checks:

1. endpoint/addressable count coherence;
2. exact partition of endpoints across the six declared adapter status classes;
3. agreement among the three explicit callable counts;
4. wired edge/composition counts do not exceed their totals;
5. future/unknown status classes HOLD rather than silently PASS;
6. consumer claims cannot promote addressability, blocked endpoints, or wired compositions into broader callability/verification.

The reference receipt yields PASS with `23,472` classified endpoints and exactly `3` explicitly callable endpoints.

## Falsifiers retained

The focused tests reject or HOLD:

- claiming all addressable endpoints are callable;
- treating addressability itself as callability;
- treating blocked endpoints as callable;
- treating all wired compositions as verified;
- disagreement among source/workflow/status callable counts;
- adapter-status partition drift;
- missing source-callable evidence;
- future unknown status classes;
- future unsupported schemas.

## Evidence ceiling

This is **receipt-level refinement evidence**, not archive verification.

The Invariant Lab did not receive or inspect the reported `194,320,426` byte ZIP or `SNAPSHOT_FILE_RECEIPT.json` during this run. The fixture's embedded ZIP hash is therefore preserved as a claim from the supplied receipt, not independently recomputed from the archive.

PASS does **not** establish that 23,472 endpoints exist in the archive, that the Blackline Relay route executes correctly, that any candidate composition is production-safe, or that a wired graph is executable. It does not grant execution, merge, installation, device, network, promotion, or CANON authority.

General model fidelity remains at the existing seed rung 5 boundary; this receipt does not independently earn a higher rung.
