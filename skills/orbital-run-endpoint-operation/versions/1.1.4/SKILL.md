---
name: orbital-run-osquery-live-query
description: Run generic Cisco Orbital API osquery statements against explicit target selectors. Use when Codex needs to validate osquery table or column assumptions, resolve an active Codex ORG Mapping and its credential source, choose safe scheduled or live execution, submit an Orbital query, monitor an existing Job ID, parse results/errors, or present targeted endpoint rows.
---

# Orbital Run osquery Query

Run custom osquery through the Orbital API only against explicit `nodes` selectors. Validate table/column, platform, target scope, ORG mapping, and credentials before an API call.

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
10. Poll a Job ID at most through 20 seconds after submission. Fetch stored results only after a completed endpoint is reported. If status retrieval fails, retain and report the Job ID rather than resubmitting.
11. Treat no data rows as a no-hit only when at least one endpoint answered, the job is no longer pending, and `query_error_count` is zero. A missing response means the endpoint may not have answered within the scheduled window.
12. For multi-query work, inspect the run ledger by task name and report each query label, Job ID, status/error outcome, and purpose.

## Helper

Run from the project root. The helper never prints credentials.

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-osquery-live-query/scripts/run_live_query.py \
  --target host:EXAMPLE-HOST \
  --label codex_system_info \
  --name "codex scheduled system information" \
  --task-name "Inspect one endpoint" \
  --sql-file /tmp/query.sql
```

The preceding command uses scheduled mode automatically. Use `--live` only for an explicitly requested immediate probe:

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-osquery-live-query/scripts/run_live_query.py \
  --live \
  --target host:EXAMPLE-HOST \
  --label codex_system_info \
  --sql-file /tmp/query.sql
```

Use a broad selector only after explicit approval:

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-osquery-live-query/scripts/run_live_query.py \
  --target netmask:192.168.1.168/24 \
  --approve-broad-target \
  --label codex_system_info \
  --sql-file /tmp/query.sql
```

Check an existing job without rerunning the endpoint query:

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-osquery-live-query/scripts/run_live_query.py \
  --job-id "{{orbital_queryID}}" \
  --job-results
```

Use `--raw-response` only for response-shape troubleshooting. Do not expose raw API payloads by default.

## Result Handling

The helper returns compact JSON with `query_mode`, `api_path`, `targets`, `orbital_queryID`, `run_ledger`, `answered_endpoint_count`, `row_count`, `query_error_count`, `query_errors`, `meta`, and `rows`. New submissions also include non-secret `org_context` and `credential_context` source metadata.

- `row_count` counts data rows only.
- `query_error_count` includes endpoint-level and osquery-level failures; never call these successful no-hits.
- Endpoint identity is available in `meta`; include it when multiple targets or ambiguous rows require it.
- For a high-volume result, present a relevant preview and total count. For a small result, show only columns needed to answer the user. Do not emit raw JSON unless requested.
- When explaining a Windows stock catalog query, use its Catalog ID and the matching sanitized profile under `queries_and_scripts/catalog_result_profiles/windows/`.

Default user-facing trace: target selector list, purpose, execution mode, SQL summary or exact SQL when needed, Job ID/status, answered endpoint count, data-row count, error count, compact result, caveat, and whether reusable method memory should be updated.

## Outcome Guardrails, Version Review, And Retention

Apply `$skill-governance-guardrail` to every material update of this skill, its scripts, references, or assets. Before editing, inspect retained history and record the four release inputs below:

1. **Problem and success:** state the observed problem and a falsifiable success criterion.
2. **Trigger boundary:** give one request that should trigger the skill and one similar request that must not; review the frontmatter description against both.
3. **Dependencies and conflicts:** check related skills, referenced files, scripts, and tools for overlap, stale references, or contradictory instructions.
4. **Risk-based validation:** classify the change as `documentation`, `code`, or `sensitive`; run and record the relevant validation. For `sensitive`, also validate a failure or safe-rejection path.

```bash
python3 scripts/version_skill.py --history
```

After validation, increment `VERSION` and create the release snapshot. The command rejects missing outcome data, an unchanged release, or an unreviewed reintroduction from an older retained version.

```bash
python3 scripts/version_skill.py \
  --version "$(tr -d '\n' VERSION)" \
  --change-type maintenance \
  --change-summary "Describe the user-visible improvement." \
  --problem-statement "Describe the observed failure or gap." \
  --success-criteria "State the observable result that proves the improvement." \
  --positive-trigger "A request that should activate this skill." \
  --negative-trigger "A similar request that should use another approach." \
  --dependency-review "State checked skills, files, tools, and conflicts." \
  --risk-tier documentation \
  --review-notes "State the previous release and regression risks reviewed." \
  --validation "State the exact command or task and its result." \
  --keep 5
```

For `code`, run the changed script or a representative test. For `sensitive`, add `--failure-path-validation` with the rejected-input or safe-failure test. Keep at most five local snapshots in `versions/`. Publish only current files, including `VERSION` and `scripts/version_skill.py`, to GitHub; never publish `versions/` or runtime state.
