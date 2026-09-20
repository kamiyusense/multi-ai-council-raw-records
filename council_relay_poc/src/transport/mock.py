from .base import Transport

class MockTransport(Transport):
    def __init__(self, config=None):
        self.config = config or {}

    def start(self):
        pass

    def send(self, payload):
        return {"result": {"mock": True, "status": "SIMULATED_DELIVERED"}}

    def shutdown(self):
        pass
