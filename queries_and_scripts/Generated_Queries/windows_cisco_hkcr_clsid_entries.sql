WITH matching_clsids AS (
  SELECT DISTINCT key AS clsid_key
  FROM registry
  WHERE key LIKE 'HKEY_CLASSES_ROOT\CLSID\{%'
    AND (
      data LIKE '%Cisco%'
      OR data LIKE '%AnyConnect%'
      OR data LIKE '%Secure Client%'
      OR data LIKE '%SecureClient%'
    )
)
SELECT
  r.key AS reg_key,
  r.path,
  r.name,
  r.type,
  r.data,
  datetime(r.mtime, 'unixepoch', 'UTC') AS modified_utc
FROM registry r
JOIN matching_clsids m
  ON r.key = m.clsid_key
  OR r.key LIKE m.clsid_key || '\%'
ORDER BY r.key, r.path, r.name
LIMIT 500;
