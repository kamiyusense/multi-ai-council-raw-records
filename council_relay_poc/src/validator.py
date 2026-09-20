import json

BLOCKED_FIELDS = {
    "model", "modelProvider", "serviceTier", "reasoning", "reasoning_effort",
    "reasoningEffort", "effort", "thinking", "approvalPolicy", "approvalsReviewer",
    "sandbox", "sandboxPolicy", "cwd", "config", "baseInstructions",
    "developerInstructions", "general instructions", "personality", "disabledPluginIds"
}

ALLOWED_FIELDS = {
    "turn/start": {"clientUserMessageId", "input", "threadId"},
    "thread/start": set(),
    "thread/resume": {"threadId"},
    "thread/read": {"threadId"},
    "thread/turns/list": {"itemsView", "threadId"}
}

def check_overrides(payload):
    method = payload.get("method")

    if "params" in payload and method in ALLOWED_FIELDS:
        params = payload["params"]
        allowed = ALLOWED_FIELDS[method]

        for key, value in params.items():
            if key in BLOCKED_FIELDS:
                return False, "OVERRIDE_PRESENT"
            if value is None:
                return False, "OVERRIDE_PRESENT" # Explicit null block
            if key not in allowed:
                return False, "UNRECOGNIZED_LIVE_FIELD"

    return True, None
