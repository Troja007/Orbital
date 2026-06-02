# Orbital Project Guidance

This project is for working on Cisco Orbital queries and scripts.

Orbital queries use SQL syntax and osquery tables to inspect endpoint information. Verify table names, columns, platform assumptions, and expected result shape before finalizing query work.

For Orbital query work, account for query type and targeting behavior. Custom queries, also called live queries or probes, run immediately and return immediate results. Scheduled queries run over a defined time window and frequency. Query prefixes control target devices and can be special, dynamic, or static. Use the `all` prefix with caution because broad targeting can affect endpoint performance. Check whether `allowos` or an operating system filter is required for platform-specific queries.

For Orbital target selection terminology, use `00_Project_Context/Orbital_Target_Node_Selectors.md`. Customer-facing wording may say targets, devices, endpoints, or hosts, while the Query API uses `nodes` and the `Specifying Nodes` section. In API request bodies, target selectors belong in the `nodes` array. Preserve the distinction between endpoint selector IDs, Catalog `ID`, Orbital ID, Secure Endpoint computer GUID, Secure Client computer GUID, AnyConnect UDID, and `queryId`.

For osquery table and column lookup, use `01_Source_Files/API_References/osquery_schema_5_23_0.json` as the upstream osquery 5.23.0 schema reference. Orbital is based on osquery but can include additional capabilities, disabled tables, or platform-specific differences; verify Orbital availability before treating an upstream osquery table as usable in Orbital.

For query catalog analysis, link three sources: upstream osquery schema for table/column structure, Orbital Catalog API for programmatic catalog data such as `/v0/stock`, and authenticated Orbital UI analysis for Cisco-managed query metadata and user-facing terms. Use `00_Project_Context/Orbital_Query_Catalog_Source_Map.md` as the cross-reference.

Orbital scripts run in an independent Python environment on endpoints and can be used as response actions. Treat scripts as endpoint automation: keep changes safe, idempotent where possible, explicit about output, and aware of platform differences.

For Orbital script work, account for endpoint execution behavior. Devices run only one script at a time. Ad hoc scripts sent to a busy node are ignored with a busy message; scheduled scripts are queued. If scripting is disabled, running scripts finish, but no new scripts can run and pending scheduled scripts are canceled. Scripts can be linked to existing queries and then act only on devices matching the linked query criteria.

For Python script work, account for the Orbital endpoint runtime: Python 3.10 or later, independent from other endpoint Python installations, 64 KB script size limit, 10 minute execution timeout, 16 MB stdout cap, and 16 MB stderr cap. Use customer exit codes in the range `0` to `199`; codes `200` and higher are reserved by Orbital.

For Orbital API work, use `00_Project_Context/Orbital_API_DevNet.md` as the project API entry point. Verify individual API operation pages before implementing request bodies, response handling, server region, or authentication. Never store bearer tokens or API credentials in the project files.

When adding new project context, check whether cross-references need to be created or updated. Generate or update a cross-reference when the new context changes terminology, API fields, identifiers, source priority, folder ownership, catalog mapping, target selection, query behavior, script behavior, or links between UI, API, catalog, osquery, and local source files.

When generating context from chat messages or the user's personal input, check whether the user may be using a project term in the wrong or ambiguous context. If a term could reasonably refer to multiple project concepts, or could conflict with established Orbital terminology, ask for clarification before executing commands, editing files, generating context, or encoding the assumption in project artifacts.

When creating reusable project assets, keep names generic unless the user explicitly requests a specific name. This applies to generated skills, tools, scripts, helper modules, templates, folders, documentation sections, and any similar reusable artifacts. Prefer names that describe the capability or workflow rather than names tied to a single customer, incident, one-off task, person, or temporary context.

Use existing Orbital catalog templates where available before creating new queries or scripts from scratch. The Orbital Catalog includes stock queries and scripts created by the Orbital team and Cisco Talos, plus custom user-created queries and scripts. Preserve and document any fields that affect the product UI.

The Orbital Catalog is available through both the authenticated product UI and the Orbital API. Use UI context for user-facing labels, filters, table columns, detail drawers, and route behavior. Use API context for automation, schemas, and programmatic catalog access. When comparing the two, map both `Name` and `ID`.

For Orbital Catalog UI terminology, use `00_Project_Context/Orbital_Catalog_UI_Terms.md`. Treat `ID` as the product/catalog reference key for a query or script. Preserve catalog IDs exactly, including prefixes such as `org:`, and record both `Name` and `ID` when documenting catalog entries.

The folders `01_Source_Files/Orbital_Repo_Source/Catalog_queries` and `01_Source_Files/Orbital_Repo_Source/Catalog_scripts` are 1:1 copies from the Orbital product catalog. Treat them as read-only source material. Do not edit these files directly; copy catalog material into `02_Working_Files` before adapting it.

The folders `01_Source_Files/Orbital_Repo_Source/custom_queries` and `01_Source_Files/Orbital_Repo_Source/custom_scripts` contain the user's personal Orbital work maintained through VS Code and GitHub. Treat them as user-owned source material. Do not modify them unless the user explicitly asks to update the GitHub-tracked work.

When using files as sources, prefer explicit content dates or validity dates over upload or modification dates. If source freshness conflicts and cannot be resolved, state the conflict.
