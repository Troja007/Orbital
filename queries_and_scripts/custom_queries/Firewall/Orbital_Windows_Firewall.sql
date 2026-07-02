SELECT
  REPLACE(REPLACE(REPLACE(SUBSTR(datetime, 1, 19), 'T', ' '), '.', ''), 'Z', '') AS "timestamp_evt",
  datetime(CAST(JSON_EXTRACT(data, '$.EventData.Timestamp') AS INTEGER) / 1000, 'unixepoch', 'localtime') AS "timestamp_fw",
  JSON_EXTRACT(json(data), '$.EventData.Protocol') AS "protocol",
  JSON_EXTRACT(json(data), '$.EventData.LocalIP') AS "source_ip",
  JSON_EXTRACT(json(data), '$.EventData.LocalPort') AS "source_port",
  JSON_EXTRACT(json(data), '$.EventData.RemoteIP') AS "remote_ip",
  JSON_EXTRACT(json(data), '$.EventData.RemotePort') AS "remote_port",
  --!JSON_EXTRACT(json(data), '$.EventData.action') AS "action",
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
  eventid
FROM
  windows_eventlog
WHERE
  channel = 'CiscoSecureEndpoint/Events'
  AND eventid IN (1801, 1800)
  AND direction IN ('OUTGOING', 'INCOMING')
  AND action IN ('Block', 'Allow')
  AND ApplicationPath not like "%sfc.exe"
  AND ApplicationPath not like "%Cisco Secure Client%"
  AND remote_port = "9000"
ORDER BY datetime DESC
LIMIT 500 OFFSET 0;
