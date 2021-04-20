from modules.Module import BaseModule


class Module(BaseModule):
    def run(self):
        if self.isShellRun:
            print("Module loading and running is working!")
        return True

    def set_vars(self):
        default_vars = {
        }
        return default_vars

    def get_description(self):
        desc = """This module test to see if lucifer's module loading is working."""
        return desc
