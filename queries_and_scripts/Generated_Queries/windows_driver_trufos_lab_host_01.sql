SELECT
  'driver' AS evidence_type,
  d.service AS item_name,
  d.image AS path_or_image,
  d.device_name AS display_name,
  d.provider AS provider,
  d.version AS version,
  d.signed AS signed,
  d.description AS details
FROM drivers d
WHERE lower(d.image) LIKE '%trufos.sys'
   OR lower(d.service) LIKE '%trufos%'
   OR lower(d.device_name) LIKE '%trufos%'
   OR lower(d.description) LIKE '%trufos%'

UNION ALL

SELECT
  'service' AS evidence_type,
  s.name AS item_name,
  COALESCE(s.path, s.module_path, '') AS path_or_image,
  s.display_name AS display_name,
  '' AS provider,
  '' AS version,
  '' AS signed,
  'status=' || COALESCE(s.status, '') || ' start_type=' || COALESCE(s.start_type, '') || ' type=' || COALESCE(s.service_type, '') AS details
FROM services s
WHERE lower(s.name) LIKE '%trufos%'
   OR lower(s.display_name) LIKE '%trufos%'
   OR lower(s.path) LIKE '%trufos.sys%'
   OR lower(s.module_path) LIKE '%trufos.sys%'

UNION ALL

SELECT
  'file' AS evidence_type,
  f.filename AS item_name,
  f.path AS path_or_image,
  '' AS display_name,
  '' AS provider,
  COALESCE(f.file_version, f.product_version, '') AS version,
  '' AS signed,
  'size=' || CAST(f.size AS TEXT) || ' mtime=' || datetime(f.mtime, 'unixepoch', 'UTC') AS details
FROM file f
WHERE f.path IN (
    'C:\Windows\System32\drivers\trufos.sys',
    'C:\Windows\SysWOW64\drivers\trufos.sys'
  )
ORDER BY evidence_type, item_name, path_or_image;
