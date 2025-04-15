SELECT pid, name, 
ROUND((resident_size / 1024 / 1024) ,0) AS "priv mem (MB)",
ROUND((elapsed_time / 3600) ,0) AS "uptime hours",
path
FROM processes

where path like "%cisco%"
OR name in ("acnvmagent.exe", "cscm.exe", "csc_cmid.exe", "csc_cms", "csc_pm.exe", "orbital.exe", "osqueryd.exe", "sfc.exe", "vpnagent.exe")



ORDER BY total_size
DESC LIMIT 100;
