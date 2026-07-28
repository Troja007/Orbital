# Catalog Result Profiles

This folder contains GitHub-synced, sanitized result-profile artifacts for Orbital catalog validation runs.

These files are designed to help an incident responder understand what an Orbital catalog query result means: expected result shape, row-count behavior, common caveats, safe assumptions, and sanitized sample shape where it is useful.

Included files:

- `<platform>_stock_catalog_result_profiles.jsonl`: structured per-Catalog-ID profiles for a platform's stock catalog queries. It contains no sample-row values.
- `<platform>_stock_catalog_result_profiles.md`: human-readable summary and table. It contains no sample-row values.
- `<platform>/`: one analyst-facing Markdown file per platform-specific stock catalog query, named `<catalog_id>__<normalized_query_name>.md`.

Privacy boundary:

- Store interpretation profiles, row counts, returned column names, catalog metadata, sanitized caveats, and no more than 15 structural sample rows in each per-Catalog-ID Markdown file.
- Do not store raw endpoint result rows, hostnames, target selectors, Job IDs, raw API responses, tenant data, credentials, IP addresses, GUIDs, usernames, customer-identifying values, or sample-row values in the JSONL or summary Markdown files.

Raw operational validation files stay local-only under `local/orbital_catalog_<platform>_validation/`.
