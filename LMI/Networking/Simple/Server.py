from threading import Thread
from LMI.Networking.Simple.Handlers import ClientRecvContinuously
import socket


class SimpleServer:
    def __init__(self, handler=ClientRecvContinuously.handle_client, trackClients=True):
        self.handler = handler
        self.clientThreadList = []
        self.clients = {}
        self.trackClients = trackClients
        self.socketObject = None
        self.serverThread = None

    def _asyncServerLoop(self):
        while True:
            client, addr = self.socketObject.accept()
            clientThread = Thread(target=self.handler, args=(client, addr,
                                                             (self.clients if self.trackClients else None),))
            clientThread.setDaemon(True)
            clientThread.start()
            self.clientThreadList.append(clientThread)

    def createTCPSocket(self, ip, port):
        self.socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketObject.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socketObject.bind((ip, port))
        self.socketObject.listen(100)
        self.socketObject.setblocking(True)
        return True

    def startAsync(self):
        if self.serverThread is not None:
            raise Exception("Server Thread Is Already Running, Kill It First!")
        serverThread = Thread(target=self._asyncServerLoop)
        serverThread.setDaemon(True)
        serverThread.start()
        return serverThread
