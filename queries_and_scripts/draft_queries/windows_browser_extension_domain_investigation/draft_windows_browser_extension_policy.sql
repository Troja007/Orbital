-- Chrome and Edge policy locations that can force-install or configure extensions.
SELECT
  key,
  name,
  type,
  data,
  datetime(mtime, 'unixepoch', 'UTC') AS modified_utc
FROM registry
WHERE key IN (
  'HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Google\\Chrome\\ExtensionInstallForcelist',
  'HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Google\\Chrome\\ExtensionSettings',
  'HKEY_CURRENT_USER\\SOFTWARE\\Policies\\Google\\Chrome\\ExtensionInstallForcelist',
  'HKEY_CURRENT_USER\\SOFTWARE\\Policies\\Google\\Chrome\\ExtensionSettings',
  'HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Edge\\ExtensionInstallForcelist',
  'HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Edge\\ExtensionSettings',
  'HKEY_CURRENT_USER\\SOFTWARE\\Policies\\Microsoft\\Edge\\ExtensionInstallForcelist',
  'HKEY_CURRENT_USER\\SOFTWARE\\Policies\\Microsoft\\Edge\\ExtensionSettings'
)
ORDER BY key, name;
