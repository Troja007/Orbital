# Linux pkexec Settings and Events Monitoring

## Catalog Identity

- Catalog ID: `linux_pkexec_settings`
- Catalog name: `Linux pkexec Settings and Events Monitoring`
- Platform: linux
- Profile type: sanitized catalog result profile
- Source run: 2026-07-28
- Catalog updated: 2023-11-14T17:51:59.150055646Z

## What This Query Answers

Use the catalog name, categories, MITRE mapping, and returned columns to decide whether this query is detection-oriented, inventory-oriented, posture-oriented, or forensic context.

Categories:
- `posture-assessment`
- `forensics`
- `threat-hunting`

MITRE tactics:
- `TA0002`: Execution
- `TA0003`: Persistence
- `TA0005`: Defense Evasion

MITRE techniques:
- None recorded.

MITRE subtechniques:
- None recorded.

This profile does not prove maliciousness by itself. It explains how to read this catalog query's result shape and caveats.

## Expected Result Shape

- Endpoint answered in validation: yes
- Validation status: `completed`
- Observed row count: 5
- Row-count bucket: `low_1_10`
- Returned labels:
- `linux_deb_packages_polkit`
- `linux_pkexec_permission_bits`

Observed columns:

| Label | Columns |
| --- | --- |
| `linux_deb_packages_polkit` | `name`, `version`, `source`, `arch`, `revision`, `status`, `maintainer` |
| `linux_pkexec_permission_bits` | `path`, `mode`, `last_access_time`, `last_modification_time`, `last_status_change_time`, `create_time` |

Label row counts:
- `linux_deb_packages_polkit`: 4
- `linux_pkexec_permission_bits`: 1

## How To Read The Result

Observed validation result:

The endpoint answered and returned 5 rows in the validation run.

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

Unsafe assumptions:
- Do not assume returned rows are malicious without context.
- Do not assume missing rows prove the behavior never happened.
- Do not generalize this validation row count to all endpoints.
- Do not treat no endpoint response as a clean result.

## Caveats

Catalog warnings:
- None recorded.

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

The `linux_pkexec_settings` catalog query (Linux pkexec Settings and Events Monitoring) returned results that should be interpreted according to the catalog purpose and observed result shape. An answered endpoint with zero rows means no matching rows were returned for this exact query scope. Returned rows are endpoint evidence for the query condition or inventory shape, but they are not automatically a malicious verdict. A missing endpoint response is operationally different from zero rows and should be checked through target availability and job/result status.

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

Label: `linux_deb_packages_polkit`

| `arch` | `maintainer` | `name` | `revision` | `source` | `status` | `version` |
| --- | --- | --- | --- | --- | --- | --- |
| <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <state-category> | <redacted:sensitive-value> |
| <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <state-category> | <redacted:sensitive-value> |
| <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <state-category> | <redacted:sensitive-value> |

Label: `linux_pkexec_permission_bits`

| `create_time` | `last_access_time` | `last_modification_time` | `last_status_change_time` | `mode` | `path` |
| --- | --- | --- | --- | --- | --- |
| <timestamp:iso-8601> | <timestamp:iso-8601> | <timestamp:iso-8601> | <timestamp:iso-8601> | <redacted:sensitive-value> | <path> |
