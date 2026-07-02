SELECT directory, SUM(CAST(ROUND((size * 10e-7),4) AS varchar)) AS SizeInMB
FROM file

/** works with single directory only **/

WHERE directory like "/opt/cisco/%%"
-- WHERE directory like "c:\Program Files\Cisco\%%"
-- WHERE directory like "c:\Program Files (x86)\Cisco\%%"
