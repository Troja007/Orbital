# Orbital Script Page Linked Context

Source page: https://orbital.amp.cisco.com/help/Content/Topics/Script.htm

Retrieved: 2026-06-02

Import type: Structured summary of all Cisco Orbital help-topic links visible from the Script page. This file is not a verbatim copy of the linked pages.

## Imported Link Set

- Orbital Overview: https://orbital.amp.cisco.com/help/Content/Topics/Orbital-Overview.htm
- Orbital Release Notes: https://orbital.amp.cisco.com/help/Content/Topics/New-Releases.htm
- MITRE ATT&CK: https://orbital.amp.cisco.com/help/Content/Topics/Mitre-Att&ck.htm
- What Are Orbital Nodes?: https://orbital.amp.cisco.com/help/Content/Topics/Orbital-Nodes.htm
- Get Orbital: https://orbital.amp.cisco.com/help/Content/Topics/Get-Orbital.htm
- Orbital Setup: https://orbital.amp.cisco.com/help/Content/Topics/Orbital-Setup.htm
- Investigate: https://orbital.amp.cisco.com/help/Content/Topics/Investigation.htm
- Builder: https://orbital.amp.cisco.com/help/Content/Topics/Orbital-Builder.htm
- Script: https://orbital.amp.cisco.com/help/Content/Topics/Script.htm
- Using Scripts: https://orbital.amp.cisco.com/help/Content/Topics/Use-Scripts.htm
- Custom Scripts: https://orbital.amp.cisco.com/help/Content/Topics/Custom-Scripts.htm
- Scheduled Scripts: https://orbital.amp.cisco.com/help/Content/Topics/Scheduled-Scripts.htm
- Linked Scripts: https://orbital.amp.cisco.com/help/Content/Topics/Linked-Scripts.htm
- Connect Scripts to Linked Queries: https://orbital.amp.cisco.com/help/Content/Topics/Connect-Scripts-Linked-Queries.htm
- Python: https://orbital.amp.cisco.com/help/Content/Topics/Python.htm
- Script Exit Codes: https://orbital.amp.cisco.com/help/Content/Topics/Script-Exit-Codes.htm
- Queries: https://orbital.amp.cisco.com/help/Content/Topics/Queries.htm
- Orbital Results: https://orbital.amp.cisco.com/help/Content/Topics/Orbital-Results.htm
- Orbital Devices: https://orbital.amp.cisco.com/help/Content/Topics/Orbital-Devices.htm
- Catalog: https://orbital.amp.cisco.com/help/Content/Topics/Orbital-Catalog.htm
- Administration: https://orbital.amp.cisco.com/help/Content/Topics/Administration.htm
- Orbital Troubleshooting: https://orbital.amp.cisco.com/help/Content/Topics/Orbital-Troubleshooting.htm
- Frequently Asked Questions: https://orbital.amp.cisco.com/help/Content/Topics/Frequently-Asked-Questions.htm
- IPv6 Statement: https://orbital.amp.cisco.com/help/Content/Topics/IPv6-Statement.htm
- Organizations: https://orbital.amp.cisco.com/help/Content/Topics/Organizations-Page.htm

## Script Workflow Context

The Script page positions Orbital Script as a response capability paired with Orbital Query. Queries identify endpoint conditions or threats; scripts can then gather additional information or take response actions on endpoints.

Scripts are Python-based. They can be selected from the Catalog or entered as custom Python in the Builder. Script output is collected as Orbital results.

Script work in this project should distinguish:

- Ad hoc scripts: run immediately against selected endpoints.
- Scheduled scripts: run automatically based on configured duration and frequency.
- Linked scripts: run against devices selected by one or more existing query results.

## Using Scripts

Scripts are created and executed from the Investigate page.

Script targets can be one or more endpoint identifiers. Orbital also supports adding a random set of devices for testing, but destructive or state-changing scripts should not be run against random devices.

Catalog scripts can include metadata such as description, ID, operating system, type, categories, MITRE ATT&CK mapping, warnings, parameters, and script content.

Some catalog scripts require parameters. After a catalog script is added to the Builder, Orbital displays parameter fields for required values.

Custom scripts can be saved to the Catalog with a name, description, and supported operating systems.

## Custom Scripts

Custom scripts are similar in concept to custom queries. They are useful for iterative investigation and response.

A custom script can be edited and run again, with refreshed results shown after execution.

Project rule: when adapting a catalog script or personal script, copy it to `queries_and_scripts/draft_scripts/` before changing it unless the user explicitly asks to update the GitHub-tracked source file.

## Scheduled Scripts

Scheduled scripts use duration and frequency. Duration defines how long the script remains active. Frequency defines how often it runs during that active window.

Scheduled scripts can run across many devices, including environments where some devices may be offline.

Project rule: document whether a script is intended for scheduled use, because scheduled execution changes endpoint impact, result volume, and busy-node behavior.

## Linked Scripts

Linked scripts are connected to existing queries. The linked script uses the device list returned by the linked query and only acts on devices that meet that query criteria.

Scripts can be linked to existing queries, but not to other scripts.

Linked scripts are a results-based device selector. They use the query's matching devices, not the actual returned query data.

Project rule: for linked scripts, document the upstream query dependency and expected non-empty result condition.

## Connecting Scripts To Linked Queries

Linked query/script selection can be started from the Investigate page or from the Results page.

From Investigate, the link query selector shows recent queries. From Results, a query can be selected through the result action menu.

Once a query is linked, the target device field is populated from the linked query. The user can then use a custom script or catalog script against that derived device set.

## Python Runtime Context

Orbital installs Python with the Orbital node when the Script feature is enabled. This Python environment is independent from other Python installations on the device.

Orbital uses Python 3.10 or later.

Included libraries listed by the help page:

- certifi
- chardet
- idna
- iptools
- requests
- scapy
- urllib3
- psutil
- volatility3

Script limits listed by the help page:

- Maximum script size: 64 KB.
- Execution timeout: 10 minutes.
- stdout cap: 16 MB.
- stderr cap: 16 MB.
- Child processes spawned by a script are not terminated by Orbital and must exit on their own.

Project rule: avoid relying on local machine Python behavior. Treat Orbital Python as its own endpoint runtime with explicit limits.

## Script Parameters

Orbital supports typed script parameters. Parameter types described by the help page include:

- Basic string
- Raw string
- Integer
- Float
- Email
- URL
- IPv4
- IPv6

Orbital can detect parameters from custom script syntax and populate parameter fields in the UI.

Project rule: define parameters explicitly and prefer assigning Orbital parameters to Python variables before using them in code. Ensure string parameters are quoted correctly when embedded into Python.

## Script Exit Codes

Scripts should return exit codes using Python's `sys.exit()`.

Exit code handling:

- `0`: successful execution.
- `1` to `199`: available for customer scripts.
- `200` and higher: reserved for Orbital internal use.

Special Orbital exit codes described by the help page:

- `200`: script timed out.
- `201`: Orbital error.
- `202`: Python execution error.
- `203`: script exception occurred.
- `204`: script failed to run.
- `205`: Script feature not enabled.
- `206`: Python missing from node.
- `207`: node feature update in progress or operating system mismatch.
- `208`: operating system mismatch.
- `209`: invalid exit code.

Project rule: use stderr for warnings or non-fatal error details when the script can still complete successfully.

## Builder And Investigate Context

The Investigate page is where queries and scripts are created and executed through Orbital Builder.

Builder supports:

- Query mode and Script mode.
- Device targeting by hostname, IP address, MAC address, node ID, and connector GUID.
- Optional operating system filters.
- Linking to existing query results.
- Random device selection for limited testing.
- Catalog selection.
- Custom SQL or Python entry.
- Immediate run.
- Scheduled run.
- Remote data store output where supported.

Project rule: test new read-only queries on limited targets before wider use. Do not run state-changing scripts against random devices.

## Results Context

Orbital Results provides an overview of completed or in-progress query and script results.

Important result-handling points:

- Result content retention is 90 days.
- Important data should be exported or sent to a remote data store before expiry.
- Results can be downloaded, including JSON for result tables and CSV/JSON formats depending on result type.
- Script result downloads are limited by record count.
- Results include status, progress, timing, filters, catalog association, and links to detailed result views.

Project rule: when creating scripts or queries intended for longer-term evidence, define how results will be retained or exported.

## Devices And Nodes Context

Orbital devices are endpoints with an Orbital node installed.

Device targeting and review can use fields such as hostname, IP address, MAC address, operating system, node ID, Secure Endpoint connector GUID, and Secure Client UID.

Orbital nodes are endpoint services used to collect system information for threat investigation.

Node version status matters. Unsupported nodes may still connect and run queries/scripts, but should be updated. Rejected nodes cannot connect.

Project rule: query/script behavior may depend on node version, endpoint platform, and whether the node is online.

## MITRE ATT&CK Context

Predefined catalog queries and scripts have MITRE ATT&CK tactics and techniques assigned.

The product UI uses an ATT&CK indicator for stock query/script mapping.

Project rule: when adapting catalog content, preserve MITRE-related context when present. For custom work, document intended ATT&CK relevance if known.

## Setup And Administration Context

Orbital access depends on Cisco Security products such as Cisco Secure Endpoint or Cisco XDR.

Secure Endpoint deployment requires supported connector versions and administrative permissions.

Orbital service endpoints are region-specific for North America, European Union, and Asia Pacific/Japan/Greater China.

The Administration area manages users, organizations, remote data stores, and Script enablement.

Script enablement is controlled from organization settings and requires administrator permissions. After enabling Script, nodes may need time and internet connectivity to update their configuration.

Project rule: if a script-related behavior fails, verify organization Script enablement and node readiness before assuming a code issue.

## Troubleshooting And Operational Constraints

Orbital does not support SSL proxies.

Orbital node logs are written to native operating system logging:

- Windows: Windows Application Event Log with source `CiscoOrbital`.
- macOS: Unified Log with subsystem `com.cisco.endpoint.orbital`.
- Linux: Journald unit `cisco-orbital`.

osquery logs are included as an osqueryd subcomponent of Orbital logs.

Some osquery tables require constraints in the `WHERE` clause. Missing required constraints can cause query failures.

Project rule: for query failures, check table constraints before changing query logic broadly.

## FAQ And Retention Context

Device visibility and result content are retained for 90 days.

Query metadata is retained longer than result content and includes SQL statement, creator, and creation timestamp.

Longer-term retention requires download, API collection within the retention window, or remote data store delivery.

Script readiness can be confirmed through operating system logs after Script is enabled.

## IPv6 Context

Orbital does not support receiving data from pure IPv6 devices.

Specific devices can be targeted for queries and scripts using IPv6 addresses. Advanced IPv6 operations such as wildcards and subnets are not supported.

Project rule: avoid assuming IPv6 wildcard or subnet targeting support.

## Latest Release Notes Observed

The latest release note observed during import was Orbital Service Release 1.74 dated 2026-05-26.

Relevant observed change: the Run button in the query/script Builder can store results to a selected Remote Data Store. Previously this capability was available only for scheduled queries and/or scripts.

Also observed: result data retention was increased to 90 days in Orbital Service Release 1.69 dated 2026-03-24.
