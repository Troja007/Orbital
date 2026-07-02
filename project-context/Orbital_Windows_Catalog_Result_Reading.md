# Orbital Windows Catalog Result Reading

Validated from a controlled Windows stock catalog execution against one Windows endpoint on 2026-06-15/2026-06-16. This file records interpretation guidance, not endpoint evidence.

GitHub-synced sanitized per-query result profiles generated from this validation are stored under `queries_and_scripts/catalog_result_profiles/`. Use those profiles when a future agent or analyst needs to explain what an Orbital catalog query result means for a specific Catalog `ID`.

Raw operational validation files remain local-only under `local/orbital_catalog_windows_validation/` and must not be pushed because they can contain target selectors, Job IDs, raw API fragments, or other operational identifiers.

## Execution Summary

- Scope: active Windows-related stock catalog queries from the imported Orbital Catalog API file.
- Targeting model used for validation: one explicit host selector.
- Total catalog entries selected: 384.
- Completed catalog entries: 383 from the consolidated runner output.
- Additional direct Job ID verification: `registry_safe_dll_search_monitoring` had an API result-fetch error in the runner, but the existing Job ID returned successfully with 0 rows when checked directly.
- Endpoint stability: the endpoint continued to answer through the full sequence when queries were spaced by 30 seconds.

## Result Interpretation

Treat these states differently:

- `completed` with `row_count = 0`: the endpoint answered and no matching rows were returned. This is not the same as query failure.
- For catalog entries that explicitly search for malicious, vulnerable, suspicious, or unwanted conditions, `row_count = 0` can be read as "no endpoint matched this specific condition in the queried data scope." This is a no-hit result for that catalog check, not a global proof that the endpoint is unaffected by all related attack activity.
- `completed` with rows: the query returned matching data, but the catalog title determines whether rows are normal inventory, posture context, forensic artifact data, or likely suspicious evidence.
- `completed` with `endpoint_errors`: the endpoint answered, but one or more SQL blocks failed. Inspect `label_errors` before interpreting row counts.
- API HTTP error with a Job ID: the query may still have run. Re-check the existing Job ID before assuming endpoint failure.
- Missing endpoint response: stop the sequence and inspect the last Job ID before launching additional work.

## Observed Catalog Compatibility Issues

Two Windows catalog entries completed at the job level but failed inside osquery on the endpoint because the query expected a column not available in the endpoint's Orbital/osquery runtime:

- `eqnedt32_child_processes_monitoring`: `no such column: p.is_elevated_token`
- `windows_hh_process_monitoring`: `no such column: is_elevated_token`

For these catalog entries, validate the local Orbital/osquery schema before relying on them. If the column is unavailable, adapt the query or treat the catalog entry as incompatible with that endpoint runtime.

## High-Volume Query Patterns

Some catalog entries are intentionally broad and can return thousands of rows with default parameters. Use them carefully on broad targets:

- Full snapshots: `forensic-snapshot-windows-0.0.9`, `system-snapshot-windows-0.0.9`
- Module/process inventory: `loaded_modules_monitoring`, `process_dll_parameterized_search`
- Broad file/registry/certificate searches: `file_parameterized_search`, `registry_parameterized_search`, `valid_certificate_param_search`
- Temporary files and service inventory: `temp_directories_monitoring`, `running_services_search`, `running_services_search_by_path`

For production investigations, narrow these with parameters, host selectors, time windows, paths, process names, hashes, registry paths, or other constraints before using broad endpoint groups.

## Timing Guidance

The 30-second inter-query delay prevented overload in this validation run. Some catalog entries can return after the first polling window but still complete later. Keep the Job ID and re-check existing job results before treating slow responses as failures.

Observed slow or larger-result examples:

- `windows_shortcut_files_monitoring` completed only after a longer wait and returned hundreds of rows.
- `auto_execs` returned the maximum observed catalog cap-style volume in this run and should be treated as potentially expensive.
- Snapshot and loaded-module catalog entries can produce very large result sets and should not be run broadly without a clear reason.

## Analyst Reading Rules

- Read catalog `description`, `warnings`, MITRE mappings, and category before interpreting result rows.
- A row from an inventory or baseline query is not automatically malicious.
- For malicious-activity, vulnerability, or suspicious-behavior catalog checks, 0 rows usually means the endpoint is not affected by the exact condition the query checks, assuming the endpoint answered successfully and the relevant telemetry source is available.
- Event-log queries with 0 rows usually mean no matching event was found in available logs, not proof that the behavior never happened.
- Registry artifact queries often show configuration or history; validate suspiciousness against path, value, timestamp, signature, service state, and process context.
- Historical artifact queries, such as connected networks or ShimCache, should not be read as live state.
- Multi-query catalog entries return per-label results. Check each label's row count, columns, and errors separately.
- Preserve the execution-specific `orbital_queryID` for follow-up, but do not confuse it with Catalog `ID` or the `queryId:<id>` target selector.
