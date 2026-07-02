# 2026-06-10 Skill Separation

## Decision

Keep Orbital skills separated by responsibility.

## Scope

- `orbital-api-access`: API connectivity, authentication flow, network/sandbox checks, catalog download/import, and catalog context locations.
- `orbital-run-osquery-live-query`: live osquery query execution against explicit endpoint targets, including SQL/table validation, target selector validation, and result parsing.
- Additional capabilities should become separate skills when they introduce a different workflow or safety model.

## Change Control

Larger changes to skill scope, trigger behavior, bundled helper scripts, or cross-skill responsibilities require explicit user confirmation before implementation.

## Reason

Keeping skills separated makes behavior easier to predict, avoids one skill becoming too broad, and lets each workflow keep its own safety checks.

## References

- User instruction on 2026-06-10: keep skills separated and require confirmation for bigger skill changes.
- `02_Working_Files/Skills/README.md`
