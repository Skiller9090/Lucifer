from socket import socket, AF_INET, SOCK_DGRAM

DEFAULT_ADDRESS = ('127.0.0.1', 11113)


class Server():
    '''
    Simple server written in Python3. Waits for a connection on the listening_address.
    '''
    def __init__(self, listening_address=DEFAULT_ADDRESS):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(listening_address)
        print("Server started. Listening on", listening_address)
    
    def listen(self):
        while True:
            data, addr = self.socket.recvfrom(1024)
            response = bytes(self.act_on(data, addr), "utf-8")
            self.socket.sendto(response, addr)
    
    def act_on(self, data, addr):
        print("Connection from", addr)
        return data.upper().decode()


if __name__ == '__main__':
    test_server = Server()
    test_server.listen()