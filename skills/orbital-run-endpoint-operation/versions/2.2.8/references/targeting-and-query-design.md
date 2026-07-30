# Targeting And Query Design

Use this reference for queries outside the fast path, unfamiliar tables, broad scope, platform-sensitive work, or expensive investigation logic.

## Select Targets

Use documented selectors such as `host:NAME`, `hostname:NAME`, `orb:ID`, `amp:GUID`, `cm:GUID`, `ip:ADDRESS`, `ipv4:PATTERN`, `netmask:CIDR`, `machine:ID`, `os:PLATFORM`, `random:COUNT`, and `queryId:ID`.

- Treat `queryId` as a target selector, never as an Orbital Job ID.
- Treat `os` as adding devices to the target set. Treat `allowOS` as filtering returned results after target selection. Do not describe both as generic operating-system filters.
- Use either `allowOS:PLATFORM` in `nodes` or `--allow-os PLATFORM`, never both.
- Do not combine `all` with another selector or `allowOS`.
- Treat `host:` and `hostname:` wildcards as potentially multi-device. A trailing wildcard is narrow only when the literal hostname stem has at least four characters and contains no other wildcard.

Require explicit user approval and `--approve-broad-target` for broad target scope. Never infer it from words such as "any", "online", "all", or "every". The sole automatic exception is the endpoint-operation skill's hostname-resolution fallback: after `host:NAME` returns zero answered endpoints without an API or endpoint query error, it may retry `host:NAME%` with `--approve-broad-target`. The fallback can return multiple endpoints and must never silently select one.

When a hostname selector returns exactly one endpoint, its response `nodeId` is the Orbital ID for `orb:NODE_ID`. Re-submit the requested read-only SQL to that stable selector before treating it as the final single-device result. When a selector returns multiple endpoints, show all host results and request device-definition clarification rather than choosing a node ID.

## Design Queries

Validate table names and columns against the upstream osquery schema when it is locally available. Then verify Orbital availability, operating-system requirements, constraints, and expected endpoint cost. In the Orbital project, use `product-context/osquery/osquery_schema_5_23_0.json`; outside that project, do not spend time searching for this relative path.

Use query-method memory and catalog context when the investigation logic should be repeatable, when a catalog query may already implement it, or when a table requires product-specific interpretation. Prefer specific columns and a `LIMIT` for exploration. Avoid `SELECT *` on broad or expensive tables unless the user explicitly requests it.

Before submitting a non-fast-path query, show the exact SQL, target list, execution profile, and any relevant `os` or `allowOS` behavior whenever approval or safety depends on them.
