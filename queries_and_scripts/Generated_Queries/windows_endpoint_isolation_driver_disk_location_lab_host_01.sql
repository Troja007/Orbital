SELECT
  'service_path' AS evidence_type,
  s.name AS driver_service,
  s.path AS path_on_disk,
  s.service_type,
  s.status,
  s.start_type,
  '' AS file_type,
  '' AS file_size,
  '' AS file_version,
  '' AS mtime_utc
FROM services s
WHERE lower(s.name) = 'ancrcl'
   OR lower(s.path) = '\??\c:\program files\cisco\amp\endpointisolation\ancrcl64.sys'
UNION ALL
SELECT
  'file_exists_exact_path' AS evidence_type,
  'ancrcl' AS driver_service,
  f.path AS path_on_disk,
  '' AS service_type,
  '' AS status,
  '' AS start_type,
  f.type AS file_type,
  CAST(f.size AS TEXT) AS file_size,
  f.file_version,
  datetime(f.mtime, 'unixepoch', 'UTC') AS mtime_utc
FROM file f
WHERE f.path = 'C:\Program Files\Cisco\AMP\endpointisolation\ancrcl64.sys'
ORDER BY evidence_type;
