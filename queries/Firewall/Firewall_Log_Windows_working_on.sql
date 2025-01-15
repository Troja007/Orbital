SELECT
  REPLACE(REPLACE(REPLACE(SUBSTR(datetime, 1, 19), 'T', ' '), '.', ''), 'Z', '') AS "timestamp_evt",
  datetime(CAST(JSON_EXTRACT(data, '$.EventData.Timestamp') AS INTEGER) / 1000, 'unixepoch', 'localtime') AS "timestamp_fw",
  JSON_EXTRACT(json(data), '$.EventData.Protocol') AS "protocol",
  JSON_EXTRACT(json(data), '$.EventData.LocalIP') AS "source-ip",
  JSON_EXTRACT(json(data), '$.EventData.LocalPort') AS "source-port",
  JSON_EXTRACT(json(data), '$.EventData.RemoteIP') AS "remote-ip",
  JSON_EXTRACT(json(data), '$.EventData.RemotePort') AS "remote-port",
  -- JSON_EXTRACT(json(data), '$.EventData.action') AS "action2",
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
-- Remove the two hiphen in front to mark/unmark a line or parts or a line as a comment.
-- The WHERE statement lets you search for specific content in the firewall log.

  channel = 'CiscoSecureEndpoint/Events'
   --do not remove this line, otherwise the query searches the whole windows event log!!

  AND eventid IN (1801, 1800)
  --Adjust the conditions here: 1800 is for allowed traffic, 1801 for blocked traffic.

  AND direction = 'OUTGOING'
  --use this parameter to filter for incoming and outgoing traffic.
  --AND direction <> 'OUTGOING'
  --same as above, just using the uneven sql statement '<>'.


  AND action = 'Allow'
  --use the values allow or block to filter for the action.


  AND ApplicationPath not like '%sfc.exe'
  --this line removes all entries from the Windows Connector in the output.
    --AND ApplicationPath IN ("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "C:\Windows\System32\svchost.exe")
    --use this line to define specific application paths to be shown.

  AND "remote-ip" IN ("208.67.222.222", "208.67.220.220")
  --use this parameter to filter for a specific list of IPs. Also works with a single entry.
  --AND "remote-ip" like "%208%"
  --use this this query parameter to search for a specific part of an remote-ip.

  AND "remote-port" IN ("443", "80", "53")
  --use this parameter to filter for specific list or remot ports. Also works with a single entry.

  AND "ruleName" == "Allow Umbrella - DNS1"
  --use this parameter to filter based on Firewall Rule Name.
  AND "ruleName" like "%DNS%"
  --use this parameter to filter based on parts of the Firewall Rulename.

  -- the WHERE clause uses the full statement instead of the translated date value from the SQL to avoid translation issues.
  AND datetime(CAST(JSON_EXTRACT(data, '$.EventData.Timestamp') AS INTEGER) / 1000, 'unixepoch', 'localtime') >= datetime('now', '-10 hours')
  -- Filter for last 10 hours. Update the value as needed if the endpoint is not using the UTC timezone
  --use the two statements below to search for a specific date and timerange.
  --AND datetime(CAST(JSON_EXTRACT(data, '$.EventData.Timestamp') AS INTEGER) / 1000, 'unixepoch', 'localtime') >= '2024-03-21 00:00:00' -- Start date condition
  --AND datetime(CAST(JSON_EXTRACT(data, '$.EventData.Timestamp') AS INTEGER) / 1000, 'unixepoch', 'localtime') <= '2024-03-21 23:59:59' -- End date condition


ORDER BY datetime DESC -- order by date and time
LIMIT 500 --limit the output to 500 results
OFFSET 0 -- start with the first entry
;
