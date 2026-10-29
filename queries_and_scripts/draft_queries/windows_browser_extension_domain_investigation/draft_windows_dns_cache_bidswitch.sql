-- Current Windows DNS-cache evidence for the exact domain and its suffix.
SELECT
  name AS domain,
  type AS record_type,
  flags
FROM dns_cache
WHERE lower(name) = 'x.bidswitch.net'
   OR lower(name) LIKE '%.bidswitch.net'
ORDER BY domain, record_type;
