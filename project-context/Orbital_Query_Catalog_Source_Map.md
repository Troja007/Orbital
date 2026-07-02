# Orbital Query Catalog Source Map

Retrieved/updated: 2026-06-02

Purpose: Link the main information sources used to understand Orbital queries: upstream osquery schema, Orbital Catalog API, authenticated Orbital Catalog UI, and sanitized catalog result profiles.

## Relationship Summary

Orbital queries are based on osquery. osquery provides the SQL table model: table names, column names, column types, and descriptions.

Orbital adds product-specific behavior around that base model. This includes Cisco-managed catalog queries, custom organization queries, product UI metadata, catalog IDs, API access, and possible Orbital-specific capabilities or restrictions.

The Orbital UI shows Cisco-managed catalog queries with additional product information that is not part of the upstream osquery schema.

Sanitized catalog result profiles show how catalog query results should be read after execution. They add expected result shape, row-count behavior, returned columns, validation caveats, and incident-responder interpretation guidance without storing endpoint evidence.

## Source Roles

### osquery Schema

Source context file:

```text
project-context/Osquery_Schema_5_23_0.md
```

Structured source files:

```text
01_Source_Files/API_References/osquery_schema_5_23_0.json
01_Source_Files/API_References/osquery_schema_5_23_0_table_index.json
```

Use for:

- Table names
- Column names
- Column types
- Table descriptions
- Evented table indication
- Upstream osquery SQL reference

Do not use alone for:

- Confirming Orbital availability of a table
- Cisco-managed catalog metadata
- Orbital Catalog IDs
- Query categories
- MITRE mappings
- UI labels or routes

### Orbital Catalog API

Source context file:

```text
project-context/Orbital_API_DevNet.md
```

Primary API reference:

```text
https://developer.cisco.com/docs/orbital/introduction/#orbital-api
```

Relevant catalog API concept:

```text
/v0/stock
```

Note: use `/v0`, not `/vo`. The API version path uses the digit zero.

Use for:

- Programmatic access to stock catalog entries
- Programmatic access to organization catalog entries
- Automation around catalog queries and scripts
- API request and response schemas
- Mapping API data to local catalog exports

Do not use alone for:

- Understanding how terms appear to a user in the product UI
- Confirming current UI labels, filters, or drawer layout

### Orbital Catalog UI

Source context file:

```text
project-context/Orbital_Catalog_UI_Terms.md
```

Authenticated UI example:

```text
https://orbital.amp.cisco.com/stock?search=sha256
```

Use for:

- User-facing table labels
- Filters
- Detail drawer fields
- Product terminology
- UI route behavior
- Understanding how `ID`, `Name`, `Type`, `OS`, `Category`, and `MITRE | ATT&CK` appear in the product

Do not use alone for:

- Complete API schema
- Full catalog export
- Upstream osquery table/column validation

### Catalog Result Profiles

Source folder:

```text
queries_and_scripts/catalog_result_profiles/
```

Use for:

- Explaining what a catalog query result means after execution
- Understanding observed row-count behavior from a controlled validation run
- Seeing returned labels and column shapes for completed catalog entries
- Separating no-hit results, inventory/posture output, event-log caveats, high-volume output, and query/endpoint caveats
- Giving incident responders safe assumptions and limits per Catalog `ID`

Do not use alone for:

- Proving fleet-wide endpoint state
- Replacing live result review
- Replacing catalog API/UI metadata
- Storing or reconstructing endpoint evidence

## Field Mapping

| Concept | osquery schema | Orbital Catalog API | Orbital Catalog UI | Catalog result profiles |
|---|---|---|---|---|
| Table name | Yes | Present indirectly inside query SQL/content | Present inside query content | No |
| Column name | Yes | Present indirectly inside query SQL/content | Present inside query content | Returned column shape when observed |
| Query SQL | No | Yes, for catalog query payloads | Yes, in query content drawer | No |
| Catalog item ID | No | Yes, operation/schema dependent | Yes, shown as `ID` | Yes, primary lookup key |
| Human-readable name | No | Yes, operation/schema dependent | Yes, shown as `Name` | Yes |
| Type: Query/Script | No | Yes | Yes, shown as `Type` | Query profiles only |
| OS/platform metadata | Table dependent | Yes, operation/schema dependent | Yes, shown as `OS` | Yes, copied from catalog metadata |
| Category | No | Yes, operation/schema dependent | Yes, shown as `Category` | Yes, copied from catalog metadata |
| MITRE mapping | No | Yes, operation/schema dependent | Yes, shown as `MITRE | ATT&CK` | Yes, copied from catalog metadata |
| Created/updated metadata | No | Yes, operation/schema dependent | Yes, shown in table/detail drawer | Catalog update date when present |
| Result row counts | No | Execution dependent | Execution dependent | Sanitized validation row-count behavior |
| Result interpretation | No | No | Limited | Yes |

## Practical Workflow For Query Review

1. Start with the Orbital Catalog UI or API entry to identify the catalog item.
2. Record both `Name` and `ID`.
3. Extract or inspect the query SQL.
4. Validate referenced tables and columns against `osquery_schema_5_23_0.json`.
5. Check whether Orbital-specific availability, disabled tables, `allowos`, or platform filters apply.
6. Preserve Catalog metadata such as OS, category, MITRE mapping, owner/updater, and update date.
7. If explaining an executed catalog result, check `queries_and_scripts/catalog_result_profiles/` by Catalog `ID`.
8. If adapting the query, copy it into `02_Working_Files/Queries` before editing.

## Example From UI Analysis

Catalog search:

```text
https://orbital.amp.cisco.com/stock?search=sha256
```

Observed Cisco-managed query:

```text
Name: SHA256 Hash Of Running Processes
ID: process_hashes
Type: Query
Category: Live Acquisition Of Volatile Data
Updated by: Cisco
Updated: 2023-11-14 18:51:59
```

Observed query content:

```sql
SELECT
  p.pid, p.name, p.path, p.cmdline, p.state, h.sha256
FROM processes p
INNER JOIN hash h
ON p.path=h.path;
```

osquery schema use:

- Validate `processes` table.
- Validate `hash` table.
- Validate referenced columns: `pid`, `name`, `path`, `cmdline`, `state`, and `sha256`.

Orbital UI/API use:

- Preserve `process_hashes` as the Catalog `ID`.
- Preserve Cisco-managed catalog metadata.
- Treat the UI detail drawer as product-facing metadata, not as upstream osquery schema.

## Project Rule

For Orbital query work, do not treat one source as complete by itself.

- Use osquery schema for SQL table/column structure.
- Use the Orbital Catalog API for programmatic catalog access.
- Use Orbital UI analysis for product terminology and Cisco-managed query metadata.
- Use sanitized catalog result profiles for result-shape and incident-responder interpretation guidance.
