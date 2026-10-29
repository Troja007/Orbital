-- Browser and proxy configuration values that directly reference the domain.
SELECT
  key,
  name,
  type,
  data,
  datetime(mtime, 'unixepoch', 'UTC') AS modified_utc
FROM registry
WHERE key IN (
  'HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Internet Explorer\\Main',
  'HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Internet Settings',
  'HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\Connections',
  'HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Google\\Chrome',
  'HKEY_CURRENT_USER\\SOFTWARE\\Policies\\Google\\Chrome',
  'HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Edge',
  'HKEY_CURRENT_USER\\SOFTWARE\\Policies\\Microsoft\\Edge'
)
  AND lower(data) LIKE '%bidswitch.net%'
ORDER BY key, name;
