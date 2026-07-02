# 2026-07-02 Query Method Memory Boundary

## Decision

Use `tools-and-memory/query-method-memory/` as the durable store for reusable query-method knowledge.

Query-method memory stores how to choose, design, validate, target, and interpret queries. It does not store endpoint result rows or endpoint-specific evidence.

## Scope

Query-method records may store:

- investigation input patterns
- threat or behavior context
- catalog `Name` and `ID`
- relevant osquery tables and columns
- SQL patterns and joins
- targeting and platform guidance
- validation status
- caveats and lessons learned

Query-method records must not store:

- endpoint result rows
- hostnames, usernames, IP addresses, MAC addresses, GUIDs, tenant names, customer names, tokens, raw API responses, Job IDs, or raw investigation output

## Reason

This boundary lets endpoint work improve future query quality and speed without turning the repository into a sensitive evidence store.

## References

- `tools-and-memory/query-method-memory/README.md`
- `skills/orbital-query-method-memory/SKILL.md`
- `README.md`
- Git commit `8f2c0f2` (`Rename query methods to query method memory`)

## Open Risks Or Follow-Up

- Method memory needs regular updates after useful validated investigations; otherwise query quality will not improve as intended.
