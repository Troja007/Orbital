SELECT
  si.hostname AS host,
  'installed_program' AS evidence_type,
  pr.name AS item_name,
  pr.version AS version_or_status,
  pr.install_location AS path_or_location,
  COALESCE(pr.publisher, '') || ' | install_date=' || COALESCE(pr.install_date, '') || ' | install_source=' || COALESCE(pr.install_source, '') || ' | uninstall=' || COALESCE(pr.uninstall_string, '') AS detail,
  'programs' AS source
FROM programs pr
CROSS JOIN system_info si
WHERE lower(pr.name) LIKE '%cisco%'
   OR lower(pr.publisher) LIKE '%cisco%'
   OR lower(pr.name) LIKE '%secure client%'
   OR lower(pr.name) LIKE '%secure endpoint%'
   OR lower(pr.name) LIKE '%amp%'
   OR lower(pr.name) LIKE '%anyconnect%'

UNION ALL

SELECT
  si.hostname AS host,
  'installer_registry' AS evidence_type,
  r.key || '\' || r.name AS item_name,
  r.type AS version_or_status,
  r.path AS path_or_location,
  r.data AS detail,
  'registry' AS source
FROM registry r
CROSS JOIN system_info si
WHERE (
    r.key LIKE 'HKEY_CLASSES_ROOT\Installer\Products\%%'
    OR r.key LIKE 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\%%'
    OR r.key LIKE 'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\%%'
  )
  AND (
    lower(r.data) LIKE '%cisco%'
    OR lower(r.data) LIKE '%secure client%'
    OR lower(r.data) LIKE '%secure endpoint%'
    OR lower(r.data) LIKE '%amp%'
    OR lower(r.data) LIKE '%anyconnect%'
  )

UNION ALL

SELECT
  si.hostname AS host,
  'service' AS evidence_type,
  s.name AS item_name,
  COALESCE(s.status, '') || ' / ' || COALESCE(s.start_type, '') AS version_or_status,
  COALESCE(s.path, s.module_path, '') AS path_or_location,
  COALESCE(s.display_name, '') || ' | ' || COALESCE(s.description, '') || ' | account=' || COALESCE(s.user_account, '') || ' | pid=' || CAST(COALESCE(s.pid, -1) AS TEXT) AS detail,
  'services' AS source
FROM services s
CROSS JOIN system_info si
WHERE lower(s.name) LIKE '%cisco%'
   OR lower(s.display_name) LIKE '%cisco%'
   OR lower(s.description) LIKE '%cisco%'
   OR lower(s.path) LIKE '%cisco%'
   OR lower(s.module_path) LIKE '%cisco%'
   OR lower(s.name) IN ('csc_nvmagent', 'csc_umbrellaagent')

UNION ALL

SELECT
  si.hostname AS host,
  'running_process' AS evidence_type,
  p.name AS item_name,
  'pid=' || CAST(p.pid AS TEXT) || ' state=' || COALESCE(p.state, '') AS version_or_status,
  p.path AS path_or_location,
  p.cmdline AS detail,
  'processes' AS source
FROM processes p
CROSS JOIN system_info si
WHERE lower(p.path) LIKE '%cisco%'
   OR lower(p.path) LIKE '%secure client%'
   OR lower(p.path) LIKE '%amp%'
   OR lower(p.name) IN (
    'sfc.exe',
    'cscm.exe',
    'csc_ui.exe',
    'vpnagent.exe',
    'acnvmagent.exe',
    'csc_cmid.exe',
    'csc_cms.exe',
    'csc_pm.exe'
  )
ORDER BY evidence_type, item_name;
