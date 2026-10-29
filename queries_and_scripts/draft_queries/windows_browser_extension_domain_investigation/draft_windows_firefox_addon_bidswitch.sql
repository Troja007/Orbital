-- Firefox addon metadata that directly mentions the target domain.
SELECT
  uid,
  name,
  identifier,
  creator,
  type,
  version,
  source_url,
  active,
  disabled,
  autoupdate,
  location,
  path
FROM firefox_addons
WHERE lower(source_url) LIKE '%bidswitch.net%'
   OR lower(description) LIKE '%bidswitch%'
   OR lower(name) LIKE '%bidswitch%'
ORDER BY uid, name, identifier, version;
