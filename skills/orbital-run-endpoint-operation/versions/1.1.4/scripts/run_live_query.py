#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SERVERS = {
    "na": "https://orbital.amp.cisco.com/v0",
    "us": "https://orbital.amp.cisco.com/v0",
    "apjc": "https://apjc.orbital.amp.cisco.com/v0",
    "eu": "https://eu.orbital.amp.cisco.com/v0",
}

TOKEN_SERVERS = {
    "na": "https://visibility.amp.cisco.com/iroh/oauth2/token",
    "us": "https://visibility.amp.cisco.com/iroh/oauth2/token",
    "apjc": "https://visibility.apjc.amp.cisco.com/iroh/oauth2/token",
    "eu": "https://visibility.eu.amp.cisco.com/iroh/oauth2/token",
}

TARGET_PREFIXES = {
    "allowOS",
    "amp",
    "ampuuid",
    "cm",
    "cmid",
    "anyconnectudid",
    "host",
    "hostname",
    "hwaddr",
    "orb",
    "orbital",
    "ip",
    "ip4",
    "ipv4",
    "ip6",
    "ipv6",
    "mac",
    "machine",
    "os",
    "nodeversion",
    "osqueryversion",
    "netmask",
    "random",
    "queryId",
}

JOB_ID_HEADERS = {
    "jobid",
    "x-job-id",
    "location",
}


ORG_CONTEXT_VERSION = 1


def default_org_mapping_state_file() -> str:
    return str(
        Path.home()
        / ".codex"
        / "state"
        / "cisco-security-api-access"
        / "current_org_mapping.json"
    )


def env_list(names: list[str]) -> list[str]:
    values: list[str] = []
    for name in names:
        raw = os.environ.get(name, "")
        if raw:
            values.extend(split_org_values([raw]))
    return values


def split_org_values(values: list[str]) -> list[str]:
    orgs: list[str] = []
    for value in values:
        for part in value.replace(";", ",").split(","):
            cleaned = part.strip()
            if cleaned and cleaned not in orgs:
                orgs.append(cleaned)
    return orgs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a Cisco Orbital osquery query against explicit target selectors."
    )
    parser.add_argument(
        "--job-id",
        default="",
        help="Existing Orbital query/job ID. When set, do not run a new query; fetch /jobs/{ID}.",
    )
    parser.add_argument(
        "--job-results",
        action="store_true",
        help="With --job-id, fetch /jobs/{ID}/results instead of /jobs/{ID}.",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="With --job-id, print query/result summaries without full stored result payload.",
    )
    parser.add_argument(
        "--raw-response",
        action="store_true",
        help="Include raw API response and response headers in output for response-shape debugging.",
    )
    parser.add_argument(
        "--run-ledger",
        default="local/orbital_query_runs/live_query_runs.jsonl",
        help="JSONL ledger for query job IDs and status metadata. Stores no endpoint rows.",
    )
    parser.add_argument(
        "--org-context-file",
        default=os.environ.get(
            "ORBITAL_ORG_CONTEXT_FILE", "local/orbital_query_runs/org_context.json"
        ),
        help="Local non-secret ORG context cache. It does not select the Orbital API tenant.",
    )
    parser.add_argument(
        "--org-mapping-state-file",
        default=os.environ.get("ORBITAL_ORG_MAPPING_STATE_FILE", default_org_mapping_state_file()),
        help="Codex ORG Mapping state JSON. Used before the legacy local ORG context file.",
    )
    parser.add_argument(
        "--org-group",
        default=os.environ.get("ORBITAL_ORG_GROUP", ""),
        help="Active ORG group label. It must match the selected Codex ORG Mapping alias.",
    )
    parser.add_argument(
        "--org",
        action="append",
        default=env_list(["ORBITAL_ORG", "ORBITAL_ORGS"]),
        help="Explicit ORG label or ID to associate with the active ORG group. Can be repeated; comma-separated env values are also supported.",
    )
    parser.add_argument(
        "--task-id",
        default=os.environ.get("ORBITAL_TASK_ID", ""),
        help="Optional investigation/task identifier used to group multiple query jobs in the run ledger.",
    )
    parser.add_argument(
        "--task-name",
        default=os.environ.get("ORBITAL_TASK_NAME", ""),
        help="Optional investigation/task name used to group multiple query jobs in the run ledger.",
    )
    parser.add_argument(
        "--scheduled",
        action="store_true",
        help="Create a scheduled query with POST /query. Host/hostname targets use this mode by default.",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Force a live query with POST /query/run instead of the default scheduled mode for host targets.",
    )
    parser.add_argument(
        "--target",
        action="append",
        default=[],
        help="Orbital node selector such as host:NAME, ipv4:10.0.0.1, netmask:CIDR, orb:ID, or queryId:ID. Can be repeated.",
    )
    parser.add_argument(
        "--approve-broad-target",
        action="store_true",
        help="Required for all, random, OS, CIDR, and broad wildcard target selectors.",
    )
    parser.add_argument(
        "--host",
        action="append",
        default=[],
        help="Deprecated convenience input. Hostname without prefix; converted to host:<value>. Can be repeated.",
    )
    parser.add_argument("--label", default="", help="Orbital osQuery label.")
    parser.add_argument("--name", default="", help="Query display name.")
    parser.add_argument("--sql-file", default="", help="File containing SQL. Defaults to stdin.")
    parser.add_argument(
        "--env-file",
        default=os.environ.get("ORBITAL_ENV_FILE", ""),
        help="Explicit credential env file. Defaults to the source_env_file from Codex ORG Mapping state.",
    )
    parser.add_argument("--region", default="", help="Override ORBITAL_REGION.")
    parser.add_argument("--expiry-minutes", default="2")
    parser.add_argument(
        "--interval-seconds",
        default="0",
        help="Scheduled query interval in seconds. Default 0 creates a one-shot scheduled query.",
    )
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument(
        "--no-status-poll",
        action="store_true",
        help="After submitting a new query, do not poll /jobs/{ID} for short status updates.",
    )
    parser.add_argument(
        "--poll-delay-seconds",
        type=int,
        default=10,
        help="Seconds to wait before first /jobs/{ID} status poll.",
    )
    parser.add_argument(
        "--poll-max-seconds",
        type=int,
        default=20,
        help="Maximum seconds after submission to spend polling /jobs/{ID}.",
    )
    parser.add_argument(
        "--os",
        action="append",
        default=[],
        help="Optional API os field value. Adds all hosts with the listed OS to the target set. Can be repeated.",
    )
    parser.add_argument(
        "--allow-os",
        action="append",
        default=[],
        help="Optional API allowOS filter value. Filters returned results after target selection. Can be repeated.",
    )
    return parser.parse_args()


def load_env_file(path: str) -> None:
    if not path:
        return
    env_path = Path(path).expanduser()
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def env_file_from_codex_mapping(mapping: dict[str, object]) -> Path | None:
    source_env_file = str(mapping.get("source_env_file") or "").strip()
    if not source_env_file:
        return None
    return Path(source_env_file).expanduser()


def resolve_credential_context(args: argparse.Namespace, mapping: dict[str, object]) -> dict[str, object]:
    if args.env_file:
        env_path = Path(args.env_file).expanduser()
        if not env_path.exists():
            raise RuntimeError(f"Credential env file not found: {env_path}")
        load_env_file(str(env_path))
        return {
            "source": "explicit_env_file",
            "env_file": str(env_path),
            "mapping_state_file": str(Path(args.org_mapping_state_file).expanduser()),
        }

    env_path = env_file_from_codex_mapping(mapping)
    if env_path:
        if not env_path.exists():
            raise RuntimeError(
                "Codex ORG Mapping state references a credential env file that was not found: "
                f"{env_path}"
            )
        load_env_file(str(env_path))
        return {
            "source": "codex_org_mapping_source_env_file",
            "env_file": str(env_path),
            "mapping_state_file": str(Path(args.org_mapping_state_file).expanduser()),
        }

    legacy_env = Path("tools-and-memory/orbital_credentials.env")
    if legacy_env.exists():
        load_env_file(str(legacy_env))
        return {
            "source": "legacy_project_orbital_env_file",
            "env_file": str(legacy_env),
            "mapping_state_file": str(Path(args.org_mapping_state_file).expanduser()),
        }

    return {
        "source": "environment_only",
        "env_file": "",
        "mapping_state_file": str(Path(args.org_mapping_state_file).expanduser()),
    }


def read_sql(args: argparse.Namespace) -> str:
    if args.sql_file:
        sql = Path(args.sql_file).read_text(encoding="utf-8")
    else:
        sql = sys.stdin.read()
    sql = sql.strip()
    if not sql:
        raise RuntimeError("No SQL provided. Use --sql-file or pipe SQL on stdin.")
    return sql


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def append_run_ledger(path: str, record: dict[str, object]) -> None:
    if not path:
        return
    ledger_path = Path(path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def task_context(args: argparse.Namespace) -> dict[str, str]:
    context = {}
    if args.task_id:
        context["task_id"] = args.task_id
    if args.task_name:
        context["task_name"] = args.task_name
    return context


def load_org_context(path: str) -> dict[str, object]:
    context_path = Path(path)
    if not context_path.exists():
        return {}
    try:
        loaded = json.loads(context_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"ORG context file is not valid JSON: {path}: {exc}") from exc
    if not isinstance(loaded, dict):
        raise RuntimeError(f"ORG context file must contain a JSON object: {path}")
    return loaded


def load_codex_org_mapping(path: str) -> dict[str, object]:
    mapping_path = Path(path).expanduser()
    if not mapping_path.exists():
        return {}
    try:
        loaded = json.loads(mapping_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"ORG Mapping state file is not valid JSON: {path}: {exc}") from exc
    if not isinstance(loaded, dict):
        raise RuntimeError(f"ORG Mapping state file must contain a JSON object: {path}")
    mapping = loaded.get("mapping") if isinstance(loaded.get("mapping"), dict) else loaded
    return mapping


def add_org_entry(orgs: list[str], value: object, prefix: str) -> None:
    text = str(value or "").strip()
    if not text:
        return
    entry = f"{prefix}:{text}"
    if entry not in orgs:
        orgs.append(entry)


def org_context_from_codex_mapping(path: str, mapping: dict[str, object]) -> dict[str, object]:
    edr = mapping.get("edr") if isinstance(mapping.get("edr"), dict) else {}
    xdr = mapping.get("xdr") if isinstance(mapping.get("xdr"), dict) else {}
    orbital = mapping.get("orbital") if isinstance(mapping.get("orbital"), dict) else {}
    secure_endpoint_v3 = (
        mapping.get("secure_endpoint_v3")
        if isinstance(mapping.get("secure_endpoint_v3"), dict)
        else {}
    )
    orgs: list[str] = []
    add_org_entry(orgs, edr.get("org_id"), "edr")
    add_org_entry(orgs, edr.get("org_guid"), "edr_guid")
    add_org_entry(orgs, xdr.get("org_id"), "xdr")
    add_org_entry(orgs, orbital.get("org_id"), "orbital")
    add_org_entry(orgs, secure_endpoint_v3.get("organization_identifier"), "secure_endpoint_v3")

    return {
        "source": "codex_org_mapping",
        "org_group": str(mapping.get("mapping_alias") or "").strip(),
        "mapping_name": str(mapping.get("mapping_name") or "").strip(),
        "mapping_state_file": str(Path(path).expanduser()),
        "region": str(mapping.get("region") or "").strip(),
        "orgs": orgs,
        "products": {
            "edr": edr,
            "xdr": xdr,
            "orbital": orbital,
            "secure_endpoint_v3": secure_endpoint_v3,
        },
    }


def validate_org_context_against_mapping(args: argparse.Namespace, mapping: dict[str, object]) -> None:
    provided_group = args.org_group.strip()
    provided_orgs = split_org_values(args.org)
    mapping_alias = str(mapping.get("mapping_alias") or "").strip()
    if provided_orgs and not provided_group:
        if not mapping_alias:
            raise RuntimeError(
                "--org requires --org-group when the selected Codex ORG Mapping has no mapping_alias."
            )
        args.org_group = mapping_alias
        provided_group = mapping_alias
    if provided_group and mapping_alias and provided_group != mapping_alias:
        raise RuntimeError(
            f"--org-group '{provided_group}' does not match the active Codex ORG Mapping alias "
            f"'{mapping_alias}'. Switch the active mapping first or pass the matching "
            "--org-mapping-state-file; an ORG label alone cannot switch the Orbital tenant."
        )


def write_org_context(path: str, context: dict[str, object]) -> None:
    context_path = Path(path)
    context_path.parent.mkdir(parents=True, exist_ok=True)
    context_path.write_text(json.dumps(context, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_org_context(args: argparse.Namespace, region: str) -> dict[str, object]:
    context_path = args.org_context_file
    provided_group = args.org_group.strip()
    provided_orgs = split_org_values(args.org)
    now = utc_now()

    stored = load_org_context(context_path)
    groups = stored.get("groups") if isinstance(stored.get("groups"), dict) else {}
    active_group = str(stored.get("active_org_group") or "").strip()

    if provided_group or provided_orgs:
        source = "provided"
        group = provided_group or active_group or "default"
        existing_group = groups.get(group) if isinstance(groups.get(group), dict) else {}
        existing_orgs = existing_group.get("orgs") if isinstance(existing_group.get("orgs"), list) else []
        orgs = provided_orgs or [str(org) for org in existing_orgs if str(org).strip()]
        groups[group] = {
            "orgs": orgs,
            "region": region,
            "updated_at": now,
            "last_used_at": now,
        }
        stored = {
            "version": ORG_CONTEXT_VERSION,
            "active_org_group": group,
            "groups": groups,
        }
        write_org_context(context_path, stored)
        return {
            "context_file": str(context_path),
            "source": source,
            "org_group": group,
            "orgs": orgs,
        }

    codex_mapping = load_codex_org_mapping(args.org_mapping_state_file)
    if codex_mapping:
        context = org_context_from_codex_mapping(args.org_mapping_state_file, codex_mapping)
        if context.get("org_group") or context.get("orgs"):
            return context

    if active_group and isinstance(groups.get(active_group), dict):
        group_data = groups[active_group]
        stored_orgs = group_data.get("orgs") if isinstance(group_data.get("orgs"), list) else []
        orgs = [str(org) for org in stored_orgs if str(org).strip()]
        group_data["last_used_at"] = now
        group_data["region"] = group_data.get("region") or region
        groups[active_group] = group_data
        stored["groups"] = groups
        write_org_context(context_path, stored)
        return {
            "context_file": str(context_path),
            "source": "legacy_org_context",
            "org_group": active_group,
            "orgs": orgs,
        }

    return {
        "context_file": str(context_path),
        "mapping_state_file": str(Path(args.org_mapping_state_file).expanduser()),
        "source": "unset",
        "org_group": "",
        "orgs": [],
    }


def compact_status_polls(polls: list[dict]) -> list[dict]:
    compact: list[dict] = []
    for poll in polls:
        compact.append(
            {
                "elapsed_seconds": poll.get("elapsed_seconds"),
                "status": poll.get("status"),
                "done_count": poll.get("done_count"),
                "target_count": poll.get("target_count"),
                "submission": poll.get("submission"),
                "update": poll.get("update"),
                "expiry": poll.get("expiry"),
            }
        )
    return compact


def first_env(names: list[str]) -> str:
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return ""


def fetch_access_token(region: str, timeout: int) -> str:
    existing = first_env(
        [
            "ORBITAL_API_TOKEN",
            "ORBITAL_TOKEN",
            "SECUREX_TOKEN",
            "CISCO_SECUREX_TOKEN",
            "CISCO_TOKEN",
            "SECURE_ENDPOINT_BEARER_TOKEN",
            "AMP_BEARER_TOKEN",
            "BEARER_TOKEN",
        ]
    )
    if existing:
        return existing

    client_id = first_env(
        [
            "ORBITAL_CLIENT_ID",
            "SECUREX_CLIENT_ID",
            "SECURE_ENDPOINT_V3_OAUTH_CLIENT_ID",
        ]
    )
    client_secret = first_env(
        [
            "ORBITAL_CLIENT_SECRET",
            "SECUREX_CLIENT_SECRET",
            "SECURE_ENDPOINT_V3_OAUTH_CLIENT_SECRET",
        ]
    )
    if not (client_id and client_secret):
        raise RuntimeError("No Orbital token or client credentials found.")

    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
    token_url = (
        os.environ.get("ORBITAL_TOKEN_URL")
        or os.environ.get("SECURE_ENDPOINT_V3_VISIBILITY_TOKEN_URL")
        or TOKEN_SERVERS[region]
    )
    request = Request(
        token_url,
        data=b"grant_type=client_credentials",
        headers={
            "authorization": f"Basic {credentials}",
            "content-type": "application/x-www-form-urlencoded",
            "accept": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8") or "{}")
    access_token = payload.get("access_token")
    if not access_token:
        raise RuntimeError("Token response did not contain access_token.")
    return access_token


def normalize_targets(args: argparse.Namespace) -> list[str]:
    targets = list(args.target)
    for host in args.host:
        value = host.strip()
        if value.startswith("host:") or value.startswith("hostname:"):
            targets.append(value)
        elif value:
            targets.append(f"host:{value}")

    cleaned: list[str] = []
    for target in targets:
        value = target.strip()
        if not value:
            continue
        if value == "all":
            cleaned.append(value)
            continue
        if ":" not in value:
            raise RuntimeError(
                f"Invalid target selector '{value}'. Use prefix:value, for example host:NAME."
            )
        prefix, suffix = value.split(":", 1)
        if prefix not in TARGET_PREFIXES:
            raise RuntimeError(
                f"Unsupported target prefix '{prefix}'. Check Orbital_Target_Node_Selectors.md."
            )
        if not suffix:
            raise RuntimeError(f"Target selector '{value}' is missing a value after ':'.")
        cleaned.append(value)

    deduped = list(dict.fromkeys(cleaned))
    if not deduped:
        raise RuntimeError("No target selectors provided. Use --target or --host.")
    return deduped


def is_narrow_fqdn_fallback(target: str) -> bool:
    if not (target.startswith("host:") or target.startswith("hostname:")):
        return False
    _, value = target.split(":", 1)
    stem = value[:-1]
    return value.endswith("%") and len(stem) >= 4 and "%" not in stem and "_" not in stem


def validate_target_scope(args: argparse.Namespace, targets: list[str]) -> None:
    prefixes = [target.split(":", 1)[0] for target in targets if ":" in target]
    has_all = "all" in targets
    has_allow_os_selector = "allowOS" in prefixes
    non_filter_targets = [target for target in targets if not target.startswith("allowOS:")]

    if has_all and (len(targets) != 1 or args.allow_os):
        raise RuntimeError("The all selector cannot be combined with other selectors or --allow-os.")
    if has_allow_os_selector and args.allow_os:
        raise RuntimeError("Use either allowOS:<platform> in --target or --allow-os, not both.")
    if not non_filter_targets:
        raise RuntimeError("allowOS filters do not define targets; add at least one endpoint selector.")

    broad = bool(args.os) or has_all
    for target in targets:
        if target == "all":
            continue
        prefix, value = target.split(":", 1)
        if prefix in {"random", "os", "netmask"}:
            broad = True
        elif "%" in value and not is_narrow_fqdn_fallback(target):
            broad = True

    if broad and not args.approve_broad_target:
        raise RuntimeError(
            "Broad target scope requires --approve-broad-target after explicit user approval. "
            "This includes all, random, OS, CIDR, and non-narrow wildcard selectors."
        )


def uses_host_target(targets: list[str]) -> bool:
    return any(target.startswith("host:") or target.startswith("hostname:") for target in targets)


def parse_rows(payload: dict) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    meta: list[dict] = []
    for result in payload.get("results") or []:
        host = result.get("hostName") or result.get("hostname")
        node_id = result.get("nodeId")
        reported = result.get("reported")
        meta.append({"host": host, "nodeId": node_id, "reported": reported})
        if result.get("error"):
            rows.append({"host": host, "nodeId": node_id, "error": result["error"]})
            continue
        for query_result in result.get("queryResult") or []:
            if query_result.get("error"):
                rows.append({"error": query_result["error"], "host": host, "nodeId": node_id})
                continue
            row_payload = query_result.get("queryResultRow") or {}
            columns = row_payload.get("columns") or []
            values = row_payload.get("values") or []
            width = len(columns)
            if not (width and values):
                continue
            for index in range(0, len(values), width):
                chunk = values[index : index + width]
                if len(chunk) == width:
                    rows.append(dict(zip(columns, chunk)))
    return rows, meta


def parse_result_rows(result: dict) -> list[dict]:
    rows: list[dict] = []
    hostinfo = result.get("hostinfo") if isinstance(result.get("hostinfo"), dict) else {}
    host = (
        result.get("hostName")
        or result.get("hostname")
        or hostinfo.get("hostname")
        or result.get("node")
    )
    node_id = result.get("nodeId") or result.get("node")
    for query_result in (result.get("queryResult") or result.get("osQueryResult") or []):
        label = query_result.get("label")
        if query_result.get("error"):
            rows.append(
                {
                    "host": host,
                    "nodeId": node_id,
                    "label": label,
                    "error": query_result["error"],
                }
            )
            continue
        columns = query_result.get("columns") or []
        values = query_result.get("values") or []
        width = len(columns)
        if not (width and values):
            continue
        for index in range(0, len(values), width):
            chunk = values[index : index + width]
            if len(chunk) == width:
                row = {"host": host, "nodeId": node_id, "label": label}
                row.update(dict(zip(columns, chunk)))
                rows.append(row)
    return rows


def parse_any_rows(payload: dict) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    meta: list[dict] = []
    for result in payload.get("results") or []:
        hostinfo = result.get("hostinfo") if isinstance(result.get("hostinfo"), dict) else {}
        host = result.get("hostName") or result.get("hostname") or hostinfo.get("hostname")
        node_id = result.get("nodeId") or result.get("node")
        reported = result.get("reported")
        meta.append({"host": host, "nodeId": node_id, "reported": reported})
        if result.get("error"):
            rows.append({"host": host, "nodeId": node_id, "error": result["error"]})
            continue
        rows.extend(parse_result_rows(result))
    return rows, meta


def parse_immediate_rows(payload: dict) -> tuple[list[dict], list[dict]]:
    """Parse both legacy live-query and stored job/result response shapes."""
    rows, meta = parse_rows(payload)
    if rows or meta:
        return rows, meta
    return parse_any_rows(payload)


def summarize_job_results(payload: dict) -> dict:
    summaries: list[dict] = []
    for result in payload.get("results") or []:
        hostinfo = result.get("hostinfo") if isinstance(result.get("hostinfo"), dict) else {}
        osinfo = hostinfo.get("osinfo") if isinstance(hostinfo.get("osinfo"), dict) else {}
        query_summaries: list[dict] = []
        for query_result in result.get("osQueryResult") or result.get("queryResult") or []:
            values = query_result.get("values")
            columns = query_result.get("columns") or []
            row_count = 0
            if isinstance(values, list) and columns:
                row_count = len(values) // len(columns)
            query_summaries.append(
                {
                    "label": query_result.get("label"),
                    "row_count": row_count,
                    "error": query_result.get("error") or "",
                    "seconds": query_result.get("secs"),
                }
            )
        summaries.append(
            {
                "host": hostinfo.get("hostname") or result.get("hostname") or result.get("node"),
                "nodeId": result.get("node"),
                "reported": result.get("reported"),
                "os": osinfo.get("os"),
                "osname": osinfo.get("osname"),
                "endpoint_error": (result.get("error") or {}).get("en")
                if isinstance(result.get("error"), dict)
                else result.get("error"),
                "total_rowcount": result.get("rowcount"),
                "queries": query_summaries,
            }
        )
    return {"endpoint_count": len(summaries), "endpoints": summaries}


def infer_table_columns(rows: list[dict]) -> list[str]:
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    return columns


def split_query_errors(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    """Separate endpoint/osquery execution errors from returned data rows."""
    data_rows: list[dict] = []
    query_errors: list[dict] = []
    for row in rows:
        if row.get("error"):
            query_errors.append(row)
        else:
            data_rows.append(row)
    return data_rows, query_errors


def job_id_from_headers(headers: dict[str, str]) -> object:
    for key, value in headers.items():
        normalized = key.lower()
        if normalized not in JOB_ID_HEADERS:
            continue
        if not value:
            continue
        if normalized == "location":
            return value.rstrip("/").split("/")[-1]
        return value
    return None


def top_level_orbital_query_id(payload: dict, headers: dict[str, str] | None = None) -> object:
    return payload.get("ID") or payload.get("id") or job_id_from_headers(headers or {})


def first_count(value: object, keys: set[str]) -> int | None:
    if isinstance(value, dict):
        for key in keys:
            candidate = value.get(key)
            if isinstance(candidate, int):
                return candidate
            if isinstance(candidate, str) and candidate.isdigit():
                return int(candidate)
        for child in value.values():
            candidate = first_count(child, keys)
            if candidate is not None:
                return candidate
    elif isinstance(value, list):
        for child in value:
            candidate = first_count(child, keys)
            if candidate is not None:
                return candidate
    return None


def summarize_job_status(payload: dict) -> dict:
    return {
        "done_count": first_count(payload, {"done_count", "doneCount", "answered_count"}),
        "target_count": first_count(
            payload,
            {
                "target_count",
                "targetCount",
                "node_count",
                "nodeCount",
                "total_count",
                "totalCount",
                "endpoint_count",
                "endpointCount",
            },
        ),
        "submission": payload.get("submission"),
        "update": payload.get("update"),
        "expiry": payload.get("expiry"),
        "interval": payload.get("interval"),
    }


def fetch_job(region: str, token: str, job_id: str, timeout: int, results: bool) -> dict:
    suffix = "/results" if results else ""
    request = Request(
        f"{SERVERS[region]}/jobs/{job_id}{suffix}",
        headers={
            "authorization": f"Bearer {token}",
            "accept": "application/json",
        },
        method="GET",
    )
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8") or "{}")
        return {"status": response.status, "payload": payload}


def poll_job_status(
    region: str,
    token: str,
    job_id: str,
    timeout: int,
    delay_seconds: int,
    max_seconds: int,
) -> tuple[list[dict], str]:
    polls: list[dict] = []
    if delay_seconds <= 0 or max_seconds <= 0:
        return polls, "Job status polling skipped because polling interval is disabled."

    elapsed = 0
    previous_done_count: int | None = None
    while elapsed < max_seconds:
        sleep_for = min(delay_seconds, max_seconds - elapsed)
        time.sleep(sleep_for)
        elapsed += sleep_for

        job_response = fetch_job(region, token, job_id, timeout, results=False)
        payload = job_response["payload"]
        status_summary = summarize_job_status(payload if isinstance(payload, dict) else {})
        done_count = status_summary.get("done_count")
        poll_record = {
            "elapsed_seconds": elapsed,
            "status": job_response["status"],
            **status_summary,
        }
        polls.append(poll_record)

        if previous_done_count is not None and done_count == previous_done_count:
            return (
                polls,
                f"Stopped waiting after {elapsed}s because responded endpoint count did not increase. Use orbital_queryID {job_id} with /v0/jobs/{job_id} or /v0/jobs/{job_id}/results for follow-up.",
            )
        previous_done_count = done_count if isinstance(done_count, int) else previous_done_count

    return (
        polls,
        f"Stopped waiting after {max_seconds}s maximum. Use orbital_queryID {job_id} with /v0/jobs/{job_id} or /v0/jobs/{job_id}/results for follow-up.",
    )


def has_completed_endpoint(polls: list[dict]) -> bool:
    return any(isinstance(poll.get("done_count"), int) and poll["done_count"] > 0 for poll in polls)


def main() -> int:
    args = parse_args()
    task = task_context(args)
    codex_mapping = load_codex_org_mapping(args.org_mapping_state_file)
    mapping_region = str(codex_mapping.get("region") or "").strip().lower()
    region = (
        args.region
        or os.environ.get("ORBITAL_REGION")
        or mapping_region
        or os.environ.get("SECURE_ENDPOINT_REGION")
        or "eu"
    ).strip().lower()
    if region not in SERVERS:
        raise RuntimeError(f"Unsupported region: {region}")
    validate_org_context_against_mapping(args, codex_mapping)
    org_context = resolve_org_context(args, region)
    credential_context = resolve_credential_context(args, codex_mapping)

    token = fetch_access_token(region, args.timeout)

    if args.job_id:
        job_response = fetch_job(region, token, args.job_id, args.timeout, args.job_results)
        payload = job_response["payload"]
        rows, meta = parse_any_rows(payload if isinstance(payload, dict) else {})
        data_rows, query_errors = split_query_errors(rows)
        output = {
            "status": job_response["status"],
            "region": region,
            "mode": "job_results" if args.job_results else "job_status",
            "orbital_queryID": args.job_id,
            "response_id": args.job_id,
            "org_context": org_context,
            "credential_context": credential_context,
            "task_id": args.task_id,
            "task_name": args.task_name,
            "answered_endpoint_count": len(meta),
            "row_count": len(data_rows),
            "query_error_count": len(query_errors),
            "table_columns": infer_table_columns(data_rows),
            "meta": meta,
        }
        if query_errors:
            output["query_errors"] = query_errors
        if args.summary_only and args.job_results and isinstance(payload, dict):
            output["summary"] = summarize_job_results(payload)
        else:
            output["rows"] = data_rows
        if args.raw_response:
            output["raw_response"] = payload
        append_run_ledger(
            args.run_ledger,
            {
                "record_type": "orbital_existing_job_lookup",
                "recorded_at": utc_now(),
                "region": region,
                "mode": "job_results" if args.job_results else "job_status",
                "status": job_response["status"],
                "orbital_queryID": args.job_id,
                "answered_endpoint_count": len(meta),
                "row_count": len(data_rows),
                "query_error_count": len(query_errors),
                "summary_only": args.summary_only,
            }
            | task,
        )
        print(json.dumps(output, indent=2))
        return 0

    if not args.label:
        raise RuntimeError("--label is required when running a new live query.")

    sql = read_sql(args)
    targets = normalize_targets(args)
    validate_target_scope(args, targets)
    scheduled_mode = bool(args.scheduled or (uses_host_target(targets) and not args.live))
    if args.live and args.scheduled:
        raise RuntimeError("Use only one of --live or --scheduled.")
    expiry_minutes = int(args.expiry_minutes)
    interval_seconds = int(args.interval_seconds)

    body: dict[str, object] = {
        "name": args.name or args.label,
        "nodes": targets,
        "osQuery": [{"label": args.label, "name": args.name or args.label, "sql": sql}],
    }
    if scheduled_mode:
        body["expiry"] = int(time.time()) + (expiry_minutes * 60)
        body["interval"] = interval_seconds
    else:
        body["expiryInMinutes"] = str(args.expiry_minutes)
    if args.os:
        body["os"] = args.os
    if args.allow_os:
        body["allowOS"] = args.allow_os

    api_path = "/query" if scheduled_mode else "/query/run"
    request = Request(
        f"{SERVERS[region]}{api_path}",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "accept": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=args.timeout) as response:
        payload = json.loads(response.read().decode("utf-8") or "{}")
        status = response.status
        response_headers = dict(response.headers.items())

    rows, meta = parse_immediate_rows(payload)
    data_rows, query_errors = split_query_errors(rows)
    orbital_query_id = top_level_orbital_query_id(payload, response_headers)
    output = {
        "status": status,
        "region": region,
        "query_mode": "scheduled" if scheduled_mode else "live",
        "api_path": api_path,
        "targets": targets,
        "submitted_sql": sql,
        "query_label": args.label,
        "query_name": args.name or args.label,
        "orbital_queryID": orbital_query_id,
        "response_id": orbital_query_id,
        "org_context": org_context,
        "credential_context": credential_context,
        "task_id": args.task_id,
        "task_name": args.task_name,
        "errors": payload.get("errors"),
        "answered_endpoint_count": len(meta),
        "row_count": len(data_rows),
        "query_error_count": len(query_errors),
        "table_columns": infer_table_columns(data_rows),
        "meta": meta,
        "rows": data_rows,
    }
    if query_errors:
        output["query_errors"] = query_errors
    ledger_base = {
        "record_type": "orbital_query_submission",
        "recorded_at": utc_now(),
        "region": region,
        "query_mode": "scheduled" if scheduled_mode else "live",
        "api_path": api_path,
        "status": status,
        "orbital_queryID": orbital_query_id,
        "query_label": args.label,
        "query_name": args.name or args.label,
        "targets": targets,
        "sql_sha256": sha256_text(sql),
        "response_had_immediate_rows": bool(data_rows),
        "immediate_answered_endpoint_count": len(meta),
        "immediate_row_count": len(data_rows),
        "immediate_query_error_count": len(query_errors),
        "errors": payload.get("errors"),
    } | task
    append_run_ledger(args.run_ledger, ledger_base)
    output["run_ledger"] = args.run_ledger
    if args.raw_response:
        output["response_headers"] = response_headers
        output["raw_response"] = payload
    if not orbital_query_id:
        output["job_check_status"] = (
            f"Job status was not checked because the POST {api_path} response did not expose a job ID. "
            "The submission was still recorded in the run ledger."
        )
        append_run_ledger(
            args.run_ledger,
            {
                "record_type": "orbital_query_job_id_missing",
                "recorded_at": utc_now(),
                "region": region,
                "query_mode": "scheduled" if scheduled_mode else "live",
                "api_path": api_path,
                "query_label": args.label,
                "query_name": args.name or args.label,
                "targets": targets,
                "sql_sha256": sha256_text(sql),
                "status": status,
            }
            | task,
        )
    if orbital_query_id and not args.no_status_poll:
        try:
            polls, poll_message = poll_job_status(
                region,
                token,
                str(orbital_query_id),
                args.timeout,
                args.poll_delay_seconds,
                args.poll_max_seconds,
            )
            output["job_status_polls"] = polls
            output["wait_status"] = poll_message
            append_run_ledger(
                args.run_ledger,
                {
                    "record_type": "orbital_query_job_status_check",
                    "recorded_at": utc_now(),
                    "region": region,
                    "query_mode": "scheduled" if scheduled_mode else "live",
                    "api_path": api_path,
                    "orbital_queryID": orbital_query_id,
                    "query_label": args.label,
                    "query_name": args.name or args.label,
                    "targets": targets,
                    "sql_sha256": sha256_text(sql),
                    "polls": compact_status_polls(polls),
                    "wait_status": poll_message,
                }
                | task,
            )
            if not data_rows and has_completed_endpoint(polls):
                job_results = fetch_job(region, token, str(orbital_query_id), args.timeout, results=True)
                result_payload = job_results["payload"]
                result_rows, result_meta = parse_any_rows(result_payload if isinstance(result_payload, dict) else {})
                result_data_rows, result_query_errors = split_query_errors(result_rows)
                append_run_ledger(
                    args.run_ledger,
                    {
                        "record_type": "orbital_query_job_results_check",
                        "recorded_at": utc_now(),
                        "region": region,
                        "query_mode": "scheduled" if scheduled_mode else "live",
                        "api_path": api_path,
                        "status": job_results["status"],
                        "orbital_queryID": orbital_query_id,
                        "query_label": args.label,
                        "query_name": args.name or args.label,
                        "targets": targets,
                        "sql_sha256": sha256_text(sql),
                        "answered_endpoint_count": len(result_meta),
                        "row_count": len(result_data_rows),
                        "query_error_count": len(result_query_errors),
                    }
                    | task,
                )
                if result_rows or result_meta:
                    output["job_results_status"] = job_results["status"]
                    output["answered_endpoint_count"] = len(result_meta)
                    output["row_count"] = len(result_data_rows)
                    output["query_error_count"] = len(result_query_errors)
                    output["table_columns"] = infer_table_columns(result_data_rows)
                    output["meta"] = result_meta
                    output["rows"] = result_data_rows
                    if result_query_errors:
                        output["query_errors"] = result_query_errors
                    if args.raw_response:
                        output["raw_job_results"] = result_payload
        except (HTTPError, URLError, RuntimeError) as exc:
            output["job_check_status"] = (
                "The query was submitted and recorded, but follow-up status/results retrieval failed: "
                f"{exc}. Reuse orbital_queryID {orbital_query_id}; do not resubmit the query."
            )
            append_run_ledger(
                args.run_ledger,
                {
                    "record_type": "orbital_query_job_check_error",
                    "recorded_at": utc_now(),
                    "region": region,
                    "orbital_queryID": orbital_query_id,
                    "error": str(exc),
                }
                | task,
            )
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(json.dumps({"status": exc.code, "error_body": body[:2000]}, indent=2))
        raise SystemExit(2)
    except (RuntimeError, URLError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        raise SystemExit(1)
