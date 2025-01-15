SELECT DISTINCT p.name,
  u.username,
  h.sha256,
  p.path
FROM processes AS p

INNER JOIN hash AS h ON h.path = p.path
INNER JOIN users AS u ON u.uid = p.uid

where p.path like "%cisco%"

-- WHERE p.name like "%trusted%" ORDER BY start_time DESC LIMIT 20;
