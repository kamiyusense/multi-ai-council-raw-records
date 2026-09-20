import json

BLOCKED_FIELDS = {
    "model", "modelProvider", "serviceTier", "reasoning", "reasoning_effort",
    "reasoningEffort", "effort", "thinking", "approvalPolicy", "approvalsReviewer",
    "sandbox", "sandboxPolicy", "cwd", "config", "baseInstructions",
    "developerInstructions", "general instructions", "personality", "disabledPluginIds"
}

ALLOWED_FIELDS_TURN_START = {
    "clientUserMessageId", "input", "threadId"
}

def check_overrides(payload):
    if "params" in payload:
        params = payload["params"]

        # Check explicit nulls and unknown fields
        if payload.get("method") == "turn/start":
             for key, value in params.items():
                 if key in BLOCKED_FIELDS:
                     return False, "OVERRIDE_PRESENT"
                 if value is None:
                     return False, "OVERRIDE_PRESENT" # Explicit null block
                 if key not in ALLOWED_FIELDS_TURN_START:
                     return False, "UNRECOGNIZED_LIVE_FIELD"

    return True, None
