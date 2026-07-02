# Orbital Scripts

Source URL: https://orbital.amp.cisco.com/help/Content/Topics/Script.htm

Source title: Script

Retrieved: 2026-06-02

Import type: Structured summary from Cisco Orbital help page and browser page evidence. This file is not a verbatim copy of the page.

## Summary

Orbital Script is a companion to Orbital Query. Queries search for malicious activity and potential endpoint misuse. Scripts can be used to respond to threats found through queries.

Script lets users create or select a Python script from the Catalog, send it to one or more devices, execute it, and collect results.

Scripts can return information that osquery does not report, extending the query capability.

## Typical Device Actions

Orbital scripts can support endpoint response actions such as:

- Starting and stopping services and processes
- Deleting files
- Shutting down or rebooting an endpoint
- Applying patches
- Performing deeper forensic investigations

## Execution Guidelines

Devices run only one script at a time. Multiple scripts cannot run on the same node simultaneously.

If an ad hoc script is sent to a busy node, the node returns a busy message and ignores the script.

If a scheduled script is sent to a busy node, the node queues it and runs it in turn.

If a user is deactivated while a scheduled script is running, the script continues until completion.

## Script Feature Disable Behavior

If the administrator disables scripting while a script is running, the running script completes, but no more scripts are allowed to run.

No new scripts can be run after the Script feature is disabled. This takes effect immediately.

If the organization does not have Script enabled, scripts are not shown in the Explore More area on the Investigate page; only queries are shown.

When the Orbital Script feature is disabled:

- The Script option is no longer available in Orbital Builder.
- Type filters are removed from the Catalog page.
- Stock and organizational scripts stored in the Orbital Catalog are removed from use.
- Currently executing scripts are allowed to complete.
- Scheduled scripts that have not yet run are canceled.
- Python libraries on Windows and Linux systems are disabled.

## Linking Scripts

Orbital can link a script to an existing query.

Linked scripts use the device list from the linked query and act only on devices that meet the query criteria.

The linking process follows the same concept as linked queries, but the link is from a script to an existing query.

## Project Handling Rules

For script review or creation in this project:

- Treat scripts as endpoint response automation, not generic local Python.
- Check whether the action is safe for the target endpoint population.
- Consider node busy behavior and scheduling behavior.
- Document whether a script is intended for ad hoc use, scheduled use, or linked-query use.
- Include clear output and error handling.
- Avoid destructive actions unless the purpose, target criteria, and rollback/impact considerations are explicit.
- Check platform assumptions, especially Windows and Linux Python library behavior.
- Prefer existing catalog examples before creating new script logic from scratch.

## Related References Found On Page

- Python
- Script Exit Codes
- Using Scripts
- Custom Scripts
- Scheduled Scripts
- Linked Scripts
- Connect Scripts to Linked Queries
- Investigation
- Organizations

See also: `Orbital_Script_Page_Linked_Context.md` for the consolidated import of all help-topic links visible from the Script page.
