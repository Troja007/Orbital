-- Startup registrations whose executable path or arguments reference the domain.
SELECT
  name,
  path,
  args,
  type,
  source,
  status,
  username
FROM startup_items
WHERE lower(COALESCE(path, '')) LIKE '%bidswitch.net%'
   OR lower(COALESCE(args, '')) LIKE '%bidswitch.net%'
ORDER BY type, name, path;
