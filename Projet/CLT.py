import socket
import uuid
import configparser
import time

# Server configuration
SERVER_HOST = '127.0.0.2'  # Change this to the server's IP address
SERVER_PORT = 12345
BUFFER_SIZE = 1024
CLIENT_CONFIG_FILE = "client_config.ini"
IP_CLIENT = None

configFile = configparser.ConfigParser()

def writeFile():
    f = open("myfile.txt", "x")
    f.close()


def setID():
    clientID = str(uuid.uuid4())
    configFile['Client'] = {'ID': clientID}
    try:
        with open(CLIENT_CONFIG_FILE, 'w') as file:
            configFile.write(file)
    except IOError as e:
        print(f"Error writing to configuration file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        print(f"[*] Assigned ID: {clientID}")
    return clientID

def getID():
    try:
        configFile.read(CLIENT_CONFIG_FILE)
        return configFile.get("Client", "ID")
    except (configparser.NoSectionError, configparser.NoOptionError, FileNotFoundError):
        return setID()






def connectionServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while True:
            try:
                s.connect((SERVER_HOST, SERVER_PORT))
                print("Client connected successfully to Server!")
                break
            except ConnectionRefusedError:
                print("Server not available. Retrying in 10 seconds..")
                time.sleep(10)
        
        id = getID().encode()
        s.sendall(b"Hello, server! My ID is "+ id)
        data = s.recv(1024)

    print(f"Received {data!r}")

def main():
    connectionServer()


    #Close the connection
    #client_socket.close()

if __name__ == "__main__":
    main()
