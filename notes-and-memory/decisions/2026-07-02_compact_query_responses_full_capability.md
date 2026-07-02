# Compact Traceable Query Responses With Full Capability Use

- Date: 2026-07-02
- Decision: Orbital query interactions should be concise and traceable by default, while Codex still uses all relevant project capabilities internally.
- Reason: The user wants short query interactions for speed, but still needs enough information on screen to know what happened. Query quality must continue to benefit from project context, product context, query-method memory, catalog snapshots, catalog result profiles, osquery schema validation, target-safety checks, and skills.
- Default visible output: exact target selector list, query purpose, execution mode, SQL summary or exact SQL when approval/safety requires it, `orbital_queryID` / Job ID and status when available, answered endpoint count, row count, compact result summary, key caveat, and whether reusable memory/context should be updated.
- Detail expansion: Show full row tables, raw helper output, long reasoning, or detailed source traces only when needed for approval, troubleshooting, safety, or when the user asks.
- Boundary: Concise output does not reduce traceability, safety checks, target clarification, schema validation, catalog/memory lookup, result interpretation, or privacy controls.
