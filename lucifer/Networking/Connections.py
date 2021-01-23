class Connections:
    """
    This class keeps track of all active connections.
    """
    def __init__(self):
        """
        Creates a connections list to store all 'conn's.
        """
        self.connections = []

    def add_conn(self, conn):
        self.connections.append(conn)
        return True

    def remove_conn(self, conn):
        if conn in self.connections:
            self.connections.remove(conn)
            return True
        return False
