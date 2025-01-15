select f.path, f.filename, f.product_version, f.size, h.sha256, datetime(f.mtime,"unixepoch","UTC")
as last_modification_time
FROM file f JOIN hash h ON f.path=h.path
WHERE (f.path LIKE "\%%\system32\Drivers\%"
OR f.path LIKE "\%%\Cisco\AMP\7%\%"
OR f.path LIKE "\%%\Cisco\AMP\8%\%"
OR f.path LIKE "\%%\Cisco\AMP\endpointisolation\%")
AND f.filename IN
(
"immunetselfprotect.sys",
"immunetprotect.sys",
"immunetutildrivers.sys",
"ImmunetNetworkMonitor.sys",
"bddci.sys",
"trufos.sys",
"ancrcl64.sys",
"CiscoAMPHeurDriver.sys",
"CiscoAMPELAMDriver.sys",
"CiscoAMPCEFWDriver.sys",
"CiscoSAMApi.dll",
"CiscoSAM.sys"
)
ORDER BY f.filename;
