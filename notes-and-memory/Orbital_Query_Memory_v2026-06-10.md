# Orbital Query Memory v2026-06-10

Generated: 2026-06-10 17:55:43 CEST

Purpose: summarize reusable Orbital/osquery query-method memory. This report stores method context only. It does not store endpoint result rows, hostnames, usernames, IP addresses, GUIDs, customer names, bearer tokens, raw API responses, or raw investigation output.

## Source Of Truth

Reusable method records live under:

```text
02_Working_Files/query-method-memory/
```

Template:

```text
02_Working_Files/query-method-memory/_template.yaml
```

## Method Index

| Method | Status | Category | Platforms | Tables | Primary Catalog Context | Orbital Catalog Categories | MITRE TTP Summary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Check endpoints for non-default hosts file entries` | tested | network | cross_platform | `etc_hosts`, `system_info` | `Hosts File Monitoring` / `etc_hosts_monitoring` | `Posture Assessment`; `Forensics`; `Live Acquisition Of Volatile Data` | `TA0011` Command and Control; `T1008` Fallback Channels; `T1102` Web Service |
| `Inventory Orbital computer names` | tested | orbital_health | cross_platform | `system_info` | `Inventory System Information` / `system_info` | `Posture Assessment`; `Forensics`; `Live Acquisition Of Volatile Data` | Related context: `TA0005` Defense Evasion |
| `Inventory operating systems on Orbital endpoints` | tested | orbital_health | cross_platform | `os_version`, `system_info` | `Operating System Attributes` / `os_info`; `Inventory System Information` / `system_info` | `Posture Assessment`; `Forensics`; `Live Acquisition Of Volatile Data` | Related context: `TA0002` Execution; `TA0004` Privilege Escalation; `TA0005` Defense Evasion; `TA0006` Credential Access; `TA0007` Discovery; `TA0008` Lateral Movement; `T1068`; `T1082`; `T1135`; `T1203`; `T1210`; `T1212` |
| `Get SHA256 hashes for running processes` | draft | suspicious_process | cross_platform | `processes`, `hash` | `SHA256 Hash Of Running Processes` / `process_hashes` | `Live Acquisition Of Volatile Data`; `Threat Hunting`; `Posture Assessment`; `Forensics` | Related context: `TA0001` Initial Access; `TA0002` Execution; `TA0003` Persistence; `TA0004` Privilege Escalation; `TA0005` Defense Evasion; `TA0011` Command and Control; `T1036`; `T1053.005`; `T1055`; `T1055.012`; `T1071`; `T1102`; `T1219`; `T1543.003`; `T1546.008`; `T1547.001`; `T1547.015`; `T1564.001`; `T1566.001`; `T1571` |
| `Find running sfc.exe processes on Windows` | draft | suspicious_process | windows | `processes`, `system_info` | Organization/custom process patterns plus stock table context | `process inventory`; `Threat Hunting`; `Posture Assessment`; `Live Acquisition Of Volatile Data` | Related context: `TA0002` Execution; `TA0004` Privilege Escalation; `TA0005` Defense Evasion; `TA0011` Command and Control; `T1036`; `T1055`; `T1055.012`; `T1071`; `T1102`; `T1219`; `T1571` |

Note: rows marked `Related context` use MITRE/category mappings from Orbital stock catalog entries that share the same osquery tables. They guide future query design but do not mean the method itself detects every listed TTP.

## Method Details

### Check endpoints for non-default hosts file entries

Record:

```text
02_Working_Files/query-method-memory/network/hosts_file_entries.yaml
```

Goal: find non-default hosts-file mappings on endpoints that respond to Orbital.

Tables:

- `etc_hosts`
- `system_info`

Primary catalog context:

- Name: `Hosts File Monitoring`
- ID: `etc_hosts_monitoring`
- Category: `Posture Assessment`
- OS: Windows, Linux, macOS

Related table-derived catalog categories:

- `Posture Assessment`
- `Forensics`
- `Live Acquisition Of Volatile Data`

MITRE TTP context from Orbital Catalog:

- Tactic: `TA0011` Command and Control
- Technique: `T1008` Fallback Channels
- Technique: `T1102` Web Service

Reusable lessons:

- Use stock catalog query `etc_hosts_monitoring` as the starting point for hosts-file checks.
- Include `system_info.hostname` when showing cross-endpoint hosts-file entries.
- Hosts-file entries can be legitimate or malicious; review mapped domains/IPs before judging intent.

### Inventory Orbital computer names

Record:

```text
02_Working_Files/query-method-memory/orbital_health/computer_name_inventory.yaml
```

Goal: list computer names for endpoints that respond to an Orbital live query.

Tables:

- `system_info`

Primary catalog context:

- Name: `Inventory System Information`
- ID: `system_info`
- Category: `Posture Assessment`
- OS: Windows, macOS, Linux

Related table-derived catalog categories:

- `Posture Assessment`
- `Forensics`
- `Live Acquisition Of Volatile Data`

MITRE TTP context from related catalog entries:

- Tactic: `TA0005` Defense Evasion

Caution: this inventory method is not a threat detection. The TTP context comes from related stock catalog entries that also use `system_info`.

Reusable lessons:

- When user wording says `systeminfo`, translate to osquery table `system_info`.
- For Orbital-only computer-name inventory, `computer_name` from `system_info` is usable despite the upstream osquery 5.23 schema mismatch. Verify portability if using outside Orbital.

### Inventory operating systems on Orbital endpoints

Record:

```text
02_Working_Files/query-method-memory/orbital_health/operating_system_inventory.yaml
```

Goal: list operating system details for endpoints that respond to Orbital live queries.

Tables:

- `os_version`
- `system_info`

Primary catalog context:

- Name: `Operating System Attributes`
- ID: `os_info`
- Categories: `Posture Assessment`, `Forensics`
- OS: Windows, macOS, Linux
- Name: `Inventory System Information`
- ID: `system_info`
- Category: `Posture Assessment`

Related table-derived catalog categories:

- `Posture Assessment`
- `Forensics`
- `Live Acquisition Of Volatile Data`

MITRE TTP context from related catalog entries:

- Tactic: `TA0002` Execution
- Tactic: `TA0004` Privilege Escalation
- Tactic: `TA0005` Defense Evasion
- Tactic: `TA0006` Credential Access
- Tactic: `TA0007` Discovery
- Tactic: `TA0008` Lateral Movement
- Technique: `T1068` Exploitation for Privilege Escalation
- Technique: `T1082` System Information Discovery
- Technique: `T1135` Network Share Discovery
- Technique: `T1203` Exploitation for Client Execution
- Technique: `T1210` Exploitation of Remote Services
- Technique: `T1212` Exploitation for Credential Access

Caution: this OS inventory method is not a vulnerability or threat detection by itself. The TTP context comes from related stock catalog entries that also use `os_version` or `system_info`.

Reusable lessons:

- Store catalog table context after execution, including categories and MITRE mappings shown by the Orbital Catalog.
- Use `os_version` for OS details and `system_info.hostname` for computer-name ordering.

### Get SHA256 hashes for running processes

Record:

```text
02_Working_Files/query-method-memory/suspicious_processes/running_process_sha256_from_catalog.yaml
```

Goal: identify currently running processes and calculate SHA256 hashes for their executable paths.

Tables:

- `processes`
- `hash`

Primary catalog context:

- Name: `SHA256 Hash Of Running Processes`
- ID: `process_hashes`
- Category: `Live Acquisition Of Volatile Data`
- OS: Windows, macOS, Linux

Related table-derived catalog categories:

- `Threat Hunting`
- `Posture Assessment`
- `Live Acquisition Of Volatile Data`
- `Forensics`

MITRE TTP context from related catalog entries:

- Tactic: `TA0001` Initial Access
- Tactic: `TA0002` Execution
- Tactic: `TA0003` Persistence
- Tactic: `TA0004` Privilege Escalation
- Tactic: `TA0005` Defense Evasion
- Tactic: `TA0011` Command and Control
- Technique: `T1036` Masquerading
- Technique: `T1053.005` Scheduled Task
- Technique: `T1055` Process Injection
- Technique: `T1055.012` Process Hollowing
- Technique: `T1071` Application Layer Protocol
- Technique: `T1102` Web Service
- Technique: `T1219` Remote Access Software
- Technique: `T1543.003` Windows Service
- Technique: `T1546.008` Accessibility Features
- Technique: `T1547.001` Registry Run Keys / Startup Folder
- Technique: `T1547.015` Login Items
- Technique: `T1564.001` Hidden Files and Directories
- Technique: `T1566.001` Spearphishing Attachment
- Technique: `T1571` Non-Standard Port

Caution: related TTP context helps future process/hash query design. Process hashing alone does not detect every listed TTP.

Reusable lessons:

- Use this as a method for current-state process hash triage, not as historical process evidence.
- Querying the osquery `processes` table has low endpoint performance impact.
- Keep separate performance caution for joins to `hash` because file hashing adds work beyond process enumeration.

### Find running sfc.exe processes on Windows

Record:

```text
02_Working_Files/query-method-memory/suspicious_processes/windows_sfc_running_process.yaml
```

Goal: identify currently running `sfc.exe` processes on Windows endpoints and show process execution context.

Tables:

- `processes`
- `system_info`

Primary catalog context:

- Organization/custom process query patterns
- Closest stock table context: `SHA256 Hash Of Running Processes` / `process_hashes`
- Supporting identity context: `Inventory System Information` / `system_info`

Related table-derived catalog categories:

- `Threat Hunting`
- `Posture Assessment`
- `Live Acquisition Of Volatile Data`

MITRE TTP context from related catalog entries:

- Tactic: `TA0002` Execution
- Tactic: `TA0004` Privilege Escalation
- Tactic: `TA0005` Defense Evasion
- Tactic: `TA0011` Command and Control
- Technique: `T1036` Masquerading
- Technique: `T1055` Process Injection
- Technique: `T1055.012` Process Hollowing
- Technique: `T1071` Application Layer Protocol
- Technique: `T1102` Web Service
- Technique: `T1219` Remote Access Software
- Technique: `T1571` Non-Standard Port

Caution: related TTP context helps future process-query design. The `sfc.exe` lookup itself does not detect every listed TTP.

Reusable lessons:

- For cross-endpoint display, include `computer_name` even when the requested table focuses on process fields.
- Querying the osquery `processes` table has low endpoint performance impact.

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
