-- Active Chromium extensions with broad host access for correlation with domain hits.
SELECT
  browser_type,
  uid,
  profile,
  name,
  identifier,
  version,
  referenced,
  state,
  permissions_json,
  optional_permissions_json,
  manifest_hash,
  path
FROM chrome_extensions
WHERE state = '1'
  AND (
    lower(permissions_json) LIKE '%<all_urls>%'
    OR lower(optional_permissions_json) LIKE '%<all_urls>%'
    OR lower(manifest_json) LIKE '%://*%'
  )
ORDER BY browser_type, uid, profile, name, identifier, version;
