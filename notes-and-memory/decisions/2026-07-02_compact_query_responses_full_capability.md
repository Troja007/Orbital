# Compact Query Responses With Full Capability Use

- Date: 2026-07-02
- Decision: Orbital query interactions should be concise by default, while Codex still uses all relevant project capabilities internally.
- Reason: The user wants short query interactions for speed, but query quality must still benefit from project context, product context, query-method memory, catalog snapshots, catalog result profiles, osquery schema validation, target-safety checks, and skills.
- Default visible output: exact target selector list, query purpose, `orbital_queryID` / Job ID and status when available, compact result summary, key caveat, and whether reusable memory/context should be updated.
- Detail expansion: Show full SQL, full row tables, raw helper output, long reasoning, or detailed source traces only when needed for approval, troubleshooting, safety, or when the user asks.
- Boundary: Concise output does not reduce safety checks, target clarification, schema validation, catalog/memory lookup, result interpretation, or privacy controls.
