from modules.Module import BaseModule
from libs.LuciferErrors import IncompatibleSystemError
from subprocess import check_output
import os


def get_uname():
    return check_output(["uname", "-a"]).decode()


class Module(BaseModule):
    def run(self):
        if os.name == "nt":
            raise IncompatibleSystemError("Not Unix")
        if self.isShellRun:
            print(get_uname())
        else:
            return get_uname()
