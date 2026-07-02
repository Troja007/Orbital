# 2026-07-02 osquery Schema Source Snapshots

## Decision

Store upstream osquery schema snapshots under `product-context/osquery/` as refreshable, versioned source snapshots.

## Reason

Orbital queries are based on osquery. The schema snapshots provide table and column validation context for query design and review. Keeping versioned snapshots in product context makes the source explicit and GitHub-synced for future Codex workspaces.

## Boundaries

- The upstream osquery schema is not a guarantee that every table is available in Orbital.
- Orbital can add, remove, disable, or modify table behavior by endpoint, platform, or product version.
- A new Orbital catalog snapshot and a new upstream osquery schema version are related but separate update signals.

## References

- `product-context/osquery/README.md`
- `product-context/osquery/osquery_schema_5_23_0.json`
- `product-context/osquery/osquery_schema_5_23_0_table_index.json`
- `project-context/Osquery_Schema_5_23_0.md`
- Git commit `035ebb4` (`Move osquery schema to product context`)

## Open Risks Or Follow-Up

- Add newer schema versions with versioned filenames rather than overwriting older snapshots.
- Update cross-references and skills when the active schema validation reference changes.
