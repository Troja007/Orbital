SELECT
  'Cisco Network Visibility Module' AS module,
  'Installed' AS status,
  package_id,
  version
FROM package_receipts
WHERE LOWER(package_id) LIKE '%cisco%'
  AND (
    LOWER(package_id) LIKE '%nvm%'
    OR LOWER(package_id) LIKE '%network%visibility%'
  )
ORDER BY install_time DESC
LIMIT 1;