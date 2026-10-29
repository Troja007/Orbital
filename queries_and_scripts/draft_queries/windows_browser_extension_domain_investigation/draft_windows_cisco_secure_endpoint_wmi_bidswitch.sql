-- Cisco Secure Endpoint WMI-channel records containing the target domain.
SELECT
  datetime,
  provider_name,
  eventid,
  level,
  data
FROM windows_eventlog
WHERE channel = 'CiscoSecureEndpoint/WMI'
  AND lower(data) LIKE '%bidswitch.net%'
ORDER BY datetime DESC
LIMIT 200;
