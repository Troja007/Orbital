# Linux Stock Catalog Result Profiles

Generated from a sanitized local Linux catalog validation run.

This file is GitHub-safe project context. It does not include endpoint result rows, hostnames, target selectors, Job IDs, raw API responses, tenant data, credentials, or customer-identifying values.

## Summary

- Catalog entries profiled: 64
- Completed in runner: 64
- Completed by documented direct verification: 0
- Entries with query/API/endpoint caveat classes: 1
- High or very high row-count profiles: 13

## Row Count Buckets

- `zero`: 18
- `low_1_10`: 20
- `medium_11_100`: 13
- `high_101_1000`: 6
- `very_high_over_1000`: 7

## How To Use

- Use this as interpretation context before explaining Orbital catalog results to an incident responder.
- Match by Catalog `ID` first, then by `title` if needed.
- Treat row counts as validation-run shape information, not as customer or fleet baseline data.
- For zero-row detection-oriented checks, explain this as no returned evidence for the exact catalog condition after the endpoint answered.
- For event-log checks, explain that empty results depend on available logs and retention.
- For high-volume profiles, narrow query parameters or target scope before broad use.
- For entries with `error_class`, resolve the caveat before relying on the result profile operationally.

## Profile Table

| Catalog ID | Title | Status | Rows | Bucket | Error class | Analyst reading |
| --- | --- | --- | ---: | --- | --- | --- |
| `chrome_extensions_monitoring` | Chrome Browser Extensions Monitoring | `completed` | 2 | `low_1_10` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `windows_intel_me_info` | Windows Intel ME/CSE Version | `completed` | 0 | `zero` | `` | Endpoint answered with no rows. Treat as no matching inventory/configuration/artifact data for this query shape on the tested endpoint. |
| `process_no_disk_binary` | Process Running Without A Binary On Disk | `completed` | 0 | `zero` | `` | Endpoint answered with no matching rows. For this catalog check, treat it as no evidence for the exact suspicious/vulnerable condition in the queried data scope. |
| `process_memory_allocation_parameterized_search` | Process Memory Allocation Search | `completed` | 0 | `zero` | `` | Endpoint answered with no matching rows. For this catalog check, treat it as no evidence for the exact suspicious/vulnerable condition in the queried data scope. |
| `windows_macos_linux_ssh_configs_monitoring` | SSH Configuration Monitoring | `completed` | 3 | `low_1_10` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `interface_ips` | Interface Names And Associated IPs | `completed` | 2 | `low_1_10` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `macos_linux_crontab_monitoring` | Crontab Monitoring | `completed` | 8 | `low_1_10` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `search_processes_by_listening_port` | Search Processes by Listening Port | `completed` | 0 | `zero` | `` | Endpoint answered with no matching rows. For this catalog check, treat it as no evidence for the exact suspicious/vulnerable condition in the queried data scope. |
| `macos_linux_shell_history_monitoring` | Shell History Monitoring | `completed` | 140 | `high_101_1000` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `cpuid_features_monitoring` | CPU Feature Search | `completed` | 69 | `medium_11_100` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `linux_log4j_monitoring` | Linux Log4j Monitoring | `completed` | 4 | `low_1_10` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `process_hashes` | SHA256 Hash Of Running Processes | `completed` | 182 | `high_101_1000` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `macos_linux_writable_suid_bin_monitoring` | Writable Suid Binaries Monitoring | `completed` | 0 | `zero` | `` | Endpoint answered with no matching rows. For this catalog check, treat it as no evidence for the exact suspicious/vulnerable condition in the queried data scope. |
| `unusual_executable_permissions_monitoring` | Unusual Executable Permissions Monitoring | `completed` | 0 | `zero` | `` | Endpoint answered with no rows. Treat as no matching inventory/configuration/artifact data for this query shape on the tested endpoint. |
| `root_processes_with_non_local_remote_ports` | Privileged Processes With Non-localhost Network Connections | `completed` | 2 | `low_1_10` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `logged_in_users` | Logged In Users | `completed` | 3 | `low_1_10` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `linux_openssl_vulnerabilities_monitoring` | Linux OpenSSL Vulnerable Versions Monitoring | `completed` | 0 | `zero` | `` | Endpoint answered with no matching rows. For this catalog check, treat it as no evidence for the exact suspicious/vulnerable condition in the queried data scope. |
| `etc_hosts_monitoring` | Hosts File Monitoring | `completed` | 6 | `low_1_10` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `process_children_parameterized_search` | Process Children Search | `completed` | 250 | `high_101_1000` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `system_info` | Inventory System Information | `completed` | 1 | `low_1_10` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `established_network_connections_search` | Process Socket Search | `completed` | 5 | `low_1_10` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `macos_linux_disk_encryption_monitoring` | Disk Encryption Status Monitoring | `completed` | 0 | `zero` | `` | Endpoint answered with no rows. Treat as no matching inventory/configuration/artifact data for this query shape on the tested endpoint. |
| `linux_kernel_modules_monitoring` | Kernel Modules Monitoring | `completed` | 77 | `medium_11_100` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `macos_linux_process_envs_monitoring` | Process Environment Variables Monitoring | `completed` | 4720 | `very_high_over_1000` | `` | Endpoint answered with a very large result set. Treat this as broad inventory/forensic output; narrow targets, parameters, paths, time windows, or labels before broad production use. |
| `user_accounts` | User Accounts Monitoring | `completed` | 46 | `medium_11_100` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `linux_webshell_china_chopper_monitoring` | Linux China Chopper Webshell Monitoring | `completed` | 0 | `zero` | `` | Endpoint answered with no matching rows. For this catalog check, treat it as no evidence for the exact suspicious/vulnerable condition in the queried data scope. |
| `linux_memory_info` | Memory Information Monitoring | `completed` | 1 | `low_1_10` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `process_parent_parameterized_search` | Process Parent Monitoring | `completed` | 31 | `medium_11_100` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `linux_rpm_package_files` | RPM Package Files Monitoring | `completed` | 0 | `zero` | `` | Endpoint answered with no rows. Treat as no matching inventory/configuration/artifact data for this query shape on the tested endpoint. |
| `file_parameterized_search` | File Search | `completed` | 28 | `medium_11_100` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `user_groups_monitoring` | User Groups Monitoring | `completed` | 82 | `medium_11_100` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `macos_linux_sudoers_monitoring` | Sudoers Monitoring | `completed` | 7 | `low_1_10` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `linux_shadow_monitoring` | Shadow File Monitoring | `completed` | 46 | `medium_11_100` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `macos_linux_usb_devices_monitoring` | USB Devices Monitoring | `completed` | 0 | `zero` | `` | Endpoint answered with no rows. Treat as no matching inventory/configuration/artifact data for this query shape on the tested endpoint. |
| `loaded_modules_monitoring` | Loaded Modules Monitoring | `completed` | 12300 | `very_high_over_1000` | `` | Endpoint answered with a very large result set. Treat this as broad inventory/forensic output; narrow targets, parameters, paths, time windows, or labels before broad production use. |
| `os_info` | Operating System Attributes | `completed` | 1 | `low_1_10` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `uptime_based_search` | Host Uptime Search | `completed` | 1 | `low_1_10` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `processes_with_network_connections` | Processes With Network Connections | `completed` | 5 | `low_1_10` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `macos_linux_bypass_security_using_env_variables_monitoring` | Security Bypass Using Environment Variables Monitoring | `completed` | 0 | `zero` | `` | Endpoint answered with no rows. Treat as no matching inventory/configuration/artifact data for this query shape on the tested endpoint. |
| `process_dll_parameterized_search` | Process Module Search | `completed` | 8186 | `very_high_over_1000` | `` | Endpoint answered with a very large result set. Treat this as broad inventory/forensic output; narrow targets, parameters, paths, time windows, or labels before broad production use. |
| `windows_macos_linux_process_not_running` | Find Hosts Where Certain Process not Running | `completed` | 0 | `zero` | `` | Endpoint answered with no rows. Treat as no matching inventory/configuration/artifact data for this query shape on the tested endpoint. |
| `macos_linux_known_hosts_monitoring` | Known Hosts Monitoring | `completed` | 0 | `zero` | `` | Endpoint answered with no rows. Treat as no matching inventory/configuration/artifact data for this query shape on the tested endpoint. |
| `macos_linux_mounts_monitoring` | System Mounted Devices And Filesystems Monitoring | `completed` | 38 | `medium_11_100` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `ip_address_of_active_interfaces` | IP Address of Active Interfaces | `completed` | 0 | `zero` | `` | Endpoint answered with no rows. Treat as no matching inventory/configuration/artifact data for this query shape on the tested endpoint. |
| `linux_pkexec_settings` | Linux pkexec Settings and Events Monitoring | `completed` | 5 | `low_1_10` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `linux_systemd_units_monitoring` | Systemd Units Monitoring | `completed` | 348 | `high_101_1000` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `forensic-snapshot-linux-0.0.9` | Forensic Snapshot Linux 0.0.9 | `completed` | 19102 | `very_high_over_1000` | `` | Endpoint answered with a very large result set. Treat this as broad inventory/forensic output; narrow targets, parameters, paths, time windows, or labels before broad production use. |
| `3cx_desktop_apps_compromise_monitoring` | 3CX Desktop App Vulnerable Versions Monitoring | `completed` | 0 | `zero` | `completed_with_query_or_endpoint_errors` | Endpoint answered, but one or more query blocks produced errors. Read label_errors/endpoint_errors before interpreting row counts. |
| `arp_cache_inspection` | ARP Cache Inspection | `completed` | 0 | `zero` | `` | Endpoint answered with no rows. Treat as no matching inventory/configuration/artifact data for this query shape on the tested endpoint. |
| `macos_linux_system_controls` | System Controls Monitoring | `completed` | 4409 | `very_high_over_1000` | `` | Endpoint answered with a very large result set. Treat this as broad inventory/forensic output; narrow targets, parameters, paths, time windows, or labels before broad production use. |
| `macos_linux_configuration_files_modification_monitoring` | Configuration Files Modification Monitoring | `completed` | 70 | `medium_11_100` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `network_connection_listening` | Listening Ports Monitoring | `completed` | 3 | `low_1_10` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `linux_iptables_monitoring` | IP Tables Configuration Monitoring | `completed` | 0 | `zero` | `` | Endpoint answered with no rows. Treat as no matching inventory/configuration/artifact data for this query shape on the tested endpoint. |
| `macos_linux_process_open_files_monitoring` | Process Open Files Monitoring | `completed` | 903 | `high_101_1000` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `python_packages_param_search` | Python Packages Search | `completed` | 59 | `medium_11_100` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `windows_macos_linux_firefox_addons_monitoring` | Firefox Addons Monitoring | `completed` | 15 | `medium_11_100` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `system-snapshot-linux-0.0.9` | System Snapshot Linux 0.0.9 (formerly Forensic Snapshot Linux 0.0.9) | `completed` | 19100 | `very_high_over_1000` | `` | Endpoint answered with a very large result set. Treat this as broad inventory/forensic output; narrow targets, parameters, paths, time windows, or labels before broad production use. |
| `macos_linux_last_logins_logouts_monitoring` | Logins/Logouts Monitoring | `completed` | 1 | `low_1_10` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `process_data_parameterized_search` | Process Data Search | `completed` | 252 | `high_101_1000` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `macos_linux_dns_resolvers_monitoring` | DNS Resolvers Monitoring | `completed` | 2 | `low_1_10` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `linux_hidden_files_and_directories_in_home` | Hidden Files And Directories Monitoring | `completed` | 23 | `medium_11_100` | `` | Endpoint answered with rows. Review each row as potential evidence for the catalog condition, then validate against context, timestamps, paths, users, signatures, and related follow-up queries. |
| `linux_deb_packages_monitoring` | Debian Packages Monitoring | `completed` | 1721 | `very_high_over_1000` | `` | Endpoint answered with a very large result set. Treat this as broad inventory/forensic output; narrow targets, parameters, paths, time windows, or labels before broad production use. |
| `user_groups_search` | Users Group Search | `completed` | 55 | `medium_11_100` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
| `linux_apt_sources_monitoring` | APT Sources Monitoring | `completed` | 10 | `low_1_10` | `` | Endpoint answered with rows. Interpret rows according to the catalog description: often inventory, posture, configuration, or forensic context rather than malicious evidence by itself. |
