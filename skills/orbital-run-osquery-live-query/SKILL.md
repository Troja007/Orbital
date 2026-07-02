---
name: orbital-run-osquery-live-query
description: Run generic Cisco Orbital API queries with arbitrary osquery SQL against explicit target selectors. Use when Codex needs to validate osquery tables or columns from project context, check required inputs such as targets and SQL, execute host-targeted scheduled queries with POST /query for Job ID tracking, run live queries with POST /query/run when explicitly appropriate, use Orbital target/node selectors such as host, hostname, ip, ipv4, netmask, orb, amp, cm, machine, os, random, or queryId, parse query results, or present endpoint rows from any supported osquery table.
---

# Orbital Run osquery Query

Use this skill to run a Cisco Orbital query through the API against explicit target endpoints. The skill is generic: it can use any osquery table or SQL statement after validating the requested table/column assumptions against project context.

For host-targeted investigations, use a scheduled query with a 2-minute expiry by default. In this project, host queries are scheduled runs so Orbital returns a Job ID for follow-up through `/v0/jobs/{id}` and `/v0/jobs/{id}/results`. Use live mode only when the user explicitly asks for a live/immediate probe and accepts that the API may not expose a Job ID.

Use `orbital-api-access` for API connectivity tests, authentication troubleshooting, and catalog download/import work. Use `orbital-query-method-memory` to speed up query design by reusing prior query methods and catalog/osquery mappings. Keep these skills separated unless the user explicitly confirms a larger skill scope change.

## Project Change Log

After changing query helpers, skill instructions, reusable SQL artifacts, project context, query-memory files, or other durable project artifacts, append a sanitized entry to `local/project-change-log.md`. Do not use the project change log for routine sync activity.

Use `local/sync-activity-log.md` for useful operational sync traceability, such as GitHub sync issues, skill installation/update events, workspace-to-global skill sync dates, authentication problems, or permission troubleshooting. Both local logs must not be staged, committed, pushed, or contain endpoint results, hostnames, IP addresses, GUIDs, raw API responses, tenant data, credentials, or customer-identifying values.

## Required Inputs

Before executing anything, confirm these inputs are defined:

- Well-defined target selector: at least one explicit Orbital target selector, for example `host:EXAMPLE-HOST`, `ipv4:10.0.0.1`, `netmask:192.168.1.168/24`, `orb:<id>`, or `queryId:<id>`.
- SQL: either user-provided SQL or enough user intent to build SQL.
- Query purpose: a short label/name for the query.
- Region/credentials: project credentials through env vars or `02_Working_Files/orbital_credentials.env`.
- Network-enabled Codex runtime: before API calls, verify the current Codex shell is not running with `CODEX_SANDBOX_NETWORK_DISABLED=1`.

If the query target is not well-defined, stop before any API call and ask for clarification. Do not execute the query, run a preview, or infer a broader target while target scope is unclear.

If the user says "target", "device", "endpoint", "host", "node", "ID", or "GUID" ambiguously, ask for clarification before running the query. Do not guess between Catalog `ID`, Orbital endpoint ID, Secure Endpoint GUID, Secure Client GUID, AnyConnect UDID, `queryId`, or `orbital_queryID`.

Ambiguous scope words must also be clarified before execution. Do not infer between these meanings:

- "any endpoint", "any online endpoint", or "one endpoint" can mean `random:1` or can be casual wording for all endpoints. Ask which one unless the user explicitly says "random", "one", or supplies `random:<n>`.
- "every endpoint", "all endpoints", "all hosts", or "the whole fleet" means broad targeting such as `all`; show the target and require explicit confirmation before execution unless the same message clearly authorizes broad execution.
- "online endpoints" is not itself a precise Orbital selector. Ask whether the user wants a selector such as `all`, `random:<n>`, `os:<platform>`, or a known host/IP selector.
- If the user corrects a prior target interpretation, update future behavior and do not repeat the old interpretation.

Important ID distinction:

- `orbital_queryID`: the `ID` returned by `POST /v0/query/run`. It identifies the cloud-stored query/job and is used with `GET /v0/jobs/{{orbital_queryID}}` and `GET /v0/jobs/{{orbital_queryID}}/results`.
- `queryId:<id>`: a target selector in the `nodes` array that reuses an existing query definition. It is not the same as `orbital_queryID`.

Operational run ledger:

- Every future query submission must persist the returned `orbital_queryID` / Job ID before attempting result interpretation.
- When one analyst task requires multiple Orbital query submissions, assign one stable task name before the first submission and pass it to every helper call with `--task-name`. If a short stable identifier is useful, also pass `--task-id`. The run ledger must then allow the full set of query names and Job IDs for that task to be reconstructed.
- Host-targeted queries must be scheduled runs with 2-minute expiry unless the user explicitly requests live mode.
- The project helper writes query run metadata to `local/orbital_query_runs/live_query_runs.jsonl` by default. This path is ignored by git and is for operational follow-up only.
- The ledger may include task ID, task name, job ID, label, query name, target selectors, SQL hash, API status, and job/status check metadata.
- Do not store endpoint result rows in the ledger or method memory.
- If the API response does not expose a Job ID for a host-targeted scheduled query, record that fact in the ledger and report it as unexpected.
- For final answers after multi-query tasks, include a compact "Queries Run" summary with each query name/label, `orbital_queryID`, status/error outcome, and why that query was needed. This is operational metadata and may include Job IDs; do not include endpoint result rows in method memory.

## Project Context Checks

When inside this Orbital workspace, read these files as needed:

- `AGENTS.md` for project rules.
- `project-context/Orbital_Target_Node_Selectors.md` for target/node selector syntax.
- `project-context/Orbital_Queries.md` for live query, scheduled query, prefix, dynamic/static, and `allowOS` behavior.
- `project-context/Orbital_API_DevNet.md` for API endpoint and authentication context.
- `project-context/Osquery_Schema_5_23_0.md` and `01_Source_Files/API_References/osquery_schema_5_23_0.json` for table and column validation.
- `project-context/Orbital_Query_Catalog_Source_Map.md` when the query comes from a catalog item or should be compared with catalog/API/UI metadata.
- `project-context/Orbital_Windows_Catalog_Result_Reading.md` and `queries_and_scripts/catalog_result_profiles/windows/` when explaining a Windows stock catalog query result by Catalog `ID`.
- `notes-and-memory/Codex_Network_Access_Fix.md` if DNS or network calls fail inside Codex but work from the user's terminal.
- `02_Working_Files/Query_Methods` through `orbital-query-method-memory` when the user asks for investigation guidance, SQL construction, table selection, catalog reuse, or repeated query patterns.

## Query Preparation Workflow

0. Check network state before any API call:

```bash
env | sort | rg -i 'CODEX_SANDBOX|NETWORK|SANDBOX'
python3 - <<'PY'
import socket
s = socket.socket()
s.settimeout(2)
try:
    s.connect(("8.8.8.8", 53))
    print("network_ok")
except Exception as exc:
    print(type(exc).__name__, exc)
finally:
    s.close()
PY
```

If the output shows `CODEX_SANDBOX_NETWORK_DISABLED=1` or socket calls fail with `Operation not permitted`, do not treat it as an Orbital credential failure. Tell the user this Codex thread needs to be restarted with network-enabled sandbox settings, or ask the user to run the project helper in Terminal and then inspect the refreshed files locally.

1. Identify the intended target set and convert it to API `nodes` selectors.
2. Validate that the target is well-defined before any API call:
   - each target must have an explicit selector prefix and value, except only deliberately approved `all`
   - ambiguous scope wording such as "any", "every", "online", "hosts", or "endpoints" must be mapped to an exact selector list or clarified before execution
   - ambiguous identifiers such as a bare hostname, bare GUID, bare ID, or vague phrase like "all Windows hosts" require clarification or explicit conversion to a selector
   - broad targeting such as `all`, `random`, large wildcards, large network ranges, or OS-only targeting requires explicit user approval before execution
   - if the target cannot be written as the exact `nodes` array to submit, stop and ask for clarification
3. Reject or clarify broad targeting such as `all`, `random`, large wildcards, or large network ranges unless the user explicitly approves the scope.
4. Before writing new SQL, use `orbital-query-method-memory` when the task involves investigation logic, table selection, catalog reuse, or a repeated query pattern:
   - search `02_Working_Files/Query_Methods` for prior methods
   - search Orbital Catalog/API context for matching catalog entries
   - reuse or adapt proven SQL patterns when they fit
5. Build or inspect SQL.
6. Verify table names and column names against `osquery_schema_5_23_0.json` when the query uses upstream osquery tables.
7. Check platform assumptions, evented tables, required constraints, expensive tables, and whether `os` or `allowOS` filters are needed.
8. Choose a short, generic query label. Prefer `codex_<table_or_goal>`.
8a. If the task may need more than one query submission, choose a stable `--task-name` before the first submission. Reuse it for corrected, follow-up, or supporting queries so the ledger can show which Job IDs were needed for the one task.
9. Before executing, show the user:
   - the exact SQL query
   - the exact target selector list
   - relevant OS or `allowOS` filters
10. Only proceed when the target selector list is explicit and approved enough for execution.
11. Request network permission before calling the Orbital API when the tool is available. If the current session lacks that permission path, report the sandbox limitation clearly.
12. Run `scripts/run_live_query.py`. For `host:` or `hostname:` targets, the helper defaults to scheduled mode: `POST /query`, `expiry = now + 120 seconds`, and `interval = 0`.
13. After completion, always report:
   - `orbital_queryID` / Job ID from the response `ID` field
   - task name/task ID when used for a multi-query task
   - whether the helper stored the run in `local/orbital_query_runs/live_query_runs.jsonl`
   - how many endpoints answered
   - row count
   - target metadata/timestamp if useful
   - the result rows as a Markdown table whose columns match the SQL query result shape
   - only the result columns relevant to the user request
13a. If the query is a catalog-derived Windows stock query and the Catalog `ID` is known, check the matching per-Catalog-ID Markdown file under `queries_and_scripts/catalog_result_profiles/windows/` before explaining the result. Use it to distinguish no-hit results, inventory/posture rows, event-log caveats, high-volume output, no-response handling, and known validation caveats. Use `queries_and_scripts/catalog_result_profiles/windows_stock_catalog_result_profiles.jsonl` for automated lookup when the filename is not known.
14. Explain that scheduled host runs store the query in the cloud and can be checked later through:
   - `GET /v0/jobs/{{orbital_queryID}}`
   - `GET /v0/jobs/{{orbital_queryID}}/results`
15. When waiting for a query to finish, do not execute the same query again and do not use `queryId:` for monitoring. Use the stored `orbital_queryID` and monitor status/results with `/v0/jobs/{{orbital_queryID}}` or `/v0/jobs/{{orbital_queryID}}/results`.
16. Default waiting behavior after a new query returns `orbital_queryID`:
   - wait 10 seconds, then call `GET /v0/jobs/{{orbital_queryID}}`
   - show how many endpoints responded, using `done_count` when present
   - check at most until 20 seconds after submission
   - if `done_count` does not increase between checks, stop waiting and show a message with the `orbital_queryID`
   - if the 20 second maximum is reached, stop waiting and show a message with the `orbital_queryID`
17. For expensive tables such as `process_memory_map`, `hash`, `authenticode`, broad `file`, or event/log tables, never rerun the same query to validate execution. First check the stored Job ID. If no Job ID was captured, treat that as a workflow defect for host-targeted queries and use scheduled mode on the next run.
18. If multiple query submissions were required, review the run ledger entries for the task name before the final response and list the query names and Job IDs that were needed to gather or validate the information.
19. If the SQL/table/caveat pattern is reusable, ask whether to save or update it through `orbital-query-method-memory`. Save only the method, not endpoint result rows or tenant-specific output.

## Query Helper Script

Run the helper from the Orbital project root. It reads credentials from environment variables and, by default, from `02_Working_Files/orbital_credentials.env` if that file exists. Never print or store tokens.

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-osquery-live-query/scripts/run_live_query.py \
  --target host:EXAMPLE-HOST \
  --label codex_processes \
  --name "codex scheduled processes lookup" \
  --task-name "Investigate specific endpoint process state" \
  --sql-file /tmp/query.sql
```

With a `host:` or `hostname:` target, the helper uses scheduled mode automatically:

- API path: `POST /query`
- expiry: `now + 2 minutes`
- interval: `0`
- expected response: Job object with `ID`, exposed as `orbital_queryID`

The SQL can also be piped through stdin:

```bash
printf '%s\n' "SELECT pid, name, path, cmdline FROM processes ORDER BY pid LIMIT 50;" \
  | python3 /Users/tschranz/.codex/skills/orbital-run-osquery-live-query/scripts/run_live_query.py \
      --target host:EXAMPLE-HOST \
      --label codex_processes \
      --name "codex scheduled process inventory"
```

To force immediate live mode, use `--live`. Only do this when the user explicitly wants a live/probe response and accepts that Job ID tracking may not be available:

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-osquery-live-query/scripts/run_live_query.py \
  --live \
  --target host:EXAMPLE-HOST \
  --label codex_processes \
  --sql-file /tmp/query.sql
```

To check an existing cloud-stored query/job without rerunning the endpoint query:

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-osquery-live-query/scripts/run_live_query.py \
  --job-id "{{orbital_queryID}}"
```

To fetch stored results for an existing query/job:

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-osquery-live-query/scripts/run_live_query.py \
  --job-id "{{orbital_queryID}}" \
  --job-results
```

The helper polls job status briefly after new query submission by default when the response includes `orbital_queryID`. To disable this behavior:

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-osquery-live-query/scripts/run_live_query.py \
  --target host:EXAMPLE-HOST \
  --label codex_processes \
  --sql-file /tmp/query.sql \
  --no-status-poll
```

Multiple target selectors are allowed:

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-osquery-live-query/scripts/run_live_query.py \
  --target host:EXAMPLE-HOST \
  --target ipv4:192.168.1.% \
  --allow-os windows \
  --label codex_logged_in_users \
  --name "codex live logged in users" \
  --sql-file /tmp/query.sql
```

Supported credential inputs:

- `ORBITAL_API_TOKEN`, `ORBITAL_TOKEN`, `SECUREX_TOKEN`, `CISCO_SECUREX_TOKEN`, or `CISCO_TOKEN`
- `ORBITAL_CLIENT_ID` plus `ORBITAL_CLIENT_SECRET`
- `SECUREX_CLIENT_ID` plus `SECUREX_CLIENT_SECRET`
- `ORBITAL_REGION`, defaulting to `eu`; supported values: `eu`, `us`, `na`, `apjc`

## Target Selector Rules

Use documented selectors from `Orbital_Target_Node_Selectors.md`. Examples:

- `host:EXAMPLE-HOST`
- `hostname:EXAMPLE-HOST`
- `ipv4:192.168.1.%`
- `ip:10.0.0.1`
- `netmask:192.168.1.168/24`
- `mac:02:42:c8:1f:7d:fa`
- `orb:<orbital_id>`
- `amp:<secure_endpoint_guid>`
- `cm:<secure_client_guid>`
- `machine:<machine_id>`
- `os:windows`
- `queryId:<query_id>`

Prefer exact host or exact endpoint identifiers for first tests. Treat `%` wildcard selectors as dynamic targeting. Use `netmask` for IPv4 CIDR ranges. Do not assume IPv6 wildcard or subnet support.

Do not confuse `queryId:<query_id>` with `orbital_queryID`. `queryId:<query_id>` is a target selector for reusing an existing query definition. `orbital_queryID` is returned by query creation and is used for `/v0/jobs/...` status and results lookup.

## Result Handling

The helper emits JSON:

- `submitted_sql`: SQL submitted to Orbital.
- `query_label`: label submitted to Orbital.
- `query_name`: display name submitted to Orbital.
- `task_id`: optional investigation/task identifier used to group multiple query jobs.
- `task_name`: optional investigation/task name used to group multiple query jobs.
- `query_mode`: `scheduled` or `live`.
- `api_path`: `/query` for scheduled mode or `/query/run` for live mode.
- `targets`: target selectors submitted to Orbital.
- `orbital_queryID`: Orbital Job ID from the API response `ID` field. Show this in user-facing output so the user can verify the same query in Postman or another API client.
- `response_id`: compatibility alias for `orbital_queryID`.
- `run_ledger`: local JSONL path where operational run metadata was recorded. This is ignored by git and must not contain endpoint rows.
- `job_check_status`: reason why job status could not be checked, when no job ID was exposed.
- `answered_endpoint_count`: number of endpoint result objects returned by Orbital.
- `job_status_polls`: short `/v0/jobs/{{orbital_queryID}}` status checks after submission, including `done_count` when present.
- `wait_status`: why Codex stopped waiting. If progress stalls or 20 seconds is reached, use the `orbital_queryID` for follow-up instead of rerunning.
- `table_columns`: ordered column names to use for the user-facing Markdown result table.
- `meta`: host, node ID, and reported timestamp where returned.
- `rows`: parsed row dictionaries.
- `errors`: API-level errors if present.

Orbital stores scheduled host query jobs/results in the cloud. When the API returns `ID`, treat it as `orbital_queryID` and use it for follow-up checks:

- `GET /v0/jobs/{{orbital_queryID}}` shows the query/job metadata.
- `GET /v0/jobs/{{orbital_queryID}}/results` retrieves the stored results.

Important: never rerun the same query just to monitor waiting status. Reuse `orbital_queryID` and call the job endpoints. Do not use the `queryId:` target selector for monitoring a submitted query.

If `rows` is empty and the API returned target metadata, report that the query succeeded but found no matching rows. If no result appears for a target, explain that scheduled host queries only return data from endpoints that answer within the query window.

For non-empty results, present the user-facing result as a Markdown table:

- Use the SQL result columns as table headers in the same order returned by Orbital.
- Include endpoint identity columns such as `host` or `nodeId` when results combine multiple endpoints or when those fields are needed to interpret the rows.
- Do not present raw JSON as the primary result unless the user asks for raw output or troubleshooting requires it.
- If the result has many rows, show a useful preview table and state the total `row_count`.

## Safety Rules

- Never run live queries without an explicit target selector.
- Never run live queries while the target is ambiguous, incomplete, or not expressible as the exact `nodes` array.
- Never silently broaden a target from one host to `all`, `random`, wildcard, or network range.
- Never store bearer tokens or client secrets in the skill, project context, or GitHub.
- In this lab project, a local credentials env file may exist under `02_Working_Files`; never print its values in chat or command output.
- Keep API/catalog access workflow in `orbital-api-access`; larger skill scope changes require explicit user confirmation.
- Use `orbital-query-method-memory` to speed up and improve query design, but never store returned endpoint data there.
- Avoid `SELECT *` for broad or expensive tables unless the user explicitly asks for full rows.
- Prefer `LIMIT` for exploratory queries.
