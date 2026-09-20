# Design Document

## Core Components
- **Transport**: Abstractions allowing safe `mock`, `dry-run`, and `prepare-live` evaluations.
- **Runner**: The single entrypoint handling the state machine, provenance checks, and payload dispatch.
- **Ledger**: A SQLite-backed record preserving transaction history and enforcing data integrity across transactions.

## State Transitions
```
RESERVED -> PREFLIGHT_OK -> SENT -> COMPLETED -> DELIVERED
```
Abnormal states: `BLOCKED`, `UNKNOWN`, `FAILED`
Transitions are strictly forward-only.

## Integrity Checks
- **Runner Provenance**: Validates runner executable path and hash before allowing operations.
- **Override Blocking**: Detects and rejects any attempt to override internal model/reasoning parameters.
