# GitHub Repository

Repository: https://github.com/Troja007/Orbital

Purpose: Top-level Codex and VS Code workspace repository for Cisco Orbital queries, scripts, catalog templates, API references, and project notes.

Local project root: `_Codex_Orbital`

Orbital query/script source folder: `queries_and_scripts`

Default branch: `main`

Remote:

```text
origin https://github.com/Troja007/Orbital.git
```

Use this repository as the full project workspace. Before relying on source-folder content, check the file content date, filename date when present, and Git commit context if relevant.

Catalog folders:

- `queries_and_scripts/catalog_queries` is a 1:1 copy from the Orbital product catalog.
- `queries_and_scripts/catalog_scripts` is a 1:1 copy from the Orbital product catalog.

Do not edit these catalog folders directly. Use them as source files and copy items into `tools-and-memory` before making changes.

Personal work folders:

- `queries_and_scripts/custom_queries` contains the user's personal Orbital query work.
- `queries_and_scripts/custom_scripts` contains the user's personal Orbital script work.

These folders are maintained through VS Code and GitHub as part of the top-level project repository. Treat them as user-owned source material unless the user explicitly asks to update them.

Use `Orbital_Source_Repository_Model.md` for the current source ownership model. Catalog folders are stable read-only source snapshots/templates; custom folders are the user's personal reusable query/script repository.
