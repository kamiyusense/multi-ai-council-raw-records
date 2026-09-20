import json

FIXTURES = {
    "initialize": {
        "method": "initialize",
        "params": {}
    },
    "initialized": {
        "method": "initialized",
        "params": {}
    },
    "thread/start": {
        "method": "thread/start",
        "params": {}
    },
    "thread/resume": {
        "method": "thread/resume",
        "params": {"threadId": "thread_123"}
    },
    "thread/read": {
        "method": "thread/read",
        "params": {"threadId": "thread_123"}
    },
    "thread/turns/list": {
        "method": "thread/turns/list",
        "params": {"itemsView": "full", "threadId": "thread_123"}
    },
    "turn/start": {
        "method": "turn/start",
        "params": {
            "clientUserMessageId": "msg_abc",
            "input": [{"text": "test prompt", "type": "text"}],
            "threadId": "thread_123"
        }
    },
    "turn/completed": {
        "method": "turn/completed",
        "params": {
            "turn": {
                "id": "turn_123",
                "status": "completed"
            }
        }
    }
}
