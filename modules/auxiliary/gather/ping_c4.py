from modules.Module import BaseModule
from lucifer.Errors import ArgumentUndefinedError
import os


def ping_response(host):
    if "://" in host:
        host = host.split("://")[1]
    response = os.system("ping " + host)
    if response == 0:
        return True
    else:
        return False


class Module(BaseModule):
    def run(self):
        if "hostname" in self.shell.vars.keys():
            hostname = self.shell.vars["hostname"]
        else:
            raise ArgumentUndefinedError("hostname")
        if self.isShellRun:
            print(ping_response(hostname))
        else:
            return ping_response(hostname)

    def set_vars(self):
        new_vars = {
            "hostname": "www.google.com"
        }
        return new_vars

    def get_description(self):
        desc = """Ping a host to check if it is up"""
        return desc
