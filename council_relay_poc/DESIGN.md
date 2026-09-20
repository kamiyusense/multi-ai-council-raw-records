# Design Document

## Core Components
- **Transport**: Abstractions allowing safe `mock`, `dry-run`, and `prepare-live` evaluations.
- **Runner**: The single entrypoint handling the state machine, double-gating checks, and payload dispatch.
- **Ledger**: A SQLite-backed record preserving transaction history and enforcing data integrity.
- **Parsers & Validation**: Deep introspection to avoid field overrides and safely confirm successful delivery through backend readback (`thread/read`, `thread/turns/list`, and `turn/completed`).

## State Transitions
```
RESERVED -> PREFLIGHT_OK -> SENT -> COMPLETED -> DELIVERED
```
Abnormal states: `BLOCKED`, `UNKNOWN`, `FAILED`. Transitions are strictly forward-only.

## Integrity Checks
- **Runner Provenance**: Validates runner executable path and hash, recording it alongside runtime metadata.
- **Override Blocking**: Blocks overridden model, reasoning, and system instructions.
- **Double Gate**: Enforces execution block unless `metadata_pass`, `allowlist_pass`, `busy=False`, `live_enabled=True` are met, stopping the runner from unintended side-effects.
