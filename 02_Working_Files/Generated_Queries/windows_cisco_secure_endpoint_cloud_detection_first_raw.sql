SELECT
  datetime AS event_time,
  channel,
  eventid,
  data
FROM windows_eventlog
WHERE channel = 'CiscoSecureEndpoint/Cloud'
  AND eventid = 401
  AND data LIKE '%EVENT_DETECTION%'
ORDER BY datetime DESC
LIMIT 1;
