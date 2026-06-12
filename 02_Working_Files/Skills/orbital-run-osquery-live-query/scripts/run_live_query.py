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

RESPONSE_ID_KEYS = {
    "ID",
    "id",
    "queryId",
    "queryID",
    "query_id",
    "jobId",
    "jobID",
    "job_id",
    "requestId",
    "requestID",
    "request_id",
    "responseId",
    "responseID",
    "response_id",
    "runId",
    "runID",
    "run_id",
}

RESPONSE_ID_HEADERS = {
    "id",
    "x-id",
    "queryid",
    "x-query-id",
    "jobid",
    "x-job-id",
    "requestid",
    "x-request-id",
    "responseid",
    "x-response-id",
    "location",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a Cisco Orbital live osquery query against explicit target selectors."
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
        help="JSONL ledger for live query job IDs and status metadata. Stores no endpoint rows.",
    )
    parser.add_argument(
        "--target",
        action="append",
        default=[],
        help="Orbital node selector such as host:NAME, ipv4:10.0.0.1, netmask:CIDR, orb:ID, or queryId:ID. Can be repeated.",
    )
    parser.add_argument(
        "--host",
        action="append",
        default=[],
        help="Deprecated convenience input. Hostname without prefix; converted to host:<value>. Can be repeated.",
    )
    parser.add_argument("--label", default="", help="Orbital osQuery label.")
    parser.add_argument("--name", default="", help="Live query display name.")
    parser.add_argument("--sql-file", default="", help="File containing SQL. Defaults to stdin.")
    parser.add_argument("--env-file", default="02_Working_Files/orbital_credentials.env")
    parser.add_argument("--region", default="", help="Override ORBITAL_REGION.")
    parser.add_argument("--expiry-minutes", default="2")
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
    env_path = Path(path)
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
        ]
    )
    if existing:
        return existing

    client_id = first_env(["ORBITAL_CLIENT_ID", "SECUREX_CLIENT_ID"])
    client_secret = first_env(["ORBITAL_CLIENT_SECRET", "SECUREX_CLIENT_SECRET"])
    if not (client_id and client_secret):
        raise RuntimeError("No Orbital token or client credentials found.")

    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
    request = Request(
        TOKEN_SERVERS[region],
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


def parse_rows(payload: dict) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    meta: list[dict] = []
    for result in payload.get("results") or []:
        host = result.get("hostName") or result.get("hostname")
        node_id = result.get("nodeId")
        reported = result.get("reported")
        meta.append({"host": host, "nodeId": node_id, "reported": reported})
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


def find_response_id(value: object) -> object:
    if isinstance(value, dict):
        for key in RESPONSE_ID_KEYS:
            candidate = value.get(key)
            if candidate:
                return candidate
        for child in value.values():
            candidate = find_response_id(child)
            if candidate:
                return candidate
    elif isinstance(value, list):
        for child in value:
            candidate = find_response_id(child)
            if candidate:
                return candidate
    return None


def find_response_id_in_headers(headers: dict[str, str]) -> object:
    for key, value in headers.items():
        normalized = key.lower()
        if normalized not in RESPONSE_ID_HEADERS:
            continue
        if not value:
            continue
        if normalized == "location":
            return value.rstrip("/").split("/")[-1]
        return value
    return None


def top_level_orbital_query_id(payload: dict, headers: dict[str, str] | None = None) -> object:
    return payload.get("ID") or find_response_id(payload) or find_response_id_in_headers(headers or {})


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


def main() -> int:
    args = parse_args()
    load_env_file(args.env_file)
    region = (args.region or os.environ.get("ORBITAL_REGION") or "eu").strip().lower()
    if region not in SERVERS:
        raise RuntimeError(f"Unsupported region: {region}")

    token = fetch_access_token(region, args.timeout)

    if args.job_id:
        job_response = fetch_job(region, token, args.job_id, args.timeout, args.job_results)
        payload = job_response["payload"]
        rows, meta = parse_any_rows(payload if isinstance(payload, dict) else {})
        output = {
            "status": job_response["status"],
            "region": region,
            "mode": "job_results" if args.job_results else "job_status",
            "orbital_queryID": args.job_id,
            "response_id": args.job_id,
            "answered_endpoint_count": len(meta),
            "row_count": len(rows),
            "table_columns": infer_table_columns(rows),
            "meta": meta,
        }
        if args.summary_only and args.job_results and isinstance(payload, dict):
            output["summary"] = summarize_job_results(payload)
        else:
            output["rows"] = rows
            output["raw_response"] = payload
        print(json.dumps(output, indent=2))
        return 0

    if not args.label:
        raise RuntimeError("--label is required when running a new live query.")

    sql = read_sql(args)
    targets = normalize_targets(args)

    body: dict[str, object] = {
        "name": args.name or args.label,
        "expiryInMinutes": str(args.expiry_minutes),
        "nodes": targets,
        "osQuery": [{"label": args.label, "name": args.name or args.label, "sql": sql}],
    }
    if args.os:
        body["os"] = args.os
    if args.allow_os:
        body["allowOS"] = args.allow_os

    request = Request(
        f"{SERVERS[region]}/query/run",
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
    orbital_query_id = top_level_orbital_query_id(payload, response_headers)
    output = {
        "status": status,
        "region": region,
        "targets": targets,
        "submitted_sql": sql,
        "query_label": args.label,
        "orbital_queryID": orbital_query_id,
        "response_id": orbital_query_id,
        "errors": payload.get("errors"),
        "answered_endpoint_count": len(meta),
        "row_count": len(rows),
        "table_columns": infer_table_columns(rows),
        "meta": meta,
        "rows": rows,
    }
    ledger_base = {
        "record_type": "orbital_live_query_submission",
        "recorded_at": utc_now(),
        "region": region,
        "status": status,
        "orbital_queryID": orbital_query_id,
        "query_label": args.label,
        "query_name": args.name or args.label,
        "targets": targets,
        "sql_sha256": sha256_text(sql),
        "response_had_immediate_rows": bool(rows),
        "immediate_answered_endpoint_count": len(meta),
        "immediate_row_count": len(rows),
        "errors": payload.get("errors"),
    }
    append_run_ledger(args.run_ledger, ledger_base)
    output["run_ledger"] = args.run_ledger
    if args.raw_response:
        output["response_headers"] = response_headers
        output["raw_response"] = payload
    if not orbital_query_id:
        output["job_check_status"] = (
            "Job status was not checked because the POST /query/run response did not expose a job ID. "
            "The submission was still recorded in the run ledger."
        )
        append_run_ledger(
            args.run_ledger,
            {
                "record_type": "orbital_live_query_job_id_missing",
                "recorded_at": utc_now(),
                "region": region,
                "query_label": args.label,
                "query_name": args.name or args.label,
                "targets": targets,
                "sql_sha256": sha256_text(sql),
                "status": status,
            },
        )
    if orbital_query_id and not args.no_status_poll:
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
                "record_type": "orbital_live_query_job_status_check",
                "recorded_at": utc_now(),
                "region": region,
                "orbital_queryID": orbital_query_id,
                "query_label": args.label,
                "query_name": args.name or args.label,
                "targets": targets,
                "sql_sha256": sha256_text(sql),
                "polls": compact_status_polls(polls),
                "wait_status": poll_message,
            },
        )
        if not rows:
            job_results = fetch_job(region, token, str(orbital_query_id), args.timeout, results=True)
            result_payload = job_results["payload"]
            result_rows, result_meta = parse_any_rows(result_payload if isinstance(result_payload, dict) else {})
            append_run_ledger(
                args.run_ledger,
                {
                    "record_type": "orbital_live_query_job_results_check",
                    "recorded_at": utc_now(),
                    "region": region,
                    "status": job_results["status"],
                    "orbital_queryID": orbital_query_id,
                    "query_label": args.label,
                    "query_name": args.name or args.label,
                    "targets": targets,
                    "sql_sha256": sha256_text(sql),
                    "answered_endpoint_count": len(result_meta),
                    "row_count": len(result_rows),
                },
            )
            if result_rows or result_meta:
                output["job_results_status"] = job_results["status"]
                output["answered_endpoint_count"] = len(result_meta)
                output["row_count"] = len(result_rows)
                output["table_columns"] = infer_table_columns(result_rows)
                output["meta"] = result_meta
                output["rows"] = result_rows
                if args.raw_response:
                    output["raw_job_results"] = result_payload
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
