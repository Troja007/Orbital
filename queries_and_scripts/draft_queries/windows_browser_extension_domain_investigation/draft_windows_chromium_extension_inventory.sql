-- Full Chromium-based extension inventory for later ID/path/policy correlation.
SELECT
  ce.browser_type,
  ce.uid,
  COALESCE(u.username, '') AS username,
  ce.profile,
  ce.name,
  ce.identifier,
  ce.referenced_identifier,
  ce.version,
  ce.description,
  ce.referenced,
  ce.state,
  ce.from_webstore,
  ce.update_url,
  ce.install_timestamp,
  ce.manifest_hash,
  ce.path
FROM chrome_extensions ce
LEFT JOIN users u ON u.uid = ce.uid
ORDER BY ce.browser_type, ce.uid, ce.profile, ce.name, ce.identifier, ce.version;
