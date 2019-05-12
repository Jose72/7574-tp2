import zmq
import sys
from os import path


class ZMQSocket:

    def __init__(self, s_type):
        self.context = zmq.Context()
        self.socket = self.context.socket(s_type)

    def recv_string(self):
        return self.socket.recv_string()

    def recv_json(self):
        return self.socket.recv_json()

    def send_string(self, msg):
        return self.socket.send_string(msg)

    def send_json(self, msg):
        return self.socket.send_json(msg)

    def close(self):
        return self.socket.close()


class ZMQSocketPullBind(ZMQSocket):

    def __init__(self, address, port):
        super().__init__(zmq.PULL)
        self.socket.bind("tcp://{}:{}".format(address, port))


class ZMQSocketPullCon(ZMQSocket):

    def __init__(self, address, port):
        super().__init__(zmq.PULL)
        self.socket.connect("tcp://{}:{}".format(address, port))


class ZMQSocketPushBind(ZMQSocket):

    def __init__(self, address, port):
        super().__init__(zmq.PUSH)
        self.socket.bind("tcp://{}:{}".format(address, port))


class ZMQSocketPushCon(ZMQSocket):

    def __init__(self, address, port):
        super().__init__(zmq.PUSH)
        self.socket.connect("tcp://{}:{}".format(address, port))


class ZMQSocketReq(ZMQSocket):

    def __init__(self, address, port):
        super().__init__(zmq.REQ)
        self.socket.connect("tcp://{}:{}".format(address, port))


class ZMQSocketRep(ZMQSocket):
    def __init__(self, address, port):
        super().__init__(zmq.REP)
        self.socket.bind("tcp://{}:{}".format(address, port))


class ZMQSocketPub(ZMQSocket):
    def __init__(self, address, port):
        super().__init__(zmq.PUB)
        self.socket.bind("tcp://{}:{}".format(address, port))


class ZMQSocketSus(ZMQSocket):
    def __init__(self, address, port):
        super().__init__(zmq.SUS)
        self.socket.bind("tcp://{}:{}".format(address, port))
