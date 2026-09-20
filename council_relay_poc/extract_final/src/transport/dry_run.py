from .base import Transport

class DryRunTransport(Transport):
    def send(self, payload):
        return {"result": "dry_run_success"}

    def start(self):
        pass
