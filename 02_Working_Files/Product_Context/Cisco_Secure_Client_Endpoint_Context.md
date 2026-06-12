# Cisco Secure Client / Secure Endpoint Context

Created: 2026-06-11
Status: working collection
Scope: Windows endpoint context for Cisco Secure Endpoint, Cisco Secure Client, and adjacent Cisco endpoint components visible through Orbital/osquery.

This file collects product context, expected endpoint artifacts, Orbital query patterns, and script-design notes for later monitor/check/repair automation. It is intentionally method-focused: do not store live endpoint result rows, hostnames, IP addresses, tenant identifiers, or raw API responses here.

## Source Basis

- Verified Orbital UI SQL pattern for `sfc.exe` running/not-running status.
- Live-tested Orbital query method for running processes where executable path contains `Cisco`.
- Redacted organization catalog query pattern for Secure Endpoint memory consumption.
- Redacted organization catalog query pattern for Secure Endpoint disk usage.
- Redacted organization catalog query pattern for Windows firewall/event telemetry.
- Organization catalog process-memory examples for Cisco DLLs loaded into running processes.
- Stock catalog script: `List the Definition's Version of Secure Endpoint Engines`, ID `se_engine_definitions`.
- Organization catalog scripts for `sfc.exe` start, stop, force update, and Secure Client NVM/Umbrella service start/stop.
- osquery 5.23.0 schema in `01_Source_Files/API_References/osquery_schema_5_23_0.json`.

## Product Families

### Cisco Secure Endpoint

Legacy install paths and process names still commonly include `AMP`.

Primary observed Windows process families:

| Process | Likely role | Typical path pattern | Notes |
| --- | --- | --- | --- |
| `sfc.exe` | Secure Endpoint connector process / control binary | `C:\Program Files\Cisco\AMP\<version>\sfc.exe` | Used by catalog scripts for connector start, stop, and force update. |
| `cscm.exe` | Secure Endpoint / AMP component | `C:\Program Files\Cisco\AMP\<version>\cscm.exe` | Seen as a common companion process to `sfc.exe`. |

Secure Endpoint Exploit Prevention context:

- Exploit Prevention can load a small Cisco DLL into running processes.
- Seeing a process with the Exploit Prevention DLL loaded indicates that Secure Endpoint is running and that the Exploit Prevention engine is active for that process.
- This evidence does not show whether the engine is in audit mode or protect mode.
- The loaded DLL evidence helps identify which processes are protected by Exploit Prevention.
- It can also help application troubleshooting: if an application has issues, check whether Exploit Prevention changed or instrumented the process memory by loading its DLL.
- `Protector64.dll` is the 64-bit variant. A 32-bit variant also exists and should be queried separately, for example with `Protector32.dll` or a broader `Protector%.dll` pattern after validation.

Important command examples from redacted organization script patterns:

```powershell
Start-Process -NoNewWindow -FilePath "C:\Program Files\Cisco\AMP\<version>\sfc.exe" -ArgumentList "-forceupdate"
Start-Process -NoNewWindow -FilePath "C:\Program Files\Cisco\AMP\<version>\sfc.exe" -ArgumentList "-k"
Start-Process -NoNewWindow -FilePath "C:\Program Files\Cisco\AMP\<version>\sfc.exe" -ArgumentList "-s"
```

Do not hard-code the version directory in future repair scripts. Discover `sfc.exe` first through `processes`, `file`, `programs`, registry, or directory search, then execute the discovered path.

### Cisco Secure Client

Primary observed Windows process families:

| Process | Likely role | Typical path pattern | Notes |
| --- | --- | --- | --- |
| `csc_ui.exe` | Secure Client user interface | `C:\Program Files (x86)\Cisco\Cisco Secure Client\UI\csc_ui.exe` | Often user-facing and may run minimized. |
| `vpnagent.exe` | Secure Client VPN service | `C:\Program Files (x86)\Cisco\Cisco Secure Client\vpnagent.exe` | Service-backed component. |
| `acnvmagent.exe` | Network Visibility Module agent | `C:\Program Files (x86)\Cisco\Cisco Secure Client\NVM\acnvmagent.exe` | Related service name appears as `csc_nvmagent`. |
| `csc_cmid.exe` | Cloud Management identity component | `C:\Program Files\Cisco\Cisco Secure Client\CM\<version>\CMID\<version>\csc_cmid.exe` | Uses Cloud Management configuration path. |
| `csc_cms.exe` | Cloud Management service component | `C:\Program Files\Cisco\Cisco Secure Client\CM\<version>\Service\<version>\csc_cms.exe` | Service component. |
| `csc_pm.exe` | Cloud Management profile/config component | `C:\Program Files\Cisco\Cisco Secure Client\CM\<version>\CMPM\<version>\csc_pm.exe` | Uses Cloud Management bootstrap/config files. |
| `csc_evm.exe` | Endpoint Visibility Module component | `C:\Program Files\Cisco\Cisco Secure Client\EVM\bin\csc_evm.exe` | Optional module. |

Known service names from redacted organization script patterns:

| Service | Product/module | Existing action scripts |
| --- | --- | --- |
| `csc_nvmagent` | Secure Client NVM | start/stop service action pattern |
| `csc_umbrellaagent` | Secure Client Umbrella | start/stop service action pattern |

Service discovery must be validated with the `services` table before creating repair scripts; the process list alone does not prove the service name or start mode.

### Cisco Orbital

Orbital is not Secure Endpoint/Secure Client, but it is part of the same endpoint context because this project uses Orbital to collect evidence.

| Process | Likely role | Typical path pattern |
| --- | --- | --- |
| `orbital.exe` | Orbital endpoint service | `C:\Program Files\Cisco\Orbital\orbital.exe` |
| `osqueryd.exe` | Orbital osquery runtime | `C:\Program Files\Cisco\Orbital\osqueryd.exe` |

### Cisco Forensics AIR

| Process | Likely role | Typical path pattern |
| --- | --- | --- |
| `AIR.exe` | Cisco Forensics AIR | `C:\Program Files\Cisco\Forensics\AIR\AIR.exe` |

Treat AIR as related Cisco context, not as Secure Endpoint/Secure Client core health.

## Important Paths

Use path discovery rather than fixed versions.

| Purpose | Path pattern |
| --- | --- |
| Secure Endpoint / AMP binaries | `C:\Program Files\Cisco\AMP\%` |
| Secure Endpoint local definition/config file | `C:\Program Files\Cisco\AMP\local.xml` |
| Secure Client root | `C:\Program Files\Cisco\Cisco Secure Client\%` |
| Secure Client 32-bit UI/VPN/NVM paths | `C:\Program Files (x86)\Cisco\Cisco Secure Client\%` |
| Cisco program data | `C:\ProgramData\Cisco\%` |
| Orbital binaries | `C:\Program Files\Cisco\Orbital\%` |
| Forensics AIR | `C:\Program Files\Cisco\Forensics\AIR\%` |

## Query Building Blocks

Use these tables for monitor/check logic:

| Evidence type | osquery table | Relevant columns |
| --- | --- | --- |
| Endpoint identity | `system_info` | `hostname`, `uuid`, `computer_name`, `local_hostname` |
| Running process state | `processes` | `pid`, `name`, `path`, `cmdline`, `state`, `start_time`, `parent`, `threads`, `resident_size`, `total_size`, `elapsed_time` |
| Loaded process memory mappings | `process_memory_map` | `pid`, `path`, `permissions`, `start`, `end`, `pseudo` |
| Windows services | `services` | `name`, `display_name`, `status`, `pid`, `start_type`, `path`, `module_path`, `description`, `user_account` |
| Installed applications | `programs` | `name`, `version`, `install_location`, `publisher`, `uninstall_string`, `install_date` |
| Files and directories | `file` | `path`, `size`, `type`, `btime`, `mtime`, `atime`, `file_version`, `product_version`, `original_filename` |
| File hashes | `hash` | `path`, `md5`, `sha1`, `sha256` |
| Windows signatures | `authenticode` | `path`, `issuer_name`, `subject_name`, `result`, `original_program_name` |
| Windows registry | `registry` | `key`, `path`, `name`, `data`, `mtime` |
| Drivers | `drivers` | `device_id`, `device_name`, `image`, `service`, `provider`, `manufacturer`, `signed`, `version` |

## Orbital Targeting

For Windows-only collection:

```json
{
  "nodes": ["os:windows"]
}
```

For API bodies with multiple related checks, use `osQuery` as an array:

```json
{
  "name": "Cisco endpoint context",
  "nodes": ["os:windows"],
  "osQuery": [
    {
      "label": "cisco_running_processes",
      "sql": "SELECT ..."
    },
    {
      "label": "cisco_services",
      "sql": "SELECT ..."
    }
  ]
}
```

For reusable catalog entries, use `config.osquery` as an array.

## Query Patterns

### Cisco Running Processes

Purpose: show currently running processes whose executable path includes Cisco. This is the first broad context query.

```sql
SELECT
  si.hostname AS host,
  si.uuid AS uuid,
  p.pid,
  p.name AS process_name,
  p.path AS process_path,
  p.cmdline AS command_line,
  p.state,
  datetime(p.start_time, 'unixepoch', 'UTC') AS started_utc
FROM processes p
CROSS JOIN system_info si
WHERE lower(p.path) LIKE '%cisco%'
ORDER BY si.hostname, p.name, p.pid;
```

### Cisco Running Process Summary

Purpose: quick endpoint/process overview without full command lines.

```sql
SELECT
  si.hostname AS host,
  p.name AS process_name,
  COUNT(*) AS process_count
FROM processes p
CROSS JOIN system_info si
WHERE lower(p.path) LIKE '%cisco%'
GROUP BY si.hostname, p.name
ORDER BY si.hostname, p.name;
```

### `sfc.exe` Running Status For All Responding Endpoints

Purpose: one row per responding endpoint, including endpoints where `sfc.exe` is absent.

```sql
SELECT
  si.hostname AS host,
  si.uuid AS uuid,
  CASE
    WHEN COUNT(p.pid) > 0 THEN 'sfc.exe_running'
    ELSE 'sfc.exe_not_running'
  END AS status,
  COUNT(p.pid) AS sfc_process_count
FROM system_info si
LEFT JOIN processes p
  ON lower(p.name) = 'sfc.exe'
  OR lower(p.path) LIKE '%\sfc.exe'
GROUP BY
  si.hostname,
  si.uuid
ORDER BY
  status,
  si.hostname;
```

### Secure Endpoint / Secure Client Memory Consumption

Purpose: identify high-memory Cisco processes. Based on a redacted organization catalog query pattern for Secure Endpoint memory consumption.

```sql
SELECT
  si.hostname AS host,
  p.pid,
  p.name,
  ROUND((p.resident_size / 1024 / 1024), 0) AS working_set_mb,
  ROUND((p.total_size / 1024 / 1024), 0) AS commit_mb,
  p.threads AS thread_count,
  ROUND((p.disk_bytes_read / 1024 / 1024 / 1024), 0) AS disk_read_gb,
  ROUND((p.disk_bytes_written / 1024 / 1024), 0) AS disk_write_mb,
  ROUND((p.elapsed_time / 3600), 0) AS uptime_hours,
  p.path
FROM processes p
CROSS JOIN system_info si
WHERE lower(p.path) LIKE '%cisco%'
ORDER BY p.total_size DESC
LIMIT 100;
```

### Cisco Services

Purpose: map service names, display names, status, start type, and executable paths. This should be run before any service repair script is created.

```sql
SELECT
  si.hostname AS host,
  s.name AS service_name,
  s.display_name,
  s.status,
  s.start_type,
  s.pid,
  s.path,
  s.module_path,
  s.description,
  s.user_account
FROM services s
CROSS JOIN system_info si
WHERE lower(s.name) LIKE '%cisco%'
   OR lower(s.display_name) LIKE '%cisco%'
   OR lower(s.path) LIKE '%cisco%'
   OR lower(s.module_path) LIKE '%cisco%'
   OR lower(s.name) IN ('csc_nvmagent', 'csc_umbrellaagent')
ORDER BY si.hostname, s.name;
```

### Installed Cisco Products

Purpose: identify installed Cisco products and versions through Windows installed-program inventory.

```sql
SELECT
  si.hostname AS host,
  pr.name,
  pr.version,
  pr.publisher,
  pr.install_location,
  pr.install_date,
  pr.uninstall_string
FROM programs pr
CROSS JOIN system_info si
WHERE lower(pr.name) LIKE '%cisco%'
   OR lower(pr.publisher) LIKE '%cisco%'
   OR lower(pr.install_location) LIKE '%cisco%'
ORDER BY si.hostname, pr.name;
```

### Cisco Files And Disk Footprint

Purpose: list Cisco files/directories and metadata. Based on a redacted organization catalog query pattern for Secure Endpoint disk usage.

Important: keep path constraints. Do not run the `file` table broadly without a bounded path.

```sql
SELECT
  si.hostname AS host,
  f.path,
  ROUND(f.size / 1024) AS size_kb,
  ROUND(f.size / 1024 / 1024) AS size_mb,
  f.type,
  f.file_version,
  f.product_version,
  strftime('%Y-%m-%d %H:%M:%S', f.btime, 'unixepoch') AS file_created,
  strftime('%Y-%m-%d %H:%M:%S', f.mtime, 'unixepoch') AS last_modified,
  strftime('%Y-%m-%d %H:%M:%S', f.atime, 'unixepoch') AS last_access
FROM file f
CROSS JOIN system_info si
WHERE f.path LIKE 'C:\Program Files\Cisco\%%'
   OR f.path LIKE 'C:\Program Files (x86)\Cisco\%%'
   OR f.path LIKE 'C:\ProgramData\Cisco\%%'
ORDER BY si.hostname, f.path;
```

### Cisco Process Hashes

Purpose: enrich running Cisco processes with SHA256 hashes. Use only after initial process scoping because hashing adds work.

```sql
SELECT
  si.hostname AS host,
  p.pid,
  p.name AS process_name,
  p.path AS process_path,
  h.sha256
FROM processes p
JOIN hash h
  ON h.path = p.path
CROSS JOIN system_info si
WHERE lower(p.path) LIKE '%cisco%'
ORDER BY si.hostname, p.name, p.pid;
```

### Cisco Process Authenticode Status

Purpose: validate Windows signing status for Cisco binaries. Use after process/path scoping.

```sql
SELECT
  si.hostname AS host,
  p.pid,
  p.name AS process_name,
  p.path AS process_path,
  a.issuer_name,
  a.subject_name,
  a.result
FROM processes p
LEFT JOIN authenticode a
  ON a.path = p.path
CROSS JOIN system_info si
WHERE lower(p.path) LIKE '%cisco%'
ORDER BY si.hostname, p.name, p.pid;
```

### Secure Endpoint Exploit Prevention Protected Processes

Purpose: identify running processes where Secure Endpoint Exploit Prevention has loaded its protection DLL. Positive rows show processes that have the Exploit Prevention DLL mapped into memory.

Interpretation:

- A positive row means the Exploit Prevention engine is running and has loaded a Cisco protection DLL into that process.
- The query shows which processes are protected or instrumented.
- The query does not show audit mode versus protect mode.
- The query can support application compatibility investigations by showing whether Exploit Prevention has changed the process memory layout.
- The 64-bit DLL is `Protector64.dll`. Query the 32-bit variant separately or use a broader `Protector%.dll` pattern when both architectures are needed.

64-bit working SQL:

```sql
SELECT DISTINCT
  si.hostname AS host,
  p.pid,
  p.name AS "Process Name",
  p.path AS "Process Path",
  pm.path AS "DLL-Loaded-path",
  h.sha256,
  a.issuer_name AS "DLL-Cert-Issuer_Name",
  a.subject_name AS "DLL-Cert-Subject_Name",
  a.result
FROM processes p
CROSS JOIN system_info si
LEFT JOIN process_memory_map pm ON p.pid = pm.pid
LEFT JOIN authenticode a ON pm.path = a.path
LEFT JOIN hash h ON pm.path = h.path
WHERE pm.path != ''
  AND lower(pm.path) NOT LIKE '%windows\system32%'
  AND lower(pm.path) LIKE '%.dll'
  AND lower(pm.path) LIKE '%cisco%'
  AND lower(pm.path) LIKE '%protector64.dll%'
ORDER BY si.hostname, p.pid;
```

Original working SQL shape without endpoint identity:

```sql
select DISTINCT p.pid, p.name AS "Process Name",
p.path AS "Process Path",
pm.path AS "DLL-Loaded-path",
sha256,
a.issuer_name AS "DLL-Cert-Issuer_Name",
a.subject_name as "DLL-Cert-Subject_Name",
a.result
from processes p
   
LEFT JOIN process_memory_map pm ON p.pid=pm.pid
LEFT JOIN authenticode a ON pm.path = a.path
LEFT JOIN hash h on pm.path = h.path
   
-- WHERE p.path LIKE "%:\windows%"
Where pm.path != ""
AND pm.path NOT LIKE "%windows\system32%"
AND pm.path LIKE "%.dll"
-- This row can be used to filter for untrusted signing certificates
-- AND a.result NOT LIKE "trusted"
AND pm.path like "%cisco%"
AND pm.path like "%Protector64.dll%"
-- checking Processes where exPrev injected code
-- AND pm.path like "%filezilla%"
ORDER BY p.pid;
```

32-bit follow-up pattern:

```sql
SELECT DISTINCT
  si.hostname AS host,
  p.pid,
  p.name AS "Process Name",
  p.path AS "Process Path",
  pm.path AS "DLL-Loaded-path",
  h.sha256,
  a.issuer_name AS "DLL-Cert-Issuer_Name",
  a.subject_name AS "DLL-Cert-Subject_Name",
  a.result
FROM processes p
CROSS JOIN system_info si
LEFT JOIN process_memory_map pm ON p.pid = pm.pid
LEFT JOIN authenticode a ON pm.path = a.path
LEFT JOIN hash h ON pm.path = h.path
WHERE pm.path != ''
  AND lower(pm.path) NOT LIKE '%windows\system32%'
  AND lower(pm.path) LIKE '%.dll'
  AND lower(pm.path) LIKE '%cisco%'
  AND lower(pm.path) LIKE '%protector32.dll%'
ORDER BY si.hostname, p.pid;
```

Combined architecture pattern:

```sql
SELECT DISTINCT
  si.hostname AS host,
  p.pid,
  p.name AS "Process Name",
  p.path AS "Process Path",
  pm.path AS "DLL-Loaded-path",
  CASE
    WHEN lower(pm.path) LIKE '%protector64.dll%' THEN '64-bit'
    WHEN lower(pm.path) LIKE '%protector32.dll%' THEN '32-bit'
    ELSE 'unknown'
  END AS protector_architecture,
  h.sha256,
  a.issuer_name AS "DLL-Cert-Issuer_Name",
  a.subject_name AS "DLL-Cert-Subject_Name",
  a.result
FROM processes p
CROSS JOIN system_info si
LEFT JOIN process_memory_map pm ON p.pid = pm.pid
LEFT JOIN authenticode a ON pm.path = a.path
LEFT JOIN hash h ON pm.path = h.path
WHERE pm.path != ''
  AND lower(pm.path) NOT LIKE '%windows\system32%'
  AND lower(pm.path) LIKE '%.dll'
  AND lower(pm.path) LIKE '%cisco%'
  AND (
    lower(pm.path) LIKE '%protector64.dll%'
    OR lower(pm.path) LIKE '%protector32.dll%'
  )
ORDER BY si.hostname, protector_architecture, p.pid;
```

Validation note:

- The 64-bit `Protector64.dll` SQL was tested through Orbital on 2026-06-11.
- `nodes = ["random:2", "allowOS:windows"]` returned no endpoint coverage in this API path.
- A rerun with `nodes = ["random:2"]` also returned no rows/coverage.
- A two-host Windows validation excluding `victim3` executed successfully but returned no `Protector64.dll` rows in that sample.
- The same catalog query was later verified directly in the Orbital UI against one exact Windows host and returned positive protected-process rows.
- The UI target selector used lowercase `host:<hostname>`. If API live query returns `answered_endpoint_count = 0` for an exact host while the UI returns rows, retry with the exact UI selector spelling/case before interpreting the result as no protected processes.
- Repeated execution of this `process_memory_map` query can destabilize or crash the Orbital query on the endpoint. Store the job ID for every run and use `/jobs/{id}` and `/jobs/{id}/results` for follow-up instead of rerunning the endpoint query.
- No live endpoint result rows are stored in this context file.

### Cisco Registry Inventory

Purpose: find Cisco-related installer/product registry entries. Existing organization examples search installer products for `DUO`, `AMP`, and `AnyConnect`.

```sql
SELECT
  si.hostname AS host,
  r.key,
  r.path,
  r.name,
  r.data,
  datetime(r.mtime, 'unixepoch', 'UTC') AS modified_utc
FROM registry r
CROSS JOIN system_info si
WHERE r.key LIKE 'HKEY_CLASSES_ROOT\Installer\Products\%%'
  AND (
    r.data LIKE '%%Cisco%%'
    OR r.data LIKE '%%AMP%%'
    OR r.data LIKE '%%AnyConnect%%'
    OR r.data LIKE '%%Secure Client%%'
  )
ORDER BY si.hostname, r.key, r.name;
```

### Secure Endpoint Event Log Context

Purpose: read Cisco Secure Endpoint firewall/event telemetry when available. Based on a redacted organization catalog query pattern for Windows firewall/event telemetry.

```sql
SELECT
  REPLACE(REPLACE(REPLACE(SUBSTR(datetime, 1, 19), 'T', ' '), '.', ''), 'Z', '') AS timestamp_evt,
  datetime(CAST(JSON_EXTRACT(data, '$.EventData.Timestamp') AS INTEGER) / 1000, 'unixepoch', 'localtime') AS timestamp_fw,
  JSON_EXTRACT(json(data), '$.EventData.Protocol') AS protocol,
  JSON_EXTRACT(json(data), '$.EventData.LocalIP') AS source_ip,
  JSON_EXTRACT(json(data), '$.EventData.LocalPort') AS source_port,
  JSON_EXTRACT(json(data), '$.EventData.RemoteIP') AS remote_ip,
  JSON_EXTRACT(json(data), '$.EventData.RemotePort') AS remote_port,
  CASE
    WHEN eventid = 1800 THEN 'Allow'
    WHEN eventid = 1801 THEN 'Block'
    ELSE 'Other'
  END AS action,
  JSON_EXTRACT(json(data), '$.EventData.Direction') AS direction,
  JSON_EXTRACT(json(data), '$.EventData.PID') AS pid,
  JSON_EXTRACT(json(data), '$.EventData.Application Path') AS application_path,
  JSON_EXTRACT(json(data), '$.EventData.url') AS url,
  JSON_EXTRACT(json(data), '$.EventData.RuleGUID') AS rule_guid,
  JSON_EXTRACT(json(data), '$.EventData.RuleName') AS rule_name,
  JSON_EXTRACT(json(data), '$.EventData.RuleSetGUID') AS configuration_guid,
  eventid
FROM windows_eventlog
WHERE channel = 'CiscoSecureEndpoint/Events'
  AND eventid IN (1801, 1800)
ORDER BY datetime DESC
LIMIT 500;
```

Validate `windows_eventlog` availability before using this in broad automation; evented or log-backed tables can vary by endpoint and configuration.

## API Body Pattern

Use one API request with multiple `osQuery` blocks when collecting a full Cisco context snapshot:

```json
{
  "name": "Cisco Secure Endpoint / Secure Client context",
  "nodes": ["os:windows"],
  "osQuery": [
    {
      "label": "cisco_running_processes",
      "sql": "SELECT si.hostname AS host, p.pid, p.name AS process_name, p.path AS process_path, p.cmdline AS command_line, p.state FROM processes p CROSS JOIN system_info si WHERE lower(p.path) LIKE '%cisco%' ORDER BY si.hostname, p.name, p.pid;"
    },
    {
      "label": "cisco_services",
      "sql": "SELECT si.hostname AS host, s.name AS service_name, s.display_name, s.status, s.start_type, s.pid, s.path FROM services s CROSS JOIN system_info si WHERE lower(s.name) LIKE '%cisco%' OR lower(s.display_name) LIKE '%cisco%' OR lower(s.path) LIKE '%cisco%' OR lower(s.name) IN ('csc_nvmagent', 'csc_umbrellaagent') ORDER BY si.hostname, s.name;"
    },
    {
      "label": "cisco_installed_products",
      "sql": "SELECT si.hostname AS host, pr.name, pr.version, pr.publisher, pr.install_location FROM programs pr CROSS JOIN system_info si WHERE lower(pr.name) LIKE '%cisco%' OR lower(pr.publisher) LIKE '%cisco%' OR lower(pr.install_location) LIKE '%cisco%' ORDER BY si.hostname, pr.name;"
    }
  ]
}
```

## Future Monitor/Check/Repair Script Design

Use this sequence for scripts:

1. Check endpoint OS and exit clearly if unsupported.
2. Discover installed product paths dynamically.
3. Discover services dynamically through service APIs or the `services` query output.
4. Check current process state before taking action.
5. For Secure Endpoint, discover the active `sfc.exe` path rather than hard-coding an AMP version directory.
6. For service repair, prefer service control by discovered service name only after confirming product/module match.
7. Make repair scripts idempotent: if the process/service is already healthy, report success and avoid restarting.
8. Print explicit stdout for every check and action.
9. Use custom exit codes `0` to `199`; reserve `200+` for Orbital.
10. Keep script output below Orbital stdout/stderr caps and avoid dumping large logs.

### Candidate Check Scripts

| Script goal | Inputs | Checks | Repair action |
| --- | --- | --- | --- |
| Secure Endpoint running check | none or expected product family | `sfc.exe` and `cscm.exe` process state; Secure Endpoint service state after service names are confirmed | Start service or invoke discovered `sfc.exe -s` only after validation |
| Secure Endpoint force update | discovered `sfc.exe` path | Verify `sfc.exe` exists and product path is Cisco AMP | Invoke `sfc.exe -forceupdate` |
| Secure Endpoint stop/start | explicit approval | Verify path and process/service relationship | Invoke discovered `sfc.exe -k` or `sfc.exe -s` |
| Secure Client NVM check | expected service name | `csc_nvmagent` service status and `acnvmagent.exe` process state | `net start csc_nvmagent` only when stopped |
| Secure Client Umbrella check | expected service name | `csc_umbrellaagent` service status | `net start csc_umbrellaagent` only when stopped |
| Cisco binary trust check | Cisco process paths | `authenticode.result`, issuer/subject, hash | No repair initially; report mismatch |
| Exploit Prevention protected-process check | `process_memory_map` plus Cisco Protector DLL path | `Protector64.dll`, `Protector32.dll`, signed Cisco DLL metadata, protected process path | No repair initially; use as evidence for engine activity and application compatibility triage |
| Disk footprint check | Cisco path list | file sizes under bounded Cisco paths | No repair initially; report large or stale paths |

### Repair Safety Rules

- Do not stop or restart endpoint security services without explicit operator approval.
- Do not use hard-coded version paths such as `C:\Program Files\Cisco\AMP\8.2.1.21650\sfc.exe` in generalized scripts.
- Do not assume Secure Client modules are installed on every endpoint.
- Do not delete files or registry keys in the first repair iteration.
- Treat Secure Endpoint and Secure Client as separate products even when paths and vendor names overlap.

## Open Validation Items

- Confirm canonical Windows service names for Secure Endpoint connector components in the target environment.
- Confirm whether `cscm.exe` is service-backed and which service owns it.
- Confirm whether `sfc.exe -s`, `-k`, and `-forceupdate` are supported across all deployed connector versions.
- Confirm Secure Client module service names beyond `csc_nvmagent` and `csc_umbrellaagent`.
- Validate `windows_eventlog` availability for `CiscoSecureEndpoint/Events` across target endpoints.
- Confirm exact 32-bit Exploit Prevention DLL filename and deployed paths before using the 32-bit or combined architecture query in production.
- Determine whether there is a separate queryable source for Exploit Prevention audit versus protect mode; loaded DLL evidence alone does not answer mode.
- Decide whether repair scripts should be product-specific or a single dispatcher script with modes.
