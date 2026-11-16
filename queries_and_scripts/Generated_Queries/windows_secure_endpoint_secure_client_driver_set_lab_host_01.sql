SELECT
  'driver' AS evidence_type,
  d.service AS driver_or_service,
  d.device_name AS display_name,
  d.image AS path_or_image,
  d.description,
  d.provider,
  d.manufacturer,
  d.version,
  d.signed,
  d.class,
  '' AS status_or_start,
  '' AS file_details
FROM drivers d
WHERE lower(d.service) IN (
    'bddci',
    'trufos',
    'immunetselfprotectdriver',
    'immunetprotectdriver',
    'immunetnetworkmonitordriver',
    'ciscoampheurdriver',
    'ciscoampelamdriver',
    'ciscoampcefwdriver',
    'ancrcl'
  )
   OR lower(d.device_name) IN (
    'bddci',
    'trufos',
    'immunetselfprotectdriver',
    'immunetprotectdriver',
    'immunetnetworkmonitordriver',
    'ciscoampheurdriver',
    'ciscoampelamdriver',
    'ciscoampcefwdriver',
    'ancrcl'
  )
   OR lower(d.image) IN (
    'c:\windows\system32\drivers\bddci.sys',
    'c:\windows\system32\drivers\trufos.sys',
    'c:\windows\system32\drivers\immunetselfprotect.sys',
    'c:\windows\system32\drivers\immunetprotect.sys',
    'c:\windows\system32\drivers\immunetnetworkmonitor.sys',
    'c:\windows\system32\drivers\ciscoampheurdriver.sys',
    'c:\windows\system32\drivers\ciscoampelamdriver.sys',
    'c:\windows\system32\drivers\ciscoampcefwdriver.sys',
    'c:\program files\cisco\amp\endpointisolation\ancrcl64.sys'
  )

UNION ALL

SELECT
  'service' AS evidence_type,
  s.name AS driver_or_service,
  s.display_name,
  COALESCE(s.path, s.module_path, '') AS path_or_image,
  s.description,
  '' AS provider,
  '' AS manufacturer,
  '' AS version,
  '' AS signed,
  s.service_type AS class,
  'status=' || COALESCE(s.status, '') || ' start_type=' || COALESCE(s.start_type, '') AS status_or_start,
  '' AS file_details
FROM services s
WHERE lower(s.name) IN (
    'bddci',
    'trufos',
    'immunetselfprotectdriver',
    'immunetprotectdriver',
    'immunetnetworkmonitordriver',
    'ciscoampheurdriver',
    'ciscoampelamdriver',
    'ciscoampcefwdriver',
    'ancrcl'
  )
   OR lower(s.display_name) IN (
    'bddci',
    'trufos',
    'immunetselfprotectdriver',
    'immunetprotectdriver',
    'immunetnetworkmonitordriver',
    'ciscoampheurdriver',
    'ciscoampelamdriver',
    'ciscoampcefwdriver',
    'ancrcl'
  )
   OR lower(s.path) LIKE '%bddci.sys%'
   OR lower(s.path) LIKE '%trufos.sys%'
   OR lower(s.path) LIKE '%immunetselfprotect.sys%'
   OR lower(s.path) LIKE '%immunetprotect.sys%'
   OR lower(s.path) LIKE '%immunetnetworkmonitor.sys%'
   OR lower(s.path) LIKE '%ciscoampheurdriver.sys%'
   OR lower(s.path) LIKE '%ciscoampelamdriver.sys%'
   OR lower(s.path) LIKE '%ciscoampcefwdriver.sys%'
   OR lower(s.path) LIKE '%ancrcl64.sys%'
   OR lower(s.module_path) LIKE '%bddci.sys%'
   OR lower(s.module_path) LIKE '%trufos.sys%'
   OR lower(s.module_path) LIKE '%immunetselfprotect.sys%'
   OR lower(s.module_path) LIKE '%immunetprotect.sys%'
   OR lower(s.module_path) LIKE '%immunetnetworkmonitor.sys%'
   OR lower(s.module_path) LIKE '%ciscoampheurdriver.sys%'
   OR lower(s.module_path) LIKE '%ciscoampelamdriver.sys%'
   OR lower(s.module_path) LIKE '%ciscoampcefwdriver.sys%'
   OR lower(s.module_path) LIKE '%ancrcl64.sys%'

UNION ALL

SELECT
  'file' AS evidence_type,
  f.filename AS driver_or_service,
  '' AS display_name,
  f.path AS path_or_image,
  COALESCE(f.original_filename, '') AS description,
  '' AS provider,
  '' AS manufacturer,
  COALESCE(f.file_version, f.product_version, '') AS version,
  '' AS signed,
  f.type AS class,
  '' AS status_or_start,
  'size=' || CAST(f.size AS TEXT) || ' mtime=' || datetime(f.mtime, 'unixepoch', 'UTC') AS file_details
FROM file f
WHERE f.path IN (
  'C:\Windows\System32\Drivers\bddci.sys',
  'C:\Windows\System32\Drivers\trufos.sys',
  'C:\Windows\System32\Drivers\immunetselfprotect.sys',
  'C:\Windows\System32\Drivers\immunetprotect.sys',
  'C:\Windows\System32\Drivers\ImmunetNetworkMonitor.sys',
  'C:\Windows\System32\Drivers\CiscoAMPHeurDriver.sys',
  'C:\Windows\System32\Drivers\CiscoAMPELAMDriver.sys',
  'C:\Windows\System32\Drivers\CiscoAMPCEFWDriver.sys',
  'C:\Program Files\Cisco\AMP\endpointisolation\ancrcl64.sys'
)
ORDER BY driver_or_service, evidence_type, path_or_image;
