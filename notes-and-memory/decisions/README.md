# Decision Log

Store decisions that affect query/script behavior, source selection, catalog template reuse, API assumptions, or endpoint safety.

This folder is GitHub-synced project memory. It exists so a new Codex workspace importing the repository can understand why the project is structured this way and continue from prior decisions instead of rediscovering them.

Update this decision log when a durable choice changes:

- project scope or behavior
- folder ownership
- query/script source handling
- memory model
- GitHub sharing boundary
- API/catalog/source-of-truth assumptions
- skill responsibility boundaries
- endpoint safety or privacy rules

Do not add routine GitHub sync activity here. Store operational sync notes in `local/sync-activity-log.md`.

Recommended entry format:

- Date
- Decision
- Reason
- Source files or references used
- Open risks or follow-up items

## Current Decisions

| Date | Decision | File |
| --- | --- | --- |
| 2026-06-10 | Keep Orbital skills separated by workflow responsibility. | `2026-06-10_skill_separation.md` |
| 2026-07-02 | Treat the repository as a GitHub-synced continuous improvement system. | `2026-07-02_continuous_improvement_model.md` |
| 2026-07-02 | Keep reusable memory/context in GitHub but keep raw endpoint evidence local-only. | `2026-07-02_github_memory_boundary.md` |
| 2026-07-02 | Keep all query and script files under `queries_and_scripts/`, separated by source and status. | `2026-07-02_query_script_source_model.md` |
| 2026-07-02 | Use `tools-and-memory/` for helper tools and query-method memory. | `2026-07-02_tools_and_memory_folder.md` |
| 2026-07-02 | Use `query-method-memory` as the reusable method knowledge store. | `2026-07-02_query_method_memory_boundary.md` |
| 2026-07-02 | Store the offline stock catalog snapshot and catalog result profiles in GitHub as sanitized reusable context. | `2026-07-02_catalog_snapshot_and_result_profiles.md` |
| 2026-07-02 | Store upstream osquery schema snapshots under product context as refreshable source snapshots. | `2026-07-02_osquery_schema_source_snapshots.md` |
