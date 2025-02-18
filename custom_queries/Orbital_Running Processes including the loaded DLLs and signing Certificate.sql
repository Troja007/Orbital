select DISTINCT p.pid,
  p.name AS "Process Name",
  p.path AS "Process Path",
  pm.path AS "DLL-Loaded-path",
  sha256,
  a.issuer_name AS "DLL-Cert-Issuer_Name",
  a.subject_name as "DLL-Cert-Subject_Name",
  a.result
from processes p

LEFT JOIN process_memory_map pm ON p.pid=pm.pid
LEFT JOIN authenticode a ON pm.path = a.path
LEFT JOIN hash h on pm.path = h.path

-- WHERE p.path LIKE "%:\windows%"
Where pm.path != ""
AND pm.path NOT LIKE "%windows\system32%"
AND pm.path LIKE "%.dll"
-- This row can be used to filter for untrusted signing certificates
-- AND a.result NOT LIKE "trusted"
AND pm.path like "%cisco%"
AND pm.path like "%Protector%.dll"
-- checking Processes where exPrev injected code
-- AND pm.path like "%filezilla%" ORDER BY p.pid;
