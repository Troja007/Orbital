SELECT
  si.hostname AS host,
  'EDR / Cisco Secure Endpoint' AS module,
  CASE
    WHEN EXISTS (
      SELECT 1 FROM programs pr
      WHERE lower(pr.name) LIKE '%cisco secure endpoint%'
         OR lower(pr.name) LIKE '%cisco amp%'
    ) THEN 'installed'
    ELSE 'missing'
  END AS installed_status,
  CASE
    WHEN EXISTS (
      SELECT 1 FROM services s
      WHERE s.name IN ('CiscoAMP', 'CiscoSCMS')
        AND s.status = 'RUNNING'
    )
    OR EXISTS (
      SELECT 1 FROM processes p
      WHERE lower(p.name) IN ('sfc.exe', 'cscm.exe')
    ) THEN 'active'
    ELSE 'not_active'
  END AS active_status,
  COALESCE((
    SELECT group_concat(pr.name || ' ' || pr.version, '; ')
    FROM programs pr
    WHERE lower(pr.name) LIKE '%cisco secure endpoint%'
       OR lower(pr.name) LIKE '%cisco amp%'
  ), '') AS installed_evidence,
  COALESCE((
    SELECT group_concat(s.name || '=' || s.status || '/' || s.start_type, '; ')
    FROM services s
    WHERE s.name IN ('CiscoAMP', 'CiscoSCMS')
  ), '') AS service_evidence,
  COALESCE((
    SELECT group_concat(p.name || ' pid=' || CAST(p.pid AS TEXT), '; ')
    FROM processes p
    WHERE lower(p.name) IN ('sfc.exe', 'cscm.exe')
  ), '') AS process_evidence
FROM system_info si

UNION ALL

SELECT
  si.hostname AS host,
  'Orbital / Query & Script' AS module,
  CASE
    WHEN EXISTS (
      SELECT 1 FROM programs pr
      WHERE lower(pr.name) LIKE '%orbital%'
    )
    OR EXISTS (
      SELECT 1 FROM services s
      WHERE s.name = 'CiscoOrbital'
    ) THEN 'installed'
    ELSE 'missing'
  END AS installed_status,
  CASE
    WHEN EXISTS (
      SELECT 1 FROM services s
      WHERE s.name = 'CiscoOrbital'
        AND s.status = 'RUNNING'
    )
    OR EXISTS (
      SELECT 1 FROM processes p
      WHERE lower(p.name) IN ('orbital.exe', 'osqueryd.exe')
         OR lower(p.path) LIKE '%\orbital.exe'
         OR lower(p.path) LIKE '%\osqueryd.exe'
    ) THEN 'active'
    ELSE 'not_active'
  END AS active_status,
  COALESCE((
    SELECT group_concat(pr.name || ' ' || pr.version, '; ')
    FROM programs pr
    WHERE lower(pr.name) LIKE '%orbital%'
  ), '') AS installed_evidence,
  COALESCE((
    SELECT group_concat(s.name || '=' || s.status || '/' || s.start_type, '; ')
    FROM services s
    WHERE s.name = 'CiscoOrbital'
  ), '') AS service_evidence,
  COALESCE((
    SELECT group_concat(p.name || ' pid=' || CAST(p.pid AS TEXT), '; ')
    FROM processes p
    WHERE lower(p.name) IN ('orbital.exe', 'osqueryd.exe')
       OR lower(p.path) LIKE '%\orbital.exe'
       OR lower(p.path) LIKE '%\osqueryd.exe'
  ), '') AS process_evidence
FROM system_info si

UNION ALL

SELECT
  si.hostname AS host,
  'EVM / Endpoint Visibility' AS module,
  CASE
    WHEN EXISTS (
      SELECT 1 FROM programs pr
      WHERE lower(pr.name) LIKE '%endpoint visibility module%'
    ) THEN 'installed'
    ELSE 'missing'
  END AS installed_status,
  CASE
    WHEN EXISTS (
      SELECT 1 FROM services s
      WHERE s.name IN ('CiscoEVMService', 'CiscoEVMDriver')
        AND s.status = 'RUNNING'
    )
    OR EXISTS (
      SELECT 1 FROM processes p
      WHERE lower(p.name) = 'csc_evm.exe'
    ) THEN 'active'
    ELSE 'not_active'
  END AS active_status,
  COALESCE((
    SELECT group_concat(pr.name || ' ' || pr.version, '; ')
    FROM programs pr
    WHERE lower(pr.name) LIKE '%endpoint visibility module%'
  ), '') AS installed_evidence,
  COALESCE((
    SELECT group_concat(s.name || '=' || s.status || '/' || s.start_type, '; ')
    FROM services s
    WHERE s.name IN ('CiscoEVMService', 'CiscoEVMDriver', 'CiscoEVMElam')
  ), '') AS service_evidence,
  COALESCE((
    SELECT group_concat(p.name || ' pid=' || CAST(p.pid AS TEXT), '; ')
    FROM processes p
    WHERE lower(p.name) = 'csc_evm.exe'
  ), '') AS process_evidence
FROM system_info si

UNION ALL

SELECT
  si.hostname AS host,
  'NVM / Network Visibility' AS module,
  CASE
    WHEN EXISTS (
      SELECT 1 FROM programs pr
      WHERE lower(pr.name) LIKE '%network visibility module%'
    ) THEN 'installed'
    ELSE 'missing'
  END AS installed_status,
  CASE
    WHEN EXISTS (
      SELECT 1 FROM services s
      WHERE s.name IN ('csc_nvmagent', 'cscnvmpt')
        AND s.status = 'RUNNING'
    )
    OR EXISTS (
      SELECT 1 FROM processes p
      WHERE lower(p.name) = 'acnvmagent.exe'
    ) THEN 'active'
    ELSE 'not_active'
  END AS active_status,
  COALESCE((
    SELECT group_concat(pr.name || ' ' || pr.version, '; ')
    FROM programs pr
    WHERE lower(pr.name) LIKE '%network visibility module%'
  ), '') AS installed_evidence,
  COALESCE((
    SELECT group_concat(s.name || '=' || s.status || '/' || s.start_type, '; ')
    FROM services s
    WHERE s.name IN ('csc_nvmagent', 'cscnvmpt')
  ), '') AS service_evidence,
  COALESCE((
    SELECT group_concat(p.name || ' pid=' || CAST(p.pid AS TEXT), '; ')
    FROM processes p
    WHERE lower(p.name) = 'acnvmagent.exe'
  ), '') AS process_evidence
FROM system_info si

UNION ALL

SELECT
  si.hostname AS host,
  'Digital Forensics / XDR Forensics' AS module,
  CASE
    WHEN EXISTS (
      SELECT 1 FROM programs pr
      WHERE lower(pr.name) LIKE '%forensics responder%'
    )
    OR EXISTS (
      SELECT 1 FROM services s
      WHERE s.name = 'Cisco.Forensics.Responder.Service'
    ) THEN 'installed'
    ELSE 'missing'
  END AS installed_status,
  CASE
    WHEN EXISTS (
      SELECT 1 FROM services s
      WHERE s.name = 'Cisco.Forensics.Responder.Service'
        AND s.status = 'RUNNING'
    )
    OR EXISTS (
      SELECT 1 FROM processes p
      WHERE lower(p.name) = 'air.exe'
    ) THEN 'active'
    ELSE 'not_active'
  END AS active_status,
  COALESCE((
    SELECT group_concat(pr.name || ' ' || pr.version, '; ')
    FROM programs pr
    WHERE lower(pr.name) LIKE '%forensics responder%'
  ), '') AS installed_evidence,
  COALESCE((
    SELECT group_concat(s.name || '=' || s.status || '/' || s.start_type, '; ')
    FROM services s
    WHERE s.name = 'Cisco.Forensics.Responder.Service'
  ), '') AS service_evidence,
  COALESCE((
    SELECT group_concat(p.name || ' pid=' || CAST(p.pid AS TEXT), '; ')
    FROM processes p
    WHERE lower(p.name) = 'air.exe'
  ), '') AS process_evidence
FROM system_info si

ORDER BY module;
