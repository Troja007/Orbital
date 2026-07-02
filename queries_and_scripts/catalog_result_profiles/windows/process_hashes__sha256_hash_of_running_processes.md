# SHA256 Hash Of Running Processes

## Catalog Identity

- Catalog ID: `process_hashes`
- Catalog name: `SHA256 Hash Of Running Processes`
- Platform: windows, darwin, linux
- Profile type: sanitized catalog result profile
- Source run: 2026-07-02
- Catalog updated: 2023-11-14T17:51:59.150055646Z

## What This Query Answers

Use the catalog name, categories, MITRE mapping, and returned columns to decide whether this query is detection-oriented, inventory-oriented, posture-oriented, or forensic context.

Categories:
- `live-acquisition-of-volatile-data`

MITRE tactics:
- None recorded.

MITRE techniques:
- None recorded.

MITRE subtechniques:
- None recorded.

This profile does not prove maliciousness by itself. It explains how to read this catalog query's result shape and caveats.

## Expected Result Shape

- Endpoint answered in validation: yes
- Validation status: `completed`
- Observed row count: 157
- Row-count bucket: `high_101_1000`
- Returned labels:
- `sha256_hash_of_running_processes`

Observed columns:

| Label | Columns |
| --- | --- |
| `sha256_hash_of_running_processes` | `pid`, `name`, `path`, `cmdline`, `state`, `sha256` |

Label row counts:
- `sha256_hash_of_running_processes`: 157

## How To Read The Result

Observed validation result:

The endpoint answered and returned 157 rows in the validation run.

If rows are returned:

Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself.

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
- This query may be slow and produce large volume of results if the host has a high number of processes
- Query results are limited to processes that have a file on disk

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

The `process_hashes` catalog query (SHA256 Hash Of Running Processes) returned results that should be interpreted according to the catalog purpose and observed result shape. An answered endpoint with zero rows means no matching rows were returned for this exact query scope. Returned rows are endpoint evidence for the query condition or inventory shape, but they are not automatically a malicious verdict. A missing endpoint response is operationally different from zero rows and should be checked through target availability and job/result status.

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

Label: `sha256_hash_of_running_processes`

| `pid` | `name` | `path` | `cmdline` | `state` | `sha256` |
| --- | --- | --- | --- | --- | --- |
| <redacted:pid> | system_process.exe | C:\Windows\System32\system_process.exe | <redacted:system-command-line> | STILL_ACTIVE | <redacted:sha256-64-hex> |
| <redacted:pid> | service_host_process.exe | C:\Windows\System32\service_host_process.exe | <redacted:service-command-line> | STILL_ACTIVE | <redacted:sha256-64-hex> |
| <redacted:pid> | application_process.exe | C:\Program Files\Vendor\Application\application_process.exe | <redacted:application-command-line> | STILL_ACTIVE | <redacted:sha256-64-hex> |
