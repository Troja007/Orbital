# Installable Codex Skills

This folder contains project skills that can be installed into Codex from GitHub.

Install all project skills:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Troja007/Orbital \
  --path skills/github-sync-workflow \
  --path skills/orbital-api-access \
  --path skills/orbital-catalog-result-profiles \
  --path skills/orbital-query-method-memory \
  --path skills/orbital-run-osquery-live-query \
  --path skills/orbital-update-catalog
```

Install one skill:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Troja007/Orbital \
  --path skills/orbital-run-osquery-live-query
```

Restart Codex after installing or updating skills.

Do not commit `skills/.system/`; those are local Codex system skills.
