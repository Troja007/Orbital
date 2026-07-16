#!/usr/bin/env python3
"""Fetch Orbital catalog data and import it into project context.

The script is intentionally read-only against the Orbital API. It never writes
tokens to disk; provide a token through an environment variable or paste it at
the prompt when running interactively.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "local" / "orbital-catalog-api-cache"
SNAPSHOT_DIR = ROOT / "queries_and_scripts" / "catalog_snapshot"
CONTEXT_FILE = ROOT / "project-context" / "Orbital_Catalog_API_Import.md"

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

ENDPOINTS = {
    "stock_query_catalog": "/stock",
    "organization_catalog_queries": "/catalogs",
    "organization_catalog_scripts": "/catalogs/scripts",
    "stock_catalog_scripts": "/catalogs/cisco/scripts",
}

GITHUB_SYNCED_STOCK_FILES = {"stock_query_catalog", "stock_catalog_scripts"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch Orbital catalog API data and write project context."
    )
    parser.add_argument(
        "--region",
        choices=sorted(SERVERS),
        default="",
        help="Orbital API region. Defaults to ORBITAL_REGION, Codex ORG Mapping region, SECURE_ENDPOINT_REGION, or eu.",
    )
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
    parser.add_argument(
        "--token-env",
        default="",
        help="Environment variable that contains the bearer token.",
    )
    parser.add_argument(
        "--token-op-ref",
        default="",
        help="1Password secret reference that contains an existing bearer token.",
    )
    parser.add_argument(
        "--client-id-env",
        default="",
        help="Environment variable that contains the OAuth client ID.",
    )
    parser.add_argument(
        "--client-secret-env",
        default="",
        help="Environment variable that contains the OAuth client secret.",
    )
    parser.add_argument(
        "--client-id-op-ref",
        default="",
        help="1Password secret reference that contains the OAuth client ID.",
    )
    parser.add_argument(
        "--client-secret-op-ref",
        default="",
        help="1Password secret reference that contains the OAuth client secret.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="HTTP timeout in seconds.",
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


def resolve_env_file(args: argparse.Namespace, mapping: dict[str, Any]) -> tuple[str, str]:
    if args.env_file:
        return str(Path(args.env_file).expanduser()), "explicit_env_file"
    source_env_file = str(mapping.get("source_env_file") or "").strip()
    if source_env_file:
        return str(Path(source_env_file).expanduser()), "codex_org_mapping_source_env_file"
    legacy_env = Path("tools-and-memory/orbital_credentials.env")
    if legacy_env.exists():
        return str(legacy_env), "legacy_project_orbital_env_file"
    return "", "environment_only"


def read_1password_ref(secret_ref: str) -> str:
    try:
        result = subprocess.run(
            ["op", "read", secret_ref],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "1Password CLI (`op`) is not installed or not available in PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or "1Password CLI failed to read the secret reference."
        raise RuntimeError(message) from exc
    return result.stdout.strip()


def read_env(names: list[str]) -> str:
    for name in names:
        if name and os.environ.get(name):
            return os.environ[name].strip()
    return ""


def fetch_access_token(region: str, client_id: str, client_secret: str, timeout: int) -> str:
    credentials = f"{client_id}:{client_secret}".encode("utf-8")
    token_url = (
        os.environ.get("ORBITAL_TOKEN_URL")
        or os.environ.get("SECURE_ENDPOINT_V3_VISIBILITY_TOKEN_URL")
        or TOKEN_SERVERS[region]
    )
    request = Request(
        token_url,
        data=b"grant_type=client_credentials",
        headers={
            "authorization": f"Basic {base64.b64encode(credentials).decode('ascii')}",
            "content-type": "application/x-www-form-urlencoded",
            "accept": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Token request failed with HTTP {exc.code}: {body[:500]}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error requesting access token: {exc}") from exc

    token = payload.get("access_token")
    if not isinstance(token, str) or not token:
        raise RuntimeError("Token response did not contain an access_token.")
    return token


def resolve_token(args: argparse.Namespace) -> str:
    env_names = [
        args.token_env,
        "ORBITAL_API_TOKEN",
        "ORBITAL_TOKEN",
        "SECUREX_TOKEN",
        "CISCO_SECUREX_TOKEN",
        "CISCO_TOKEN",
        "SECURE_ENDPOINT_BEARER_TOKEN",
        "AMP_BEARER_TOKEN",
        "BEARER_TOKEN",
    ]
    token = read_env(env_names)
    if token:
        return token

    if args.token_op_ref:
        return read_1password_ref(args.token_op_ref)

    client_id = read_env(
        [
            args.client_id_env,
            "ORBITAL_CLIENT_ID",
            "SECUREX_CLIENT_ID",
            "SECURE_ENDPOINT_V3_OAUTH_CLIENT_ID",
        ]
    )
    client_secret = read_env(
        [
            args.client_secret_env,
            "ORBITAL_CLIENT_SECRET",
            "SECUREX_CLIENT_SECRET",
            "SECURE_ENDPOINT_V3_OAUTH_CLIENT_SECRET",
        ]
    )
    if args.client_id_op_ref:
        client_id = read_1password_ref(args.client_id_op_ref)
    if args.client_secret_op_ref:
        client_secret = read_1password_ref(args.client_secret_op_ref)

    if client_id and client_secret:
        return fetch_access_token(args.region, client_id, client_secret, args.timeout)

    if not sys.stdin.isatty():
        raise RuntimeError(
            "No token or client credentials found. Set ORBITAL_API_TOKEN, provide "
            "1Password references, or run interactively to paste a bearer token."
        )

    return getpass.getpass("Orbital bearer token, without the 'Bearer ' prefix: ").strip()


def fetch_json(base_url: str, path: str, token: str, timeout: int) -> tuple[int, Any]:
    request = Request(
        f"{base_url}{path}",
        headers={
            "authorization": f"Bearer {token}",
            "accept": "application/json",
        },
        method="GET",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else {}
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed: Any = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"errors": [body[:500]]}
        return exc.code, parsed
    except URLError as exc:
        raise RuntimeError(f"Network error calling {path}: {exc}") from exc


def collection_count(payload: Any) -> int | str:
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list):
            return len(data)
        if "queries" in payload and isinstance(payload["queries"], list):
            return len(payload["queries"])
    return "n/a"


def summarize_stock(payload: Any) -> dict[str, int | str]:
    if not isinstance(payload, dict):
        return {}
    return {
        "authors": len(payload.get("authors", [])) if isinstance(payload.get("authors"), list) else "n/a",
        "categories": len(payload.get("categories", [])) if isinstance(payload.get("categories"), list) else "n/a",
        "queries": len(payload.get("queries", [])) if isinstance(payload.get("queries"), list) else "n/a",
        "scripts": len(payload.get("scripts", [])) if isinstance(payload.get("scripts"), list) else "n/a",
        "tactics": len(payload.get("tactics", [])) if isinstance(payload.get("tactics"), list) else "n/a",
        "techniques": len(payload.get("techniques", [])) if isinstance(payload.get("techniques"), list) else "n/a",
    }


def item_title(item: Any) -> str:
    if not isinstance(item, dict):
        return ""
    config = item.get("config") if isinstance(item.get("config"), dict) else {}
    for key in ("title", "name", "id", "ID"):
        if item.get(key):
            return str(item[key])
        if config.get(key):
            return str(config[key])
    script = item.get("script") if isinstance(item.get("script"), dict) else {}
    if script.get("name"):
        return str(script["name"])
    return ""


def write_summary(region: str, base_url: str, fetched_at: str, results: dict[str, dict[str, Any]]) -> None:
    lines = [
        "# Orbital Catalog API Import",
        "",
        f"Retrieved: {fetched_at}",
        "",
        "Import type: Structured context generated from read-only Orbital API catalog calls. Raw API responses are stored under `local/orbital-catalog-api-cache`. GitHub-synced Cisco-managed stock snapshots are stored under `queries_and_scripts/catalog_snapshot`.",
        "",
        "## API Source",
        "",
        f"- Region: `{region}`",
        f"- Server: `{base_url}`",
        "- Authentication: bearer token generated/read at runtime; bearer tokens are not written to project files.",
        "",
        "## Endpoints Fetched",
        "",
        "| Name | Method | Path | Status | Count |",
        "| --- | --- | --- | --- | --- |",
    ]

    for name, result in results.items():
        payload = result["payload"]
        count = collection_count(payload)
        if name == "stock_query_catalog":
            stock_summary = summarize_stock(payload)
            count = ", ".join(f"{k}: {v}" for k, v in stock_summary.items())
        lines.append(
            f"| {name} | GET | `{ENDPOINTS[name]}` | {result['status']} | {count} |"
        )

    lines.extend(
        [
            "",
            "## Raw Files",
            "",
        ]
    )
    for name in results:
        lines.append(f"- `{RAW_DIR.relative_to(ROOT) / f'{name}.json'}`")

    lines.extend(["", "## GitHub-Synced Stock Snapshot", ""])
    for name in sorted(GITHUB_SYNCED_STOCK_FILES):
        lines.append(f"- `{SNAPSHOT_DIR.relative_to(ROOT) / f'{name}.json'}`")
    lines.append("")
    lines.append("Only Cisco-managed stock catalog snapshots are synced to GitHub. Organization catalog exports remain local-only because they may contain tenant-specific content.")

    lines.extend(
        [
            "",
            "## Organization Catalog Privacy",
            "",
            "- Organization catalog query and script responses remain local-only because titles and content can be tenant-specific.",
            "- This GitHub-synced summary records only endpoint status; it does not include organization catalog titles or content.",
        ]
    )

    lines.extend(
        [
            "",
            "## Handling Notes",
            "",
            "- Treat imported API response files as source context, not editable catalog templates.",
            "- Do not commit or store bearer tokens. Refresh this import by rerunning `tools-and-memory/import_orbital_catalog.py` with a runtime token.",
            "- Use the operation-specific Cisco DevNet pages listed in `project-context/Orbital_API_DevNet.md` before implementing create, update, delete, live query, or live script calls.",
        ]
    )

    CONTEXT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    mapping = load_codex_org_mapping(args.org_mapping_state_file)
    env_file, credential_source = resolve_env_file(args, mapping)
    load_env_file(env_file)
    args.region = (
        args.region
        or os.environ.get("ORBITAL_REGION")
        or str(mapping.get("region") or "")
        or os.environ.get("SECURE_ENDPOINT_REGION")
        or "eu"
    ).strip().lower()
    if args.region not in SERVERS:
        raise RuntimeError(f"Unsupported region: {args.region}")
    token = resolve_token(args)
    if token.lower().startswith("bearer "):
        token = token.split(None, 1)[1]

    base_url = SERVERS[args.region]
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    results: dict[str, dict[str, Any]] = {}
    failures: list[str] = []

    for name, path in ENDPOINTS.items():
        status, payload = fetch_json(base_url, path, token, args.timeout)
        results[name] = {"status": status, "payload": payload}
        (RAW_DIR / f"{name}.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        if name in GITHUB_SYNCED_STOCK_FILES and 200 <= status < 300:
            (SNAPSHOT_DIR / f"{name}.json").write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        if status < 200 or status >= 300:
            failures.append(f"{name} returned HTTP {status}")

    write_summary(args.region, base_url, fetched_at, results)

    print(f"Wrote raw catalog API files to {RAW_DIR.relative_to(ROOT)}")
    print(f"Wrote stock catalog snapshots to {SNAPSHOT_DIR.relative_to(ROOT)}")
    print(f"Wrote project context to {CONTEXT_FILE.relative_to(ROOT)}")
    for name, result in results.items():
        print(f"{name}: HTTP {result['status']}")
    print(f"credential_source: {credential_source}")

    if failures:
        print("Failures: " + "; ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
