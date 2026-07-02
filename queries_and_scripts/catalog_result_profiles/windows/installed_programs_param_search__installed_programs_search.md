# Installed Programs Search

## Catalog Identity

- Catalog ID: `installed_programs_param_search`
- Catalog name: `Installed Programs Search`
- Platform: windows
- Profile type: sanitized catalog result profile
- Source run: 2026-06-15/2026-06-16
- Catalog updated: 2023-11-14T17:51:59.150055646Z

## What This Query Answers

Use the catalog name, categories, MITRE mapping, and returned columns to decide whether this query is detection-oriented, inventory-oriented, posture-oriented, or forensic context.

Categories:
- `posture-assessment`
- `threat-hunting`

MITRE tactics:
- None recorded.

MITRE techniques:
- None recorded.

This profile does not prove maliciousness by itself. It explains how to read this catalog query's result shape and caveats.

## Expected Result Shape

- Endpoint answered in validation: yes
- Validation status: `completed`
- Observed row count: 18
- Row-count bucket: `medium_11_100`
- Returned labels:
- `installed_programs_search`

Observed columns:

| Label | Columns |
| --- | --- |
| `installed_programs_search` | `name`, `version`, `install_location`, `install_source`, `language`, `publisher`, `uninstall_string`, `identifying_number`, `installation_date` |

Label row counts:
- `installed_programs_search`: 18

## How To Read The Result

Observed validation result:

The endpoint answered and returned 18 rows in the validation run.

If rows are returned:

Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries.

If zero rows are returned:

If a future execution returns zero rows after the endpoint answered, read it as no matching rows for the exact query scope. Do not treat zero rows as proof that the related behavior never happened.

If the endpoint does not respond:

If a future execution has no endpoint response, do not interpret it as zero rows. Zero rows require an answered endpoint. No response requires operational follow-up on target state, job status, and result retrieval.

## Incident Responder Assumptions

Safe assumptions and limits:
- Validation used one explicit Windows endpoint; do not generalize row counts to other endpoints or fleets.
- Row counts describe this validation run only; they are useful for expected result shape and interpretation, not baseline truth.
- Read catalog warnings before interpreting empty or positive results.

Unsafe assumptions:
- Do not assume returned rows are malicious without context.
- Do not assume missing rows prove the behavior never happened.
- Do not generalize this validation row count to all endpoints.
- Do not treat no endpoint response as a clean result.

## Caveats

Catalog warnings:
- This query only returns data on programs where an installed data is available. Wildcard '%' does not match NULL column values. Please edit or remove appropriate conditions to include null values in results.

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

The `installed_programs_param_search` catalog query (Installed Programs Search) returned results that should be interpreted according to the catalog purpose and observed result shape. An answered endpoint with zero rows means no matching rows were returned for this exact query scope. Returned rows are endpoint evidence for the query condition or inventory shape, but they are not automatically a malicious verdict. A missing endpoint response is operationally different from zero rows and should be checked through target availability and job/result status.

## Privacy Boundary

This profile intentionally does not store:

- Endpoint result rows
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

No sanitized sample result data was recorded for this profile.