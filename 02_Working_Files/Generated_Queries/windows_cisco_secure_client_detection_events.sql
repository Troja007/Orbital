SELECT
  channel,
  datetime,
  level,
  provider_name,
  eventid,
  pid,
  substr(data, 1, 1200) AS event_data
FROM windows_eventlog
WHERE channel = 'CiscoSecureEndpoint/Events'
  AND (
    lower(data) LIKE '%detect%'
    OR lower(data) LIKE '%threat%'
    OR lower(data) LIKE '%malware%'
    OR lower(data) LIKE '%exploit%'
    OR lower(data) LIKE '%block%'
    OR lower(data) LIKE '%quarantine%'
    OR lower(data) LIKE '%convict%'
    OR lower(data) LIKE '%malicious%'
    OR lower(data) LIKE '%prevent%'
    OR lower(data) LIKE '%remediat%'
    OR eventid IN (1800, 1801)
  )

UNION ALL

SELECT
  channel,
  datetime,
  level,
  provider_name,
  eventid,
  pid,
  substr(data, 1, 1200) AS event_data
FROM windows_eventlog
WHERE channel = 'Cisco Secure Client'
  AND (
    lower(data) LIKE '%detect%'
    OR lower(data) LIKE '%threat%'
    OR lower(data) LIKE '%malware%'
    OR lower(data) LIKE '%exploit%'
    OR lower(data) LIKE '%block%'
    OR lower(data) LIKE '%quarantine%'
    OR lower(data) LIKE '%convict%'
    OR lower(data) LIKE '%malicious%'
    OR lower(data) LIKE '%prevent%'
    OR lower(data) LIKE '%remediat%'
  )

UNION ALL

SELECT
  channel,
  datetime,
  level,
  provider_name,
  eventid,
  pid,
  substr(data, 1, 1200) AS event_data
FROM windows_eventlog
WHERE channel = 'Cisco Secure Client - AnyConnect VPN'
  AND (
    lower(data) LIKE '%detect%'
    OR lower(data) LIKE '%threat%'
    OR lower(data) LIKE '%malware%'
    OR lower(data) LIKE '%exploit%'
    OR lower(data) LIKE '%block%'
    OR lower(data) LIKE '%quarantine%'
    OR lower(data) LIKE '%convict%'
    OR lower(data) LIKE '%malicious%'
    OR lower(data) LIKE '%prevent%'
    OR lower(data) LIKE '%remediat%'
  )

UNION ALL

SELECT
  channel,
  datetime,
  level,
  provider_name,
  eventid,
  pid,
  substr(data, 1, 1200) AS event_data
FROM windows_eventlog
WHERE channel = 'Cisco Secure Client - Diagnostics and Reporting Tool'
  AND (
    lower(data) LIKE '%detect%'
    OR lower(data) LIKE '%threat%'
    OR lower(data) LIKE '%malware%'
    OR lower(data) LIKE '%exploit%'
    OR lower(data) LIKE '%block%'
    OR lower(data) LIKE '%quarantine%'
    OR lower(data) LIKE '%convict%'
    OR lower(data) LIKE '%malicious%'
    OR lower(data) LIKE '%prevent%'
    OR lower(data) LIKE '%remediat%'
  )

UNION ALL

SELECT
  channel,
  datetime,
  level,
  provider_name,
  eventid,
  pid,
  substr(data, 1, 1200) AS event_data
FROM windows_eventlog
WHERE channel = 'Cisco Secure Client - Network Visibility Module'
  AND (
    lower(data) LIKE '%detect%'
    OR lower(data) LIKE '%threat%'
    OR lower(data) LIKE '%malware%'
    OR lower(data) LIKE '%exploit%'
    OR lower(data) LIKE '%block%'
    OR lower(data) LIKE '%quarantine%'
    OR lower(data) LIKE '%convict%'
    OR lower(data) LIKE '%malicious%'
    OR lower(data) LIKE '%prevent%'
    OR lower(data) LIKE '%remediat%'
  )
ORDER BY datetime DESC
LIMIT 100;
