WITH driver_candidates AS (
  SELECT
    'drivers' AS source_table,
    COALESCE(d.service, '') AS item_name,
    COALESCE(d.device_name, '') AS display_name,
    COALESCE(d.image, '') AS path_or_image,
    COALESCE(d.description, '') AS description,
    COALESCE(d.provider, '') AS provider,
    COALESCE(d.manufacturer, '') AS manufacturer,
    COALESCE(d.version, '') AS version,
    COALESCE(d.class, '') AS type_or_class,
    CAST(d.signed AS TEXT) AS signed,
    '' AS status,
    '' AS start_type
  FROM drivers d
  WHERE
    lower(COALESCE(d.service, '')) LIKE '%cisco%'
    OR lower(COALESCE(d.device_name, '')) LIKE '%cisco%'
    OR lower(COALESCE(d.description, '')) LIKE '%cisco%'
    OR lower(COALESCE(d.provider, '')) LIKE '%cisco%'
    OR lower(COALESCE(d.manufacturer, '')) LIKE '%cisco%'
    OR lower(COALESCE(d.image, '')) LIKE '%\cisco\%'
    OR lower(COALESCE(d.image, '')) LIKE '%secure client%'
    OR lower(COALESCE(d.image, '')) LIKE '%orbital%'
    OR lower(COALESCE(d.image, '')) LIKE '%forensics%'
    OR lower(COALESCE(d.service, '')) LIKE '%immunet%'
    OR lower(COALESCE(d.device_name, '')) LIKE '%immunet%'
    OR lower(COALESCE(d.description, '')) LIKE '%immunet%'
    OR lower(COALESCE(d.service, '')) LIKE '%amp%'
    OR lower(COALESCE(d.device_name, '')) LIKE '%amp%'
    OR lower(COALESCE(d.description, '')) LIKE '%amp%'
    OR lower(COALESCE(d.provider, '')) LIKE '%bitdefender%'
    OR lower(COALESCE(d.manufacturer, '')) LIKE '%bitdefender%'
),
service_driver_candidates AS (
  SELECT
    'services' AS source_table,
    COALESCE(s.name, '') AS item_name,
    COALESCE(s.display_name, '') AS display_name,
    COALESCE(NULLIF(s.path, ''), s.module_path, '') AS path_or_image,
    COALESCE(s.description, '') AS description,
    '' AS provider,
    '' AS manufacturer,
    '' AS version,
    COALESCE(s.service_type, '') AS type_or_class,
    '' AS signed,
    COALESCE(s.status, '') AS status,
    COALESCE(s.start_type, '') AS start_type
  FROM services s
  WHERE
    lower(COALESCE(s.service_type, '')) LIKE '%driver%'
    AND (
      lower(COALESCE(s.name, '')) LIKE '%cisco%'
      OR lower(COALESCE(s.display_name, '')) LIKE '%cisco%'
      OR lower(COALESCE(s.description, '')) LIKE '%cisco%'
      OR lower(COALESCE(s.path, '')) LIKE '%\cisco\%'
      OR lower(COALESCE(s.module_path, '')) LIKE '%\cisco\%'
      OR lower(COALESCE(s.path, '')) LIKE '%secure client%'
      OR lower(COALESCE(s.module_path, '')) LIKE '%secure client%'
      OR lower(COALESCE(s.path, '')) LIKE '%orbital%'
      OR lower(COALESCE(s.module_path, '')) LIKE '%orbital%'
      OR lower(COALESCE(s.path, '')) LIKE '%forensics%'
      OR lower(COALESCE(s.module_path, '')) LIKE '%forensics%'
      OR lower(COALESCE(s.name, '')) LIKE '%immunet%'
      OR lower(COALESCE(s.display_name, '')) LIKE '%immunet%'
      OR lower(COALESCE(s.description, '')) LIKE '%immunet%'
      OR lower(COALESCE(s.name, '')) LIKE '%amp%'
      OR lower(COALESCE(s.display_name, '')) LIKE '%amp%'
      OR lower(COALESCE(s.description, '')) LIKE '%amp%'
    )
)
SELECT DISTINCT
  source_table,
  item_name,
  display_name,
  path_or_image,
  description,
  provider,
  manufacturer,
  version,
  type_or_class,
  signed,
  status,
  start_type
FROM (
  SELECT * FROM driver_candidates
  UNION ALL
  SELECT * FROM service_driver_candidates
)
WHERE lower(item_name) NOT IN (
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
  AND lower(path_or_image) NOT LIKE '%bddci.sys%'
  AND lower(path_or_image) NOT LIKE '%trufos.sys%'
  AND lower(path_or_image) NOT LIKE '%immunetselfprotect.sys%'
  AND lower(path_or_image) NOT LIKE '%immunetprotect.sys%'
  AND lower(path_or_image) NOT LIKE '%immunetnetworkmonitor.sys%'
  AND lower(path_or_image) NOT LIKE '%ciscoampheurdriver.sys%'
  AND lower(path_or_image) NOT LIKE '%ciscoampelamdriver.sys%'
  AND lower(path_or_image) NOT LIKE '%ciscoampcefwdriver.sys%'
  AND lower(path_or_image) NOT LIKE '%ancrcl64.sys%'
ORDER BY source_table, item_name, path_or_image;
