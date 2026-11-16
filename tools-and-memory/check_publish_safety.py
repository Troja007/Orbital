#!/usr/bin/env python3
"""Check tracked files for values that must not be published.

Scans every file tracked by Git, both its path and its text content, for:
- user profile paths (/Users/<name>, /home/<name>, C:\\Users\\<name>)
- e-mail addresses
- private IPv4 addresses
- GUIDs
- bearer tokens and key=value secrets
- any literal from an optional local deny list (one value per line), such as
  lab hostnames or usernames. The deny list stays local so that the names
  themselves are never published: default path `local/publish-denylist.txt`.

Allowed literals (documented examples) are listed in `.publish-check-allow.txt`.
Cisco-managed read-only catalog copies are skipped for GUID/IP checks.

Exit code 0 = clean, 1 = findings. Use before every push or share:
    python3 tools-and-memory/check_publish_safety.py
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

PATTERNS = {
    "user-path": re.compile(r"(?:/Users/|/home/|[Cc]:\\{1,2}Users\\{1,2})(?!<|\$|%|\{|[Pp]ublic\b|[Dd]efault\b|[Aa]ll Users\b|\*)[A-Za-z0-9._-]+"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "private-ip": re.compile(r"\b(?:10\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b"),
    "guid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"),
    "secret": re.compile(r"(?i)\b(?:bearer\s+[A-Za-z0-9._-]{20,}|(?:client_secret|api_key|password|token)\s*[=:]\s*['\"][^'\"<>{}$]{8,}['\"])"),
}
CATALOG_COPIES = (
    "queries_and_scripts/catalog_snapshot/",
    "queries_and_scripts/catalog_queries/",
    "queries_and_scripts/catalog_scripts/",
)
SKIP_IN_CATALOG = {"guid", "private-ip"}
SAFE_EMAIL_DOMAINS = ("example.com", "example.org", "users.noreply.github.com", "anthropic.com")


def tracked_files(root: Path) -> list[str]:
    out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=True)
    return [p for p in out.stdout.decode("utf-8").split("\0") if p]


def load_list(path: Path) -> list[str]:
    if not path.is_file():
        return []
    values = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            values.append(line)
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--denylist", default="local/publish-denylist.txt")
    parser.add_argument("--allowlist", default=".publish-check-allow.txt")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    allow = set(load_list(root / args.allowlist))
    deny = [v.lower() for v in load_list(root / args.denylist)]
    deny_re = (
        re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(re.escape(v) for v in deny) + r")(?![A-Za-z0-9])", re.IGNORECASE)
        if deny
        else None
    )

    findings: list[str] = []

    def report(path: str, line: int | None, kind: str, value: str) -> None:
        if value in allow:
            return
        if kind == "email" and value.lower().endswith(SAFE_EMAIL_DOMAINS):
            return
        where = f"{path}:{line}" if line else f"{path} (file name)"
        findings.append(f"{where}: {kind}: {value}")

    for rel in tracked_files(root):
        in_catalog = rel.startswith(CATALOG_COPIES)
        if deny_re:
            for m in deny_re.finditer(rel):
                report(rel, None, "denylist", m.group(0))
        if rel == args.allowlist:
            continue
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
        for no, line in enumerate(text.splitlines(), 1):
            for kind, rx in PATTERNS.items():
                if in_catalog and kind in SKIP_IN_CATALOG:
                    continue
                for m in rx.finditer(line):
                    report(rel, no, kind, m.group(0))
            if deny_re:
                for m in deny_re.finditer(line):
                    report(rel, no, "denylist", m.group(0))

    if not deny:
        print(f"note: no local deny list at {args.denylist}; hostname/username literals not checked", file=sys.stderr)
    if findings:
        print("\n".join(findings))
        print(f"\n{len(findings)} finding(s). Anonymize them or, for documented examples, add the exact value to {args.allowlist}.")
        return 1
    print("publish safety check: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
