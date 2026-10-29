-- Current network connections owned by Microsoft Edge.
SELECT
  p.pid,
  p.name,
  p.path,
  p.cmdline,
  datetime(p.start_time, 'unixepoch', 'UTC') AS process_start_utc,
  pos.protocol,
  pos.local_address,
  pos.local_port,
  pos.remote_address,
  pos.remote_port,
  pos.state
FROM process_open_sockets pos
JOIN processes p ON p.pid = pos.pid
WHERE lower(p.name) = 'msedge.exe'
  AND pos.remote_address NOT IN ('', '0.0.0.0', '127.0.0.1', '::', '::1')
ORDER BY p.pid, pos.remote_address, pos.remote_port;
