# Council Relay POC v1.2.5

This is the Council Relay POC v1.2.5 rebuild.

## Objective

Create a single canonical runner for the Council Relay, focusing strictly on static verification, ledgering, schema blocking (overrides, nulls, unhandled), and preventing live execution.

In v1.2.5: We have strictly integrated the `openai_codex.client.CodexClient` interface statically without maintaining duplicate process logic inside the transport.

## Features

- **Ledger:** Strict monotonic state transitions using SQLite (`BEGIN IMMEDIATE`).
- **Safety Blocks:** Overrides (`model`, `thinking`, `reasoning_effort` etc.), explicit nulls, unknown fields.
- **Fail-Closed Approval:** The system fails closed (`APPROVAL_FAIL_CLOSED`) requiring human intervention if approval requests trigger.
- **Execution Prevented:** Real live execution is STRICTLY PROHIBITED in this POC (`live_enabled=False`).
- **Transport Modes:** Mock, Dry-Run, Prepare-Live.

## Constraints Check

- **Automatic Retries:** None.
- **Double Lifecycle:** None, CodexClient manages `start()`/`close()`.
- **Zip Packaging:** No zips are pushed to git.

## Running Tests

```bash
pytest tests/
```
