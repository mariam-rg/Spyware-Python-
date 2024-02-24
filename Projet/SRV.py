"""
LIEN GIT : https://github.com/mariam-rg/Spyware-Python-.git
"""

import socket
import threading

# Server configuration
SERVER_HOST = '127.0.0.2'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# Dictionary to store client IDs and connections
CLIENT_FILE_DAY = {}


def receiveFile(data):
    print("Receive a file from a client")


def inputServer(valueToPrint):
    print(f"SERVER > {valueToPrint}")


def manageClient(clientSocket, address):
    print(f"Accepted connection from {address}")

    IPClient = address[0]
    while True:
        data = clientSocket.recv(BUFFER_SIZE)
        receiveFile(data)
        if not data:
            break

        clientSocket.sendall(data)

    clientSocket.close()
    print(f"Connection from ID {IPClient} ({address}) closed.")


def connectClients():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(5)
        print(f"Listening on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            # Accept a new connection from client
            clientSocket, clientAddress = s.accept()

            # Start a new thread to manage client
            threadClient = threading.Thread(target=manageClient, args=(clientSocket, clientAddress))
            threadClient.start()


def main():
    connectClients()

if __name__ == "__main__":
    main()