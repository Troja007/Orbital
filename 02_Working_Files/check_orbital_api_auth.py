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

REDACT_KEYS = {"jwt", "token", "access_token", "refresh_token", "authorization"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check Orbital API auth with GET /ok.")
    parser.add_argument("--env-file", default="02_Working_Files/orbital_credentials.env")
    parser.add_argument("--region", default="")
    parser.add_argument("--timeout", type=int, default=30)
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
        return existing.removeprefix("Bearer ").strip()

    client_id = first_env(["ORBITAL_CLIENT_ID", "SECUREX_CLIENT_ID"])
    client_secret = first_env(["ORBITAL_CLIENT_SECRET", "SECUREX_CLIENT_SECRET"])
    if not (client_id and client_secret):
        raise RuntimeError("No Orbital token or client credentials found.")

    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode(
        "ascii"
    )
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
    load_env_file(args.env_file)
    region = (args.region or os.environ.get("ORBITAL_REGION") or "eu").strip().lower()
    if region not in SERVERS:
        raise RuntimeError(f"Unsupported region: {region}")

    token = fetch_access_token(region, args.timeout)
    result = call_ok(region, token, args.timeout)
    result = redact(result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == 200 else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, URLError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        raise SystemExit(1)
