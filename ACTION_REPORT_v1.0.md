# AXM Invariant Lab — Action Report v1.0

## Question tested

Can the lab strengthen its held-out closure boundary using State Research's later unlabeled multi-project challenge without merely adding more traces from the same single-project evidence?

## Pre-build scan

Before claiming work:

- `main` was `4deeb4be118737d550a4736b047e7de8c1f50d2f` (`Capability: held-out observed-read closure ceiling v0.9`);
- the latest main workflow completed SUCCESS;
- there were no open pull requests;
- historical growth branches remained, but no branch or PR owned the unlabeled multi-project refinement;
- `RESEARCH_SEED_v0.1.md` remained preserved unchanged as provenance;
- the existing v0.9 adapter already owned the single-project held-out observed-read completeness ceiling, so semantic overlap ruled out another single-project/favorable-trace extension.

The selected donor frontier was State Research Experiment 06, the frozen unlabeled multi-project closure challenge over two distinct canonical project versions.

## Exact delta

Added **INV-16**:

> A cross-project closure claim is not supported by final equality alone: every held-out project/version must retain zero silent-stale outputs through the trace, and absent/corrupt checkpoints must be quarantined and reconstructed only from verified source with provenance.

Added:

- `adapters/state_research_unlabeled_multiproject_closure.py`;
- `fixtures/state-research-unlabeled-multiproject-closure-v1.projection.json`;
- `tests/test_state_research_unlabeled_multiproject_closure.py`;
- `tools/run_state_research_unlabeled_multiproject_closure_refinement.py`;
- `evidence/STATE_RESEARCH_UNLABELED_MULTIPROJECT_CLOSURE_REFINEMENT.json`;
- `STATE_RESEARCH_UNLABELED_MULTIPROJECT_CLOSURE_REFINEMENT.md`.

The fixture pins the donor repository, commit, evidence paths, and Git blobs. It projects two distinct held-out project identities, ten unlabeled held-out mutations, `OBSERVED_READS`, the separate `COMBINED_STRUCTURAL_OBSERVED` candidate, and checkpoint validation/recovery receipts. Donor `necessary_wakes`, `missed_wakes`, timing measurements, and scoring implementation details are excluded.

## Falsifier

The refinement must fail if any of the following happens:

- the pinned donor identities drift;
- the two held-out project identities collapse into one;
- the observed-only record no longer demonstrates final equality with retained silent stale outputs;
- the selected candidate retains a silent stale output or loses final equality;
- candidate counted work no longer remains below the pinned full-oracle reference;
- an absent/corrupt checkpoint is replayed as trusted instead of quarantined;
- checkpoint reconstruction loses source/replacement identity or provenance-bearing action;
- required evidence disappears, in which case the adapter must HOLD rather than PASS.

## Focused evidence before publication

Local isolated fixture gate: **8/8 PASS**.

Covered:

1. valid projection separates final equality from trace closure;
2. missing required evidence HOLDs;
3. donor blob drift FAILs;
4. removing the hidden-stale evidence invalidates the falsifier;
5. candidate silent-stale output FAILs;
6. duplicate project identity cannot fake cross-project coverage;
7. replaying an untrusted checkpoint FAILs;
8. candidate work must remain below the full-oracle reference.

The deterministic evidence generator also reproduced the retained receipt byte-semantically and `--check` passed locally.

## Measured pinned result

- held-out projects: **2**;
- held-out mutations: **10**;
- declared risk labels in held-out manifest: **false**;
- `OBSERVED_READS`: final equality **true**, silent stale outputs **8** total (**4 + 4** across the two projects);
- `COMBINED_STRUCTURAL_OBSERVED`: final equality **true**, silent stale outputs **0**;
- candidate counted check work: **597**;
- full-oracle held-out reference: **1,955** check executions;
- checkpoint cases: one `corrupt_payload`, one `absent`, both quarantined before reconstruction from verified canonical source.

## Evidence level

No general model-fidelity promotion was made. The bounded exploration/model fidelity ceiling remains seed rung **5 / CROSS-IMPLEMENTATION**. Counterexample packet/result consumption remains separately at rung **6 / CROSS-REPO**.

This run adds a stronger pinned execution-refinement boundary, not an independent donor oracle or real-environment proof.

## Four-root check

**Truth:** PASS is limited to exact pinned fields. Final equality cannot erase transient silent-stale evidence. Missing evidence HOLDs.

**Agency / non-domination:** the adapter is read-only and creates no execution, merge, installation, device, network, or CANON authority.

**Continuity:** donor identity, commit, paths, Git blobs, project identities, checkpoint failure modes, source hashes, and replacement checkpoint hashes remain explicit.

**Wisdom before speed:** the run extends the exact unresolved multi-project question and does not add a generic test framework, solver dependency, or donor reimplementation.

## Remaining unknown

The donor's own report still leaves open cross-version evaluator changes, opaque helpers without useful path-shaped signals, unreconstructable checkpoints, organic histories, effectful checks, concurrency, additional project families, and checkpoint trust across processes/runtimes/machines.

Those unknowns remain research. A later run should advance only if one of them can be tested with a materially different falsifier rather than by increasing fixture count.
