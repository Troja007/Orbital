# Forensic Snapshot Windows 0.0.9

## Catalog Identity

- Catalog ID: `forensic-snapshot-windows-0.0.9`
- Catalog name: `Forensic Snapshot Windows 0.0.9`
- Platform: windows
- Profile type: sanitized catalog result profile
- Source run: 2026-06-15/2026-06-16
- Catalog updated: 2025-08-21T21:45:00Z

## What This Query Answers

Use the catalog name, categories, MITRE mapping, and returned columns to decide whether this query is detection-oriented, inventory-oriented, posture-oriented, or forensic context.

Categories:
- `forensics`
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
- Observed row count: 15841
- Row-count bucket: `very_high_over_1000`
- Returned labels:
- `bitlocker_encryption_monitoring`
- `chrome_extensions_monitoring`
- `connected_networks_history_monitoring`
- `dns_cache_table_monitoring`
- `installed_programs_on_windows_host`
- `interface_names_and_associated_ips`
- `listening_ports`
- `loaded_modules_hashes`
- `loaded_modules_processes`
- `loaded_modules_vs_processes`
- `logged_in_users`
- `logon_sessions_monitoring`
- `mapped_drives`
- `operating_system_attributes`
- `powershell_history`
- `process_running_without_a_binary_on_disk`
- `processes_with_network_connections`
- `running_services_monitoring`
- `scheduled_tasks_monitoring`
- `sha256_hash_of_running_processes`
- `shared_resources_monitoring`
- `startup_items`
- `system_network_state_monitoring`
- `temp_directories_monitoring`
- `trusted_root_certificates_monitoring`
- `user_accounts`
- `user_groups_monitoring`
- `userassist_monitoring`
- `windows_av_products_monitoring`
- `windows_bam_entries_monitoring`
- `windows_environment_variables_monitoring`
- `windows_executables_that_automatically_execute`
- `windows_hotfixes`
- `windows_nt_domains_search`
- `windows_prefetch_directory`
- `windows_shellbags_monitoring`
- `windows_shimcache_monitoring`
- `wmi_event_filters_monitoring`

Observed columns:

| Label | Columns |
| --- | --- |
| `bitlocker_encryption_monitoring` | `device_id`, `drive_letter`, `persistent_volume_id`, `conversion_status`, `protection_status`, `encryption_method` |
| `chrome_extensions_monitoring` | `username`, `name`, `identifier`, `version`, `description`, `locale`, `update_url`, `persistent`, `path` |
| `connected_networks_history_monitoring` | `name`, `data`, `last_modified` |
| `dns_cache_table_monitoring` | `domain`, `type` |
| `installed_programs_on_windows_host` | `name`, `version`, `install_location`, `install_source`, `language`, `publisher`, `uninstall_string`, `install_date` |
| `interface_names_and_associated_ips` | `interface`, `address`, `mask`, `type`, `friendly_name` |
| `listening_ports` | `name`, `path`, `address`, `protocol`, `port` |
| `loaded_modules_hashes` | `module_id`, `sha256`, `module_path` |
| `loaded_modules_processes` | `pid`, `process_name`, `process_path` |
| `loaded_modules_vs_processes` | `module_id`, `pid` |
| `logged_in_users` | `user`, `login_type`, `device_name`, `remote_hostname`, `time`, `pid`, `sid` |
| `logon_sessions_monitoring` | `user`, `logon_domain`, `authentication_package`, `logon_type`, `logon_time`, `logon_server`, `dns_domain_name`, `upn`, `logon_script`, `profile_path`, `home_directory`, `home_directory_drive` |
| `mapped_drives` | `device_id`, `type`, `free_space`, `size`, `file_system`, `boot_partition`, `encryption_method` |
| `operating_system_attributes` | `name`, `version`, `major`, `minor`, `patch`, `build`, `platform`, `codename`, `install_date` |
| `powershell_history` | `time`, `datetime`, `script_block_id`, `script_block_count`, `script_text`, `script_name`, `script_path` |
| `process_running_without_a_binary_on_disk` | `pid`, `name`, `path`, `cmdline`, `state` |
| `processes_with_network_connections` | `pid`, `name`, `cmdline`, `local_address`, `local_port`, `remote_address`, `remote_port` |
| `running_services_monitoring` | `name`, `service_type`, `display_name`, `status`, `pid`, `start_type`, `win32_exit_code`, `service_exit_code`, `path`, `module_path`, `description`, `user_account` |
| `scheduled_tasks_monitoring` | `name`, `action`, `path`, `enabled`, `state`, `hidden`, `last_run_time`, `next_run_time`, `last_run_message`, `last_run_code` |
| `sha256_hash_of_running_processes` | `pid`, `name`, `path`, `cmdline`, `state`, `owner_uid`, `owner_username`, `sha256` |
| `shared_resources_monitoring` | `description`, `install_date`, `status`, `allow_maximum`, `maximum_allowed`, `name`, `path`, `type` |
| `startup_items` | `name`, `path`, `args`, `source`, `type`, `status`, `username` |
| `system_network_state_monitoring` | `disconnected`, `ipv4_no_traffic`, `ipv6_no_traffic`, `ipv4_subnet`, `ipv4_local_network`, `ipv4_internet`, `ipv6_subnet`, `ipv6_local_network`, `ipv6_internet` |
| `temp_directories_monitoring` | `path`, `filename`, `sha256`, `uid`, `gid`, `mode`, `size`, `last_access_time`, `last_modified`, `last_status_change_time`, `creation_time`, `hard_links`, `symlink`, `type` |
| `trusted_root_certificates_monitoring` | `common_name`, `subject`, `issuer`, `ca`, `self_signed`, `Not Valid Before`, `Not Valid After`, `sha1`, `serial`, `sid`, `username` |
| `user_accounts` | `uid`, `gid`, `username`, `description`, `directory`, `shell`, `uuid`, `type` |
| `user_groups_monitoring` | `groupname`, `username`, `comment` |
| `userassist_monitoring` | `path`, `last_execution_time`, `count`, `sid` |
| `windows_av_products_monitoring` | `displayName`, `Path To Signed Executable`, `Path To Signed Reporting Executable` |
| `windows_bam_entries_monitoring` | `path`, `last_execution_time`, `sid` |
| `windows_environment_variables_monitoring` | `name`, `value` |
| `windows_executables_that_automatically_execute` | `name`, `path`, `source`, `sha256` |
| `windows_hotfixes` | `hotfix_id`, `caption`, `description`, `fix_comments`, `installed_by`, `install_date`, `installed_on` |
| `windows_nt_domains_search` | `name`, `client_site_name`, `dc_site_name`, `dns_forest_name`, `domain_controller_address`, `domain_controller_name`, `domain_name`, `status` |
| `windows_prefetch_directory` | `filename`, `path`, `uid`, `gid`, `last_access_time`, `last_modification_time`, `last_status_change_time`, `create_time`, `hard_links`, `symlink`, `type`, `attributes`, `volume_serial`, `file_id` |
| `windows_shellbags_monitoring` | `username`, `sid`, `source`, `directory_name`, `directory_modified_time`, `directory_created_time`, `directory_accessed_time`, `mft_entry`, `mft_sequence` |
| `windows_shimcache_monitoring` | `entry`, `path`, `modified_time`, `sha256` |
| `wmi_event_filters_monitoring` | `name`, `query`, `class`, `relative_path` |

Label row counts:
- `bitlocker_encryption_monitoring`: 1
- `chrome_extensions_monitoring`: 10
- `connected_networks_history_monitoring`: 20
- `dns_cache_table_monitoring`: 85
- `installed_programs_on_windows_host`: 31
- `interface_names_and_associated_ips`: 1
- `listening_ports`: 11
- `loaded_modules_hashes`: 1921
- `loaded_modules_processes`: 157
- `loaded_modules_vs_processes`: 8183
- `logged_in_users`: 1
- `logon_sessions_monitoring`: 11
- `mapped_drives`: 3
- `operating_system_attributes`: 1
- `powershell_history`: 459
- `process_running_without_a_binary_on_disk`: 2
- `processes_with_network_connections`: 8
- `running_services_monitoring`: 681
- `scheduled_tasks_monitoring`: 239
- `sha256_hash_of_running_processes`: 186
- `shared_resources_monitoring`: 4
- `startup_items`: 12
- `system_network_state_monitoring`: 1
- `temp_directories_monitoring`: 1141
- `trusted_root_certificates_monitoring`: 42
- `user_accounts`: 9
- `user_groups_monitoring`: 21
- `userassist_monitoring`: 122
- `windows_av_products_monitoring`: 2
- `windows_bam_entries_monitoring`: 76
- `windows_environment_variables_monitoring`: 37
- `windows_executables_that_automatically_execute`: 1000
- `windows_hotfixes`: 10
- `windows_nt_domains_search`: 2
- `windows_prefetch_directory`: 239
- `windows_shellbags_monitoring`: 87
- `windows_shimcache_monitoring`: 1024
- `wmi_event_filters_monitoring`: 1

## How To Read The Result

Observed validation result:

The endpoint answered and returned 15841 rows in the validation run.

If rows are returned:

Endpoint answered with a very large result set. Treat this as broad inventory/forensic output; narrow targets, parameters, paths, time windows, or labels before broad production use.

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
- This query can result in excessive amounts of data.

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

The `forensic-snapshot-windows-0.0.9` catalog query (Forensic Snapshot Windows 0.0.9) returned results that should be interpreted according to the catalog purpose and observed result shape. An answered endpoint with zero rows means no matching rows were returned for this exact query scope. Returned rows are endpoint evidence for the query condition or inventory shape, but they are not automatically a malicious verdict. A missing endpoint response is operationally different from zero rows and should be checked through target availability and job/result status.

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