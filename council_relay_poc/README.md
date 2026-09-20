# Council Relay POC v1.2.6

This is the Council Relay POC v1.2.6.

## Objective

Create a single canonical runner for the Council Relay, focusing strictly on static verification, ledgering, schema blocking, and preventing live execution.

In v1.2.6: We fixed the SDK signature integration (`CodexConfig(codex_bin=...)`) and corrected terminal states for mock and dry-run execution modes so that they do not falsely report `DELIVERED` but instead land in `SIMULATED_DELIVERED` or `DRY_RUN_COMPLETED`. Tests skip if the real SDK isn't present instead of passing with a dummy fallback.

## Features

- **Ledger:** Strict monotonic state transitions using SQLite (`BEGIN IMMEDIATE`).
- **Safety Blocks:** Overrides (`model`, `thinking`, `reasoning_effort` etc.), explicit nulls, unknown fields.
- **Fail-Closed Approval:** The system fails closed (`APPROVAL_FAIL_CLOSED`).
- **Execution Prevented:** Real live execution is STRICTLY PROHIBITED in this POC (`live_enabled=False`).
- **Terminal State Segregation:** `mock` and `dry-run` modes are structurally prevented from claiming real `DELIVERED` states on the ledger.

## Running Tests

```bash
PYTHONPATH=. pytest tests/
```
