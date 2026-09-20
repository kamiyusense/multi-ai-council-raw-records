from .base import Transport

class DryRunTransport(Transport):
    def __init__(self, config=None):
        self.config = config or {}

    def start(self):
        pass

    def send(self, payload):
        return {"result": {"dry_run": True, "status": "DRY_RUN_COMPLETED"}}

    def shutdown(self):
        pass
