#!/usr/bin/env python3
"""Preview, create, update, or delete Cisco Orbital organization catalog queries.

This helper saves reusable query definitions in the Orbital organization
catalog. It does not execute endpoint queries.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[4]
LEDGER = ROOT / "local" / "orbital_catalog_updates" / "catalog_update_runs.jsonl"

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

REDACT_KEYS = {"authorization", "token", "access_token", "refresh_token", "jwt"}
CATALOG_SIZE_LIMIT = 65536


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview or create an Orbital organization catalog query."
    )
    parser.add_argument("--input-json", default="", help="Catalog query JSON body.")
    parser.add_argument(
        "--env-file",
        default=os.environ.get("ORBITAL_ENV_FILE", ""),
        help="Explicit credential env file. Defaults to the source_env_file from Codex ORG Mapping state.",
    )
    parser.add_argument(
        "--org-mapping-state-file",
        default=os.environ.get(
            "ORBITAL_ORG_MAPPING_STATE_FILE",
            str(
                Path.home()
                / ".codex"
                / "state"
                / "cisco-security-api-access"
                / "current_org_mapping.json"
            ),
        ),
        help="Codex ORG Mapping state JSON used to find the default credential env file.",
    )
    parser.add_argument("--region", default="")
    parser.add_argument("--timeout", type=int, default=30)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--preview", action="store_true", help="Validate and print body only.")
    mode.add_argument("--create", action="store_true", help="POST the body to /catalogs.")
    mode.add_argument(
        "--delete-catalog-id",
        action="append",
        default=[],
        help="Disable/remove an organization catalog query by catalog ID. Can be supplied more than once.",
    )
    mode.add_argument(
        "--rename-catalog-id",
        default="",
        help="Rename an organization catalog query by catalog ID while preserving the existing query body.",
    )
    parser.add_argument("--new-title", default="", help="New title for --rename-catalog-id.")
    parser.add_argument(
        "--describe-before-delete",
        action="store_true",
        help="Fetch /catalogs before deletion to include title/context in output. Slower; not needed when the ID is known.",
    )
    parser.add_argument(
        "--no-verify-delete",
        action="store_true",
        help="Skip post-delete /catalogs verification. Fastest path, but only confirms the DELETE response.",
    )
    parser.add_argument(
        "--allow-duplicate-title",
        action="store_true",
        help="Allow creating a new catalog entry even if the title already exists.",
    )
    parser.add_argument(
        "--skip-duplicate-check",
        action="store_true",
        help="Skip GET /catalogs duplicate-title check.",
    )
    parser.add_argument(
        "--check-duplicate-title",
        action="store_true",
        help="For rename mode, scan /catalogs for duplicate titles before updating. Slower; skipped by default for known-ID fast path.",
    )
    parser.add_argument(
        "--use-config-wrapper",
        action="store_true",
        help="POST title plus config.description/config.osquery instead of top-level description/osquery.",
    )
    parser.add_argument(
        "--allow-non-codex-title",
        action="store_true",
        help="Allow creating a catalog query whose title does not start with 'codex'.",
    )
    return parser.parse_args()


def load_codex_org_mapping(path: str) -> dict[str, Any]:
    mapping_path = Path(path).expanduser()
    if not mapping_path.exists():
        return {}
    loaded = json.loads(mapping_path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise RuntimeError(f"ORG Mapping state file must contain a JSON object: {path}")
    mapping = loaded.get("mapping") if isinstance(loaded.get("mapping"), dict) else loaded
    return mapping if isinstance(mapping, dict) else {}


def resolve_env_file(args: argparse.Namespace, mapping: dict[str, Any]) -> tuple[str, str]:
    if args.env_file:
        return str(Path(args.env_file).expanduser()), "explicit_env_file"
    source_env_file = str(mapping.get("source_env_file") or "").strip()
    if source_env_file:
        return str(Path(source_env_file).expanduser()), "codex_org_mapping_source_env_file"
    legacy_env = ROOT / "tools-and-memory" / "orbital_credentials.env"
    if legacy_env.exists():
        return str(legacy_env), "legacy_project_orbital_env_file"
    return "", "environment_only"


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


def first_env(names: list[str]) -> str:
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value.removeprefix("Bearer ").strip()
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

    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode(
        "ascii"
    )
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


def call_json(
    region: str, token: str, method: str, path: str, timeout: int, body: Any | None = None
) -> tuple[int, Any]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {
        "authorization": f"Bearer {token}",
        "accept": "application/json",
    }
    if data is not None:
        headers["content-type"] = "application/json"
    request = Request(f"{SERVERS[region]}{path}", data=data, headers=headers, method=method)
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw) if raw else {}
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            payload: Any = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload = {"errors": [raw[:1000]]}
        return exc.code, payload


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[redacted]" if key.lower() in REDACT_KEYS or "token" in key.lower() else redact(child)
            for key, child in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


def load_body(path: str) -> dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("Catalog query body must be a JSON object.")
    return payload


def validate_body(body: dict[str, Any], require_codex_prefix: bool = True) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(body.get("title"), str) or not body["title"].strip():
        errors.append("title is required.")
    elif require_codex_prefix and not body["title"].strip().casefold().startswith("codex"):
        errors.append("Codex-generated catalog query titles must start with 'codex'.")
    if not isinstance(body.get("description"), str) or len(body["description"].strip()) < 20:
        errors.append("description is required and should be meaningful.")
    platform = body.get("platform")
    if not isinstance(platform, list) or not platform or not all(isinstance(x, str) for x in platform):
        errors.append("platform must be a non-empty string array, for example ['windows'].")
    osquery = body.get("osquery")
    if not isinstance(osquery, list) or not osquery:
        errors.append("osquery must be a non-empty array.")
    elif osquery:
        labels: set[str] = set()
        for idx, item in enumerate(osquery):
            if not isinstance(item, dict):
                errors.append(f"osquery[{idx}] must be an object.")
                continue
            label = item.get("label")
            sql = item.get("sql")
            if not isinstance(label, str) or not label.strip():
                errors.append(f"osquery[{idx}].label is required.")
            elif label in labels:
                errors.append(f"duplicate osquery label: {label}")
            else:
                labels.add(label)
            if not isinstance(sql, str) or not sql.strip():
                errors.append(f"osquery[{idx}].sql is required.")
            elif not sql.strip().endswith(";"):
                warnings.append(f"osquery[{idx}].sql does not end with a semicolon.")
    body_size = len(json.dumps(body, separators=(",", ":")).encode("utf-8"))
    if body_size > CATALOG_SIZE_LIMIT:
        errors.append(f"catalog query body is {body_size} bytes; limit is {CATALOG_SIZE_LIMIT}.")
    body["_validation_warnings"] = warnings
    body["_validation_body_size"] = body_size
    return errors


def build_api_body(body: dict[str, Any], use_config_wrapper: bool) -> dict[str, Any]:
    if not use_config_wrapper:
        return body
    api_body: dict[str, Any] = {
        "title": body.get("title"),
        "config": {
            "description": body.get("description"),
            "osquery": body.get("osquery"),
        },
    }
    for optional_key in ("version", "platform"):
        if optional_key in body:
            api_body[optional_key] = body[optional_key]
    return api_body


def iter_catalog_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        if isinstance(data, dict):
            return [data]
        for key in ("queries", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def find_duplicate_titles(payload: Any, title: str) -> list[dict[str, Any]]:
    title_norm = title.strip().casefold()
    matches = []
    for item in iter_catalog_items(payload):
        candidate = str(item.get("title") or item.get("name") or "").strip()
        if candidate.casefold() == title_norm:
            matches.append(
                {
                    "id": item.get("id") or item.get("ID"),
                    "title": candidate,
                    "version": item.get("version"),
                    "platform": item.get("platform") or item.get("os"),
                }
            )
    return matches


def catalog_item_summary(item: dict[str, Any]) -> dict[str, Any]:
    config = item.get("config") if isinstance(item.get("config"), dict) else {}
    return {
        "id": item.get("id") or item.get("ID"),
        "title": item.get("title") or item.get("name"),
        "version": item.get("version"),
        "platform": item.get("platform") or item.get("os"),
        "config_osquery_count": len(config.get("osquery") or []),
    }


def extract_catalog_item(payload: Any) -> dict[str, Any] | None:
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, dict):
            return data
    items = iter_catalog_items(payload)
    return items[0] if len(items) == 1 else None


def find_catalog_item_by_id(payload: Any, catalog_id: str) -> dict[str, Any] | None:
    for item in iter_catalog_items(payload):
        item_id = item.get("id") or item.get("ID")
        if item_id == catalog_id:
            return item
    return None


def catalog_item_to_update_body(item: dict[str, Any], title: str) -> dict[str, Any]:
    config = item.get("config") if isinstance(item.get("config"), dict) else {}
    description = item.get("description") or config.get("description") or ""
    osquery = (
        item.get("osquery")
        or item.get("osQuery")
        or config.get("osquery")
        or config.get("osQuery")
        or []
    )
    if not isinstance(osquery, list) or not osquery:
        raise RuntimeError("Fetched catalog entry does not contain config.osquery/osquery blocks.")
    body: dict[str, Any] = {
        "id": item.get("id") or item.get("ID"),
        "title": title,
        "description": description,
        "osquery": osquery,
    }
    for key in ("platform", "version"):
        value = item.get(key)
        if value is not None:
            body[key] = value
    if "platform" not in body:
        os_value = item.get("os") or config.get("platform") or config.get("os")
        if isinstance(os_value, list):
            body["platform"] = os_value
        elif isinstance(os_value, str) and os_value:
            body["platform"] = [os_value]
    return body


def write_ledger(record: dict[str, Any]) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def response_catalog_summary(payload: Any) -> dict[str, Any]:
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        return {}
    config = data.get("config") if isinstance(data.get("config"), dict) else {}
    return {
        "id": data.get("id") or data.get("ID"),
        "title": data.get("title") or data.get("name"),
        "version": data.get("version"),
        "platform": data.get("platform") or data.get("os"),
        "osquery_count": len(
            data.get("osQuery") or data.get("osquery") or config.get("osquery") or []
        ),
    }


def main() -> int:
    args = parse_args()
    if not args.preview and not args.create and not args.delete_catalog_id and not args.rename_catalog_id:
        args.preview = True

    mapping = load_codex_org_mapping(args.org_mapping_state_file)
    env_file, credential_source = resolve_env_file(args, mapping)
    load_env_file(env_file)
    region = (
        args.region
        or os.environ.get("ORBITAL_REGION")
        or str(mapping.get("region") or "")
        or os.environ.get("SECURE_ENDPOINT_REGION")
        or "eu"
    ).strip().lower()
    if region not in SERVERS:
        raise RuntimeError(f"Unsupported region: {region}")

    if args.rename_catalog_id:
        catalog_id = args.rename_catalog_id.strip()
        new_title = args.new_title.strip()
        output: dict[str, Any] = {
            "mode": "rename",
            "region": region,
            "catalog_id": catalog_id,
            "new_title": new_title,
            "flow": "direct_rename_by_known_id",
        }
        if not catalog_id.startswith("org:"):
            output["error"] = "Only organization catalog query IDs starting with 'org:' are accepted."
            print(json.dumps(output, indent=2, sort_keys=True))
            return 2
        if not new_title:
            output["error"] = "--new-title is required for --rename-catalog-id."
            print(json.dumps(output, indent=2, sort_keys=True))
            return 2
        if not args.allow_non_codex_title and not new_title.casefold().startswith("codex"):
            output["error"] = "Codex-generated catalog query titles must start with 'codex'. Use --allow-non-codex-title only when the user explicitly requested a non-Codex title."
            print(json.dumps(output, indent=2, sort_keys=True))
            return 2

        total_start = time.time()
        token = fetch_access_token(region, args.timeout)
        lookup_start = time.time()
        catalog_status, catalog_payload = call_json(
            region,
            token,
            "GET",
            f"/catalogs/{catalog_id}",
            args.timeout,
        )
        output["catalog_lookup_status"] = catalog_status
        output["catalog_lookup_path"] = f"/catalogs/{catalog_id}"
        output["catalog_lookup_elapsed_ms"] = round((time.time() - lookup_start) * 1000)
        if catalog_status != 200:
            output["error"] = "Could not fetch catalog before rename."
            output["catalog_lookup_error"] = redact(catalog_payload)
            print(json.dumps(output, indent=2, sort_keys=True))
            return 1

        current_item = extract_catalog_item(catalog_payload)
        if current_item and (current_item.get("id") or current_item.get("ID")) != catalog_id:
            current_item = None
        if current_item is None:
            output["error"] = "Catalog ID not found."
            print(json.dumps(output, indent=2, sort_keys=True))
            return 1
        output["before"] = catalog_item_summary(current_item)

        output["duplicate_check"] = "skipped_known_id_fast_path"
        if args.check_duplicate_title:
            duplicate_status, duplicate_payload = call_json(region, token, "GET", "/catalogs", args.timeout)
            output["duplicate_check"] = "performed_full_catalog_scan"
            output["duplicate_check_status"] = duplicate_status
            if duplicate_status != 200:
                output["error"] = "Could not fetch catalog for duplicate-title check."
                output["duplicate_check_error"] = redact(duplicate_payload)
                print(json.dumps(output, indent=2, sort_keys=True))
                return 1
            duplicates = [
                item
                for item in find_duplicate_titles(duplicate_payload, new_title)
                if item.get("id") != catalog_id
            ]
            output["duplicate_matches"] = duplicates
            if duplicates and not args.allow_duplicate_title:
                output["error"] = "Another catalog query with this title already exists; not renaming."
                print(json.dumps(output, indent=2, sort_keys=True))
                return 3

        update_body = catalog_item_to_update_body(current_item, new_title)
        update_body["id"] = catalog_id
        body_size = len(json.dumps(update_body, separators=(",", ":")).encode("utf-8"))
        output["request_body_size"] = body_size
        if body_size > CATALOG_SIZE_LIMIT:
            output["error"] = f"catalog query body is {body_size} bytes; limit is {CATALOG_SIZE_LIMIT}."
            print(json.dumps(output, indent=2, sort_keys=True))
            return 2

        start = time.time()
        status, payload = call_json(
            region,
            token,
            "PUT",
            "/catalogs",
            args.timeout,
            update_body,
        )
        elapsed_ms = round((time.time() - start) * 1000)
        update_errors = redact(payload.get("errors") if isinstance(payload, dict) else None)
        attempts = [
            {
                "method": "PUT",
                "path": "/catalogs",
                "body_shape": "top_level_osquery",
                "status": status,
                "errors": update_errors,
            }
        ]
        output.update(
            {
                "update_attempts": attempts,
                "update_method": "PUT",
                "update_body_shape": "top_level_osquery",
                "status": status,
                "update_elapsed_ms": elapsed_ms,
                "response_summary": response_catalog_summary(payload),
                "errors": update_errors,
            }
        )

        verify_start = time.time()
        verify_status, verify_payload = call_json(
            region,
            token,
            "GET",
            f"/catalogs/{catalog_id}",
            args.timeout,
        )
        verify_item = extract_catalog_item(verify_payload) if verify_status == 200 else None
        if verify_item and (verify_item.get("id") or verify_item.get("ID")) != catalog_id:
            verify_item = None
        output["verify_status"] = verify_status
        output["verify_path"] = f"/catalogs/{catalog_id}"
        output["verify_elapsed_ms"] = round((time.time() - verify_start) * 1000)
        output["after"] = catalog_item_summary(verify_item) if verify_item else None
        output["verified_title"] = bool(verify_item and catalog_item_summary(verify_item)["title"] == new_title)
        output["total_elapsed_ms"] = round((time.time() - total_start) * 1000)
        write_ledger(
            {
                "recorded_at": utc_now(),
                "operation": "rename_catalog_query",
                "region": region,
                "catalog_id": catalog_id,
                "new_title": new_title,
                "status": status,
                "errors": output["errors"],
                "verified_title": output["verified_title"],
                "flow": output["flow"],
                "total_elapsed_ms": output["total_elapsed_ms"],
            }
        )
        print(json.dumps(output, indent=2, sort_keys=True))
        return 0 if status == 200 and not output["errors"] and output["verified_title"] else 1

    if args.delete_catalog_id:
        token = fetch_access_token(region, args.timeout)
        output = {
            "mode": "delete",
            "region": region,
            "flow": "direct_delete_by_known_id",
            "deleted": [],
            "failed": [],
        }
        for catalog_id in args.delete_catalog_id:
            catalog_id = catalog_id.strip()
            if not catalog_id.startswith("org:"):
                output["failed"].append(
                    {
                        "catalog_id": catalog_id,
                        "error": "Only organization catalog query IDs starting with 'org:' are accepted.",
                    }
                )
                continue
            before_item = None
            if args.describe_before_delete:
                before_status, before_payload = call_json(region, token, "GET", "/catalogs", args.timeout)
                before_item = (
                    find_catalog_item_by_id(before_payload, catalog_id)
                    if before_status == 200
                    else None
                )
            delete_status, delete_payload = call_json(
                region,
                token,
                "DELETE",
                f"/catalogs/{catalog_id}",
                args.timeout,
            )
            verified_absent_after_delete: bool | None = None
            if not args.no_verify_delete:
                after_status, after_payload = call_json(region, token, "GET", "/catalogs", args.timeout)
                after_item = find_catalog_item_by_id(after_payload, catalog_id) if after_status == 200 else None
                verified_absent_after_delete = after_status == 200 and after_item is None
            record = {
                "catalog_id": catalog_id,
                "before": catalog_item_summary(before_item) if before_item else None,
                "delete_status": delete_status,
                "delete_errors": redact(delete_payload.get("errors") if isinstance(delete_payload, dict) else None),
                "verified_absent_after_delete": verified_absent_after_delete,
            }
            write_ledger(
                {
                    "recorded_at": utc_now(),
                    "operation": "delete_catalog_query",
                    "region": region,
                    **record,
                }
            )
            if (
                delete_status == 200
                and not record["delete_errors"]
                and record["verified_absent_after_delete"] is not False
            ):
                output["deleted"].append(record)
            else:
                output["failed"].append(record)
        print(json.dumps(output, indent=2, sort_keys=True))
        return 0 if not output["failed"] else 1

    if not args.input_json:
        raise RuntimeError("--input-json is required for preview/create mode.")
    body = load_body(args.input_json)
    validation_errors = validate_body(body, require_codex_prefix=not args.allow_non_codex_title)
    validation = {
        "body_size": body.pop("_validation_body_size"),
        "warnings": body.pop("_validation_warnings"),
        "errors": validation_errors,
    }

    output: dict[str, Any] = {
        "mode": "create" if args.create else "preview",
        "region": region,
        "input_json": args.input_json,
        "title": body.get("title"),
        "platform": body.get("platform"),
        "osquery_count": len(body.get("osquery") or []),
        "api_shape": "config_wrapper" if args.use_config_wrapper else "top_level_osquery",
        "validation": validation,
    }
    if args.preview:
        output["request_body"] = build_api_body(body, args.use_config_wrapper)
        print(json.dumps(output, indent=2, sort_keys=True))
        return 0 if not validation_errors else 2

    if validation_errors:
        output["error"] = "Validation failed; catalog entry was not created."
        print(json.dumps(output, indent=2, sort_keys=True))
        return 2

    token = fetch_access_token(region, args.timeout)
    duplicates: list[dict[str, Any]] = []
    if not args.skip_duplicate_check:
        catalog_status, catalog_payload = call_json(region, token, "GET", "/catalogs", args.timeout)
        output["duplicate_check_status"] = catalog_status
        if catalog_status == 200:
            duplicates = find_duplicate_titles(catalog_payload, str(body.get("title") or ""))
            output["duplicate_matches"] = duplicates
        else:
            output["duplicate_check_error"] = redact(catalog_payload)
    if duplicates and not args.allow_duplicate_title:
        output["error"] = "A catalog query with this title already exists; not creating duplicate."
        write_ledger(
            {
                "recorded_at": utc_now(),
                "operation": "create_catalog_query",
                "status": "duplicate_title",
                "title": body.get("title"),
                "region": region,
                "duplicates": duplicates,
            }
        )
        print(json.dumps(output, indent=2, sort_keys=True))
        return 3

    start = time.time()
    api_body = build_api_body(body, args.use_config_wrapper)
    status, payload = call_json(region, token, "POST", "/catalogs", args.timeout, api_body)
    elapsed_ms = round((time.time() - start) * 1000)
    output.update(
        {
            "status": status,
            "elapsed_ms": elapsed_ms,
            "response_summary": response_catalog_summary(payload),
            "errors": redact(payload.get("errors") if isinstance(payload, dict) else None),
        }
    )
    write_ledger(
        {
            "recorded_at": utc_now(),
            "operation": "create_catalog_query",
            "status": status,
            "title": body.get("title"),
            "region": region,
            "response_summary": output["response_summary"],
            "errors": output["errors"],
        }
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if status == 200 and not output["errors"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, URLError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        raise SystemExit(1)
