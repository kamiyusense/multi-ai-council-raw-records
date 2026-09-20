import pytest
import json
import os
import hashlib
import sys
from src.ledger import Ledger
from src.validator import check_overrides
from src.parser import Parsers
from src.fixtures import FIXTURES
from src.transport.live import LiveAppServerTransport
from runner import Runner

def get_hash(filepath):
    from runner import get_file_sha256
    return get_file_sha256(filepath)

def test_canonical_serialization():
    from runner import canonical_json
    data1 = {"b": 2, "a": 1}
    data2 = {"a": 1, "b": 2}
    assert canonical_json(data1) == canonical_json(data2)
    assert canonical_json(data1) == b'{"a":1,"b":2}'

def test_override_omission():
    payload = FIXTURES["turn/start"]
    valid, err = check_overrides(payload)
    assert valid is True
    assert err is None

def test_explicit_null_override_block():
    payload = {
        "method": "turn/start",
        "params": {
            "threadId": "123",
            "input": [{"text": "hello", "type": "text"}],
            "model": None
        }
    }
    valid, err = check_overrides(payload)
    assert valid is False
    assert err == "OVERRIDE_PRESENT"

def test_structured_reasoning_minimal_block():
    payload = {
        "method": "turn/start",
        "params": {
            "threadId": "123",
            "input": [{"text": "hello", "type": "text"}],
            "reasoning_effort": "minimal"
        }
    }
    valid, err = check_overrides(payload)
    assert valid is False
    assert err == "OVERRIDE_PRESENT"

def test_prompt_minimal_no_false_positive():
    payload = {
        "method": "turn/start",
        "params": {
            "threadId": "123",
            "input": [{"text": "use minimal code", "type": "text"}],
            "clientUserMessageId": "abc"
        }
    }
    valid, err = check_overrides(payload)
    assert valid is True
    assert err is None

def test_unknown_live_field_block():
    payload = {
        "method": "turn/start",
        "params": {
            "threadId": "123",
            "input": [{"text": "hello", "type": "text"}],
            "unknown_future_field": "some_value"
        }
    }
    valid, err = check_overrides(payload)
    assert valid is False
    assert err == "UNRECOGNIZED_LIVE_FIELD"

def test_approval_request_fail_closed(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    config = {
        "live_enabled": False,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    payload = {"method": "approval/request", "params": {}}
    r = Runner(str(config_path), "mock")
    status, detail = r.execute(payload, "task1", 1, "thread_123")
    assert status == "BLOCKED"
    assert detail == "APPROVAL_FAIL_CLOSED"

def test_duplicate(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    config = {
        "live_enabled": False,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    payload = {"method": "turn/start", "params": {"threadId": "123", "input": []}}
    r = Runner(str(config_path), "mock")
    status, detail = r.execute(payload, "task1", 1, "thread_123")
    assert status == "DELIVERED"

    status, detail = r.execute(payload, "task1", 1, "thread_123")
    assert status == "DUPLICATE"

def test_message_conflict(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    config = {
        "live_enabled": False,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    payload1 = {"method": "turn/start", "params": {"threadId": "123", "input": [{"text":"a"}]}}
    payload2 = {"method": "turn/start", "params": {"threadId": "123", "input": [{"text":"b"}]}}

    r = Runner(str(config_path), "mock")
    r.execute(payload1, "task1", 1, "thread_123")

    status, detail = r.execute(payload2, "task1", 1, "thread_123")
    assert status == "BLOCKED"
    assert detail == "MESSAGE_HASH_CONFLICT"

def test_runner_path_mismatch(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    config = {
        "live_enabled": False,
        "runner_expected_path": "/fake/path/runner.py",
        "runner_expected_sha256": "fakehash",
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    r = Runner(str(config_path), "mock")
    status, detail = r.execute({}, "task1", 1, "thread_123")
    assert status == "BLOCKED"
    assert detail == "RUNNER_INTEGRITY_MISMATCH"

def test_runner_hash_mismatch(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)

    config = {
        "live_enabled": False,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": "wronghash",
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    r = Runner(str(config_path), "mock")
    status, detail = r.execute({}, "task1", 1, "thread_123")
    assert status == "BLOCKED"
    assert detail == "RUNNER_INTEGRITY_MISMATCH"

def test_live_enabled_false_live_block(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    config = {
        "live_enabled": False,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    r = Runner(str(config_path), "live")
    status, detail = r.execute({"method": "thread/start", "params": {}}, "task1", 1, "thread_123")
    assert status == "BLOCKED"
    assert detail == "LIVE_DISABLED"

def test_allowlist_block(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    config = {
        "live_enabled": True,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_abc"],
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    r = Runner(str(config_path), "mock", live_flag=True)
    status, detail = r.execute({"method": "thread/start", "params": {}}, "task1", 1, "thread_123")
    assert status == "BLOCKED"
    assert detail == "TARGET_NOT_ALLOWED"

def test_metadata_mismatch_block(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    config = {
        "live_enabled": True,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "metadata_pass": False,
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    r = Runner(str(config_path), "mock", live_flag=True)
    status, detail = r.execute({"method": "thread/start", "params": {}}, "task1", 1, "thread_123")
    assert status == "BLOCKED"
    assert detail == "METADATA_MISMATCH"

def test_busy_block(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    config = {
        "live_enabled": True,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "busy": True,
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    r = Runner(str(config_path), "mock", live_flag=True)
    status, detail = r.execute({"method": "thread/start", "params": {}}, "task1", 1, "thread_123")
    assert status == "BLOCKED"
    assert detail == "BUSY"

def test_pre_send_failure_blocked(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    config = {
        "live_enabled": False,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "preflight_fail": True,
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    r = Runner(str(config_path), "mock")
    status, detail = r.execute({"method": "turn/start", "params": {"threadId": "123", "input": []}}, "task1", 1, "thread_123")
    assert status == "BLOCKED"
    assert detail == "PREFLIGHT_FAIL"

def test_crash_after_accepted_unknown(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    config = {
        "live_enabled": False,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "crash_after_send": True,
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    r = Runner(str(config_path), "mock")
    status, detail = r.execute({"method": "turn/start", "params": {"threadId": "123", "input": []}}, "task1", 1, "thread_123")
    assert status == "UNKNOWN"
    assert detail == "CRASH_AFTER_SEND"

def test_completed_readback_fail_unknown(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    config = {
        "live_enabled": False,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "mock_backend_readback_fail": True,
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    r = Runner(str(config_path), "mock")
    status, detail = r.execute({"method": "turn/start", "params": {"threadId": "123", "input": []}}, "task1", 1, "thread_123")
    assert status == "UNKNOWN"
    assert detail == "READBACK_FAIL"

def test_parsers():
    turn_completed = {"method": "turn/completed", "params": {"turn": {"id": "turn_123", "status": "completed"}}}
    thread_read = {"method": "thread/read", "result": {"thread": {"id": "thread_456"}}}
    turns_list = {"method": "thread/turns/list", "result": {"turns": [{"id": "turn_123", "messages": [{"author": {"role": "user"}, "clientId": "client_789"}]}]}}

    assert Parsers.parse_turn_completed(turn_completed) == "turn_123"
    assert Parsers.parse_thread_read(thread_read) == "thread_456"
    assert Parsers.parse_thread_turns_list(turns_list) == "turn_123"

    assert Parsers.correlate_backend(turn_completed, thread_read, turns_list, "client_789") is True
    assert Parsers.correlate_backend(turn_completed, thread_read, turns_list, "wrong_id") is False

    bad_turn_completed = {"method": "turn/completed", "params": {"turn": {"id": "turn_123", "status": "failed"}}}
    assert Parsers.correlate_backend(bad_turn_completed, thread_read, turns_list, "client_789") is False

def test_monotonic_state(tmp_path):
    db_path = tmp_path / "ledger.db"
    ledger = Ledger(str(db_path))
    ok, req_id = ledger.record_reservation("t1", 1, "target", "method", "hash", "client")
    assert ok

    assert ledger.update_state(req_id, "PREFLIGHT_OK") is True
    assert ledger.update_state(req_id, "RESERVED") is False # backward transition blocked
    assert ledger.update_state(req_id, "SENT") is True
    assert ledger.update_state(req_id, "COMPLETED") is True
    assert ledger.update_state(req_id, "DELIVERED") is True
    assert ledger.update_state(req_id, "UNKNOWN") is False # terminal state

def test_lazy_loading(tmp_path):
    if "openai_codex" in sys.modules:
        del sys.modules["openai_codex"]

    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    config = {
        "live_enabled": False,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    payload = {"method": "turn/start", "params": {"threadId": "123", "input": []}}

    # Dry run
    r = Runner(str(config_path), "dry-run")
    r.execute(payload, "task_dry", 1, "thread_123")
    assert not isinstance(getattr(r, 'transport', None), LiveAppServerTransport)
    assert "openai_codex" not in sys.modules

    # Mock
    r = Runner(str(config_path), "mock")
    r.execute(payload, "task_mock", 1, "thread_123")
    assert not isinstance(getattr(r, 'transport', None), LiveAppServerTransport)
    assert "openai_codex" not in sys.modules

    # Prepare Live
    r = Runner(str(config_path), "prepare-live")
    r.execute(payload, "task_prep", 1, "thread_123")
    assert not isinstance(getattr(r, 'transport', None), LiveAppServerTransport)
    assert "openai_codex" not in sys.modules

def test_no_auto_retry(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    config = {
        "live_enabled": False,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "crash_after_send": True,
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    r = Runner(str(config_path), "mock")
    status, detail = r.execute({"method": "turn/start", "params": {"threadId": "123", "input": []}}, "task1", 1, "thread_123")
    assert status == "UNKNOWN"

    # Same task again -> AUTO_RETRY_PROHIBITED
    status, detail = r.execute({"method": "turn/start", "params": {"threadId": "123", "input": []}}, "task1", 1, "thread_123")
    assert status == "BLOCKED"
    assert detail == "AUTO_RETRY_PROHIBITED"

def test_concurrent_reservation(tmp_path):
    db_path = tmp_path / "ledger.db"
    ledger1 = Ledger(str(db_path))
    ledger2 = Ledger(str(db_path))

    ledger1.conn.execute('BEGIN EXCLUSIVE')

    ok, res = ledger2.record_reservation("task1", 1, "thread_123", "turn/start", "hash", "msg1")
    assert not ok
    assert res == "DATABASE_LOCKED"

    ledger1.conn.execute('ROLLBACK')

def test_runner_provenance_logged(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    config = {
        "live_enabled": False,
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.3",
        "target_allowlist": ["thread_123"],
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    payload = {"method": "turn/start", "params": {"threadId": "123", "input": []}}
    r = Runner(str(config_path), "mock")
    r.execute(payload, "task1", 1, "thread_123")

    import sqlite3
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM requests").fetchone()

    assert row["runner_path"] == actual_runner_path
    assert row["runner_sha256"] == actual_hash
    assert row["artifact_version"] == "v1.2.3"
    assert row["cwd"] is not None

def test_live_execution_default_and_blocks(tmp_path):
    config_path = tmp_path / "config.json"
    db_path = tmp_path / "ledger.db"

    import runner
    actual_runner_path = os.path.abspath(runner.__file__)
    actual_hash = get_hash(actual_runner_path)

    # Do not provide live_enabled or live_execution_permitted in config -> defaults to false
    config = {
        "runner_expected_path": actual_runner_path,
        "runner_expected_sha256": actual_hash,
        "artifact_version": "v1.2.4",
        "target_allowlist": ["thread_123"],
        "db_path": str(db_path)
    }
    config_path.write_text(json.dumps(config))

    payload = {"method": "turn/start", "params": {"threadId": "123", "input": []}}

    r = Runner(str(config_path), "live")
    status, detail = r.execute(payload, "task_live", 1, "thread_123")

    assert status == "BLOCKED"
    assert detail == "LIVE_DISABLED"
