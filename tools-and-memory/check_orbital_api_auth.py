#!/usr/bin/env python3
"""Check Orbital API authentication with GET /ok.

This is a read-only health/auth check. It prints status and a compact response
summary, and never prints bearer tokens or credentials.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
from typing import Any
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

REDACT_KEYS = {
    "application",
    "email",
    "jwt",
    "organization",
    "organizationname",
    "token",
    "access_token",
    "refresh_token",
    "authorization",
    "user",
    "username",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Orbital API auth with GET /ok.")
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


def first_env(names: list[str]) -> str:
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return ""


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
        return existing.removeprefix("Bearer ").strip()

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


def call_ok(region: str, token: str, timeout: int) -> dict[str, Any]:
    request = Request(
        f"{SERVERS[region]}/ok",
        headers={"authorization": f"Bearer {token}", "accept": "application/json"},
        method="GET",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            try:
                payload: Any = json.loads(body) if body else {}
            except json.JSONDecodeError:
                payload = body
            return {"status": response.status, "region": region, "response": payload}
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            payload = body[:500]
        return {"status": exc.code, "region": region, "response": payload}


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        cleaned: dict[str, Any] = {}
        for key, child in value.items():
            if key.lower() in REDACT_KEYS or "token" in key.lower():
                cleaned[key] = "[redacted]"
            else:
                cleaned[key] = redact(child)
        return cleaned
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


def main() -> int:
    args = parse_args()
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

    token = fetch_access_token(region, args.timeout)
    result = call_ok(region, token, args.timeout)
    result = redact(result)
    result["credential_context"] = {
        "source": credential_source,
        "env_file_loaded": bool(env_file),
        "mapping_state_file_loaded": bool(mapping),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == 200 else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, URLError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        raise SystemExit(1)
