SELECT
  si.hostname AS host,
  'dns_cache' AS evidence_area,
  'dns_cache' AS source_table,
  dc.name AS indicator,
  dc.type AS protocol_or_type,
  '' AS process_name,
  '' AS process_path,
  '' AS local_address,
  '' AS local_port,
  '' AS remote_address,
  '' AS remote_port,
  'flags=' || CAST(dc.flags AS TEXT) AS detail,
  '' AS event_time
FROM dns_cache dc
CROSS JOIN system_info si
WHERE lower(dc.name) LIKE '%microsoft.com%'

UNION ALL

SELECT
  si.hostname AS host,
  'hosts_file' AS evidence_area,
  'etc_hosts' AS source_table,
  eh.hostnames AS indicator,
  '' AS protocol_or_type,
  '' AS process_name,
  '' AS process_path,
  eh.address AS local_address,
  '' AS local_port,
  '' AS remote_address,
  '' AS remote_port,
  'hosts mapping=' || eh.address || ' ' || eh.hostnames AS detail,
  '' AS event_time
FROM etc_hosts eh
CROSS JOIN system_info si
WHERE lower(eh.hostnames) LIKE '%microsoft.com%'

UNION ALL

SELECT
  si.hostname AS host,
  'active_socket_process_domain_literal' AS evidence_area,
  'process_open_sockets+processes' AS source_table,
  p.name AS indicator,
  CASE pos.protocol
    WHEN 6 THEN 'tcp'
    WHEN 17 THEN 'udp'
    ELSE CAST(pos.protocol AS TEXT)
  END AS protocol_or_type,
  p.name AS process_name,
  p.path AS process_path,
  pos.local_address AS local_address,
  CAST(pos.local_port AS TEXT) AS local_port,
  pos.remote_address AS remote_address,
  CAST(pos.remote_port AS TEXT) AS remote_port,
  'socket_state=' || COALESCE(pos.state, '') || '; cmdline=' || COALESCE(p.cmdline, '') AS detail,
  datetime(p.start_time, 'unixepoch') AS event_time
FROM process_open_sockets pos
CROSS JOIN system_info si
LEFT JOIN processes p ON p.pid = pos.pid
WHERE pos.remote_address NOT IN ('', '0.0.0.0', '::', '::1', '127.0.0.1')
  AND (
    lower(COALESCE(p.path, '')) LIKE '%microsoft.com%'
    OR lower(COALESCE(p.cmdline, '')) LIKE '%microsoft.com%'
  )

UNION ALL

SELECT
  si.hostname AS host,
  'windows_eventlog_dns_client_domain_match' AS evidence_area,
  'windows_eventlog' AS source_table,
  wel.provider_name || ':' || CAST(wel.eventid AS TEXT) AS indicator,
  wel.channel AS protocol_or_type,
  p.name AS process_name,
  p.path AS process_path,
  '' AS local_address,
  '' AS local_port,
  '' AS remote_address,
  '' AS remote_port,
  substr(wel.data, 1, 500) AS detail,
  wel.datetime AS event_time
FROM windows_eventlog wel
CROSS JOIN system_info si
LEFT JOIN processes p ON p.pid = wel.pid
WHERE lower(wel.data) LIKE '%microsoft.com%'
  AND wel.channel = 'Microsoft-Windows-DNS-Client/Operational'

UNION ALL

SELECT
  si.hostname AS host,
  'windows_eventlog_secure_endpoint_domain_match' AS evidence_area,
  'windows_eventlog' AS source_table,
  wel.provider_name || ':' || CAST(wel.eventid AS TEXT) AS indicator,
  wel.channel AS protocol_or_type,
  p.name AS process_name,
  p.path AS process_path,
  '' AS local_address,
  '' AS local_port,
  '' AS remote_address,
  '' AS remote_port,
  substr(wel.data, 1, 500) AS detail,
  wel.datetime AS event_time
FROM windows_eventlog wel
CROSS JOIN system_info si
LEFT JOIN processes p ON p.pid = wel.pid
WHERE lower(wel.data) LIKE '%microsoft.com%'
  AND wel.channel = 'CiscoSecureEndpoint/Events'
ORDER BY evidence_area, event_time DESC, process_name, indicator;
