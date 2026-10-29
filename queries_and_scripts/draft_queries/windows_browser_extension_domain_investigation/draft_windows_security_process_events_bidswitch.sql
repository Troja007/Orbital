-- Security process-creation events whose retained command line includes the domain.
SELECT
  datetime,
  provider_name,
  eventid,
  level,
  data
FROM windows_eventlog
WHERE channel = 'Security'
  AND eventid = 4688
  AND lower(data) LIKE '%bidswitch.net%'
ORDER BY datetime DESC
LIMIT 200;
