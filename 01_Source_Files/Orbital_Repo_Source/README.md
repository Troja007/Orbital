# Orbital
SQL queries for Orbital

This is a summary of SQL queries and scripts, which can be used with Orbital. 
- It includes customized SQL queries to tweak result output. Learn more about SQL under: https://www.w3schools.com/sql/
- it includes some custom scripts i collected and generated over time.

## Transform result data
- datetime(table_column_name, "unixepoch", "UTC")
- round((table_column_name / 1024 / 1024) ,0) AS "diplayed_column_name”
- select substr (table_column_name,42,10)
- case table_column_name when 'bs.json' then 'CM config exists’when 'cm_config.json' then 'CM config exists’
- order by "Cloud Management Config" ASC
- where hostnames not in ("localhost", "::1", "fe00::0", "ff00::0", "ff02::1", "ff02::2")
- JSON_EXTRACT(json(data), '$.EventData.LocalPort') AS "source-port",
- SPLIT(message, ',', 1) AS protocol,


## Uninstall Secure Client with scripts
- do a query to search for installed files
- execute the predefined script: Execute Powershell cmdlet:
-- add the following string to uninstall e.g. Secure Client: wmic product where "name like 'Cisco Secure Client%'" call uninstall

  ![image](https://github.com/user-attachments/assets/dffa6baa-818b-483d-b185-c59ced880086)

## Codex Project

This folder is also intended to be usable as source material for a Codex workspace around Cisco Orbital query and script work.

Codex can use this folder to understand and reuse:

- custom Orbital SQL queries in `custom_queries`
- custom Orbital Python scripts in `custom_scripts`
- catalog query examples in `Catalog_queries`
- catalog script examples in `Catalog_scripts`
- project notes and usage context documented in this README

### Recommended Codex Workflow

1. Clone or pull this repository locally.
2. Open the local repository or the parent Codex workspace folder in Codex.
3. Ask Codex to use the files in this repository as source material.
4. Copy source examples into a working area before adapting them.
5. Keep finished or reusable outputs separate from original source examples.

### Handling Rules for Codex

- Treat `Catalog_queries` and `Catalog_scripts` as read-only catalog source material.
- Do not modify `custom_queries` or `custom_scripts` unless the GitHub-tracked work should intentionally change.
- For Orbital SQL queries, verify osquery table names, column names, platform assumptions, expected result shape, query type, targeting behavior, and whether `allowos` or an operating system filter is required.
- Use broad target prefixes such as `all` carefully because broad live queries can affect endpoint performance.
- For Orbital scripts, keep changes safe, explicit, idempotent where possible, and aware of platform differences.
- Do not store bearer tokens, API credentials, or customer-specific secrets in this repository.

### Codex Workspace Structure

In the top-level Codex project, this folder is used as `01_Source_Files/Orbital_Repo_Source` inside this workspace structure:

| Folder | Purpose |
| --- | --- |
| `00_Project_Context` | Product notes, API context, assumptions, and source indexes. |
| `01_Source_Files` | Original or exported source material. |
| `02_Working_Files` | Drafts, adapted templates, experiments, and helper scripts. |
| `03_Outputs` | Finished queries, scripts, reports, or reusable deliverables. |
| `04_Notes` | Decision logs and learning notes. |
| `AGENTS.md` | Codex instructions for Orbital-specific work. |

The parent Codex workspace includes additional context files and `AGENTS.md`. This folder remains the source area for Orbital queries and scripts.
