# Validated Method Fast Path

**Date:** 2026-07-29

## Decision

Treat one unambiguous, tested or validated reusable method as the direct execution path for a recurring exact read-only task. Do not repeat catalog discovery, broad research, or a proposal step before executing that method.

## Reason

The repository is intended to improve speed and specificity through use. Re-deriving already validated work adds latency without improving quality when target, platform, scope, and parameters are already clear.

## Guardrails

- Use deeper reasoning when the method is missing, ambiguous, stale, parameter-incomplete, risky, or fails.
- Empty answered results are valid no-hits, not retry triggers.
- Make only clear, bounded, same-scope corrective retries after classifying a real error.
- State-changing actions always require explicit approval, one narrow target, preconditions, and independent verification.
- Store only approved, sanitized method knowledge; never store raw endpoint evidence, identifiers, credentials, tenant data, or user-specific results.

## Scope

This applies to every project skill that has a reusable operational method. Skills without a safe durable-memory use case must explicitly keep their work task-local.
