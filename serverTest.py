import json
import socket
import rsa

class UDPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        print(f"UDP Server initialized and listening on {self.host}:{self.port}")

    def listen(self, buffer_size=1024):
        try:
            print("Waiting for messages from clients...")
            while True:
                data, client_address = self.server_socket.recvfrom(buffer_size)
                print(data, client_address)
                ejemResponse = {
                    "View": [
                        "1. Register client",
                        "2. Exit"
                    ]
                }
                jsonString = json.dumps(ejemResponse)
                jsonData = jsonString.encode('utf-8')
                self.server_socket.sendto(jsonData, ('127.0.0.1', 6000))
        except Exception as e:
            print(f"Error while receiving message: {e}")

    def close(self):
        self.server_socket.close()
        print("UDP Server socket closed.")


# Example usage:
if __name__ == "__main__":
    server = UDPServer("127.0.0.1", 12000)
    server.listen()
    server.close()