SELECT
  'secure_client_cisco_branch' AS evidence_type,
  key AS reg_key,
  path,
  name,
  type,
  data,
  datetime(mtime, 'unixepoch', 'UTC') AS modified_utc
FROM registry
WHERE key LIKE 'HKEY_LOCAL_MACHINE\SOFTWARE\Cisco\SecureClient%'
   OR path LIKE '\HKEY_LOCAL_MACHINE\SOFTWARE\Cisco\SecureClient%'
   OR key LIKE 'HKEY_LOCAL_MACHINE\SOFTWARE\Cisco\Cisco Secure Client%'
   OR path LIKE '\HKEY_LOCAL_MACHINE\SOFTWARE\Cisco\Cisco Secure Client%'
   OR key LIKE 'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Cisco\SecureClient%'
   OR path LIKE '\HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Cisco\SecureClient%'
   OR key LIKE 'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Cisco\Cisco Secure Client%'
   OR path LIKE '\HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Cisco\Cisco Secure Client%'
   OR key LIKE 'HKEY_LOCAL_MACHINE\SOFTWARE\Cisco\Cloud Management%'
   OR path LIKE '\HKEY_LOCAL_MACHINE\SOFTWARE\Cisco\Cloud Management%'
   OR key LIKE 'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Cisco\Cloud Management%'
   OR path LIKE '\HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Cisco\Cloud Management%'

UNION ALL

SELECT
  'secure_client_uninstall_entry' AS evidence_type,
  key AS reg_key,
  path,
  name,
  type,
  data,
  datetime(mtime, 'unixepoch', 'UTC') AS modified_utc
FROM registry
WHERE (
    key LIKE 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\%'
    OR path LIKE '\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\%'
    OR key LIKE 'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\%'
    OR path LIKE '\HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\%'
  )
  AND (
    data LIKE '%Cisco Secure Client%'
    OR data LIKE '%SecureClientUI%'
    OR data LIKE '%AnyConnect%'
  )

UNION ALL

SELECT
  'secure_client_installer_product_entry' AS evidence_type,
  key AS reg_key,
  path,
  name,
  type,
  data,
  datetime(mtime, 'unixepoch', 'UTC') AS modified_utc
FROM registry
WHERE (
    key LIKE 'HKEY_CLASSES_ROOT\Installer\Products\%'
    OR path LIKE '\HKEY_CLASSES_ROOT\Installer\Products\%'
  )
  AND (
    data LIKE '%Cisco Secure Client%'
    OR data LIKE '%SecureClientUI%'
    OR data LIKE '%AnyConnect%'
  )
ORDER BY evidence_type, reg_key, path, name
LIMIT 500;
