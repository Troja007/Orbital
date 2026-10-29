-- Cisco Secure Endpoint Events-channel records containing the target domain.
SELECT
  datetime,
  provider_name,
  eventid,
  level,
  data
FROM windows_eventlog
WHERE channel = 'CiscoSecureEndpoint/Events'
  AND lower(data) LIKE '%bidswitch.net%'
ORDER BY datetime DESC
LIMIT 200;
