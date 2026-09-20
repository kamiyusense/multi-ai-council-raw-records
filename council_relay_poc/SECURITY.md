# Security and Safety

- **No Overrides**: All requests attempting to override core model functionality (e.g., `model`, `reasoningEffort`) are immediately blocked (`OVERRIDE_PRESENT`).
- **Fail-Closed on Approval**: Any approval routing will pause operation (`fail-closed`), awaiting explicit manual human authorization.
- **No Retries**: Retries are explicitly prohibited. Failures land in an `UNKNOWN` or `FAILED` state to prevent duplicate/accidental action invocation.
- **Strict Provenance**: Runner execution is strictly bound to its expected SHA256 sum and path.
