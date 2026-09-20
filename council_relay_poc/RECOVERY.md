# Recovery

In the event of an `UNKNOWN` state:
- Check the SQLite ledger to see where the last action was recorded.
- Review server logs for backend correlation.
- Manual verification of the turn status in the target thread via human review.
- Do NOT perform automatic retries.
