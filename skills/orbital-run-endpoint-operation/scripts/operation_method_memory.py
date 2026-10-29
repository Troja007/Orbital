#!/usr/bin/env python3
"""Persist non-sensitive runtime knowledge from Cisco Orbital query execution."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator


STATE_VERSION = 1
MAX_METHODS = 200


def default_memory_file() -> Path:
    return Path.home() / ".codex" / "state" / "orbital-run-endpoint-operation" / "query_method_memory.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sql_fingerprint(sql: str) -> str:
    return hashlib.sha256(sql.encode("utf-8")).hexdigest()


def target_kinds(targets: list[str]) -> list[str]:
    kinds = []
    for target in targets:
        prefix = target.split(":", 1)[0].casefold() if ":" in target else "unknown"
        if prefix not in kinds:
            kinds.append(prefix)
    return kinds


def outcome_class(status: object, answered: int, row_count: int, query_errors: int) -> str:
    if query_errors:
        return "endpoint_query_error"
    if not isinstance(status, int) or status >= 400:
        return "api_error"
    if answered < 1:
        return "no_response"
    if row_count < 1:
        return "no_hit"
    return "completed"


def load_memory(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"schema_version": STATE_VERSION, "methods": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid Orbital runtime memory: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"Invalid Orbital runtime memory: {path}: expected object")
    if not isinstance(data.get("methods"), list):
        data["methods"] = []
    return data


def atomic_write(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.chmod(temporary_name, 0o600)
        os.replace(temporary_name, path)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise


@contextmanager
def state_lock(path: Path) -> Iterator[None]:
    """Serialize state updates from concurrently running Codex tasks."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_suffix(path.suffix + ".lock")
    handle = lock_path.open("a+", encoding="utf-8")
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
    try:
        yield
    finally:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


def record_query(
    memory_file: Path,
    *,
    sql: str,
    tables: list[str],
    targets: list[str],
    execution_profile: str,
    query_mode: str,
    status: object,
    answered_endpoint_count: int,
    row_count: int,
    query_error_count: int,
) -> dict[str, object] | None:
    """Update generic query method memory without persisting evidence or query text."""
    fingerprint = sql_fingerprint(sql)
    safe_tables = [table for table in tables if isinstance(table, str) and table]
    safe_kinds = target_kinds(targets)
    key = "|".join(("query", fingerprint, ",".join(safe_tables), execution_profile, query_mode))
    now = utc_now()
    outcome = outcome_class(status, answered_endpoint_count, row_count, query_error_count)
    entry: dict[str, object] = {
        "key": key,
        "operation": "query",
        "sql_fingerprint": fingerprint,
        "tables": safe_tables,
        "target_selector_kinds": safe_kinds,
        "execution_profile": execution_profile,
        "query_mode": query_mode,
        "last_outcome": outcome,
        "last_used_at_utc": now,
    }
    try:
        with state_lock(memory_file):
            memory = load_memory(memory_file)
            prior = next(
                (item for item in memory["methods"] if isinstance(item, dict) and item.get("key") == key),
                {},
            )
            entry["execution_count"] = int(prior.get("execution_count", 0)) + 1 if isinstance(prior, dict) else 1
            if outcome in {"completed", "no_hit"}:
                entry["last_success_at_utc"] = now
                entry["success_count"] = int(prior.get("success_count", 0)) + 1 if isinstance(prior, dict) else 1
            elif isinstance(prior, dict) and prior.get("last_success_at_utc"):
                entry["last_success_at_utc"] = prior["last_success_at_utc"]
                entry["success_count"] = int(prior.get("success_count", 0))
            methods = [
                item for item in memory["methods"]
                if not isinstance(item, dict) or item.get("key") != key
            ]
            methods.insert(0, entry)
            atomic_write(memory_file, {
                "schema_version": STATE_VERSION,
                "saved_at_utc": now,
                "methods": methods[:MAX_METHODS],
            })
    except (OSError, ValueError):
        return None
    return {
        "saved": True,
        "memory_file": str(memory_file),
        "key": key,
        "outcome": outcome,
    }


def show(args: argparse.Namespace) -> int:
    try:
        memory = load_memory(args.memory_file)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    methods = memory["methods"]
    if args.table:
        wanted = set(args.table)
        methods = [
            item for item in methods
            if isinstance(item, dict) and wanted.intersection(item.get("tables", []))
        ]
    print(json.dumps({"memory_file": str(args.memory_file), "methods": methods}, indent=2, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect non-sensitive Orbital query runtime memory.")
    parser.add_argument("--memory-file", type=Path, default=default_memory_file())
    parser.add_argument("--table", action="append", default=[], help="Filter by osquery table name.")
    args = parser.parse_args()
    return show(args)


if __name__ == "__main__":
    raise SystemExit(main())
