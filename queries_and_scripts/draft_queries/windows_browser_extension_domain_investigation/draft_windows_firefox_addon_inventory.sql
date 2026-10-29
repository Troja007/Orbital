-- Full Firefox extension/addon inventory for later ID/path correlation.
SELECT
  fa.uid,
  COALESCE(u.username, '') AS username,
  fa.name,
  fa.identifier,
  fa.creator,
  fa.type,
  fa.version,
  fa.source_url,
  fa.visible,
  fa.active,
  fa.disabled,
  fa.autoupdate,
  fa.location,
  fa.path
FROM firefox_addons fa
LEFT JOIN users u ON u.uid = fa.uid
ORDER BY fa.uid, fa.active DESC, fa.name, fa.identifier, fa.version;
