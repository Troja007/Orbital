select * from sqlite_temp_master
WHERE type = "table"
AND name not like "sqlite_%";
