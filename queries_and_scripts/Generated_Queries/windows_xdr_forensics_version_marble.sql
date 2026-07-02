SELECT
  'installed_program' AS evidence_type,
  pr.name AS item_name,
  pr.version AS version,
  pr.publisher AS publisher,
  pr.install_location AS path_or_location,
  pr.install_source AS extra_detail
FROM programs pr
WHERE lower(pr.name) LIKE '%forensics%'
   OR lower(pr.name) LIKE '%xdr forensics%'
   OR lower(pr.name) LIKE '%forensics responder%'

UNION ALL

SELECT
  'service' AS evidence_type,
  s.display_name AS item_name,
  '' AS version,
  '' AS publisher,
  COALESCE(s.path, s.module_path, '') AS path_or_location,
  s.name || ' status=' || s.status || ' start_type=' || s.start_type AS extra_detail
FROM services s
WHERE s.name = 'Cisco.Forensics.Responder.Service'
   OR lower(s.display_name) LIKE '%forensics%'
   OR lower(s.path) LIKE '%\cisco\forensics\%'
   OR lower(s.module_path) LIKE '%\cisco\forensics\%'

UNION ALL

SELECT
  'running_process' AS evidence_type,
  p.name AS item_name,
  COALESCE(f.file_version, '') AS version,
  '' AS publisher,
  p.path AS path_or_location,
  'pid=' || CAST(p.pid AS TEXT) || ' product_version=' || COALESCE(f.product_version, '') AS extra_detail
FROM processes p
LEFT JOIN file f
  ON p.path = f.path
WHERE lower(p.name) = 'air.exe'
   OR lower(p.path) LIKE '%\cisco\forensics\%'

UNION ALL

SELECT
  'expected_file' AS evidence_type,
  f.filename AS item_name,
  COALESCE(f.file_version, '') AS version,
  '' AS publisher,
  f.path AS path_or_location,
  'product_version=' || COALESCE(f.product_version, '') AS extra_detail
FROM file f
WHERE f.path = 'C:\Program Files\Cisco\Forensics\AIR\AIR.exe'
ORDER BY evidence_type, item_name, path_or_location;
