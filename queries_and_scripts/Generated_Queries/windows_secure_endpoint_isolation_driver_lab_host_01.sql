SELECT
  'services' AS evidence_source,
  s.name AS driver_service,
  s.display_name,
  s.path AS driver_path,
  s.service_type,
  s.status,
  s.start_type,
  '' AS version,
  '' AS provider,
  '' AS manufacturer,
  '' AS signed
FROM services s
WHERE lower(s.name) = 'ancrcl'
   OR lower(s.path) LIKE '%endpointisolation%ancrcl64.sys%'
   OR lower(s.description) LIKE '%endpoint isolation%'
UNION ALL
SELECT
  'drivers' AS evidence_source,
  d.service AS driver_service,
  d.device_name AS display_name,
  d.image AS driver_path,
  d.class AS service_type,
  '' AS status,
  '' AS start_type,
  d.version,
  d.provider,
  d.manufacturer,
  CAST(d.signed AS TEXT) AS signed
FROM drivers d
WHERE lower(d.service) = 'ancrcl'
   OR lower(d.image) LIKE '%endpointisolation%ancrcl64.sys%'
   OR lower(d.description) LIKE '%endpoint isolation%'
UNION ALL
SELECT
  'file' AS evidence_source,
  'ancrcl' AS driver_service,
  f.filename AS display_name,
  f.path AS driver_path,
  f.type AS service_type,
  '' AS status,
  '' AS start_type,
  f.file_version AS version,
  '' AS provider,
  '' AS manufacturer,
  '' AS signed
FROM file f
WHERE f.path = 'C:\Program Files\Cisco\AMP\endpointisolation\ancrcl64.sys'
ORDER BY evidence_source;
