-- Scheduled tasks whose action or path references the domain.
SELECT
  name,
  action,
  path,
  enabled,
  state,
  hidden,
  last_run_time,
  next_run_time,
  last_run_message,
  last_run_code
FROM scheduled_tasks
WHERE lower(COALESCE(action, '')) LIKE '%bidswitch.net%'
   OR lower(COALESCE(path, '')) LIKE '%bidswitch.net%'
ORDER BY name, action;
