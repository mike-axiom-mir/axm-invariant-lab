AXM / AXIOM–MIR
RESEARCH SEED
Date: 2026-09-11

STATUS
------
RESEARCH SEED / NOT CANON / NOT BUILT / NO REPO CREATED BY THIS FILE

ROOTS
-----
Truth · Agency · Continuity · Wisdom before speed

FOUNDING RULE
-------------
This file preserves a research direction. It does not create authority, canon,
a merge decision, or a claim that the proposed architecture is correct.

Preserve existing AXM work. Do not rebuild working systems merely because this
research lane exists. Fresh evidence outranks this document.

REPO CANDIDATE
--------------
axm-invariant-lab

FIELD
-----
Formal Invariants & Model Checking

ESTIMATED MULTIPLIER
--------------------
10/10

1. CORE RESEARCH QUESTION
-------------------------
Can AXM express its most important safety, authority, continuity, and deterministic-state claims as explicit invariants and then systematically search reachable state-space for counterexamples?

2. WHY THIS COULD MULTIPLY AXM
------------------------------
AXM increasingly relies on state machines, permission boundaries, replay,
rollback, deterministic merge, roots, leases, selective inheritance, and
no-auto-canon rules. Unit tests prove examples. An invariant lane would ask the
harder question: can any reachable sequence of valid transitions violate a rule
we thought was impossible to violate?

That makes this a multiplier across TruthGrid, State Research, WALMI/Mirror,
Universal Creation, multiplayer, lifecycle, merge gates, permission systems,
and future embodied machines.

3. LIVE AXM OVERLAP / DONOR BOUNDARY
------------------------------------
Already present:
- axm-TruthGrid: canonical ordering, hashing, replay, two-instance comparison,
  checkpoint integrity and deterministic failure tests.
- axm-state-research: state -> output / node-state reduction research.
- axm-collaboration-platform: many local invariant-like guards, leases,
  permissions, rollback and evidence gates.
- axm-universal-creation: detached growth, admission boundaries, snapshots,
  explicit source and capability contracts.

Missing as a standalone science lane:
- a small formal state model independent of any one repo;
- machine-checkable invariants spanning multiple transitions;
- automatic counterexample traces;
- refinement between tiny formal models and real AXM implementations.

DO NOT turn this into another generic test framework.

4. THIS REPO WOULD OWN
----------------------
- A minimal AXM invariant vocabulary: state, actor, authority, transition,
  precondition, postcondition, invariant, liveness condition, counterexample.
- Tiny formal models of AXM claims.
- Exhaustive/bounded state exploration where feasible.
- Counterexample reduction into human-readable traces.
- Refinement checks linking a formal model to a bounded implementation fixture.
- A reusable invariant packet format other repos can consume without importing
  this repo as an authority.

5. THIS REPO MUST NOT OWN
-------------------------
- Product-specific business logic.
- Merge/CANON authority.
- Replacement of unit/integration/fuzz tests.
- A claim that mathematical verification proves the real world or unmodelled code.
- Secret chain-of-thought capture.
- A giant universal formal model of all AXM.

6. WORKING HYPOTHESES
---------------------
- H1: Several AXM safety rules can be expressed as small state invariants without encoding implementation detail.
- H2: Bounded exploration will find transition-order bugs ordinary happy-path tests miss.
- H3: Authority and continuity invariants can be reused across otherwise unrelated repos.
- H4: Counterexample traces can be translated into deterministic regression fixtures.
- H5: The smallest useful model will outperform a giant 'formalize everything' attempt.

7. FALSIFICATION / STOP CONDITIONS
---------------------------------
- If useful AXM rules cannot be expressed without smuggling in vague human interpretation, keep them outside formal scope.
- If a model cannot be linked to any executable or observable boundary, label it conceptual only.
- If formal complexity exceeds the value of the bugs/counterexamples it finds, reduce scope instead of expanding the framework.
- If model and implementation diverge, implementation evidence wins and the model must be repaired or retired.

8. FIRST RESEARCH LADDER
------------------------
1. Map 12 existing AXM rules into candidate invariants; no solver yet.
2. Implement a dependency-free bounded state explorer for 2–4 tiny models.
3. Model 'no silent authority escalation', 'no auto-canon', and 'rollback preserves a known-good state'.
4. Generate minimal counterexample traces and convert one into a regression fixture.
5. Add one TruthGrid or State Research refinement adapter.
6. Compare brute-force exploration with a mature formal tool only after the local semantics are understood.
7. Attempt one cross-repo invariant: a candidate may be tested and transported but never silently become authoritative.

9. FIRST ARTIFACTS TO CREATE
----------------------------
- `INVARIANT_CONTRACT.md`
- `models/no_silent_authority.*`
- `models/rollback_continuity.*`
- `models/selective_inheritance.*`
- `src/bounded_explorer.*`
- `COUNTEREXAMPLE_PACKET.schema.json`
- `evidence/first_counterexample_receipt.json`
- `REFINEMENT_BOUNDARY.md`

10. FIRST TEN QUESTIONS
-----------------------
1. What is the smallest formal state needed to represent AXM authority?
2. Which current 'must never happen' rules are actually invariants versus human judgments?
3. Can rollback itself violate continuity?
4. Can two individually legal transitions compose into an illegal state?
5. What does liveness mean without introducing permanent action pressure?
6. How do unknown/unobserved fields remain explicit rather than defaulting to safe values?
7. Can root integrity be represented without defining future WALMI behavior?
8. Which deterministic multiplayer guarantees survive adversarial event ordering?
9. How should counterexamples be stored without becoming canon?
10. Where does formal proof stop and empirical verification begin?

11. EVIDENCE LADDER
-------------------
0. IDEA — question only.
1. SOURCE-MAPPED — existing AXM overlap and relevant precedents identified.
2. CONTRACTED — exact inputs, outputs, authority and failure states declared.
3. FIXTURE-TESTED — deterministic authored fixtures pass and fail as expected.
4. ADVERSARIAL — counterexamples/failure injection tested.
5. CROSS-IMPLEMENTATION — a second implementation or independent verifier agrees
   on a bounded claim.
6. CROSS-REPO — at least two real AXM systems use the result without semantic
   rewriting.
7. REAL-ENVIRONMENT — tested on real users/hardware/networks/platforms where the
   field requires it.
8. RETAIN / REVISE / RETIRE — evidence decides whether the direction continues.

Passing one rung never silently grants the next.

12. ROOT CHECK
--------------
TRUTH
- Unknown, unsupported and conflicting states stay visible.
- A test proves only the claim it actually measures.

AGENCY
- Research output never grants itself execution, merge, device, network or
  CANON authority.
- Existing repo owners remain authoritative for their own systems.

CONTINUITY
- Preserve source identity, lineage, rollback and donor boundaries.
- New research must not require destructive migration of existing AXM work.

WISDOM BEFORE SPEED
- Prefer the smallest falsifiable experiment.
- No-change / HOLD is better than building a duplicate or misleading substrate.

13. REPO CREATION GATE
----------------------
Create the repo only when at least three materially different AXM systems
share an invariant shape and one tiny executable model can either find a real
counterexample or provide a useful proof boundary. Otherwise keep this as a
research note.

14. FIRST FUTURE-BUILDER PROMPT
-------------------------------
/returncore /soulcheck /mergegate

You are opening research candidate `axm-invariant-lab`.

Read this seed first. Then inspect current AXM repositories before creating code.
Treat semantic overlap as overlap even when filenames differ.

Your job is NOT to prove this idea correct.

1. Re-scan current AXM implementations and newest PRs.
2. Mark every relevant capability EXISTING / EXTEND / ADAPT / NEW / HOLD.
3. Choose the smallest unresolved research question from this seed.
4. Define the falsifier before implementation.
5. Build one bounded experiment.
6. Produce evidence and explicit limitations.
7. Do not merge, promote, install, migrate, publish, or declare CANON automatically.
8. If existing AXM work already closes the gap, stop and report that finding.

Return:
- question tested;
- donor systems inspected;
- exact delta;
- test/evidence result;
- what remains unknown;
- whether this candidate still deserves its own repository.

15. ACTION REPORT
-----------------
Created as a stronger future-start file.
No repository was created.
No implementation was claimed.
No existing AXM component was replaced.
The research direction remains optional until its repo-creation gate is met.
