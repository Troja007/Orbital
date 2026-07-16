---
name: orbital-run-endpoint-operation
description: Run targeted Cisco Orbital endpoint operations. Use when Codex needs to validate and execute an osquery query, resolve an active Codex ORG Mapping and its credential source, monitor a query Job ID, parse query results or errors, or prepare future Orbital script work through its separate API path.
---

# Orbital Run Endpoint Operation

Use this as the shared endpoint-operation boundary for Orbital. Run custom osquery through the Orbital API only against explicit `nodes` selectors. Validate table/column, platform, target scope, ORG mapping, and credentials before an API call.

## Operation Modes

- **Query mode is implemented.** Use `scripts/run_live_query.py` for custom osquery queries and their existing Job IDs.
- **Script mode is reserved, not implemented by this helper.** Do not submit a script to a query endpoint or represent a query result as script execution.
- When a script adapter is added, use the script-specific API path and retain the shared ORG, target, local-context, run-ledger, and error-recording rules. Classify the script as observational or state-changing before submission; require the applicable review and explicit approval for state-changing work.

## Operating Model

- Use `POST /query` for scheduled queries. It is the default for `host:` and `hostname:` targets: expiry is 2 minutes and interval is 0.
- Use `POST /query/run` only when the user explicitly requests an immediate/live probe and accepts that it may not return a Job ID.
- Treat a response `ID` or `id`, or an explicit job-ID response header, as `orbital_queryID`. Never treat `queryId`, request ID, or another nested identifier as a Job ID.
- Persist the submission record before status or result retrieval. Reuse `orbital_queryID` for `/v0/jobs/{id}` and `/v0/jobs/{id}/results`; never resubmit a query merely to monitor it.
- Use `orbital-api-access` for connectivity, authentication troubleshooting, or catalog import. Use `orbital-query-method-memory` for investigation design, table selection, catalog reuse, or repeatable query methods.

Cisco distinguishes scheduled queries for results that arrive over time from live queries for currently connected nodes; both support custom `osQuery` statements. [Cisco Orbital Query API](https://developer.cisco.com/docs/orbital/queries/)

## ORG And Credential Resolution

The active global mapping is `~/.codex/state/cisco-security-api-access/current_org_mapping.json`, unless `--org-mapping-state-file` explicitly selects another mapping state file.

- The mapping supplies non-secret EDR, XDR, Orbital, and Secure Endpoint v3 identifiers plus `source_env_file`.
- The credential env file supplies the token or OAuth client credentials. It determines the effective Orbital tenant; `org_context` is local metadata and is never sent in the Orbital request body.
- In the current chat, retain the mapping/group already established for short follow-ups. The helper's local context cache is only a durable hint; it cannot inspect Codex chat history.
- A supplied `--org-group` must match the selected mapping alias. An ORG label or `--org` list cannot switch tenants. Switch the global mapping with the credential-management workflow, or explicitly select the matching mapping state file, before a new group is queried.
- Keep ORG IDs, product mappings, and credential-file paths local only. Do not include them in GitHub artifacts or routine user-facing output.

Resolve in this order: selected mapping state -> matching ORG metadata -> mapping `source_env_file`; use `--env-file` only as an explicit override. Use the project-local credential file only as legacy fallback.

## Required Inputs

Before a new submission, confirm:

- an exact `nodes` selector list;
- SQL, either supplied or safely constructed from clear intent;
- a concise query label/purpose;
- a selected ORG mapping and a credential source;
- a network-enabled Codex runtime.

If the user supplies a bare hostname, ID, GUID, `device`, `node`, `target`, or `endpoint`, ask which identifier and selector type it represents. Do not guess among Catalog ID, Orbital ID, Secure Endpoint GUID, Secure Client GUID, AnyConnect UDID, `queryId`, and `orbital_queryID`.

Do not infer broad scope from "any", "online", "all", or "every". Require the exact submitted selector list. `all`, `random`, OS selectors, CIDR ranges, and broad wildcards require explicit approval and `--approve-broad-target`.

## Target Rules

Use documented selectors from `project-context/Orbital_Target_Node_Selectors.md`, for example:

- `host:EXAMPLE-HOST`, `hostname:EXAMPLE-HOST`
- `orb:<orbital_id>`, `amp:<secure_endpoint_guid>`, `cm:<secure_client_guid>`
- `ip:10.0.0.1`, `ipv4:192.168.1.%`, `netmask:192.168.1.168/24`
- `machine:<machine_id>`, `os:windows`, `random:5`, `queryId:<query_id>`

`os` adds all hosts with the selected operating system to the target set. `allowOS` filters results after target selection. Do not describe both as generic OS filters. `all` cannot be combined with other node selectors or `allowOS`; it can use the operating-system field as documented in project context.

`allowOS:<platform>` inside `nodes` and `--allow-os <platform>` are alternative representations. Use only one and always include another endpoint selector. `queryId:<id>` is a selector, not a Job ID; this helper still requires explicit `osQuery` SQL.

For a concrete short hostname that may be stored as an FQDN, try a narrow trailing wildcard such as `host:slate%` or `hostname:slate%` before treating the endpoint as unavailable. Do not begin with contains matching such as `host:%late%`; it can match unrelated devices. The helper considers a single trailing hostname wildcard with a four-character-or-longer stem narrow; every other wildcard requires broad-target approval.

## Execution Workflow

1. Check `CODEX_SANDBOX_NETWORK_DISABLED`; if network policy blocks sockets, report a sandbox limitation rather than a credential failure.
2. Resolve the active mapping, validate any supplied ORG group against its alias, and load only the selected credential source.
3. Convert the intended targets to the exact `nodes` array. Reject unclear, invalid, or unapproved broad scope before any API call.
4. For new SQL, search query-method memory and relevant catalog context when the task involves investigation logic, repeatable patterns, or catalog reuse.
5. Validate upstream osquery tables/columns against `product-context/osquery/osquery_schema_5_23_0.json`; also check Orbital availability, platform, required constraints, and cost.
6. Prefer specific columns and `LIMIT` for exploration. Avoid `SELECT *` on broad or expensive tables unless explicitly requested.
7. Show the exact SQL, exact target list, execution mode, and relevant `os`/`allowOS` semantics before submission whenever approval or safety depends on them. For an already-approved narrow follow-up, a SQL summary is sufficient.
8. Use `--task-name` before the first query when one analyst task may need multiple submissions.
9. Submit through `scripts/run_live_query.py`. Record the returned Job ID before interpretation.
10. Poll a Job ID at most through 20 seconds after submission. Fetch stored results after a completed endpoint is reported; if `done_count` is unavailable but a Job ID exists and no rows/errors were returned yet, perform one stored-results check after polling before concluding there are no rows. If status retrieval fails, retain and report the Job ID rather than resubmitting.
11. Treat no data rows as a no-hit only when at least one endpoint answered, the job is no longer pending, and `query_error_count` is zero. A missing response means the endpoint may not have answered within the scheduled window.
12. If the endpoint answered and `query_error_count` is non-zero, do not immediately rewrite or rerun the query. The helper must surface a nested `osQueryResult.error` before a generic endpoint error and store both meaningful response errors locally. Inspect the stored Job ID once with `--job-results --raw-response` only when the response shape needs troubleshooting. If the error is real, stop execution and route SQL/table/column correction to `orbital-query-method-memory`; do not run diagnostic replacement queries in this execution skill unless the user explicitly asks.
13. For multi-query work, inspect the run ledger by task name and report each query label, Job ID, status/error outcome, and purpose.

## Helper

Run from the project root. The helper never prints credentials.

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-endpoint-operation/scripts/run_live_query.py \
  --target host:EXAMPLE-HOST \
  --label codex_system_info \
  --name "codex scheduled system information" \
  --task-name "Inspect one endpoint" \
  --sql-file /tmp/query.sql
```

The preceding command uses scheduled mode automatically. Use `--live` only for an explicitly requested immediate probe:

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-endpoint-operation/scripts/run_live_query.py \
  --live \
  --target host:EXAMPLE-HOST \
  --label codex_system_info \
  --sql-file /tmp/query.sql
```

Use a broad selector only after explicit approval:

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-endpoint-operation/scripts/run_live_query.py \
  --target netmask:192.168.1.168/24 \
  --approve-broad-target \
  --label codex_system_info \
  --sql-file /tmp/query.sql
```

Check an existing job without rerunning the endpoint query:

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-endpoint-operation/scripts/run_live_query.py \
  --job-id "{{orbital_queryID}}" \
  --job-results
```

Use `--raw-response` only for response-shape troubleshooting. Do not expose raw API payloads by default.

## Result Handling

The helper returns compact JSON with `query_mode`, `api_path`, `targets`, `orbital_queryID`, `run_ledger`, `answered_endpoint_count`, `row_count`, `query_error_count`, `query_errors`, `meta`, and `rows`. New submissions also include a sanitized `context` summary. Full local `org_context` and `credential_context` details are included only with `--raw-response` for troubleshooting and must not be shown routinely.

- `row_count` counts data rows only.
- `query_error_count` includes endpoint-level and osquery-level failures; never call these successful no-hits. Empty Orbital error placeholders, such as empty strings or dictionaries without a non-empty localized message, are not meaningful errors.
- If a stored Job ID result contains valid rows and an empty error placeholder, present the rows and mention that the raw response included a non-meaningful error field only when troubleshooting requires it.
- Store every meaningful error in `local/orbital_query_runs/live_query_runs.jsonl` as an `orbital_error` record. Record `phase`, `scope`, error text and hash, optional query label, Job ID, and HTTP status. Do not store raw responses, endpoint rows, host/node identity, ORG data, credentials, or tokens in the error record.
- Use `scope=endpoint_osquery` for SQL/table/column errors reported by an endpoint. Use `scope=foundational` for failures before or while creating/following an API call, including validation, mapping/credential resolution, token acquisition, HTTP/API responses, Job-ID extraction, status polling, and stored-results retrieval.
- Endpoint identity is available in `meta`; include it when multiple targets or ambiguous rows require it.
- For a high-volume result, present a relevant preview and total count. For a small result, show only columns needed to answer the user. Do not emit raw JSON unless requested.
- When explaining a Windows stock catalog query, use its Catalog ID and the matching sanitized profile under `queries_and_scripts/catalog_result_profiles/windows/`.

Default user-facing trace: target selector list, purpose, execution mode, SQL summary or exact SQL when needed, Job ID/status, answered endpoint count, data-row count, error count, compact result, caveat, and whether reusable method memory should be updated.

## Version Retention

`VERSION` is the current semantic version. `scripts/version_skill.py` creates a non-recursive snapshot under `versions/<version>/` with a SHA-256 manifest and automatically retains only the newest five version directories.

Before releasing a substantive change, verify that the current version already has a snapshot. After validation, increment `VERSION` and create the release snapshot:

```bash
python3 scripts/version_skill.py --version "$(tr -d '\n' < VERSION)" --keep 5
```

Sync the complete skill folder, including `VERSION`, `versions/`, and scripts, to the global skill only after validation.

## Durable Project Updates

After changing this skill, its helper, reusable SQL artifacts, project context, or query-method memory, append a sanitized entry to `local/project-change-log.md`. Record workspace-to-global skill syncs in `local/sync-activity-log.md`. Do not stage either log or include endpoint rows, target selectors, Job IDs, credentials, tenant data, raw responses, hostnames, IPs, GUIDs, or other customer-identifying data.

Promote reusable, sanitized lessons to `notes-and-memory/decisions/`, query-method memory, project context, product context, or catalog result profiles as appropriate. Never store endpoint evidence in GitHub.

## Safety

- Never execute with an ambiguous or missing target.
- Never silently broaden one host to a wildcard, range, random sample, OS scope, or `all`.
- Never store or display tokens and client secrets.
- Never store raw API responses or endpoint result rows in the error ledger; store only the minimal error record needed to diagnose and correlate the failure.
- Never rerun a query merely to check status or compensate for a failed status call.
- Never use this execution skill to iterate on broken SQL after a real endpoint/osquery error. Preserve the Job ID, summarize the error, and move query correction to `orbital-query-method-memory`.
- Keep API/catalog access workflows and query-method memory separate from this execution skill.
