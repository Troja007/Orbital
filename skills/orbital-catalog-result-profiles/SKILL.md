---
name: orbital-catalog-result-profiles
description: Generate, refresh, validate, or explain sanitized Cisco Orbital catalog result profiles from local catalog validation output. Use when Codex needs to build the GitHub-synced `queries_and_scripts/catalog_result_profiles/` artifacts, regenerate one Markdown file per Catalog ID, update profile-generation rules, validate that raw endpoint evidence is not published, or explain how catalog result profiles should be used to translate Orbital query results into incident-responder guidance.
---

# Orbital Catalog Result Profiles

Use this skill to maintain sanitized, GitHub-synced result profiles for Orbital stock catalog queries.

The profiles are interpretation artifacts. They help explain what an Orbital catalog query result means, including row-count behavior, returned columns, no-response handling, caveats, safe assumptions, an analyst-facing explanation template, and sanitized sample result data. They are not raw endpoint evidence.

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

## Sample Result Data

When profiles are regenerated or refreshed, each per-Catalog-ID Markdown profile, and any human-readable report updated from the same profile data, must end with a `Sample Result Data` section.

Include a small, representative sample only when the validation source has rows. Prefer enough rows to show the result shape without turning the profile into evidence storage. If a response includes many rows, the generated profile must show no more than 15 sanitized sample rows total for that Catalog ID. If multiple labels return rows, distribute the 15-row maximum across labels in a representative way.

Sanitize sample values before writing them:

- Remove or replace usernames, user profile paths, email addresses, hostnames, IP addresses, GUIDs, tenant/customer identifiers, target selectors, Job IDs, API URLs, tokens, secrets, and any value that could identify a person, endpoint, tenant, customer, or validation run.
- Preserve column names and safe structural cues where useful, such as file-extension shape, registry-root family, process-name class, service-state class, timestamp shape, or hash-format shape.
- Use explicit redaction markers such as `<redacted:username>`, `<redacted:hostname>`, `<redacted:ip>`, `<redacted:guid>`, or `<redacted:sensitive-value>` rather than leaving sensitive values blank.
- If a sample row cannot be safely sanitized without losing meaning, omit that row and state that sample data was omitted for privacy.

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
- Sanitized sample result rows at the end of generated Markdown files
- Sanitized error classes and caveats
- No-response handling and explanation templates

Profiles must not store:

- Raw endpoint result rows
- Hostnames
- Target selectors
- Job IDs
- Usernames
- IP addresses
- GUIDs
- Tenant data
- Raw API responses
- Credentials or tokens

Sanitized sample rows are still subject to a maximum of 15 rows per generated per-Catalog-ID Markdown profile.

## Change Logging

When profile generation behavior, profile format, project references, or skill instructions change, append a sanitized entry to `local/project-change-log.md`.

When pushing profile changes to GitHub, append a sanitized operational entry to `local/sync-activity-log.md`.

Neither local log may be staged or pushed.
