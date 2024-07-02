import math
import socket
import os
import json
import threading

def floor(x):
    return math.floor(x)

def nroot(n, x):
    return math.pow(x, 1/n)

def reverse(s):
    return s[::-1]

def validAnagram(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()
    return sorted(str1) == sorted(str2)

def sort(strArr):
    return sorted(strArr)

functionsHashmap = {
    'floor': floor,
    'nroot': nroot,
    'reverse': reverse,
    'validAnagram': validAnagram,
    'sort': sort
}

class SocketServer:
    def __init__(self):
        self.sock = None
        self.server_address = f'./tmp/socket_file'
    
    def create_socket(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        try:
            os.unlink(self.server_address)
        except FileNotFoundError:
            pass

        print('Starting up on {}'.format(self.server_address))

    def bind_socket(self):
        self.sock.bind(self.server_address)
    
    def listen(self):
        self.sock.listen(5)
    
    def accept_connections(self, handlerClass):
        while True:
            connection, client_address = self.sock.accept()
            handler = handlerClass(connection, client_address)
            thread = threading.Thread(target=handler.handle_request)
            thread.start()

class RequestResponseHandler:
    def __init__(self, connection, client_address):
        self.connection = connection
        self.client_address = client_address
    
    def handle_request(self):
        try:
            print('connection from', self.client_address)
            while True:
                byte_data = self.connection.recv(4096)

                if not byte_data:
                    print('no data from', self.client_address)
                    break 

                json_data = byte_data.decode('utf-8')
                print('Received ' + json_data)

                data = json.loads(json_data)

                method = data.get('method')
                params = data.get('params', [])
                id = data.get('id')

                try:
                    if method in functionsHashmap:
                        results = functionsHashmap[method](*params)
                    
                        response = {
                            "results": str(results),
                            "result_type": type(results).__name__,
                            "id": id
                        }
                    else:
                        raise ValueError(f"Method {method} not found")
                except Exception as e:
                    response = {
                        "results": None,
                        "result_type": None,
                        "id": id,
                        "error": str(e)
                    }
                    
                json_response = json.dumps(response)
                self.connection.sendall(json_response.encode('utf-8'))
        finally:
            print("Closing current connection")
            self.connection.close()

if __name__ == "__main__":
    server = SocketServer()
    server.create_socket()
    server.bind_socket()
    server.listen()
    server.accept_connections(RequestResponseHandler)