

class Processor:

    def __init__(self, out_pipes):
        self.out_pipes = out_pipes

    def process(self, msg):
        pass

    def send(self, msg):
        if msg is not None:
            for p in self.out_pipes:
                p.send(msg)

    def close(self):
        pass
