# Candidate invariant map v0.1

These are research candidates, not CANON rules created by this repository.

| ID | Candidate invariant | Formal status |
|---|---|---|
| INV-01 | A candidate/test/transport step cannot silently grant new execution authority. | MODEL NOW |
| INV-02 | Candidate transport/testing cannot silently make content CANON. | MODEL NOW |
| INV-03 | A rollback result labeled successful must resolve to a declared known-good snapshot and preserve its lineage identity. | MODEL NOW |
| INV-04 | Selective inheritance copies only explicitly allowlisted fields; authority fields are excluded unless separately granted. | MODEL NOW |
| INV-05 | Unknown or unobserved required fields never default to a safe value. | ENGINE NOW |
| INV-06 | TruthGrid client directions do not themselves declare authoritative consequences. | ADAPTER NEXT |
| INV-07 | TruthGrid merge receipt `rollbackRef` names the exact base revision it claims to roll back to. | ADAPTER NOW |
| INV-08 | Deterministic duplicate execution should agree on the declared state identity. | ADAPTER NOW |
| INV-09 | Detached checkpoint reconstruction must bind to the checkpoint/source identity it claims to reconstruct. | ADAPTER LATER |
| INV-10 | Donor adaptation preserves source identity and makes held/ambiguous fields explicit. | MODEL/ADAPTER LATER |
| INV-11 | Technical execution credentials do not outrank the four constitutional roots. | HUMAN/JUDGMENT BOUNDARY |
| INV-12 | A tested/transported candidate may move between repos without gaining merge/CANON authority from transport itself. | CROSS-REPO MODEL NOW |
| INV-13 | Every oracle-required check for a sparse transition must be awakened; a missed required check forbids an oracle-equivalence claim for that step. | EXECUTION-RECEIPT ADAPTER NOW |
| INV-14 | When runtime-observed activation identifies a check omitted by declared sparse routing, and that check produces an output change present in the sparse mismatch set, sparse oracle-equivalence must be rejected for that transition. | RUNTIME-OBSERVATION ADAPTER NOW |

The purpose of the lab is to discover which of these survive precise modeling.
If a candidate requires vague interpretation to make the predicate return true,
it stays outside formal scope.
