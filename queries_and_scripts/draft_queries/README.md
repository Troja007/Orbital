# Query Drafts

Working area for query drafts, test variants, validation queries, adapted catalog queries, and investigation-specific SQL that should live near the query/script source tree but is not yet promoted to personal reusable custom query work.

Use clear file names that describe platform, purpose, and status where useful, for example:

- `draft_windows_<purpose>.sql`
- `test_windows_<purpose>.sql`
- `validation_cross_platform_<purpose>.sql`

Do not store raw endpoint results, hostnames, usernames, IP addresses, GUIDs, tenant identifiers, Job IDs, or credentials in query files.

Promote a query into `../custom_queries/` only when the user explicitly wants it stored as personal reusable custom query work.
