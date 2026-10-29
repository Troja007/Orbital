-- Sysmon process, network, and DNS events containing the target domain.
SELECT
  datetime,
  provider_name,
  eventid,
  level,
  data
FROM windows_eventlog
WHERE channel = 'Microsoft-Windows-Sysmon/Operational'
  AND eventid IN (1, 3, 22)
  AND lower(data) LIKE '%bidswitch.net%'
ORDER BY datetime DESC
LIMIT 200;
