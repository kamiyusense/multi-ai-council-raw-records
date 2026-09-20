# Council Relay POC v1.2 - Jules Rebuild

Council Relay POC v1.2.
This rebuild ensures strict static implementation of the Council Relay to connect between ChatGPT Work and Sol, safely handling JSON-RPC communication via stdio for live transports, without actually executing live tasks.

## Status
- **Live Mode**: DISABLED by default.
- **Transports**: `mock`, `dry-run`, `prepare-live` are available. `live` is strictly guarded and inherently blocked for this iteration.

## Schema
- Aligned with Codex app-server API.
- Rejects explicit nulls and any unknown/override fields to ensure safe transmission across all known methods (`turn/start`, `thread/start`, `thread/resume`, `thread/read`, `thread/turns/list`).

## Features
- **Ledger**: SQLite-based ledger enforcing uniqueness, preventing duplication or hash conflicts, and storing runner provenance (`cwd`, `config_path`, `runner_sha256`, etc.).
- **State Machine**: Strict monotonically advancing states: `RESERVED`, `PREFLIGHT_OK`, `SENT`, `COMPLETED`, `DELIVERED`. `UNKNOWN`, `FAILED`, and `BLOCKED` states are also handled. No backward transitions.
- **Correlation**: Strict backend readback correlation requires matching ID across `turn/completed`, `thread/read`, `thread/turns/list`, and `clientUserMessageId` before final `DELIVERED` status.
- **No Automatic Retry**: Enforces exactly-once intention but doesn't assert it blindly. Stops on failure.
- **Approval Request Fail-Closed**: Automatically halts and requests human intervention upon receiving approval requests.
