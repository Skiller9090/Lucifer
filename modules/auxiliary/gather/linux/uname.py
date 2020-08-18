from modules.Module import BaseModule
from libs.LuciferErrors import IncompatibleSystemError
from subprocess import check_output
import os


def get_uname(arg):
    arg.insert(0, "uname")
    return check_output(arg).decode()


class Module(BaseModule):
    def run(self):
        args = ["-a"]
        if os.name == "nt":
            raise IncompatibleSystemError("Not Unix")
        if "args" in self.shell.vars.keys():
            args = self.shell.vars["args"].split(" ")
        if self.isShellRun:
            print(get_uname(args))
        else:
            return get_uname(args)

    def set_vars(self):
        new_vars = {
            "args": "-a"
        }
        return new_vars

    def get_description(self):
        desc = """Gets the output of uname on a unix system with any arguments supplied in the args variable"""
        return desc