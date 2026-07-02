SELECT
  datetime AS event_time,
  eventid,
  CASE
    WHEN eventid = 1800 THEN 'Allow'
    WHEN eventid = 1801 THEN 'Block'
    ELSE 'Other'
  END AS action,
  JSON_EXTRACT(json(data), '$.EventData.Direction') AS direction,
  JSON_EXTRACT(json(data), '$.EventData.Protocol') AS protocol,
  JSON_EXTRACT(json(data), '$.EventData.LocalIP') AS source_ip,
  JSON_EXTRACT(json(data), '$.EventData.LocalPort') AS source_port,
  JSON_EXTRACT(json(data), '$.EventData.RemoteIP') AS remote_ip,
  JSON_EXTRACT(json(data), '$.EventData.RemotePort') AS remote_port,
  JSON_EXTRACT(json(data), '$.EventData.PID') AS pid,
  JSON_EXTRACT(json(data), '$.EventData.Application Path') AS application_path,
  JSON_EXTRACT(json(data), '$.EventData.url') AS url,
  JSON_EXTRACT(json(data), '$.EventData.RuleName') AS rule_name,
  substr(data, 1, 800) AS event_data
FROM windows_eventlog
WHERE channel = 'CiscoSecureEndpoint/Events'
  AND eventid IN (1800, 1801)
ORDER BY datetime DESC
LIMIT 100;
