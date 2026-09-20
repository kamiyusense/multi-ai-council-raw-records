import pytest
import os
import json
from runner import Runner

def get_base_payload():
    return {"method": "turn/start", "params": {"clientUserMessageId": "msg123", "input": [{"text": "Hello", "type": "text"}], "threadId": "thread_mock"}}

def test_runner_mock_terminal_state():
    config = {
        "live_enabled": False,
        "runner_expected_path": os.path.abspath("runner.py"),
        "runner_expected_sha256": "mock_hash",
        "artifact_version": "v1.2",
        "target_allowlist": ["thread_mock"],
        "db_path": "test_mock.db"
    }

    with open("runner.py", "rb") as f:
        import hashlib
        config["runner_expected_sha256"] = hashlib.sha256(f.read()).hexdigest()

    with open("test_config.json", "w") as f:
        json.dump(config, f)

    if os.path.exists("test_mock.db"): os.remove("test_mock.db")

    runner = Runner("test_config.json", "mock")
    state, msg = runner.execute(get_base_payload(), "t1", 1, "thread_mock")

    assert state == "SIMULATED_DELIVERED"

    if os.path.exists("test_mock.db"): os.remove("test_mock.db")

def test_runner_dry_run_terminal_state():
    config = {
        "live_enabled": False,
        "runner_expected_path": os.path.abspath("runner.py"),
        "runner_expected_sha256": "mock_hash",
        "artifact_version": "v1.2",
        "target_allowlist": ["thread_mock"],
        "db_path": "test_dry.db"
    }

    with open("runner.py", "rb") as f:
        import hashlib
        config["runner_expected_sha256"] = hashlib.sha256(f.read()).hexdigest()

    with open("test_config.json", "w") as f:
        json.dump(config, f)

    if os.path.exists("test_dry.db"): os.remove("test_dry.db")

    runner = Runner("test_config.json", "dry-run")
    state, msg = runner.execute(get_base_payload(), "t2", 1, "thread_mock")

    assert state == "DRY_RUN_COMPLETED"

    if os.path.exists("test_dry.db"): os.remove("test_dry.db")
