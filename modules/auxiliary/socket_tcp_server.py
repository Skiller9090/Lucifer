from LMI.Networking.Simple.Handlers import ClientRecvContinuously
from LMI.Networking.Simple.Server import SimpleServer
from modules.Module import BaseModule


class Module(BaseModule):
    def run(self):
        server = SimpleServer(ClientRecvContinuously.handle_client, True)
        server.createTCPSocket("localhost", 1338)
        server.startAsync()
        self.luciferManager.servers.add_server(server)

    def set_vars(self):
        default_vars = {"host": "localhost",
                        "port": "1337",
                        "async": "true"}
        return default_vars

    def get_description(self):
        desc = """Hosts a tcp server constantly receiving data from connections."""
        return desc
