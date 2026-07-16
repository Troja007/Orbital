# Orbital Catalog API Import

Retrieved: 2026-07-16T11:42:05+00:00

Import type: Structured context generated from read-only Orbital API catalog calls. Raw API responses are stored under `local/orbital-catalog-api-cache`. GitHub-synced Cisco-managed stock snapshots are stored under `queries_and_scripts/catalog_snapshot`.

## API Source

- Region: `us`
- Server: `https://orbital.amp.cisco.com/v0`
- Authentication: bearer token generated/read at runtime; bearer tokens are not written to project files.

## Endpoints Fetched

| Name | Method | Path | Status | Count |
| --- | --- | --- | --- | --- |
| stock_query_catalog | GET | `/stock` | 200 | authors: 5, categories: 11, queries: 467, scripts: 51, tactics: 14, techniques: 211 |
| organization_catalog_queries | GET | `/catalogs` | 200 | 13 |
| organization_catalog_scripts | GET | `/catalogs/scripts` | 200 | 19 |
| stock_catalog_scripts | GET | `/catalogs/cisco/scripts` | 200 | 75 |

## Raw Files

- `local/orbital-catalog-api-cache/stock_query_catalog.json`
- `local/orbital-catalog-api-cache/organization_catalog_queries.json`
- `local/orbital-catalog-api-cache/organization_catalog_scripts.json`
- `local/orbital-catalog-api-cache/stock_catalog_scripts.json`

## GitHub-Synced Stock Snapshot

- `queries_and_scripts/catalog_snapshot/stock_catalog_scripts.json`
- `queries_and_scripts/catalog_snapshot/stock_query_catalog.json`

Only Cisco-managed stock catalog snapshots are synced to GitHub. Organization catalog exports remain local-only because they may contain tenant-specific content.

## Organization Catalog Privacy

- Organization catalog query and script responses remain local-only because titles and content can be tenant-specific.
- This GitHub-synced summary records only endpoint status; it does not include organization catalog titles or content.

## Handling Notes

- Treat imported API response files as source context, not editable catalog templates.
- Do not commit or store bearer tokens. Refresh this import by rerunning `tools-and-memory/import_orbital_catalog.py` with a runtime token.
- Use the operation-specific Cisco DevNet pages listed in `project-context/Orbital_API_DevNet.md` before implementing create, update, delete, live query, or live script calls.
