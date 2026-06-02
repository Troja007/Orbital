# Orbital
SQL queries for Orbital

This is a summary of SQL queries and scripts, which can be used with Orbital.
- It includes customized SQL queries to tweak result output. Learn more about SQL under: https://www.w3schools.com/sql/
- it includes some custom scripts i collected and generated over time.

## Transform result data
- datetime(table_column_name, "unixepoch", "UTC")
- round((table_column_name / 1024 / 1024) ,0) AS "diplayed_column_name"
- select substr (table_column_name,42,10)
- case table_column_name when 'bs.json' then 'CM config exists' when 'cm_config.json' then 'CM config exists'
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

This repository is structured as a Codex-ready workspace for Cisco Orbital query, script, catalog, and API work.

Codex should use:

- `AGENTS.md` for project-specific instructions
- `00_Project_Context` for Orbital product, query, script, catalog, and API notes
- `01_Source_Files/Orbital_Repo_Source` for source query and script material
- `02_Working_Files` for drafts, adapted templates, experiments, and helper scripts
- `03_Outputs` for finished reusable queries, scripts, and reports
- `04_Notes` for decision logs and learning notes

### Recommended Codex Workflow

1. Clone or pull this repository locally.
2. Open the repository folder in Codex or VS Code.
3. Start with `AGENTS.md` and `00_Project_Context/README.md`.
4. Copy source examples into `02_Working_Files` before adapting them.
5. Keep finished or reusable outputs under `03_Outputs`.

### Handling Rules for Codex

- Treat `01_Source_Files/Orbital_Repo_Source/Catalog_queries` and `01_Source_Files/Orbital_Repo_Source/Catalog_scripts` as read-only catalog source material.
- Do not modify `01_Source_Files/Orbital_Repo_Source/custom_queries` or `01_Source_Files/Orbital_Repo_Source/custom_scripts` unless the GitHub-tracked source work should intentionally change.
- For Orbital SQL queries, verify osquery table names, column names, platform assumptions, expected result shape, query type, targeting behavior, and whether `allowos` or an operating system filter is required.
- Use broad target prefixes such as `all` carefully because broad live queries can affect endpoint performance.
- For Orbital scripts, keep changes safe, explicit, idempotent where possible, and aware of platform differences.
- Do not store bearer tokens, API credentials, customer-specific secrets, local Codex runtime state, or generated tenant-specific API snapshots in this repository.

### Local Credentials

Use a local ignored credentials file when needed:

```bash
cp 02_Working_Files/orbital_credentials.env.example 02_Working_Files/orbital_credentials.env
```

Then edit `02_Working_Files/orbital_credentials.env` locally. The real `.env` file is ignored by Git.
