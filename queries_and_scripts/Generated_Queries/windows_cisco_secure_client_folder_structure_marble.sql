WITH cisco_dirs AS (
  SELECT
    'C:\Program Files\Cisco' AS root,
    f.path,
    f.directory,
    f.filename,
    f.type,
    f.size,
    f.btime,
    f.mtime
  FROM file f
  WHERE f.type = 'directory'
    AND (
      f.path = 'C:\Program Files\Cisco'
      OR f.path LIKE 'C:\Program Files\Cisco\%'
    )
  UNION ALL
  SELECT
    'C:\Program Files (x86)\Cisco' AS root,
    f.path,
    f.directory,
    f.filename,
    f.type,
    f.size,
    f.btime,
    f.mtime
  FROM file f
  WHERE f.type = 'directory'
    AND (
      f.path = 'C:\Program Files (x86)\Cisco'
      OR f.path LIKE 'C:\Program Files (x86)\Cisco\%'
    )
  UNION ALL
  SELECT
    'C:\ProgramData\Cisco' AS root,
    f.path,
    f.directory,
    f.filename,
    f.type,
    f.size,
    f.btime,
    f.mtime
  FROM file f
  WHERE f.type = 'directory'
    AND (
      f.path = 'C:\ProgramData\Cisco'
      OR f.path LIKE 'C:\ProgramData\Cisco\%'
    )
)
SELECT
  root,
  CASE
    WHEN path = root THEN '.'
    ELSE substr(path, length(root) + 2)
  END AS relative_path,
  CASE
    WHEN path = root THEN 0
    ELSE length(substr(path, length(root) + 2)) - length(replace(substr(path, length(root) + 2), '\', '')) + 1
  END AS depth,
  path,
  directory,
  filename,
  type,
  size,
  datetime(btime, 'unixepoch', 'UTC') AS created_utc,
  datetime(mtime, 'unixepoch', 'UTC') AS modified_utc
FROM cisco_dirs
ORDER BY root, depth, path;
