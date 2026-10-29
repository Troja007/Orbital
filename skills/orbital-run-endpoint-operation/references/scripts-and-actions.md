# Scripts And Actions

Read this reference before any Orbital script operation. Scripts run through `POST /script/run`, not a query endpoint.

## Observational Catalog Scripts

Inspect the catalog ID, source, supported operating systems, arguments, and behavior before use. Do not infer that a script is observational from its title. Require the user to identify both the script and exact targets.

Use a narrow `host:` or `hostname:` selector. The Script API requires `os`; a platform list is a compatibility filter, not permission to broaden the target set. Live script responses use `result_id`, endpoint stdout/stderr, and exit codes; they do not produce an `orbital_queryID`.

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/orbital-run-endpoint-operation/scripts/run_live_script.py" \
  --catalog-id check_cisco_nvm_module \
  --target host:EXAMPLE-HOST \
  --os windows \
  --name "codex NVM installation check"
```

Treat the script's reported condition precisely. A result that only says installed does not prove that a related service or process is running; use a separate platform-appropriate query when runtime state matters.

## Inline Python And State Change

Use a reviewed inline Python script only when no suitable catalog script exists. Send base64-encoded source in `script.content`; use `script.args` for parameters. Do not create a catalog entry solely for one-time work.

For every state-changing script, require explicit user approval, exactly one non-wildcard target, `--operation-class state-changing`, and `--approve-state-change`. Independently validate endpoint identity and every destructive precondition inside the script. Refuse the action on any mismatch.

Keep scripts under the endpoint constraints: Python 3.10 or later, 64 KB source, ten-minute timeout, 16 MB stdout/stderr limits, and custom exit codes from `0` through `199`. Nodes execute only one script at a time; ad hoc scripts sent to a busy node can be ignored.

Store only sanitized operation metadata and meaningful API/foundational errors in local ledgers. Never store endpoint stdout/stderr, host identity, raw responses, ORG data, credentials, or tokens.
