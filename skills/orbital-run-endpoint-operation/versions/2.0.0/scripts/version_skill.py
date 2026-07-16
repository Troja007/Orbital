#!/usr/bin/env python3
"""Create a retained, non-recursive snapshot of this skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


EXCLUDED_PARTS = {"versions", "__pycache__", ".DS_Store"}
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def version_sort_key(path: Path) -> tuple[int, int, int]:
    return tuple(int(part) for part in path.name.split("."))


def snapshot(skill_dir: Path, version: str, keep: int) -> Path:
    versions_dir = skill_dir / "versions"
    target = versions_dir / version
    if target.exists():
        raise RuntimeError(f"Version snapshot already exists: {target}")
    if not SEMVER_PATTERN.fullmatch(version):
        raise RuntimeError("--version must use semantic version format MAJOR.MINOR.PATCH.")
    if keep < 1:
        raise RuntimeError("--keep must be at least 1")

    target.mkdir(parents=True)
    manifest_files: list[dict[str, str]] = []
    for source in sorted(skill_dir.rglob("*")):
        relative = source.relative_to(skill_dir)
        if any(part in EXCLUDED_PARTS for part in relative.parts) or not source.is_file():
            continue
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        manifest_files.append(
            {"path": relative.as_posix(), "sha256": sha256_file(source)}
        )

    manifest = {
        "version": version,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "files": manifest_files,
    }
    (target / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    retained = sorted(
        (path for path in versions_dir.iterdir() if path.is_dir() and SEMVER_PATTERN.fullmatch(path.name)),
        key=version_sort_key,
    )
    for old_snapshot in retained[:-keep]:
        shutil.rmtree(old_snapshot)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Snapshot an Orbital skill and retain recent versions.")
    parser.add_argument("--skill-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--version", required=True, help="Unique semantic version, for example 1.1.0.")
    parser.add_argument("--keep", type=int, default=5)
    args = parser.parse_args()

    created = snapshot(Path(args.skill_dir).resolve(), args.version, args.keep)
    print(json.dumps({"snapshot": str(created), "retained_versions": args.keep}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
