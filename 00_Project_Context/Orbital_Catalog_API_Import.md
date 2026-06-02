# Orbital Catalog API Import

Retrieved: 2026-06-02T07:42:39+00:00

Import type: Structured context generated from read-only Orbital API catalog calls. Raw API responses are stored under `01_Source_Files/API_References/Orbital_Catalog_API`.

Latest stock catalog refresh: `GET /v0/stock` returned HTTP 200 on 2026-06-02T08:02:40+00:00. The full response is stored in `01_Source_Files/API_References/Orbital_Catalog_API/stock_query_catalog.json`.

## API Source

- Region: `us`
- Server: `https://orbital.amp.cisco.com/v0`
- Authentication: bearer token generated/read at runtime; bearer tokens are not written to project files.

## Endpoints Fetched

| Name | Method | Path | Status | Count |
| --- | --- | --- | --- | --- |
| stock_query_catalog | GET | `/stock` | 200 | authors: 5, categories: 11, queries: 467, scripts: 48, tactics: 14, techniques: 211 |
| organization_catalog_queries | GET | `/catalogs` | not published | redacted |
| organization_catalog_scripts | GET | `/catalogs/scripts` | not published | redacted |
| stock_catalog_scripts | GET | `/catalogs/cisco/scripts` | 200 | 72 |

## Raw Files

- `01_Source_Files/API_References/Orbital_Catalog_API/stock_query_catalog.json`
- `01_Source_Files/API_References/Orbital_Catalog_API/stock_catalog_scripts.json`

## Sample Organization Query Titles

- Redacted for the public GitHub copy because organization catalog names can be tenant-specific.

## Sample Organization Script Titles

- Redacted for the public GitHub copy because organization catalog names can be tenant-specific.

## Handling Notes

- Treat imported API response files as source context, not editable catalog templates.
- Do not commit or store bearer tokens. Refresh this import by rerunning `02_Working_Files/import_orbital_catalog.py` with a runtime token.
- Use the operation-specific Cisco DevNet pages listed in `00_Project_Context/Orbital_API_DevNet.md` before implementing create, update, delete, live query, or live script calls.
