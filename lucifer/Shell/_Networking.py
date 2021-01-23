from LMI.Table import generate_table
from lucifer.Utils import check_int


def listServers(self, *args, **kwargs):
    ids = [str(x) for x in self.luciferManager.servers.serverObjects.keys()]
    addresses = [str(x.socketObject.getsockname()) for x in self.luciferManager.servers.serverObjects.values()]
    array = [[_id, addr] for _id, addr in zip(ids, addresses)]
    print(generate_table(array,
                         "Servers",
                         headings=["ID", "Address"]))


def killServer(self, com_args: list):
    _id = com_args[1]
    if check_int(_id):
        if int(_id) in self.luciferManager.servers.serverObjects:
            self.luciferManager.servers.serverObjects[int(_id)].close()
            del self.lucifermanager.servers.serverObjects[int(_id)]
            print(f"Killed Server with id of {_id}")
        else:
            print(f"A server with id of {_id} is not found")
    else:
        print("Error: enter a id as an argument")
