# Known Method Direct Execution

**Date:** 2026-07-29

## Decision

Use a single unambiguous `tested` or `validated` query-method record as a direct execution route for a read-only Orbital query against one exact target. Do not require catalog discovery, broad research, or a separate proposal step before submitting the stored method.

## Guardrails

- The method must contain executable read-only SQL with no unresolved parameters.
- The target must be one explicit host or hostname selector and the current global ORG mapping must remain selected.
- Draft, deprecated, ambiguous, broad-target, script, and state-changing methods remain outside the direct route.
- Empty results are valid no-hits, not retry triggers.
- For a real failure, classify the error and make at most one same-scope, read-only correction when the repair is clear. Authentication, credential, ORG mapping, and target-scope failures require correction before another submission.

## Rationale

Method memory exists to shorten repeated work. Treating a verified record only as background documentation reintroduces unnecessary planning latency while providing no additional safety for an exact, read-only operation.
