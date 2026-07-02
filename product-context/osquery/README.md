# osquery Schema Source Snapshot

This folder stores Git-tracked upstream osquery schema snapshots used for Orbital query work.

Current snapshot:

- Source: https://osquery.io/schema/5.23.0/
- Source type: upstream osquery schema webpage
- Retrieved: 2026-06-02
- Schema version: 5.23.0
- Full schema: `osquery_schema_5_23_0.json`
- Compact index: `osquery_schema_5_23_0_table_index.json`

Update policy:

- Treat these files as refreshable source snapshots, not generated query output.
- Refresh when the upstream osquery schema version changes.
- Review after Orbital catalog refreshes, especially when new or changed catalog queries reference unknown tables or columns.
- Keep versioned filenames when adding a newer osquery schema version. Do not overwrite an older version until dependent references and skills have been reviewed.
- After adding a new schema version, update project cross-references, skills, and `project-context/Osquery_Schema_5_23_0.md` or create a new version-specific context file.

Important distinction:

- The osquery schema defines upstream table and column structure.
- The Orbital catalog shows how Cisco-managed queries use osquery and Orbital-specific capabilities.
- A new Orbital catalog snapshot can require review even when the upstream osquery schema version has not changed.
- A new upstream osquery schema version can add or change tables that are not automatically available in Orbital.
