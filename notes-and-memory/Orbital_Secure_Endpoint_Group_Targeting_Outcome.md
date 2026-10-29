# Orbital Queries For Secure Endpoint Groups

Scope: Corporate

Classification: Corporate confidential; technical finding based on public API documentation.

Status: Defined project outcome; retained in this project pending a separately authorized migration.

Date defined / last reviewed / valid as of: 2026-10-15

Source publication date: Unknown; API documentation was reviewed in the originating chat.

## Table Of Contents

- [Defined Outcome](#defined-outcome)
- [API Method](#api-method)
- [Limits And Validation](#limits-and-validation)
- [Future Knowledge Placement](#future-knowledge-placement)
- [Sources And Provenance](#sources-and-provenance)

## Defined Outcome

The documented Orbital Query API has no direct target selector for a Secure
Endpoint group ID. Group-based targeting therefore requires resolving group
membership through the Secure Endpoint API and submitting the resulting
computer connector GUIDs as explicit Orbital targets.

This is a finding about the documented public API. It does not establish that
no undocumented or future group-targeting capability exists.

## API Method

1. Retrieve computers with the Secure Endpoint v1 group filter:

   ```http
   GET /v1/computers?group_guid=<GROUP_GUID>&limit=500&offset=0
   ```

2. Follow pagination, collect and deduplicate `data[].connector_guid`, and
   check Orbital availability. Report excluded or unavailable devices.
3. Submit an Orbital query with `nodes` entries such as
   `amp:<COMPUTER_CONNECTOR_GUID>`. An `amp:` value identifies a computer,
   not a Secure Endpoint group.
4. For this project's tracked two-minute scheduled run, use `POST /v0/query`,
   set `expiry` to the current Unix time plus 120 seconds, set `interval` to
   `0`, label the query with `codex`, and retain the returned Job ID.

Use matching regional endpoints and product organization context. Secure
Endpoint v1 authentication and Orbital bearer authentication are separate
API concerns.

## Limits And Validation

- Membership is a snapshot taken during resolution. Later group members are
  not automatically added to the submitted target list.
- Do not assume that filtering a parent group includes child-group members.
  Resolve the intended subgroup scope explicitly.
- Orbital enablement and connectivity determine which selected computers
  can answer. Zero answering endpoints is different from answered endpoints
  returning zero rows.
- Validation status: documentation-reviewed method; no group-targeted
  endpoint query was executed as part of this finding.
- Recheck the public selector list and group filter before implementing the
  method if the API documentation changes.

## Future Knowledge Placement

The following is a placement definition, not a completed migration or an
authorization to perform one.

| Layer | Intended content when migration is authorized |
| --- | --- |
| LLM-Wiki | Concise reusable finding on the Orbital product/API topic, with source references and a link to the canonical outcome. |
| LLM-Wiki-RAW | Selected API documentation extracts or a dated source note sufficient to reconstruct the claim, including the documentation-only validation boundary. |
| LLM-Wiki-Outcomes | This dedicated outcome file as the canonical human-readable deliverable, with an entry in the Outcome library README. |

Current canonical location: this project file. No Wiki, RAW, central Outcome
library, KB, environment profile, or routing index is updated by this record.

## Sources And Provenance

- [Cisco Orbital Query API: Specifying Nodes](https://developer.cisco.com/docs/orbital/queries/#specifying-nodes): documented selectors, including `amp:` for Secure Endpoint computer GUIDs; no Secure Endpoint group selector is listed.
- [Cisco Orbital Query API](https://developer.cisco.com/docs/orbital/queries/): scheduled query request fields and API operation.
- [Cisco Secure Endpoint Computer API](https://developer.cisco.com/docs/secure-endpoint/v1-api-reference-computer/): API source for computer inventory. The originating review also checked the imported v1 OpenAPI definition for the `group_guid` query parameter; the web-rendered reference was not readable through the browsing tool.
- [Project target-selector cross-reference](../project-context/Orbital_Target_Node_Selectors.md): existing local terminology and identifier mapping.

Origin: the Orbital project chat discussion of Secure Endpoint group-based
query targeting. The user selected the immediately preceding finding as an
outcome and clarified corporate scope, project-local retention, and deferred
Wiki/RAW/Outcome-library migration.
