SELECT
  (SELECT hostname FROM system_info LIMIT 1) AS computer_name,
  address,
  hostnames
FROM etc_hosts
WHERE hostnames NOT IN ('localhost', '::1', 'fe00::0', 'ff00::0', 'ff02::1', 'ff02::2')
ORDER BY computer_name ASC, address ASC, hostnames ASC;
