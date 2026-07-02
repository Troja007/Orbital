# Queries And Scripts

This is the root source repository for Orbital query and script content.

## Folder Ownership

| Folder | Source | Edit rule |
| --- | --- | --- |
| `catalog_queries/` | Imported from the Orbital Catalog | Treat as read-only source/template snapshots. |
| `catalog_scripts/` | Imported from the Orbital Catalog | Treat as read-only source/template snapshots. |
| `catalog_snapshot/` | Offline Cisco-managed stock catalog snapshot | Sync to GitHub and refresh periodically from Orbital API. |
| `catalog_result_profiles/` | Sanitized catalog validation result profiles | Sync to GitHub and use for query-result explanation. |
| `Generated_Queries/` | Generated SQL/JSON query artifacts | Temporary by default; commit only explicitly retained project artifacts. |
| `custom_queries/` | User-created query repository | Edit only when intentionally updating personal custom query work. |
| `custom_scripts/` | User-created script repository | Edit only when intentionally updating personal custom script work. |

Subfolders are allowed when separating queries or scripts by purpose, product area, investigation type, or reuse pattern.

Do not mix catalog imports and custom user-created work in the same folder.

When adapting a catalog item, copy it into `02_Working_Files/` first. Promote finished custom work into `custom_queries/` or `custom_scripts/` only when the user explicitly wants it stored as personal reusable repository content.

Generated SQL/JSON under `Generated_Queries/` is not the same as personal custom query work. Keep new generated scratch files local-only by default. Move or copy a finished query into `custom_queries/` only when it should become reusable personal repository content.

Only Cisco-managed stock catalog snapshots belong in `catalog_snapshot/`. Organization catalog exports remain local-only because they can contain tenant-specific data.

Catalog result profiles in `catalog_result_profiles/` are interpretation artifacts, not raw endpoint output. The `windows/` subfolder stores one human-readable Markdown file per Windows stock Catalog ID using the naming pattern `<catalog_id>__<normalized_query_name>.md`. Profiles may store Catalog IDs, row-count buckets, returned column names, no-response handling, sanitized caveats, and incident-responder reading guidance. They must not store endpoint result rows, hostnames, target selectors, Job IDs, raw API responses, tenant data, credentials, IP addresses, GUIDs, usernames, or customer-identifying values.
