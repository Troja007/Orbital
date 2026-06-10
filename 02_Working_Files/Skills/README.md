# Project Skills

Project skill working copies live here.

Decision from 2026-06-10:

- Keep Orbital skills separated by responsibility.
- Larger skill scope changes require explicit user confirmation before implementation.
- Use a separate skill for Orbital API access and catalog context.
- Use a separate skill for running live osquery queries against endpoints.
- Use a separate skill for reusable Orbital query-method memory that stores how to query and when to use which query, not endpoint results.
- For query work, chain the skills when relevant: query-method memory for design and reuse, API access for fresh catalog/API context, live-query execution for explicit target runs, then query-method memory again for method-only lessons and catalog enrichment.
