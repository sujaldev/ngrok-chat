import pickle
import socket

from server import Server
from client import Client


def get_auth_token():
    try:
        with open("auth.token", "rb") as auth_file:
            return pickle.load(auth_file)
    except FileNotFoundError:
        with open("auth.token", "wb") as auth_file:
            token = input("Enter your ngrok auth token: ")
            pickle.dump(token, auth_file)
            return token


def host():
    token = get_auth_token()
    Server(token)


def join():
    tunnel_url = input("Enter joining code: ").split(":")
    host_ip = socket.gethostbyname(tunnel_url[0])
    host_port = int(tunnel_url[1])
    server = (host_ip, host_port)

    client_name = input("Enter your display name: ")

    Client(server, client_name)


def main():
    print("Welcome to ngrok chat, let's begin:",
          "Do you want to host a server or join a server?",
          "\t1: Host",
          "\t2: Join", sep="\n")
    choice = input(">>> ")
    if choice == "1":
        host()
    elif choice == "2":
        join()
    else:
        print("No such choice, exiting...")


if __name__ == '__main__':
    main()
