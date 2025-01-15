SELECT
  REPLACE(REPLACE(REPLACE(SUBSTR(datetime, 1, 19), 'T', ' '), '.', ''), 'Z', '') AS "timestamp_evt",
  datetime(CAST(JSON_EXTRACT(data, '$.EventData.Timestamp') AS INTEGER) / 1000, 'unixepoch', 'localtime') AS "timestamp_fw",
  JSON_EXTRACT(json(data), '$.EventData.Protocol') AS "protocol",
  JSON_EXTRACT(json(data), '$.EventData.LocalIP') AS "source-ip",
  JSON_EXTRACT(json(data), '$.EventData.LocalPort') AS "source-port",
  JSON_EXTRACT(json(data), '$.EventData.RemoteIP') AS "remote-ip",
  JSON_EXTRACT(json(data), '$.EventData.RemotePort') AS "remote-port",
  CASE
    WHEN eventid = 1800 THEN 'Allow'
    WHEN eventid = 1801 THEN 'Block'
    ELSE 'Other'
  END AS action,
  JSON_EXTRACT(json(data), '$.EventData.Direction') AS "direction",
  JSON_EXTRACT(json(data), '$.EventData.PID') AS "pid",
  JSON_EXTRACT(json(data), '$.EventData.Application Path') AS "ApplicationPath",
  JSON_EXTRACT(json(data), '$.EventData.url') AS "url",
  JSON_EXTRACT(json(data), '$.EventData.RuleGUID') AS "ruleGUID",
  JSON_EXTRACT(json(data), '$.EventData.RuleName') AS "ruleName",
  JSON_EXTRACT(json(data), '$.EventData.RuleSetGUID') AS "ConfigurationGuid",
  eventid,
  (
    SELECT COUNT(*) FROM windows_eventlog AS inner_log
    WHERE inner_log.channel = 'CiscoSecureEndpoint/Events'
    AND inner_log.eventid IN (1800, 1801)
    --> AND inner_log.direction = 'OUTGOING'
    --> AND inner_log.action = 'Allow'
    --> AND inner_log.ApplicationPath NOT LIKE '%sfc.exe'
  ) AS allowed_hits,
  (
    SELECT COUNT(*) FROM windows_eventlog AS inner_log
    WHERE inner_log.channel = 'CiscoSecureEndpoint/Events'
    AND inner_log.eventid IN (1800, 1801)
    -->AND inner_log.direction = 'OUTGOING'
    -->AND inner_log.action = 'Block'
    -->AND inner_log.ApplicationPath NOT LIKE '%sfc.exe'
  ) AS blocked_hits
FROM
  windows_eventlog
WHERE
  channel = 'CiscoSecureEndpoint/Events'
  AND eventid IN (1801, 1800)
  AND direction = 'OUTGOING'
  AND ApplicationPath NOT LIKE '%sfc.exe'
ORDER BY datetime DESC
LIMIT 10 OFFSET 0;
