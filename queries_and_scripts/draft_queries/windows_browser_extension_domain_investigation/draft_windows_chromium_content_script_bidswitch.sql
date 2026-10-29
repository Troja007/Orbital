-- Chromium extension content scripts whose declared match pattern mentions the domain.
SELECT
  browser_type,
  uid,
  identifier,
  version,
  script,
  match,
  referenced,
  profile_path,
  path
FROM chrome_extension_content_scripts
WHERE lower(match) LIKE '%bidswitch.net%'
   OR lower(script) LIKE '%bidswitch%'
ORDER BY browser_type, uid, identifier, version, script;
