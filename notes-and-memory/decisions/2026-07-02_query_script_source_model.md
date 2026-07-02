# 2026-07-02 Query And Script Source Model

## Decision

All query and script files with any status should live under `queries_and_scripts/`.

Use source/status-specific folders:

- `catalog_queries/`: Cisco-managed catalog query source snapshots.
- `catalog_scripts/`: Cisco-managed catalog script source snapshots.
- `catalog_snapshot/`: offline stock catalog JSON snapshots.
- `catalog_result_profiles/`: sanitized catalog result interpretation profiles.
- `Generated_Queries/`: retained generated SQL/JSON artifacts; new scratch files are ignored by default.
- `draft_queries/`: draft, test, validation, adapted, or investigation-specific query files.
- `draft_scripts/`: draft, test, validation, adapted, or investigation-specific script files.
- `custom_queries/`: user-owned reusable custom query work.
- `custom_scripts/`: user-owned reusable custom script work.

## Reason

Keeping all query/script material under one source root makes the repository easier to navigate and prevents legacy working folders from becoming hidden source locations.

Separating catalog, draft, generated, and custom material prevents accidental editing of catalog sources and prevents temporary work from being mistaken for reusable personal custom work.

## References

- `queries_and_scripts/README.md`
- `project-context/Orbital_Source_Repository_Model.md`
- `AGENTS.md`
- `README.md`

## Open Risks Or Follow-Up

- Consider normalizing `Generated_Queries/` to lowercase in a future naming cleanup.
