---
name: orbital-catalog-result-profiles
description: Generate, refresh, validate, or explain sanitized Cisco Orbital catalog result profiles from local catalog validation output. Use when Codex needs to build the GitHub-synced `queries_and_scripts/catalog_result_profiles/` artifacts, regenerate one Markdown file per Catalog ID, update profile-generation rules, validate that raw endpoint evidence is not published, or explain how catalog result profiles should be used to translate Orbital query results into incident-responder guidance.
---

# Orbital Catalog Result Profiles

Use this skill to maintain sanitized, GitHub-synced result profiles for Orbital stock catalog queries.

The profiles are interpretation artifacts. They help explain what an Orbital catalog query result means, including row-count behavior, returned columns, no-response handling, caveats, safe assumptions, and an analyst-facing explanation template. They are not raw endpoint evidence.

## Core Workflow

1. Read project rules first:
   - `AGENTS.md`
   - `queries_and_scripts/catalog_result_profiles/README.md`
   - `project-context/Orbital_Query_Catalog_Source_Map.md`
   - `project-context/Orbital_Windows_Catalog_Result_Reading.md`
2. Read `references/profile_format.md` when changing profile structure, privacy rules, or generated Markdown sections.
3. Verify the local validation source exists:
   - `local/orbital_catalog_windows_validation/windows_catalog_execution_results.jsonl`
4. Run the project generator from the repository root:

```bash
python3 02_Working_Files/generate_catalog_result_profiles.py
```

5. Validate generated output:

```bash
PYTHONPYCACHEPREFIX=/tmp/orbital_pycache python3 -m py_compile 02_Working_Files/generate_catalog_result_profiles.py
find queries_and_scripts/catalog_result_profiles/windows -type f -name '*.md' | wc -l
rg -n "host:|orbital_queryID|/v0/jobs/|Bearer|ORBITAL_API_TOKEN|client_secret" queries_and_scripts/catalog_result_profiles 02_Working_Files/generate_catalog_result_profiles.py || true
```

Expected current baseline:

- `384` files under `queries_and_scripts/catalog_result_profiles/windows/`
- `queries_and_scripts/catalog_result_profiles/windows_stock_catalog_result_profiles.jsonl`
- `queries_and_scripts/catalog_result_profiles/windows_stock_catalog_result_profiles.md`
- `queries_and_scripts/catalog_result_profiles/windows/process_hashes__sha256_hash_of_running_processes.md`

## Output Locations

Generated GitHub-synced artifacts:

- `queries_and_scripts/catalog_result_profiles/windows_stock_catalog_result_profiles.jsonl`
- `queries_and_scripts/catalog_result_profiles/windows_stock_catalog_result_profiles.md`
- `queries_and_scripts/catalog_result_profiles/windows/*.md`

Local-only source material:

- `local/orbital_catalog_windows_validation/*.jsonl`
- `local/orbital_catalog_windows_validation/*.json`
- `local/orbital_catalog_windows_validation/*.md`

Do not stage or publish local raw validation files. They can include target selectors, Job IDs, API fragments, or operational identifiers.

## Per-Catalog File Naming

Use this filename pattern:

```text
<catalog_id>__<normalized_query_name>.md
```

Example:

```text
process_hashes__sha256_hash_of_running_processes.md
```

Keep Catalog ID first because it is the stable lookup key across API, UI, and local profile context.

## Privacy Boundary

Profiles may store:

- Catalog ID and name
- Platform, categories, labels, MITRE mapping, catalog update date
- Row-count bucket and sanitized validation row count
- Returned label names and column names
- Sanitized error classes and caveats
- No-response handling and explanation templates

Profiles must not store:

- Endpoint result rows
- Hostnames
- Target selectors
- Job IDs
- Usernames
- IP addresses
- GUIDs
- Tenant data
- Raw API responses
- Credentials or tokens

## Change Logging

When profile generation behavior, profile format, project references, or skill instructions change, append a sanitized entry to `local/project-change-log.md`.

When pushing profile changes to GitHub, append a sanitized operational entry to `local/sync-activity-log.md`.

Neither local log may be staged or pushed.
