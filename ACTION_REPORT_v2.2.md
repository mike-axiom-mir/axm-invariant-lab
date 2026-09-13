# AXM Invariant Lab — Action Report v2.2

## Decision

**GROW / INV-20 promoted to executable Connected Monolith receipt refinement.**

The bounded run used the newly supplied `AXM_Connected_Monolith_v0.3.2.zip.receipt.json` as a large-system evidence boundary rather than adding another solver encoding or donor-specific toy fixture.

## Starting state inspected

Invariant Lab `main` started at `fb314b5417f06f1613c608f91be8e96f176dac99` with no open PR. Hosted `main` workflow run `34734319735` had completed SUCCESS on that exact commit. The preserved `RESEARCH_SEED_v0.1.md` remains provenance and explicitly says fresh evidence outranks the seed.

Existing semantic overlap was inspected before building:

- INV-19 already protects machine-discovery declaration integrity;
- `MONOLITH_PIPELINE_REFINEMENT.md` already protects candidate-only Pipeline Fabric statuses and explicit no-automatic-authority flags;
- current Monolith PR #6 is a separate Ghost Studio asset-trial lane and does not implement receipt-level addressable/wired/callable classification.

The selected delta is therefore the non-promotion boundary between large connected topology and explicit callable evidence.

## Source evidence

The exact supplied result receipt is retained at `fixtures/monolith-connected-zip-v0.3.2.receipt.json` with SHA-256:

`06588a18e592a5b553562ad9a4c5b6f911c943fc4bbcee6ebf86ee56afddcc93`

It reports:

- 38 modules;
- 23,472 endpoints and 23,472 addressable endpoints;
- a six-status adapter partition summing to 23,472 endpoints;
- 23,248 blocked for missing callable binding;
- 68 blocked for missing native contract;
- 3 callable through a named workflow;
- 3 source-callable endpoints and 3 callable workflow stages;
- 3,618 edges, all reported wired;
- 80 compositions, all reported wired.

The receipt's own truth boundary limits workflow proof to the exact Blackline Relay route and leaves unrelated unbound leaf capabilities/candidate compositions blocked.

## Capability delta

Added:

- `adapters/monolith_connected_zip.py`;
- exact source receipt fixture;
- `tests/test_monolith_connected_zip_refinement.py`;
- `tools/run_monolith_connected_zip_refinement.py`;
- retained deterministic evidence at `evidence/monolith-connected-zip-refinement-latest.json`;
- `MONOLITH_CONNECTED_ZIP_REFINEMENT.md`;
- INV-20 in `CANDIDATE_INVARIANTS.md`;
- a dedicated CI evidence-drift gate.

INV-20 is:

> Connected topology, wiring, packaging, or aggregate composition does not by itself establish callability or verification. A consumer may claim callable coverage only from explicit callable evidence, and explicitly blocked states remain blocked.

## Adversarial boundary

Eleven focused tests cover:

- valid reference PASS;
- addressable-count callability promotion FAIL;
- addressability-implies-callability FAIL;
- blocked-endpoint promotion FAIL;
- wired-composition verification promotion FAIL;
- callable-count disagreement FAIL;
- status-partition drift FAIL;
- missing source-callable evidence HOLD;
- future status HOLD;
- future schema HOLD;
- read-only adapter behavior.

## Evidence ceiling

The user supplied the result receipt, not the reported 194 MB archive or its `SNAPSHOT_FILE_RECEIPT.json`. The fixture pins the receipt bytes; it does not independently verify the ZIP contents or its embedded ZIP hash claim.

This run therefore establishes a reusable receipt-level non-promotion check, not a proof of Monolith endpoint existence, runtime execution, Blackline Relay behavior, arbitrary composition correctness, deployment, or real-world operation. It grants no execution, merge, installation, device, network, promotion, or CANON authority.

General model fidelity remains at seed rung 5 / CROSS-IMPLEMENTATION. No rung promotion is claimed.

## Four-root gate

### Truth

The code distinguishes topology/wiring from explicit callability, fails explicit contradictions, and HOLDs future/unknown semantics. The archive itself is not claimed inspected.

### Agency / non-domination

The adapter is read-only and creates no execution or authority path.

### Continuity

The exact supplied receipt bytes and embedded source claims are preserved. Existing Monolith and discovery refinements remain intact rather than being rewritten.

### Wisdom before speed

One narrow aggregate-evidence invariant was added. No generic graph framework, Monolith clone, or universal package verifier was introduced.

## Merge condition

Merge only after the exact final PR head passes the complete hosted workflow on both supported Python versions and an immediate overlap re-scan shows no competing semantic lane.
