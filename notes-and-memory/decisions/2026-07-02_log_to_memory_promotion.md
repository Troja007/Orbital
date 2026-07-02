# Promote Local Log Lessons Into GitHub Memory

- Date: 2026-07-02
- Decision: Local logs remain local-only traceability, but reusable lessons from those logs must be promoted into GitHub-synced project memory.
- Reason: `local/project-change-log.md` and `local/sync-activity-log.md` explain what happened in one workspace. They are intentionally ignored by Git and do not help a future Codex workspace imported from GitHub. Reusable learning must therefore be copied, in sanitized form, into the synced artifact that future work will read.
- Promotion targets:
  - Durable project decisions: `notes-and-memory/decisions/`
  - Reusable query methods: `tools-and-memory/query-method-memory/`
  - Durable project context: `project-context/`
  - Durable product context: `product-context/`
  - Catalog result interpretation: `queries_and_scripts/catalog_result_profiles/`
  - Reusable workflow behavior: `skills/`
- Boundary: Do not promote secrets, credentials, endpoint result rows, raw API responses, tenant data, hostnames, IP addresses, GUIDs, usernames, customer names, or customer-identifying values.
- Open risk: A local log entry can still be useful only locally if no follow-up promotion is performed. Future skills and sync work should explicitly check this after local logging.
