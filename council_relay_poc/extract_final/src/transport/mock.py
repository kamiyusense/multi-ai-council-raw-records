from .base import Transport

class MockTransport(Transport):
    def send(self, payload):
        return {"result": "mock_success", "payload_sent": payload}

    def start(self):
        pass
