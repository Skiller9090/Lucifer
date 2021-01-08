class Servers:
    def __init__(self):
        self.nextID = 0
        self.serverObjects = {}

    def add_server(self, server):
        self.serverObjects[self.nextID] = server
        return True

    def remove_server(self, server):
        if server in self.serverObjects.values():
            key = list(self.serverObjects.keys())[list(self.serverObjects.values()).index(server)]
            del self.serverObjects[key]
            return True
        return False
