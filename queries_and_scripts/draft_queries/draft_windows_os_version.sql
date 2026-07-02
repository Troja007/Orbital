SELECT
  si.hostname AS computer_name,
  ov.name AS operating_system,
  ov.version,
  ov.platform,
  ov.platform_like,
  ov.arch
FROM os_version ov
CROSS JOIN system_info si
ORDER BY computer_name ASC;
