# Use small worlds to discover reusable counterexamples

Status: proposed applications of an existing method; documentation only.
Inspected source: `b65dc277802de27dca6f92ae68b1afc8c1d0920a`.

[Shared method and measured neural example](https://github.com/mike-axiom-mir/axm-state-research/blob/main/docs/SIMULATION_AS_REUSABLE_EXPERIENCE.md).

The [bounded explorer](src/bounded_explorer.py),
[independent path verifier](src/reference_verifier.py) and
[cross-verifier](src/cross_verifier.py) already provide the relevant machinery.
Their PASS/FAIL/HOLD meanings remain authoritative.

## First useful comparison

Start with one current donor refinement, such as
[Wakeup Fuzzer](STATE_RESEARCH_WAKEUP_FUZZER_REFINEMENT.md).
Vary explicit transition ordering and dependency omissions inside an authored
model. Preserve the shortest failing trace and the exact model/source revision.
Replay it against a donor execution before calling it a donor bug.

Compare visited-state exploration, the independent path enumerator where its
budget permits, and a seeded sampling baseline. Report state/path counts,
coverage and exhausted budgets separately; sampled success is not exhaustive
bounded PASS. Keep the [tractability limit](TRACTABILITY_BOUNDARY.md) visible.

## Retained value and limits

Useful accumulated knowledge is a minimized counterexample plus an executable
regression and a clearer model boundary. A neural scheduler may later prioritize
which modeled cases to try; it cannot reinterpret HOLD as PASS or manufacture
donor fidelity. The two explorers share authored model functions, so agreement
does not independently validate the model.

Any exported failure uses the existing counterexample packet and
[consumer continuity rules](EXTERNAL_CONSUMERS.json). This note changes no
explorer, packet, consumer pin, authority field or evidence rung.
