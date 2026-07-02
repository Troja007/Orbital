#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = Path("/Users/tschranz/.codex/skills/orbital-run-osquery-live-query/scripts/run_live_query.py")
CATALOG_PATH = ROOT / "local/orbital-catalog-api-cache/stock_query_catalog.json"
OUT_DIR = ROOT / "local/orbital_catalog_windows_validation"


def load_helper():
    spec = importlib.util.spec_from_file_location("orbital_live_query_helper", HELPER_PATH)
    if not spec or not spec.loader:
        raise RuntimeError(f"Could not load helper from {HELPER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


helper = load_helper()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sql_literal(value: object) -> str:
    if isinstance(value, list):
        value = value[0] if value else ""
    text = "" if value is None else str(value)
    return "'" + text.replace("'", "''") + "'"


def inject_default_vars(sql: str, parameters: list[dict]) -> str:
    if "__vars" not in sql or not parameters:
        return sql.strip()
    values = []
    for param in parameters:
        name = param.get("name", "")
        default = param.get("default", "")
        if not name:
            continue
        values.append(f"({sql_literal(name)}, {sql_literal(default)})")
    if not values:
        return sql.strip()
    cte = "__vars(n, v) AS (VALUES " + ", ".join(values) + ")"
    stripped = sql.strip()
    if re.match(r"(?is)^with\s+", stripped):
        return re.sub(r"(?is)^with\s+", f"WITH {cte},\n", stripped, count=1)
    return f"WITH {cte}\n{stripped}"


def normalized_os(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).lower() for item in value]


def active_windows_queries(catalog: dict) -> list[dict]:
    queries = []
    for entry in catalog.get("queries") or []:
        if entry.get("disabled") or entry.get("deprecated"):
            continue
        if "windows" not in normalized_os(entry.get("os")):
            continue
        if not entry.get("osQuery"):
            continue
        queries.append(entry)
    return queries


def compact_entry(entry: dict, sequence: int) -> dict:
    labels = [item.get("label") for item in entry.get("osQuery") or []]
    return {
        "sequence": sequence,
        "catalog_id": entry.get("id"),
        "title": entry.get("title"),
        "description": entry.get("description", ""),
        "os": entry.get("os") or [],
        "categories": entry.get("categories") or [],
        "tactics": entry.get("tactics") or {},
        "techniques": entry.get("techniques") or {},
        "parameters": entry.get("parameters") or [],
        "warnings": entry.get("warnings") or [],
        "osquery_count": len(entry.get("osQuery") or []),
        "labels": labels,
        "created": entry.get("created"),
        "updated": entry.get("updated"),
    }


def build_osquery(entry: dict) -> list[dict]:
    parameters = entry.get("parameters") or []
    rendered = []
    for item in entry.get("osQuery") or []:
        label = item.get("label") or entry.get("id") or "catalog_query"
        name = item.get("name") or entry.get("title") or label
        sql = inject_default_vars(item.get("sql") or "", parameters)
        rendered.append({"label": label, "name": name, "sql": sql})
    return rendered


def post_query(region: str, token: str, target: str, entry: dict, timeout: int) -> tuple[int, dict, dict]:
    body = {
        "name": f"Catalog validation: {entry.get('title') or entry.get('id')}",
        "nodes": [target],
        "interval": 0,
        "expiry": int(time.time()) + 120,
        "osQuery": build_osquery(entry),
    }
    request = Request(
        f"{helper.SERVERS[region]}/query",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "accept": "application/json",
        },
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8") or "{}")
        return response.status, payload, dict(response.headers.items())


def summarize_results(payload: dict) -> dict:
    rows, meta = helper.parse_any_rows(payload if isinstance(payload, dict) else {})
    result_summaries = helper.summarize_job_results(payload if isinstance(payload, dict) else {})
    label_columns: dict[str, list[str]] = {}
    label_errors: dict[str, str] = {}
    label_row_counts: dict[str, int] = {}
    for row in rows:
        label = str(row.get("label") or "")
        if row.get("error"):
            label_errors[label] = str(row.get("error"))
            continue
        label_row_counts[label] = label_row_counts.get(label, 0) + 1
        cols = label_columns.setdefault(label, [])
        for key in row:
            if key not in {"host", "nodeId", "label"} and key not in cols:
                cols.append(key)
    endpoint_errors = []
    for endpoint in result_summaries.get("endpoints") or []:
        if endpoint.get("endpoint_error"):
            endpoint_errors.append(endpoint.get("endpoint_error"))
    return {
        "answered_endpoint_count": len(meta),
        "row_count": len(rows),
        "labels_returned": sorted(set(label_row_counts) | set(label_errors)),
        "label_row_counts": label_row_counts,
        "label_columns": label_columns,
        "label_errors": label_errors,
        "endpoint_errors": endpoint_errors,
        "meta_present": bool(meta),
    }


def fetch_results_with_grace(region: str, token: str, job_id: str, timeout: int, attempts: int, delay_seconds: int) -> tuple[dict, dict, int]:
    last_response: dict = {}
    last_summary: dict = {}
    for attempt in range(1, attempts + 1):
        last_response = helper.fetch_job(region, token, str(job_id), timeout, results=True)
        last_summary = summarize_results(last_response["payload"])
        if last_summary.get("meta_present"):
            return last_response, last_summary, attempt
        if attempt < attempts:
            time.sleep(delay_seconds)
    return last_response, last_summary, attempts


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def write_markdown_summary(path: Path, records: list[dict]) -> None:
    latest_by_sequence: dict[int, dict] = {}
    for record in records:
        sequence = int(record.get("catalog", {}).get("sequence", 0) or 0)
        if not sequence:
            continue
        latest_by_sequence[sequence] = record
    records = [latest_by_sequence[key] for key in sorted(latest_by_sequence)]
    lines = [
        "# Windows Catalog Query Validation",
        "",
        f"Updated: {utc_now()}",
        "",
        "| Seq | Catalog ID | Title | Job ID | Status | Rows | Endpoint answered | Notes |",
        "| --- | --- | --- | --- | --- | ---: | --- | --- |",
    ]
    for record in records:
        catalog = record.get("catalog", {})
        result = record.get("result_summary", {})
        notes = []
        if record.get("api_error"):
            notes.append("API error")
        if result.get("label_errors"):
            notes.append("query label error")
        if result.get("endpoint_errors"):
            notes.append("endpoint error")
        if not result.get("meta_present") and record.get("orbital_queryID"):
            notes.append("no endpoint metadata")
        lines.append(
            "| {seq} | `{cid}` | {title} | `{job}` | {status} | {rows} | {answered} | {notes} |".format(
                seq=catalog.get("sequence", ""),
                cid=str(catalog.get("catalog_id", "")).replace("|", "\\|"),
                title=str(catalog.get("title", "")).replace("|", "\\|"),
                job=record.get("orbital_queryID") or "",
                status=record.get("status") or record.get("api_status") or "",
                rows=result.get("row_count", 0),
                answered="yes" if result.get("meta_present") else "no",
                notes=", ".join(notes),
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="host:EXAMPLE-HOST")
    parser.add_argument("--delay-seconds", type=int, default=30)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--region", default="")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--start-sequence", type=int, default=1)
    parser.add_argument("--stop-on-no-response", action="store_true", default=True)
    parser.add_argument("--env-file", default="tools-and-memory/orbital_credentials.env")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    os.chdir(ROOT)
    helper.load_env_file(args.env_file)
    region = (args.region or os.environ.get("ORBITAL_REGION") or "eu").strip().lower()
    token = ""
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    queue = active_windows_queries(catalog)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT_DIR / "windows_catalog_execution_manifest.json"
    results_path = OUT_DIR / "windows_catalog_execution_results.jsonl"
    summary_path = OUT_DIR / "windows_catalog_execution_summary.md"
    state_path = OUT_DIR / "windows_catalog_execution_state.json"
    manifest = [compact_entry(entry, index + 1) for index, entry in enumerate(queue)]
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    existing_records = []
    if results_path.exists():
        for line in results_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                existing_records.append(json.loads(line))
    completed_sequences = {
        int(r.get("catalog", {}).get("sequence", 0))
        for r in existing_records
        if r.get("status") in {"completed", "stopped_no_endpoint_response", "no_job_id"}
    }
    all_records = list(existing_records)

    print(json.dumps({
        "event": "queue_ready",
        "target": args.target,
        "region": region,
        "windows_catalog_queries": len(queue),
        "already_completed": len(completed_sequences),
        "manifest": str(manifest_path),
        "results": str(results_path),
        "summary": str(summary_path),
    }), flush=True)

    executed_this_run = 0
    for index, entry in enumerate(queue, start=1):
        if index < args.start_sequence or index in completed_sequences:
            continue
        if args.limit and executed_this_run >= args.limit:
            break
        catalog_info = compact_entry(entry, index)
        record = {
            "recorded_at": utc_now(),
            "target": args.target,
            "catalog": catalog_info,
            "status": "started",
        }
        print(json.dumps({"event": "start", "sequence": index, "catalog_id": entry.get("id"), "title": entry.get("title")}), flush=True)
        try:
            token = helper.fetch_access_token(region, args.timeout)
            api_status, payload, headers = post_query(region, token, args.target, entry, args.timeout)
            job_id = helper.top_level_orbital_query_id(payload, headers)
            record.update({
                "api_status": api_status,
                "orbital_queryID": job_id,
                "status": "submitted",
                "errors": payload.get("errors") if isinstance(payload, dict) else None,
            })
            helper.append_run_ledger(
                "local/orbital_query_runs/live_query_runs.jsonl",
                {
                    "record_type": "orbital_catalog_validation_submission",
                    "recorded_at": utc_now(),
                    "region": region,
                    "api_path": "/query",
                    "status": api_status,
                    "orbital_queryID": job_id,
                    "query_label": entry.get("id"),
                    "query_name": entry.get("title"),
                    "targets": [args.target],
                    "task_name": "Windows Orbital catalog validation on Marble",
                    "catalog_id": entry.get("id"),
                    "catalog_sequence": index,
                },
            )
            if job_id:
                polls, wait_status = helper.poll_job_status(region, token, str(job_id), args.timeout, 10, 20)
                record["job_status_polls"] = helper.compact_status_polls(polls)
                record["wait_status"] = wait_status
                job_results, result_summary, result_attempts = fetch_results_with_grace(
                    region,
                    token,
                    str(job_id),
                    args.timeout,
                    attempts=7,
                    delay_seconds=30,
                )
                record["job_results_status"] = job_results["status"]
                record["job_results_attempts"] = result_attempts
                record["result_summary"] = result_summary
                record["status"] = "completed"
                helper.append_run_ledger(
                    "local/orbital_query_runs/live_query_runs.jsonl",
                    {
                        "record_type": "orbital_catalog_validation_results",
                        "recorded_at": utc_now(),
                        "region": region,
                        "api_path": "/query",
                        "status": job_results["status"],
                        "orbital_queryID": job_id,
                        "query_label": entry.get("id"),
                        "query_name": entry.get("title"),
                        "targets": [args.target],
                        "task_name": "Windows Orbital catalog validation on Marble",
                        "catalog_id": entry.get("id"),
                        "catalog_sequence": index,
                        "answered_endpoint_count": result_summary.get("answered_endpoint_count"),
                        "row_count": result_summary.get("row_count"),
                    },
                )
                if args.stop_on_no_response and not result_summary.get("meta_present"):
                    record["status"] = "stopped_no_endpoint_response"
                    append_jsonl(results_path, record)
                    all_records.append(record)
                    write_markdown_summary(summary_path, all_records)
                    state_path.write_text(json.dumps({"stopped_at": utc_now(), "reason": "no_endpoint_response", "sequence": index, "catalog_id": entry.get("id"), "orbital_queryID": job_id}, indent=2), encoding="utf-8")
                    print(json.dumps({"event": "stop", "reason": "no_endpoint_response", "sequence": index, "job_id": job_id}), flush=True)
                    return 3
            else:
                record["status"] = "no_job_id"
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            record.update({"status": "api_http_error", "api_status": exc.code, "api_error": body[:2000]})
        except (RuntimeError, URLError, TimeoutError) as exc:
            record.update({"status": "api_runtime_error", "api_error": str(exc)})

        append_jsonl(results_path, record)
        all_records.append(record)
        write_markdown_summary(summary_path, all_records)
        state_path.write_text(json.dumps({"updated_at": utc_now(), "last_sequence": index, "last_catalog_id": entry.get("id"), "last_status": record.get("status"), "last_job_id": record.get("orbital_queryID")}, indent=2), encoding="utf-8")
        executed_this_run += 1
        print(json.dumps({"event": "done", "sequence": index, "catalog_id": entry.get("id"), "status": record.get("status"), "job_id": record.get("orbital_queryID"), "rows": (record.get("result_summary") or {}).get("row_count", 0)}), flush=True)

        if index < len(queue):
            print(json.dumps({"event": "sleep", "seconds": args.delay_seconds}), flush=True)
            time.sleep(args.delay_seconds)

    state_path.write_text(json.dumps({"completed_at": utc_now(), "executed_this_run": executed_this_run, "total_catalog_queries": len(queue)}, indent=2), encoding="utf-8")
    print(json.dumps({"event": "complete", "executed_this_run": executed_this_run, "total_catalog_queries": len(queue)}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
