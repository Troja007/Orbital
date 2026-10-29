-- Running browser command lines with an explicit target-domain reference.
SELECT
  pid,
  name,
  path,
  cmdline,
  datetime(start_time, 'unixepoch', 'UTC') AS process_start_utc
FROM processes
WHERE lower(name) IN ('chrome.exe', 'msedge.exe', 'brave.exe', 'opera.exe', 'firefox.exe')
  AND lower(cmdline) LIKE '%bidswitch.net%'
ORDER BY start_time DESC;
