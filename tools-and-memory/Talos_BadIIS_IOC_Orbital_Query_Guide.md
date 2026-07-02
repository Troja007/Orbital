# Talos BadIIS IOC Investigation With Cisco Orbital

Source example: [Cisco Talos commodity_badiis.json](https://github.com/Cisco-Talos/IOCs/blob/main/2026/05/commodity_badiis.json)

The Talos STIX bundle for **BadIIS** contains:

- 151 SHA256 file hashes
- 7 URL indicators
- ATT&CK context including IIS Components `T1505.004`, Scheduled Task `T1053.005`, and network communication context

This guide shows how the IOC information can be converted into Cisco Orbital queries. It does not execute any query.

## Investigation Approach

Do not treat the Talos JSON as one generic IOC list. Split it by IOC type and evidence source:

- SHA256 hashes: running processes, loaded modules, and file paths where available.
- URLs: extract domains, IP addresses, ports, and URL path fragments.
- IIS context: check IIS services, IIS paths, loaded modules, and registry references.
- Persistence context: scheduled tasks and registry references.
- Network context: active sockets and DNS cache.

For IOC-matching queries, `0 rows` usually means no match for that exact IOC type and queried telemetry source, assuming the endpoint answered successfully. It does not prove the endpoint was never affected.

## 1. Running Malicious File Hashes

Use this first because it is high-signal and scoped to currently running executables.

```sql
WITH iocs(sha256) AS (
  VALUES
    ('<sha256_1>'),
    ('<sha256_2>'),
    ('<sha256_3>')
)
SELECT
  p.pid,
  p.name,
  p.path,
  p.cmdline,
  h.sha256
FROM processes p
JOIN hash h ON p.path = h.path
JOIN iocs i ON lower(h.sha256) = lower(i.sha256);
```

Interpretation: `0 rows` means no currently running process executable matched the Talos hashes.

## 2. Loaded DLL Or Module Hash Matches

BadIIS is IIS-component oriented, so loaded DLLs and modules matter.

```sql
WITH iocs(sha256) AS (
  VALUES
    ('<sha256_1>'),
    ('<sha256_2>')
)
SELECT DISTINCT
  p.pid,
  p.name AS process_name,
  p.path AS process_path,
  pm.path AS loaded_module,
  h.sha256
FROM processes p
JOIN process_memory_map pm ON p.pid = pm.pid
JOIN hash h ON pm.path = h.path
JOIN iocs i ON lower(h.sha256) = lower(i.sha256)
WHERE pm.path != '';
```

Use this to find malicious IIS modules or suspicious components loaded into active processes.

## 3. Active Network Connections To Talos IPs

Extract IPs from the URL indicators and query active sockets.

```sql
WITH ioc_ips(ip) AS (
  VALUES
    ('143.92.36.109'),
    ('38.181.52.147'),
    ('154.23.186.99'),
    ('154.36.149.4'),
    ('45.194.17.133')
)
SELECT
  p.pid,
  p.name,
  p.path,
  p.cmdline,
  s.remote_address,
  s.remote_port,
  s.local_address,
  s.local_port
FROM process_open_sockets s
LEFT JOIN processes p ON s.pid = p.pid
JOIN ioc_ips i ON s.remote_address = i.ip;
```

Interpretation: `0 rows` means no current active socket to those IPs at query time.

## 4. DNS Cache For Talos Domains

Use this to find local DNS cache evidence for domains extracted from the URL indicators.

```sql
WITH ioc_domains(domain) AS (
  VALUES
    ('lee.6686ty.vip'),
    ('iis.01nmwe.xyz')
)
SELECT
  d.name,
  d.type,
  d.flags
FROM dns_cache d
JOIN ioc_domains i
  ON lower(d.name) = lower(i.domain)
  OR lower(d.name) LIKE '%' || lower(i.domain) || '%';
```

DNS cache is not the same as a live connection. Treat this as local resolver history or cached evidence.

## 5. Scheduled Tasks Referencing IOCs

The Talos bundle includes Scheduled Task ATT&CK context. Query scheduled task actions for domains, IPs, and URL path fragments.

```sql
WITH iocs(value) AS (
  VALUES
    ('143.92.36.109'),
    ('38.181.52.147'),
    ('154.36.149.4'),
    ('lee.6686ty.vip'),
    ('iis.01nmwe.xyz'),
    ('authorize.txt'),
    ('listen.php')
)
SELECT
  name,
  action,
  path,
  enabled,
  state,
  hidden,
  datetime(last_run_time, 'unixepoch', 'UTC') AS last_run_utc,
  datetime(next_run_time, 'unixepoch', 'UTC') AS next_run_utc
FROM scheduled_tasks
WHERE EXISTS (
  SELECT 1 FROM iocs
  WHERE lower(action) LIKE '%' || lower(iocs.value) || '%'
     OR lower(path) LIKE '%' || lower(iocs.value) || '%'
);
```

This can show scheduled execution or persistence references related to the IOC set.

## 6. Registry Persistence And IIS-Related References

Search registry keys, value names, and data for URL, domain, path, and IP fragments.

```sql
WITH iocs(value) AS (
  VALUES
    ('lee.6686ty.vip'),
    ('iis.01nmwe.xyz'),
    ('authorize.txt'),
    ('listen.php'),
    ('143.92.36.109'),
    ('154.36.149.4')
)
SELECT
  key,
  path,
  name,
  type,
  data,
  datetime(mtime, 'unixepoch', 'UTC') AS modified_utc
FROM registry
WHERE EXISTS (
  SELECT 1 FROM iocs
  WHERE lower(key) LIKE '%' || lower(iocs.value) || '%'
     OR lower(path) LIKE '%' || lower(iocs.value) || '%'
     OR lower(name) LIKE '%' || lower(iocs.value) || '%'
     OR lower(data) LIKE '%' || lower(iocs.value) || '%'
);
```

Registry matches need review. A match is evidence of reference or configuration, not automatically proof of malicious execution.

## 7. IIS Service And Process Context

Because the report is BadIIS-related, check whether IIS services and paths exist or are active.

```sql
SELECT
  name,
  display_name,
  status,
  start_type,
  path,
  module_path,
  description
FROM services
WHERE lower(name) IN ('w3svc', 'was', 'iisadmin')
   OR lower(display_name) LIKE '%internet information services%'
   OR lower(path) LIKE '%inetsrv%';
```

This is context. It tells whether the endpoint has IIS-related services, not whether it is compromised.

## Recommended Orbital Custom Query Shape

Orbital supports multiple SQL blocks in one custom query definition. A practical custom query could be structured like this:

```json
{
  "name": "Talos BadIIS IOC Sweep",
  "nodes": ["os:windows"],
  "interval": 86400,
  "expiry": "<expiry>",
  "osQuery": [
    {
      "label": "talos_badiis_running_process_hashes",
      "sql": "<SQL 1>"
    },
    {
      "label": "talos_badiis_loaded_module_hashes",
      "sql": "<SQL 2>"
    },
    {
      "label": "talos_badiis_active_network_connections",
      "sql": "<SQL 3>"
    },
    {
      "label": "talos_badiis_dns_cache",
      "sql": "<SQL 4>"
    },
    {
      "label": "talos_badiis_scheduled_tasks",
      "sql": "<SQL 5>"
    },
    {
      "label": "talos_badiis_registry_references",
      "sql": "<SQL 6>"
    },
    {
      "label": "talos_badiis_iis_services",
      "sql": "<SQL 7>"
    }
  ]
}
```

## Operational Notes

- Start with narrow target selectors for testing.
- Store the Orbital Job ID and query label for each execution.
- For broad endpoint groups, avoid combining very expensive hash and module scans without testing endpoint impact.
- Keep `0 rows` interpretation scoped to the exact query block.
- For URL indicators, split into domain, IP, port, and path fragments before querying.
- For IIS-related threats, combine direct IOC matching with IIS service/module context and persistence checks.

## Result Interpretation Summary

| Query block | `0 rows` means | Rows mean |
|---|---|---|
| Running process hashes | No running executable matched the hash list | A live process executable hash matched |
| Loaded module hashes | No loaded module matched the hash list | A process loaded a module matching a Talos hash |
| Active network connections | No active socket to listed IPs at query time | A process currently connects to or has a socket with a listed IP |
| DNS cache | No cached DNS evidence for listed domains | Local DNS cache contains a listed domain |
| Scheduled tasks | No task action/path references listed IOCs | A scheduled task references IOC material |
| Registry references | No registry key/value/data references listed IOCs | Registry contains IOC-related references |
| IIS services | No IIS service/path evidence from this query | IIS-related service context exists |

