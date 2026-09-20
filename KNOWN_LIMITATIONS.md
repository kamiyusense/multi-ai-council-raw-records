# Known Limitations

- **No Live Execution**: The `live` transport mode is strictly prohibited and heavily guarded.
- **Exactly-Once Delivery**: Cannot be fully guaranteed programmatically; manual intervention might be required if state ends in `UNKNOWN`.
