# Orbital Project Workspace

This repository is a working knowledge base and source workspace for Cisco Orbital
queries, scripts, catalog/API research, and reusable Codex skills.

The project is not only a collection of SQL snippets. It now contains:

- Orbital product, query, script, catalog, API, and target-selector context.
- Source copies of Cisco-managed catalog queries/scripts and user-owned custom work.
- Reusable query-method memory that explains when to use which query.
- Reusable query-method memory for Secure Endpoint, Secure Client, Orbital
  health, networking, catalog validation, and endpoint inventory.
- Local helper scripts for Orbital API authentication, catalog import, query
  execution, and catalog validation.
- Codex skill working copies for Orbital API access, query-method memory, live or
  scheduled osquery execution, and catalog update work.

## Continuous Improvement Model

The project is designed to improve query quality and investigation speed over time.

Each useful query, script, catalog comparison, endpoint investigation, context import, and analyst correction should improve future work when it produces reusable knowledge. Store that reusable knowledge as sanitized project context, product context, query-method memory, catalog result profiles, notes, or skills.

The repository should contain enough GitHub-synced memory, knowledge, context, and reusable skills that a new Codex workspace can import the repo and immediately benefit from prior outcomes.

Do not sync raw endpoint evidence. The reusable outcome is the method: what question was asked, which table/query/script pattern helped, when it applies, what assumptions or caveats matter, and how to interpret the result shape safely.

## Start Here

For Codex or human review, read these files first:

- `INSTALL.md`: how to install the full project from GitHub in a new Codex
  workspace. Use this before installing skills.
- `AGENTS.md`: project-specific rules and terminology.
- `project-context/README.md`: index of durable Orbital context files.
- `project-context/Orbital_Query_Catalog_Source_Map.md`: how to combine
  osquery schema, Orbital Catalog API, and authenticated UI context.
- `project-context/Orbital_Target_Node_Selectors.md`: target/device/endpoint
  terminology and API `nodes` selector rules.
- `project-context/Orbital_Source_Repository_Model.md`: source ownership model
  for catalog templates versus user-owned custom query/script repository files.
- `tools-and-memory/query-method-memory/README.md`: reusable query-method memory.
- `product-context/Cisco_Secure_Client_Endpoint_Context.md`:
  Secure Client / Secure Endpoint investigation context.

## Directory Map

- `project-context/`: durable project context, source maps, terminology, API
  notes, catalog notes, target selector notes, and osquery schema summaries.
- `queries_and_scripts/catalog_queries/`: Cisco-managed catalog
  query source snapshots/templates. Do not edit in place.
- `queries_and_scripts/catalog_scripts/`: Cisco-managed catalog
  script source snapshots/templates. Do not edit in place.
- `queries_and_scripts/catalog_snapshot/`: full offline Cisco-managed stock
  catalog JSON snapshot used for query/script decision support and periodic
  refreshes.
- `queries_and_scripts/catalog_result_profiles/`: GitHub-synced sanitized
  catalog result profiles used to explain expected query outcomes, row-count
  behavior, returned columns, no-response handling, caveats, and
  incident-responder assumptions. The `windows/` subfolder contains one
  analyst-facing Markdown file per Windows stock Catalog ID.
- `queries_and_scripts/Generated_Queries/`: generated SQL/JSON query artifacts.
  Existing tracked files are retained for project continuity; new generated
  scratch files are ignored by default unless explicitly promoted.
- `queries_and_scripts/draft_queries/`: draft, test, validation, adapted, and
  investigation-specific query files that are not yet promoted to custom query
  work.
- `queries_and_scripts/draft_scripts/`: draft, test, validation, adapted, and
  investigation-specific script files that are not yet promoted to custom script
  work.
- `queries_and_scripts/custom_queries/`: user-owned custom query
  repository content. Store a query here only when the user explicitly asks to
  save that query as a custom query.
- `queries_and_scripts/custom_scripts/`: user-owned custom script
  repository content. Edit only when intentionally updating personal custom work.
- `tools-and-memory/`: legacy working area for active helpers, project skills,
  query-method memory, and investigation support files. Query and script files
  should live under `queries_and_scripts/`.
- Generated query artifacts are temporary by default. Do not add new generated
  SQL/JSON files to GitHub unless the user explicitly asks to promote a specific
  query into `queries_and_scripts/custom_queries/`.
- `product-context/`: product-specific investigation context,
  currently focused on Cisco Secure Client and Cisco Secure Endpoint.
- `tools-and-memory/query-method-memory/`: reusable query-method memory. These records
  store query design and lessons, not endpoint result rows.
- `skills/`: installable Orbital Codex skills for use from GitHub.
- `notes-and-memory/`: decision logs, learning notes, and query-memory summaries.
- `local/orbital-catalog-api-cache/`: ignored local raw Orbital catalog API
  cache, including organization catalog exports that must not be committed.
- `local/`, `.codex/`, `tmp/`, `.tmp/`, SQLite files, and real credential files:
  local runtime state only. Do not commit.

## Local Logs

Local traceability that should be visible to future Codex work but not synced to
GitHub lives under `local/`.

Use `local/project-change-log.md` for durable project-scope changes:

- File and folder structure changes.
- Scope changes.
- Main behavior changes.
- Durable project rules.
- Project/product context changes.
- Notes, memory model, skill, or helper-script changes that affect how the
  project is used.

Use `local/sync-activity-log.md` for useful operational traceability:

- GitHub push/pull runs when the result or issue is worth remembering.
- Workspace skill to global skill syncs.
- Skill installation or update events.
- Authentication, permission, or sync troubleshooting notes.
- Dates when a skill was synced.

Do not store credentials, endpoint results, tenant data, raw API responses,
hostnames, IP addresses, GUIDs, or customer-identifying values in either log.
Both files are local-only and must not be staged or pushed.

After writing a local log entry, check whether it contains a reusable lesson.
If yes, promote the sanitized lesson into the GitHub-synced project memory:

- `notes-and-memory/decisions/` for durable decisions.
- `tools-and-memory/query-method-memory/` for reusable query methods.
- `project-context/` or `product-context/` for durable context.
- `queries_and_scripts/catalog_result_profiles/` for catalog result
  interpretation.
- `skills/` for reusable workflow behavior.

Local logs explain what happened in this workspace. GitHub-synced memory
explains what future imported workspaces should learn from it.

## Query-Method Memory

Query-method memory lives under `tools-and-memory/query-method-memory/`.

It is used to answer: "Which Orbital query should I use now?"

This memory is the main mechanism for improving quality and speed as more endpoint work is performed. After useful query design, endpoint testing, catalog validation, result interpretation, or analyst feedback, update memory only with reusable and sanitized lessons. Never store raw endpoint rows or identifying values.

Method records may store:

- Investigation intent and sanitized input patterns.
- Query goal, when to use it, and when not to use it.
- Tables, columns, joins, SQL patterns, and platform assumptions.
- Orbital Catalog `Name` and `ID` context.
- Targeting guidance, query type, `allowOS`, and broad-targeting cautions.
- Validation status and lessons learned.

Method records must not store endpoint result rows, hostnames, usernames, IP
addresses, GUIDs, tenant names, bearer tokens, client secrets, raw API responses,
or raw investigation output.

## Orbital Query Work

Orbital queries use SQL syntax and osquery tables to inspect endpoint state. Before
finalizing query work:

- Validate table and column names against
  `product-context/osquery/osquery_schema_5_23_0.json`.
- Check Orbital-specific availability, catalog examples, and platform assumptions.
- Decide whether the query should be a catalog query, live/custom query, or
  scheduled query.
- Use explicit target selectors in the API `nodes` array.
- Use broad selectors such as `all` only with caution and explicit scope.
- Use `allowOS` or OS selector guidance for platform-specific queries.
- Preserve the distinction between Catalog `ID`, Orbital endpoint ID, Secure
  Endpoint GUID, Secure Client GUID, AnyConnect UDID, `queryId:<id>`, and
  `orbital_queryID` / Job ID.
- Do not persist generated SQL by default. Keep generated queries in chat, pass
  them directly to helper scripts, or use local-only scratch files. Store a query
  in `queries_and_scripts/custom_queries/` only when explicitly asked to save it
  as a custom query.

For host-targeted API investigations, this project prefers scheduled one-shot
queries with a short expiry so Orbital returns a Job ID for follow-up through
`/v0/jobs/{id}` and `/v0/jobs/{id}/results`.

Default query interaction should stay compact but traceable. Codex should still
use the full project capability stack internally: project/product context,
query-method memory, catalog snapshots, catalog result profiles, osquery schema
validation, target-safety checks, and relevant skills. The visible answer should
show what happened: target selector, query purpose, execution mode, SQL summary
or exact SQL when it affects approval/safety, Job ID/status, answered endpoint
count, row count, compact result summary, key caveats, and whether
memory/context should be updated. Full row tables, raw helper output, long
reasoning, and detailed source traces should be shown only when needed for
approval, troubleshooting, safety, or when requested.

## Orbital Script Work

Orbital scripts run in an independent Python runtime on endpoints. Keep scripts
safe, explicit, and platform-aware.

Key script constraints:

- Python 3.10 or later in the Orbital endpoint runtime.
- 64 KB script size limit.
- 10 minute execution timeout.
- 16 MB stdout cap and 16 MB stderr cap.
- Customer exit codes should be `0` through `199`; `200` and higher are reserved
  by Orbital.
- Devices run only one script at a time.
- Ad hoc scripts sent to a busy node can be ignored; scheduled scripts are queued.

## Orbital API And Catalog Data

Use `project-context/Orbital_API_DevNet.md` as the project API entry point.
Verify individual API operation pages before implementing request bodies, response
handling, server region, or authentication.

Catalog context comes from three source types:

- Upstream osquery schema for table and column structure.
- Orbital Catalog API data, including `/v0/stock`.
- Authenticated Orbital UI context for labels, filters, route behavior, and
  user-facing terminology.

Use `project-context/Orbital_Query_Catalog_Source_Map.md` when comparing these
sources. Preserve catalog `Name` and `ID` exactly.

## Credentials

Use the global Codex credential mapping by default. Orbital helpers read the
active mapping from:

```text
~/.codex/state/cisco-security-api-access/current_org_mapping.json
```

The mapping points to a global credential env file through `source_env_file`.
That global file is the preferred source for Orbital bearer tokens or OAuth
client credentials. Use `ORBITAL_ENV_FILE=/absolute/path/to/credential.env` or a
helper `--env-file` argument only as an explicit override.

`tools-and-memory/orbital_credentials.env` is legacy fallback only. Avoid using
it for normal workflows.

Never commit bearer tokens, client IDs, client secrets, raw API responses with
tenant data, or local runtime state.

Supported credential fields include:

- `ORBITAL_REGION=eu|na|us|apjc` or `SECURE_ENDPOINT_REGION`
- `ORBITAL_API_TOKEN`, `SECURE_ENDPOINT_BEARER_TOKEN`, `AMP_BEARER_TOKEN`, or `BEARER_TOKEN`
- `ORBITAL_CLIENT_ID` plus `ORBITAL_CLIENT_SECRET`
- `SECURE_ENDPOINT_V3_OAUTH_CLIENT_ID` plus `SECURE_ENDPOINT_V3_OAUTH_CLIENT_SECRET`
- `ORBITAL_TOKEN_URL` or `SECURE_ENDPOINT_V3_VISIBILITY_TOKEN_URL`

## Local Helpers

Useful helper files in the project:

- `check_orbital_api_auth.py`: validate Orbital API authentication.
- `import_orbital_catalog.py`: import or refresh Orbital catalog data.
- `generate_catalog_result_profiles.py`: regenerate sanitized GitHub-synced
  catalog result profiles from local validation output.
- `run_orbital_catalog_import.sh`: wrapper for catalog import.
- `run_windows_catalog_query_validation.py`: validate Windows catalog query
  assumptions.
- `skills/orbital-run-osquery-live-query/scripts/run_live_query.py`: run
  host-targeted scheduled queries or explicit live queries and record operational
  Job ID metadata locally.

Operational run metadata is local-only and should stay under `local/`.

## Current Investigation Focus

Current reusable work is strongest around:

- Cisco Secure Endpoint and Cisco Secure Client inventory.
- Secure Endpoint Host Based Firewall event analysis.
- Secure Endpoint Exploit Prevention protected-process checks.
- Secure Client module detection, including NVM/EVM/Cloud Management context.
- Orbital health and endpoint OS/computer-name inventory.
- Network evidence such as DNS cache, hosts file entries, current sockets, and
  Cisco/cloud connectivity troubleshooting.
- Orbital catalog validation, result explanation profiles, and multi-SQL
  catalog/API request structure.

## SQL Result Helpers

Common SQL snippets used in Orbital query output shaping:

```sql
datetime(table_column_name, 'unixepoch', 'UTC')
round((table_column_name / 1024 / 1024), 0) AS displayed_column_name
select substr(table_column_name, 42, 10)
case table_column_name when 'bs.json' then 'CM config exists' when 'cm_config.json' then 'CM config exists' end
order by "Cloud Management Config" ASC
where hostnames not in ('localhost', '::1', 'fe00::0', 'ff00::0', 'ff02::1', 'ff02::2')
JSON_EXTRACT(json(data), '$.EventData.LocalPort') AS source_port
SPLIT(message, ',', 1) AS protocol
```

## Secure Client Uninstall Note

One historical workflow in this repository is uninstalling Cisco Secure Client
with Orbital scripts:

1. Query installed files or installed products first.
2. Execute the predefined script pattern for a PowerShell cmdlet.
3. Example uninstall command:

```powershell
wmic product where "name like 'Cisco Secure Client%'" call uninstall
```

Prefer current product-specific guidance and validate the installed product names
before using this workflow.

![Secure Client uninstall script example](https://github.com/user-attachments/assets/dffa6baa-818b-483d-b185-c59ced880086)

## Git And Sync Notes

Before syncing to GitHub:

- Review `git status --short`.
- Exclude real credentials, local runtime state, `.DS_Store`, local SQLite files,
  raw tenant snapshots, and generated endpoint result data.
- Commit reusable method/context/source changes only after checking privacy rules.
- Sync global Codex skills only when workspace skill folders with `SKILL.md`
  differ from their global copies.

## Install In A New Codex Workspace

Use `INSTALL.md` for the full onboarding flow.

The correct model is:

1. Clone or open this GitHub repository as the active Codex workspace.
2. Install the project skills from `skills/`.

Installing only the skills is insufficient because the skills depend on the
GitHub-synced repository content for project context, product context,
query-method memory, catalog snapshots, catalog result profiles, helper scripts,
and decision records.
