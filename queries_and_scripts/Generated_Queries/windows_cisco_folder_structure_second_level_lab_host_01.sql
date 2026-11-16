WITH roots(root) AS (
  VALUES
    ('C:\Program Files\Cisco\AMP'),
    ('C:\Program Files\Cisco\Cisco Secure Client'),
    ('C:\Program Files\Cisco\Forensics'),
    ('C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client'),
    ('C:\Program Files (x86)\Cisco\Cisco Secure Client'),
    ('C:\ProgramData\Cisco\AMP'),
    ('C:\ProgramData\Cisco\Cisco AnyConnect Secure Mobility Client'),
    ('C:\ProgramData\Cisco\Cisco Secure Client')
),
cisco_dirs AS (
  SELECT
    r.root,
    f.path,
    f.directory,
    f.filename,
    f.type,
    f.size,
    f.btime,
    f.mtime
  FROM roots r
  JOIN file f
    ON f.path = r.root
    OR f.path LIKE r.root || '\%'
  WHERE f.type = 'directory'
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
