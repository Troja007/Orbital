SELECT pid, name, 
ROUND((resident_size / 1024 / 1024) ,0) AS "priv mem (MB)",
ROUND((elapsed_time / 3600) ,0) AS "uptime hours",
path
FROM processes

where path like "%cisco%"
OR name in (
    "acnamagent.exe",
    "acnvmagent.exe",
    "acnamlogonagent.exe",
    "acumbrellaagent.exe",
    "cscm.exe", 
    "csc_cmid.exe", 
    "csc_cms", 
    "csc_pm.exe",
    "csc_iseagent.exe",
    "csc_iseposture.exe",
    "csc_ui.exe", 
    "orbital.exe", 
    "osqueryd.exe", 
    "sfc.exe", 
    "vpnagent.exe", 
    "dnscryptproxy.exe",
    "csc_zta_agent.exe",
    "DUO Desktop,exe",
    "vpnagent.exe")

ORDER BY name ASC
LIMIT 100;
