# Codex Network Access Fix

Observed on 2026-06-10:

- The endpoint DNS resolver works outside Codex, but this Codex thread runs with `CODEX_SANDBOX_NETWORK_DISABLED=1`.
- Direct socket connections from the Codex shell fail with `Operation not permitted`.
- DNS resolution inside the sandbox fails because the sandbox has no usable DNS configuration.
- Removing the environment variable in a child process does not restore network access, so this is an enforced sandbox policy.
- The project `.codex/config.toml` is mounted read-only in this session, so it could not be updated from inside Codex.

Recommended project setting for future Codex sessions:

```toml
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
```

After applying this setting outside the current restricted session, start a new Codex thread or restart the current workspace session and rerun:

```zsh
tools-and-memory/run_orbital_catalog_import.sh
```

Expected successful output:

- `stock_query_catalog: HTTP 200`
- `organization_catalog_queries: HTTP 200`
- `organization_catalog_scripts: HTTP 200`
- `stock_catalog_scripts: HTTP 200`
