# Orbital Project Guidance

This project is for working on Cisco Orbital queries and scripts.

Orbital queries use SQL syntax and osquery tables to inspect endpoint information. Verify table names, columns, platform assumptions, and expected result shape before finalizing query work.

For Orbital query work, account for query type and targeting behavior. Custom queries, also called live queries or probes, run immediately and return immediate results. Scheduled queries run over a defined time window and frequency. Query prefixes control target devices and can be special, dynamic, or static. Use the `all` prefix with caution because broad targeting can affect endpoint performance. Check whether `allowos` or an operating system filter is required for platform-specific queries.

Orbital scripts run in an independent Python environment on endpoints and can be used as response actions. Treat scripts as endpoint automation: keep changes safe, idempotent where possible, explicit about output, and aware of platform differences.

For Orbital script work, account for endpoint execution behavior. Devices run only one script at a time. Ad hoc scripts sent to a busy node are ignored with a busy message; scheduled scripts are queued. If scripting is disabled, running scripts finish, but no new scripts can run and pending scheduled scripts are canceled. Scripts can be linked to existing queries and then act only on devices matching the linked query criteria.

For Python script work, account for the Orbital endpoint runtime: Python 3.10 or later, independent from other endpoint Python installations, 64 KB script size limit, 10 minute execution timeout, 16 MB stdout cap, and 16 MB stderr cap. Use customer exit codes in the range `0` to `199`; codes `200` and higher are reserved by Orbital.

For Orbital API work, use `00_Project_Context/Orbital_API_DevNet.md` as the project API entry point. Verify individual API operation pages before implementing request bodies, response handling, server region, or authentication. Never store bearer tokens or API credentials in the project files.

Use existing Orbital catalog templates where available before creating new queries or scripts from scratch. The Orbital Catalog includes stock queries and scripts created by the Orbital team and Cisco Talos, plus custom user-created queries and scripts. Preserve and document any fields that affect the product UI.

The folders `01_Source_Files/Orbital_Repo_Source/Catalog_queries` and `01_Source_Files/Orbital_Repo_Source/Catalog_scripts` are 1:1 copies from the Orbital product catalog. Treat them as read-only source material. Do not edit these files directly; copy catalog material into `02_Working_Files` before adapting it.

The folders `01_Source_Files/Orbital_Repo_Source/custom_queries` and `01_Source_Files/Orbital_Repo_Source/custom_scripts` contain the user's personal Orbital work maintained through VS Code and GitHub. Treat them as user-owned source material. Do not modify them unless the user explicitly asks to update the GitHub-tracked work.

When using files as sources, prefer explicit content dates or validity dates over upload or modification dates. If source freshness conflicts and cannot be resolved, state the conflict.
