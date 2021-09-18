import pickle
import socket
import threading
from pyngrok import ngrok


class Server:
    LISTEN_QUEUE = 10
    RECV_BUFFER = 11264
    PORT = 50000

    def __init__(self, auth_token):
        self.socket = socket.socket()
        self.socket.bind(("127.0.0.1", self.PORT))

        ngrok.set_auth_token(auth_token)
        self.tunnel = ngrok.connect(self.PORT, "tcp")
        print("JOIN CODE: ", self.tunnel.public_url.replace("tcp://", ""))

        self.clients = []
        self.chat_log = []

        self.start()

    def start(self):
        print(f">>> STARTING SERVER@{self.PORT}")
        client_accept_loop = threading.Thread(target=self.client_accept_loop)
        client_accept_loop.start()

    def client_accept_loop(self):
        print(">>> CLIENT ACCEPT LOOP STARTED")
        self.socket.listen(self.LISTEN_QUEUE)
        while True:
            client = ClientSocket(self, *self.socket.accept())
            self.on_new_client(client)  # EVENT CALLBACK

    ######################################################################################
    # EVENTS #############################################################################
    def on_new_client(self, client):
        print(f"\n>>> NEW CLIENT -> {client.display_name}@{client.ip}:{client.port}")
        self.clients.append(client)
        receive_loop = threading.Thread(target=client.receive_loop)
        receive_loop.start()
        print(">>> STARTED NEW CLIENT'S RECEIVE LOOP")

    def on_new_msg(self, msg_data):
        print("\n>>> NEW MESSAGE -> [{}] {}: {}".format(*msg_data))
        self.chat_log.append(msg_data)
        for client in self.clients:  # RELAY CHAT TO ALL CLIENT(s)
            client.pickle_and_send(msg_data)

    def on_client_disconnect(self, client):
        print(f">>> CLIENT DISCONNECTED -> {client.display_name}@{client.ip}:{client.port}")
        self.clients.remove(client)
        del client


class ClientSocket:
    def __init__(self, server: Server, connection, address):
        self.server = server
        self.connection = connection
        self.ip, self.port = address

        self.display_name = self.connection.recv(self.server.RECV_BUFFER).decode()

    def pickle_and_send(self, data):
        serialized_data = pickle.dumps(data)
        self.connection.sendall(serialized_data)

    def receive_loop(self):
        while True:
            msg_data = self.connection.recv(self.server.RECV_BUFFER)
            if msg_data:
                msg_data = pickle.loads(msg_data)
                self.server.on_new_msg(msg_data)  # EVENT CALLBACK
            else:
                self.connection.close()
                self.server.on_client_disconnect(self)
                break


if __name__ == '__main__':
    Server()
