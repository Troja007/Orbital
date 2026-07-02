# Orbital AI Investigation Layer Context

Created: 2026-06-24
Status: working product context
Scope: Product outcome and workflow context for using Codex skills as a natural-language investigation layer over Cisco Orbital.

This file captures reusable product context from user-provided narrative input and existing project material. It is intentionally method- and outcome-focused. Do not store live endpoint result rows, hostnames, usernames, IP addresses, tenant identifiers, API tokens, raw API responses, or raw investigation output here.

## Source Basis

- User-provided LinkedIn post text received in this project chat on 2026-06-24. Original post publication date was not provided.
- `project-context/Orbital_Product_Overview.md`: high-level Orbital product context.
- `project-context/Orbital_API_DevNet.md`: API entry point, query/script operations, authentication and server-region notes.
- `project-context/Orbital_Catalog_API_Import.md`: catalog import behavior and API response file pointers.
- `project-context/Orbital_Catalog.md`: catalog concepts and local catalog source mapping.
- `project-context/Orbital_Catalog_UI_Terms.md`: user-facing catalog terminology, especially `Name` and `ID`.
- `project-context/Orbital_Query_Catalog_Source_Map.md`: relationship between osquery schema, Orbital Catalog API, and authenticated Orbital UI analysis.
- `project-context/Orbital_Target_Node_Selectors.md`: target/device/endpoint/host wording versus API `nodes` selectors.
- `project-context/Osquery_Schema_5_23_0.md`: upstream osquery table and column reference.
- `product-context/Cisco_Secure_Client_Endpoint_Context.md`: Secure Endpoint, Secure Client, Orbital, and adjacent Cisco endpoint artifact context.
- `tools-and-memory/query-method-memory/README.md`: query-method memory rules and storage boundaries.
- `queries_and_scripts/Generated_Queries/windows_tdnr_secure_client_module_status.sql`: generated Windows query for TDNR-relevant Cisco endpoint module installation and active-state evidence.
- Local Codex skills for Orbital API access, catalog updates, live osquery execution, and query-method memory.

## Product Outcome

The project positions Orbital as more than a manual query engine. The desired product outcome is an endpoint investigation layer that can be driven by analyst intent:

- The analyst states the investigation goal in natural language.
- Codex maps the intent to Orbital product concepts, endpoint artifacts, catalog entries, osquery tables, query type, and target selector behavior.
- Codex selects or adapts a suitable query method, preferring existing Orbital catalog content and local query-method memory before creating new SQL.
- Codex can execute the query through the Orbital API when the user provides explicit target context and the execution is appropriate.
- Codex explains returned evidence in analyst-friendly language, including confidence, gaps, and what the result does not prove.
- Codex can review previous result material again and re-explain it without requiring the analyst to manually reconstruct the query context.
- Codex improves speed and quality over time by storing reusable query-method memory, not raw endpoint results.

The important product framing: natural language does not replace analyst judgment. It reduces friction between investigation intent and endpoint telemetry, especially when the analyst does not already know which Orbital catalog entry, osquery table, field, or SQL pattern to use.

## Core Workflow

Use this workflow when turning natural-language endpoint questions, screenshots, IOCs, or incident context into Orbital work:

1. Clarify the investigation intent.
   - Identify whether the user wants inventory, configuration, runtime state, IOC sweep, communication evidence, product health, or response action support.
   - Ask for clarification when a product term is ambiguous, especially if it could refer to Orbital target selectors, catalog IDs, Secure Endpoint identifiers, Secure Client modules, or endpoint host identity.

2. Map the intent to product context.
   - Use Secure Client / Secure Endpoint context for Cisco endpoint artifact names, module names, services, processes, drivers, registry paths, and expected interpretation.
   - Use Orbital target selector context for translating customer-facing terms such as target, device, endpoint, or host into API `nodes` selectors.
   - Preserve the distinction between Catalog `ID`, query ID, Orbital endpoint selector IDs, Secure Endpoint computer GUID, Secure Client computer GUID, AnyConnect UDID, and hostnames.

3. Select the query method.
   - Prefer stock or organization catalog entries where a suitable template exists.
   - Use local query-method memory to reuse validated table choices, SQL patterns, platform assumptions, and interpretation cautions.
   - Use the osquery 5.23.0 schema for upstream table and column structure, then verify Orbital availability and platform behavior before treating a table as usable.
   - Use generated SQL only when catalog and memory do not already cover the intent, or when the investigation needs a composed view across multiple evidence sources.

4. Validate execution details.
   - Confirm platform assumptions such as Windows-only tables or Secure Client module-specific artifacts.
   - Confirm whether the request needs live query/probe behavior or scheduled query behavior.
   - Avoid broad `all` targeting unless the user has explicitly accepted the risk and the query is safe for broad execution.
   - Include `allowos` or an operating-system filter when needed for platform-specific queries.

5. Execute or prepare.
   - When executing through the API, put target selectors in the `nodes` array.
   - Keep bearer tokens and credentials out of project files.
   - For reusable catalog entries, preserve fields that affect the Orbital UI and record both `Name` and `ID`.

6. Explain the result.
   - Summarize what the evidence shows, what it does not show, and whether follow-up evidence is needed.
   - Separate installation evidence from active runtime evidence.
   - Treat absence of rows carefully. It can mean missing artifact, table limitation, platform mismatch, timing issue, privilege/visibility issue, or a query that was too narrow.
   - Store only reusable method lessons after the investigation, never raw endpoint rows or sensitive identifiers.

## Enabled Capabilities

The current project state supports these capabilities:

| Capability | Project basis | Product value |
| --- | --- | --- |
| Import and understand the Orbital query catalog | Catalog API import context, catalog source map, catalog UI terms | Makes query discovery programmatic instead of manual UI browsing. |
| Select suitable Orbital queries from natural language | Query-method memory, catalog source map, osquery schema, product context | Helps answer "which query should I use?" from the analyst's intent. |
| Execute endpoint queries through the Orbital API | API DevNet context and live-query skill | Converts selected methods into endpoint evidence when target context is explicit. |
| Explain results in analyst language | Product artifact context and method lessons | Helps answer "how should I interpret this result?" without requiring SQL expertise. |
| Re-explain previous results | Result interpretation rules and source-context mapping | Allows later analysis of previously captured evidence without losing product meaning. |
| Build memory from query methods | `tools-and-memory/query-method-memory` | Improves future query selection while avoiding storage of sensitive endpoint data. |
| Use screenshots, IOCs, or incident context as input | Natural-language intent mapping plus product artifact context | Turns unstructured investigation input into concrete Orbital steps. |

## TDNR-Relevant Secure Client Example

The user-provided example is not a classic IOC sweep. It is a product-state validation task:

Question shape:

> Are the Cisco Secure Client modules relevant for TDNR installed and active on this host?

Reusable interpretation:

- The task starts from natural language and screenshot/product context, not from a known malicious hash, IP, or domain.
- The investigation goal is to validate endpoint module presence and active state for a specific host.
- The useful evidence is a combined view across installed programs, services, and running processes.
- The generated query `queries_and_scripts/Generated_Queries/windows_tdnr_secure_client_module_status.sql` checks module-level state for:
  - EDR / Cisco Secure Endpoint
  - Orbital / Query & Script
  - EVM / Endpoint Visibility
  - NVM / Network Visibility
  - Digital Forensics / XDR Forensics
- The result should be interpreted as endpoint evidence, not as a complete licensing, policy, cloud-console, or product-entitlement verdict.

Important nuance:

- Installed does not always mean active.
- Active service/process evidence does not prove that every feature is configured, healthy, licensed, or receiving cloud policy.
- Driver services can report PID `0`, and stopped boot-start drivers can be normal depending on driver type and runtime state.
- Secure Client module versions can differ from the base VPN client version.
- A host may have relevant modules installed but idle until policy, traffic, user session, VPN state, or product configuration activates them.

## Analyst-Friendly Explanation Rules

When explaining Orbital results in this workflow:

- Start with the direct answer: confirmed, not confirmed, partial, or inconclusive.
- Tie each conclusion to the evidence source: `programs`, `services`, `processes`, `drivers`, `file`, `registry`, `process_open_sockets`, DNS cache, event logs, or catalog metadata.
- Explain confidence and limitations explicitly.
- Avoid claiming a negative from absence alone unless the query scope, platform, table availability, and expected artifact path were validated.
- Distinguish endpoint telemetry from management-plane truth. Orbital can show endpoint artifacts and observed runtime state; some questions still require Secure Endpoint, Secure Client, XDR, firewall, proxy, or policy-console confirmation.
- Preserve analyst control. Recommend follow-up queries or external checks where evidence is insufficient rather than over-interpreting one query.

## Memory Rules

Store reusable memory as query methods when a run teaches a durable lesson:

- Good investigation input patterns.
- Catalog `Name` and `ID` references.
- Useful tables, columns, joins, and platform assumptions.
- SQL patterns that worked or failed.
- Targeting guidance.
- Interpretation cautions.

Do not store:

- Endpoint rows.
- Hostnames, usernames, IP addresses, GUIDs, tenant identifiers, or customer names.
- API tokens, raw API responses, or raw screenshots.
- One-off incident facts that are not reusable method knowledge.

## Design Implications

For future skills, scripts, or helper tools in this project:

- Treat the natural-language layer as an orchestration and interpretation layer over Orbital, not as a replacement for catalog validation or osquery schema checks.
- Make query selection explainable: show why a catalog entry or SQL pattern was selected, which tables it uses, and which assumptions must hold.
- Keep the user-facing language product-aware but evidence-bound.
- Reuse generic names for project assets unless the user explicitly asks for customer-, incident-, or campaign-specific naming.
- Maintain cross-references when new context changes terminology, API fields, identifiers, source priority, catalog mapping, target selection, query behavior, script behavior, or UI/API/osquery relationships.
