# Orbital Source Repository Model

This project separates Cisco-managed catalog source material from user-owned custom Orbital work.

## Source Classes

| Source class | Current folder | Ownership | Edit rule | Purpose |
| --- | --- | --- | --- | --- |
| Catalog query templates | `queries_and_scripts/catalog_queries/` | Cisco-managed catalog source copy | Read-only | Stable source/template material for query design without repeatedly pulling from the live catalog. |
| Catalog script templates | `queries_and_scripts/catalog_scripts/` | Cisco-managed catalog source copy | Read-only | Stable source/template material for response script design without repeatedly pulling from the live catalog. |
| Catalog snapshot | `queries_and_scripts/catalog_snapshot/` | Cisco-managed stock catalog API snapshot | Refresh from Orbital API; sync to GitHub | Full offline stock catalog data used for query/script selection decisions. |
| Custom queries | `queries_and_scripts/custom_queries/` | User-owned personal repository content | Editable only when the user explicitly asks to store or update a custom query | Personal collection of custom Orbital SQL queries that the user intentionally chose to keep. |
| Custom scripts | `queries_and_scripts/custom_scripts/` | User-owned personal repository content | Editable only when intentionally updating personal GitHub work | Personal collection of custom Orbital Python scripts generated manually, with Codex, or with other tools. |

## Working Rule

Catalog folders are source snapshots and templates. Do not adapt files in place. Copy or reference catalog material in a temporary/local working area before modifying it.

Custom folders are the user's personal repository content. They can contain work generated manually, with Codex, with VS Code, or with other tools only after the user explicitly chooses to store that work there. Modify them only when the task is explicitly to update the personal query/script repository.

Generated experiments, draft adaptations, validation queries, lab-specific queries, host-specific queries, and investigation-specific queries are temporary by default. Do not store them in GitHub-tracked folders unless the user explicitly asks to store a specific artifact. Prefer chat-only output, direct helper input, or local-only scratch paths.

Finished reusable query and script work belongs in `queries_and_scripts/custom_queries/` or `queries_and_scripts/custom_scripts/` only when the user explicitly wants it promoted into the personal custom repository. Finished context, memory, profiles, and notes belong in their dedicated project folders rather than a generic output folder.

## Catalog Snapshot Reason

The catalog source folders preserve useful catalog entries locally so Codex and other tools can reuse them as templates without requiring constant catalog refreshes.

`queries_and_scripts/catalog_snapshot/` stores the full offline Cisco-managed stock catalog JSON used for decision support. Refresh it from the Orbital API when freshness matters.

Organization catalog exports do not belong in `queries_and_scripts/catalog_snapshot/` because they may contain tenant-specific content. Keep them local-only under `local/orbital-catalog-api-cache/`.

## Cross-Reference Rule

When a query or script is created from a catalog source, preserve the catalog `Name` and `ID` where known.

When a query or script is created as custom user work, document whether it came from:

- a catalog template,
- another custom file,
- generated SQL or Python,
- external tool output,
- manual editing.

This distinction matters because catalog entries are source/template material, while custom entries are the user's personal reusable repository.
