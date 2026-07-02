---
name: orbital-api-access
description: Access Cisco Orbital API and catalog context. Use when Codex needs to test Orbital API connectivity, authenticate with project credentials, diagnose Codex network/sandbox issues, download or refresh the Orbital catalog through /v0/stock and related catalog endpoints, inspect imported catalog JSON, or explain where Orbital API/catalog context is stored in the project.
---

# Orbital API Access

Use this skill for Cisco Orbital API connectivity and catalog context work. Keep this separate from live endpoint query execution; use `orbital-run-osquery-live-query` when the task is to run osquery SQL against explicit target endpoints. Use `orbital-query-method-memory` when the task is to improve SQL design, reuse prior query methods, or find relevant catalog/osquery mappings.

## Project Change Log

After changing project context, catalog/API source files, helper scripts, skill instructions, or other durable project files, append a sanitized entry to `local/project-change-log.md`. Do not use the project change log for routine sync activity.

Use `local/sync-activity-log.md` for useful operational sync traceability, such as GitHub sync issues, skill installation/update events, workspace-to-global skill sync dates, authentication problems, or permission troubleshooting. Both local logs must not be staged, committed, pushed, or contain credentials, bearer tokens, raw API responses, tenant data, endpoint results, hostnames, IP addresses, GUIDs, or customer-identifying values.

## Project Context Checks

Read these files as needed:

- `AGENTS.md` for project rules.
- `project-context/Orbital_API_DevNet.md` for API endpoint and authentication context.
- `project-context/Orbital_Catalog_API_Import.md` for the latest catalog import summary and raw response pointers.
- `queries_and_scripts/catalog_snapshot/` for GitHub-synced offline Cisco-managed stock catalog snapshots used in query/script decision support.
- `project-context/Orbital_Catalog.md` for catalog handling rules.
- `project-context/Orbital_Query_Catalog_Source_Map.md` for API/UI/osquery cross-references.
- `notes-and-memory/Codex_Network_Access_Fix.md` if DNS or API calls fail inside Codex but work from Terminal.

## Network Check

Before treating an API failure as an Orbital or credential issue, check whether the current Codex shell has network access:

```bash
env | sort | rg -i 'CODEX_SANDBOX|NETWORK|SANDBOX'
python3 - <<'PY'
import socket
s = socket.socket()
s.settimeout(2)
try:
    s.connect(("8.8.8.8", 53))
    print("network_ok")
except Exception as exc:
    print(type(exc).__name__, exc)
finally:
    s.close()
PY
```

If the output shows `CODEX_SANDBOX_NETWORK_DISABLED=1` or socket calls fail with `Operation not permitted`, do not treat it as a credential failure. Explain that the Codex thread needs network-enabled sandbox settings, or ask the user to run the project helper in Terminal and then inspect the refreshed files locally.

## Catalog Access Workflow

Use this workflow when the user asks to test Orbital API access, download the catalog, refresh project context, or import `/v0/stock`.

1. Prefer the project helper:

```bash
tools-and-memory/run_orbital_catalog_import.sh
```

2. Expected successful status lines:

- `stock_query_catalog: HTTP 200`
- `organization_catalog_queries: HTTP 200`
- `organization_catalog_scripts: HTTP 200`
- `stock_catalog_scripts: HTTP 200`

3. Verify refreshed files:

```bash
stat -f '%Sm %N' -t '%Y-%m-%d %H:%M:%S %Z' \
  local/orbital-catalog-api-cache/*.json \
  queries_and_scripts/catalog_snapshot/*.json \
  project-context/Orbital_Catalog_API_Import.md
```

4. Confirm that only Cisco-managed stock files are present under `queries_and_scripts/catalog_snapshot/`; organization catalog exports must remain local-only.

5. Summarize the latest counts from `project-context/Orbital_Catalog_API_Import.md`.

6. If Terminal succeeded while the Codex thread still has network disabled, use the local refreshed raw files and context summary as the imported project context.

## Authentication Check Workflow

Use this workflow when the user asks whether Orbital API authentication works or whether the bearer token is valid.

1. Prefer `GET /v0/ok` because it is a small read-only authentication and service check.

2. Run the project helper:

```bash
python3 tools-and-memory/check_orbital_api_auth.py
```

3. A working bearer token should return HTTP `200` and response message `OK`.

4. Do not print raw `jwt`, bearer token, client secret, or authorization header values. Redact token-bearing fields before showing output.

## `/v0/ok` Response Interpretation

Use this interpretation when explaining the authentication check result:

- `status: 200`: the API call succeeded and the bearer token was accepted.
- `response.message: OK`: Orbital confirms the authenticated request is valid.
- `region`: the API region used by the helper, such as `us`, `na`, `eu`, or `apjc`.
- `login.accessLevel`: whether the identity has read-only or write-capable API access.
- `login.admin`: whether the authenticated identity has admin privileges.
- `login.email`: account email associated with the token.
- `login.idp`: identity provider, for example Cisco SecureX Sign-On (`sxso`).
- `login.jwt`: JWT details returned by the API; always treat as sensitive and redact.
- `login.orbital_scopes`: Orbital API scopes granted to the token, for example `orbital:all`.
- `login.organization`: internal organization UUID.
- `login.organizationName`: human-readable organization name.
- `login.role`: role name for the authenticated identity.
- `login.user`: internal user UUID.
- `login.userName`: human-readable user name.
- `login.xdr`: whether the login context is XDR-based/enabled for this API context.

Practical summary:

- HTTP `200` plus `message: OK` means the bearer token works.
- HTTP `401` or `403` means the token is missing, expired, invalid, or lacks required access.
- `write`, `admin: true`, and `orbital:all` indicate broad Orbital permissions. Mention this as permission context, not as a reason to run broader-impact operations without confirmation.

## Credential Inputs

The import helper reads credentials from environment variables and, by default, from `tools-and-memory/orbital_credentials.env` if that file exists. Never print credentials or bearer tokens.

Supported inputs:

- `ORBITAL_API_TOKEN`, `ORBITAL_TOKEN`, `SECUREX_TOKEN`, `CISCO_SECUREX_TOKEN`, or `CISCO_TOKEN`
- `ORBITAL_CLIENT_ID` plus `ORBITAL_CLIENT_SECRET`
- `SECUREX_CLIENT_ID` plus `SECUREX_CLIENT_SECRET`
- `ORBITAL_REGION`, defaulting to `eu`; supported values: `eu`, `us`, `na`, `apjc`

For North America, this project uses `us`/`na` against `https://orbital.amp.cisco.com/v0` for catalog calls. `https://enterprise.orbital.amp.cisco.com/v0` did not resolve during local testing on 2026-06-02; see `project-context/Orbital_API_DevNet.md`.

## Query ID Terminology

When discussing API follow-up calls:

- `orbital_queryID` means the `ID` returned by `POST /v0/query/run`. Use it with `GET /v0/jobs/{{orbital_queryID}}` and `GET /v0/jobs/{{orbital_queryID}}/results`.
- `queryId:<id>` is a `nodes` target selector used by live-query requests to reuse an existing query definition. It is not the same as `orbital_queryID`.

## Handling Rules

- Treat imported API response files as source context, not editable catalog templates.
- Do not commit or store bearer tokens.
- In this lab project, a local credentials env file may exist under `tools-and-memory`; never print its values in chat or command output.
- Do not publish tenant-specific organization catalog names to public GitHub unless the user explicitly confirms that lab visibility is acceptable.
- Larger skill scope changes require explicit user confirmation before implementation; see `notes-and-memory/decisions/2026-06-10_skill_separation.md`.
