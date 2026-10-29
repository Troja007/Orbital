-- Windows services whose configuration directly references the domain.
SELECT
  name,
  display_name,
  status,
  start_type,
  path,
  module_path,
  description,
  user_account
FROM services
WHERE lower(COALESCE(path, '')) LIKE '%bidswitch.net%'
   OR lower(COALESCE(module_path, '')) LIKE '%bidswitch.net%'
   OR lower(COALESCE(description, '')) LIKE '%bidswitch.net%'
ORDER BY name;
