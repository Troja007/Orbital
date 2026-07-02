# Orbital Query Method Memory

Generated: 2026-06-12

Purpose: summarize reusable Orbital/osquery query-method memory. This report stores method context only. It does not store endpoint result rows, hostnames, usernames, IP addresses, GUIDs, customer names, bearer tokens, raw API responses, or raw investigation output.

Source of truth:

```text
02_Working_Files/query-method-memory/
```

## Method Index

| Method | Status | Category | Platforms | Tables | Primary Catalog Context | Orbital Catalog Categories | MITRE TTP Summary |
|---|---:|---|---|---|---|---|---|
| Inventory Orbital computer names | tested | orbital_health | cross-platform | `system_info` | `Inventory System Information` / `system_info` | `Posture Assessment`; related `Forensics`, `Live Acquisition Of Volatile Data` | related `TA0005` |
| Inventory endpoint operating systems | tested | orbital_health | cross-platform | `os_version`, `system_info` | `Operating System Attributes` / `os_info`; `Inventory System Information` / `system_info` | `Posture Assessment`; `Forensics`; `Live Acquisition Of Volatile Data` | related `TA0002`, `TA0004`, `TA0005`, `TA0006`, `TA0007`, `TA0008`, `T1068`, `T1082`, `T1135`, `T1203`, `T1210`, `T1212` |
| Multiple SQL statements in Orbital catalog and API requests | validated | orbital_catalog | cross-platform | `processes`, `arp_cache` in sanitized example | redacted organization catalog example; Cisco DevNet request schema context | not applicable | not applicable |
| Check endpoints for non-default hosts file entries | tested | network | cross-platform | `etc_hosts`, `system_info` | `Hosts File Monitoring` / `etc_hosts_monitoring` | `Posture Assessment`; related `Forensics`, `Live Acquisition Of Volatile Data` | `TA0011`, `T1008`, `T1102` |
| Query Windows endpoint DNS cache | tested | network | Windows | `dns_cache`, `system_info` | `DNS Cache Monitoring` / `dns_cache_table_monitoring` | catalog context stored in method record | catalog context stored in method record |
| Query Windows port 443 network connections | tested | network | Windows | `process_open_sockets`, `processes`, `system_info` | `Process Socket Search` / `established_network_connections_search`; `Processes With Network Connections` / `processes_with_network_connections` | `Threat Hunting`; `Posture Assessment`; `Live Acquisition Of Volatile Data` | `TA0011`, `T1102`, `T1219`, `T1071`, `T1571` |
| Query Cisco Secure Endpoint Host Based Firewall events and communication on Windows | tested | network | Windows | `windows_eventlog`, `process_open_sockets`, `processes`, `windows_firewall_rules` | local custom firewall event queries; organization CiscoSecureEndpoint/Events query context; Windows port 443 method | `Network`; related `Threat Hunting`, `Live Acquisition Of Volatile Data` | related `TA0011`, `T1071`, `T1571` |
| Check macOS Cisco Secure Client NVM package receipt | tested | software | macOS | `package_receipts` | No exact local Orbital Catalog match found | No exact local catalog category found | No exact local MITRE mapping found |
| Verify Cisco Secure Endpoint presence before querying Secure Endpoint event logs | draft | software | Windows | `processes`, `programs`, `services`, `file`, `registry`, `windows_eventlog` | `Installed Programs Search` / `installed_programs_param_search`; local `sfc.exe` and Cisco-path process methods | `Posture Assessment`; `Live Acquisition Of Volatile Data` | no exact MITRE mapping; related table context only |
| Running process SHA256 from catalog | draft | suspicious_processes | cross-platform | `processes`, `hash` | `SHA256 Hash Of Running Processes` / `process_hashes` | `Live Acquisition Of Volatile Data`; related `Threat Hunting`, `Posture Assessment`, `Forensics` | related process/hash TTP context stored in method record |
| Windows `sfc.exe` running process lookup | tested | suspicious_processes | Windows | `processes`, `system_info` | organization process patterns; related `process_hashes`; `system_info` | `Threat Hunting`; `Posture Assessment`; `Live Acquisition Of Volatile Data` | related `TA0002`, `TA0004`, `TA0005`, `TA0011`, `T1036`, `T1055`, `T1055.012`, `T1071`, `T1102`, `T1219`, `T1571` |
| Windows Cisco path running processes | tested | suspicious_processes | Windows | `processes`, `system_info` | organization Secure Endpoint / Secure Client process context | see method record | see method record |
| Windows Secure Endpoint Exploit Prevention protector DLL | tested | suspicious_processes | Windows | see method record | see method record | see method record | see method record |

Report sync notes:

- The index now reflects all YAML method records currently stored under `02_Working_Files/query-method-memory/`.
- Added the missing Secure Endpoint Host Based Firewall event/communication method.
- Added the missing Secure Endpoint presence pre-check method.
- Updated stale statuses for the `sfc.exe` method and the multiple-SQL catalog/API method.

## New Knowledge Added On 2026-06-12

### Check macOS Cisco Secure Client NVM package receipt

Record:

```text
02_Working_Files/query-method-memory/software/macos_secure_client_nvm_package_receipt.yaml
```

Goal: determine whether Cisco Secure Client Network Visibility Module appears installed on macOS by package receipt.

Tables:

- `package_receipts`

Validated osquery columns:

- `package_id`
- `version`
- `install_time`

SQL pattern:

```sql
SELECT
  'Cisco Network Visibility Module' AS module,
  'Installed' AS status,
  package_id,
  version
FROM package_receipts
WHERE LOWER(package_id) LIKE '%cisco%'
  AND (
    LOWER(package_id) LIKE '%nvm%'
    OR LOWER(package_id) LIKE '%network%visibility%'
  )
ORDER BY install_time DESC
LIMIT 1;
```

Orbital guidance:

- macOS-only method; use `darwin` OS targeting/filtering.
- Do not use for Windows or Linux.
- No live query was executed during this update because no macOS system was running.
- Package receipt evidence indicates installation, not runtime health or telemetry collection state.

Catalog and MITRE context:

- No exact local Orbital Catalog query match for `package_receipts` or macOS Secure Client NVM package receipts was found.
- No exact local Orbital Catalog category or MITRE mapping was found for this table.
- Do not infer detection coverage from this software inventory query.

Reusable lessons:

- Use `package_receipts` for lightweight macOS package-installation checks.
- Follow up with process, launch daemon, file, or service checks if operational state matters.

## Cross-Method Rules

- Use `orbital-query-method-memory` first when a request involves query design, prior methods, table choice, catalog reuse, or repeated investigation patterns.
- Use `orbital-api-access` when catalog/API context needs refresh, authentication checking, or raw catalog metadata.
- Use `orbital-run-osquery-live-query` only after SQL, targets, OS filters, and broad-scope approval are clear.
- Return to query-method memory after execution to store method-only lessons, table choices, categories, and MITRE context.
- Never store endpoint result rows in query memory.

## Privacy Rule

Query memory may store:

- analyst input pattern
- sanitized SQL pattern
- osquery tables and columns
- Orbital Catalog `Name` and `ID`
- catalog categories
- MITRE TTP context
- performance and targeting lessons

Query memory must not store:

- returned endpoint rows
- hostnames
- usernames
- IP addresses
- Orbital IDs
- Secure Endpoint GUIDs
- Secure Client GUIDs
- AnyConnect UDIDs
- customer names
- bearer tokens
- raw API responses
