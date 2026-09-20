import pytest
from src.transport.live import LiveAppServerTransport, TransportTimeoutError

def test_live_transport_initialization_no_subprocess():
    """Verify live transport does not manage its own subprocess lifecycle, delegating to CodexClient"""
    transport = LiveAppServerTransport({"live_execution_permitted": False})

    assert transport.independent_subprocess_used is False
    assert transport.client_factory_build_count == 0
    assert transport.is_initialized is False

def test_live_transport_mock_factory():
    import pytest
    transport = LiveAppServerTransport({"live_execution_permitted": False})
    with pytest.raises(Exception, match="SDK_UNAVAILABLE"):
        transport._build_client_factory()
    assert transport.client_factory_build_count == 1

def test_approval_handler_fail_closed():
    transport = LiveAppServerTransport({"live_execution_permitted": False})
    with pytest.raises(Exception, match="APPROVAL_FAIL_CLOSED"):
        transport._approval_handler({})

def test_live_transport_execution_blocked():
    transport = LiveAppServerTransport({"live_execution_permitted": False})
    import pytest
    with pytest.raises(Exception, match="SDK_UNAVAILABLE"):
        transport.start()

def test_live_transport_send_blocked():
    import pytest
    pytest.skip("Cannot reach send without valid SDK and transport.start()")

def test_codex_import_signature():
    # If openai_codex is mock installed in pytest env, test import, otherwise dummy client handles it
    transport = LiveAppServerTransport()
    transport._lazy_import_sdk()
    # It shouldn't crash

def test_shutdown_lifecycle_delegated():
    transport = LiveAppServerTransport({"live_execution_permitted": False})
    # Attach a mock client
    class MockClient:
        def __init__(self):
            self.closed = False
        def close(self):
            self.closed = True

    transport.client = MockClient()
    transport.shutdown()
    assert transport.client.closed is True

def test_send_timeout_structural():
    transport = LiveAppServerTransport({"live_execution_permitted": True})

    class MockClientWithTimeout:
        def send_request(self, method, params):
            # We want to force a timeout when waiting for turn/completed.
            # To do this cleanly, we can override the event wait just for this test
            return {"result": {"turn": {"id": "timeout_turn"}}}

    # Subclass just to mock the handle completed which signals the event
    class TimeoutLiveAppServerTransport(LiveAppServerTransport):
        def _handle_turn_completed_simulation(self, turn_id):
            # DO NOT set the event, causing a timeout!
            pass

    transport = TimeoutLiveAppServerTransport({"live_execution_permitted": True})
    transport.client = MockClientWithTimeout()
    transport._rpc_timeout = 0.01  # Very fast timeout

    # Send turn/start, it will try to wait for completion but timeout
    with pytest.raises(TransportTimeoutError, match="Timeout waiting for turn/completed notification"):
        transport.send({"method": "turn/start", "params": {"clientUserMessageId": "msg123", "threadId": "th123"}})
