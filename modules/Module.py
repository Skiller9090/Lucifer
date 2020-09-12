from lucifer.Utils import RetrieveShell


class BaseModule(RetrieveShell):
    def __init__(self, luciferManager, ShellRun=False):
        self.luciferManager = luciferManager
        self.actions = []
        self.isShellRun = ShellRun
        self.get_shell()

    def run(self):
        for action in self.actions:
            action()

    def set_vars(self):
        new_vars = {
        }
        return new_vars

    def get_description(self):
        desc = """This Module Has No Description!"""
        return desc
