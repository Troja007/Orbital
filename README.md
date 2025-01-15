# Orbital
SQL queries for Orbital

This is a summary of SQL queries, which can be used with Orbital. It includes customized SQL queries to tweak result output.
Learn more about SQL under: https://www.w3schools.com/sql/

Transform result data
- datetime(table_column_name, "unixepoch", "UTC")
- round((table_column_name / 1024 / 1024) ,0) AS "diplayed_column_name”
- select substr (table_column_name,42,10)
- case table_column_name when 'bs.json' then 'CM config exists’when 'cm_config.json' then 'CM config exists’
- order by "Cloud Management Config" ASC
- where hostnames not in ("localhost", "::1", "fe00::0", "ff00::0", "ff02::1", "ff02::2")
- JSON_EXTRACT(json(data), '$.EventData.LocalPort') AS "source-port",
- SPLIT(message, ',', 1) AS protocol,
