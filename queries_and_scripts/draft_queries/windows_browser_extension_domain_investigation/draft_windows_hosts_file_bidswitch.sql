-- Local hosts-file mappings that override the target domain or its suffix.
SELECT
  address,
  hostnames
FROM etc_hosts
WHERE lower(hostnames) = 'x.bidswitch.net'
   OR lower(hostnames) LIKE '%.bidswitch.net'
ORDER BY hostnames, address;
