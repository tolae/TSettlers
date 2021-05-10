import socket
from time import sleep

from messages import MessageFactory


class QServer:
    def __init__(self, host, port):
        self.socket = None
        self.conn = None
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.socket = s
            self.socket.bind((self.host, self.port))
            print("Bound and listening...")
            self.socket.listen()
            self.conn, addr = self.socket.accept()
            with self.conn:
                print('Connected by', addr)
                sleep(3)
                while True:
                    length = int.from_bytes(self.conn.recv(2), byteorder='big', signed=False)
                    message = MessageFactory.build({'length': length,
                                                    'type': int.from_bytes(
                                                        self.conn.recv(1),
                                                        byteorder='big',
                                                        signed=False
                                                    ),
                                                    'data': self.conn.recv(length)
                                                    })
                    print("Received: " + message.__str__())
                    self._handle_msg(message)

    def _handle_msg(self, msg):
        if msg.type() == MessageFactory.KEEP_ALIVE:
            pass # TODO: Keep track of keep alive intervals for death
        elif msg.type() == MessageFactory.END_OF_GAME:
            pass # TODO: Complete episode of training
        elif msg.type() == MessageFactory.UNKNOWN:
            print("Warning: Unknown message received! Ignoring...")
        elif msg.type() == MessageFactory.RESOURCE_SET:
            pass # TODO: Archive resource set
        elif msg.type() == MessageFactory.RESOURCE_PROD:
            pass # TODO: Archive resource production
        elif msg.type() == MessageFactory.ITEMS:
            pass # TODO: Archive items of our player and opponents
        elif msg.type() == MessageFactory.PLAN:
            package = {
                'type': msg.type(),
                'length': msg.length(),
                'data': 4,
            }
            msgToSend = MessageFactory.build(package)
            self.conn.sendall(MessageFactory.to_bytearray(msgToSend))
