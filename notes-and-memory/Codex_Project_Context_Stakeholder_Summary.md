# Codex Project Context - Stakeholder Summary

**Date:** 2026-06-24

## Executive Summary

This project is a Codex-supported workspace for Cisco Orbital query, script,
catalog, and API work. Codex is used to turn scattered Orbital, osquery, catalog,
Secure Endpoint, and Secure Client knowledge into reusable project context,
query methods, generated SQL, helper scripts, and operational guidance.

The stakeholder value is faster and more consistent investigation preparation:
Codex can help identify the right Orbital query pattern, validate table and
column assumptions, preserve catalog metadata, document lessons learned, and
separate reusable methods from sensitive endpoint results.

The project is evidence-oriented. It contains explicit guardrails requiring
table/column validation, source cross-referencing, careful target selection, and
strict avoidance of stored credentials or endpoint-specific results.

## Project Scope

The project scope is Cisco Orbital work around:

- osquery-based endpoint queries.
- Orbital scripts and response actions.
- Orbital Catalog API and authenticated UI context.
- Target selector terminology and Query API request behavior.
- Query-method memory for reusable investigation patterns.
- Secure Endpoint and Secure Client endpoint investigation context.
- Generated SQL and helper scripts for repeatable Orbital workflows.

Current technical focus areas include:

- Cisco Secure Endpoint and Cisco Secure Client inventory.
- Secure Endpoint Host Based Firewall event analysis.
- Secure Endpoint Exploit Prevention protected-process checks.
- Secure Client module detection, including NVM, EVM, and Cloud Management.
- Orbital health and endpoint OS/computer-name inventory.
- DNS, hosts file, socket, and Cisco/cloud connectivity evidence.
- Orbital catalog validation and multi-SQL catalog/API request structure.

## Current Knowledge Assets

The project has several distinct knowledge asset groups:

| Asset Group | Purpose | Representative Location |
|---|---|---|
| Project instructions | Defines terminology, source priority, handling rules, and safety boundaries | `AGENTS.md` |
| Project overview | Human/Codex orientation for repository layout and workflows | `README.md` |
| Durable context | Orbital product, query, script, catalog, API, target selector, and schema notes | `project-context/` |
| Source material | Read-only catalog/query/script source copies and user-owned custom work | `queries_and_scripts/` |
| Generated/adapted work | Drafts, generated SQL, product context, helper scripts, and active skills | `02_Working_Files/` |
| Query-method memory | Reusable methods describing when and how to query, without endpoint result rows | `02_Working_Files/Query_Methods/` |
| Product context | Secure Client / Secure Endpoint endpoint artifact and query context | `product-context/` |
| Notes and learning records | Decision logs, query memory summaries, and Codex network notes | `notes-and-memory/` |

Important source distinctions:

- `queries_and_scripts/catalog_queries` and
  `queries_and_scripts/catalog_scripts` are 1:1 Cisco-managed
  catalog source copies and should not be edited directly.
- `queries_and_scripts/custom_queries` and
  `queries_and_scripts/custom_scripts` are user-owned source
  material and should only be modified when intentionally updating that work.
- Adapted or generated query work belongs under `02_Working_Files` before it is
  promoted to a custom query/script repository file or reusable method.

## How Codex Is Used

Codex is used as a project-aware assistant for:

- **Project orientation:** reading `AGENTS.md`, the root README, project context
  files, and query-method records before acting.
- **Query design:** selecting tables, validating columns, choosing SQL patterns,
  and checking platform assumptions against the osquery 5.23.0 schema and Orbital
  catalog context.
- **Catalog-aware reuse:** preferring Cisco-managed catalog templates or existing
  custom query patterns before creating new SQL from scratch.
- **Query-method memory:** saving reusable investigation methods, decision logic,
  catalog references, and lessons learned without storing endpoint result rows.
- **Orbital API work:** using local helpers and skills for authentication checks,
  catalog import, catalog update work, scheduled host query execution, and Job ID
  follow-up.
- **Secure Client / Secure Endpoint analysis:** building structured context for
  product presence, installed modules, services, drivers, firewall events, cloud
  connectivity, and Exploit Prevention evidence.
- **Documentation and reporting:** creating project summaries, README updates,
  decision logs, query-memory reports, and stakeholder-facing summaries.
- **GitHub sync support:** checking local changes, preventing sensitive files
  from being committed, and syncing reusable project content when requested.

Codex does not replace Orbital validation. The project rules require table,
column, platform, target selector, source freshness, and catalog/API assumptions
to be checked before query work is treated as final.

## Indicative Activity Counters

These counters are scale indicators, not audited productivity metrics.

| Area | Indicator | Count / Level | Basis |
|---|---:|---:|---|
| Repository breadth | Files visible through `rg --files` | 161 | File inventory on 2026-06-24 |
| Durable context | Project context files | 14 | `project-context` file count |
| Query-method memory | Method/template records | 20 | `02_Working_Files/Query_Methods` file count excluding `.DS_Store` |
| Generated query artifacts | SQL/JSON files | 34 | `02_Working_Files/Generated_Queries` file count |
| User-owned source queries | Custom query source files | 26 | `queries_and_scripts/custom_queries` count |
| User-owned source scripts | Custom script source files | 12 | `queries_and_scripts/custom_scripts` count |
| Cisco-managed catalog source copies | Catalog query/script source files | 7 | `catalog_queries` plus `catalog_scripts` count |
| Project-local Orbital skills | Local `SKILL.md` files under `skills` | 4 | Skill file inventory |
| Supporting repository skill | GitHub sync workflow skill | 1 | `skills/github-sync-workflow/SKILL.md` |
| Sensitive-data handling | Explicit guardrail level | High | `AGENTS.md`, query-method README, root README, skill rules |

## Available Codex Skill Capabilities

### Project-Local Orbital Skills

These are local workspace skills with `SKILL.md` files under
`skills/`:

- `orbital-api-access`: Orbital API connectivity, authentication checks, catalog
  import, and catalog context inspection.
- `orbital-query-method-memory`: reusable method memory for choosing queries,
  preserving catalog context, and storing lessons without endpoint results.
- `orbital-run-osquery-live-query`: generic Orbital osquery execution against
  explicit targets, including host-targeted scheduled queries and Job ID tracking.
- `orbital-update-catalog`: create, preview, validate, and upload Orbital
  organization catalog query definitions without executing endpoint queries.

### Supporting Repository Skill

- `github-sync-workflow`: supports safe GitHub synchronization, previewing upload
  scope, excluding credentials/runtime state, and publishing project changes.

### Global Skill Used For This Report

- `codex-usage-report`: global skill used to generate this stakeholder summary.
  It is not project-local; it was explicitly requested for this task.

### Plugin Or General Capabilities Relevant When Requested

The active Codex environment includes broader capabilities such as GitHub,
documents, spreadsheets, presentations, data analytics, and browser tooling.
Those are not presented here as active project workflows unless the project files
or user task directly require them. In this project, the evidenced active
capabilities are Orbital-specific query/API/catalog work, project documentation,
and GitHub synchronization.

## Out Of Scope / Separate Project Boundaries

The following boundaries are explicit or implied by project instructions:

- The project should not store live endpoint result rows, hostnames, usernames,
  IP addresses, GUIDs, customer names, bearer tokens, raw API responses, or raw
  investigation output.
- The project does not treat upstream osquery schema as proof that a table is
  available in Orbital; Orbital availability must be verified.
- The project should not modify Cisco-managed catalog source copies directly.
- The project should not modify user-owned custom query/script source folders
  unless the user explicitly asks to update that GitHub-tracked work.
- Broad endpoint targeting, especially `all`, requires caution because it can
  affect endpoint performance.
- Secure Client / Secure Endpoint context is method and artifact knowledge, not
  a cloud-console health verdict or policy-state source of truth.
- Local folders such as `local/`, `.codex/`, `.tmp/`, `tmp/`, real credentials,
  runtime ledgers, and local SQLite state are excluded from reusable project
  content and GitHub sync.

## Operating Principles And Guardrails

Key operating rules from inspected project files:

- Read `AGENTS.md` and relevant project context before changing query, script,
  API, catalog, or skill behavior.
- Validate osquery table and column names against
  `product-context/osquery/osquery_schema_5_23_0.json`.
- Use `project-context/Orbital_Target_Node_Selectors.md` for target/device/
  endpoint/node terminology and API `nodes` selector behavior.
- Preserve distinctions between Catalog `ID`, Orbital endpoint ID, Secure
  Endpoint computer GUID, Secure Client computer GUID, AnyConnect UDID,
  `queryId:<id>`, and `orbital_queryID` / Job ID.
- Use three sources for catalog analysis: upstream osquery schema, Orbital
  Catalog API, and authenticated Orbital UI context.
- Prefer existing Orbital catalog templates and recorded query methods before
  creating new queries from scratch.
- For scripts, respect Orbital endpoint runtime constraints: Python 3.10 or
  later, 64 KB script size, 10 minute timeout, 16 MB stdout/stderr caps, and
  customer exit codes `0` through `199`.
- Keep reusable asset names generic unless the user explicitly requests a
  customer-, person-, or incident-specific name.
- Ask for clarification when project terms are ambiguous, especially terms such
  as target, device, endpoint, host, node, ID, GUID, and query ID.

## Validation Notes

### Inspected

This report is based on inspection of:

- `AGENTS.md`
- `README.md`
- `project-context/README.md`
- `project-context/Orbital_Query_Catalog_Source_Map.md`
- `02_Working_Files/Query_Methods/README.md`
- `product-context/Cisco_Secure_Client_Endpoint_Context.md`
- `notes-and-memory/Orbital_Query_Memory_v2026-06-12.md`
- `skills/README.md`
- Local project skill headers under `skills/`
- Project file inventory and representative folder/file counts

### Not Inspected

This report did not inspect every SQL query, script, catalog JSON payload, or raw
API reference file in full. It also did not execute Orbital API calls, query
endpoints, inspect ignored local runtime ledgers, or validate current Cisco
cloud-side product state.

### Explicit Exclusions

Ignored local files, credentials, runtime state, endpoint result rows, and tenant-
specific raw data were not inspected and should not be used in stakeholder
reporting.

### Assumptions

- The current working copy of `README.md` is treated as project context, even if
  it has not yet been committed.
- File counts are orientation indicators captured from the local workspace on
  2026-06-24.
- Project-local skills are counted only where a local `SKILL.md` exists.

### Needs Owner Review

- Confirm whether the current root README update should be committed before this
  report is shared as a stable project artifact.
- Confirm whether stakeholder reporting should mention specific Secure Client /
  Secure Endpoint product areas beyond the inspected project files.
- Confirm whether the `notes-and-memory/Orbital_Query_Memory_v2026-06-12.md` method index
  should be regenerated to include newer query-method files added after
  2026-06-12.
- Confirm whether any generated query artifacts should be promoted to
  `queries_and_scripts/custom_queries/` as personal reusable query work.

## Stakeholder Value

This project gives stakeholders and technical users a structured way to reuse
Orbital knowledge:

- **Faster orientation:** new users can start from `AGENTS.md`, README, and
  context indexes rather than reverse-engineering scattered SQL.
- **Reusable investigations:** query-method memory captures when and why to use a
  query, not just the SQL text.
- **Better traceability:** methods can link osquery tables, Orbital Catalog
  entries, catalog IDs, MITRE/category context, and local generated queries.
- **Reduced operational risk:** target selectors, OS filters, broad-targeting
  cautions, script limits, and endpoint-result privacy rules are explicit.
- **Improved collaboration:** project context separates read-only source
  material, working files, generated queries, notes, and reusable query/script
  repository content.
- **Stronger Secure Client / Endpoint analysis:** Codex-supported context helps
  distinguish installation evidence, runtime process/service state, event-log
  evidence, connectivity evidence, and product health assumptions.

## Recommended Improvements

1. Commit the updated root README if it is accepted as the new project overview.
2. Refresh the query-method memory summary so it includes all current YAML records
   under `02_Working_Files/Query_Methods/`.
3. Add a lightweight promotion checklist for moving generated queries into
   `queries_and_scripts/custom_queries/` when they become personal reusable work.
4. Add a lightweight report index in `notes-and-memory/README.md` so stakeholder summaries
   and query-memory reports are easier to find.
5. Periodically verify catalog/API context freshness, especially when Cisco
   Orbital UI/API behavior or Secure Endpoint documentation changes.
