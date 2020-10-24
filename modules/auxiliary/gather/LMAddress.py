from LMI import OS

from modules.Module import BaseModule


class Module(BaseModule):
    def run(self):
        if self.isShellRun:
            print(OS.getLMAddress())
        else:
            return OS.getLMAddress()

    def set_vars(self):
        new_vars = {}
        return new_vars

    def get_description(self):
        desc = """Returns the memory address of the Lucifer Manager Instance"""
        return desc
