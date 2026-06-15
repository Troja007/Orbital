SELECT
  si.hostname AS host,
  CASE
    WHEN lower(pr.name) LIKE '%anyconnect vpn%' THEN 'AnyConnect VPN'
    WHEN lower(pr.name) LIKE '%cloud management%' THEN 'Cloud Management'
    WHEN lower(pr.name) LIKE '%diagnostics and reporting tool%' THEN 'Diagnostics and Reporting Tool'
    WHEN lower(pr.name) LIKE '%endpoint visibility module%' THEN 'Endpoint Visibility Module'
    WHEN lower(pr.name) LIKE '%xdr network visibility module%' THEN 'XDR Network Visibility Module'
    WHEN lower(pr.name) LIKE '%network visibility module%' THEN 'Network Visibility Module'
    WHEN lower(pr.name) LIKE '%secureclientui%' THEN 'Secure Client UI'
    ELSE pr.name
  END AS module,
  pr.name AS installed_product,
  pr.version,
  pr.publisher,
  pr.install_location,
  pr.install_source,
  pr.install_date,
  pr.uninstall_string
FROM programs pr
CROSS JOIN system_info si
WHERE lower(pr.name) LIKE 'cisco secure client%'
   OR lower(pr.name) LIKE '%secureclientui%'
ORDER BY module, installed_product;
