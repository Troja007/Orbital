# Catalog Snapshot

Offline copy of Cisco-managed Orbital stock catalog data used for query and script selection decisions.

## Files

| File | API source | Current count | Purpose |
| --- | --- | ---: | --- |
| `stock_query_catalog.json` | `GET /v0/stock` | 467 queries, 49 scripts | Full stock query catalog and related metadata such as authors, categories, observables, tactics, techniques, and subtechniques. |
| `stock_catalog_scripts.json` | `GET /v0/catalogs/cisco/scripts` | 73 scripts | Full Cisco-managed stock script catalog response. |

## Handling Rules

- These files are intended to be synced to GitHub.
- Refresh them periodically when Cisco releases new Orbital catalog content.
- Use them as decision support when choosing which Orbital query or script to use.
- Do not edit catalog snapshot JSON by hand.
- Do not store organization catalog exports in this folder.
- Keep `organization_catalog_queries.json` and `organization_catalog_scripts.json` local-only because they may contain tenant-specific content.

## Current Snapshot

- Retrieved: 2026-06-10T17:39:04+00:00
- Region: `us`
- Source summary: `project-context/Orbital_Catalog_API_Import.md`
- Local refresh helper: `02_Working_Files/import_orbital_catalog.py`
