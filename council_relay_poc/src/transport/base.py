class Transport:
    def __init__(self):
        pass

    def send(self, payload):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError
