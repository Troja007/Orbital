SELECT
  pid,
  name AS processname,
  path,
  cmdline AS command_line,
  (SELECT hostname FROM system_info LIMIT 1) AS computer_name
FROM processes
WHERE lower(name) = 'sfc.exe'
ORDER BY computer_name ASC;
