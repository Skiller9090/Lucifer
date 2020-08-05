from socket import socket, AF_INET, SOCK_DGRAM

DEFAULT_SERVER = ('127.0.0.1', 11113) # The default Python3 server.


class Client():
    '''
    Simple client written in Python2. Polls a server and waits for its response.
    '''
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('127.0.0.1', 0)) # OS chooses port
        self.socket_name = self.socket.getsockname()
    
    def poll_server(self, data, server=DEFAULT_SERVER):
        self.socket.sendto(bytes(data), server)
        response, addr = self.socket.recvfrom(1024)
        self.socket.close()
        return response, addr


if __name__ == '__main__':
    test_client = Client()
    print test_client.poll_server("Hello world")