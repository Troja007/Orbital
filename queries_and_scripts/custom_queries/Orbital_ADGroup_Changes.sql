SELECT
  REPLACE(REPLACE(REPLACE(SUBSTR(datetime, 1, 19), 'T', ' '), '.', ''), 'Z', '') AS "timestamp_evt",
  JSON_EXTRACT(json(data), '$.EventData.TargetUserSid') AS "SubjectUserSid",
  JSON_EXTRACT(json(data), '$.EventData.SubjectUserName') AS "SubjectUserName",
  JSON_EXTRACT(json(data), '$.EventData.SubjectDomainName') AS "SubjectDomainName",
  JSON_EXTRACT(json(data), '$.EventData.TargetUserName') AS "Domain Group",
  JSON_EXTRACT(json(data), '$.EventData.WorkstationName') AS "WorkstationName",
  JSON_EXTRACT(json(data), '$.EventData.MemberName') AS "UserName",
  CASE
    WHEN eventid = 4662 THEN 'Directory Service Access'
    WHEN eventid = 4737 THEN 'Securtiy Group Management'
    WHEN eventid = 4672 THEN 'Special Logon'
    WHEN eventid = 4624 THEN 'Logon'
    WHEN eventid = 4728 THEN 'Security Group Management'
    ELSE 'Other'
  END AS "Task Category",
  eventid,
  data
FROM
  windows_eventlog
WHERE
channel = 'Security'
--!AND eventid IN (4662,4737,4728,4672,4624)
AND eventid IN (4728)
ORDER BY datetime DESC
LIMIT 5 OFFSET 0;
