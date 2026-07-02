# 2026-07-02 GitHub Memory Boundary

## Decision

Share memory, knowledge, context, source snapshots, reusable methods, sanitized result profiles, and installable skills through GitHub. Do not share raw endpoint evidence or local operational data through GitHub.

## Scope

GitHub-synced content may include:

- project and product context
- osquery schema snapshots
- Cisco-managed catalog source snapshots
- offline stock catalog snapshots
- sanitized catalog result profiles
- custom queries and scripts intentionally saved by the user
- draft query/script files intentionally retained
- query-method memory
- notes, decisions, and summaries
- reusable Codex skills

Local-only content includes:

- credentials and tokens
- local `.env` files
- raw endpoint rows
- hostnames, usernames, IP addresses, GUIDs, tenant identifiers, Job IDs, raw API responses, and customer-identifying values
- local validation run output
- local project and sync logs under `local/`

## Reason

The repository should let another Codex workspace start immediately from prior work while avoiding leakage of sensitive endpoint, tenant, or credential data.

## References

- `AGENTS.md`
- `README.md`
- `.gitignore`
- `local/project-change-log.md`
- `local/sync-activity-log.md`

## Open Risks Or Follow-Up

- Generated and draft artifacts must continue to be reviewed before GitHub sync to avoid accidentally publishing endpoint-specific data.
