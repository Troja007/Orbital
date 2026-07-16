#!/usr/bin/env python3
"""Run an observational Cisco Orbital catalog script against explicit targets."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import run_live_query as common


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run an observational Orbital catalog script against explicit targets."
    )
    parser.add_argument("--catalog-id", required=True, help="Stock or organization catalog script ID.")
    parser.add_argument("--target", action="append", default=[], help="Orbital node selector. Can be repeated.")
    parser.add_argument("--host", action="append", default=[], help="Deprecated host convenience input.")
    parser.add_argument("--os", action="append", required=True, help="Supported endpoint OS. Can be repeated.")
    parser.add_argument("--name", required=True, help="Displayed live-script job name.")
    parser.add_argument("--timeout", type=int, default=180, help="HTTP timeout in seconds.")
    parser.add_argument("--request-duration-seconds", type=int, default=20)
    parser.add_argument("--expiry-minutes", type=int, default=2)
    parser.add_argument("--region", default="", help="Override ORBITAL_REGION.")
    parser.add_argument("--env-file", default=os.environ.get("ORBITAL_ENV_FILE", ""))
    parser.add_argument(
        "--org-context-file",
        default=os.environ.get("ORBITAL_ORG_CONTEXT_FILE", "local/orbital_script_runs/org_context.json"),
    )
    parser.add_argument(
        "--org-mapping-state-file",
        default=os.environ.get("ORBITAL_ORG_MAPPING_STATE_FILE", common.default_org_mapping_state_file()),
    )
    parser.add_argument("--org-group", default=os.environ.get("ORBITAL_ORG_GROUP", ""))
    parser.add_argument("--org", action="append", default=common.env_list(["ORBITAL_ORG", "ORBITAL_ORGS"]))
    parser.add_argument("--task-id", default=os.environ.get("ORBITAL_TASK_ID", ""))
    parser.add_argument("--task-name", default=os.environ.get("ORBITAL_TASK_NAME", ""))
    parser.add_argument(
        "--run-ledger",
        default="local/orbital_script_runs/live_script_runs.jsonl",
        help="Local JSONL operation/error ledger. Endpoint output is never written here.",
    )
    parser.add_argument("--approve-broad-target", action="store_true")
    return parser.parse_args()


def task_context(args: argparse.Namespace) -> dict[str, str]:
    return {
        key: value
        for key, value in {"task_id": args.task_id, "task_name": args.task_name}.items()
        if value
    }


def validate_targets(args: argparse.Namespace, targets: list[str]) -> None:
    broad = "all" in targets
    for target in targets:
        if target == "all":
            continue
        prefix, value = target.split(":", 1)
        if prefix in {"random", "os", "netmask"}:
            broad = True
        elif "%" in value and not common.is_narrow_fqdn_fallback(target):
            broad = True
    if broad and not args.approve_broad_target:
        raise RuntimeError("Broad script target scope requires --approve-broad-target.")


def script_results(payload: dict[str, object]) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for result in payload.get("results") or []:
        if not isinstance(result, dict):
            continue
        results.append(
            {
                "exit_code": result.get("exit_code"),
                "stdout": result.get("stdout") or "",
                "stderr": result.get("stderr") or "",
                "reported": result.get("reported"),
            }
        )
    return results


def append_error(args: argparse.Namespace, phase: str, scope: str, error: object, status: int | None = None) -> None:
    message = common.error_text(error)
    record: dict[str, object] = {
        "record_type": "orbital_error",
        "recorded_at": common.utc_now(),
        "phase": phase,
        "scope": scope,
        "error": message,
        "error_sha256": common.sha256_text(message),
        "api_path": "/script/run",
    }
    if status is not None:
        record["http_status"] = status
    common.append_run_ledger(args.run_ledger, record | task_context(args))


def main() -> int:
    args = parse_args()
    phase = "mapping_resolution"
    try:
        mapping = common.load_codex_org_mapping(args.org_mapping_state_file)
        mapping_region = str(mapping.get("region") or "").strip().lower()
        region = (args.region or os.environ.get("ORBITAL_REGION") or mapping_region or "eu").lower()
        if region not in common.SERVERS:
            raise RuntimeError(f"Unsupported region: {region}")
        common.validate_org_context_against_mapping(args, mapping)
        phase = "target_validation"
        targets = common.normalize_targets(args)
        validate_targets(args, targets)
        phase = "credential_resolution"
        credential_context = common.resolve_credential_context(args, mapping)
        org_context = common.resolve_org_context(args, region)
        phase = "token_request"
        token = common.fetch_access_token(region, args.timeout)
        body = {
            "name": args.name,
            "nodes": targets,
            "os": list(dict.fromkeys(args.os)),
            "expiryinminutes": str(args.expiry_minutes),
            "requestdurationsec": str(args.request_duration_seconds),
            "script": {"catalog_id": args.catalog_id, "name": args.name},
        }
        phase = "script_submission"
        request = Request(
            f"{common.SERVERS[region]}/script/run",
            data=json.dumps(body).encode("utf-8"),
            headers={"authorization": f"Bearer {token}", "content-type": "application/json", "accept": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=args.timeout) as response:
            payload = json.loads(response.read().decode("utf-8") or "{}")
            status = response.status
    except HTTPError as exc:
        append_error(args, phase, "api_response", {"http_status": exc.code}, exc.code)
        print(json.dumps({"status": exc.code, "api_path": "/script/run", "error": "Orbital API rejected the script request."}))
        return 1
    except Exception as exc:
        append_error(args, phase, "foundational", exc)
        print(json.dumps({"api_path": "/script/run", "error": f"Script operation failed during {phase}."}))
        return 1

    errors = [error for error in payload.get("errors") or [] if common.meaningful_error(error)]
    results = script_results(payload)
    exit_codes = Counter(str(row["exit_code"]) for row in results if row.get("exit_code") is not None)
    if errors:
        append_error(args, "script_response", "api_response", errors, status)
    output = {
        "status": status,
        "mode": "live_script",
        "api_path": "/script/run",
        "catalog_id": args.catalog_id,
        "operation_class": "observational",
        "targets": targets,
        "os": body["os"],
        "result_id": payload.get("result_id"),
        "answered_endpoint_count": len(results),
        "exit_code_counts": dict(exit_codes),
        "script_error_count": len(errors),
        "results": results,
        "context": common.public_context_summary(org_context, credential_context),
    }
    if errors:
        output["errors"] = errors
    common.append_run_ledger(
        args.run_ledger,
        {
            "record_type": "orbital_live_script",
            "recorded_at": common.utc_now(),
            "region": region,
            "api_path": "/script/run",
            "catalog_id": args.catalog_id,
            "operation_class": "observational",
            "status": status,
            "result_id": payload.get("result_id"),
            "answered_endpoint_count": len(results),
            "exit_code_counts": dict(exit_codes),
            "script_error_count": len(errors),
        }
        | task_context(args),
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
