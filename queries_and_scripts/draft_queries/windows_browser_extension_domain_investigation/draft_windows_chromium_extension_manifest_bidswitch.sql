-- Chromium extension metadata or manifest fields that directly mention the domain.
SELECT
  browser_type,
  uid,
  profile,
  name,
  identifier,
  version,
  referenced,
  state,
  from_webstore,
  update_url,
  permissions_json,
  optional_permissions_json,
  manifest_hash,
  path
FROM chrome_extensions
WHERE lower(manifest_json) LIKE '%bidswitch.net%'
   OR lower(permissions_json) LIKE '%bidswitch.net%'
   OR lower(optional_permissions_json) LIKE '%bidswitch.net%'
   OR lower(update_url) LIKE '%bidswitch.net%'
   OR lower(description) LIKE '%bidswitch%'
ORDER BY browser_type, uid, name, identifier, version;
