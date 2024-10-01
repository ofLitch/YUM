import json
import pickle
import socket
import UDPClient
import View
import rsa
import time
import base64

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
        jsonData = self.createJson("log_in", "id", id)
        self.client.send_data(jsonData)
        
        # Primer Menu
        time.sleep(0.5)
        responseTopic = view.show_menu(self.client.lastData)
        jsonData = self.createJson("log_in", "option", responseTopic)
        self.client.send_data(jsonData)
        
        # Segundo Menu
        time.sleep(0.5)
        response = view.show_menu(self.client.lastData)
        jsonData = self.createJson("log_in", "option", response)
        self.client.send_data(jsonData)
        
        if responseTopic == '1':
            # Users
            if response == '1':
                # Delete
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
                print(2)
                # Update
                time.sleep(0.5)
                responseNameOrPhone = view.show_menu(self.client.lastData) # Name or phone
                jsonData = self.createJson("log_in", "option", responseNameOrPhone)
                self.client.send_data(jsonData)
                
                time.sleep(0.5)
                responseChange = view.show_menu(self.client.lastData) # Change
                jsonData = self.createJson("log_in", "option", responseChange)
                self.client.send_data(jsonData)
                
                time.sleep(0.5)
                if self.client.lastData == "200 OK":
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
                time.sleep(0.5)
                response = view.show_menu(self.client.lastData) # Name or phone
                jsonData = self.createJson("log_in", "IP", response)
                self.client.send_data(jsonData)
                
                time.sleep(0.5)
                response = view.show_menu(self.client.lastData) # Name or phone
                jsonData = self.createJson("log_in", "PORT", response)
                self.client.send_data(jsonData)
                
                self.readKeys()
                time.sleep(0.1)
                if  self.client.lastData.get('answer') == "200 OK":
                    view.showMsg("Connection success")
                    while  True:
                        msg = view.showMsgToUser()
                        print(msg, 1)
                        msg = rsa.encrypt(msg.encode('utf-8'), self.priKey)
                        print(msg)
                        self.client.send_data(msg)

            #if response == '4':
            #if response == '5':
                
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
        self.client.send_data(self.createJson("", "", ""))
        view = View.View()
        
        # Verificar conexión al Servidor
        time.sleep(1)
        response = self.client.lastData.get("answer", "")
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
