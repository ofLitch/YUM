import json
import socket
import UDPClient
import View
import rsa
import pickle

# Aux functions
def readInfoServer():
    with open('../infoServer.json', 'r') as file:
        data = json.load(file)
    return [data['ipServer'], data['portServer']]

def getIpPortClient():
    #ipClient = socket.gethostbyname( socket.gethostname() )
    ipClient = "127.0.0.1"
    portClient = 6000
    return [ipClient, portClient]

# JSON
def createJson(method, data):
    jsonData = {
        "method": method,
        "data": data
    }
    jsonString = json.dumps(jsonData)
    return jsonString.encode('utf-8')

def getInfoClient():
    try:
        with open("./infoClient.json", 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error on file infoClient: {e}")
        data = {
            "info": {
                "ip": "NULL",
                "name": "NULL",
                "number": "NULL",
                "timeCreation": "NULL"
            },
            "friends": {},
            "groups": {}
        }
        with open("./infoClient.json", 'rw', 'w') as file:
            json.dump(data, file, indent=4)
    return data

def test():
    print(createJson("is", "da asdsa"))
    
# Function main
if __name__ == "__main__":
    # Read config and info
    ipServer, portServer = readInfoServer()
    ipClient, portClient = getIpPortClient()
    portServer, portClient = int(portServer), int(portClient)
    infoClient = getInfoClient()
    lastData = ""
    client = UDPClient.UDPClient(ipServer, portServer, ipClient, portClient)
    client.start_listening()
    if infoClient['info']['ip'] != "NULL":
        data = createJson("isRegister", infoClient['info']['ip'])
        client.send_data(data)
        
    while client.listening:
        if lastData != client.lastData:
            lastData = client.lastData
            for option in lastData["View"]:
                print(option)
        