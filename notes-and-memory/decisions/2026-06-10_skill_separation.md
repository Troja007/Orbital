# 2026-06-10 Skill Separation

## Decision

Keep Orbital skills separated by responsibility.

## Scope

- `orbital-api-access`: API connectivity, authentication flow, network/sandbox checks, catalog download/import, and catalog context locations.
- `orbital-run-endpoint-operation`: shared endpoint-operation boundary. Its implemented query mode performs live or scheduled osquery execution against explicit endpoint targets, including SQL/table validation, target selector validation, and result parsing. Future script mode uses a separate API adapter and retains script-specific safety review.
- Additional capabilities should become separate skills when they introduce a different workflow or safety model.

## Change Control

Larger changes to skill scope, trigger behavior, bundled helper scripts, or cross-skill responsibilities require explicit user confirmation before implementation.

## Reason

Keeping API/catalog work, method design, and endpoint execution distinct makes behavior easier to predict. The endpoint-operation skill can share target, ORG, ledger, and error rules between query and script modes without conflating their API paths or safety checks.

## References

- User instruction on 2026-06-10: keep skills separated and require confirmation for bigger skill changes.
- `skills/README.md`
