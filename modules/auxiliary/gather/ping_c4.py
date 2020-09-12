import os
import platform

from lucifer.Errors import ArgumentUndefinedError
from modules.Module import BaseModule
from LMI import Command


class Module(BaseModule):
    def run(self):
        if "hostname" in self.shell.vars.keys():
            hostname = self.shell.vars["hostname"]
        else:
            raise ArgumentUndefinedError("hostname")
        response = self.ping_response(hostname)
        return response

    def set_vars(self):
        new_vars = {
            "hostname": "www.google.com"
        }
        return new_vars

    def get_description(self):
        desc = """Ping a host to check if it is up"""
        return desc

    def ping_response(self, host):
        if "://" in host:
            host = host.split("://")[1]
        command = ["ping"]
        if platform.system() != "Windows":
            command.append("-c")
            command.append("4")
        command.append(host)
        if self.isShellRun:
            response = Command.tee_output(command)
        else:
            response = Command.return_output(command)
        return response
