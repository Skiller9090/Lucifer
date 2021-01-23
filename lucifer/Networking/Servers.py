class Servers:
    """
    This class keep track of all server Objects and their IDS.
    """
    def __init__(self):
        """
        Initializes all variables needed for data storage of servers

        nextID stores the next available id to give out to next server instance.
        serverObjects is a dictionary of keys which are ids and values which are serverObjects.
        """
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
