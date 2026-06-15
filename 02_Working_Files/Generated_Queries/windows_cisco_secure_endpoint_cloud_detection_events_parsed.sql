WITH cloud_events AS (
  SELECT
    datetime AS event_time,
    eventid,
    JSON_EXTRACT(json(data), '$.EventData.JsonEvent') AS json_event
  FROM windows_eventlog
  WHERE channel = 'CiscoSecureEndpoint/Cloud'
    AND eventid = 401
    AND data LIKE '%EVENT_DETECTION%'
)
SELECT
  event_time,
  eventid,
  'EVENT_DETECTION' AS detection_type,
  JSON_EXTRACT(json(json_event), '$.dnm') AS detection_name,
  JSON_EXTRACT(json(json_event), '$.fnd') AS file_name,
  JSON_EXTRACT(json(json_event), '$.fpd') AS file_path,
  JSON_EXTRACT(json(json_event), '$.fnp') AS parent_file_name,
  JSON_EXTRACT(json(json_event), '$.pid') AS pid,
  JSON_EXTRACT(json(json_event), '$.dete') AS detection_engine,
  JSON_EXTRACT(json(json_event), '$.sha256d') AS sha256,
  JSON_EXTRACT(json(json_event), '$.md5d') AS md5,
  JSON_EXTRACT(json(json_event), '$.dfc') AS detection_file_context,
  JSON_EXTRACT(json(json_event), '$.dfs') AS disposition
FROM cloud_events
ORDER BY event_time DESC
LIMIT 50;
