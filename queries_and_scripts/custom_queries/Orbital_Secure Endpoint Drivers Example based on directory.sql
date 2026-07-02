select f.path, f.filename, f.product_version,
ROUND((f.size / 1024) ,0) AS "FileSize KB",
h.sha256, a.subject_name, a.issuer_name, a.result,
datetime(f.mtime,"unixepoch","UTC") as last_modification_time
FROM file f
JOIN hash h ON f.path=h.path
JOIN authenticode a ON f.path = a.path

WHERE f.path LIKE "c:\%%\system32\Drivers\%"
AND (f.filename like "%immunet%"
OR f.filename like "%trufos%"
OR f.filename like "%CiscoAMP%") 
