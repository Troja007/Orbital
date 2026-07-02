# Catalog Result Profiles

This folder contains GitHub-synced, sanitized result-profile artifacts for Orbital catalog validation runs.

These files are designed to help an incident responder understand what an Orbital catalog query result means: expected result shape, row-count behavior, common caveats, and safe assumptions.

Included files:

- `windows_stock_catalog_result_profiles.jsonl`: structured per-Catalog-ID profiles for Windows stock catalog queries.
- `windows_stock_catalog_result_profiles.md`: human-readable summary and table.

Privacy boundary:

- Store interpretation profiles, row counts, returned column names, catalog metadata, and sanitized caveats.
- Do not store endpoint result rows, hostnames, target selectors, Job IDs, raw API responses, tenant data, credentials, IP addresses, GUIDs, usernames, or customer-identifying values.

Raw operational validation files stay local-only under `local/orbital_catalog_windows_validation/`.
