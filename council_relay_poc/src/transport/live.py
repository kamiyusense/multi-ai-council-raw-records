from .base import Transport

class LiveTransport(Transport):
    def send(self, payload):
        raise Exception("Live execution is STRICTLY PROHIBITED in this POC.")

    def start(self):
        raise Exception("Live execution is STRICTLY PROHIBITED in this POC.")
