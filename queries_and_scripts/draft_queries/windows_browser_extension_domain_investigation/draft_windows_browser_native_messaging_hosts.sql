-- Native-messaging registrations that let Chrome or Edge extensions invoke local software.
SELECT
  key,
  name,
  type,
  data,
  datetime(mtime, 'unixepoch', 'UTC') AS modified_utc
FROM registry
WHERE key LIKE 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Google\\Chrome\\NativeMessagingHosts\\%'
   OR key LIKE 'HKEY_CURRENT_USER\\SOFTWARE\\Google\\Chrome\\NativeMessagingHosts\\%'
   OR key LIKE 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Edge\\NativeMessagingHosts\\%'
   OR key LIKE 'HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Edge\\NativeMessagingHosts\\%'
ORDER BY key, name;
