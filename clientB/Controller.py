import json
import pickle
import socket
import UDPClient
import View
import rsa
import time
import base64
import asyncio

class Controller:
    def __init__(self):
        self.ipServer, self.portServer = self.readInfoServer()
        self.ipClient, self.portClient = self.getIpPortClient()
        self.portServer, self.portClient = int(self.portServer), int(self.portClient)
        self.infoClient = self.getInfoClient()
        self.lastData = ""
        self.priKey = ""
        self.pubKey = ""
        self.client = UDPClient.UDPClient(self.ipServer, self.portServer, self.ipClient, self.portClient)

    # Función para leer la información del servidor desde un archivo JSON
    def readInfoServer(self):
        with open('../infoServer.json', 'r') as file:
            data = json.load(file)
        return [data['ipServer'], data['portServer']]

    # Función para obtener la IP y el puerto del cliente
    def getIpPortClient(self):
        ipClient = "127.0.0.1"
        portClient = 7000
        return [ipClient, portClient]

    # Función para crear un JSON
    def createJson(self, method, nameData, data):
        jsonData = {
            "method": method,
            nameData: data
        }
        print(jsonData)
        jsonString = json.dumps(jsonData)
        return jsonString.encode('utf-8')

    # Función para obtener la información del cliente desde un archivo JSON
    def getInfoClient(self):
        try:
            with open("./infoClient.json", 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error on file infoClient: {e}")
            data = {
                "id": "0",
                "name": "",
                "phone": "",
                "timeCreation": "",
                "friends": {},
                "groups": {},
                "privateKey": "",
                "publicKey": ""
            }
            with open("./infoClient.json", 'w') as file:
                json.dump(data, file, indent=4)
        return data

    def register(self, view, id):
        data = self.createJson("register", "", "")
        self.client.send_data(data) 
        time.sleep(0.5)
        response = view.show(self.client.lastData)
        
        # Crear nuevo JSON con los datos proporcionados por el usuario
        jsonData = self.createJson("register", "data", response)
        self.client.send_data(jsonData)
        
        # Bucle por si no esta registrado
        while id == "-1":
            time.sleep(0.1)
            id = self.client.lastData.get('id', "-1")
            
        with open("./infoClient.json", 'r') as file:
            data = json.load(file)
        
        # Actualizar los datos con la nueva información
        data['id'] = response.get("id")
        data['name'] = response.get("name")
        data['phone'] = response.get("phone")
        data['timeCreation'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        # Generación de llaves RSA
        private_key, public_key = rsa.newkeys(512)

        # Guardar la llave privada en un archivo
        with open('./privKeyUser.txt', 'wb') as file_pri:
            pickle.dump(private_key, file_pri)

        # Guardar la llave pública en un archivo
        with open('./pubKeyUser.txt', 'wb') as file_pub:
            pickle.dump(public_key, file_pub)
        
        # Sobrescribir el archivo con los datos actualizados
        with open("./infoClient.json", 'w') as file:
            json.dump(data, file, indent=4)

        # Actualizar self.infoClient para reflejar los nuevos datos
        self.infoClient = data
        
    def login(self, view, id):
        while True:
            # Primer Menu
            time.sleep(0.1)
            jsonData = self.createJson('login','','')
            self.client.send_data(jsonData)
            
            time.sleep(0.1)
            responseTopic = view.show_menu(self.client.lastData)
            if responseTopic == '1':
                jsonData = self.createJson("getMenuFunc", "id", id)
                self.client.send_data(jsonData)
                time.sleep(0.1)
                response = view.show_menu(self.client.lastData)
                # Users
                if response == '1':
                    # Delete
                    response = "deleteUser"
                    jsonData = self.createJson("log_in", "option", response)
                    self.client.send_data(jsonData)
                    with open("./infoClient.json", 'r') as file:
                        data = json.load(file)

                    # Actualizar los datos con la nueva información
                    data['id'] = '-1'
                    data['name'] = ""
                    data['phone'] = ""
                    data['timeCreation'] = ""

                    # Sobrescribir el archivo con los datos actualizados
                    with open("./infoClient.json", 'w') as file:
                        json.dump(data, file, indent=4)

                    # Actualizar self.infoClient para reflejar los nuevos datos
                    self.infoClient = data
                if response == '2':
                    jsonData = self.createJson("updateUser", "id", self.infoClient.get('id'))
                    self.client.send_data(jsonData)
                    
                    time.sleep(0.1)
                    responseNameOrPhone = view.show_menu(self.client.lastData)  # Name or phone
                    jsonData = self.createJson("updateUser", "option", responseNameOrPhone)
                    self.client.send_data(jsonData)

                    time.sleep(0.1)
                    responseChange = view.show_menu(self.client.lastData)  # Change
                    jsonData = self.createJson("updateUser", "option", responseChange)
                    self.client.send_data(jsonData)

                    time.sleep(0.1)
                    if self.client.lastData.get('answer') == "200 OK":
                        print(2)
                        if responseNameOrPhone == '1':
                            with open("./infoClient.json", 'r') as file:
                                data = json.load(file)

                            # Actualizar los datos con la nueva información
                            data['name'] = responseChange

                            # Sobrescribir el archivo con los datos actualizados
                            with open("./infoClient.json", 'w') as file:
                                json.dump(data, file, indent=4)

                            # Actualizar self.infoClient para reflejar los nuevos datos
                            self.infoClient = data

                        if responseNameOrPhone == '2':
                            with open("./infoClient.json", 'r') as file:
                                data = json.load(file)

                            # Actualizar los datos con la nueva información
                            data['phone'] = responseChange

                            # Sobrescribir el archivo con los datos actualizados
                            with open("./infoClient.json", 'w') as file:
                                json.dump(data, file, indent=4)

                            # Actualizar self.infoClient para reflejar los nuevos datos
                            self.infoClient = data
                if response == '3':
                    jsonData = self.createJson("messageUser", "", "")
                    self.client.send_data(jsonData)
                    
                    time.sleep(0.1)
                    response = view.show_menu(self.client.lastData)  # Name or phone
                    jsonData = self.createJson("messageUser", "IP", response)
                    self.client.send_data(jsonData)

                    time.sleep(0.1)
                    response = view.show_menu(self.client.lastData) 
                    jsonData = self.createJson("messageUser", "PORT", response)
                    self.client.send_data(jsonData)

                    self.readKeys()
                    time.sleep(1)
                    msg = False
                    while True:
                        # Verificar si hay nuevos datos recibidos
                        if self.client.isMsg:
                            # Separar el mensaje cifrado del teléfono
                            msg = self.client.lastData
                            print(msg, 1)
                            print(msg, 1)
                            # Cargar la llave pública del archivo <phone>KeyPublic.txt
                            public_key = self.loadPublicKey(id)

                            if public_key and msg:
                                msg_encrypt, id = msg.split("|||")
                                print(msg_encrypt, id)
                                # Descifrar el mensaje usando la llave pública correspondiente
                                decrypted_msg = rsa.decrypt(encrypted_msg, public_key)
                                view.showMsg(decrypted_msg.decode('utf-8'))  # Mostrar el mensaje descifrado
                            else:
                                print(f"Error: No se encontró la llave pública para el teléfono {id}")

                        msg = view.showMsgToUser() 
                        encrypted_msg = rsa.encrypt(msg.encode('utf-8'), self.priKey) 

                        self.client.send_data(encrypted_msg + b"|||" + self.infoClient.get('id').encode('utf-8'))
                if response == '4':
                    jsonData = self.createJson("readDataUser", "id", self.infoClient.get('id'))
                    self.client.send_data(jsonData)
                    time.sleep(0.1)
                    view.showInfo(self.client.lastData)

            if responseTopic == '2':
                if response == '1':
                    response = "deleteGroup"
                    jsonData = self.createJson("log_in", "option", response)
                    self.client.send_data(jsonData)
                    responseIDG = view.show_menu(self.client.lastData)
                    jsonData = self.createJson("log_in", "id", responseIDG)
                    self.client.send_data(jsonData)
                    print(self.client.lastData.get('answer'))
                if response == '2':
                    response = "updateGroup"
                    jsonData = self.createJson("log_in", "option", response)
                    self.client.send_data(jsonData)
                    responseIDG = view.show_menu(self.client.lastData)
                    jsonData = self.createJson("log_in", "name", responseIDG)
                    self.client.send_data(jsonData)
                    print(self.client.lastData.get('answer'))

                if response == '3':
                    response = "createGroup"
                    jsonData = self.createJson("log_in", "option", response)
                    self.client.send_data(jsonData)
                    responseIDG = view.show_menu(self.client.lastData)
                    jsonData = self.createJson("log_in", "id", responseIDG)
                    self.client.send_data(jsonData)
                    print(self.client.lastData.get('answer'))

                if response == '4':
                    response = "readGroup"
                    jsonData = self.createJson("log_in", "option", response)
                    self.client.send_data(jsonData)
                    
            if responseTopic == '3':
                # Segundo Menu
                jsonData = self.createJson("getMenuFunc3Table", "id", id)
                self.client.send_data(jsonData)

                # Segundo Menu
                time.sleep(0.5)
                response = view.show_menu(self.client.lastData)
                if response == '1':
                    jsonData = self.createJson("deleteFriend", "id", id)
                    self.client.send_data(jsonData)
                    responseID = view.show_menu(self.client.lastData)
                    jsonData = self.createJson("log_in", "id", responseID)
                    self.client.send_data(jsonData)
                    print(self.client.lastData.get('answer'))
                if response == '2':
                    jsonData = self.createJson("updateFriend", "id", id)
                    self.client.send_data(jsonData)
                    responseID = view.show_menu(self.client.lastData)
                    jsonData = self.createJson("log_in", "id", responseID)
                    self.client.send_data(jsonData)
                    responseMessg= view.show_menu(self.client.lastData)
                    jsonData = self.createJson("log_in", "change", responseMessg)
                    self.client.send_data(jsonData)

                    print(self.client.lastData.get('answer'))

                if response == '3':  ## revisar con el controller
                    jsonData = self.createJson("createFriend", "id", id)
                    self.client.send_data(jsonData)

                    responseIDG = view.show(self.client.lastData)
                    jsonData = self.createJson("createFriend", "id_relationship", responseIDG)
                    self.client.send_data(jsonData)

                    responseN = view.show(self.client.lastData)
                    jsonData = self.createJson("createFriend", "id_friend", responseN)
                    self.client.send_data(jsonData)
                    
                    time.sleep(0.1)
                    with open('infoClient.json', 'r') as file:
                        data = json.load(file)
                        
                    # Crear un nuevo ID para el nuevo amigo (por ejemplo, usar el "id" como clave)
                    friend_id = self.client.lastData.get("id")
                    
                    # Agregar el nuevo amigo al diccionario de "friends"
                    data["friends"][friend_id] = self.client.lastData

                    # Guardar de nuevo los cambios en el archivo
                    with open('infoClient.json', 'w') as file:
                        json.dump(data, file, indent=4)
                if response == '4':
                    jsonData = self.createJson("readFriend", "id", id)
                    self.client.send_data(jsonData)

                    responseF = view.show(self.client.lastData)
                    jsonData = self.createJson("log_in", "id_relationship", responseF)
                    self.client.send_data(jsonData)


    def loadPublicKey(self, id):
        """Función para cargar la llave pública del archivo <id>KeyPublic.txt."""
        try:
            with open(f'./{id}KeyPublic.txt', 'rb') as file_pub:
                public_key = pickle.load(file_pub)
                return public_key
        except FileNotFoundError:
            print(f"No se encontró el archivo de la llave pública para {id}")
            return None
    
    # Método principal que controla la conexión y procesamiento de datos
    def readKeys(self):
        file_pri_c = open('./privKeyUser.txt', 'rb')
        self.priKey = pickle.load(file_pri_c)
        file_pri_c.close()
        
        file_pub_c = open('./pubKeyUser.txt', 'rb')
        self.pubKey = pickle.load(file_pub_c)
        file_pub_c.close()
    
    # Método principal que controla la conexión y procesamiento de datos
    def run(self):
        self.client.start_listening()
        view = View.View()
        
        # Verificar conexión al Servidor
        try:
            self.client.send_data(self.createJson("connection", "", ""))  
            time.sleep(0.1)
            response = self.client.lastData.get("answer", "")
        except:
            self.run()
            return
        
        if response != "200 OK":
            return
        
        id = self.infoClient.get("id", "-1")
        if id == "-1":
            self.register(view, id)
        else:
            self.login(view, id)
        

# Ejecución principal
if __name__ == "__main__":
    controller = Controller()
    controller.run()
    controller.client.close()
