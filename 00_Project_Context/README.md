# Project Context

Store project descriptions, scope notes, GitHub repository references, access notes, and high-level assumptions here.

When adding new project context, check whether a cross-reference file should be created or updated. This is required when new information connects or changes terminology, API fields, identifiers, source priority, folder ownership, catalog data, target selection, query behavior, script behavior, or relationships between UI, API, osquery, catalog, and local source files.

When project context is generated from chat messages or personal input, check whether a project term may be used in the wrong or ambiguous context. If the meaning could conflict with established Orbital terminology, clarify the intended meaning before creating or updating context files.

Current project context files:

- `GitHub_Repo.md`: Orbital repo source folder and folder ownership notes.
- `Orbital_Product_Overview.md`: Structured product overview imported from the Cisco Orbital help page.
- `Orbital_Catalog.md`: Structured catalog notes and mapping to local source folders.
- `Orbital_Catalog_UI_Terms.md`: Authenticated product UI terminology notes for Catalog fields, especially `ID`.
- `Orbital_Queries.md`: Structured query behavior notes, including query types, prefixes, and `allowos`.
- `Orbital_Scripts.md`: Structured script behavior notes, including Python response actions, node concurrency, disabling, and linked scripts.
- `Orbital_Script_Page_Linked_Context.md`: Consolidated import of all help-topic links visible from the Script page.
- `Orbital_API_DevNet.md`: Cisco DevNet Orbital API context, server/auth notes, operation links, and model/schema link index.
- `Orbital_Target_Node_Selectors.md`: Cross-reference for target/device/endpoint/node terminology and API `nodes` selector prefixes.
- `Osquery_Schema_5_23_0.md`: osquery 5.23.0 schema import summary and pointers to structured table/column JSON files.
- `Orbital_Query_Catalog_Source_Map.md`: Cross-reference linking osquery schema, Orbital Catalog API, and authenticated UI terminology for query work.

Recommended metadata for referenced sources:

- Source name
- Original location or URL
- Owner or team
- Content date or validity date
- Copy/import date
- Notes about reliability or known conflicts
