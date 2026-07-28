# System Snapshot Linux 0.0.9 (formerly Forensic Snapshot Linux 0.0.9)

## Catalog Identity

- Catalog ID: `system-snapshot-linux-0.0.9`
- Catalog name: `System Snapshot Linux 0.0.9 (formerly Forensic Snapshot Linux 0.0.9)`
- Platform: linux
- Profile type: sanitized catalog result profile
- Source run: 2026-07-28
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
- Observed row count: 19100
- Row-count bucket: `very_high_over_1000`
- Returned labels:
- `arp_cache`
- `chrome_extensions_monitoring`
- `crontab`
- `disk_encryption_monitoring`
- `etc_protocols`
- `etc_services`
- `hosts_file`
- `interface_names_and_associated_ips`
- `linux_kernel_modules_monitoring`
- `linux_systemd_units_monitoring`
- `listening_ports`
- `loaded_modules_hashes`
- `loaded_modules_processes`
- `loaded_modules_vs_processes`
- `logged_in_users`
- `macos_linux_dns_resolvers_monitoring`
- `macos_linux_last_logins_logouts_monitoring`
- `macos_linux_process_envs_monitoring`
- `macos_linux_sudoers_monitoring`
- `mounted_devices_monitoring`
- `operating_system_attributes`
- `platform_information`
- `processes_with_network_connections`
- `sha256_hash_of_running_processes`
- `shadow`
- `shell_history`
- `ssh_configs_monitoring`
- `startup_items`
- `system_information`
- `user_accounts`
- `user_groups_monitoring`

Observed columns:

| Label | Columns |
| --- | --- |
| `arp_cache` | `address`, `mac`, `interface`, `permanent` |
| `chrome_extensions_monitoring` | `username`, `name`, `identifier`, `version`, `description`, `locale`, `update_url`, `persistent`, `path` |
| `crontab` | `event`, `minute`, `hour`, `day_of_month`, `month`, `day_of_week`, `command`, `path` |
| `disk_encryption_monitoring` | `name`, `uuid`, `encrypted`, `type`, `username`, `user_uuid`, `encryption_status` |
| `etc_protocols` | `name`, `number`, `alias`, `comment` |
| `etc_services` | `name`, `port`, `protocol`, `aliases`, `comment` |
| `hosts_file` | `address`, `hostnames` |
| `interface_names_and_associated_ips` | `interface`, `address`, `mask`, `type`, `friendly_name` |
| `linux_kernel_modules_monitoring` | `name`, `size`, `used_by`, `status`, `address` |
| `linux_systemd_units_monitoring` | `id`, `description`, `load_state`, `active_state`, `sub_state`, `following`, `object_path`, `job_id`, `job_type`, `job_path`, `fragment_path`, `user`, `source_path` |
| `listening_ports` | `name`, `path`, `address`, `protocol`, `port` |
| `loaded_modules_hashes` | `module_id`, `sha256`, `module_path` |
| `loaded_modules_processes` | `pid`, `process_name`, `process_path` |
| `loaded_modules_vs_processes` | `module_id`, `pid` |
| `logged_in_users` | `user`, `login_type`, `device_name`, `remote_hostname`, `time`, `pid`, `sid` |
| `macos_linux_dns_resolvers_monitoring` | `id`, `type`, `ip`, `netmask`, `options` |
| `macos_linux_last_logins_logouts_monitoring` | `username`, `tty`, `pid`, `process name`, `type`, `entry timestamp`, `hostname` |
| `macos_linux_process_envs_monitoring` | `Process Name`, `pid`, `Environment Variable Name`, `Environment Variable Value` |
| `macos_linux_sudoers_monitoring` | `source`, `header`, `rule_details` |
| `mounted_devices_monitoring` | `device`, `device_alias`, `path`, `type`, `blocks_size`, `blocks`, `blocks_free`, `blocks_available`, `inodes`, `inodes_free`, `flags` |
| `operating_system_attributes` | `name`, `version`, `major`, `minor`, `patch`, `build`, `platform`, `codename`, `install_date` |
| `platform_information` | `vendor`, `version`, `date`, `revision`, `address`, `size`, `volume_size`, `extra` |
| `processes_with_network_connections` | `pid`, `name`, `cmdline`, `local_address`, `local_port`, `remote_address`, `remote_port` |
| `sha256_hash_of_running_processes` | `pid`, `name`, `path`, `cmdline`, `state`, `sha256` |
| `shadow` | `password_status`, `hash_alg`, `last_change`, `min`, `max`, `warning`, `inactive`, `expire`, `username` |
| `shell_history` | `username`, `time`, `command`, `history_file` |
| `ssh_configs_monitoring` | `username`, `block`, `option`, `ssh_config_file`, `sha256` |
| `startup_items` | `name`, `path`, `args`, `source`, `type`, `status`, `username` |
| `system_information` | `hostname`, `local_hostname`, `cpu_type`, `cpu_subtype`, `cpu_brand`, `physical_memory` |
| `user_accounts` | `uid`, `gid`, `username`, `description`, `directory`, `shell`, `uuid`, `type` |
| `user_groups_monitoring` | `groupname`, `username`, `comment` |

Label row counts:
- `arp_cache`: 2
- `chrome_extensions_monitoring`: 2
- `crontab`: 8
- `disk_encryption_monitoring`: 12
- `etc_protocols`: 55
- `etc_services`: 536
- `hosts_file`: 6
- `interface_names_and_associated_ips`: 2
- `linux_kernel_modules_monitoring`: 77
- `linux_systemd_units_monitoring`: 348
- `listening_ports`: 3
- `loaded_modules_hashes`: 1058
- `loaded_modules_processes`: 252
- `loaded_modules_vs_processes`: 11019
- `logged_in_users`: 3
- `macos_linux_dns_resolvers_monitoring`: 2
- `macos_linux_last_logins_logouts_monitoring`: 1
- `macos_linux_process_envs_monitoring`: 4720
- `macos_linux_sudoers_monitoring`: 7
- `mounted_devices_monitoring`: 38
- `operating_system_attributes`: 1
- `platform_information`: 1
- `processes_with_network_connections`: 5
- `sha256_hash_of_running_processes`: 182
- `shadow`: 46
- `shell_history`: 140
- `ssh_configs_monitoring`: 3
- `startup_items`: 442
- `system_information`: 1
- `user_accounts`: 46
- `user_groups_monitoring`: 82

## How To Read The Result

Observed validation result:

The endpoint answered and returned 19100 rows in the validation run.

If rows are returned:

Endpoint answered with a very large result set. Treat this as broad inventory/forensic output; narrow targets, parameters, paths, time windows, or labels before broad production use.

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

The `system-snapshot-linux-0.0.9` catalog query (System Snapshot Linux 0.0.9 (formerly Forensic Snapshot Linux 0.0.9)) returned results that should be interpreted according to the catalog purpose and observed result shape. An answered endpoint with zero rows means no matching rows were returned for this exact query scope. Returned rows are endpoint evidence for the query condition or inventory shape, but they are not automatically a malicious verdict. A missing endpoint response is operationally different from zero rows and should be checked through target availability and job/result status.

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

Label: `arp_cache`

| `address` | `interface` | `mac` | `permanent` |
| --- | --- | --- | --- |
| <redacted:ip> | <redacted:sensitive-value> | <redacted:ip> | <redacted:sensitive-value> |

Label: `chrome_extensions_monitoring`

| `description` | `identifier` | `locale` | `name` | `path` | `persistent` | `update_url` | `username` | `version` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <path> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:username> | <redacted:ip> |

Label: `crontab`

| `command` | `day_of_month` | `day_of_week` | `event` | `hour` | `minute` | `month` | `path` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <path> | <redacted:sensitive-value> | <redacted:sensitive-value> | <empty> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <path> |

Label: `disk_encryption_monitoring`

| `encrypted` | `encryption_status` | `name` | `type` | `user_uuid` | `username` | `uuid` |
| --- | --- | --- | --- | --- | --- | --- |
| <redacted:sensitive-value> | <state-category> | <path> | <empty> | <redacted:username> | <redacted:username> | <redacted:guid> |

Label: `etc_protocols`

| `alias` | `comment` | `name` | `number` |
| --- | --- | --- | --- |
| <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> |

Label: `etc_services`

| `aliases` | `comment` | `name` | `port` | `protocol` |
| --- | --- | --- | --- | --- |
| <empty> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> |

Label: `hosts_file`

| `address` | `hostnames` |
| --- | --- |
| <redacted:ip> | <redacted:hostname> |

Label: `interface_names_and_associated_ips`

| `address` | `friendly_name` | `interface` | `mask` | `type` |
| --- | --- | --- | --- | --- |
| <redacted:ip> | <empty> | <redacted:sensitive-value> | <redacted:ip> | <redacted:sensitive-value> |

Label: `linux_kernel_modules_monitoring`

| `address` | `name` | `size` | `status` | `used_by` |
| --- | --- | --- | --- | --- |
| <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <state-category> | <redacted:sensitive-value> |

Label: `linux_systemd_units_monitoring`

| `active_state` | `description` | `following` | `fragment_path` | `id` | `job_id` | `job_path` | `job_type` | `load_state` | `object_path` | `source_path` | `sub_state` | `user` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <state-category> | <redacted:sensitive-value> | <empty> | <empty> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:sensitive-value> | <state-category> | <path> | <empty> | <state-category> | <redacted:username> |

Label: `listening_ports`

| `address` | `name` | `path` | `port` | `protocol` |
| --- | --- | --- | --- | --- |
| <redacted:ip> | <redacted:sensitive-value> | <path> | <redacted:sensitive-value> | <redacted:sensitive-value> |

Label: `loaded_modules_hashes`

| `module_id` | `module_path` | `sha256` |
| --- | --- | --- |
| <redacted:sensitive-value> | <path> | <hash:64-hex> |

Label: `loaded_modules_processes`

| `pid` | `process_name` | `process_path` |
| --- | --- | --- |
| <redacted:sensitive-value> | <process-name> | <path> |

Label: `loaded_modules_vs_processes`

| `module_id` | `pid` |
| --- | --- |
| <redacted:sensitive-value> | <redacted:sensitive-value> |

Label: `logged_in_users`

| `device_name` | `login_type` | `pid` | `remote_hostname` | `sid` | `time` | `user` |
| --- | --- | --- | --- | --- | --- | --- |
| <redacted:hostname> | <redacted:sensitive-value> | <redacted:sensitive-value> | <redacted:hostname> | <redacted:username> | <timestamp:iso-8601> | <redacted:username> |

Additional source rows were omitted to preserve privacy and the 15-row limit.