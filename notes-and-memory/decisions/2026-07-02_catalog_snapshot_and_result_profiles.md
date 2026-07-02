# 2026-07-02 Catalog Snapshot And Result Profiles

## Decision

Store the offline Cisco-managed stock catalog snapshot and sanitized catalog result profiles in GitHub.

Use:

- `queries_and_scripts/catalog_snapshot/` for the offline stock catalog JSON snapshot.
- `queries_and_scripts/catalog_result_profiles/` for sanitized expected-result and interpretation profiles.

## Reason

The catalog snapshot supports query/script selection without constantly calling the live Orbital catalog. Catalog result profiles help explain what each query returns, how to read empty responses, what columns are expected, and what assumptions an incident responder can safely make.

## Boundaries

- Stock catalog snapshots are reusable source context.
- Organization catalog exports can contain tenant-specific data and stay local-only unless explicitly sanitized and approved.
- Catalog result profiles must not contain endpoint result rows, hostnames, target selectors, Job IDs, raw API responses, tenant data, credentials, IP addresses, GUIDs, usernames, or customer-identifying values.

## References

- `queries_and_scripts/catalog_snapshot/README.md`
- `queries_and_scripts/catalog_result_profiles/`
- `skills/orbital-catalog-result-profiles/SKILL.md`
- `project-context/Orbital_Query_Catalog_Source_Map.md`

## Open Risks Or Follow-Up

- Refresh catalog snapshots periodically when Cisco releases new catalog content.
- Regenerate result profiles when validation logic or source catalog data materially changes.
