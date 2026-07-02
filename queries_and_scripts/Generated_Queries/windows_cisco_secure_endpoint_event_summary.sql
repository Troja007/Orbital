SELECT
  eventid,
  CASE
    WHEN eventid = 1800 THEN 'Allow'
    WHEN eventid = 1801 THEN 'Block'
    ELSE 'Other'
  END AS action,
  count(*) AS event_count,
  min(datetime) AS oldest_event_time,
  max(datetime) AS newest_event_time
FROM windows_eventlog
WHERE channel = 'CiscoSecureEndpoint/Events'
  AND eventid IN (1800, 1801)
GROUP BY eventid
ORDER BY eventid;
