-- Cisco Secure Endpoint Cloud-channel records containing the target domain.
SELECT
  datetime,
  provider_name,
  eventid,
  level,
  data
FROM windows_eventlog
WHERE channel = 'CiscoSecureEndpoint/Cloud'
  AND lower(data) LIKE '%bidswitch.net%'
ORDER BY datetime DESC
LIMIT 200;
