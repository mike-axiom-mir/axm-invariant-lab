# Donor scan — 2026-09-12

This scan was performed before the first implementation. The purpose is overlap
control, not ownership.

## Decision

The candidate still deserves its own repository because the donor systems have
strong deterministic examples, replay, integrity, checkpoint, authority and
admission guards, but none of the inspected lanes owns a small repo-independent
bounded state-space explorer with reusable multi-transition invariant packets.

## Capability map

| Capability | State | Donor / boundary |
|---|---|---|
| canonical deterministic ordering + replay | EXISTING | `axm-TruthGrid` |
| state hashing + two-instance comparison | EXISTING | `axm-TruthGrid` |
| merge receipts + rollback references | EXISTING | `axm-TruthGrid` |
| checkpoint reconstruction + detached verification | EXISTING | `axm-state-research` |
| state-to-output / node-state research | EXISTING | `axm-state-research` |
| local leases / permission / rollback / evidence gates | EXISTING | `axm-collaboration-platform` |
| root-based constitutional merge gate | EXISTING | `axm-collaboration-platform` governance |
| detached donor adaptation + source/capability contracts | EXISTING | `axm-universal-creation` |
| exhaustive bounded multi-transition exploration | NEW | this repo |
| shortest machine-readable counterexample traces | NEW | this repo |
| tri-state invariant evaluation where unknown => HOLD | NEW | this repo |
| donor evidence -> invariant observation mapping | ADAPT | this repo, first adapter targets TruthGrid evidence |
| unit / integration / fuzz / replay tests | HOLD | do not replace donor tests |
| giant formal model of AXM | HOLD | explicitly out of scope |
| formalizing qualitative root meaning as mathematics | HOLD | requires human/machine grounded judgment, not silent reduction |

## Fresh-work notes

- TruthGrid current work already demonstrates strict authority envelopes,
  deterministic replay, exact-head evidence, and bounded counterfactual receipts.
  The lab must consume those kinds of receipts, not recreate its engine.
- State Research current work already demonstrates detached checkpoint
  reconstruction and fresh-process verification. The lab must not become a
  second checkpoint verifier.
- Collaboration Platform currently places broad local-Codex platform growth on
  HOLD and has corrected internal constitutional merge authority to the four
  roots. This lab therefore stays small and detached.
- Universal Creation already uses detached donor adapters with explicit HOLD
  state and source identity. This lab follows the same donor-boundary pattern.

## First falsifier

The first useful claim is falsified if a tiny bounded model cannot distinguish:

1. a safe transition system where candidate transport/testing never grants
   authority or CANON state by itself; and
2. a deliberately fault-injected system where two individually admissible
   steps compose into a forbidden authority/canon state.

If the explorer cannot produce the shortest violating trace for (2) while
passing (1), this implementation is not useful enough to continue.
