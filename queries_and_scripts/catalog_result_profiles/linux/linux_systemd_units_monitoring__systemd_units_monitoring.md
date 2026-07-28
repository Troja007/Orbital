# Systemd Units Monitoring

## Catalog Identity

- Catalog ID: `linux_systemd_units_monitoring`
- Catalog name: `Systemd Units Monitoring`
- Platform: linux
- Profile type: sanitized catalog result profile
- Source run: 2026-07-28
- Catalog updated: 2023-11-14T17:51:59.150055646Z

## What This Query Answers

Use the catalog name, categories, MITRE mapping, and returned columns to decide whether this query is detection-oriented, inventory-oriented, posture-oriented, or forensic context.

Categories:
- `posture-assessment`
- `forensics`

MITRE tactics:
- `TA0003`: Persistence
- `TA0004`: Privilege Escalation

MITRE techniques:
- None recorded.

MITRE subtechniques:
- `T1543.002`: Systemd Service

This profile does not prove maliciousness by itself. It explains how to read this catalog query's result shape and caveats.

## Expected Result Shape

- Endpoint answered in validation: yes
- Validation status: `completed`
- Observed row count: 348
- Row-count bucket: `high_101_1000`
- Returned labels:
- `linux_systemd_units_monitoring`

Observed columns:

| Label | Columns |
| --- | --- |
| `linux_systemd_units_monitoring` | `id`, `description`, `load_state`, `active_state`, `sub_state`, `following`, `object_path`, `job_id`, `job_type`, `job_path`, `fragment_path`, `user`, `source_path` |

Label row counts:
- `linux_systemd_units_monitoring`: 348

## How To Read The Result

Observed validation result:

The endpoint answered and returned 348 rows in the validation run.

If rows are returned:

Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries.

If zero rows are returned:

If a future execution returns zero rows after the endpoint answered, read it as no matching rows for the exact query scope. Do not treat zero rows as proof that the related behavior never happened.

If the endpoint does not respond:

If a future execution has no endpoint response, do not interpret it as zero rows. Zero rows require an answered endpoint. No response requires operational follow-up on target state, job status, and result retrieval.

## Incident Responder Assumptions

Safe assumptions and limits:
- Validation used one explicit Linux endpoint; do not generalize row counts to other endpoints or fleets.
- Row counts describe this validation run only; they are useful for expected result shape and interpretation, not baseline truth.
- Read catalog warnings before interpreting empty or positive results.

Unsafe assumptions:
- Do not assume returned rows are malicious without context.
- Do not assume missing rows prove the behavior never happened.
- Do not generalize this validation row count to all endpoints.
- Do not treat no endpoint response as a clean result.

## Caveats

Catalog warnings:
- This query only retrieves data for systemd services executing at the system-level. It does not include systemd services executing in a single user's context.

Error class: `none`

Label errors:
- None recorded.

Endpoint errors:
- None recorded.

## Recommended Follow-Up

When the result matters for an investigation:

1. Confirm the endpoint answered before interpreting row counts.
2. Compare returned rows with the catalog purpose and warnings.
3. Validate suspicious rows with surrounding context such as time, path, user, process, signature, network, persistence, or related event evidence.
4. Use narrower targets or parameters before broad execution if the profile shows high-volume output.
5. If no endpoint response occurred, check target selection and stored job/result status before rerunning.

## Explanation Template

The `linux_systemd_units_monitoring` catalog query (Systemd Units Monitoring) returned results that should be interpreted according to the catalog purpose and observed result shape. An answered endpoint with zero rows means no matching rows were returned for this exact query scope. Returned rows are endpoint evidence for the query condition or inventory shape, but they are not automatically a malicious verdict. A missing endpoint response is operationally different from zero rows and should be checked through target availability and job/result status.

## Privacy Boundary

This profile intentionally does not store raw endpoint evidence:

- Raw endpoint result rows
- Hostnames
- Target selectors
- Job IDs
- Usernames
- IP addresses
- GUIDs
- Tenant data
- Raw API responses
- Credentials

## Sample Result Data

Representative sanitized sample rows, when available. These examples preserve result shape only and are not endpoint evidence.

Label: `linux_systemd_units_monitoring`

| `active_state` | `description` | `following` | `fragment_path` | `id` | `job_id` | `job_path` | `job_type` | `load_state` | `object_path` | `source_path` | `sub_state` | `user` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <state-category> | <redacted:sensitive-value> | <empty> | <empty> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <state-category> | <path> | <empty> | <state-category> | <redacted:username> |
| <state-category> | <path> | <empty> | <empty> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <state-category> | <path> | <empty> | <state-category> | <redacted:username> |
| <state-category> | <redacted:sensitive-value> | <empty> | <empty> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <state-category> | <path> | <empty> | <state-category> | <redacted:username> |
