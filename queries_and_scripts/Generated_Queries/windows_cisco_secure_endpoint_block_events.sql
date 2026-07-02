SELECT
  datetime AS event_time,
  eventid,
  'Block' AS action,
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
  JSON_EXTRACT(json(data), '$.EventData.AuditRuleName') AS audit_rule_name,
  JSON_EXTRACT(json(data), '$.EventData.AuditRuleAction') AS audit_rule_action
FROM windows_eventlog
WHERE channel = 'CiscoSecureEndpoint/Events'
  AND eventid = 1801
ORDER BY datetime DESC
LIMIT 100;
