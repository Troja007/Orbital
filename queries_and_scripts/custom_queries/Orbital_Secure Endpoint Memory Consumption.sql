SELECT pid, name, 
ROUND((resident_size / 1024 / 1024) ,0) AS "Memory WorkingSet MB",
ROUND((total_size / 1024 / 1024) ,0) AS "Memory Commit MB",
threads AS "Thread Count",
ROUND((disk_bytes_read / 1024 / 1024 / 1024) ,0) AS "Disk Read GB",
ROUND((disk_bytes_written / 1024 / 1024 / 1024) ,0) AS "Disk Write GB",
ROUND((elapsed_time / 3600) ,0) AS "Uptime Hours",
path

--ROUND((total_size * '10e-7') ,0) AS Wert_2
FROM processes

where path like "%cisco%"



ORDER BY total_size
DESC LIMIT 100;
