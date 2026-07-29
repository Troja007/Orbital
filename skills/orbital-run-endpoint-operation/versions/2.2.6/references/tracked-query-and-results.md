# Tracked Queries And Results

Use this reference for scheduled work, existing Job IDs, endpoint errors, missing results, and detailed reporting.

## Tracked Lifecycle

Use `POST /query` for tracked scheduled queries. A host selector defaults to a one-shot schedule with two-minute expiry and interval `0`. Treat a top-level response `ID` or `id`, or an explicit job-ID response header, as `orbital_queryID`; never substitute `queryId`, request ID, or another nested identifier.

Persist a submission before monitoring. Reuse `orbital_queryID` with `/v0/jobs/{id}` and `/v0/jobs/{id}/results`; never resubmit solely to check progress. Use `--no-status-poll` when immediate acknowledgement is more valuable than waiting for a short status update.

Treat no rows as a no-hit only when at least one endpoint answered, the job is no longer pending, and `query_error_count` is zero. A missing response can mean that an endpoint did not answer within the scheduled window. For endpoint SQL/table/column errors, surface the nested osquery error before a generic endpoint error; do not automatically rerun a replacement query.

Store meaningful errors only in the local query ledger. Store phase, error scope, sanitized text/hash, optional label, Job ID, and HTTP status. Never store raw results, endpoint identity, ORG data, credentials, or tokens.

## Report Format

```markdown
Checked `host:EXAMPLE-HOST` with `operation_name`.

- Target definition: `host:EXAMPLE-HOST`
- Target scope: `one explicit host selector`
- osquery tables: `system_info` - endpoint identity and operating-system facts
- Run: `run_label_or_name`
- `orbital_queryID`: `...`
- Target count reported by Orbital: `1` or `not reported`
- Endpoint answered: `1`
- Data rows: `N`
- Errors: `0` (only when relevant)

Result heading:

| Field | Value |
| --- | --- |
| ... | ... |

**Summary**
Executed: submitted operation and purpose.
Used results: evidence supporting the conclusion.
Verified afterwards: follow-up operation and outcome, or `No separate verification was performed.`
```

Use a result table for repeated records or key/value details. For an existing Job-ID lookup without submitted SQL, show `osquery tables: not available for existing Job ID`. Omit the table line for scripts.

When follow-up verification returns structured evidence, add a separate verification section before `**Summary**` with its own compact table, Job ID or result ID, condition checked, and outcome. Do not claim independent verification solely because the initial operation returned a result.
