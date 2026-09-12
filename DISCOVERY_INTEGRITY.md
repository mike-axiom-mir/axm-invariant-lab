# AXM Invariant Lab — Machine Discovery Integrity v0.1

## Question

Can the repository prevent `AXM_MODULE.json` from advertising a local capability entrypoint that is structurally absent, escaped outside the repository, or not actually named by the declared Python symbol/CLI path?

This boundary exists because an earlier growth cycle added a real capability but failed to expose it in machine discovery. The later repair exposed a broader continuity risk: machine discovery can drift away from executable repository structure even while ordinary capability tests stay green.

## INV-19

**A machine-discoverable local entrypoint may be claimed only when its declared repository-local path exists and the declared Python surface is structurally checkable. Unknown discovery kinds remain HOLD, not PASS.**

## Checked boundary

`src/discovery_contract.py` checks only local `AXM_MODULE.json` structure:

- schema/module/capability shape;
- unique capability IDs;
- repository-confined relative entrypoint paths;
- entrypoint file existence;
- declared top-level Python-library symbol presence by static AST inspection;
- Python-CLI command/path agreement;
- explicit bounded `--check` mode on advertised Python CLIs;
- unsupported future schema majors or entrypoint kinds as HOLD rather than silently accepting them.

The checker does **not** import or execute discovered library entrypoints. It does not prove their behavior, donor semantics, deployment, network/device safety, authority, or CANON status.

## Result semantics

- `PASS`: every currently supported machine-discovery declaration passed the structural checks and there were no unknown kinds.
- `FAIL`: a concrete contradiction exists, such as a missing file/symbol, duplicate capability ID, path escape, CLI path mismatch, or advertised CLI without `--check`.
- `HOLD`: the manifest uses a future schema major or entrypoint kind the checker does not understand and there is no concrete FAIL.

Priority is `FAIL > HOLD > PASS`.

## Evidence ceiling

The retained evidence is repository-local structural discoverability only. It does not promote bounded model fidelity beyond seed rung 5, does not add a new external consumer, and does not strengthen the separate rung-6 counterexample-packet claim.

## Authority boundary

The result grants no execution, installation, promotion, merge, device, network, or CANON authority. The four AXM roots remain the merge gate.
