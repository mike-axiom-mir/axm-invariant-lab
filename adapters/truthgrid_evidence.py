"""Read-only refinement checks for bounded TruthGrid evidence receipts."""

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class RefinementResult:
    status: str
    checks: list[dict[str, Any]]
    unknowns: list[str]
    failures: list[str]

    def to_dict(self):
        return asdict(self)


def inspect(receipt: dict[str, Any]) -> RefinementResult:
    checks: list[dict[str, Any]] = []
    unknowns: list[str] = []
    failures: list[str] = []

    def require(path: str, value):
        if value is None:
            unknowns.append(path)
            return None
        return value

    schema = require("schema", receipt.get("schema"))
    if schema is not None:
        ok = schema == "axm.truthgrid-evidence/v0.01"
        checks.append({"check": "schema", "ok": ok})
        if not ok:
            failures.append("unsupported schema")

    final_hash = require("finalHash", receipt.get("finalHash"))
    two = receipt.get("twoInstance")
    if two is None:
        unknowns.append("twoInstance")
    else:
        equal = require("twoInstance.equal", two.get("equal"))
        hash_a = require("twoInstance.hashA", two.get("hashA"))
        hash_b = require("twoInstance.hashB", two.get("hashB"))
        if None not in (equal, hash_a, hash_b, final_hash):
            ok = bool(equal) and hash_a == hash_b == final_hash
            checks.append({"check": "two-instance-final-hash", "ok": ok})
            if not ok:
                failures.append("two-instance final hashes disagree")

    ticks = receipt.get("ticks")
    if ticks is None:
        unknowns.append("ticks")
    elif not isinstance(ticks, list):
        failures.append("ticks is not a list")
    else:
        for index, tick in enumerate(ticks):
            merge = tick.get("merge")
            if merge is None:
                unknowns.append(f"ticks[{index}].merge")
                continue

            base = require(f"ticks[{index}].merge.baseRevision", merge.get("baseRevision"))
            resulting = require(
                f"ticks[{index}].merge.resultingRevision", merge.get("resultingRevision")
            )
            rollback = require(
                f"ticks[{index}].merge.rollbackRef", merge.get("rollbackRef")
            )
            tick_hash = require(f"ticks[{index}].hash", tick.get("hash"))
            merge_hash = require(
                f"ticks[{index}].merge.resultingHash", merge.get("resultingHash")
            )

            if base is not None and resulting is not None:
                ok = resulting == base + 1
                checks.append({"check": f"tick-{index+1}-revision-step", "ok": ok})
                if not ok:
                    failures.append(f"tick {index+1} revision does not advance by one")

            if base is not None and rollback is not None:
                ok = rollback == f"revision:{base}"
                checks.append({"check": f"tick-{index+1}-rollback-ref", "ok": ok})
                if not ok:
                    failures.append(f"tick {index+1} rollbackRef does not bind baseRevision")

            if tick_hash is not None and merge_hash is not None:
                ok = tick_hash == merge_hash
                checks.append({"check": f"tick-{index+1}-result-hash", "ok": ok})
                if not ok:
                    failures.append(f"tick {index+1} merge hash disagrees with tick hash")

    status = "FAIL" if failures else ("HOLD" if unknowns else "PASS")
    return RefinementResult(
        status=status,
        checks=checks,
        unknowns=sorted(set(unknowns)),
        failures=failures,
    )
