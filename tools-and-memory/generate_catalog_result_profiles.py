#!/usr/bin/env python3
"""Generate sanitized catalog result profiles from local validation output."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "local/orbital_catalog_windows_validation/windows_catalog_execution_results.jsonl"
PROFILE_UPDATES_INPUT = ROOT / "local/orbital_catalog_windows_validation/profile_updates.jsonl"
CATALOG_SNAPSHOT_INPUT = ROOT / "queries_and_scripts/catalog_snapshot/stock_query_catalog.json"
OUTPUT_DIR = ROOT / "queries_and_scripts/catalog_result_profiles"


STATUS_PRIORITY = {
    "completed": 3,
    "stopped_no_endpoint_response": 2,
    "api_http_error": 1,
}


MAX_SAMPLE_ROWS_PER_PROFILE = 15
PREFERRED_SAMPLE_ROWS_PER_LABEL = 3
SENSITIVE_COLUMN_RE = re.compile(
    r"(?:account|auth|bearer|client|computer|credential|customer|device|domain|email|endpoint|guid|host|job|"
    r"machine|node|organization|org|password|secret|selector|serial|sid|target|tenant|token|user|uuid|"
    r"(?:^|[_-])ip(?:$|[_-]))",
    re.IGNORECASE,
)
EMAIL_RE = re.compile(r"(?i)^[^\s@]+@[^\s@]+\.[^\s@]+$")
IPV4_RE = re.compile(r"^(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}$")
IPV6_RE = re.compile(r"(?i)^(?:[0-9a-f]{0,4}:){2,7}[0-9a-f]{0,4}$")
GUID_RE = re.compile(r"(?i)^\{?[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\}?$")
WINDOWS_SID_RE = re.compile(r"(?i)^s-1-\d+(?:-\d+){1,}$")
URL_RE = re.compile(r"(?i)^(?:https?|ftp)://")
TARGET_SELECTOR_RE = re.compile(r"(?i)^(?:host|queryid|node|target):")
USER_PROFILE_PATH_RE = re.compile(r"(?i)^[a-z]:\\users\\[^\\]+")
WINDOWS_PATH_RE = re.compile(r"(?i)^[a-z]:\\|^\\\\")
REGISTRY_ROOT_RE = re.compile(r"(?i)^(hklm|hkcu|hku|hkcr|hkey_local_machine|hkey_current_user|hkey_users|hkey_classes_root)(?:\\|$)")
HASH_RE = re.compile(r"(?i)^[0-9a-f]{32}$|^[0-9a-f]{40}$|^[0-9a-f]{64}$")
ISO_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:[ t]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:z|[+-]\d{2}:?\d{2})?)?$")
UNIX_TIMESTAMP_RE = re.compile(r"^\d{10}(?:\.\d+)?$")
SAFE_SAMPLE_VALUE_RE = re.compile(r"^<[a-z0-9:._ -]+>$")


def row_bucket(row_count: int | None) -> str:
    if row_count is None:
        return "unknown"
    if row_count == 0:
        return "zero"
    if row_count <= 10:
        return "low_1_10"
    if row_count <= 100:
        return "medium_11_100"
    if row_count <= 1000:
        return "high_101_1000"
    return "very_high_over_1000"


def sample_redaction_marker(column_name: str) -> str:
    column = column_name.lower()
    if "user" in column or "account" in column or "sid" in column:
        return "<redacted:username>"
    if "host" in column or "computer" in column or "machine" in column or "device" in column:
        return "<redacted:hostname>"
    if "ip" in column or "address" in column:
        return "<redacted:ip>"
    if "guid" in column or "uuid" in column:
        return "<redacted:guid>"
    return "<redacted:sensitive-value>"


def sample_value_shape(column_name: str, value: Any) -> str:
    """Return a structural, non-identifying representation of a sample value."""
    column = str(column_name or "")
    column_lower = column.lower()

    if SENSITIVE_COLUMN_RE.search(column):
        return sample_redaction_marker(column)
    if value is None:
        return "<null>"
    if isinstance(value, bool):
        return "<boolean:true>" if value else "<boolean:false>"
    if isinstance(value, int) and not isinstance(value, bool):
        return "<integer>"
    if isinstance(value, float):
        return "<number>"
    if not isinstance(value, str):
        return "<redacted:structured-value>"

    text = value.strip()
    if not text:
        return "<empty>"
    if EMAIL_RE.match(text):
        return "<redacted:email>"
    if IPV4_RE.match(text) or IPV6_RE.match(text):
        return "<redacted:ip>"
    if GUID_RE.match(text):
        return "<redacted:guid>"
    if WINDOWS_SID_RE.match(text):
        return "<redacted:username>"
    if URL_RE.match(text) or TARGET_SELECTOR_RE.match(text):
        return "<redacted:sensitive-value>"
    if re.match(r"(?i)^(?:bearer\s+|.*(?:token|secret|password|client[_ -]?id).*)", text):
        return "<redacted:sensitive-value>"
    if USER_PROFILE_PATH_RE.match(text):
        return "<path:windows-user-profile>"
    if REGISTRY_ROOT_RE.match(text):
        return "<registry-path>"
    if WINDOWS_PATH_RE.match(text) or "/" in text or "\\" in text:
        return "<path>"
    if HASH_RE.match(text):
        return f"<hash:{len(text)}-hex>"
    if ISO_TIMESTAMP_RE.match(text):
        return "<timestamp:iso-8601>"
    if UNIX_TIMESTAMP_RE.match(text):
        return "<timestamp:unix>"
    if text.lower() in {"true", "false"}:
        return f"<boolean:{text.lower()}>"
    if "extension" in column_lower and re.fullmatch(r"\.[a-z0-9]{1,10}", text, re.IGNORECASE):
        return "<file-extension>"
    if "state" in column_lower or "status" in column_lower:
        return "<state-category>"
    if "process" in column_lower and "name" in column_lower:
        return "<process-name>"

    # Default deny: never copy an arbitrary endpoint string into GitHub output.
    return "<redacted:sensitive-value>"


def sanitize_sample_result_data(raw_sample_data: Any) -> tuple[dict[str, list[dict[str, str]]], str, int]:
    """Sanitize and select representative rows without retaining raw endpoint values."""
    if not isinstance(raw_sample_data, dict) or not raw_sample_data:
        return {}, "not_available", 0

    sanitized_by_label: dict[str, list[dict[str, str]]] = {}
    omitted_rows = 0
    for raw_label, raw_rows in raw_sample_data.items():
        if not isinstance(raw_label, str) or not isinstance(raw_rows, list):
            omitted_rows += 1
            continue
        sanitized_rows: list[dict[str, str]] = []
        for raw_row in raw_rows:
            if not isinstance(raw_row, dict):
                omitted_rows += 1
                continue
            sanitized_row: dict[str, str] = {}
            for raw_column, raw_value in raw_row.items():
                if not isinstance(raw_column, str) or not raw_column.strip():
                    omitted_rows += 1
                    continue
                sanitized_row[raw_column] = sample_value_shape(raw_column, raw_value)
            if sanitized_row:
                sanitized_rows.append(sanitized_row)
            else:
                omitted_rows += 1
        if sanitized_rows:
            sanitized_by_label[raw_label] = sanitized_rows

    selected: dict[str, list[dict[str, str]]] = {}
    labels = sorted(sanitized_by_label)
    for sample_index in range(PREFERRED_SAMPLE_ROWS_PER_LABEL):
        for label in labels:
            if sum(len(rows) for rows in selected.values()) >= MAX_SAMPLE_ROWS_PER_PROFILE:
                break
            rows = sanitized_by_label[label]
            if sample_index < len(rows):
                selected.setdefault(label, []).append(rows[sample_index])
        if sum(len(rows) for rows in selected.values()) >= MAX_SAMPLE_ROWS_PER_PROFILE:
            break

    available_rows = sum(len(rows) for rows in sanitized_by_label.values())
    omitted_rows += max(available_rows - sum(len(rows) for rows in selected.values()), 0)
    if not selected:
        return {}, "omitted_for_privacy", omitted_rows
    if omitted_rows:
        return selected, "partially_omitted_for_privacy", omitted_rows
    return selected, "available", 0


def validate_sanitized_sample_data(sample_data: dict[str, list[dict[str, str]]]) -> None:
    sample_row_count = sum(len(rows) for rows in sample_data.values())
    if sample_row_count > MAX_SAMPLE_ROWS_PER_PROFILE:
        raise ValueError(f"Sample row limit exceeded: {sample_row_count} > {MAX_SAMPLE_ROWS_PER_PROFILE}")
    for label, rows in sample_data.items():
        if not isinstance(label, str) or not isinstance(rows, list):
            raise ValueError("Sample result data has an invalid label structure")
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError("Sample result data has an invalid row structure")
            for column, value in row.items():
                if not isinstance(column, str) or not isinstance(value, str) or not SAFE_SAMPLE_VALUE_RE.fullmatch(value):
                    raise ValueError("Sample result data contains a non-sanitized value")


def sanitize_label_errors(raw_label_errors: Any) -> dict[str, str]:
    if not isinstance(raw_label_errors, dict):
        return {}
    return {
        str(label): "Label error recorded during validation."
        for label, error in raw_label_errors.items()
        if error
    }


def sanitize_endpoint_errors(raw_endpoint_errors: Any) -> list[str]:
    if not isinstance(raw_endpoint_errors, list) or not raw_endpoint_errors:
        return []
    return ["Endpoint error recorded during validation."]


def error_class(record: dict[str, Any]) -> str | None:
    if record.get("status") in {"completed", "completed_direct_verification"}:
        result_summary = record.get("result_summary") or {}
        if result_summary.get("endpoint_errors") or result_summary.get("label_errors"):
            return "completed_with_query_or_endpoint_errors"
        return None

    message = " ".join(str(record.get(key, "")) for key in ("api_error", "errors", "notes"))
    message_lower = message.lower()
    if "authentication required" in message_lower:
        return "result_fetch_authentication_required"
    if "allowos" in message_lower:
        return "request_payload_allowos_format_error"
    if record.get("status") == "stopped_no_endpoint_response":
        return "no_endpoint_response_during_wait_window"
    return record.get("status") or "unknown_error"


def responder_reading(
    catalog: dict[str, Any],
    status: str | None,
    result_summary: dict[str, Any],
    caveat: str | None,
) -> str:
    row_count = result_summary.get("row_count")
    categories = set(catalog.get("categories") or [])
    title = (catalog.get("title") or "").lower()
    description = (catalog.get("description") or "").lower()
    combined_text = " ".join([title, description, " ".join(categories)])

    is_event = "event log" in combined_text or "eventlogs" in catalog.get("catalog_id", "")
    is_inventory = bool(categories & {"inventory", "posture-assessment", "forensics"}) or any(
        word in combined_text for word in ("inventory", "monitoring", "search", "status", "configuration")
    )
    is_detection = bool(categories & {"threat-hunting", "malware", "vulnerability"}) or any(
        word in combined_text
        for word in (
            "malicious",
            "suspicious",
            "vulnerab",
            "exploit",
            "persistence",
            "backdoor",
            "masquerade",
            "credential",
            "disabled",
        )
    )

    if status not in {"completed", "completed_direct_verification"}:
        return (
            "Do not make endpoint assumptions from this validation record. "
            "The catalog entry needs rerun or direct result follow-up before interpretation."
        )
    if caveat:
        return (
            "Endpoint answered, but one or more query blocks produced errors. "
            "Read label_errors/endpoint_errors before interpreting row counts."
        )
    if row_count == 0:
        if is_event:
            return (
                "Endpoint answered with no matching event rows in the available log scope. "
                "This is a no-hit for the exact event condition, not proof the behavior never happened."
            )
        if is_detection:
            return (
                "Endpoint answered with no matching rows. For this catalog check, treat it as no evidence "
                "for the exact suspicious/vulnerable condition in the queried data scope."
            )
        if is_inventory:
            return (
                "Endpoint answered with no rows. Treat as no matching inventory/configuration/artifact data "
                "for this query shape on the tested endpoint."
            )
        return (
            "Endpoint answered with no rows. The query ran, but no matching data was returned for the tested "
            "endpoint and query scope."
        )
    if row_count and row_count > 1000:
        return (
            "Endpoint answered with a very large result set. Treat this as broad inventory/forensic output; "
            "narrow targets, parameters, paths, time windows, or labels before broad production use."
        )
    if is_detection:
        return (
            "Endpoint answered with rows. Review each row as potential evidence for the catalog condition, "
            "then validate against context, timestamps, paths, users, signatures, and related follow-up queries."
        )
    if is_event:
        return (
            "Endpoint answered with event rows. Interpret as matching events present in the available log scope; "
            "validate timing, event semantics, and surrounding activity."
        )
    return (
        "Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, "
        "posture, configuration, or forensic context rather than malicious evidence by itself."
    )


def assumptions_and_limits(
    catalog: dict[str, Any],
    status: str | None,
    result_summary: dict[str, Any],
    caveat: str | None,
) -> list[str]:
    output: list[str] = []
    if status in {"completed", "completed_direct_verification"}:
        output.append("Validation used one explicit Windows endpoint; do not generalize row counts to other endpoints or fleets.")
        output.append("Row counts describe this validation run only; they are useful for expected result shape and interpretation, not baseline truth.")
        if result_summary.get("row_count", 0) == 0:
            output.append("Zero rows means no matching rows returned after the endpoint answered; it is not the same as query failure.")
        if catalog.get("warnings"):
            output.append("Read catalog warnings before interpreting empty or positive results.")
        if caveat:
            output.append("Query or endpoint errors limit interpretation until the failing label is fixed or verified separately.")
    else:
        output.append("No reliable endpoint conclusion should be drawn from this validation entry.")
        output.append("Rerun or check an existing job result before using the catalog entry operationally.")
    return output


def iter_jsonl_records(input_path: Path) -> list[dict[str, Any]]:
    if not input_path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line in input_path.read_text().splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def load_catalog_snapshot(input_path: Path = CATALOG_SNAPSHOT_INPUT) -> dict[str, Any]:
    if not input_path.exists():
        return {"queries_by_id": {}, "tactics": {}, "techniques": {}, "subtechniques": {}}

    data = json.loads(input_path.read_text())
    queries = data.get("queries", []) if isinstance(data, dict) else []

    def definition_map(values: Any) -> dict[str, str]:
        output: dict[str, str] = {}
        if not isinstance(values, list):
            return output
        for item in values:
            if not isinstance(item, dict):
                continue
            mitre_id = item.get("mitreid") or item.get("id")
            title = item.get("title")
            if mitre_id and title:
                output[str(mitre_id)] = str(title)
        return output

    return {
        "queries_by_id": {item.get("id"): item for item in queries if isinstance(item, dict) and item.get("id")},
        "tactics": definition_map(data.get("tactics")) if isinstance(data, dict) else {},
        "techniques": definition_map(data.get("techniques")) if isinstance(data, dict) else {},
        "subtechniques": definition_map(data.get("subtechniques")) if isinstance(data, dict) else {},
    }


def map_from_ids(ids: Any, definitions: dict[str, str]) -> dict[str, str]:
    if not ids:
        return {}
    return {str(item): definitions.get(str(item), "") for item in ids}


def mitre_maps(catalog: dict[str, Any], snapshot_item: dict[str, Any], snapshot: dict[str, Any]) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    tactics = catalog.get("tactics") or snapshot_item.get("tactics") or map_from_ids(
        catalog.get("tactics_mitre_ids") or snapshot_item.get("tactics_mitre_ids"),
        snapshot["tactics"],
    )

    raw_techniques = catalog.get("techniques") or snapshot_item.get("techniques") or {}
    if not raw_techniques:
        raw_techniques = map_from_ids(
            catalog.get("techniques_mitre_ids") or snapshot_item.get("techniques_mitre_ids"),
            snapshot["techniques"] | snapshot["subtechniques"],
        )

    explicit_subtechniques = map_from_ids(
        catalog.get("subtechnique_mitre_ids") or snapshot_item.get("subtechnique_mitre_ids"),
        snapshot["subtechniques"],
    )

    techniques: dict[str, str] = {}
    subtechniques: dict[str, str] = dict(explicit_subtechniques)
    for mitre_id, title in raw_techniques.items():
        target = subtechniques if "." in str(mitre_id) else techniques
        target[str(mitre_id)] = str(title)

    return dict(tactics), techniques, subtechniques


def load_best_records(input_path: Path) -> list[dict[str, Any]]:
    best_by_catalog_id: dict[str, dict[str, Any]] = {}
    records = iter_jsonl_records(input_path) + iter_jsonl_records(PROFILE_UPDATES_INPUT)
    for record in records:
        catalog_id = record.get("catalog", {}).get("catalog_id")
        if not catalog_id:
            continue
        current = best_by_catalog_id.get(catalog_id)
        if current is None or STATUS_PRIORITY.get(record.get("status"), 0) >= STATUS_PRIORITY.get(current.get("status"), 0):
            best_by_catalog_id[catalog_id] = record

    # The runner had one result-fetch error for this entry. The durable project
    # context documents that direct follow-up verification returned 0 rows.
    catalog_id = "registry_safe_dll_search_monitoring"
    if catalog_id in best_by_catalog_id and best_by_catalog_id[catalog_id].get("status") != "completed":
        record = dict(best_by_catalog_id[catalog_id])
        record["status"] = "completed_direct_verification"
        record["result_summary"] = {
            "answered_endpoint_count": 1,
            "endpoint_errors": [],
            "label_columns": {},
            "label_errors": {},
            "label_row_counts": {},
            "labels_returned": [],
            "meta_present": True,
            "row_count": 0,
        }
        record["notes"] = (
            "Direct follow-up verification documented in "
            "project-context/Orbital_Windows_Catalog_Result_Reading.md returned successfully with 0 rows."
        )
        best_by_catalog_id[catalog_id] = record

    return sorted(
        best_by_catalog_id.values(),
        key=lambda item: item.get("catalog", {}).get("sequence", 999999),
    )


def build_profiles(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    snapshot = load_catalog_snapshot()
    queries_by_id = snapshot["queries_by_id"]
    profiles: list[dict[str, Any]] = []
    for record in records:
        catalog = record.get("catalog", {})
        snapshot_item = queries_by_id.get(catalog.get("catalog_id"), {})
        result_summary = record.get("result_summary") or {}
        status = record.get("status")
        caveat = error_class(record)
        row_count = result_summary.get("row_count")
        tactics, techniques, subtechniques = mitre_maps(catalog, snapshot_item, snapshot)
        sample_result_data, sample_status, sample_omitted_rows = sanitize_sample_result_data(
            result_summary.get("sample_result_data")
        )
        validate_sanitized_sample_data(sample_result_data)

        profiles.append(
            {
                "catalog_id": catalog.get("catalog_id"),
                "title": catalog.get("title"),
                "platforms": catalog.get("os") or [],
                "categories": catalog.get("categories") or [],
                "labels": catalog.get("labels") or [],
                "osquery_count": catalog.get("osquery_count"),
                "parameters": catalog.get("parameters") or [],
                "warnings": catalog.get("warnings") or [],
                "mitre_tactics": tactics,
                "mitre_techniques": techniques,
                "mitre_subtechniques": subtechniques,
                "catalog_updated": catalog.get("updated"),
                "validation": {
                    "source": "sanitized_from_local_windows_catalog_validation",
                    "source_run_date": record.get("profile_source_run_date") or "2026-06-15/2026-06-16",
                    "target_scope": "one explicit Windows endpoint",
                    "status": status,
                    "endpoint_answered": bool(result_summary.get("answered_endpoint_count"))
                    if "answered_endpoint_count" in result_summary
                    else None,
                    "answered_endpoint_count": result_summary.get("answered_endpoint_count"),
                    "row_count": row_count,
                    "row_count_bucket": row_bucket(row_count),
                    "labels_returned": result_summary.get("labels_returned") or [],
                    "label_row_counts": result_summary.get("label_row_counts") or {},
                    "label_columns": result_summary.get("label_columns") or {},
                    "label_errors": sanitize_label_errors(result_summary.get("label_errors")),
                    "endpoint_errors": sanitize_endpoint_errors(result_summary.get("endpoint_errors")),
                    "error_class": caveat,
                    "sample_result_data": sample_result_data,
                    "sample_result_data_status": sample_status,
                    "sample_result_data_row_count": sum(len(rows) for rows in sample_result_data.values()),
                    "sample_result_data_omitted_row_count": sample_omitted_rows,
                },
                "responder_reading": responder_reading(catalog, status, result_summary, caveat),
                "assumptions_and_limits": assumptions_and_limits(catalog, status, result_summary, caveat),
            }
        )
    return profiles


def write_jsonl(profiles: list[dict[str, Any]], path: Path) -> None:
    jsonl_profiles: list[dict[str, Any]] = []
    for profile in profiles:
        validation = dict(profile["validation"])
        validation.pop("sample_result_data", None)
        jsonl_profiles.append({**profile, "validation": validation})
    path.write_text("\n".join(json.dumps(profile, sort_keys=True) for profile in jsonl_profiles) + "\n")


def escape_cell(value: Any) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def slugify(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "untitled"


def bullet_lines(values: list[Any]) -> list[str]:
    if not values:
        return ["- None recorded."]
    return [f"- `{value}`" for value in values if value is not None]


def plain_bullet_lines(values: list[Any]) -> list[str]:
    if not values:
        return ["- None recorded."]
    return [f"- {value}" for value in values if value is not None]


def format_map(mapping: dict[str, Any]) -> list[str]:
    if not mapping:
        return ["- None recorded."]
    return [f"- `{key}`: {value}" for key, value in sorted(mapping.items())]


def markdown_table_for_label_columns(label_columns: dict[str, list[str]]) -> list[str]:
    lines = ["| Label | Columns |", "| --- | --- |"]
    if not label_columns:
        lines.append("| None returned in validation | None observed |")
        return lines
    for label, columns in sorted(label_columns.items()):
        column_text = ", ".join(f"`{column}`" for column in columns) if columns else "None observed"
        lines.append(f"| `{escape_cell(label)}` | {column_text} |")
    return lines


def result_observation_text(profile: dict[str, Any]) -> str:
    validation = profile["validation"]
    status = validation["status"]
    row_count = validation["row_count"]
    endpoint_answered = validation["endpoint_answered"]
    caveat = validation["error_class"]

    if status not in {"completed", "completed_direct_verification"}:
        return (
            "The validation did not produce a reliable completed endpoint result. Treat this as no usable "
            "result profile for endpoint assumptions until the query is rerun or an existing job result is "
            "checked directly."
        )
    if caveat:
        return (
            "The endpoint answered, but the validation recorded a caveat. Interpret row counts only after "
            "reviewing the error details in the profile."
        )
    if endpoint_answered and row_count == 0:
        return (
            "The endpoint answered and returned zero rows. This is a completed no-hit result for the exact "
            "query scope, not a query failure."
        )
    if endpoint_answered:
        return f"The endpoint answered and returned {row_count} rows in the validation run."
    return "Endpoint-answer state was not available in the sanitized validation profile."


def zero_row_reading(profile: dict[str, Any]) -> str:
    validation = profile["validation"]
    if validation["status"] not in {"completed", "completed_direct_verification"}:
        return (
            "No endpoint-response assumption is valid for this profile. If an execution has no response, "
            "first confirm target availability, query status, and stored job results before interpreting "
            "the catalog condition."
        )
    if validation["endpoint_answered"] and validation["row_count"] == 0:
        return profile["responder_reading"]
    return (
        "If a future execution returns zero rows after the endpoint answered, read it as no matching rows "
        "for the exact query scope. Do not treat zero rows as proof that the related behavior never happened."
    )


def returned_row_reading(profile: dict[str, Any]) -> str:
    validation = profile["validation"]
    if validation["status"] not in {"completed", "completed_direct_verification"}:
        return (
            "No returned-row interpretation was validated. If a future execution returns rows, interpret them "
            "against the catalog description, returned columns, warnings, and follow-up evidence."
        )
    if validation["row_count"] and validation["row_count"] > 0:
        return profile["responder_reading"]
    return (
        "If a future execution returns rows, treat them as evidence matching this catalog query's condition "
        "or inventory shape. Review timestamps, paths, users, signatures, process context, and related "
        "follow-up queries before making an incident conclusion."
    )


def no_response_reading(profile: dict[str, Any]) -> str:
    validation = profile["validation"]
    if validation["status"] not in {"completed", "completed_direct_verification"} or not validation["endpoint_answered"]:
        return (
            "No response means the query did not produce endpoint evidence in the observed wait window. "
            "Do not read this as clean or affected. Verify target selection, endpoint online state, query/job "
            "status, result availability, and API errors before rerunning."
        )
    return (
        "If a future execution has no endpoint response, do not interpret it as zero rows. Zero rows require "
        "an answered endpoint. No response requires operational follow-up on target state, job status, and "
        "result retrieval."
    )


def explanation_template(profile: dict[str, Any]) -> str:
    title = profile["title"]
    catalog_id = profile["catalog_id"]
    return (
        f"The `{catalog_id}` catalog query ({title}) returned results that should be interpreted according "
        "to the catalog purpose and observed result shape. An answered endpoint with zero rows means no "
        "matching rows were returned for this exact query scope. Returned rows are endpoint evidence for "
        "the query condition or inventory shape, but they are not automatically a malicious verdict. A "
        "missing endpoint response is operationally different from zero rows and should be checked through "
        "target availability and job/result status."
    )


def markdown_table_from_rows(rows: list[dict[str, Any]]) -> list[str]:
    if not rows:
        return ["No sanitized sample rows recorded for this label."]

    columns: list[str] = []
    for row in rows:
        for column in row:
            if column not in columns:
                columns.append(column)

    lines = [
        "| " + " | ".join(f"`{escape_cell(column)}`" for column in columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_cell(row.get(column, "")) for column in columns) + " |")
    return lines


def sample_result_data_lines(profile: dict[str, Any]) -> list[str]:
    sample_data = profile["validation"].get("sample_result_data") or {}
    sample_status = profile["validation"].get("sample_result_data_status")
    omitted_row_count = profile["validation"].get("sample_result_data_omitted_row_count") or 0
    lines = [
        "## Sample Result Data",
        "",
        "Representative sanitized sample rows, when available. These examples preserve result shape only and are not endpoint evidence.",
        "",
    ]
    if not sample_data:
        if sample_status == "omitted_for_privacy":
            lines.append("Sample result data was omitted because it could not be represented safely.")
        else:
            lines.append("No sanitized sample result data was recorded for this profile.")
        return lines

    for label, rows in sorted(sample_data.items()):
        lines.extend(
            [
                f"Label: `{escape_cell(label)}`",
                "",
                *markdown_table_from_rows(rows if isinstance(rows, list) else []),
                "",
            ]
        )
    if omitted_row_count:
        lines.append("Additional source rows were omitted to preserve privacy and the 15-row limit.")
    return lines


def write_per_catalog_markdown(profiles: list[dict[str, Any]], output_dir: Path) -> None:
    windows_dir = output_dir / "windows"
    windows_dir.mkdir(parents=True, exist_ok=True)
    for old_file in windows_dir.glob("*.md"):
        old_file.unlink()

    for profile in profiles:
        validation = profile["validation"]
        filename = f"{slugify(profile['catalog_id'])}__{slugify(profile['title'])}.md"
        path = windows_dir / filename
        lines = [
            f"# {profile['title']}",
            "",
            "## Catalog Identity",
            "",
            f"- Catalog ID: `{profile['catalog_id']}`",
            f"- Catalog name: `{profile['title']}`",
            f"- Platform: {', '.join(profile['platforms']) if profile['platforms'] else 'Not recorded'}",
            "- Profile type: sanitized catalog result profile",
            f"- Source run: {validation['source_run_date']}",
            f"- Catalog updated: {profile['catalog_updated'] or 'Not recorded'}",
            "",
            "## What This Query Answers",
            "",
            "Use the catalog name, categories, MITRE mapping, and returned columns to decide whether this query is detection-oriented, inventory-oriented, posture-oriented, or forensic context.",
            "",
            "Categories:",
            *bullet_lines(profile["categories"]),
            "",
            "MITRE tactics:",
            *format_map(profile["mitre_tactics"]),
            "",
            "MITRE techniques:",
            *format_map(profile["mitre_techniques"]),
            "",
            "MITRE subtechniques:",
            *format_map(profile["mitre_subtechniques"]),
            "",
            "This profile does not prove maliciousness by itself. It explains how to read this catalog query's result shape and caveats.",
            "",
            "## Expected Result Shape",
            "",
            f"- Endpoint answered in validation: {'yes' if validation['endpoint_answered'] else 'no' if validation['endpoint_answered'] is False else 'unknown'}",
            f"- Validation status: `{validation['status']}`",
            f"- Observed row count: {validation['row_count'] if validation['row_count'] is not None else 'unknown'}",
            f"- Row-count bucket: `{validation['row_count_bucket']}`",
            "- Returned labels:",
            *bullet_lines(validation["labels_returned"]),
            "",
            "Observed columns:",
            "",
            *markdown_table_for_label_columns(validation["label_columns"]),
            "",
            "Label row counts:",
            *format_map(validation["label_row_counts"]),
            "",
            "## How To Read The Result",
            "",
            "Observed validation result:",
            "",
            result_observation_text(profile),
            "",
            "If rows are returned:",
            "",
            returned_row_reading(profile),
            "",
            "If zero rows are returned:",
            "",
            zero_row_reading(profile),
            "",
            "If the endpoint does not respond:",
            "",
            no_response_reading(profile),
            "",
            "## Incident Responder Assumptions",
            "",
            "Safe assumptions and limits:",
            *plain_bullet_lines(profile["assumptions_and_limits"]),
            "",
            "Unsafe assumptions:",
            "- Do not assume returned rows are malicious without context.",
            "- Do not assume missing rows prove the behavior never happened.",
            "- Do not generalize this validation row count to all endpoints.",
            "- Do not treat no endpoint response as a clean result.",
            "",
            "## Caveats",
            "",
            "Catalog warnings:",
            *plain_bullet_lines(profile["warnings"]),
            "",
            f"Error class: `{validation['error_class'] or 'none'}`",
            "",
            "Label errors:",
            *format_map(validation["label_errors"]),
            "",
            "Endpoint errors:",
            *plain_bullet_lines(validation["endpoint_errors"]),
            "",
            "## Recommended Follow-Up",
            "",
            "When the result matters for an investigation:",
            "",
            "1. Confirm the endpoint answered before interpreting row counts.",
            "2. Compare returned rows with the catalog purpose and warnings.",
            "3. Validate suspicious rows with surrounding context such as time, path, user, process, signature, network, persistence, or related event evidence.",
            "4. Use narrower targets or parameters before broad execution if the profile shows high-volume output.",
            "5. If no endpoint response occurred, check target selection and stored job/result status before rerunning.",
            "",
            "## Explanation Template",
            "",
            explanation_template(profile),
            "",
            "## Privacy Boundary",
            "",
            "This profile intentionally does not store raw endpoint evidence:",
            "",
            "- Raw endpoint result rows",
            "- Hostnames",
            "- Target selectors",
            "- Job IDs",
            "- Usernames",
            "- IP addresses",
            "- GUIDs",
            "- Tenant data",
            "- Raw API responses",
            "- Credentials",
            "",
            *sample_result_data_lines(profile),
        ]
        path.write_text("\n".join(lines))


def write_markdown(profiles: list[dict[str, Any]], path: Path) -> None:
    status_counts = Counter(profile["validation"]["status"] for profile in profiles)
    bucket_counts = Counter(profile["validation"]["row_count_bucket"] for profile in profiles)
    caveat_profiles = [profile for profile in profiles if profile["validation"]["error_class"]]
    high_volume_profiles = [
        profile
        for profile in profiles
        if profile["validation"]["row_count_bucket"] in {"high_101_1000", "very_high_over_1000"}
    ]

    lines = [
        "# Windows Stock Catalog Result Profiles",
        "",
        "Generated from a sanitized local Windows catalog validation run from 2026-06-15/2026-06-16.",
        "",
        "This file is GitHub-safe project context. It does not include endpoint result rows, hostnames, target selectors, Job IDs, raw API responses, tenant data, credentials, or customer-identifying values.",
        "",
        "## Summary",
        "",
        f"- Catalog entries profiled: {len(profiles)}",
        f"- Completed in runner: {status_counts.get('completed', 0)}",
        f"- Completed by documented direct verification: {status_counts.get('completed_direct_verification', 0)}",
        f"- Entries with query/API/endpoint caveat classes: {len(caveat_profiles)}",
        f"- High or very high row-count profiles: {len(high_volume_profiles)}",
        "",
        "## Row Count Buckets",
        "",
    ]

    for bucket in ("zero", "low_1_10", "medium_11_100", "high_101_1000", "very_high_over_1000", "unknown"):
        if bucket_counts.get(bucket):
            lines.append(f"- `{bucket}`: {bucket_counts[bucket]}")

    lines.extend(
        [
            "",
            "## How To Use",
            "",
            "- Use this as interpretation context before explaining Orbital catalog results to an incident responder.",
            "- Match by Catalog `ID` first, then by `title` if needed.",
            "- Treat row counts as validation-run shape information, not as customer or fleet baseline data.",
            "- For zero-row detection-oriented checks, explain this as no returned evidence for the exact catalog condition after the endpoint answered.",
            "- For event-log checks, explain that empty results depend on available logs and retention.",
            "- For high-volume profiles, narrow query parameters or target scope before broad use.",
            "- For entries with `error_class`, resolve the caveat before relying on the result profile operationally.",
            "",
            "## Profile Table",
            "",
            "| Catalog ID | Title | Status | Rows | Bucket | Error class | Analyst reading |",
            "| --- | --- | --- | ---: | --- | --- | --- |",
        ]
    )

    for profile in profiles:
        validation = profile["validation"]
        row_count = validation["row_count"] if validation["row_count"] is not None else ""
        lines.append(
            f"| `{escape_cell(profile['catalog_id'])}` | {escape_cell(profile['title'])} | "
            f"`{escape_cell(validation['status'])}` | {row_count} | "
            f"`{escape_cell(validation['row_count_bucket'])}` | "
            f"`{escape_cell(validation['error_class'])}` | {escape_cell(profile['responder_reading'])} |"
        )

    path.write_text("\n".join(lines) + "\n")


def write_readme(path: Path) -> None:
    path.write_text(
        """# Catalog Result Profiles

This folder contains GitHub-synced, sanitized result-profile artifacts for Orbital catalog validation runs.

These files are designed to help an incident responder understand what an Orbital catalog query result means: expected result shape, row-count behavior, common caveats, safe assumptions, and sanitized sample shape where it is useful.

Included files:

- `windows_stock_catalog_result_profiles.jsonl`: structured per-Catalog-ID profiles for Windows stock catalog queries. It contains no sample-row values.
- `windows_stock_catalog_result_profiles.md`: human-readable summary and table. It contains no sample-row values.
- `windows/`: one analyst-facing Markdown file per Windows stock catalog query, named `<catalog_id>__<normalized_query_name>.md`.

Privacy boundary:

- Store interpretation profiles, row counts, returned column names, catalog metadata, sanitized caveats, and no more than 15 structural sample rows in each per-Catalog-ID Markdown file.
- Do not store raw endpoint result rows, hostnames, target selectors, Job IDs, raw API responses, tenant data, credentials, IP addresses, GUIDs, usernames, customer-identifying values, or sample-row values in the JSONL or summary Markdown files.

Raw operational validation files stay local-only under `local/orbital_catalog_windows_validation/`.
"""
    )


def validate_generated_artifacts(output_dir: Path) -> None:
    jsonl_path = output_dir / "windows_stock_catalog_result_profiles.jsonl"
    for line in jsonl_path.read_text().splitlines():
        if not line.strip():
            continue
        validation = json.loads(line).get("validation") or {}
        if "sample_result_data" in validation:
            raise ValueError("JSONL must not contain sample result row values")

    for path in (output_dir / "windows").glob("*.md"):
        content = path.read_text()
        if content.count("## Sample Result Data") != 1:
            raise ValueError(f"{path.name} must contain exactly one Sample Result Data section")
        sample_section = content.split("## Sample Result Data", 1)[1]
        if "\n## " in sample_section:
            raise ValueError(f"{path.name} must end with Sample Result Data")

        sample_row_count = 0
        for line in sample_section.splitlines():
            if not line.startswith("|") or "---" in line or "`" in line:
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if not all(SAFE_SAMPLE_VALUE_RE.fullmatch(cell) for cell in cells):
                raise ValueError(f"{path.name} contains a non-sanitized sample value")
            sample_row_count += 1
        if sample_row_count > MAX_SAMPLE_ROWS_PER_PROFILE:
            raise ValueError(f"{path.name} exceeds the {MAX_SAMPLE_ROWS_PER_PROFILE}-row sample limit")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate-only", action="store_true", help="Validate existing generated profile artifacts.")
    args = parser.parse_args()

    if args.validate_only:
        validate_generated_artifacts(OUTPUT_DIR)
        print(f"Validated catalog result profiles in {OUTPUT_DIR}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    profiles = build_profiles(load_best_records(DEFAULT_INPUT))
    write_jsonl(profiles, OUTPUT_DIR / "windows_stock_catalog_result_profiles.jsonl")
    write_markdown(profiles, OUTPUT_DIR / "windows_stock_catalog_result_profiles.md")
    write_per_catalog_markdown(profiles, OUTPUT_DIR)
    write_readme(OUTPUT_DIR / "README.md")
    validate_generated_artifacts(OUTPUT_DIR)
    print(f"Generated {len(profiles)} catalog result profiles in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
