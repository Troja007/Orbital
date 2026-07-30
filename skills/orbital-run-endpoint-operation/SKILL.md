---
name: orbital-run-endpoint-operation
description: Run targeted Cisco Orbital osquery queries and approved endpoint scripts. Use for immediate single-host checks, tracked scheduled queries, Job-ID result retrieval, ORG mapping and credential resolution, osquery table reporting, and safe observational or approved state-changing endpoint operations.
---

# Orbital Run Endpoint Operation

Use the helper at `scripts/run_live_query.py` for custom osquery. Use `scripts/run_live_script.py` only for an explicit catalog or reviewed inline script. Never send a script to a query endpoint.

## Fast Query Path

Use this path first when all of these are true:

- The user gives one exact, non-wildcard `host:` or `hostname:` selector.
- The user supplies a read-only `SELECT` or `WITH ... SELECT` query, or one unambiguous tested/validated query-method record supplies it.
- The currently selected global ORG mapping is acceptable; the user does not name a new ORG group.
- The query is a simple known-table check or the table/columns are clear from the supplied SQL.

For supplied SQL or a built-in direct path, do not search catalog snapshots, project memory, or project-relative context files before submission. The helper reads the current global mapping at `~/.codex/state/cisco-security-api-access/current_org_mapping.json` and the mapping's credential source directly. Do not ask to rediscover ORGs already selected in that mapping.

For a natural-language request without SQL, make one focused lookup in available query-method memory before broader research. If exactly one `tested` or `validated` record matches the stated task, platform, and target scope and supplies a read-only SQL pattern with no unresolved parameters, execute that stored pattern directly. Do not perform catalog discovery, open-ended schema research, or a proposal/confirmation round after this kind of memory hit. If the match is missing, draft, deprecated, ambiguous, or needs a value the user did not provide, use the normal query-design path instead.

Submit with the interactive profile. It uses `POST /query/run`, skips Job-status polling, and returns after the API response:

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-endpoint-operation/scripts/run_live_query.py \
  --execution-profile interactive \
  --target host:EXAMPLE-HOST \
  --label codex_system_info \
  --name "codex immediate system information" \
  --sql-file /tmp/query.sql
```

The interactive profile accepts only one explicit host selector and a read-only query. It can return immediate results but does not promise an `orbital_queryID`. Use it when the user wants a quick online endpoint check.

## Hostname Resolution And Stable Targeting

When the user supplies a hostname such as `victim3`, start the requested read-only query directly with `host:victim3`. Treat endpoint resolution as the number of answered endpoints, not the number of data rows: a response with zero data rows can still identify exactly one target.

Apply this sequence before reporting the final result:

1. Submit the requested SQL against `host:NAME` with the interactive profile.
2. If exactly one endpoint answered and no API or endpoint query error occurred, extract its returned `nodeId`. It is the Orbital ID. Re-submit the same SQL with `orb:NODE_ID`; use that stable-target result as the final single-device result. The helper's interactive profile accepts only host selectors, so use the tracked profile for the `orb:` re-query.
3. If no endpoint answered and no API or endpoint query error occurred, repeat the same SQL with `host:NAME%`. This is the FQDN-resolution fallback, never a contains match such as `host:%NAME%`. Use the tracked profile and `--approve-broad-target`, because a trailing wildcard can select multiple endpoints.
4. If the fallback returns exactly one endpoint, extract its `nodeId` and re-submit the SQL with `orb:NODE_ID` as in step 2.
5. If either selector returns multiple endpoints, do not choose one or re-query a single Orbital ID. Continue with the result from that selector and show all returned hosts and their result rows. State clearly that `host:NAME%` included multiple endpoints.

Do not apply the hostname fallback to an API, authentication, SQL, table, column, or endpoint execution error. Diagnose those errors through the normal failure-recovery path; changing the selector would not repair the query.

After showing a multi-endpoint wildcard result, ask exactly: `Multiple hosts matched host:NAME%. Please clarify the device definition. Reply re-do to resolve the right computer name through Secure Endpoint and XDR Assets.` If the user replies `re-do`, query the Secure Endpoint Computers API with `GET /v1/computers?hostname=NAME&limit=10`, then use the `xdr-apis` Asset guidance and its current documented asset-search contract to compare candidate device identities. Show the candidate names and identity relationships, ask the user to choose the canonical device definition, and only then re-run the original query against the selected stable selector.

## Known Method Direct Execution

Treat tested or validated query-method memory as executable operational knowledge, not as documentation to re-derive. Submit the stored SQL immediately when all of these are true:

- One record is the unambiguous semantic match for the request.
- The record contains a read-only SQL pattern that matches the requested platform and has no unresolved placeholders.
- The target is one exact host or hostname selector, and the current global ORG mapping remains selected.
- The request does not change endpoint state, invoke a script, widen target scope, or explicitly ask for planning/review first.

Use the stored bounds unless the user supplies a narrower bound. Substitute only values the user explicitly supplied. In the final report, name the method record used and show the submitted SQL or a faithful SQL summary when it affects interpretation. Do not direct-execute a draft/deprecated record, a record with several equally plausible SQL patterns, a broad-target pattern, or a state-changing action.

## Windows Event Log Path

When the user asks for Windows Event Viewer records and supplies an exact channel, submit the bounded `windows_eventlog` query directly. Do not spend a preliminary call discovering the channel, catalog entry, or ORG state. For one exact Windows host, use the interactive profile without adding `--allow-os`; the target is already known to be Windows.

Use only the columns needed to interpret the records and always bound the query by exact `channel`, descending `datetime`, and the requested row limit. The default when the user asks for recent records but supplies no count is three:

```sql
SELECT datetime, provider_name, eventid, level, data
FROM windows_eventlog
WHERE channel = 'EVENT_VIEWER_CHANNEL'
ORDER BY datetime DESC
LIMIT 3;
```

For multiple supplied channels, submit one independent bounded query per channel. Do not start with `OR`, `IN`, `UNION`, a provider-wide scan, or a channel wildcard: separate results preserve the channel-specific row count, empty state, and error state. An empty result means no retained record matched the exact channel and bounds; it is not a query error and does not prove the channel is absent.

For Cisco Secure Endpoint logs, apply these direct refinements only when they match the stated question:

- `CiscoSecureEndpoint/Cloud`: query all recent records for a general log check. For detections specifically, add `eventid = 401 AND data LIKE '%EVENT_DETECTION%'`.
- `CiscoSecureEndpoint/Events`: query all recent records for a general log check. For Host Based Firewall decisions specifically, add `eventid IN (1800, 1801)`; `1800` is allow and `1801` is block.
- `CiscoSecureEndpoint/WMI`: query the exact channel with the general pattern. It can validly return zero rows.

If the user has not supplied an exact Event Viewer channel, ask for it unless they explicitly ask to enumerate available channels. Never substitute a guessed channel name or perform an unbounded event-log scan.

Use the tracked profile when a Job ID, scheduled expiry window, multiple targets, a wildcard, an endpoint that may be offline, or later result retrieval is required. Submit it without initial polling when fast acknowledgement matters:

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-endpoint-operation/scripts/run_live_query.py \
  --execution-profile tracked \
  --no-status-poll \
  --target host:EXAMPLE-HOST \
  --label codex_tracked_check \
  --sql-file /tmp/query.sql
```

Show the returned Job ID immediately, then retrieve it once with `--job-id JOB_ID --job-results`. Do not resubmit a query merely to monitor it.

## Required Safety Checks

Before every real submission, confirm the exact target selector, SQL, and query purpose. Reject ambiguous identifiers and unapproved broad scope. `all`, `random`, OS selectors, CIDR ranges, multiple broad wildcards, and wildcard host matching require explicit approval plus `--approve-broad-target`, except for the documented post-failure `host:NAME%` FQDN-resolution fallback above.

For a known short hostname that might be stored as an FQDN, retry only with a narrow trailing wildcard such as `host:slate%`. Do not use contains matching such as `host:%late%`.

Use project context, schema validation, catalog data, or query-method memory only when the query is new, complex, potentially expensive, platform-specific, incident-sensitive, or a returned table/column error needs correction. Read [references/targeting-and-query-design.md](references/targeting-and-query-design.md) for those cases. In another project, do not search relative `project-context` paths that are not present.

Do not use the fast path for scripts or state-changing work. Read [references/scripts-and-actions.md](references/scripts-and-actions.md) before any script operation.

## Failure Recovery

Treat a completed query with one or more answered endpoints, zero data rows, and zero query errors as a valid no-hit. Do not retry it simply because the result is empty.

For a real failure, keep the initial error visible and use this bounded recovery sequence:

1. Store the meaningful API, foundational, or endpoint error in the local query ledger through the helper.
2. Classify the failure before another submission. For unknown table/column, syntax, required constraint, or platform errors, consult the matched method record and schema context. For transport, `429`, or `5xx` errors, treat the request as transient. For authentication, credential, ORG mapping, or target-scope failures, correct that foundation first.
3. Submit at most one corrected replacement query only when the correction is clear, remains read-only, keeps the same exact target, and is no broader or more expensive than the initial query. A transient read-only request may be retried once unchanged. Do not retry authentication, credential, ORG mapping, or target-scope failures until their cause is resolved.
4. If the corrected query also fails, stop and report both attempts, their error classes, and the next required action. Do not probe with unrelated health checks or create an unbounded retry loop.

An exact-host no-response uses the documented trailing-FQDN selector fallback. Never use a contains hostname match.

## ORG And Credentials

The active global mapping supplies the non-secret product IDs, selected group alias, region, and `source_env_file`. The credential file determines the effective Orbital tenant; local ORG context never changes the tenant.

Retain the current mapping for follow-up work in the same task. A supplied `--org-group` must match the selected mapping alias. An ORG label or ID cannot switch tenants. Use the credential-management workflow or an explicit mapping-state file before querying a different group.

Never print or store credentials, tokens, product IDs, endpoint evidence, raw responses, or result rows in GitHub-synced artifacts.

## Simulation And Timing

Use `--dry-run` to validate a planned new query without acquiring a token, calling Orbital, or contacting an endpoint. It prints the selected profile, API path, request body, osquery tables, sanitized context summary, and local preflight timing.

```bash
python3 /Users/tschranz/.codex/skills/orbital-run-endpoint-operation/scripts/run_live_query.py \
  --dry-run \
  --execution-profile interactive \
  --target host:EXAMPLE-HOST \
  --label codex_system_info \
  --sql-file /tmp/query.sql
```

Real helper output includes sanitized `timing_ms` for mapping/context resolution, token acquisition, submission, status polling, and total runtime. Use it to distinguish assistant preflight delay from API submission and endpoint execution time.

## Results And Reports

For a query, show the unique `osquery tables` before run identifiers and before result data. List physical tables in SQL encounter order, including tables within CTEs and subqueries; do not list aliases, CTE names, or returned columns. Add a short table purpose when it helps product learning, for example `services` for installed-service configuration and state.

Start every execution result with the exact target definition and target scope. Distinguish requested target count from answered endpoints. End with `**Summary**` covering the submitted operation, the evidence used, and any separate verification. Read [references/tracked-query-and-results.md](references/tracked-query-and-results.md) for Job-ID handling, errors, and the full report format.

## Reference Selection

- Read [references/targeting-and-query-design.md](references/targeting-and-query-design.md) for non-fast-path target selection, schema checks, table selection, or platform/cost concerns.
- Read [references/tracked-query-and-results.md](references/tracked-query-and-results.md) for scheduled query lifecycle, errors, no-response interpretation, stored results, and report details.
- Read [references/scripts-and-actions.md](references/scripts-and-actions.md) only for catalog or inline script execution.
