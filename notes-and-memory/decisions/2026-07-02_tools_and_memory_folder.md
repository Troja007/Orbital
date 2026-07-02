# 2026-07-02 Tools And Memory Folder

## Decision

Rename the legacy `02_Working_Files/` folder to `tools-and-memory/`.

Use this folder for active helper tools, operational utility scripts, query-method memory, experiments, and investigation support files.

## Reason

The folder no longer stores general query/script source files. The name `tools-and-memory` reflects its current purpose better than a numbered working-files folder because memory creation is a main project outcome, not a side effect.

## Boundaries

- Query and script files with any status belong under `queries_and_scripts/`.
- Raw local credentials may exist under `tools-and-memory/` but must remain ignored.
- Query-method memory may remain under `tools-and-memory/query-method-memory/` until the memory layer grows enough to justify a root-level durable knowledge folder.

## References

- `tools-and-memory/README.md`
- `README.md`
- `.gitignore`
- Git commit `9bc11cc` (`Rename working files to tools and memory`)

## Open Risks Or Follow-Up

- Re-evaluate whether `query-method-memory/` should move to the repository root if it becomes more central than the helper tools.
