SELECT username,
  groupname,
  type,
  u.UID,
  g.GID,
  Description,
  comment

FROM users u

JOIN user_groups ug ON ug.UID = u.UID
JOIN groups g ON g.GID = ug.GID

-- WHERE g.GID = "544" -- WHERE username like "%carl%" AND u.type = "local";
