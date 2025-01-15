SELECT p.pid, p.name,
ROUND((p.resident_size / 1024 / 1024) ,0) AS "Memory WorkingSet MB",
ROUND((p.total_size / 1024 / 1024) ,0) AS "Memory Commit MB",
p.threads AS "Thread Count",
ROUND((p.disk_bytes_read / 1024 / 1024 / 1024) ,0) AS "Disk Read GB",
ROUND((p.disk_bytes_written / 1024 / 1024 / 1024) ,0) AS "Disk Write GB",
ROUND((p.elapsed_time / 3600) ,0) AS "Uptime Hours",
p.path,
sha256

--ROUND((total_size * '10e-7') ,0) AS Wert_2
FROM processes p

LEFT JOIN hash h on p.path = h.path

where p.path like "%cisco%"



ORDER BY total_size
DESC LIMIT 100;
