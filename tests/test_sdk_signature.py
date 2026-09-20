import pytest
import inspect
from src.transport.live import LiveAppServerTransport

def test_sdk_signature_real():
    """Verify CodexClient and CodexConfig signatures strictly against real SDK"""
    try:
        from openai_codex.client import CodexClient, CodexConfig
    except ImportError:
        pytest.skip("Real openai_codex SDK is not installed in this environment.")
        return

    # If we get here, the real SDK exists. We must verify exact signatures.
    config_sig = inspect.signature(CodexConfig)

    assert 'codex_bin' in config_sig.parameters, "CodexConfig must have codex_bin parameter"
    assert 'app_server_path' not in config_sig.parameters, "CodexConfig must NOT have app_server_path parameter"

    client_sig = inspect.signature(CodexClient)
    assert 'config' in client_sig.parameters
    assert 'approval_handler' in client_sig.parameters

def test_dry_run_and_mock_terminal_states():
    """Verify that dry-run and mock cannot reach DELIVERED in the ledger"""
    from src.ledger import Ledger
    import os

    db = "test_ledger_states.db"
    if os.path.exists(db): os.remove(db)

    l = Ledger(db)

    # Mock mode
    req1 = l.insert_request("t1", 1, "thread1", "turn/start", "RESERVED", transport_mode="mock")
    l.update_state(req1, "PREFLIGHT_OK")
    l.update_state(req1, "SENT")
    # Trying to go straight to DELIVERED with mock mode
    with pytest.raises(Exception, match="CRITICAL: mode 'mock' cannot reach real DELIVERED"):
        l.update_state(req1, "DELIVERED")

    # The correct mock terminal state
    success = l.update_state(req1, "SIMULATED_DELIVERED")
    assert success is True

    # Dry run mode
    req2 = l.insert_request("t2", 1, "thread1", "turn/start", "RESERVED", transport_mode="dry-run")
    l.update_state(req2, "PREFLIGHT_OK")
    l.update_state(req2, "SENT")
    with pytest.raises(Exception, match="CRITICAL: mode 'dry-run' cannot reach real DELIVERED"):
        l.update_state(req2, "DELIVERED")

    success = l.update_state(req2, "DRY_RUN_COMPLETED")
    assert success is True

    if os.path.exists(db): os.remove(db)
