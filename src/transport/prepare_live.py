from .base import Transport

class PrepareLiveTransport(Transport):
    def send(self, payload):
        return {"result": "prepare_live_success"}

    def start(self):
        pass
