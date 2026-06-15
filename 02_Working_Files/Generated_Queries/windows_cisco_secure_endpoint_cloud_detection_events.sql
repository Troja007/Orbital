SELECT
  datetime AS event_time,
  channel,
  provider_name,
  eventid,
  level,
  computer_name,
  CASE
    WHEN data LIKE '%EVENT_DETECTION%' THEN 'EVENT_DETECTION'
    ELSE ''
  END AS detection_type,
  substr(data, 1, 1600) AS event_data
FROM windows_eventlog
WHERE channel = 'CiscoSecureEndpoint/Cloud'
  AND eventid = 401
  AND data LIKE '%EVENT_DETECTION%'
ORDER BY datetime DESC
LIMIT 50;
