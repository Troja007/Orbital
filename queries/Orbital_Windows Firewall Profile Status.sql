WITH registry_data AS (
    SELECT
      SPLIT(key, '\', 7) AS profile,
      name, data, 'FW_Setting' AS idx
    FROM registry r
    where r.path IN
(
'\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile\EnableFirewall',
'\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile\EnableFirewall',
'\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile\EnableFirewall'
)
    ),
firewall_profiles AS (
      SELECT
        MAX(CASE WHEN profile = 'DomainProfile'
                 THEN data END) AS domain_profile,
        MAX(CASE WHEN profile = 'StandardProfile'
                 THEN data END) AS standard_profile,
        MAX(CASE WHEN profile = 'PublicProfile'
                 THEN data END) AS public_profile
      FROM registry_data
      GROUP BY idx
)
SELECT
  (CASE domain_profile
         when '1' then 'OK'
         when '0' then 'disabled'
         ELSE 'ERROR'
  END) AS FW_Domain_Profile,
  (CASE standard_profile
         when '1' then 'OK'
         when '0' then 'disabled'
         ELSE 'ERROR'
  END) AS FW_Standard_Profile,
  (CASE public_profile
         when '1' then 'OK'
         when '0' then 'disabled'
         ELSE 'ERROR'
  END) AS FW_Public_Profile
FROM firewall_profiles;
