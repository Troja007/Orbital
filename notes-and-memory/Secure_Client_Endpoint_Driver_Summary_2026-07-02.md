# Secure Endpoint / Secure Client Driver Summary

**Date:** 2026-07-02

## Source Basis

This summary is generated from stored project working files only, especially:

- `product-context/Cisco_Secure_Client_Endpoint_Context.md`
- `02_Working_Files/Generated_Queries/windows_secure_endpoint_secure_client_driver_set_marble.sql`
- `02_Working_Files/Generated_Queries/windows_secure_endpoint_user_and_kernel_driver_set_slate.sql`
- `02_Working_Files/Generated_Queries/windows_additional_cisco_endpoint_drivers_marble.sql`
- `02_Working_Files/Generated_Queries/windows_secure_endpoint_isolation_driver_marble.sql`
- `02_Working_Files/Generated_Queries/windows_endpoint_isolation_driver_disk_location_marble.sql`
- `02_Working_Files/Generated_Queries/windows_tdnr_secure_client_module_status.sql`

The summary stores product artifact knowledge only. It does not store endpoint
result rows, hostnames, node IDs, tenant identifiers, or raw API output.

## Interpretation Rules

- Treat this as observed driver and service artifact context, not a complete
  product-health verdict.
- Installed driver state can vary by connector version, enabled module, policy,
  reboot state, and feature use.
- A driver can appear in more than one evidence source, especially both
  `drivers` and `services`.
- Driver services commonly report PID `0`; that is expected for kernel drivers
  and should not be interpreted as a missing process.
- `STOPPED / BOOT_START` can be normal for ELAM or boot-start drivers depending
  on driver type and runtime state.
- Some driver services can appear `RUNNING` even when `start_type` reports
  `DISABLED`; use the observed state carefully and correlate across tables.
- For checks, combine `services`, `drivers`, and exact-path `file` lookups.
  Avoid broad filesystem searches.

## Consolidated Driver Table

| Driver/service | File | Typical path | Product/module hint | Stored notes |
|---|---|---|---|---|
| `bddci` | `bddci.sys` | `C:\Windows\System32\Drivers\bddci.sys` | Secure Endpoint connector stack; URLScannerEngine / Bitdefender BDDCI component | Observed version `3.0.7.18`; service can run as `KERNEL_DRIVER` with `AUTO_START`. |
| `Trufos` | `trufos.sys` | `C:\Windows\System32\Drivers\trufos.sys` | Secure Endpoint connector stack; Trufos / Bitdefender Antivirus component | Observed version `2.5.4.62`; service can run as `FILE_SYSTEM_DRIVER` with `DEMAND_START`. |
| `ImmunetSelfProtectDriver` | `immunetselfprotect.sys` | `C:\Windows\System32\Drivers\immunetselfprotect.sys` | Secure Endpoint self-protection | Observed version `7.3.2.575`; service can run as `FILE_SYSTEM_DRIVER` with `SYSTEM_START`. |
| `ImmunetProtectDriver` | `immunetprotect.sys` | `C:\Windows\System32\Drivers\immunetprotect.sys` | Secure Endpoint protection | Observed version `7.3.2.575`; service can run as `FILE_SYSTEM_DRIVER` with `SYSTEM_START`. |
| `ImmunetNetworkMonitorDriver` | `ImmunetNetworkMonitor.sys` | `C:\Windows\System32\Drivers\ImmunetNetworkMonitor.sys` | Secure Endpoint network monitoring | Observed version `2.0.1.510`; service can run as `KERNEL_DRIVER` with `AUTO_START`. |
| `CiscoAMPHeurDriver` | `CiscoAMPHeurDriver.sys` | `C:\Windows\System32\Drivers\CiscoAMPHeurDriver.sys` | Secure Endpoint heuristic driver | Observed version `1.0.0.514`; service can run as `FILE_SYSTEM_DRIVER` with `SYSTEM_START`. |
| `CiscoAMPELAMDriver` | `CiscoAMPELAMDriver.sys` | `C:\Windows\System32\Drivers\CiscoAMPELAMDriver.sys` | Secure Endpoint ELAM driver | Observed version `1.0.0.37`; `STOPPED / BOOT_START` can be normal for ELAM-style drivers. |
| `CiscoAMPCEFWDriver` | `CiscoAMPCEFWDriver.sys` | `C:\Windows\System32\Drivers\CiscoAMPCEFWDriver.sys` | Secure Endpoint Common Event Framework driver | Observed version `7.3.2.575`; service can run as `FILE_SYSTEM_DRIVER` with `SYSTEM_START`. |
| `ancrcl` | `ancrcl64.sys` | `C:\Program Files\Cisco\AMP\endpointisolation\ancrcl64.sys` | Secure Endpoint endpoint isolation / network driver framework socket layer interceptor | Observed version `1.3.2.0`; service can be `RUNNING` even when start type reports `DISABLED`. |
| `CiscoEVMDriver` | `evm_driver.sys` | `C:\Program Files\Cisco\Cisco Secure Client\EVM\bin\evm_driver.sys` | Secure Client Endpoint Visibility Module kernel driver | Service can run as `KERNEL_DRIVER` with `DEMAND_START`. |
| `CiscoEVMElam` | `evm_elam.sys` | `C:\Windows\System32\drivers\evm_elam.sys` | Secure Client Endpoint Visibility Module ELAM / PPL attestation driver | `STOPPED / BOOT_START` can be normal for ELAM-style drivers. |
| `acsock` | `acsock64.sys` | `C:\Windows\System32\DRIVERS\acsock64.sys` | Secure Client kernel driver framework socket layer interceptor | Service can run as `KERNEL_DRIVER` with `DEMAND_START`. |
| `cscnvmpt` | `cscnvmpt64.sys` | `C:\Program Files (x86)\Cisco\Cisco Secure Client\NVM\cscnvmpt64.sys` | Secure Client NVM packet/tap driver | Service can be `RUNNING` even when start type reports `DISABLED`. |
| `vpnva` | `vpnva64-6.sys` | `C:\Windows\System32\drivers\vpnva64-6.sys` | Cisco AnyConnect / Secure Client virtual miniport adapter | Observed version `5.1.11.80`; service can be `STOPPED` with `DEMAND_START` when VPN is not active. |
| `CiscoSAM` | `CiscoSAM.sys` | `C:\Windows\System32\Drivers\CiscoSAM.sys` | Cisco endpoint file-system driver candidate | Observed as `FILE_SYSTEM_DRIVER` with `SYSTEM_START`; exact module ownership still needs product-documentation validation. |
| `csadc` | `csadc.sys` | `C:\Windows\System32\DRIVERS\csadc.sys` | Cisco DeviceControl driver | Observed as `KERNEL_DRIVER` with `BOOT_START`; stopped boot-start state can be normal depending on feature use and reboot state. |

## Grouped View

### Secure Endpoint / AMP Protection Stack

These drivers are tied to Secure Endpoint / AMP protection, self-protection,
heuristics, common event framework, network monitoring, and bundled engine
components:

- `bddci`
- `Trufos`
- `ImmunetSelfProtectDriver`
- `ImmunetProtectDriver`
- `ImmunetNetworkMonitorDriver`
- `CiscoAMPHeurDriver`
- `CiscoAMPELAMDriver`
- `CiscoAMPCEFWDriver`

### Secure Endpoint Isolation

- `ancrcl` / `ancrcl64.sys`

The stored working files treat this as endpoint isolation / network driver
framework evidence. It is queried through `services`, `drivers`, and exact-path
`file` evidence because service path and disk location both matter.

### Secure Client Driver Stack

These drivers relate to Secure Client modules:

- `CiscoEVMDriver`: Endpoint Visibility Module kernel driver.
- `CiscoEVMElam`: Endpoint Visibility Module ELAM / PPL attestation driver.
- `acsock`: Secure Client kernel driver framework socket layer interceptor.
- `cscnvmpt`: Secure Client NVM packet/tap driver.
- `vpnva`: AnyConnect / Secure Client virtual miniport adapter.

### Additional Cisco Endpoint Driver Candidates

These were captured as additional candidates and need product-documentation
validation before being treated as definitive Secure Endpoint / Secure Client
core components:

- `CiscoSAM`
- `csadc`

## Recommended Query Pattern

For driver inventory, use a layered query pattern:

1. `drivers` table for loaded kernel driver evidence:
   - `service`
   - `device_name`
   - `image`
   - `provider`
   - `manufacturer`
   - `signed`
   - `version`
   - `class`
2. `services` table for service/driver registration and state:
   - `name`
   - `display_name`
   - `service_type`
   - `status`
   - `start_type`
   - `path`
   - `module_path`
   - `pid`
3. `file` table for exact disk path validation:
   - `path`
   - `filename`
   - `type`
   - `size`
   - `file_version`
   - `product_version`
   - `mtime`

Use exact file paths from the table above where possible. Constrain filesystem
lookups to known Cisco roots if exact paths are not known.

## Practical Reading Guidance

- A driver visible in `drivers` is loaded kernel evidence.
- A driver visible only in `services` may be installed/registered but not loaded
  at the moment of query.
- A file visible only in `file` proves disk presence, not runtime state.
- Version fields are useful context but should not be treated as policy or health
  verdicts by themselves.
- For Secure Client modules, pair driver evidence with `programs`, `services`,
  and process evidence so installed module state and runtime state are not
  confused.
