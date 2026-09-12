from __future__ import annotations

import ast
from pathlib import Path, PurePosixPath
from typing import Any

OUTPUT_SCHEMA = "axm.invariant-lab.discovery-integrity/v0.1"
SUPPORTED_SCHEMA_MAJOR = "1"
SUPPORTED_ENTRYPOINT_KINDS = {"python-library", "python-cli"}


def _problem(
    code: str,
    message: str,
    *,
    entrypoint: str | None = None,
    capability: str | None = None,
) -> dict[str, str]:
    item = {"code": code, "message": message}
    if entrypoint is not None:
        item["entrypoint"] = entrypoint
    if capability is not None:
        item["capability"] = capability
    return item


def _safe_relative_path(raw: Any) -> tuple[bool, str]:
    if not isinstance(raw, str) or not raw.strip():
        return False, "path must be a non-empty string"
    path = PurePosixPath(raw)
    if path.is_absolute() or ".." in path.parts:
        return False, "path must stay inside the repository"
    return True, raw


def _top_level_symbols(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    symbols: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            symbols.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    symbols.add(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            symbols.add(node.target.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                symbols.add(alias.asname or alias.name.split(".")[0])
    return symbols


def inspect(root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    holds: list[dict[str, str]] = []

    schema_version = manifest.get("schema_version")
    if not isinstance(schema_version, str) or not schema_version:
        failures.append(_problem("manifest.schema.missing", "schema_version must be a non-empty string"))
    elif schema_version.split(".", 1)[0] != SUPPORTED_SCHEMA_MAJOR:
        holds.append(_problem("manifest.schema.unsupported", f"unsupported schema major: {schema_version}"))

    module = manifest.get("module")
    if not isinstance(module, dict):
        failures.append(_problem("manifest.module.invalid", "module must be an object"))
    else:
        for key in ("name", "purpose"):
            if not isinstance(module.get(key), str) or not module[key].strip():
                failures.append(_problem(f"manifest.module.{key}", f"module.{key} must be a non-empty string"))

    capabilities = manifest.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        failures.append(_problem("capabilities.invalid", "capabilities must be a non-empty list"))
        capabilities = []

    seen_capabilities: set[str] = set()
    for index, capability in enumerate(capabilities):
        if not isinstance(capability, dict):
            failures.append(_problem("capability.invalid", f"capability #{index} must be an object"))
            continue
        capability_id = capability.get("id")
        if not isinstance(capability_id, str) or not capability_id.strip():
            failures.append(_problem("capability.id.missing", f"capability #{index} needs a non-empty id"))
            continue
        if capability_id in seen_capabilities:
            failures.append(_problem("capability.id.duplicate", "capability id is duplicated", capability=capability_id))
        seen_capabilities.add(capability_id)
        if not isinstance(capability.get("description"), str) or not capability["description"].strip():
            failures.append(_problem("capability.description", "description must be a non-empty string", capability=capability_id))
        for key in ("provides", "accepts", "tags"):
            value = capability.get(key)
            if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
                failures.append(_problem(f"capability.{key}", f"{key} must be a list of non-empty strings", capability=capability_id))
        evidence = capability.get("evidence")
        if not isinstance(evidence, dict):
            failures.append(_problem("capability.evidence", "evidence must be an object", capability=capability_id))
        else:
            for key in ("status", "ceiling"):
                if not isinstance(evidence.get(key), str) or not evidence[key].strip():
                    failures.append(_problem(f"capability.evidence.{key}", f"evidence.{key} must be a non-empty string", capability=capability_id))

    entrypoints = manifest.get("entrypoints")
    if not isinstance(entrypoints, list) or not entrypoints:
        failures.append(_problem("entrypoints.invalid", "entrypoints must be a non-empty list"))
        entrypoints = []

    seen_entrypoints: set[tuple[str, str, str]] = set()
    checked_entrypoints = 0
    for index, entrypoint in enumerate(entrypoints):
        if not isinstance(entrypoint, dict):
            failures.append(_problem("entrypoint.invalid", f"entrypoint #{index} must be an object"))
            continue
        kind = entrypoint.get("kind")
        raw_path = entrypoint.get("path")
        label = f"{kind}:{raw_path}"
        if not isinstance(kind, str) or not kind:
            failures.append(_problem("entrypoint.kind.missing", "entrypoint kind must be a non-empty string", entrypoint=label))
            continue
        path_ok, path_or_error = _safe_relative_path(raw_path)
        if not path_ok:
            failures.append(_problem("entrypoint.path.invalid", path_or_error, entrypoint=label))
            continue
        rel_path = path_or_error
        discriminator = str(entrypoint.get("symbol") or entrypoint.get("command") or "")
        identity = (kind, rel_path, discriminator)
        if identity in seen_entrypoints:
            failures.append(_problem("entrypoint.duplicate", "entrypoint declaration is duplicated", entrypoint=label))
        seen_entrypoints.add(identity)

        if kind not in SUPPORTED_ENTRYPOINT_KINDS:
            holds.append(_problem("entrypoint.kind.unsupported", f"unsupported entrypoint kind: {kind}", entrypoint=label))
            continue

        target = root / rel_path
        if not target.is_file():
            failures.append(_problem("entrypoint.path.missing", "declared entrypoint path does not exist", entrypoint=label))
            continue

        if kind == "python-library":
            symbol = entrypoint.get("symbol")
            if not isinstance(symbol, str) or not symbol:
                failures.append(_problem("entrypoint.symbol.missing", "python-library entrypoint needs a symbol", entrypoint=label))
                continue
            try:
                symbols = _top_level_symbols(target)
            except (OSError, SyntaxError, UnicodeDecodeError) as exc:
                failures.append(_problem("entrypoint.python.unparseable", f"cannot statically inspect python entrypoint: {exc}", entrypoint=label))
                continue
            if symbol not in symbols:
                failures.append(_problem("entrypoint.symbol.absent", f"declared symbol {symbol!r} is absent", entrypoint=label))
                continue
        else:
            command = entrypoint.get("command")
            expected_prefix = f"python {rel_path}"
            if not isinstance(command, str) or not command.strip():
                failures.append(_problem("entrypoint.command.missing", "python-cli entrypoint needs a command", entrypoint=label))
                continue
            if not (command == expected_prefix or command.startswith(expected_prefix + " ")):
                failures.append(_problem("entrypoint.command.path-mismatch", "command does not execute the declared path", entrypoint=label))
                continue
            if "--check" not in command.split():
                failures.append(_problem("entrypoint.command.no-check", "machine-discovery CLI must expose bounded --check mode", entrypoint=label))
                continue
        checked_entrypoints += 1

    status = "FAIL" if failures else ("HOLD" if holds else "PASS")
    return {
        "schema": OUTPUT_SCHEMA,
        "status": status,
        "moduleName": module.get("name") if isinstance(module, dict) else None,
        "manifestSchemaVersion": schema_version,
        "capabilityCount": len(capabilities),
        "entrypointCount": len(entrypoints),
        "checkedEntrypointCount": checked_entrypoints,
        "failureCount": len(failures),
        "holdCount": len(holds),
        "failures": failures,
        "holds": holds,
        "authority": {
            "execution": False,
            "installation": False,
            "merge": False,
            "promotion": False,
            "canon": False,
        },
        "truthBoundary": "Checks local AXM_MODULE structural discoverability only: manifest shape, local path confinement/existence, Python-library symbol presence by static AST inspection, and Python-CLI path/--check declarations. It does not execute discovered entrypoints, prove their semantics, verify donor runtimes, or grant authority.",
    }
