class Connections:
    def __init__(self):
        self.connections = []

    def add_conn(self, conn):
        self.connections.append(conn)
        return True

    def remove_conn(self, conn):
        if conn in self.connections:
            self.connections.remove(conn)
            return True
        return False
