-- Legacy Internet Explorer extensions retained for endpoint extension correlation.
SELECT
  name,
  registry_path,
  version,
  path
FROM ie_extensions
ORDER BY name, registry_path, version;
