# osquery Schema 5.23.0

Source URL: https://osquery.io/schema/5.23.0/

Source title: osquery | Schema

Retrieved: 2026-06-02

Import type: Structured schema extraction from the osquery schema page.

## Imported Files

- Full table and column schema: `product-context/osquery/osquery_schema_5_23_0.json`
- Compact table index: `product-context/osquery/osquery_schema_5_23_0_table_index.json`
- Source snapshot manifest: `product-context/osquery/README.md`

## Extracted Scope

- osquery version: 5.23.0
- Tables extracted: 286
- Evented tables extracted: 22
- Total columns extracted: 2624

## Project Relevance

Orbital queries are based on osquery. The osquery schema defines the database-style tables and columns used for SQL-based endpoint inspection.

Orbital includes osquery capabilities and may also include Orbital-specific capabilities, restrictions, disabled tables, or platform-specific differences. Treat this schema as the upstream osquery reference, not as a complete guarantee of what Orbital exposes on every endpoint.

For query catalog work, combine this schema with `Orbital_Query_Catalog_Source_Map.md`, `Orbital_API_DevNet.md`, and `Orbital_Catalog_UI_Terms.md`.

## Refresh Policy

Treat the JSON files as Git-tracked upstream source snapshots that may need updates over time.

Refresh or review this context when:

- A newer upstream osquery schema version becomes relevant.
- The Orbital catalog snapshot changes and new catalog queries reference tables or columns not found in the current schema snapshot.
- Orbital documentation or product behavior indicates enabled, disabled, modified, or Orbital-specific table support.

Keep upstream schema version changes separate from Orbital catalog changes. A catalog refresh can introduce different usage of existing tables without requiring a new osquery schema version. A new osquery schema version can introduce tables that are not necessarily available in Orbital.

## Query Work Rules

When creating or reviewing Orbital queries:

- Verify table names against `osquery_schema_5_23_0.json`.
- Verify column names and column types before finalizing SQL.
- Check whether a table is evented.
- Check whether the table is platform-specific.
- Check whether Orbital disables or modifies the table before assuming availability.
- Check whether the query needs `allowos` or an operating system filter.
- For expensive tables or broad targeting, consider endpoint impact before using the query at scale.

## Large Tables By Column Count

- `processes`: 39 columns
- `interface_details`: 35 columns
- `file`: 33 columns
- `curl_certificate`: 32 columns
- `docker_info`: 32 columns
- `es_process_events`: 32 columns
- `md_devices`: 31 columns
- `process_events`: 31 columns
- `chrome_extensions`: 27 columns
- `docker_container_stats`: 27 columns
- `docker_containers`: 24 columns
- `certificates`: 23 columns
- `docker_container_processes`: 23 columns
- `security_profile_info`: 23 columns
- `apparmor_events`: 22 columns

## Notes

The schema extraction preserves table descriptions and column descriptions from the page in structured JSON form. Use the JSON file for exact table and column lookup rather than relying on this summary.
