import sys
import socket
import pickle
import threading
from datetime import datetime


def get_current_time():
    time = datetime.now()
    time = "{}/{}/{} {}:{}".format(time.day, time.month, time.year, time.hour, time.minute)
    return time


class Client:
    RECV_BUFFER = 11264

    def __init__(self, server_address: tuple, display_name: str):
        self.server_address = server_address
        self.display_name = display_name

        self.socket = socket.socket()
        self.socket.connect(self.server_address)

        self.start()

    def start(self):
        receive_loop = threading.Thread(target=self.receive_loop)
        receive_loop.start()
        while True:
            msg_data = pickle.dumps((
                get_current_time(),
                self.display_name,
                input(">>> ")
            ))
            self.socket.sendall(msg_data)

    def receive_loop(self):
        # INTRODUCE YOURSELF TO THE SERVER
        self.socket.sendall(bytes(self.display_name, "UTF8"))

        while True:
            new_msg = self.socket.recv(self.RECV_BUFFER)
            if new_msg:
                new_msg = pickle.loads(new_msg)
                self.on_new_msg(new_msg)
            else:
                print(">>> SERVER OFFLINE... EXITING...")
                self.socket.close()
                self.on_server_close()
                break

    @staticmethod
    def on_new_msg(msg):
        print("\r\n[{}] {}: {}\n>>> ".format(*msg), end="")

    @staticmethod
    def on_server_close():
        sys.exit(1)


if __name__ == '__main__':
    Client(("127.0.0.1", 80), "Elon Musk")
