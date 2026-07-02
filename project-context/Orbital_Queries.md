# Orbital Queries

Source URL: https://orbital.amp.cisco.com/help/Content/Topics/Queries.htm

Source title: Queries

Retrieved: 2026-06-02

Last verified from current in-app browser page: 2026-06-02

Import type: Structured summary from Cisco Orbital help page and browser page evidence. This file is not a verbatim copy of the page.

## Summary

Orbital uses queries to search devices in an organization for malicious activity and endpoint state. Queries are written with SQL-style syntax through osquery.

osquery represents operating system and device data as relational database tables. Orbital uses both osquery stock tables and Orbital-specific tables.

Some stock osquery tables are disabled by Orbital for security and performance reasons. Platform-specific configuration must be checked for Linux, macOS, and Windows before assuming a stock table is available.

## Builder And Results

Queries are built and executed with Orbital Builder on the Investigate page.

Query results can be reviewed in Orbital Results. Results can also be sent to other applications, including Cisco Secure Endpoint, Secure Malware Analytics, and Cisco Threat Response.

Results can be stored in remote data stores such as Amazon S3, Microsoft Azure, and Splunk.

## Types Of Queries

Orbital provides two query types:

- Custom queries
- Scheduled queries

## Custom Queries

Custom queries are also called live queries or probes.

Use custom queries for quick testing and iteration. They run immediately and return results immediately.

Custom queries return one set of results for devices that match the query criteria. If a targeted device is offline, that device is not queried and returns no results.

## Scheduled Queries

Scheduled queries run at a defined time for a defined duration.

Example behavior: a query with a 24-hour execution window and a 15-minute frequency actively collects results for 24 hours after execution starts and attempts to contact each relevant device every 15 minutes.

Scheduled queries are useful for building a picture of node history across the query window.

## Query Prefixes

Orbital query prefixes define which devices the query runs against. Prefixes can identify specific devices or match device criteria.

Prefix categories:

- Special
- Dynamic
- Static

## Special Prefixes

The special prefix category currently contains the `all` prefix.

The `all` prefix runs a query against all devices in the organization. It cannot be used together with other prefixes or with the `allowos` filter.

The `all` prefix can be combined with the Operating System Filter to restrict execution to a platform group.

Use `all` with caution for CPU-intensive queries or queries expected to produce many results, because it can affect device performance.

## Dynamic Prefixes

Dynamic prefixes run queries against all devices that match specified criteria.

If matching devices are offline when the query starts, they can be included after reconnecting and continue to be included until the query expires.

Wildcard-based prefixes using `%` are treated as dynamic prefixes.

## Static Prefixes

Static prefixes directly specify one or more known devices.

Static prefixes can specify devices directly or use `%` to specify a device group. Prefixes using `%` are treated as dynamic prefixes.

If a static prefix points to an unknown or disconnected device when the query begins, that device is dropped from the query. If it reconnects later during execution, it is not queried.

## allowos Filter

The `allowos` filter specifies which operating system must be running before a query executes against a device.

The filter is relevant for catalog queries that are platform-specific. For example, a Windows registry query should not be run against macOS or Linux devices.

Use `allowos` to ensure that results only come from devices running the intended operating system.

## Query Success Conditions

A query can succeed if at least one required selector resolves. Examples include:

- The query contains the `all` special prefix.
- The query contains a dynamic prefix.
- The query contains at least one resolvable static prefix.
- At least one static or dynamic selector resolves when other static prefixes fail.

For linked queries using `queryid`, each prefix value must refer to a known query at request time or the request fails.

## Project Handling Rules

For query review or creation in this project:

- Verify table availability in Orbital, not only in upstream osquery.
- Check whether the query is platform-specific.
- Check whether `allowos` or an operating system filter is needed.
- Avoid broad `all` targeting for expensive queries unless explicitly justified.
- Treat custom/live query behavior differently from scheduled query behavior.
- Document assumptions about online/offline endpoint behavior.
- Prefer existing catalog examples before creating new query logic from scratch.

## Related References Found On Page

- Orbital Builder
- Using Queries
- Custom Queries
- Scheduled Queries
- Linked Queries
- osquery
- Windows Management Infrastructure Access Through Orbital
- Orbital Results
- Orbital Devices
- Catalog
- Query API Prefix Table on Cisco DevNet
- SQL Tutorial
- SQL Quick Reference
