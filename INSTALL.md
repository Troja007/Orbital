# Install This Orbital Codex Project

Use this when starting a new Codex workspace from the GitHub repository.

Repository:

```text
https://github.com/Troja007/Orbital
```

## Required Model

The project must be installed in two parts:

1. Clone or open the full GitHub repository as the active Codex project workspace.
2. Install the project skills from the repository.

The skills alone are not enough. They depend on the repository content for project context, product context, query-method memory, catalog snapshots, catalog result profiles, helper scripts, and decision records.

## Prompt For A New Codex Chat

```text
Install and initialize the Cisco Orbital Codex project from GitHub.

Repository:
https://github.com/Troja007/Orbital

Goal:
Set up this repository as the active Codex project workspace, then install all project skills from the repo so Codex can use the Orbital context, query-method memory, catalog snapshots, result profiles, and helper workflows.

Required steps:
1. Clone or open the GitHub repository as the active workspace.
2. Read `README.md`, `AGENTS.md`, and `INSTALL.md`.
3. Confirm the following folders/files exist:
   - `project-context/`
   - `product-context/`
   - `notes-and-memory/decisions/`
   - `tools-and-memory/query-method-memory/`
   - `queries_and_scripts/catalog_snapshot/`
   - `queries_and_scripts/catalog_result_profiles/`
   - `skills/`
4. Install all project skills from the repository:
   - `skills/github-sync-workflow`
   - `skills/orbital-api-access`
   - `skills/orbital-catalog-result-profiles`
   - `skills/orbital-query-method-memory`
   - `skills/orbital-run-osquery-live-query`
   - `skills/orbital-update-catalog`
5. Verify the skills are installed.
6. Do not create, request, print, or store credentials.
7. Do not run Orbital API calls yet.
8. Report what was installed, what project context was found, and what is still missing or local-only.

Use the repository content as the project knowledge base. The skills alone are not enough; the repo files are required context.
```

## Skill Install Command

Run this from any shell where Codex skills are available:

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

Restart Codex after installing or updating skills.

## Expected GitHub-Synced Content

A correct full project import should include:

- `AGENTS.md`: project rules and terminology.
- `README.md`: project overview and working model.
- `project-context/`: Orbital API, catalog, target selector, query, and script context.
- `product-context/`: osquery schema and product investigation context.
- `notes-and-memory/decisions/`: durable project decisions.
- `tools-and-memory/query-method-memory/`: reusable query-method knowledge.
- `queries_and_scripts/catalog_snapshot/`: offline stock catalog JSON snapshots.
- `queries_and_scripts/catalog_result_profiles/`: sanitized catalog result interpretation profiles.
- `queries_and_scripts/catalog_queries/` and `queries_and_scripts/catalog_scripts/`: Cisco-managed catalog source templates.
- `queries_and_scripts/custom_queries/` and `queries_and_scripts/custom_scripts/`: user-owned custom repository content.
- `skills/`: project skill packages.

## Expected Local-Only Content

These items are intentionally not included from GitHub and must stay local:

- Real Orbital credentials.
- `tools-and-memory/orbital_credentials.env`.
- `local/project-change-log.md`.
- `local/sync-activity-log.md`.
- Raw Orbital API cache files.
- Organization catalog exports.
- Endpoint query run ledgers.
- Raw endpoint validation results.
- Tenant, customer, hostname, IP, GUID, username, token, or raw API response data.

## First Verification Checklist

After import and skill installation:

1. Confirm the repository is the active workspace.
2. Confirm `README.md`, `AGENTS.md`, and this `INSTALL.md` were read.
3. Confirm the six project skills are installed.
4. Confirm the repository context folders exist.
5. Confirm no credentials were created or committed.
6. Confirm no Orbital API calls were run during installation.
7. Report missing local-only items only as prerequisites, not as errors.
