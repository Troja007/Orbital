#!/usr/bin/env python3
"""Create reviewed, local-only Codex-skill release snapshots and inspect history."""

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


def version_key(version: str) -> tuple[int, int, int]:
    return tuple(int(part) for part in version.split("."))


def versions_dir(skill_dir: Path) -> Path:
    return skill_dir / "versions"


def retained_versions(skill_dir: Path) -> list[Path]:
    root = versions_dir(skill_dir)
    if not root.exists():
        return []
    return sorted(
        (path for path in root.iterdir() if path.is_dir() and SEMVER_PATTERN.fullmatch(path.name)),
        key=lambda path: version_key(path.name),
    )


def records(root: Path) -> dict[str, str]:
    result = {}
    for source in sorted(root.rglob("*")):
        relative = source.relative_to(root)
        if any(part in EXCLUDED_PARTS for part in relative.parts) or not source.is_file():
            continue
        result[relative.as_posix()] = sha256_file(source)
    return result


def manifest_records(snapshot: Path) -> dict[str, str]:
    manifest = snapshot / "manifest.json"
    if manifest.is_file():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        return {item["path"]: item["sha256"] for item in data.get("files", [])}
    return records(snapshot)


def file_delta(previous: dict[str, str], current: dict[str, str]) -> dict[str, list[str]]:
    return {
        "added": sorted(set(current) - set(previous)),
        "modified": sorted(path for path in set(current) & set(previous) if current[path] != previous[path]),
        "deleted": sorted(set(previous) - set(current)),
    }


def tree_fingerprint(file_records: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for path, checksum in sorted(file_records.items()):
        digest.update(f"{path}\0{checksum}\n".encode())
    return digest.hexdigest()


def prior_matches(skill_dir: Path, previous: dict[str, str], current: dict[str, str], previous_version: str | None) -> tuple[list[dict[str, object]], list[str]]:
    reintroduced = []
    tree_matches = []
    current_tree = tree_fingerprint(current)
    for snapshot in retained_versions(skill_dir):
        if snapshot.name == previous_version:
            continue
        historic = manifest_records(snapshot)
        if tree_fingerprint(historic) == current_tree:
            tree_matches.append(snapshot.name)
        for path, checksum in current.items():
            if previous.get(path) != checksum and historic.get(path) == checksum:
                reintroduced.append({"path": path, "matches_version": snapshot.name})
    return reintroduced, tree_matches


def history(skill_dir: Path) -> int:
    releases = []
    for snapshot in retained_versions(skill_dir):
        manifest = snapshot / "manifest.json"
        data = json.loads(manifest.read_text(encoding="utf-8")) if manifest.is_file() else {}
        release = data.get("release", {})
        changes = data.get("change_set", {})
        releases.append({
            "version": snapshot.name,
            "summary": release.get("change_summary", "historical metadata unavailable"),
            "type": release.get("change_type", "legacy"),
            "previous_version": release.get("reviewed_previous_version"),
            "added": len(changes.get("added", [])),
            "modified": len(changes.get("modified", [])),
            "deleted": len(changes.get("deleted", [])),
            "possible_reintroductions": len(data.get("regression_review", {}).get("possible_reintroduced_paths", [])),
        })
    print(json.dumps({"skill": skill_dir.name, "releases": releases}, indent=2, sort_keys=True))
    return 0


def snapshot(skill_dir: Path, args: argparse.Namespace) -> Path:
    if not SEMVER_PATTERN.fullmatch(args.version):
        raise RuntimeError("--version must use MAJOR.MINOR.PATCH semantic versioning.")
    required = {
        "--change-summary": args.change_summary,
        "--review-notes": args.review_notes,
        "--validation": args.validation,
        "--problem-statement": args.problem_statement,
        "--success-criteria": args.success_criteria,
        "--positive-trigger": args.positive_trigger,
        "--negative-trigger": args.negative_trigger,
        "--dependency-review": args.dependency_review,
    }
    missing = [name for name, value in required.items() if not value.strip()]
    if missing:
        raise RuntimeError("Required release evidence missing: " + ", ".join(missing))
    if args.positive_trigger.strip().casefold() == args.negative_trigger.strip().casefold():
        raise RuntimeError("Positive and negative trigger examples must be different.")
    if args.risk_tier == "sensitive" and not args.failure_path_validation.strip():
        raise RuntimeError("Sensitive releases require --failure-path-validation.")
    if args.keep < 1:
        raise RuntimeError("--keep must be at least 1.")
    target = versions_dir(skill_dir) / args.version
    if target.exists():
        raise RuntimeError(f"Version snapshot already exists: {target}")

    prior = retained_versions(skill_dir)
    if prior and version_key(args.version) <= version_key(prior[-1].name):
        raise RuntimeError(f"New version must exceed retained version {prior[-1].name}.")
    previous_snapshot = prior[-1] if prior else None
    previous_version = previous_snapshot.name if previous_snapshot else None
    current = records(skill_dir)
    previous = manifest_records(previous_snapshot) if previous_snapshot else {}
    changes = file_delta(previous, current)
    if previous_snapshot and not any(changes.values()):
        raise RuntimeError("Refusing an unchanged release; update the skill or do not increment VERSION.")
    reintroduced, tree_matches = prior_matches(skill_dir, previous, current, previous_version)
    if (reintroduced or tree_matches) and not args.allow_reintroduction:
        raise RuntimeError("Potential reintroduction detected; review it or use --allow-reintroduction with a documented reason.")

    target.mkdir(parents=True)
    for relative in sorted(current):
        source = skill_dir / relative
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    manifest = {
        "version": args.version,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "files": [{"path": path, "sha256": checksum} for path, checksum in sorted(current.items())],
        "release": {
            "change_type": args.change_type,
            "change_summary": args.change_summary,
            "reviewed_previous_version": previous_version,
            "review_notes": args.review_notes,
            "validation": args.validation,
        },
        "change_set": changes,
        "regression_review": {
            "possible_reintroduced_paths": reintroduced,
            "matching_prior_trees": tree_matches,
            "override_used": bool(args.allow_reintroduction),
        },
        "outcome_guardrails": {
            "problem_statement": args.problem_statement,
            "success_criteria": args.success_criteria,
            "positive_trigger": args.positive_trigger,
            "negative_trigger": args.negative_trigger,
            "dependency_review": args.dependency_review,
            "risk_tier": args.risk_tier,
            "failure_path_validation": args.failure_path_validation,
        },
    }
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    retained = retained_versions(skill_dir)
    for old in retained[:-args.keep]:
        shutil.rmtree(old)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Snapshot a reviewed Codex-skill release or inspect retained history.")
    parser.add_argument("--skill-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--history", action="store_true", help="Print release metadata and file-delta counts.")
    parser.add_argument("--version", help="New MAJOR.MINOR.PATCH version.")
    parser.add_argument("--change-type", choices=["feature", "fix", "maintenance", "breaking"])
    parser.add_argument("--change-summary", default="")
    parser.add_argument("--review-notes", default="")
    parser.add_argument("--validation", default="")
    parser.add_argument("--problem-statement", default="")
    parser.add_argument("--success-criteria", default="")
    parser.add_argument("--positive-trigger", default="")
    parser.add_argument("--negative-trigger", default="")
    parser.add_argument("--dependency-review", default="")
    parser.add_argument("--risk-tier", choices=["documentation", "code", "sensitive"], default="documentation")
    parser.add_argument("--failure-path-validation", default="")
    parser.add_argument("--allow-reintroduction", action="store_true")
    parser.add_argument("--keep", type=int, default=5)
    args = parser.parse_args()
    skill_dir = Path(args.skill_dir).resolve()
    if args.history:
        return history(skill_dir)
    if not args.version or not args.change_type:
        parser.error("--version and --change-type are required unless --history is used.")
    created = snapshot(skill_dir, args)
    print(json.dumps({"snapshot": str(created), "retained_versions": args.keep}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
