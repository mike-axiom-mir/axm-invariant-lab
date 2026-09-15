# Candidate invariant map v0.1

These are research candidates, not CANON rules created by this repository.

| ID | Candidate invariant | Formal status |
|---|---|---|
| INV-01 | A candidate/test/transport step cannot silently grant new execution authority. | MODEL + Z3 BOUNDED CROSS-CHECK NOW |
| INV-02 | Candidate transport/testing cannot silently make content CANON. | MODEL NOW |
| INV-03 | A rollback result labeled successful must resolve to a declared known-good snapshot and preserve its lineage identity. | MODEL + DEPTH-6 RECEIPT-LIFECYCLE REGRESSION + Z3 BOUNDED CROSS-CHECK NOW |
| INV-04 | Selective inheritance copies only explicitly allowlisted fields; authority fields are excluded unless separately granted. | MODEL NOW |
| INV-05 | Unknown or unobserved required fields never default to a safe value. | ENGINE NOW |
| INV-06 | TruthGrid client directions do not themselves declare authoritative consequences. | PINNED TRUTHGRID CLIENT-INTENT REFINEMENT NOW |
| INV-07 | TruthGrid merge receipt `rollbackRef` names the exact base revision it claims to roll back to. | ADAPTER NOW |
| INV-08 | Deterministic duplicate execution should agree on the declared state identity. | STATEBORN HOSTILE-TRANSPORT IDEMPOTENCE ADAPTER NOW |
| INV-09 | Detached checkpoint reconstruction must bind to the checkpoint/source identity it claims to reconstruct. | FRESH-PROCESS CHECKPOINT ADAPTER NOW |
| INV-10 | Donor adaptation preserves source identity and makes held/ambiguous fields explicit. | PINNED UNIVERSAL-CREATION DONOR-FIDELITY + DONOR-OWNED EXECUTION REFINEMENT NOW |
| INV-11 | Technical execution credentials do not outrank the four constitutional roots. | HUMAN/JUDGMENT BOUNDARY |
| INV-12 | A tested/transported candidate may move between repos without gaining merge/CANON authority from transport itself. | CROSS-REPO MODEL NOW |
| INV-13 | Every oracle-required check for a sparse transition must be awakened; a missed required check forbids an oracle-equivalence claim for that step. | EXECUTION-RECEIPT ADAPTER NOW |
| INV-14 | When runtime-observed activation identifies a check omitted by declared sparse routing, and that check produces an output change present in the sparse mismatch set, sparse oracle-equivalence must be rejected for that transition. | RUNTIME-OBSERVATION ADAPTER NOW |
| INV-15 | Runtime-observed dependency evidence must not be treated as closure-complete when a frozen held-out mutation yields a minimized silent-stale counterexample under observed-only routing; absent independent closure evidence, the completeness claim fails. | HELD-OUT EXECUTION FALSIFIER NOW |
| INV-16 | A cross-project closure claim is not supported by final equality alone: every held-out project/version must retain zero silent-stale outputs through the trace, and absent/corrupt checkpoints must be quarantined and reconstructed only from verified source with provenance. | UNLABELED MULTIPROJECT EXECUTION REFINEMENT NOW |
| INV-17 | Opaque evaluator results/checkpoints must not cross evaluator-source identity changes as if semantics were unchanged; changed available source needs grounded re-execution or separately established compatibility evidence, while unavailable source keeps affected outputs explicitly unresolved and escalated rather than reconstructing unknown semantics. | CROSS-VERSION OPAQUE RECOVERY REFINEMENT NOW |
| INV-18 | A sparse execution may claim dense-oracle equivalence only if still-live contributions from sleeping components remain in shared reference closure; an identical wake set is insufficient when a sleeping reference contribution is dropped. | REFERENCE-STATE CLOSURE REFINEMENT NOW |
| INV-19 | A machine-discoverable entrypoint or capability may be claimed only when its local declaration is structurally grounded; if projected for public discovery, its declared identity/status must survive external consumer normalization without semantic promotion, while unknown discovery kinds remain HOLD rather than silently PASS. | CROSS-REPO DISCOVERY CONSUMER CHECKED NOW |
| INV-20 | Connected topology, wiring, packaging, or aggregate composition does not by itself establish callability or verification; callable coverage must come from explicit callable evidence and blocked states remain blocked. | CONNECTED MONOLITH RECEIPT + DIRECT ARCHIVE + PINNED DONOR FINALIZATION + PINNED NATIVE-ROUTE EVOLUTION REFINEMENT NOW |

The purpose of the lab is to discover which of these survive precise modeling.
If a candidate requires vague interpretation to make the predicate return true,
it stays outside formal scope.
