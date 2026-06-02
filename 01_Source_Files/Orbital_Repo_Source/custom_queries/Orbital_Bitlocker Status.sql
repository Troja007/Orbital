SELECT drive_letter AS device_id,

CASE WHEN (conversion_status = 1 AND protection_status = 1)
  THEN TRUE
  ELSE FALSE
  END AS encrypted,
  encryption_method AS method,
  percentage_encrypted AS progress
FROM bitlocker_info;
