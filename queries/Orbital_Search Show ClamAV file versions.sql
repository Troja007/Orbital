SELECT path, file_version,
ROUND(size / 1024) AS "size (KB)",
ROUND(size / 1024 / 1024) AS "size (MB)",
type,
strftime('%Y-%m-%d %H:%M:%S',btime,'unixepoch') AS file_created,
strftime('%Y-%m-%d %H:%M:%S',mtime,'unixepoch') AS last_modified,
strftime('%Y-%m-%d %H:%M:%S',atime,'unixepoch') AS last_access

FROM file
-- do NOT use this query without a path parameter
-- witout, it could cause high load on the endpoint

WHERE path LIKE "C:\Program Files\Cisco\amp\clamav\%%"
AND file_version != ""
ORDER BY size DESC;
