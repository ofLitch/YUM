import json
import socket
import UDPClient
import View
import rsa
import pickle

class Controller:
    def __init__(self):
        self.ipServer, self.portServer = self.readInfoServer()
        self.ipClient, self.portClient = self.getIpPortClient()
        self.portServer, self.portClient = int(self.portServer), int(self.portClient)
        self.infoClient = self.getInfoClient()
        self.lastData = ""
        self.client = UDPClient.UDPClient(self.ipServer, self.portServer, self.ipClient, self.portClient)

    # Función para leer la información del servidor desde un archivo JSON
    def readInfoServer(self):
        with open('../infoServer.json', 'r') as file:
            data = json.load(file)
        return [data['ipServer'], data['portServer']]

    # Función para obtener la IP y el puerto del cliente
    def getIpPortClient(self):
        # ipClient = socket.gethostbyname(socket.gethostname())
        ipClient = "127.0.0.1"
        portClient = 6000
        return [ipClient, portClient]

    # Función para crear un JSON
    def createJson(self, method, nameData, data):
        jsonData = {
            "method": method,
            nameData: data
        }
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
                "number": "",
                "timeCreation": "",
                "friends": {},
                "groups": {}
            }
            with open("./infoClient.json", 'w') as file:  # Se usa 'w' en lugar de 'rw'
                json.dump(data, file, indent=4)
        return data

    # Método para parsear lastData y devolver un arreglo iterable
    def parse_last_data(self):
        """
        Parses lastData and returns an iterable of key-value pairs.
        
        :return: Iterable of key-value pairs from lastData
        """
        # Verificar si lastData es de tipo bytes y decodificar si es necesario
        if isinstance(self.lastData, bytes):
            self.lastData = self.lastData.decode('utf-8')  # Convertir bytes a string
        
        # Verificar si lastData es un dict y convertirlo a string si es necesario
        if isinstance(self.lastData, dict):
            return self.lastData.items()  # Devuelve los items para ser iterable

        try:
            parsed_data = json.loads(self.lastData)  # Convertir la cadena JSON en un diccionario
            return parsed_data.items()  # Devuelve los items para ser iterable
        except json.JSONDecodeError:
            print("Error al decodificar lastData.")
            return []

    # Método principal que controla la conexión y procesamiento de datos
    def run(self):
        self.client.start_listening()
        
        # Inicializa la vista
        view = View.View()
        
        id = self.infoClient.get("id", "")
        if id == "-1":
            data = self.createJson("register", "", "")
            self.client.send_data(data)
            
            if self.client.lastData.get('answer') == "200 OK":
                while self.client.listening:
                    if self.lastData != self.client.lastData:
                        self.lastData = self.client.lastData
                        # Obtener datos parseados para la vista
                        iterable_data = self.parse_last_data()
                        # Mostrar en la vista
                        view.show(iterable_data)  # Pasar los datos a la vista
            else:
                print("Error en la conexión")
        else:
            print("Cliente ya registrado")


# Ejecución principal
if __name__ == "__main__":
    controller = Controller()
    controller.run()
