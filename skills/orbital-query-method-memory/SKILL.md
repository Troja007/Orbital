---
name: orbital-query-method-memory
description: Build and use a Cisco Orbital/osquery query-method knowledge base without storing endpoint results. Use when Codex needs to decide when to use which Orbital query or stock Orbital script for a threat, alert, IOC, analyst question, endpoint state question, or prior investigation pattern by combining local query-method memory with Orbital Catalog categories, MITRE TTP mappings, catalog Name/ID metadata, osquery table and column validation, platform assumptions, targeting notes, stock-script usage guidance, and prior lessons.
---

# Orbital Query Method Memory

Use this skill to improve Orbital investigation speed and quality over time by building a knowledge base that explains when to use which Orbital query and, for stock catalog scripts only, when to use which script. This skill stores methods, input patterns, decision guidance, reasoning, catalog references, MITRE/category context, stock-script usage guidance, and lessons learned. It must not store live query result rows, endpoint-specific evidence, custom script content, or custom script execution details.

Treat every useful query design, endpoint investigation, catalog comparison, context import, and analyst correction as a possible memory improvement. Save only reusable and sanitized method knowledge after user approval so the GitHub-synced project becomes faster and more accurate for future Codex workspaces.

Use `orbital-api-access` for catalog import, catalog freshness checks, authentication, API connectivity, and raw catalog context. Use `orbital-run-endpoint-operation` only when the user has explicit targets and wants to execute an Orbital osquery query or stock catalog script. When execution work requires SQL design, table choice, catalog/script reuse, or repeated investigation patterns, this skill should be used before execution to speed up and improve query quality.

Own SQL correction here. If an Orbital execution returns a real endpoint/osquery error, especially unknown column, unknown table, unsupported table, constraint, syntax, or platform-availability errors, stop the execution loop and use this skill to correct the query method. Do not let `orbital-run-endpoint-operation` iterate through replacement SQL or health probes unless the user explicitly asks for troubleshooting execution behavior. Preserve the original Job ID as operational context in chat only; do not store it in method memory.

## Default User-Facing Style

Use all available context and memory internally, but keep the visible answer short and traceable by default. When query-method memory influences a query, summarize only the selected method, why it was chosen, relevant caveat, and whether memory/context should be updated. Provide long method comparisons, source traces, catalog lists, or full SQL explanations only when needed for approval, troubleshooting, safety, or when the user asks.

## Project Change Log

After changing query-method records, query-memory summaries, project context, skill instructions, generated durable artifacts, or other durable project files, append a sanitized entry to `local/project-change-log.md`. Do not use the project change log for routine sync activity.

Use `local/sync-activity-log.md` for useful operational sync traceability, such as GitHub sync issues, skill installation/update events, workspace-to-global skill sync dates, authentication problems, or permission troubleshooting. Both local logs must not be staged, committed, pushed, or contain endpoint results, hostnames, IP addresses, GUIDs, raw API responses, tenant data, credentials, or customer-identifying values.

When query-method work creates or changes a durable project decision, also add or update a GitHub-synced decision record under `notes-and-memory/decisions/`. Use this for decisions about the memory model, validation gate, source priority, catalog reuse, privacy boundary, GitHub sharing boundary, folder ownership, or skill responsibility. Keep the record sanitized and do not include endpoint results, hostnames, IP addresses, GUIDs, raw API responses, tenant data, credentials, or customer-identifying values.

## Core Boundary

Store:

- Analyst input, threat context, alert wording, or investigation question.
- Sanitized natural-language input patterns from chat or analyst requests, stored as examples for future matching.
- Query goal and reasoning.
- When to use the query and when not to use it.
- For stock catalog scripts only: when to use the script, what endpoint state or remediation question it helps answer, and which catalog `Name` and `ID` identify it.
- Which investigation question, threat behavior, or endpoint state the query helps answer.
- Orbital Catalog matches, including both `Name` and `ID`.
- Table-level Orbital Catalog context for tables used by executed queries, including catalog categories and MITRE mappings where present.
- Related table-derived Orbital Catalog category and MITRE TTP context, clearly marked as related context when not part of the exact catalog query.
- osquery tables, columns, joins, constraints, and SQL patterns.
- Query type guidance: live/custom query, scheduled query, or catalog query reuse.
- Targeting guidance: selector type, `nodes` syntax, broad-targeting warnings, and `allowOS`/platform assumptions.
- Lessons learned, validation status, and caveats.
- Stock script usage lessons, validation status, and caveats, without storing execution output.

ID terminology for methods:

- `orbital_queryID`: returned `ID` from a live query execution. It is execution-specific and should only be referenced as an operational follow-up concept, not stored as reusable method memory.
- `queryId:<id>`: target selector for reusing an existing query definition in `nodes`.
- Catalog `ID`: catalog query/script identifier.

Do not store:

- Endpoint result rows.
- Custom script bodies, generated custom scripts, custom script execution records, or custom script output. Custom script method memory may be implemented later, but is out of scope for this skill now.
- Full raw chat transcripts.
- Unsanitized natural-language requests that include endpoint names, usernames, IP addresses, customer names, GUIDs, incident IDs, tokens, or returned result values.
- Hostnames, usernames, IP addresses, MAC addresses, Orbital IDs, Secure Endpoint GUIDs, Secure Client GUIDs, AnyConnect UDIDs, customer names, tenant identifiers, bearer tokens, client secrets, raw API responses, or raw investigation output.
- Any copied query result that could identify a customer, endpoint, user, or organization.

## User Approval Gate

Before creating or updating memory from a query, investigation, result interpretation, or newly proposed method, show the user the response first and wait for explicit approval to learn from it. This approval is separate from method validation status such as `tested` or `validated`.

Required order:

1. Produce the user-facing answer, result summary, SQL recommendation, or proposed method record.
2. Ask the user to approve that the response is correct enough, useful, and should be learned.
3. Do not write to `tools-and-memory/query-method-memory/`, regenerate reports under `notes-and-memory/`, or sync global memory until the user explicitly confirms.
4. After confirmation, save only reusable method knowledge and sanitized input patterns. Never save endpoint results or sensitive values.

Acceptable approval examples:

- "confirmed"
- "yes, update memory"
- "save this method"
- "validated"

If the user only confirms that the result is correct but does not clearly approve a memory update, ask whether the reusable method should be saved. If the user asks to change the response before approval, revise the response and ask again. If the user does not approve, leave memory unchanged.

## Stock Script Usage Boundary

This skill may store reusable guidance for stock Orbital catalog scripts only. The memory should answer "when should I use which stock script?" not "what script did I execute on which endpoint?"

Store stock script usage only in this form:

- investigation question or endpoint state question the stock script helps answer;
- catalog script `Name` and catalog `ID`;
- when to use the script;
- when not to use the script;
- supported platform or target assumptions;
- expected high-level interpretation of success/failure states, without endpoint output;
- related product context, catalog category, and MITRE context when present in Orbital Catalog;
- sanitized natural-language examples that would cause a future agent to recommend the script.

Example:

- Use the stock script `check_cisco_nvm_module` when the analyst needs to determine whether the Cisco Secure Client Network Visibility Module is installed correctly.

Do not store:

- custom script bodies or generated scripts;
- custom script execution methods;
- endpoint-specific script execution records;
- script stdout/stderr, return codes tied to real endpoints, hostnames, Job IDs, or result values;
- one-off remediation logic that is not a stock catalog script.

If the user asks to store a custom script method, explain that custom script method memory is not implemented yet and keep the script out of query-method memory unless the user explicitly asks to store the script in a different project-owned script location.

## Project Context Checks

Read these files as needed:

- `AGENTS.md` for project rules.
- `project-context/Orbital_Catalog.md` for catalog handling rules.
- `project-context/Orbital_Catalog_API_Import.md` for current catalog import status and raw catalog file locations.
- `project-context/Orbital_Query_Catalog_Source_Map.md` for how to combine catalog API, catalog UI, and osquery schema sources.
- `project-context/Orbital_Catalog_UI_Terms.md` for user-facing catalog terminology.
- `project-context/Orbital_Queries.md` for live/custom query, scheduled query, prefix, dynamic/static, and `allowOS` behavior.
- `project-context/Orbital_Target_Node_Selectors.md` for target/node selector terminology.
- `project-context/Orbital_Windows_Catalog_Result_Reading.md` and `queries_and_scripts/catalog_result_profiles/windows/` when explaining what a Windows stock catalog query result means, including expected row-count behavior, returned columns, no-response handling, caveats, and safe incident-responder assumptions.
- `project-context/Osquery_Schema_5_23_0.md` and `product-context/osquery/osquery_schema_5_23_0.json` for table and column validation.
- `project-context/Orbital_Source_Repository_Model.md` before deciding whether a query/script belongs to catalog source/template material or user-owned custom repository content.
- `product-context/Cisco_Secure_Client_Endpoint_Context.md` when Secure Client, Secure Endpoint, NVM, EVM, endpoint drivers, modules, or product-specific Windows/macOS evidence matters.
- `product-context/Orbital_AI_Investigation_Layer_Context.md` when query-memory output feeds a broader investigation or assistant workflow.
- `notes-and-memory/Orbital_Query_Memory.md` for the current query-memory report pointer.
- `notes-and-memory/Codex_Network_Access_Fix.md` if network or DNS failures affect catalog/API refresh or live query checks from Codex.

Do not use the old moved paths `00_Project_Context/` or `04_Notes/`. Their content now lives under `project-context/`, `product-context/`, and `notes-and-memory/`.

Use catalog source files as read-only references:

- `local/orbital-catalog-api-cache/*.json`
- `queries_and_scripts/catalog_snapshot/*.json`
- `queries_and_scripts/catalog_result_profiles/*.jsonl`
- `queries_and_scripts/catalog_result_profiles/windows/*.md`
- `queries_and_scripts/catalog_queries`
- `queries_and_scripts/catalog_scripts`

Use generated and working query files as implementation context, not as source-of-truth memory:

- `queries_and_scripts/Generated_Queries`
- `queries_and_scripts/draft_queries`

Do not edit catalog source folders directly. If a catalog query is adapted, save only reusable method knowledge into query-method memory after user approval, not the generated SQL artifact.

Do not create or commit generated query files by default. Keep generated SQL in chat, pass it directly to an execution helper, or use a local-only scratch path. Store a query under `queries_and_scripts/custom_queries/` only when the user explicitly asks to save that exact query as a custom query.

## Memory Locations

Store reusable query-method records under:

```text
tools-and-memory/query-method-memory/
```

Store query-memory reports and summaries under:

```text
notes-and-memory/
```

Use `notes-and-memory/Orbital_Query_Memory.md` as the current report pointer. Versioned reports should use names like `notes-and-memory/Orbital_Query_Memory_vYYYY-MM-DD.md`.

Recommended category folders:

- `suspicious_processes`
- `persistence`
- `network`
- `files`
- `registry`
- `software`
- `identity`
- `orbital_health`

Use YAML for structured records when possible. Use Markdown only when the method needs longer narrative notes.

If a generated search index is needed later, place it under `local/orbital_query_method_index/` and treat it as disposable. Do not use the index as the source of truth.

## Investigation Method Workflow

1. Clarify the input if the user's terms are ambiguous. Examples: "ID" could mean Catalog `ID`, Orbital endpoint ID, Secure Endpoint GUID, Secure Client GUID, AnyConnect UDID, `queryId`, or `orbital_queryID`.
2. Capture the user's natural-language request as sanitized input-pattern memory. Preserve how the user phrased the need, but remove endpoint names, usernames, IP addresses, customer names, GUIDs, incident IDs, tokens, and result values.
3. Normalize the input into searchable concepts: threat name, behavior, IOC type, platform, table/domain hints, stock-script hints, and expected endpoint information.
4. Search local method memory in `tools-and-memory/query-method-memory` before writing new SQL.
5. Use `orbital-api-access` when catalog data may be stale, missing, or needed from `/v0/stock` or organization catalog sources.
6. Search Orbital Catalog context for matching stock or organization queries and stock catalog scripts. Prefer catalog templates or stock scripts when they fit the investigation goal.
7. Record both catalog `Name` and catalog `ID` for any catalog item used as context.
8. Validate osquery tables and columns against `product-context/osquery/osquery_schema_5_23_0.json`; note where Orbital availability still needs product verification.
9. Decide which query to use by comparing method records on: investigation fit, platform fit, freshness/current-state limits, endpoint cost, broad-targeting risk, catalog category, MITRE TTP relevance, and validation status.
10. Recommend one or more query or stock-script methods, including when to use each method, when not to use it, query/script type, platform assumptions, target selector guidance, and broad-targeting cautions.
11. If query execution is requested, hand off to `orbital-run-endpoint-operation` after targets and SQL are explicit. If stock script execution is requested, hand off only after the stock catalog script `Name`/`ID`, targets, platform assumptions, and approval are explicit.
12. If execution returns a real query error, use the error class to revise the method before any retry:
    - unknown column: validate the table schema and choose a supported column or remove the field;
    - unknown/unsupported table: select a catalog-backed or upstream-supported table;
    - required constraint: add the required `WHERE` constraint;
    - platform mismatch: adjust target/platform guidance;
    - empty Orbital error placeholder with valid rows: treat as parser/response-shape handling, not a query-design failure.
13. After execution, show the user-facing response/result summary first and ask the user to approve whether reusable method knowledge should be learned.
14. Only after explicit user approval, enrich query methods by extracting the tables used by the SQL and adding Orbital Catalog context for those tables. Store catalog `Name`, `ID`, OS/platform, categories, MITRE tactics, techniques, subtechniques, and update date when available.
15. Only after explicit user approval, enrich stock-script methods with catalog script `Name`, catalog `ID`, use case, platform assumptions, category, MITRE tactics, techniques, subtechniques, update date, and caveats when available. Do not store custom scripts or script execution output.
16. After a useful investigation, query design, or stock-script recommendation, ask whether to save or update the method memory record. Save only the method, sanitized input pattern, and reusable context, never returned endpoint or script output data.

## Natural-Language Input Memory

Store natural language to improve future matching, but treat it as input-pattern memory, not chat history.

Use `investigation_inputs.examples` for sanitized examples:

```yaml
investigation_inputs:
  source_type: "analyst_question"
  examples:
    - "Check all endpoints for non-default hosts-file entries."
    - "Find current running process details for a named Windows process."
  keywords:
    - "hosts file"
    - "running process"
```

Rules:

- Preserve the user's intent and common phrasing.
- Normalize spelling and obvious table-name mistakes when helpful, but keep enough of the original phrasing to match future requests.
- Replace sensitive values with placeholders such as `<hostname>`, `<ipv4>`, `<sha256>`, `<username>`, `<customer>`, `<incident_id>`, or `<process_name>`.
- Do not store full raw chat messages, result rows, or one-off customer-specific wording.
- If a request contains useful reusable language plus sensitive values, store a generalized version.

Examples:

- Raw: "Check <hostname> for 127.0.0.1 adobe entries."
- Store: "Check a specific endpoint for non-default hosts-file entries."

- Raw: "Query running processes from Windows endpoints only. process name sfc.exe."
- Store: "Query running processes from Windows endpoints for a specific process name."

## Knowledge Base Requirements

Every saved method should help a future agent answer "which query should I use now?"

For stock catalog scripts, every saved method should help a future agent answer "which stock script should I use now?"

Include these decision fields in the record, either explicitly or through existing sections:

- `use_when`: investigation situations where this query is appropriate.
- `do_not_use_when`: situations where this query is weak, misleading, stale, too expensive, or the wrong evidence type.
- `answers`: concrete questions the query can answer.
- `does_not_answer`: common adjacent questions this query does not answer.
- `preferred_next_queries`: follow-up query methods to run when results need validation, expansion, or historical context.
- `stock_script_usage`: for stock scripts only, the catalog script `Name`/`ID`, use case, platform assumptions, and interpretation caveats.
- `catalog_context`: exact matching Orbital Catalog query/script entries when available.
- `catalog_table_context`: table-level catalog context for the actual tables used.
- `related_table_ttp_context`: broader table-derived categories and MITRE TTPs from Orbital Catalog entries, clearly marked as related context.
- `orbital_guidance`: query type, platform filters, target selector advice, and broad-targeting/performance risk.
- `investigation_inputs.examples`: sanitized natural-language request patterns that future users are likely to type.

Do not treat `related_table_ttp_context` as a detection claim. It is for search, triage routing, and query selection.

Do not create `custom_script_usage` or similar fields yet. Custom-script memory is intentionally reserved for a later implementation.

## Orbital Skill Routing

Use the available Orbital skills together instead of treating query work as a single-step SQL task:

- Start with this skill when the user asks what to query, how to query, how to investigate a threat, or when a request resembles a reusable pattern.
- Use `orbital-api-access` before or during design when catalog/API context matters, catalog files may need refresh, authentication needs checking, or raw catalog metadata is needed for categories, MITRE mappings, UI/API IDs, or stock/organization query comparison.
- Use `orbital-run-endpoint-operation` only for execution after SQL or the stock catalog script `Name`/`ID`, target selectors, OS filters, and broad-targeting approval are clear.
- Use this skill, not the execution skill, to repair wrong SQL after endpoint/osquery errors. The execution skill should preserve and report the Job ID, not run multiple replacement queries on its own.
- Use `orbital-catalog-result-profiles` when explaining or refreshing sanitized catalog result-profile artifacts, expected row-count behavior, returned columns, no-response handling, caveats, or incident-responder reading guidance for stock catalog query results.
- Return to this skill after execution to save or update reusable query method context or stock-script usage guidance, catalog context, validation notes, performance lessons, and caveats. Never store script output or custom script content.

For broad endpoint query runs, the preferred chain is:

1. `orbital-query-method-memory`: search memory and catalog context, design SQL, identify tables and platform assumptions.
2. `orbital-api-access`: refresh or verify catalog/API context if needed.
3. `orbital-run-endpoint-operation`: execute against explicit targets.
4. Show the user-facing response/result summary and wait for explicit user approval to learn from it.
5. `orbital-query-method-memory`: after approval, store reusable method context and catalog enrichment, never endpoint results.

## Cross-Skill Usage For Endpoint Queries

When a user asks to run an endpoint query and the SQL is not already fully specified:

1. Use this skill to search prior methods and catalog context first.
2. Return the recommended SQL pattern, required columns, platform assumptions, and target cautions.
3. Then hand off to `orbital-run-endpoint-operation` for the actual API execution.
4. After the query completes, show the user-facing response/result summary and ask the user to approve whether reusable method knowledge should be saved.
5. Only after explicit user approval, use the method, SQL pattern, table names, catalog context, validation notes, and lessons learned for memory updates. Do not store hostnames, endpoint IDs, rows, or result values.

When a user asks whether a stock script should be used:

1. Use this skill to search prior methods and catalog context first.
2. Return the recommended stock script `Name` and catalog `ID`, plus when to use it, when not to use it, platform assumptions, and caveats.
3. If execution is requested, hand off to `orbital-run-endpoint-operation` only after the stock script and targets are explicit.
4. After execution, show the user-facing response/result summary and ask whether the stock-script usage guidance should be learned.
5. Only after explicit user approval, save reusable stock-script usage guidance. Do not store endpoint-specific execution details, custom scripts, stdout/stderr, return codes tied to real endpoints, Job IDs, or result values.

## Post-Execution Catalog Enrichment

When a query is executed or finalized and the user has approved learning from the response:

1. Identify the tables used in `FROM`, `JOIN`, and subquery clauses.
2. Search local method memory and Orbital Catalog sources for each table name.
3. Prefer catalog query entries whose SQL or metadata directly uses the same tables and serves a similar goal.
4. Store table-level context under `catalog_table_context` in the method record:
   - table name
   - catalog `Name` / title
   - catalog `ID`
   - catalog source
   - catalog categories shown by Orbital
   - MITRE tactics, techniques, and subtechniques when present
   - supported OS/platform values
   - update date
   - short relevance note
5. If the catalog has no MITRE mapping for a matching entry, record an empty list and note that no MITRE mapping was present in the catalog source.
6. Also add `related_table_ttp_context` when other Orbital stock catalog entries using the same tables provide useful category or MITRE context for future query selection.
7. Do not infer MITRE mappings unless clearly marked as an inference. Prefer the mapping shown by the Orbital Catalog.

## Catalog Context Workflow

When using Orbital Catalog context:

1. Search local catalog API files, catalog query files, and catalog script files for relevant terms, table names, script names, tactics, techniques, and query names.
2. Prefer entries whose SQL, script metadata, or catalog metadata match the user's investigation question.
3. Preserve catalog metadata that affects future reuse: `Name`, `ID`, OS/platform, category, author/source, MITRE mapping when present, and update date when available.
4. Treat catalog SQL as a method source, not automatically as a final query. Validate table/column assumptions and adapt only when needed.
5. For Cisco-managed catalog source folders, do not modify the original files.

## Record Quality Rules

Each method record should include enough context that a future investigation can reuse it without re-discovering the same query, stock script, catalog mapping, or decision boundary.

Required common fields:

- `title`
- `status`: `draft`, `tested`, `validated`, or `deprecated`
- `created`
- `updated`
- `investigation_inputs`
- `query_goal` for query records or `script_goal` for stock-script records
- `catalog_context`
- `orbital_guidance`
- `validation`
- `lessons`
- `privacy`

Required query-method fields:

- `query_goal`
- `catalog_table_context`
- `related_table_ttp_context`
- `osquery_context`
- `sql_patterns`

Required stock-script fields:

- `stock_script_usage`
- `script_goal`
- `script_catalog_context`
- `script_output_boundary`: state explicitly that endpoint-specific stdout/stderr, return codes tied to real endpoints, Job IDs, and result values must not be stored.

Mark records as `draft` until the method has been reviewed or used successfully. Do not claim a method is validated just because the SQL is syntactically plausible.

## Search Patterns

Use `rg` against method memory and source context. Useful searches:

```bash
rg -i "powershell|encodedcommand|scriptblock|bitsadmin" tools-and-memory/query-method-memory queries_and_scripts/Generated_Queries local/orbital-catalog-api-cache queries_and_scripts/catalog_queries project-context product-context
rg -i "persistence|services|scheduled_tasks|startup|launchd|autorun" tools-and-memory/query-method-memory queries_and_scripts/Generated_Queries local/orbital-catalog-api-cache queries_and_scripts/catalog_queries project-context product-context
rg -i "processes|listening_ports|process_open_sockets|hash|file|registry" tools-and-memory/query-method-memory queries_and_scripts/Generated_Queries local/orbital-catalog-api-cache queries_and_scripts/catalog_queries project-context product-context
```

If `tools-and-memory/query-method-memory` does not exist yet, create it before saving records.

## Save Or Update Workflow

Before saving a new method record:

1. Confirm the user has approved learning from the response/result summary or proposed method and explicitly approved the memory update.
2. Check for an existing related method record to update instead of creating a duplicate.
3. Remove endpoint-specific values from examples. Replace them with placeholders such as `<hostname>`, `<ipv4>`, `<sha256>`, `<path>`, or `<process_name>`.
4. Add sanitized natural-language examples that preserve the user's intent and likely future phrasing.
5. Link catalog `Name` and `ID` if catalog context influenced the method.
6. Include why this method is useful, when to use it, and when it is not enough.
7. Include query type guidance and whether live query or scheduled query is more appropriate. For stock scripts, include the stock catalog script `Name`/`ID` and why script execution is more appropriate than a query.
8. Include index-ready Orbital Catalog categories and MITRE TTP summaries so reports can show them in the Method Index.
9. Keep SQL examples generic and bounded. Avoid `SELECT *` unless the reason is documented.
10. Reject custom script storage in method memory for now. If the useful lesson came from a custom script, store only a sanitized note that custom-script method memory is out of scope unless another project artifact is explicitly requested.

When updating an existing method record, preserve useful prior lessons and add a dated note rather than overwriting historical reasoning.

## Output Style

When recommending a method, return:

- Best matching prior method records.
- Relevant Orbital Catalog entries by `Name` and `ID`.
- Orbital Catalog category and MITRE TTP context, clearly distinguishing exact catalog mappings from related table-derived context.
- Recommended SQL pattern, catalog query, or stock catalog script to start from.
- When to use the query/script and when not to use it.
- Platform and targeting guidance.
- Caveats and validation status.
- Whether the method should be saved or updated after the investigation.

When generating a query-memory report, the Method Index must include columns for:

- method title
- status
- category
- platforms
- tables
- stock script Name/ID when applicable
- primary catalog context
- Orbital Catalog categories
- MITRE TTP summary

Add a note when MITRE context is related table-derived context rather than an exact catalog query mapping.

Do not present stored method memory as proof that a threat is present on an endpoint. Method memory only describes how to query.
