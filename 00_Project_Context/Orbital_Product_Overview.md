# Orbital Product Overview

Source URL: https://orbital.amp.cisco.com/help/Content/Topics/Orbital-Overview.htm

Source title: Orbital Overview

Retrieved: 2026-06-02

Import type: Structured summary from Cisco Orbital help page. This file is not a verbatim copy of the page.

## Product Summary

Cisco Orbital is a cloud-based endpoint investigation and response tool. It is used to collect system and security information from networked devices and to respond to identified threats.

Orbital integrates with Cisco XDR and Cisco Secure Endpoint. Parts of Orbital functionality are available from within those product consoles.

## Core Workflows

Orbital supports two main technical workflows:

- Queries: SQL-based endpoint inspection using osquery.
- Scripts: Python-based response actions executed on endpoints.

Queries and scripts are created and run from the Investigate area. Results from query and script runs are reviewed on the Results page.

## Queries

Orbital queries use SQL syntax through osquery. osquery exposes operating system and endpoint information as database-like tables.

For query work in this project, validate:

- osquery table names
- column names
- supported operating systems
- expected result structure
- assumptions about endpoint state
- query type: custom/live/probe or scheduled
- query targeting prefixes
- whether `allowos` or an operating system filter is needed

## Scripts

Orbital scripts use Python for endpoint response actions.

For script work in this project, validate:

- endpoint safety
- platform assumptions
- error handling
- expected output
- whether the action is idempotent
- impact on the endpoint
- ad hoc, scheduled, or linked-query execution mode
- behavior when the target node is busy
- behavior if scripting is disabled

## Catalog

The Orbital Catalog provides researched and tested queries and scripts. The Catalog includes stock queries and scripts created by the Orbital team and Cisco Talos, plus custom user-created queries and scripts. Custom SQL queries and Python scripts can also be saved in the Catalog.

Project rule: use catalog content as reference material before creating new query or script work from scratch.

## Important Product Notes

Orbital supports proxies, but not SSL-terminating proxies. Proxy use is supported across operating systems.

Apple Silicon is supported for macOS 11 or newer.

The Orbital API documentation is available on Cisco DevNet:

https://developer.cisco.com/docs/orbital

The product help notes that screenshots may not always match the latest product names or UI changes.

Orbital pages support keyboard accessibility.

## Related Help Topics Found On Page

- Orbital Release Notes
- MITRE ATT&CK
- What Are Orbital Nodes?
- Get Orbital
- Orbital Setup
- Investigate
- Orbital Results
- Orbital Devices
- Catalog
- Administration
- Remote Data Stores
- My Account
- Users Page
- Organizations
- Orbital Troubleshooting
- Windows Troubleshooting
- macOS Troubleshooting
- Alerts, Errors, and Warnings
- Frequently Asked Questions
- IPv6 Statement
- osquery

## Project Usage

Use this overview as product context when reviewing, adapting, or creating Orbital queries and scripts.

Do not treat this file as complete API documentation. For API details, catalog schema, authentication, endpoint URLs, or available templates, use Cisco DevNet documentation or company-provided API source files.
