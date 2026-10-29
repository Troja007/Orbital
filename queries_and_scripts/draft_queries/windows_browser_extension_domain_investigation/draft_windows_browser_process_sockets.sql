-- Current browser sockets. Remote IPs require external DNS/proxy correlation to prove domain use.
SELECT
  p.pid,
  p.name AS process_name,
  p.path AS process_path,
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
WHERE lower(p.name) IN (
  'chrome.exe',
  'msedge.exe',
  'brave.exe',
  'opera.exe',
  'firefox.exe'
)
  AND pos.remote_address NOT IN ('', '0.0.0.0', '127.0.0.1', '::', '::1')
ORDER BY p.name, p.pid, pos.remote_address, pos.remote_port;
