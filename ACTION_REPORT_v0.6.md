# AXM Invariant Lab — Action Report v0.6

## Question tested

Can a second, materially different real AXM system consume Invariant Lab's existing FAIL/HOLD counterexample packet without changing its meaning or gaining authority, so the packet/result contract honestly earns the seed's rung 6 / CROSS-REPO boundary?

## Pre-run scan

- Invariant Lab `main` started at `6bf42a40a052184571f22a50a10ae89ea6aeebed`.
- No open Invariant Lab PRs were present.
- Non-main Invariant Lab branches were historical merged v0.1-v0.5 lanes.
- Latest main workflow run `34689742111` was SUCCESS on that exact head.
- `RESEARCH_SEED_v0.1.md` remains unchanged provenance and explicitly requires at least two real AXM systems for rung 6.
- Existing external-consumer registry contained only AXM Monolith.
- AXM Profession Mesh had no open PR and no invariant-evidence/admission branch before this lane. Its older `foundation/transport-authority-boundary` branch is semantically the already-merged foundation boundary, not a competing consumer lane.

## Why Profession Mesh is materially different

Monolith is a whole-stack assembly/analysis surface. Profession Mesh is a package transport/discovery/verification/admission layer whose founding rule is `transport authority is not profession authority`.

That difference makes Mesh a useful second consumer: the same FAIL/HOLD result is not merely summarized; it becomes bounded receiving evidence while preserving local agency and profession authority boundaries.

## External consumer delta

Profession Mesh PR #3 added:

- `src/invariant-evidence.mjs` — content-addressed v0.1 packet intake;
- exact producer pin in `INVARIANT_LAB_CONSUMER.json`;
- an exact-byte retained packet fixture;
- preservation of source FAIL/HOLD status;
- local policy only: FAIL -> `quarantine`, HOLD -> `hold`;
- `mayAcceptCandidate: false` for all invariant evidence;
- rejection of unsupported PASS, unknown fields, authority escalation, and digest mismatch;
- README boundary documentation;
- adversarial consumer tests while retaining the original Mesh foundation authority test.

Focused local proof passed before publication.

Hosted Profession Mesh workflow run `34692275335` used Node 22 and completed SUCCESS on PR source head `293272e08cf6af0a18f4b011447e10a36957faf9`. Its `npm test` output explicitly passed both:

- `Profession Mesh foundation PASS: transport objects and content-address primitives preserve authority boundary.`
- `Profession Mesh invariant evidence consumer PASS: FAIL/HOLD preserved, candidate acceptance forbidden, authority escalation rejected.`

PR #3 was squash-merged as `8a9a471fd2fda1d2b548c738de96b5249ae17429` after the four-root gate.

## Invariant Lab delta

- register AXM Profession Mesh as the second pinned consumer in `EXTERNAL_CONSUMERS.json`;
- regenerate `evidence/external-consumers-latest.json` with both producer pins intact;
- require registered consumer repositories to be distinct so one system cannot be counted twice accidentally;
- add multi-consumer intact/drift and duplicate-repository regressions;
- update `EXTERNAL_CONSUMERS.md`, README, and `AXM_MODULE.json`;
- promote **only** `invariant.counterexample-packet` / external-consumer continuity to seed rung 6 / CROSS-REPO.

## Falsifier

This promotion fails if:

- Profession Mesh rewrites producer FAIL/HOLD into a different source status;
- invariant evidence can itself accept a Mesh candidate or grant profession/transport authority;
- the consumer accepts unsupported PASS/future fields or authority escalation;
- the exact consumer CI fails;
- producer continuity can count one repository twice;
- either registered consumer pins packet/schema bytes different from current producer bytes;
- the work promotes bounded exploration/model fidelity to rung 6 merely because consumers use an emitted packet.

## Evidence result

Before Invariant Lab publication:

- Profession Mesh focused local consumer proof: PASS;
- Profession Mesh exact PR hosted `npm test`: PASS on Node 22;
- second consumer merged as `8a9a471fd2fda1d2b548c738de96b5249ae17429`;
- deterministic producer continuity generation reports `consumerCount: 2` and `allPinnedProducerContractsIntact: true`;
- both consumers pin packet blob `02eeddfd12351ff6b7647bc412db3695ee45e5b3` and schema blob `cc9f1fde4855a56557ad6338c7595a99fc71cb21`.

Invariant Lab's complete hosted suite and retained-evidence checks remain the final exact-branch merge gate for this lane.

## Evidence promotion

**Promoted:** counterexample packet/result external consumption -> seed **rung 6 / CROSS-REPO**.

Grounds:

- real consumer #1: AXM Monolith, assembly/analysis role;
- real consumer #2: AXM Profession Mesh, transport/admission role;
- both preserve FAIL/HOLD meaning;
- neither grants authority from the packet;
- exact producer byte continuity is pinned for both.

**Not promoted:** bounded exploration/model fidelity remains seed **rung 5 / CROSS-IMPLEMENTATION**. Both search engines still share authored model semantics; consumers using an emitted packet do not independently prove those semantics represent donor runtime behavior.

No solver-backed or real-environment proof is claimed.

## Root check

**Truth:** status meaning stays intact; exact producer/consumer identities are pinned; the promotion is scoped to packet consumption rather than the entire lab.

**Agency / non-domination:** invariant evidence can hold/quarantine a Mesh candidate but cannot accept it, apply a proposal, create profession truth, execute, merge, promote, or declare CANON.

**Continuity:** both consumers pin the same producer packet/schema blobs; producer drift fails closed; duplicate consumer repositories are rejected.

**Wisdom before speed:** one narrow second consumer closed the exact rung-6 gap. No generic consumer framework, solver, or universal model was added.

## Next meaningful frontier

Do **not** add a third consumer merely to raise the count. The next useful gap is model-to-implementation fidelity: derive or observe a bounded real donor transition/receipt and compare it against an Invariant Lab model/refinement without hand-rewriting donor semantics. If that cannot be done narrowly and falsifiably, HOLD is better than more machinery.
